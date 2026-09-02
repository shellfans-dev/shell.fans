#!/usr/bin/env python3
"""
為手寫的 AEO 頁面補上 Organization 實體節點。冪等。

## 為什麼

2026-09-02 的能見度探測：unbranded 品牌提及率 0%、官方引用率 3%——AI 已在
讀與引用這些頁面，但沒有把內容連回 ShellFans 這個實體。

由產生器輸出的 26 個 /aeo 頁面早就有 Organization 節點；但三個手寫的 AEO
頁面沒有：

    aeo-geo/methodology.html      TechArticle + BreadcrumbList
    aeo-geo/taiwan-aeo-tools.html Article + BreadcrumbList
    tools/aeo-geo-checker.html    WebApplication + FAQPage + BreadcrumbList

這三頁的 TechArticle/Article 都有 publisher 欄位，但那只是一個名稱字串，
沒有對應的 Organization 節點可以解析——AI 拿到「publisher: ShellFans」卻
無法知道那是哪一家公司、統編多少、地址在哪。補上帶 @id 的完整節點，
publisher 才有東西可指。

## 為什麼不直接沿用 build-aeo-pages.py

那支腳本會重新產生整頁。這三頁是手寫維護的，重新產生會覆蓋掉人工內容。
本腳本只新增一個獨立的 ld+json 區塊，不動既有 JSON 的排版與內容。

用法：python3 scripts/add-org-to-aeo-pages.py [--check]
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    'build_aeo_pages', os.path.join(ROOT, 'scripts', 'build-aeo-pages.py'))
_gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gen)

# 直接取產生器的節點——全站 Organization 必須是同一份，兩處各自維護遲早分歧
ORGANIZATION_NODE = _gen.ORGANIZATION_NODE

TARGETS = [
    'aeo-geo/methodology.html',
    'aeo-geo/taiwan-aeo-tools.html',
    'tools/aeo-geo-checker.html',
]


def main():
    check = '--check' in sys.argv
    done, already = [], []

    for rel in TARGETS:
        path = os.path.join(ROOT, rel)
        src = open(path, encoding='utf-8').read()

        blocks = list(re.finditer(
            r'<script type="application/ld\+json">(.*?)</script>', src, re.S))
        if not blocks:
            raise SystemExit(f'{rel}：找不到 ld+json 區塊')

        # 先確認既有區塊都能解析，並檢查是否已有 Organization
        has_org = False
        for m in blocks:
            try:
                data = json.loads(m.group(1))
            except json.JSONDecodeError as e:
                raise SystemExit(f'{rel}：既有 JSON-LD 無法解析 —— {e}')
            nodes = data.get('@graph', [data]) if isinstance(data, dict) else data
            for n in nodes:
                if isinstance(n, dict) and n.get('@type') == 'Organization':
                    has_org = True
        if has_org:
            already.append(rel)
            continue

        # 這三頁用的是「每個型別一個獨立區塊」，不是 @graph 陣列。
        # 因此新增一個獨立區塊，而不是塞進既有結構——後者會改動人工維護的
        # JSON 排版，diff 變得難以審查。
        node = dict(ORGANIZATION_NODE)
        node['@context'] = 'https://schema.org'
        node = {'@context': 'https://schema.org',
                **{k: v for k, v in node.items() if k != '@context'}}
        block = ('<script type="application/ld+json">\n'
                 + json.dumps(node, ensure_ascii=False, indent=2)
                 + '\n</script>\n')

        # 插在第一個既有區塊之前：讓「這是誰發布的」出現在最前面，
        # 與產生器頁面把 Organization 排在 @graph 首位的作法一致。
        out = src[:blocks[0].start()] + block + src[blocks[0].start():]

        # 產出即驗證
        found = False
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', out, re.S):
            d = json.loads(b)
            for n in (d.get('@graph', [d]) if isinstance(d, dict) else d):
                if isinstance(n, dict) and n.get('@type') == 'Organization':
                    found = True
                    for field in ('name', 'legalName', 'url', 'taxID', 'address', 'contactPoint'):
                        if field not in n:
                            raise SystemExit(f'{rel}：Organization 缺 {field}')
        if not found:
            raise SystemExit(f'{rel}：插入後找不到 Organization')

        if not check:
            open(path, 'w', encoding='utf-8').write(out)
        done.append(rel)

    print(f'{"待處理" if check else "已處理"} {len(done)} 頁'
          f'（已有而略過：{len(already)}）')
    for rel in done:
        print(f'  + {rel}')


if __name__ == '__main__':
    main()
