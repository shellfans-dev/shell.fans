#!/usr/bin/env python3
"""
AEO 知識叢集頁面產生器。

## 為什麼需要這支腳本

shell.fans 是純靜態站，每頁的 nav、footer、CSS 都各自內嵌。手工複製 23 個新頁
等於把同一份 nav 複製 23 份——之後任何一次 nav 改版都會漏掉幾頁，而漏掉的那幾頁
不會報錯，只會安靜地長得不一樣。

因此改成：外殼從既有頁面「抽取」而非「複製貼上」。donor 改版後重跑本腳本，
23 頁一起跟上。這也是既有 scripts/*.py 冪等修補器的一貫作法。

## 外殼來源

donor = aeo-geo/methodology.html —— 既有 AEO 叢集中結構最接近文章頁的一頁。
取用：<style>、<header class="nav">、<footer>、nav 行為 script。

抽取時做兩件事：

1. **移除 data-i18n / data-i18n-attr**
   donor 是全站 7 個雙語頁之一，語系切換靠一段 20KB 的 i18n bootstrap。
   新頁是中文頁，不載入該引擎；若保留 data-i18n，sf-footer.js 的 texts() 會
   誤判本頁支援雙語，把登入鈕切成英文，出現「整頁中文、一顆英文按鈕」。
   移除後產品開關仍然有效 —— sf-footer.js 對舊版 nav 有文字比對的 fallback。

2. **移除語言切換器**
   它的行為綁在沒有一起載入的 lang-switcher script 上，留著就是一顆死按鈕。

用法：
    python3 scripts/build-aeo-pages.py            # 產生全部頁面
    python3 scripts/build-aeo-pages.py --check    # 只驗證，不寫檔
"""

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONOR = os.path.join(ROOT, 'aeo-geo', 'methodology.html')
SITE = 'https://shell.fans'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aeo_pages_content import PAGES, ORG_NAME, ORG_LOGO  # noqa: E402

# 法人名稱。署名列要同時帶品牌名與法人名，AI 才能把兩者連到同一個實體。
LEGAL_NAME = '唄粉智能科技股份有限公司'


# ---------------------------------------------------------------------------
# 外殼抽取
# ---------------------------------------------------------------------------

def slice_between(text, start_marker, end_marker):
    i = text.index(start_marker)
    j = text.index(end_marker, i) + len(end_marker)
    return text[i:j]


def remove_balanced(markup, open_pattern, tag='div'):
    """
    移除一個標籤與其配對的結束標籤（含巢狀內容）。

    不用 regex —— 巢狀 <div> 沒辦法用 regex 正確配對，而錯誤的配對會把後面
    半個 nav 一起吃掉，且產出的 HTML 仍然「看起來像對的」。
    """
    m = re.search(open_pattern, markup)
    if not m:
        return markup
    start = m.start()
    depth = 0
    pos = start
    token = re.compile(r'<(/?)%s\b' % tag)
    while True:
        t = token.search(markup, pos)
        if not t:
            raise ValueError('找不到配對的結束標籤：%s' % open_pattern)
        if t.group(1) == '/':
            depth -= 1
            if depth == 0:
                end = markup.index('>', t.end()) + 1
                return markup[:start] + markup[end:]
        else:
            depth += 1
        pos = t.end()


