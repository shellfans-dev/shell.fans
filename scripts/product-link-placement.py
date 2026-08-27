#!/usr/bin/env python3
"""
確保 /product 的入口在 footer 的「產品」分組，而不在主導覽。冪等。

## 為什麼從 nav 移到 footer

2026-08-26 曾把「產品服務」放進主導覽第一順位，解決 /product 是 orphan 的
問題。但主導覽的其他項目是 AEO/GEO 代管、續航引擎、粉絲分析、口碑行銷——
每一個都是具體服務。「產品服務」擺在同一排，讀起來像是第五個服務，
和後面四個在敘述上重複，反而讓導覽變得難以解讀。

footer 的「產品」分組本來就是「一組產品連結」的語意容器，總覽放在該組
第一個位置不會產生同樣的歧義。

## 這不會讓 /product 變回 orphan

footer 出現在全部 49 頁，inbound 連結數與放在 nav 時相同。差別只在版面
位置與語意脈絡，不在可達性。

## 三個渲染來源

  1. 各頁靜態烘焙的 footer HTML  ← 本腳本處理。無 JS 的訪客與 AI 爬蟲
                                    看到的就是這一份，對 AEO 而言最重要
  2. js/sf-footer.js 的 SHELL_BASE ← 本腳本處理。API 斷線時的 fallback
  3. console.shell.fans/api/site/footer ← 本腳本**不會**改動。
                                    有 JS 的一般訪客實際看到的是這一份，
                                    需要在後台（UIUX Design → Footer）另外設定

/aeo 那 26 頁的 nav 來自 donor（aeo-geo/methodology.html），本腳本改到
donor 之後重跑 build-aeo-pages.py 即同步。

本腳本取代先前的 add-product-nav.py（已刪除）——留著一支會把連結加回
主導覽的腳本，日後必定有人誤跑。

用法：python3 scripts/product-link-placement.py [--check]
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HREF = 'https://shell.fans/product'
FOOTER_GROUP = '<div class="sf-footer-col"><h3>產品</h3>'
FOOTER_LINK = f'<a href="{HREF}">產品服務</a>'

NAV_CONTAINER = re.compile(
    r'<nav\b[^>]*class="[^"]*\bnav-menu\b[^"]*"[^>]*>'
    r'|<div\b[^>]*class="[^"]*\bmobile-menu\b[^"]*"[^>]*>')


def strip_from_nav(html):
    """從 nav 容器中移除 /product 連結，連同其後的分隔符。"""
    total = 0
    while True:
        removed = False
        for m in NAV_CONTAINER.finditer(html):
            start = m.end()
            close = '</nav>' if m.group(0).startswith('<nav') else '</div>'
            end = html.find(close, start)
            if end < 0:
                continue
            seg = html[start:end]
            # 連結本體 + 其後可能的分隔符（　·　 / ' · ' / 空白）
            link = re.search(
                r'<a\b[^>]*href="' + re.escape(HREF) + r'"[^>]*>.*?</a>\s*(?:　·　|\s·\s)?',
                seg, re.S)
            if not link:
                continue
            html = html[:start + link.start()] + html[start + link.end():]
            total += 1
            removed = True
            break
        if not removed:
            return html, total


def strip_dict_keys(html):
    """移除 nav.product 的 i18n 字典項（兩個語系）。"""
    out, n = re.subn(r"'nav\.product'\s*:\s*'(?:[^'\\]|\\.)*',\s*", '', html)
    return out, n


def add_to_footer(html):
    """把 /product 放進 footer「產品」分組的第一個位置。"""
    if FOOTER_GROUP not in html:
        return html, 0
    idx = html.find(FOOTER_GROUP)
    end = html.find('</div>', idx)
    if HREF in html[idx:end]:
        return html, 0                                   # 冪等
    at = idx + len(FOOTER_GROUP)
    return html[:at] + FOOTER_LINK + html[at:], 1


def main():
    check = '--check' in sys.argv
    rows = []

    for rel in sorted(glob.glob('**/*.html', recursive=True, root_dir=ROOT)):
        if rel.startswith('.git'):
            continue
        path = os.path.join(ROOT, rel)
        src = open(path, encoding='utf-8').read()

        out, n_nav = strip_from_nav(src)
        out, n_dict = strip_dict_keys(out) if n_nav or "'nav.product'" in out else (out, 0)
        out, n_ft = add_to_footer(out)

        if not (n_nav or n_dict or n_ft):
            continue

        # 產出即驗證
        for m in NAV_CONTAINER.finditer(out):
            start = m.end()
            close = '</nav>' if m.group(0).startswith('<nav') else '</div>'
            end = out.find(close, start)
            if end > 0 and HREF in out[start:end]:
                raise SystemExit(f'{rel}：nav 內仍殘留 /product')
        if "'nav.product'" in out:
            raise SystemExit(f'{rel}：字典仍殘留 nav.product')
        if FOOTER_GROUP in out:
            i = out.find(FOOTER_GROUP)
            if out[i:out.find('</div>', i)].count(HREF) != 1:
                raise SystemExit(f'{rel}：footer 產品分組的 /product 數量不是 1')
        # 用相對不變量而非絕對配對：index.html 原本就有一個未配對的 <a>
        # （既有狀況，非本次造成）。這裡要保證的是「我沒有讓它更糟」，
        # 也就是開合標籤的差值不變。
        def imbalance(h):
            return len(re.findall(r'<a\b', h)) - h.count('</a>')
        if imbalance(out) != imbalance(src):
            raise SystemExit(
                f'{rel}：a 標籤配對被改變（{imbalance(src)} → {imbalance(out)}）')

        if not check:
            open(path, 'w', encoding='utf-8').write(out)
        rows.append((rel, n_nav, n_dict, n_ft))

    print(f'{"待處理" if check else "已處理"} {len(rows)} 頁　'
          f'nav 移除 {sum(r[1] for r in rows)}　'
          f'字典 {sum(r[2] for r in rows)}　'
          f'footer 新增 {sum(r[3] for r in rows)}')
    for rel, a, b, c in rows[:5]:
        print(f'  {rel:<36} nav-{a}  dict-{b}  footer+{c}')
    if len(rows) > 5:
        print(f'  …其餘 {len(rows) - 5} 頁')


if __name__ == '__main__':
    main()
