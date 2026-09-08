#!/usr/bin/env python3
"""
修正文件標題大綱的兩個結構問題。冪等。

Is Agentic 稽核「Content without JavaScript」判為 Partial：
"2993 chars with H1 but flat heading structure"。實測首頁無 JS 可見文字
是 3564 字元，而稽核算到 2993——差的約 570 字元正好是 FAQ 的答案內容，
亦即掃描器把 <details> 內折疊的部分排除了。折疊後 FAQ 只剩六個問句，
而問句寫在 <summary> 裡不是標題，於是那一整段在大綱裡是「一個 H2 底下
什麼都沒有」。

## 修正一：FAQ 問句成為真標題

  <summary data-i18n="k">問句</summary>
  →
  <summary><h3 data-i18n="k" style="…">問句</h3></summary>

data-i18n 必須跟著移到 <h3>。applyTranslations() 走的是
el.textContent = val（非 innerHTML），留在 <summary> 上會把剛加的 <h3>
連同內容一起清掉。

外觀必須不變（稽核明訂保留現有視覺設計），因此 h3 帶
display:inline;font:inherit;margin:0;padding:0;color:inherit——
把標題的預設樣式全部中和成與原本的裸文字節點一致。

## 修正二：footer 欄位標題不再懸掛在內容 H2 底下

footer 的「產品 / 資源 / 聯繫」是 <h3>，出現在頁面最後一個內容 H2
之後。在文件大綱裡它們會被讀成該 H2 的子節——首頁就是掛在「常見問題」
底下，about 頁也一樣。HTML5 的 outline 演算法從未被瀏覽器實作，<footer>
包起來並不會讓它們自成一區。

補一個視覺隱藏的 <h2>「網站導覽」在 footer 欄位之前，H3 就有了正確的
父節點。用 inline style 而不是 CSS class：本站每頁各自內嵌 CSS，沒有
共用樣式表可放，inline 是唯一能保證 49 頁一致生效的做法。

這不是隱藏關鍵字堆砌——文字只有「網站導覽」四個字，是 WCAG 建議的
導覽區塊標題，對螢幕閱讀器使用者同樣有用。

用法：python3 scripts/fix-heading-outline.py [--check]
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 把 h3 的預設樣式完全中和，渲染結果與原本的裸文字節點相同
H3_INLINE = 'display:inline;font:inherit;margin:0;padding:0;color:inherit'

HIDDEN_H2 = (
    '<h2 style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;'
    'overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0">網站導覽</h2>'
)

# footer 第一個欄位的起點
FOOTER_COL = '<div class="sf-footer-col">'


def fix_summary(html):
    """把 <summary> 的文字內容包成 <h3>，data-i18n 一併移入。"""
    n = 0

    def repl(m):
        nonlocal n
        attrs, inner = m.group(1), m.group(2)
        if '<h3' in inner:
            return m.group(0)                      # 冪等
        # data-not-heading：這個 <summary> 是「展開更多」的操作標籤，不是內容標題。
        # 案例頁用 <details> 收納技術細節與模型版本表，那些 summary 若被包成 h3，
        # 文件大綱裡就會多出兩個不存在的章節，反而破壞它原本要修的東西。
        if 'data-not-heading' in attrs:
            return m.group(0)
        # data-i18n 系列屬性要移到 h3；其餘（如 class）留在 summary
        moved = re.findall(r'\s(data-i18n(?:-attr|-html)?(?:="[^"]*")?)', attrs)
        rest = re.sub(r'\s(data-i18n(?:-attr|-html)?(?:="[^"]*")?)', '', attrs)
        h3_attrs = (' ' + ' '.join(moved)) if moved else ''
        n += 1
        return (f'<summary{rest}><h3{h3_attrs} style="{H3_INLINE}">'
                f'{inner}</h3></summary>')

    out = re.sub(r'<summary\b([^>]*)>(.*?)</summary>', repl, html, flags=re.S)
    return out, n


def fix_footer(html):
    """在 footer 第一個欄位之前插入視覺隱藏的區塊標題。"""
    if '網站導覽' in html or FOOTER_COL not in html:
        return html, 0
    return html.replace(FOOTER_COL, HIDDEN_H2 + FOOTER_COL, 1), 1


def main():
    check = '--check' in sys.argv
    rows = []
    for rel in sorted(glob.glob('**/*.html', recursive=True, root_dir=ROOT)):
        if rel.startswith('.git'):
            continue
        path = os.path.join(ROOT, rel)
        src = open(path, encoding='utf-8').read()
        out, n_sum = fix_summary(src)
        out, n_ft = fix_footer(out)
        if n_sum == 0 and n_ft == 0:
            continue
        # 產出即驗證：h1 數量不得改變，且 summary/h3 必須配對
        if out.count('<h1') != src.count('<h1'):
            raise SystemExit(f'{rel}：h1 數量被改動')
        if out.count('<summary') != out.count('</summary>'):
            raise SystemExit(f'{rel}：summary 標籤不配對')
        if not check:
            open(path, 'w', encoding='utf-8').write(out)
        rows.append((rel, n_sum, n_ft))

    print(f'{"待處理" if check else "已處理"} {len(rows)} 頁'
          f'（FAQ 問句 {sum(r[1] for r in rows)} 個、footer 標題 {sum(r[2] for r in rows)} 個）')
    for rel, a, b in rows[:6]:
        print(f'  {rel:<38} summary×{a}  footer×{b}')
    if len(rows) > 6:
        print(f'  …其餘 {len(rows) - 6} 頁')


if __name__ == '__main__':
    main()