def extract_shell():
    src = open(DONOR, encoding='utf-8').read()

    style = slice_between(src, '<style>', '</style>')
    nav = slice_between(src, '<header class="nav"', '</header>')
    mobile = slice_between(src, '<div class="mobile-menu"', '</div>')
    footer = slice_between(src, '<footer class="sf-footer"', '</footer>')

    # nav 行為 script（scroll / 登入下拉 / 漢堡選單）
    tail = src[src.index('</footer>'):]
    blocks = re.findall(r'<script([^>]*)>(.*?)</script>', tail, re.S)
    nav_script = None
    for attrs, body in blocks:
        if "getElementById('nav')" in body and 'navHamburger' in body:
            nav_script = body
            break
    if nav_script is None:
        raise SystemExit('donor 中找不到 nav 行為 script —— donor 結構可能已改變')

    nav = remove_balanced(nav, r'<div class="lang-switcher"', 'div')
    nav = re.sub(r'\s+data-i18n(?:-attr|-html)?="[^"]*"', '', nav)
    nav = re.sub(r'\s+data-i18n(?:-attr|-html)?(?=[\s>])', '', nav)
    mobile = re.sub(r'\s+data-i18n(?:-attr|-html)?="[^"]*"', '', mobile)
    mobile = re.sub(r'\s+data-i18n(?:-attr|-html)?(?=[\s>])', '', mobile)

    if 'data-i18n' in nav or 'data-i18n' in mobile:
        raise SystemExit('data-i18n 未清乾淨 —— 會讓登入鈕在中文頁變英文')
    if 'langSwitcher' in nav:
        raise SystemExit('語言切換器未移除 —— 會留下一顆沒有行為的死按鈕')

    return {'style': style, 'nav': nav, 'mobile': mobile,
            'footer': footer, 'nav_script': nav_script}


# ---------------------------------------------------------------------------
# 內容渲染
# ---------------------------------------------------------------------------

def esc(s):
    return html.escape(str(s), quote=True)


def render_table(spec):
    head = ''.join('<th scope="col">%s</th>' % c for c in spec['cols'])
    rows = []
    for r in spec['rows']:
        cells = '<th scope="row">%s</th>' % r[0]
        cells += ''.join('<td>%s</td>' % c for c in r[1:])
        rows.append('<tr>%s</tr>' % cells)
    cap = '<caption>%s</caption>' % esc(spec['caption']) if spec.get('caption') else ''
    return ('<div class="sf-table-wrap"><table class="sf-dim-table">%s'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            % (cap, head, ''.join(rows)))


def render_block(b):
    kind = b[0]
    if kind == 'p':
        return '<p>%s</p>' % b[1]
    if kind == 'h3':
        return '<h3>%s</h3>' % esc(b[1])
    if kind == 'ul':
        return '<ul>%s</ul>' % ''.join('<li>%s</li>' % x for x in b[1])
    if kind == 'ol':
        return '<ol>%s</ol>' % ''.join('<li>%s</li>' % x for x in b[1])
    if kind == 'table':
        return render_table(b[1])
    if kind == 'note':
        return '<div class="disclaimer"><p>%s</p></div>' % b[1]
    raise ValueError('未知的內容區塊型別：%s' % kind)


def content_last_modified(source_rel='scripts/aeo_pages_content.py'):
    """
    指定內容來源檔在 git 中的最後修改日。

    source_rel 必須指向**該頁內容實際所在的檔案**。/aeo 那 26 頁的內容在
    aeo_pages_content.py，但 /about 與 /developers 的內容在各自的
    build-*-page.py 裡——若一律用 aeo_pages_content.py 的日期，那兩頁會顯示
    一個與自身內容無關的更新日。署名列的更新日若不準，比不顯示更糟。

    用內容的實際修改日而不是 build timestamp——後者會讓每次部署都產生假的
    freshness，AI 看到「今天更新」但內容其實三個月沒動，反而降低可信度。
    與 build-markdown-alternates.py 的 git_last_modified() 同一套邏輯。
    """
    import datetime
    import subprocess
    path = os.path.join(ROOT, source_rel)
    try:
        out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', path],
                             cwd=ROOT, capture_output=True, text=True, timeout=10).stdout.strip()
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', out):
            return out
    except Exception:
        pass
    try:
        return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()
    except OSError:
        return ''


BYLINE_STYLE = ('font-size:0.85rem;line-height:1.9;color:var(--text-secondary);'
                'margin:-16px 0 28px;max-width:780px')


