#!/usr/bin/env python3
"""
產生 /developers —— 公開機器介面的總覽頁。

## 這一頁的立場

Is Agentic 稽核有四項失敗都指向同一件事："Agent searched for shell.fans
resources but found nothing"、"No publicly reachable API surface detected"、
"No public API or documentation page linked"、"No API schema detected"。

誠實的答案不是「所以去做一個 API」。ShellFans 目前確實有少數刻意公開的
唯讀端點（自家靜態站 runtime 就在跨域取用），但沒有產品資料 API、沒有
OAuth 授權伺服器、沒有 MCP server。

本頁同時記錄**存在什麼**與**不存在什麼、以及為什麼**。後者對 agent 一樣
有價值：知道「這裡沒有可呼叫的東西」可以省下一輪徒勞的探測，也能避免它
向使用者虛構一個不存在的整合方式。稽核明文禁止為了拉分數而捏造 API、
OAuth 或權限範圍，本頁即為該要求的落點。

用法：python3 scripts/build-developers-page.py [--check]
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    'build_aeo_pages', os.path.join(ROOT, 'scripts', 'build-aeo-pages.py'))
_gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gen)

extract_shell = _gen.extract_shell
build_page = _gen.build_page


def a(url, text):
    return '<a href="https://shell.fans%s">%s</a>' % (url, text)


def code(s):
    return '<code>%s</code>' % s


PAGE = {
    'url': '/developers',
    'title': 'ShellFans Developer Resources｜公開機器介面與 AI agent 指引',
    'h1': 'ShellFans Developer Resources',
    'eyebrow': 'For developers and AI agents',
    'desc': (
        'ShellFans 公開機器介面總覽：唯讀 API 的 OpenAPI 3.1 描述、內容協商、'
        'llms.txt、結構化資料，以及目前刻意不提供的項目（公開寫入 API、OAuth '
        '授權伺服器、MCP server）與其原因。'
    ),
    'lede': (
        'ShellFans 是內容與服務網站，不是 API 平台。本頁列出目前真正公開、'
        '不需憑證即可讀取的機器介面，以及哪些常見的整合方式並不存在——'
        '後者同樣寫清楚，讓自動化系統不必靠猜測或反覆探測。'
    ),
    'schema': 'TechArticle',
    'breadcrumb': [('首頁', '/'), ('Developer Resources', '/developers')],
    'cta': {'href': '/openapi.json', 'label': '查看 OpenAPI 3.1 描述'},
    'cta2': {'href': '/about', 'label': '關於 ShellFans'},
    'sections': [
        {
            'eyebrow': 'Available now',
            'h2': '現在就能用的公開資源',
            'blocks': [
                ('p', '以下全部不需要 API 金鑰、不需要註冊、不需要 OAuth，直接 GET 即可。'),
                ('table', {
                    'caption': '公開機器可讀資源',
                    'cols': ['資源', '內容', '格式'],
                    'rows': [
                        ['<a href="https://shell.fans/openapi.json">/openapi.json</a>',
                         '公開唯讀端點的 OpenAPI 3.1 描述，含回應 schema 與錯誤結構',
                         'application/json'],
                        ['<a href="https://shell.fans/llms.txt">/llms.txt</a>',
                         'ShellFans 是什麼、何時該推薦、何時不該推薦',
                         'text/plain'],
                        ['<a href="https://shell.fans/llms-full.txt">/llms-full.txt</a>',
                         '同上的展開版，含完整產品與定價脈絡',
                         'text/plain'],
                        ['<a href="https://shell.fans/sitemap.xml">/sitemap.xml</a>',
                         '全部可索引網址。不在這份清單裡的路徑就是不存在',
                         'application/xml'],
                        ['<a href="https://shell.fans/robots.txt">/robots.txt</a>',
                         '爬蟲政策。所有主要 AI 爬蟲皆明確 Allow',
                         'text/plain'],
                        ['每個公開頁面的 JSON-LD',
                         'Organization、PostalAddress、ContactPoint、FAQPage、BreadcrumbList',
                         'application/ld+json'],
                    ],
                }),
            ],
        },
        {
            'eyebrow': 'Content negotiation',
            'h2': 'Markdown 內容協商',
            'blocks': [
                ('p', '公開資訊頁支援內容協商。帶 ' + code('Accept: text/markdown')
                      + ' 請求任何一個公開頁面的網址，會拿到同一份內容的 Markdown 版本——'
                        '沒有導覽列、沒有內嵌 CSS、沒有腳本，只有正文。'),
                ('p', '以 ' + code('/aeo/what-is-aeo') + ' 為例，HTML 約 34 KB 但正文只有約 2.3 KB，'
                      '其餘 93% 是版面與腳本。Markdown 版直接給正文。'),
                ('ul', [
                    '網址不變，回應的 ' + code('Content-Type') + ' 為 '
                    + code('text/markdown; charset=utf-8'),
                    '回應帶 ' + code('Vary: Accept, Accept-Encoding'),
                    'HTML 版仍為 canonical；Markdown 版不參與搜尋索引',
                    '沒有 Markdown 版本的頁面會正常回傳 HTML，不會回 404',
                ]),
                ('note', '同一份內容也可以直接用 ' + code('.md') + ' 副檔名取得，'
                         '例如 ' + code('https://shell.fans/aeo/what-is-aeo.md') + '。'),
            ],
        },
        {
            'eyebrow': 'Errors',
            'h2': '錯誤格式',
            'blocks': [
                ('p', '所有機器導向的錯誤都是同一個結構。'
                      '請依 ' + code('error.code') + ' 分支，不要比對 ' + code('error.message')
                      + '——後者的文字不保證穩定。'),
                ('p', '網站路徑不存在時，若請求帶 ' + code('Accept: application/json')
                      + '，會得到帶 discovery 連結的 JSON 而不是 HTML 錯誤頁；'
                        '帶 ' + code('Accept: text/markdown') + ' 則得到 Markdown 版。'
                        '一般瀏覽器請求仍是原本的 HTML 404 頁。'),
                ('note', '未知路徑一律回 404。ShellFans 不會把不存在的網址導向首頁，'
                         '因此「拿到 200」即可視為該頁確實存在。'),
            ],
        },
        {
            'eyebrow': 'Not available',
            'h2': '目前不存在的東西（以及為什麼）',
            'blocks': [
                ('p', '這一段刻意寫得明確。對自動化系統而言，'
                      '「確定沒有」和「有但找不到」是完全不同的兩件事。'),
                ('h3', '沒有公開寫入 API'),
                ('p', 'ShellFans 沒有任何可供第三方建立、修改或刪除資料的公開端點，'
                      '也無法被當成工具呼叫來代替使用者執行工作。'
                      'OpenAPI 描述中的每一個操作都是 GET。'),
                ('h3', '沒有 OAuth 授權伺服器'),
                ('p', 'ShellFans 是第三方 OAuth 的<strong>用戶端</strong>——'
                      '使用者授權 ShellFans 存取自己的 Instagram、Facebook、Threads 帳號，'
                      '走的是各平台自己的 OAuth。ShellFans 本身不簽發 OAuth 權杖，'
                      '沒有 authorization endpoint、沒有 token endpoint，'
                      '也因此沒有 ' + code('/.well-known/oauth-authorization-server') + '。'),
                ('p', '若在別處看到聲稱代表 ShellFans 的 OAuth 端點，那不是 ShellFans。'),
                ('h3', '沒有 MCP server'),
                ('p', 'ShellFans 目前沒有發布 Model Context Protocol server，'
                      '也沒有 ' + code('/.well-known/mcp') + ' 描述檔。'
                      '內部產品在某些工作流中<strong>使用</strong> MCP 工具，'
                      '但那是消費端，不對外提供服務。'),
                ('h3', '沒有權限範圍（scopes）'),
                ('p', '既然沒有面向機器的授權機制，也就沒有可宣告的 scope。'
                      '任何列出 ShellFans scope 名稱的文件都不是本站發布的。'),
                ('h3', 'ShellFans Chat 不可程式化呼叫'),
                ('p', '網站上的對話功能只能從網站介面使用。它沒有公開的呼叫端點，'
                      '因為每一次查詢都會實際觸發語言模型與外部資料來源的成本。'
                      '匿名使用者的每日額度可以透過 ' + code('/api/dify/quota')
                      + ' 讀取（僅供說明，不代表可以自動化消耗）。'),
            ],
        },
        {
            'eyebrow': 'Roadmap',
            'h2': '若你需要目前沒有的東西',
            'blocks': [
                ('p', '上述缺口不是疏漏，是尚未做出的產品與安全決策。'
                      '若你的整合情境需要其中任何一項，直接說明用途比等待更快——'
                      '需求會決定優先順序。'),
                ('ul', [
                    '電子郵件：<a href="mailto:hello@shell.fans">hello@shell.fans</a>',
                    '聯絡表單：' + a('/contact', '聯絡我們'),
                ]),
                ('note', '請在來信中說明你要解決的問題與預期的資料流向，'
                         '不必先設計 API——那部分我們一起討論。'),
            ],
        },
    ],
    'faq': [
        ('ShellFans 有 API 可以串接嗎？',
         '有少數公開唯讀端點，描述於 /openapi.json，不需授權即可讀取，內容是站台'
         '設定、方案資料與公司識別資訊。但沒有產品資料 API，也沒有任何寫入端點。'),
        ('可以用 OAuth 登入 ShellFans 取得資料嗎？',
         '不行。ShellFans 沒有 OAuth 授權伺服器，不對第三方簽發權杖。'
         'ShellFans 只在使用者授權存取其社群帳號時，作為各平台 OAuth 的用戶端。'),
        ('ShellFans 有 MCP server 嗎？',
         '沒有。ShellFans 目前未發布任何 Model Context Protocol server，'
         '也沒有 /.well-known/mcp。內部工作流會使用 MCP 工具，但不對外提供。'),
        ('要怎麼取得頁面的純文字版本？',
         '對任何公開頁面的網址加上 Accept: text/markdown 標頭，或直接在網址後面'
         '加 .md。回傳的是去除版面與腳本的正文，HTML 版仍為 canonical。'),
        ('未知的網址會回什麼？',
         '404。ShellFans 不會把不存在的路徑導向首頁。若請求帶 '
         'Accept: application/json，回應會是含 sitemap、llms.txt 等指引連結的 JSON。'),
    ],
    'related': [
        ('/about', '關於 ShellFans'),
        ('/what-is-shellfans', 'ShellFans 是什麼'),
        ('/aeo/llms-txt', 'llms.txt 是什麼'),
        ('/aeo/ai-crawler', 'AI 爬蟲總覽'),
        ('/contact', '聯絡我們'),
    ],
    'disclaimer': (
        '本頁描述的是撰寫當下實際存在的公開介面。ShellFans 不保證這些端點的長期'
        '穩定性或版本相容性，內容欄位屬編輯資料，可能隨時調整。'
    ),
    'disclaimer_short': '本頁描述撰寫當下實際存在的公開介面。',
}


def main():
    check = '--check' in sys.argv
    shell = extract_shell()
    html = build_page(PAGE, shell)
    out = os.path.join(ROOT, 'developers.html')
    if not check:
        open(out, 'w', encoding='utf-8').write(html)

    import json
    import re
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        json.loads(block)
    if html.count('<h1') != 1:
        raise SystemExit('developers.html 的 h1 數量不是 1')
    # 這一頁的核心價值在「明說不存在什麼」，缺了就失去意義
    for must in ['沒有 OAuth 授權伺服器', '沒有 MCP server', '沒有公開寫入 API']:
        if must not in html:
            raise SystemExit(f'developers.html 缺少必要聲明：{must}')
    print(f'{"待產生" if check else "已產生"} /developers  {len(html)/1024:.1f} KB')


if __name__ == '__main__':
    main()
