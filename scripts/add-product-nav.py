#!/usr/bin/env python3
"""
把「產品服務」（/product）加進全站主選單的第一個位置。冪等，可重複執行。

## 為什麼要有這支腳本

shell.fans 是純靜態站，48 個頁面各自內嵌一份 nav。手動改 48 次必然漏頁，
而漏掉的那幾頁「看起來仍然是對的」——只有從那一頁進站的訪客會發現少一個入口。
插入邏輯集中在這裡，不散在各檔案。

## 三種 nav 形式

  桌面（手寫頁）   <a href="…" class="nav-link" …>
  桌面（Webflow）  <a href="…" class="nav-link w-nav-link" …>
  行動版           <a href="…" …>          （在 <div class="mobile-menu">，無 class）

Webflow 頁的 nav 之間有 <div class="footer-line-2 chose"></div> 分隔線，
但該 class 的 CSS 是 display:none（css/shellfans-v2.webflow.css:4362），
實際不顯示，因此新連結不補分隔線——與稍早加入的「AEO/GEO 代管」一致。

## 刻意不加 data-sf-product

data-sf-product 是給 Cloudflare Worker 依產品服務開關在 edge 移除 nav 項目用的
（見 scripts/mark-product-nav.py）。/product 是「所有產品線的總覽」，不隸屬任何
單一產品——若標上任一產品的 key，該產品一關掉，總覽入口就跟著消失，而總覽頁本身
仍然存在且仍在 sitemap 裡，等於製造一個新的 orphan。

## i18n

全站 7 個雙語頁有 inline i18n bootstrap，applyTranslations() 在 DOMContentLoaded
無條件執行——只改 HTML 不補字典的話，文字會在載入後被清空。因此只在「該頁確實有
i18n 引擎」時才掛 data-i18n，並同時補 zh-TW 與 en 兩份字典。

## /aeo 那 26 頁

它們的 nav 由 build-aeo-pages.py 從 donor（aeo-geo/methodology.html）抽取。
本腳本會一併改到它們，但真正的來源是 donor——donor 改完後重跑產生器即可保持同步。

用法：
    python3 scripts/add-product-nav.py [--check]
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HREF = 'https://shell.fans/product'
I18N_KEY = 'nav.product'
LABEL_ZH = '產品服務'
LABEL_EN = 'Products'

# 插在這個連結之前 —— 目前主選單的第一項
FIRST_ITEM = 'nav.aeoGeo'          # i18n 頁用 data-i18n 定位
FIRST_TEXT = 'AEO/GEO 代管'        # 非 i18n 頁用文字定位


def has_i18n_engine(src):
    """該頁是否有 inline i18n bootstrap。只看字典是否存在，不看個別 data-i18n。"""
    return "'nav.aeoGeo':" in src or '"nav.aeoGeo":' in src


def anchor(class_attr, i18n, current=False):
    cls = class_attr
    if current and cls:
        cls += ' w--current'
    parts = [f'href="{HREF}"']
    if cls:
        parts.append(f'class="{cls}"')
    if i18n:
        parts.append(f'data-i18n="{I18N_KEY}"')
    return f'<a {" ".join(parts)}>{LABEL_ZH}</a>'


def insert_navs(src, is_product_page, i18n):
    """在三種 nav 的第一項之前插入連結。回傳 (新內容, 插入次數)。"""
    n = 0
    out = []
    pos = 0
    # 逐個 nav 容器處理，避免把內文中恰好等於 FIRST_TEXT 的連結誤判成 nav
    container = re.compile(
        r'<nav\b[^>]*class="[^"]*\bnav-menu\b[^"]*"[^>]*>|<div\b[^>]*class="[^"]*\bmobile-menu\b[^"]*"[^>]*>')
    for m in container.finditer(src):
        start = m.end()
        end = src.find('</nav>' if m.group(0).startswith('<nav') else '</div>', start)
        if end < 0:
            continue
        seg = src[start:end]
        if f'href="{HREF}"' in seg:
            continue                                    # 冪等
        is_mobile = 'mobile-menu' in m.group(0)
        # 找該 nav 的第一項
        if i18n:
            am = re.search(r'<a\b[^>]*data-i18n="' + re.escape(FIRST_ITEM) + r'"', seg)
        else:
            am = re.search(r'<a\b[^>]*>\s*' + re.escape(FIRST_TEXT) + r'\s*</a>', seg)
        if not am:
            continue
        cls = '' if is_mobile else ('nav-link w-nav-link' if 'w-nav-link' in seg else 'nav-link')
        link = anchor(cls, i18n, current=is_product_page and not is_mobile)
        sep = '\n        ' if not is_mobile else '\n    '
        out.append(src[pos:start + am.start()])
        out.append(link + sep)
        pos = start + am.start()
        n += 1
    out.append(src[pos:])
    return ''.join(out), n


def insert_dict(src):
    """在 zh-TW 與 en 兩份字典的 nav.aeoGeo 之前插入 nav.product。"""
    if f"'{I18N_KEY}'" in src:
        return src, 0
    n = 0
    out = []
    pos = 0
    for i, m in enumerate(re.finditer(r"'nav\.aeoGeo'\s*:", src)):
        val = LABEL_ZH if i == 0 else LABEL_EN
        out.append(src[pos:m.start()])
        out.append(f"'{I18N_KEY}': '{val}',")
        pos = m.start()
        n += 1
    out.append(src[pos:])
    return ''.join(out), n


def main():
    check = '--check' in sys.argv
    touched, skipped = [], []

    for rel in sorted(glob.glob('**/*.html', recursive=True, root_dir=ROOT)):
        if rel.startswith('.git'):
            continue
        path = os.path.join(ROOT, rel)
        src = open(path, encoding='utf-8').read()
        if 'nav-menu' not in src and 'mobile-menu' not in src:
            continue

        i18n = has_i18n_engine(src)
        out, n_nav = insert_navs(src, rel == 'product.html', i18n)
        n_dict = 0
        if i18n:
            out, n_dict = insert_dict(out)

        if n_nav == 0 and n_dict == 0:
            continue
        if i18n and n_nav and n_dict == 0 and f"'{I18N_KEY}'" not in out:
            # 掛了 data-i18n 卻沒有字典 → 文字會被清空，寧可不改
            skipped.append((rel, '有 i18n 引擎但找不到字典插入點'))
            continue
        if not check:
            open(path, 'w', encoding='utf-8').write(out)
        touched.append((rel, n_nav, n_dict, 'i18n' if i18n else '純文字'))

    print(f'{"待處理" if check else "已處理"} {len(touched)} 頁')
    for rel, n_nav, n_dict, kind in touched:
        print(f'  {rel:<40} nav×{n_nav}  字典×{n_dict}  ({kind})')
    for rel, why in skipped:
        print(f'  ⚠ {rel:<40} {why}')


if __name__ == '__main__':
    main()
