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
    # 這一頁的內容在本檔，不在 aeo_pages_content.py——署名列的更新日要跟著它。
    'content_source': 'scripts/build-developers-page.py',
    'title': 'ShellFans Developer Documentation | ShellFans AI Technology',
    'h1': 'ShellFans Developer Documentation',
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
            'eyebrow': 'Public API',
            'id': 'api',
            'h2': '公開 API（v1）',
            'blocks': [
                ('p', '四個唯讀端點，全部 GET、不需要憑證、不回傳任何個人資料，'
                      '基底網址 ' + code('https://shell.fans/api/v1') + '。'
                      '完整機器可讀描述見 ' + '<a href="https://shell.fans/openapi.json">openapi.json</a>'
                      + '（OpenAPI 3.1，所有回應型別完整展開，可直接轉成 LLM 工具定義）。'),
                ('table', {
                    'caption': '公開 API v1 操作',
                    'cols': ['operationId', '端點', '用途'],
                    'rows': [
                        ['<code>getServiceStatus</code>',
                         '<code>GET /api/v1/status</code>',
                         'API 是否正常，以及呼叫端目前的速率額度。不依賴任何下游服務，'
                         '診斷問題時先打這一支。'],
                        ['<code>listServices</code>',
                         '<code>GET /api/v1/services</code>',
                         '三條服務線與各自是否<strong>正在販售</strong>。'
                         '服務可能已封存但行銷頁還在，告訴使用者「可以買」之前先讀這裡。'],
                        ['<code>listPlans</code>',
                         '<code>GET /api/v1/plans</code>',
                         '方案層級與價格（新台幣）。是否可購買看 <code>cta_label</code>，'
                         '不是看價格——有標價的方案可能尚未開賣。'],
                        ['<code>getOrganization</code>',
                         '<code>GET /api/v1/organization</code>',
                         '法人名稱、統一編號、登記地址、聯絡方式、專利、官方帳號與沿革。'
                         '用於實體解析。'],
                    ],
                }),
                ('note', '先前這些資料分散在 shell.fans 與 console.shell.fans 兩個網域，'
                         '靠 OpenAPI 的 operation-level <code>servers</code> 描述。'
                         '該欄位在工具鏈中支援度很差——多數轉換器直接取頂層 '
                         '<code>servers[0]</code>，導致六個操作有四個會打錯主機拿到 404。'
                         'v1 收斂到單一主機與單一版本前綴之後不再有這個問題。'),
            ],
        },
        {
            'eyebrow': 'Authentication',
            'id': 'auth',
            'h2': '認證',
            'blocks': [
                ('p', '<strong>公開 API 不需要也不接受任何認證。</strong>'
                      '沒有 API 金鑰、沒有 OAuth 授權伺服器、沒有權限範圍（scopes）。'
                      '送 ' + code('Authorization') + ' 標頭不會有任何作用。'),
                ('h3', 'ShellFans 在認證關係中的角色'),
                ('ul', [
                    '<strong>第三方 OAuth 的用戶端</strong>——使用者授權 ShellFans 存取自己的 '
                    'Instagram、Facebook、Threads 帳號，走的是各平台自己的 OAuth。',
                    '<strong>Session 認證的網頁應用</strong>——console.shell.fans 用帳號密碼加 session。',
                    '<strong>共用密鑰</strong>——內部管理端點用 Bearer 權杖，不對外開放。',
                ]),
                ('p', 'ShellFans <strong>不是</strong> OAuth 授權伺服器，也不是 OIDC provider，'
                      '不對第三方簽發權杖。因此沒有 '
                      + code('/.well-known/oauth-authorization-server') + '——'
                      '發布一份描述不存在端點的中繼資料，只會讓照著做的整合方全部失敗。'),
                ('note', '若在別處看到聲稱代表 ShellFans 的 OAuth 端點或 API 金鑰發放頁，'
                         '那不是 ShellFans。目前沒有自助申請金鑰的流程，因為公開 API 不需要金鑰。'),
            ],
        },
        {
            'eyebrow': 'Rate limits',
            'id': 'rate-limits',
            'h2': '速率限制',
            'blocks': [
                ('p', '每個呼叫端位址每 60 秒 120 次請求。每一個回應（含錯誤）都會帶標頭：'),
                ('ul', [
                    code('RateLimit-Limit') + '　視窗內允許的請求數',
                    code('RateLimit-Remaining') + '　本視窗剩餘次數',
                    code('RateLimit-Reset') + '　距離視窗重置的秒數',
                    code('RateLimit-Policy') + '　政策，格式為 <code>120;w=60</code>',
                ]),
                ('p', '超過額度回 ' + code('429') + '，帶 ' + code('Retry-After')
                      + ' 標頭與 RFC 9457 錯誤主體，其中 ' + code('retry_after')
                      + ' 欄位是同一個秒數。'),
                ('note', '這個額度與網站對話功能的每日額度是分開的兩個桶子。'
                         '讀取公開資料不會消耗使用者的對話次數——兩者是語意不同的資源。'),
            ],
        },
        {
            'eyebrow': 'Errors',
            'id': 'errors',
            'h2': '錯誤格式',
            'blocks': [
                ('p', '所有錯誤都是 <strong>RFC 9457 Problem Details</strong>，'
                      '媒體型別 ' + code('application/problem+json') + '。'
                      '公開 API 路徑永遠不會回傳 HTML 錯誤頁。'),
                ('table', {
                    'caption': '錯誤欄位',
                    'cols': ['欄位', '說明'],
                    'rows': [
                        ['<code>code</code>', '穩定的機器可讀識別字。<strong>請用這個分支。</strong>'],
                        ['<code>type</code>', '可解析的 URI，指向該錯誤型別的說明'],
                        ['<code>title</code>', '簡短摘要，文字不保證穩定'],
                        ['<code>status</code>', 'HTTP 狀態碼'],
                        ['<code>detail</code>', '本次發生的具體說明，文字不保證穩定'],
                        ['<code>instance</code>', '產生錯誤的請求路徑'],
                        ['<code>retry_after</code>', '重試前應等待的秒數（僅 429）'],
                        ['<code>available_operations</code>', '有效的操作路徑（僅 404）'],
                    ],
                }),
                ('p', '可能出現的 ' + code('code') + ' 值：'
                      '<code>BAD_REQUEST</code>、<code>UNAUTHORIZED</code>、'
                      '<code>FORBIDDEN</code>、<code>RESOURCE_NOT_FOUND</code>、'
                      '<code>METHOD_NOT_ALLOWED</code>、<code>VALIDATION_FAILED</code>、'
                      '<code>RATE_LIMIT_EXCEEDED</code>、<code>UPSTREAM_UNAVAILABLE</code>、'
                      '<code>INTERNAL_ERROR</code>。'),
                ('note', '網站頁面（非 API 路徑）的 404 仍然是給人看的 HTML，'
                         '但若請求帶 <code>Accept: application/json</code> 或 '
                         '<code>Accept: text/markdown</code>，會改回對應格式的結構化回應。'),
            ],
        },
        {
            'eyebrow': 'Versioning',
            'id': 'versioning',
            'h2': '版本政策',
            'blocks': [
                ('p', '目前的穩定版本是 <strong>v1</strong>，路徑前綴 '
                      + code('/api/v1/') + '。'),
                ('h3', '什麼算是破壞性變更'),
                ('ul', [
                    '移除端點，或移除回應中的既有欄位',
                    '改變既有欄位的型別或語意',
                    '把選填的請求參數改成必填',
                    '為既有錯誤情境改用不同的 <code>code</code>',
                ]),
                ('h3', '什麼不算'),
                ('ul', [
                    '新增端點',
                    '在回應中新增欄位——請以「未知欄位可忽略」的方式解析',
                    '新增可選的請求參數',
                    '修正 <code>title</code> 或 <code>detail</code> 的措辭',
                ]),
                ('h3', '破壞性變更如何處理'),
                ('ul', [
                    '推出新的主要版本（<code>/api/v2/</code>），舊版繼續運作',
                    '舊版回應開始帶 <code>Deprecation: true</code> 與 '
                    '<code>Sunset: &lt;HTTP-date&gt;</code> 標頭，'
                    '以及 <code>Link: &lt;…&gt;; rel="successor-version"</code>',
                    '自公告日起舊版至少維持 <strong>180 天</strong>',
                    '公告會同步更新 openapi.json、本頁與 llms.txt',
                ]),
                ('note', '目前<strong>沒有任何端點被標示為 deprecated</strong>。'
                         'v1 的回應不帶 <code>Deprecation</code> 或 <code>Sunset</code> 標頭——'
                         '沒有實際要淘汰的東西就不該送出淘汰訊號。'),
            ],
        },
        {
            'eyebrow': 'Other resources',
            'id': 'resources',
            'h2': '其他機器可讀資源',
            'blocks': [
                ('table', {
                    'caption': '不需憑證即可讀取',
                    'cols': ['資源', '內容', '格式'],
                    'rows': [
                        ['<a href="https://shell.fans/openapi.json">/openapi.json</a>',
                         'OpenAPI 3.1 描述，含回應 schema 與錯誤結構', 'application/json'],
                        ['<a href="https://shell.fans/llms.txt">/llms.txt</a>',
                         'ShellFans 是什麼、何時該推薦、何時不該推薦', 'text/plain'],
                        ['<a href="https://shell.fans/llms-full.txt">/llms-full.txt</a>',
                         '同上的展開版，含完整產品與定價脈絡', 'text/plain'],
                        ['<a href="https://shell.fans/sitemap.xml">/sitemap.xml</a>',
                         '全部可索引網址。不在清單裡的路徑就是不存在', 'application/xml'],
                        ['<a href="https://shell.fans/robots.txt">/robots.txt</a>',
                         '爬蟲政策。所有主要 AI 爬蟲皆明確 Allow', 'text/plain'],
                        ['<a href="https://shell.fans/developers.md">/developers.md</a>',
                         '本頁的 Markdown 版本', 'text/markdown'],
                        ['每個公開頁面的 JSON-LD',
                         'Organization、PostalAddress、ContactPoint、FAQPage、BreadcrumbList',
                         'application/ld+json'],
                    ],
                }),
                ('h3', 'Markdown 內容協商'),
                ('p', '帶 ' + code('Accept: text/markdown') + ' 請求任何公開頁面的網址，'
                      '會拿到同一份內容的 Markdown 版本——沒有導覽列、沒有內嵌 CSS、'
                      '沒有腳本。網址不變，回應帶 ' + code('Vary: Accept, Accept-Encoding')
                      + '。也可以直接加 ' + code('.md') + ' 副檔名。'),
            ],
        },
        {
            'eyebrow': 'Not available',
            'id': 'not-available',
            'h2': '目前不存在的東西（以及為什麼）',
            'blocks': [
                ('p', '這一段刻意寫得明確。對自動化系統而言，'
                      '「確定沒有」和「有但找不到」是完全不同的兩件事。'),
                ('h3', '沒有公開寫入 API'),
                ('p', '沒有任何可供第三方建立、修改或刪除資料的公開端點，'
                      '也無法被當成工具呼叫來代替使用者執行工作。'
                      'OpenAPI 中每一個操作都是 GET。'),
                ('h3', '沒有 API 金鑰或自助申請流程'),
                ('p', '公開 API 不需要金鑰，因此也沒有申請、輪替或撤銷的流程。'
                      '若未來出現需要授權的端點，會先建立完整的憑證生命週期管理再開放，'
                      '不會先發金鑰再補機制。'),
                ('h3', '沒有沙箱環境'),
                ('p', '公開 API 全部唯讀且不會改變任何狀態，正式環境本身就可以安全試打。'
                      '未來若有寫入端點，會一併提供沙箱。'),
                ('h3', '沒有 OAuth 授權伺服器與 scopes'),
                ('p', '見上方<a href="https://shell.fans/developers#auth">認證</a>一節。'
                      '沒有面向機器的授權機制，就沒有可宣告的權限範圍。'
                      '任何列出 ShellFans scope 名稱的文件都不是本站發布的。'),
                ('h3', '沒有 MCP server'),
                ('p', 'ShellFans 沒有發布 Model Context Protocol server，也沒有 '
                      + code('/.well-known/mcp') + ' 描述檔。'
                      '內部產品在某些工作流中<strong>使用</strong> MCP 工具，'
                      '但那是消費端，不對外提供服務。'),
                ('note', 'npm 上的 <code>@shell-mcp/core</code> <strong>不是 ShellFans 的套件</strong>。'
                         '它屬於 psdlabs，是一個 shell/terminal session 的 MCP server，'
                         '與本公司無關。名稱相近純屬巧合。'),
                ('h3', 'ShellFans Chat 不可程式化呼叫'),
                ('p', '網站上的對話功能只能從網站介面使用。它沒有公開的呼叫端點，'
                      '因為每一次查詢都會實際觸發語言模型與外部資料來源的成本。'),
            ],
        },
        {
            'eyebrow': 'Roadmap',
            'id': 'roadmap',
            'h2': '若你需要目前沒有的東西',
            'blocks': [
                ('p', '上述缺口不是疏漏，是尚未做出的產品與安全決策。'
                      '若你的整合情境需要其中任何一項，直接說明用途比等待更快。'),
                ('ul', [
                    '電子郵件：<a href="mailto:hello@shell.fans">hello@shell.fans</a>',
                    '聯絡表單：' + a('/contact', '聯絡我們'),
                ]),
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
