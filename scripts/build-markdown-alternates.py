#!/usr/bin/env python3
"""
Markdown alternate 產生器 —— 給 AI agent 讀的乾淨版本。

## 為什麼要有 .md

AI agent 抓 HTML 時要自己剝掉 nav、footer、inline CSS、i18n bootstrap（20KB）、
chat widget 等雜訊。以 /aeo/what-is-aeo 為例，HTML 34KB 但正文只有約 2.3KB ——
93% 是版面與腳本。.md 直接給正文，抓取成本與誤解機率都低得多。

## 為什麼從 content module 產生而不是從 HTML 剝

26 個 /aeo 頁面的**內容來源是 scripts/aeo_pages_content.py**，HTML 只是它的一種
輸出。從 content module 產生 .md，兩種輸出永遠同源，不會出現「HTML 改了但 .md
忘了改」。

非產生器管理的頁面（what-is-shellfans、aeo-geo）沒有 content module，
其內容來源就是 HTML 本身，因此只能從 HTML 抽取 —— 這種情況會明確標記，
並且只抽 <main> 內的語意元素，不碰版面。

## 索引策略

.md 由 nginx 帶 `X-Robots-Tag: noindex`（見 shell.fans.conf 的 location ~* \\.md$）。
刻意不加 nofollow／noarchive：
  nofollow 會讓 .md 內的連結不被跟隨，失去導流作用
  noarchive 沒有必要，部分 AI 檢索會參考快取
noindex 只影響「是否列入搜尋結果」，不影響 AI 抓取。

HTML 仍然 self-canonical，.md 不參與 canonical 競爭。

用法：
    python3 scripts/build-markdown-alternates.py
    python3 scripts/build-markdown-alternates.py --check
"""

import html as H
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://shell.fans'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aeo_pages_content import PAGES, ORG_NAME  # noqa: E402

LEGAL_NAME = '唄粉智能科技股份有限公司'
BRAND_TW = '唄粉智能科技ShellFans'

# content module 之外、但值得提供 .md 的頁面。內容來源是 HTML 本身。
EXTRA_PAGES = ['what-is-shellfans.html', 'aeo-geo.html']


# ---------------------------------------------------------------------------
# 共用
# ---------------------------------------------------------------------------

def git_last_modified(path):
    """
    取檔案在 git 中的最後修改日。

    用內容的實際修改日而不是 build timestamp —— 後者會讓每次部署都產生
    假的 freshness，AI 看到「今天更新」但內容其實三個月沒動，反而降低可信度。
    不在 git 中（新檔）時回退到檔案 mtime。
    """
    try:
        out = subprocess.run(
            ['git', 'log', '-1', '--format=%cs', '--', path],
            cwd=ROOT, capture_output=True, text=True, timeout=10,
        ).stdout.strip()
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', out):
            return out
    except Exception:
        pass
    import datetime
    try:
        return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()
    except OSError:
        return ''


def footer(canonical, updated, source_note=''):
    lines = [
        '',
        '---',
        '',
        f'**Canonical:** {canonical}',
        f'**Brand:** {ORG_NAME}（{BRAND_TW}）',
        f'**Publisher:** {LEGAL_NAME}（Taiwan, 統一編號 83032387）',
        f'**Last-Updated:** {updated}',
        '',
        f'本檔是 {canonical} 的 Markdown 等價版本，供 AI agent 讀取。'
        'HTML 版為 canonical，本檔不參與搜尋索引。',
    ]
    if source_note:
        lines.append('')
        lines.append(source_note)
    return '\n'.join(lines) + '\n'


# 實際會產生 .md 的頁面集合。由 main() 在產生前填入。
_MD_AVAILABLE: set = set()


def md_link(href, text):
    """
    站內連結優先指向 .md，但**只在該 .md 確實存在時**。

    指向不存在的 .md 會讓 AI agent 拿到 404 —— 那比直接連 HTML 更糟，
    因為它會讓整份 Markdown 的可信度下降。因此以實際產生清單為準，
    不做「看起來像頁面就加 .md」的猜測。
    """
    if href.startswith('/') or href.startswith(SITE):
        path = href.replace(SITE, '')
        if path in _MD_AVAILABLE:
            return f'[{text}]({SITE}{path}.md)'
        return f'[{text}]({SITE}{path})'
    return f'[{text}]({href})'


def inline_html_to_md(s):
    """把內容裡允許的行內 HTML 轉成 Markdown。"""
    s = re.sub(r'<strong>(.*?)</strong>', r'**\1**', s, flags=re.S)
    s = re.sub(r'<b>(.*?)</b>', r'**\1**', s, flags=re.S)
    s = re.sub(r'<em>(.*?)</em>', r'*\1*', s, flags=re.S)
    s = re.sub(r'<code>(.*?)</code>', r'`\1`', s, flags=re.S)
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>',
               lambda m: md_link(m.group(1), re.sub(r'<[^>]+>', '', m.group(2))), s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'[ \t]+', ' ', H.unescape(s)).strip()


# ---------------------------------------------------------------------------
# 由 content module 產生（26 頁）
# ---------------------------------------------------------------------------

