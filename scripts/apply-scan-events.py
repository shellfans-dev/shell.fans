#!/usr/bin/env python3
"""
為 AEO 檢測工具埋入 GA4 轉換事件。冪等。

## 只對真實存在的互動埋點

站上盤點到的表單：

    aeoCheckerForm   → POST console.shell.fans/api/site/aeo-geo/scan（真的會執行）
    email-form-2     → onsubmit="alert('此功能即將開放…'); return false"
    sfChatForm       → chat 功能已自官網移除
    /search          → Webflow 站內搜尋，非轉換
    401 密碼頁       → 非轉換

因此只埋 aeoCheckerForm。contact 表單刻意**不埋**：它只跳一個 alert，
沒有任何東西被送出。埋 contact_submit 會在報表上產生一個實際不存在的
轉換，比沒有數據更糟——看報表的人會以為有人成功聯絡了。

## 送什麼、不送什麼

送：score（數字）、grade（等級字母）
不送：**使用者輸入的網址**

網址是使用者輸入的文字。雖然檢測的是公開網站，但那是對方尚未公開表示
要檢測的資產，且 GA4 不是存放這類資料的地方。score 與 grade 足以回答
「AI 推薦來的人檢測結果如何」，不需要知道是誰的網站。

## 事件

    aeo_scan_start      表單送出時
    aeo_scan_complete   成功取得結果並渲染時（失敗不送——那不是完成）

兩者都經 window.sfAnalytics.track()，AI 歸因會自動附上；非 AI session
也會送，只是不帶那幾個欄位，這樣轉換率的分母仍然完整。

用法：python3 scripts/apply-scan-events.py [--check]
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TARGETS = ['tools/aeo-geo-checker.html', 'aeo-geo.html']

MARKER = 'sf_scan_events'

# 表單送出：插在 setBtn(true); 之後——此時已確認有輸入值且即將發出請求
START_ANCHOR = "setBtn(true);"
START_CODE = (
    "setBtn(true);"
    "/*" + MARKER + "*/"
    "try{window.sfAnalytics&&window.sfAnalytics.track('aeo_scan_start',"
    "{scan_source:location.pathname});}catch(e){}"
)

# 成功渲染：插在 render(o.body.data); 之前
DONE_ANCHOR = "render(o.body.data);"
DONE_CODE = (
    "/*" + MARKER + "*/"
    "try{window.sfAnalytics&&window.sfAnalytics.track('aeo_scan_complete',"
    "{scan_score:(o.body.data&&typeof o.body.data.score==='number')?o.body.data.score:null,"
    "scan_grade:(o.body.data&&o.body.data.grade)?String(o.body.data.grade):null,"
    "scan_source:location.pathname});}catch(e){}"
    "render(o.body.data);"
)


def main():
    check = '--check' in sys.argv
    done, already, missing = [], [], []

    for rel in TARGETS:
        path = os.path.join(ROOT, rel)
        src = open(path, encoding='utf-8').read()

        if MARKER in src:
            already.append(rel)
            continue

        if src.count(START_ANCHOR) != 1 or src.count(DONE_ANCHOR) != 1:
            missing.append(
                (rel, f'錨點數量非 1（start={src.count(START_ANCHOR)}, '
                      f'done={src.count(DONE_ANCHOR)}）'))
            continue

        out = src.replace(START_ANCHOR, START_CODE, 1)
        out = out.replace(DONE_ANCHOR, DONE_CODE, 1)

        # 產出即驗證
        if out.count(MARKER) != 2:
            raise SystemExit(f'{rel}：標記數不是 2')
        if 'aeoUrlInput.value' in out.split(MARKER)[1][:400]:
            raise SystemExit(f'{rel}：事件中疑似夾帶使用者輸入的網址')
        # 括號平衡的粗檢——插入的是完整敘述，不該改變平衡
        for ch, cl in (('{', '}'), ('(', ')')):
            if out.count(ch) - out.count(cl) != src.count(ch) - src.count(cl):
                raise SystemExit(f'{rel}：{ch}{cl} 平衡被改變')

        if not check:
            open(path, 'w', encoding='utf-8').write(out)
        done.append(rel)

    print(f'{"待處理" if check else "已處理"} {len(done)} 頁（已有 {len(already)}）')
    for rel in done:
        print(f'  + {rel}')
    for rel, why in missing:
        print(f'  ⚠ {rel}：{why}')


if __name__ == '__main__':
    main()
