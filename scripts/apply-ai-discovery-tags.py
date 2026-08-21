#!/usr/bin/env python3
"""
為非產生器管理的頁面加入 AI discovery 標籤。冪等，可重複執行。

## 加什麼

  <link rel="describedby" href="https://shell.fans/llms.txt">
      站台層的導覽檔。任何一頁被抓到，agent 都能順著找到 llms.txt，
      進而知道整個網站的結構與品牌實體 —— 不必先猜到根目錄有這個檔案。

  <link rel="alternate" type="text/markdown" href="…​.md">
      只在該頁確實有 .md 時才加。指向不存在的檔案會產生 404，
      比沒有這個標籤更糟。

## 不動 canonical

HTML 仍然 self-canonical。alternate 只是「同一份內容的另一種格式」，
不是另一個 canonical 候選。.md 由 nginx 帶 X-Robots-Tag: noindex，
不會與 HTML 競爭索引。

## 為什麼要有這支腳本

shell.fans 是純靜態站，沒有共用 layout。/aeo 叢集的 26 頁由
build-aeo-pages.py 產生（標籤寫在產生器裡），其餘頁面是獨立維護的 HTML，
只能逐檔插入 —— 但插入邏輯集中在這裡，不是散在各檔案。
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://shell.fans'

DESCRIBEDBY = f'<link rel="describedby" href="{SITE}/llms.txt">'

# 不需要 discovery 標籤的頁面
SKIP = {'401.html', '404.html', 'search.html', 'detail_news.html'}

# 由 build-aeo-pages.py 產生，標籤已寫在產生器裡，這裡不重複處理
GENERATED = re.compile(r'^aeo\.html$|^aeo/')


def page_url(rel):
    if rel == 'index.html':
        return SITE + '/'
    return SITE + '/' + rel[:-len('.html')]


def main():
    check = '--check' in sys.argv
    touched, skipped = [], []

    for rel in sorted(glob.glob('**/*.html', recursive=True, root_dir=ROOT)):
        if rel in SKIP or rel.startswith('.git') or GENERATED.match(rel):
            continue
        path = os.path.join(ROOT, rel)
        src = open(path, encoding='utf-8').read()
        out = src
        added = []

        if 'rel="describedby"' not in out:
            # 插在 canonical 之後 —— 兩者都是「這一頁是什麼」的宣告，放一起好讀
            m = re.search(r'<link rel="canonical"[^>]*>\n?', out)
            anchor = m.end() if m else None
            if anchor is None:
                m2 = re.search(r'<meta name="viewport"[^>]*>\n?', out)
                anchor = m2.end() if m2 else None
            if anchor is None:
                skipped.append((rel, '找不到可插入的位置'))
                continue
            block = ('\n<!-- AI agent discovery：llms.txt 是站台層導覽檔，不影響 canonical。 -->\n'
                     + DESCRIBEDBY + '\n')
            out = out[:anchor] + block + out[anchor:]
            added.append('describedby')

        md_rel = rel[:-len('.html')] + '.md'
        if os.path.exists(os.path.join(ROOT, md_rel)) and 'type="text/markdown"' not in out:
            alt = (f'<link rel="alternate" type="text/markdown" href="{page_url(rel)}.md"'
                   ' title="Markdown version for AI agents">\n')
            out = out.replace(DESCRIBEDBY + '\n', DESCRIBEDBY + '\n' + alt, 1)
            added.append('alternate')

        if added and not check:
            open(path, 'w', encoding='utf-8').write(out)
        if added:
            touched.append((rel, '+'.join(added)))

    print(f'{"待處理" if check else "已處理"} {len(touched)} 頁')
    for rel, what in touched:
        print(f'  {rel:<34} {what}')
    for rel, why in skipped:
        print(f'  ⚠ {rel:<34} {why}')


if __name__ == '__main__':
    main()