def render_block(b):
    kind = b[0]
    if kind == 'p':
        return inline_html_to_md(b[1])
    if kind == 'h3':
        return f'### {inline_html_to_md(b[1])}'
    if kind == 'ul':
        return '\n'.join(f'- {inline_html_to_md(x)}' for x in b[1])
    if kind == 'ol':
        return '\n'.join(f'{i+1}. {inline_html_to_md(x)}' for i, x in enumerate(b[1]))
    if kind == 'note':
        # 註記在 HTML 是 disclaimer 區塊，在 Markdown 用引言表達同等語意
        return '\n'.join('> ' + ln for ln in inline_html_to_md(b[1]).split('\n'))
    if kind == 'table':
        spec = b[1]
        cols = [inline_html_to_md(c) for c in spec['cols']]
        out = []
        if spec.get('caption'):
            out.append(f'*{inline_html_to_md(spec["caption"])}*')
            out.append('')
        out.append('| ' + ' | '.join(cols) + ' |')
        out.append('|' + '|'.join(['---'] * len(cols)) + '|')
        for r in spec['rows']:
            out.append('| ' + ' | '.join(inline_html_to_md(str(c)) for c in r) + ' |')
        return '\n'.join(out)
    raise ValueError(f'未知區塊：{kind}')


def build_from_content(page, updated):
    canonical = SITE + page['url']
    out = [f'# {page["h1"]}', '', inline_html_to_md(page['lede']), '']
    for sec in page['sections']:
        out += [f'## {sec["h2"]}', '']
        for b in sec['blocks']:
            out += [render_block(b), '']
    if page.get('faq'):
        out += ['## 常見問題', '']
        for q, a in page['faq']:
            out += [f'### {q}', '', inline_html_to_md(a), '']
    out += ['## 說明', '', inline_html_to_md(page['disclaimer']), '']
    out += ['## 相關頁面', '']
    out += [f'- {md_link(u, t)}' for u, t in page['related']]
    return '\n'.join(out) + footer(canonical, updated)


# ---------------------------------------------------------------------------
# 由 HTML 抽取（content module 未涵蓋的頁面）
# ---------------------------------------------------------------------------

def build_from_html(path, updated):
    src = open(os.path.join(ROOT, path), encoding='utf-8').read()
    m = re.search(r'<main.*?</main>', src, re.S)
    body = m.group(0) if m else src
    canonical_m = re.search(r'rel="canonical" href="([^"]+)"', src)
    canonical = canonical_m.group(1) if canonical_m else SITE + '/' + path.replace('.html', '')

    # 只取語意元素，不碰版面。順序保留原文順序。
    out = []
    pattern = re.compile(
        r'<(h1|h2|h3|p|li|summary|caption)[^>]*>(.*?)</\1>|<(details)[^>]*>', re.S)
    seen_h1 = False
    for mm in pattern.finditer(body):
        tag, inner = mm.group(1), mm.group(2)
        if tag is None:
            continue
        txt = inline_html_to_md(inner)
        if not txt:
            continue
        if tag == 'h1':
            if seen_h1:
                continue
            seen_h1 = True
            out += [f'# {txt}', '']
        elif tag == 'h2':
            out += ['', f'## {txt}', '']
        elif tag == 'h3':
            out += ['', f'### {txt}', '']
        elif tag == 'summary':
            out += ['', f'### {txt}', '']
        elif tag == 'li':
            out.append(f'- {txt}')
        elif tag == 'caption':
            out += [f'*{txt}*', '']
        else:
            out += [txt, '']
    note = ('> 本檔由 HTML 頁面抽取產生（該頁未使用內容模組）。'
            '若與 HTML 有出入，以 canonical HTML 為準。')
    return '\n'.join(out).strip() + '\n' + footer(canonical, updated, note)


# ---------------------------------------------------------------------------

def main():
    check = '--check' in sys.argv
    written = []

    # 先算出哪些頁面會有 .md，md_link 才能只連向真的存在的檔案
    _MD_AVAILABLE.update(p['url'] for p in PAGES)
    _MD_AVAILABLE.update('/' + e.replace('.html', '') for e in EXTRA_PAGES)

    for page in PAGES:
        rel = page['url'].lstrip('/') + '.html'
        updated = git_last_modified(os.path.join(ROOT, 'scripts', 'aeo_pages_content.py'))
        md = build_from_content(page, updated)
        out_path = os.path.join(ROOT, page['url'].lstrip('/') + '.md')
        if not check:
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            open(out_path, 'w', encoding='utf-8').write(md)
        written.append((page['url'] + '.md', len(md), 'content-module'))

    for rel in EXTRA_PAGES:
        updated = git_last_modified(os.path.join(ROOT, rel))
        md = build_from_html(rel, updated)
        out_path = os.path.join(ROOT, rel.replace('.html', '.md'))
        if not check:
            open(out_path, 'w', encoding='utf-8').write(md)
        written.append(('/' + rel.replace('.html', '.md'), len(md), 'html-extract'))

    # 產出即驗證：不得殘留 HTML 標籤或版面殘骸
    for url, _, _ in written:
        p = os.path.join(ROOT, url.lstrip('/'))
        if check and not os.path.exists(p):
            continue
        txt = open(p, encoding='utf-8').read()
        for bad in ['<script', '<nav', '<footer', '<header', '<style', 'sf-footer', 'data-i18n']:
            if bad in txt:
                raise SystemExit(f'{url} 殘留版面元素：{bad}')

    print(f'{"已驗證" if check else "已產生"} {len(written)} 份 Markdown')
    for u, n, src in written:
        print(f'  {u:<40} {n/1024:>6.1f} KB  ({src})')


if __name__ == '__main__':
    main()
