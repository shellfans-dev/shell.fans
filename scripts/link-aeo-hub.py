#!/usr/bin/env python3
"""
把既有 AEO 頁面連回新的知識中心 /aeo。冪等，可重複執行。

## 為什麼需要

新建的 /aeo 叢集若沒有任何既有頁面指向它，等於一座孤島 —— 爬蟲要靠 sitemap
才找得到，而既有頁面累積的權重也完全傳不過去。內部連結要雙向：hub 指向
child（產生器已處理），既有的已索引頁面也要指向 hub。

## 作法

在既有頁面的 `<p class="sf-inline-links">相關頁面：...</p>` 尾端追加一條連結。
選這個位置是因為它已經是「相關頁面」的語意區塊，插在這裡不需要改版面。

what-is-shellfans.html 沒有這個區塊（它是品牌實體頁，結構不同），改為在
`</main>` 之前插入一個完整區塊。

## 錨文字

刻意每頁不同 —— 全站用同一句錨文字會讓這批連結看起來像機器批次產生的，
對兩邊都沒有好處。
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUB = 'https://shell.fans/aeo'

# 檔案 → 錨文字（每頁不同）
TARGETS = {
    'aeo-geo.html': 'AEO/GEO 知識中心：定義、技術實作與採購指南',
    'aeo-geo/methodology.html': 'AEO/GEO 知識中心：各評分面向的完整說明',
    'aeo-geo/taiwan-aeo-tools.html': 'AEO/GEO 知識中心：如何挑選 AEO 廠商與工具',
    'tools/aeo-geo-checker.html': 'AEO/GEO 知識中心：檢測結果的每一項該怎麼修',
}

STANDALONE = {
    'what-is-shellfans.html': [
        ('/aeo', 'AEO/GEO 知識中心'),
        ('/aeo/what-is-aeo', 'AEO 是什麼'),
        ('/aeo/managed-hosting', 'AEO Managed Hosting'),
    ],
}

MARKER = 'href="%s"' % HUB


def patch_inline_links(path, anchor):
    src = open(path, encoding='utf-8').read()
    if MARKER in src:
        return False, '已存在'

    m = re.search(r'(<p class="sf-inline-links">.*?)(</p>)', src, re.S)
    if not m:
        return False, '找不到 sf-inline-links 區塊'

    addition = '　·　<a href="%s">%s</a>' % (HUB, anchor)
    src = src[:m.end(1)] + addition + src[m.end(1):]
    open(path, 'w', encoding='utf-8').write(src)
    return True, '已追加'


def patch_standalone(path, links):
    src = open(path, encoding='utf-8').read()
    if MARKER in src:
        return False, '已存在'
    if '</main>' not in src:
        return False, '找不到 </main>'

    block = ('\n  <section>\n    <div class="container">\n'
             '      <p class="sf-inline-links">延伸閱讀：%s</p>\n'
             '    </div>\n  </section>\n\n'
             % '　·　'.join('<a href="https://shell.fans%s">%s</a>' % (u, t) for u, t in links))
    src = src.replace('</main>', block + '</main>', 1)
    open(path, 'w', encoding='utf-8').write(src)
    return True, '已插入區塊'


def main():
    changed = 0
    for rel, anchor in TARGETS.items():
        ok, msg = patch_inline_links(os.path.join(ROOT, rel), anchor)
        changed += ok
        print('  %-34s %s' % (rel, msg))
    for rel, links in STANDALONE.items():
        ok, msg = patch_standalone(os.path.join(ROOT, rel), links)
        changed += ok
        print('  %-34s %s' % (rel, msg))
    print('異動 %d 個檔案' % changed)


if __name__ == '__main__':
    main()