def render_byline(updated):
    """
    署名列 —— 放在 H1 與導言之間。

    ## 為什麼一定要在這個位置

    2026-09-02 的能見度探測：unbranded 品牌提及率 0%（0/36），但官方引用率
    3%——AI **已經在讀也在引用**這些頁面，只是不知道是誰寫的。

    實測被 Claude 引用的 /aeo/gptbot-oai-searchbot：正文 1419 字，「ShellFans」
    只出現 1 次，在 88% 處的免責聲明裡。AI 擷取答案看的是前段，那個區間完全
    沒有實體訊號，因此它有內容可用、有網址可引，卻沒有任何文字依據能說出
    「根據 ShellFans」。其餘技術頁同樣：what-is-aeo 91%、implementation 89%。

    JSON-LD 的 author/publisher 早就有了，但那是給搜尋引擎建索引用的；
    生成式回答是從**可見文字**組出來的，結構化資料不會自動變成句子。

    ## 為什麼不用長版宣傳句

    刻意只寫「整理者＋法人名＋更新日」，不列服務項目。每頁都塞一段服務介紹
    會變成樣板噪音，對讀者沒有價值，也容易被判為填充內容。需要的只是讓
    「這份內容屬於誰」出現在可擷取的位置一次。

    同時滿足 answer-first 對「應顯示更新日與發布者」的要求。
    """
    parts = ['整理者：<strong>%s</strong>（%s）' % (ORG_NAME, LEGAL_NAME)]
    if updated:
        parts.append('更新於 %s' % updated)
    return '      <p class="page-byline" style="%s">%s</p>' % (BYLINE_STYLE, '　·　'.join(parts))


def render_main(page):
    out = ['<main style="padding-top:72px">', '',
           '  <section class="hero">', '    <div class="container">',
           '      <span class="hero-eyebrow">%s</span>' % esc(page['eyebrow']),
           '      <h1>%s</h1>' % esc(page['h1']),
           '      <p class="hero-lead">%s</p>' % page['lede'],
           render_byline(content_last_modified(
               page.get('content_source', 'scripts/aeo_pages_content.py'))),
           '      <div class="hero-cta">',
           '        <a href="%s%s" class="btn-primary">%s</a>'
           % (SITE, page['cta']['href'], esc(page['cta']['label'])),
           '        <a href="%s%s" class="btn-secondary">%s</a>'
           % (SITE, page['cta2']['href'], esc(page['cta2']['label'])),
           '      </div>', '    </div>', '  </section>', '']

    for sec in page['sections']:
        # sec['id'] 讓區段可被片段網址錨定（例如 /developers#auth）。
        # 沒有 id 的區段維持原樣，不影響既有頁面。
        _sid = (' id="%s"' % esc(sec['id'])) if sec.get('id') else ''
        out += ['  <section%s>' % _sid, '    <div class="container">',
                '      <span class="section-eyebrow">%s</span>' % esc(sec['eyebrow']),
                '      <h2>%s</h2>' % esc(sec['h2'])]
        for b in sec['blocks']:
            out.append('      ' + render_block(b))
        out += ['    </div>', '  </section>', '']

    if page.get('faq'):
        out += ['  <section>', '    <div class="container">',
                '      <span class="section-eyebrow">FAQ</span>',
                '      <h2>常見問題</h2>',
                '      <div class="faq" style="margin-top:32px">']
        for q, a in page['faq']:
            # 問句包成 h3：折疊狀態下 <summary> 的文字不是標題，整個 FAQ 區
            # 在文件大綱裡會是「一個 H2 底下什麼都沒有」。inline style 把 h3
            # 的預設樣式中和成與裸文字節點相同，外觀不變。
            out.append(
                '        <details><summary><h3 style="display:inline;font:inherit;'
                'margin:0;padding:0;color:inherit">%s</h3></summary><p>%s</p></details>'
                % (esc(q), a))
        out += ['      </div>', '    </div>', '  </section>', '']

    out += ['  <section>', '    <div class="container">',
            '      <div class="disclaimer"><p>%s</p></div>' % page['disclaimer'],
            '      <p class="sf-inline-links">相關頁面：%s</p>'
            % '　·　'.join('<a href="%s%s">%s</a>' % (SITE, u, esc(t)) for u, t in page['related']),
            '    </div>', '  </section>', '', '</main>']
    return '\n'.join(out)


# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------

