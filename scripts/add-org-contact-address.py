#!/usr/bin/env python3
"""
為全站 Organization JSON-LD 補上 address / contactPoint / foundingDate。冪等。

## 為什麼

Is Agentic 稽核「Organization schema completeness」判為 Partial，理由是
"Missing: contactPoint, address in JSON-LD"。這兩個欄位是 agent 做實體解析
（entity resolution）時最常查的：它要確認「網路上這個 ShellFans」與「台灣某
一家登記在案的公司」是同一個實體，靠的就是地址、統編、聯絡管道能不能對上
第三方紀錄。缺了它們，Organization 節點只是一組自我宣告。

## 資料來源 —— 全部取自站上已公開的內容，沒有一個是新編的

  address       footer「地址：臺北市內湖區瑞光路335號4樓」（每一頁都有）
  email         footer「信箱：hello@shell.fans」
  telephone     footer「電話：02-77143635」→ 轉成 E.164 的 +886-2-7714-3635
                （同一支號碼的國際格式，不是另一支號碼）
  taxID         footer「統編：83032387」（節點中已有）
  foundingDate  /co-founder 沿革「2023/03 創辦唄粉智能科技股份有限公司」
                資料實際來自 console.shell.fans/api/site/cofounder

刻意不填的欄位：
  numberOfEmployees、foundingLocation 的精確地址、revenue —— 站上沒有，
  也無法從公開資料確認。寧可留空也不猜。

用法：python3 scripts/add-org-contact-address.py [--check]
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# taxID 在站上有兩種形式：
#   有逗號 —— 節點後面還有 description / makesOffer（手寫頁）
#   無逗號 —— taxID 是節點最後一個欄位（早期由產生器短版節點寫出的頁面）
# 兩種都要能處理，且插入後仍是合法 JSON。
ANCHOR_RE = re.compile(r'"taxID": "83032387"(,?)')

# 縮排跟著既有節點走（node 內的欄位是 6 空格），插在 anchor 之後
BLOCK = '''      "foundingDate": "2023-03",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "瑞光路335號4樓",
        "addressLocality": "內湖區",
        "addressRegion": "臺北市",
        "addressCountry": "TW"
      },
      "contactPoint": [
        {
          "@type": "ContactPoint",
          "contactType": "customer support",
          "email": "hello@shell.fans",
          "telephone": "+886-2-7714-3635",
          "areaServed": "TW",
          "availableLanguage": ["zh-Hant", "en"]
        }
      ],'''


def _assert_jsonld_ok(html, rel):
    """每個 ld+json 區塊都要能解析，且 Organization 必須帶齊新欄位。"""
    import json
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    if not blocks:
        raise SystemExit(f'{rel}：找不到 ld+json 區塊')
    seen_org = False
    for b in blocks:
        try:
            data = json.loads(b)
        except json.JSONDecodeError as e:
            raise SystemExit(f'{rel}：JSON-LD 解析失敗 —— {e}')
        for node in (data.get('@graph', [data]) if isinstance(data, dict) else data):
            if isinstance(node, dict) and node.get('@type') == 'Organization':
                seen_org = True
                for field in ('address', 'contactPoint', 'foundingDate'):
                    if field not in node:
                        raise SystemExit(f'{rel}：Organization 缺 {field}')
                if node['address'].get('@type') != 'PostalAddress':
                    raise SystemExit(f'{rel}：address 不是 PostalAddress')
                if node['contactPoint'][0].get('@type') != 'ContactPoint':
                    raise SystemExit(f'{rel}：contactPoint 不是 ContactPoint')
    if not seen_org:
        raise SystemExit(f'{rel}：ld+json 內找不到 Organization 節點')


def main():
    check = '--check' in sys.argv
    touched, already = [], 0

    for rel in sorted(glob.glob('**/*.html', recursive=True, root_dir=ROOT)):
        if rel.startswith('.git'):
            continue
        path = os.path.join(ROOT, rel)
        src = open(path, encoding='utf-8').read()
        m = ANCHOR_RE.search(src)
        if not m:
            continue
        if '"contactPoint"' in src and '"PostalAddress"' in src:
            already += 1
            continue
        had_comma = m.group(1) == ','
        # 無逗號版的 taxID 是節點最後一欄，插入後它不再是最後一欄，要補逗號；
        # 反過來新區塊就不能再帶結尾逗號，否則變成 trailing comma（非法 JSON）。
        body = BLOCK if had_comma else BLOCK.rstrip().rstrip(',')
        out = src[:m.end()] + ('' if had_comma else ',') + '\n' + body + src[m.end():]
        # 產出即驗證：改壞 JSON-LD 比缺欄位嚴重得多 —— 解析失敗的 @graph
        # 會讓整頁的結構化資料一起失效，連原本正確的節點都不算數。
        _assert_jsonld_ok(out, rel)
        if not check:
            open(path, 'w', encoding='utf-8').write(out)
        touched.append(rel)

    print(f'{"待處理" if check else "已處理"} {len(touched)} 頁（已有欄位而略過：{already}）')
    for rel in touched[:5]:
        print(f'  {rel}')
    if len(touched) > 5:
        print(f'  …其餘 {len(touched) - 5} 頁')


if __name__ == '__main__':
    main()
