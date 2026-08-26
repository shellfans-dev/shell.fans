#!/usr/bin/env python3
"""
修正四個頁面缺少 H1、以及標題層級跳階的問題。冪等。

## 問題

  404.html                   最上層標題是 <h2>無法找到此頁</h2>，沒有 h1
  401.html                   最上層標題是 <h2>Password Protected</h2>，沒有 h1
  privacy-policy.html        <h3>隱私權條款</h3> → 八個 <h5>，沒有 h1，且跳階
  terms-and-conditions.html  <h3>服務條款</h3> → 十個 <h5>，沒有 h1，且跳階

前兩者是實際的錯誤頁（改成真 404 之後 404.html 才真正開始被送出）；
後兩者是 Is Agentic 稽核會檢查的信任錨點頁。四頁都是「無 JS 也應該
可讀」的頁面，沒有 h1 會讓抽取器找不到頁面主題。

## 為什麼改標籤不會動到外觀

這幾個標題的樣式都掛在 class 上（heading-style-h2 / heading-style-h3 /
heading-style-h5），不是靠標籤選擇器。CSS 特異性 class(0,1,0) 高於
tag(0,0,1)，所以 <h3 class="heading-style-h3"> 換成
<h1 class="heading-style-h3"> 之後，套用的仍然是同一條規則，
字級、字重、顏色、間距全部不變。

刻意保留原本的 class 名稱（不改成 heading-style-h1），因為 class 名稱
描述的是「長什麼樣」，而標籤描述的是「在文件結構裡是什麼」。這兩件事
本來就可以不一致，硬要對齊反而會改動視覺。

## 404.html 另外補救援連結

改成真 404 之後這一頁才會真正被送出。稽核要求錯誤回應要指向
sitemap / llms.txt / developers，機器可讀的 404.json 與 404.md 已經照做，
人類看的 HTML 版也應該一致——否則同一個錯誤在不同 Accept 下給的資訊量差很多。

用法：python3 scripts/fix-heading-levels.py [--check]
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (檔名, [(原標籤, 新標籤, 錨定字串)])
PROMOTIONS = [
    ('404.html', [('h2', 'h1', '無法找到此頁')]),
    ('401.html', [('h2', 'h1', 'Password Protected')]),
    ('privacy-policy.html', [('h3', 'h1', '隱私權條款')]),
    ('terms-and-conditions.html', [('h3', 'h1', '服務條款')]),
]

# 這兩頁的內文小節是 h5，主標題升為 h1 之後會從 h1 直接跳到 h5。
# 一併升為 h2，讓大綱連續。
SECTION_PROMOTIONS = ['privacy-policy.html', 'terms-and-conditions.html']

RECOVERY_LINKS = '''<nav aria-label="找不到頁面時的替代入口" style="max-width:640px;margin:24px auto 0;text-align:left;font-size:0.95rem;line-height:2">
<p style="margin:0 0 8px;font-weight:600">或從這些地方找到你要的內容：</p>
<ul style="margin:0;padding-left:1.2em">
<li><a href="https://shell.fans/sitemap.xml">網站地圖</a>　全部可用的網址都在這裡</li>
<li><a href="https://shell.fans/what-is-shellfans">ShellFans 是什麼</a>　服務總覽</li>
<li><a href="https://shell.fans/developers">開發者資源</a>　公開機器介面與 API 說明</li>
<li><a href="https://shell.fans/llms.txt">llms.txt</a>　給 AI agent 的站台導覽</li>
<li><a href="https://shell.fans/contact">聯絡我們</a>　找不到就直接問</li>
</ul>
</nav>
'''


def promote(html, old, new, anchor):
    """把包含 anchor 文字的 <old …> 標籤換成 <new …>，class 等屬性原封不動。"""
    pat = re.compile(
        r'<' + old + r'(\s[^>]*)?>(\s*' + re.escape(anchor) + r'.*?)</' + old + r'>', re.S)
    return pat.subn(lambda m: f'<{new}{m.group(1) or ""}>{m.group(2)}</{new}>', html, count=1)


def main():
    check = '--check' in sys.argv
    rows = []

    for rel, jobs in PROMOTIONS:
        path = os.path.join(ROOT, rel)
        src = open(path, encoding='utf-8').read()
        out = src
        changed = []

        if out.count('<h1') == 0:
            for old, new, anchor in jobs:
                out, n = promote(out, old, new, anchor)
                if n:
                    changed.append(f'{old}→{new}')

        if rel in SECTION_PROMOTIONS and '<h5' in out:
            out, n = re.subn(r'<h5(\s[^>]*)?>(.*?)</h5>',
                             lambda m: f'<h2{m.group(1) or ""}>{m.group(2)}</h2>', out, flags=re.S)
            if n:
                changed.append(f'h5→h2 ×{n}')

        if rel == '404.html' and 'aria-label="找不到頁面時的替代入口"' not in out:
            # 插在「回到首頁」按鈕之後，維持既有版面順序
            m = re.search(r'<a href="/" class="button is-secondary w-inline-block">.*?</a>', out, re.S)
            if m:
                out = out[:m.end()] + '\n' + RECOVERY_LINKS + out[m.end():]
                changed.append('救援連結')

        if not changed:
            continue

        # 產出即驗證
        if out.count('<h1') != 1:
            raise SystemExit(f'{rel}：h1 數量為 {out.count("<h1")}，應為 1')
        for tag in ('h1', 'h2', 'h3'):
            if out.count(f'<{tag}') != out.count(f'</{tag}>'):
                raise SystemExit(f'{rel}：{tag} 標籤不配對')
        if not check:
            open(path, 'w', encoding='utf-8').write(out)
        rows.append((rel, ', '.join(changed)))

    print(f'{"待處理" if check else "已處理"} {len(rows)} 頁')
    for rel, what in rows:
        print(f'  {rel:<30} {what}')


if __name__ == '__main__':
    main()