#
# Organization 節點與首頁 index.html 的宣告逐欄一致。
#
# 這不是複製貼上的懶惰，而是刻意的：/aeo/entity-clarity 那頁自己寫的原則就是
# 「名稱、logo、地址應該完全相同，不一致會直接削弱實體訊號」。若知識中心宣稱
# 這件事、自己卻寫成另一個版本，就是最糟的示範。改動時兩邊必須同步。
#
ORGANIZATION_NODE = {
    '@type': 'Organization',
    '@id': SITE + '/#organization',
    # name 用品牌名而非法人中文名 —— 2026-08-19 的稽核發現 OpenAI 查「唄粉智能科技」
    # 完全找不到，還推薦了一堆粉體物料處理公司（把「粉」當成粉末）。
    # 法人名放 legalName，各種寫法放 alternateName，讓實體收斂到同一個節點。
    'name': 'ShellFans AI Technology',
    # 「唄粉智能科技ShellFans」是刻意的合併寫法：台灣使用者用中文搜尋，
    # 而 AI 查「唄粉智能科技」時曾誤判為粉體產業。把中英文綁在同一個字串裡，
    # 等於在實體層直接建立兩者的關聯，比分開列更明確。
    'alternateName': ['ShellFans', 'ShellFans AI', '唄粉智能科技ShellFans',
                      '唄粉智能科技股份有限公司', '唄粉智能科技', 'shell.fans'],
    'legalName': '唄粉智能科技股份有限公司',
    'url': SITE,
    'logo': ORG_LOGO,
    # 第三方身分來源（社群平台）排在自有子網域之前 —— 前者才是可獨立驗證的實體佐證。
    # LinkedIn 於 2026-08-25 補上：稽核發現它實測 200 但全站完全沒有連結，
    # 而那是 B2B 場景中最重要的公司身分來源。
    'sameAs': [
        'https://www.facebook.com/profile.php?id=61581243232686',
        'https://www.instagram.com/shell_fansai/',
        'https://www.linkedin.com/company/shellfans/',
        'https://console.shell.fans',
        'https://blog.shell.fans',
    ],
    'taxID': '83032387',
    # 2026-08-26 補：Is Agentic 稽核把 Organization schema 判為 Partial，
    # 缺的正是 address 與 contactPoint。這兩個欄位是 agent 做實體解析時的
    # 對照依據 —— 要確認「網路上這個 ShellFans」與「台灣某家登記在案的公司」
    # 是同一個實體，靠的就是地址、統編、聯絡管道能不能跟第三方紀錄對上。
    # 全部取自 footer 既有的公開資訊，電話只是轉成 E.164 國際格式。
    'foundingDate': '2023-03',   # /co-founder 沿革：2023/03 創辦唄粉智能科技
    'address': {
        '@type': 'PostalAddress',
        'streetAddress': '瑞光路335號4樓',
        'addressLocality': '內湖區',
        'addressRegion': '臺北市',
        'addressCountry': 'TW',
    },
    'contactPoint': [{
        '@type': 'ContactPoint',
        'contactType': 'customer support',
        'email': 'hello@shell.fans',
        'telephone': '+886-2-7714-3635',
        'areaServed': 'TW',
        'availableLanguage': ['zh-Hant', 'en'],
    }],
}


