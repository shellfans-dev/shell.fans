#!/usr/bin/env python3
"""
把 ShellFans 自管的 GA4 標籤與 AI 推薦歸因腳本套用到全站。冪等。

## 為什麼需要這支腳本

2026-09-04 盤點結果：

    有 GA4 的頁面     15 / 50
    完全沒有的        35 頁，其中 **29 頁是 /aeo 叢集**

/aeo 叢集正是 AI 會引用並導流的落地頁。要量測「AI 回答 → 點擊 → 落地 →
轉換」這條鏈，但落地頁沒有任何追蹤——這條鏈從第二步就斷了。

## 兩個 measurement ID 的來歷

    G-NE4639EL2B   2 頁（index、social-media-backup），帶 data-shellfans-ga="1"
    G-ND3TSXDQX0   13 頁，同一段 script 帶 gtag('set','developer_id.dZGVlNj')

`developer_id.dZGVlNj` 是 **Webflow** 的識別碼——那 13 頁是 Webflow 匯出時
內建的舊標籤。而 Admin API 查證：properties/410150889（ShellFans 帳戶下唯一
的 property）只有一個資料串流，measurement ID 正是 G-NE4639EL2B。

也就是說 G-ND3TSXDQX0 不屬於這個 GA4 帳戶。13 頁的資料送去了一個
service account 看不到、也可能沒人在看的地方。

本腳本只做「補上正確的標籤」，**不動 Webflow 的舊標籤**——移除它會中斷那個
property 的歷史連續性，那是產品決策不是技術決策，留給人決定。兩個標籤並存
不會在同一個 property 內重複計算 page_view：各自送給各自的 property。

## 插入什麼

    <script async data-shellfans-ga="1" src="…gtag/js?id=G-NE4639EL2B"></script>
    <script data-shellfans-ga="1">…gtag config…</script>
    <script defer data-shellfans-ga="1" src="/js/sf-analytics.js"></script>

gtag 用 async 且內嵌 config——它必須早於任何事件送出。
sf-analytics.js 用 defer——它只在 DOMContentLoaded 後才需要執行，
不該擋住頁面渲染。

## 冪等標記

以 `data-shellfans-ga="1"` 判斷是否已套用。這個屬性是既有頁面本來就在用的
慣例（index.html），沿用它而不是另創標記。

用法：python3 scripts/apply-ga4-tracking.py [--check]
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ShellFans 自管的 property。以 Admin API 查證：
# properties/410150889 → dataStreams/6253319282 → defaultUri https://shell.fans
MEASUREMENT_ID = 'G-NE4639EL2B'

MARKER = 'data-shellfans-ga="1"'

# 不需要追蹤的頁面：
#   401/404  錯誤頁。記錄它們會讓 landing page 報表混入不存在的路徑。
#   search / detail_news  Webflow CMS 模板殘留，未對外連結、不在 sitemap。
SKIP = {'401.html', '404.html', 'search.html', 'detail_news.html'}

GA_BLOCK = (
    '<script async {m} src="https://www.googletagmanager.com/gtag/js?id={mid}"></script>'
    '<script {m}>window.dataLayer=window.dataLayer||[];'
    'function gtag(){{dataLayer.push(arguments);}}'
    'gtag("js",new Date());gtag("config","{mid}");</script>'
    '<script defer {m} src="https://shell.fans/js/sf-analytics.js"></script>'
).format(m=MARKER, mid=MEASUREMENT_ID)


def main():
    check = '--check' in sys.argv
    added, already, skipped = [], [], []

    for rel in sorted(glob.glob('**/*.html', recursive=True, root_dir=ROOT)):
        if rel.startswith('.git') or os.path.basename(rel) in SKIP:
            continue
        path = os.path.join(ROOT, rel)
        src = open(path, encoding='utf-8').read()

        if MARKER in src:
            already.append(rel)
            continue

        # 插在 </head> 之前。gtag 必須在 body 之前載入，否則落地當下的
        # page_view 可能在 gtag 就緒前就錯過。
        m = re.search(r'</head>', src, re.I)
        if not m:
            skipped.append((rel, '找不到 </head>'))
            continue
        out = src[:m.start()] + GA_BLOCK + src[m.start():]

        # 產出即驗證
        if out.count('gtag/js?id=' + MEASUREMENT_ID) != 1:
            raise SystemExit(f'{rel}：ShellFans GA 標籤數不是 1')
        if out.count('sf-analytics.js') != 1:
            raise SystemExit(f'{rel}：sf-analytics.js 數不是 1')
        if out.count('</head>') != src.count('</head>'):
            raise SystemExit(f'{rel}：</head> 數量被改動')

        if not check:
            open(path, 'w', encoding='utf-8').write(out)
        added.append(rel)

    legacy = [r for r in sorted(glob.glob('**/*.html', recursive=True, root_dir=ROOT))
              if not r.startswith('.git')
              and 'G-ND3TSXDQX0' in open(os.path.join(ROOT, r), encoding='utf-8').read()]

    print(f'{"待處理" if check else "已處理"} {len(added)} 頁'
          f'（已有標記 {len(already)}、略過 {len(SKIP)} 個工具頁）')
    for rel in added[:6]:
        print(f'  + {rel}')
    if len(added) > 6:
        print(f'  …其餘 {len(added) - 6} 頁')
    for rel, why in skipped:
        print(f'  ⚠ {rel}：{why}')
    if legacy:
        print(f'\n  ℹ {len(legacy)} 頁仍帶 Webflow 舊標籤 G-ND3TSXDQX0（本腳本不動它）：')
        print(f'    {", ".join(os.path.basename(r) for r in legacy)}')
        print('    移除與否是產品決策——會中斷該 property 的歷史連續性。')


if __name__ == '__main__':
    main()