def build_jsonld(page):
    url = SITE + page['url']
    graph = [dict(ORGANIZATION_NODE)]

    node = {
        '@type': page['schema'],
        '@id': url + '#main',
        'headline': page['h1'],
        'name': page['h1'],
        'description': page['desc'],
        'url': url,
        'inLanguage': 'zh-Hant',
        'isPartOf': {'@type': 'WebSite', 'name': ORG_NAME, 'url': SITE},
        # 指向 @graph 中的 Organization 節點，而不是再宣告一份內嵌的。
        # 重複宣告同一個實體是 entity clarity 的典型反例。
        'author': {'@id': SITE + '/#organization'},
        'publisher': {'@id': SITE + '/#organization'},
    }
    if page['schema'] == 'Service':
        # Service 沒有 headline/author 語意，改用 provider + areaServed
        for k in ('headline', 'author', 'publisher', 'isPartOf'):
            node.pop(k, None)
        node['provider'] = {'@id': SITE + '/#organization'}
        node['areaServed'] = {'@type': 'Country', 'name': 'Taiwan'}
        node['serviceType'] = page.get('service_type', 'Answer Engine Optimization')
    elif page['schema'] == 'CollectionPage':
        node.pop('headline', None)
    if page.get('disclaimer_short'):
        node['disclaimer'] = page['disclaimer_short']
    graph.append(node)

    crumbs = [('首頁', '/')] + page['breadcrumb'] + [(page['h1'], page['url'])]
    graph.append({
        '@type': 'BreadcrumbList',
        '@id': url + '#breadcrumb',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + u}
            for i, (n, u) in enumerate(crumbs)
        ],
    })

    if page.get('faq'):
        graph.append({
            '@type': 'FAQPage',
            '@id': url + '#faq',
            'mainEntity': [
                {'@type': 'Question', 'name': q,
                 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'<[^>]+>', '', a)}}
                for q, a in page['faq']
            ],
        })

    return json.dumps({'@context': 'https://schema.org', '@graph': graph},
                      ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# 組頁
# ---------------------------------------------------------------------------

HEAD_TMPL = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#101214">
<link rel="canonical" href="{url}">

<link rel="alternate" hreflang="zh-Hant" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">

<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:site_name" content="ShellFans AI Technology">
<meta property="og:image" content="{logo}">
<meta property="og:locale" content="zh_TW">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{logo}">

<!-- AI agent discovery：llms.txt 是站台層的導覽檔，.md 是本頁的乾淨版本。
     兩者都不影響 canonical —— HTML 仍是唯一 canonical。 -->
<link rel="describedby" href="https://shell.fans/llms.txt">
<link rel="alternate" type="text/markdown" href="{url}.md" title="Markdown version for AI agents">

<link rel="icon" href="https://shell.fans/images/favicon.png">
<link rel="apple-touch-icon" href="https://shell.fans/images/webclip.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700&family=Noto+Serif+TC:wght@600;700&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">

<script type="application/ld+json">
{jsonld}
</script>

{style}
  <link rel="stylesheet" href="/css/sf-footer.css">
</head>
<body>

<!-- ===== NAV ===== -->
{nav}
{mobile}

{main}

<!-- ===== FOOTER ===== -->
{footer}

<script>
{nav_script}
</script>
<script src="/js/sf-footer.js?v=20260729a" defer></script>
<script src="https://shell.fans/js/aeo-chat.js" defer></script>
</body>
</html>
"""


def build_page(page, shell):
    return HEAD_TMPL.format(
        title=esc(page['title']), desc=esc(page['desc']),
        url=SITE + page['url'], logo=ORG_LOGO,
        jsonld=build_jsonld(page), style=shell['style'],
        nav=shell['nav'], mobile=shell['mobile'], footer=shell['footer'],
        nav_script=shell['nav_script'], main=render_main(page),
    )


def main():
    check_only = '--check' in sys.argv
    shell = extract_shell()

    seen = set()
    written = []
    for page in PAGES:
        if page['url'] in seen:
            raise SystemExit('URL 重複：%s' % page['url'])
        seen.add(page['url'])

        markup = build_page(page, shell)

        # 產出即驗證：JSON-LD 必須可 parse，H1 必須恰好一個
        for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', markup, re.S):
            json.loads(m)
        if markup.count('<h1>') != 1:
            raise SystemExit('%s 的 H1 數量為 %d，必須恰好 1 個' % (page['url'], markup.count('<h1>')))

        path = os.path.join(ROOT, page['url'].lstrip('/') + '.html')
        if not check_only:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(markup)
        written.append((page['url'], len(markup)))

    print('%s %d 頁' % ('已驗證' if check_only else '已產生', len(written)))
    for u, n in written:
        print('  %-38s %6.1f KB' % (u, n / 1024))


if __name__ == '__main__':
    main()
