#!/usr/bin/env python3
"""
產生 AEO 案例頁與案例索引。

## 為什麼這是「進度案例」而不是「成效案例」

完整的驗證過程見 docs/aeo/cet-case-study-verification.md（不公開）。
關鍵結論：量測工具在專案期間變更過兩次——

    08-07（原 baseline）  claude-sonnet-5     + gpt-4o-mini-search-preview
    08-12 起              claude-haiku-4-5    + gpt-4o-mini-search-preview
    08-27 起              claude-haiku-4-5    + gpt-5-search-api

因此「9% → 19%」這種跨期比較不可發布：那個差值裡混合了網站實際改善、
模型換代與平台組合變動，無法拆解就不能宣稱。

本頁只呈現同一量測條件下的三次觀測（08-27／08-31／09-07），並明說
資料點少、期間短，不足以判定為穩定趨勢。

## 內容規則

每一個數字都必須能回溯到 crawler_access_logs、AI 能見度探測結果，或線上
HTML 的實際解析。不寫名次、市佔、招生、營收、詢問量——那些完全未量測。

用法：python3 scripts/build-case-studies.py [--check]
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

SITE = 'https://shell.fans'
CET = 'https://www.cet-taiwan.com'


def a(url, text):
    return '<a href="https://shell.fans%s">%s</a>' % (url, text)


def ext(url, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, text)


def code(s):
    return '<code>%s</code>' % s


# ---------------------------------------------------------------------------
# 索引頁
# ---------------------------------------------------------------------------

INDEX = {
    'url': '/aeo/case-studies',
    'content_source': 'scripts/build-case-studies.py',
    'title': 'AEO/GEO 實作案例｜ShellFans AI Technology',
    'h1': 'AEO/GEO 實作案例',
    'eyebrow': 'Case studies',
    'desc': ('ShellFans AEO/GEO 專案的公開實作紀錄。每一則都以實測資料為準，'
             '分開呈現技術整備、AI 爬蟲活動、引用與品牌提及，並標明量測條件與限制。'),
    'lede': ('這裡收錄 ShellFans 執行中或已完成的 AEO/GEO 專案紀錄。'
             '每一則案例都區分「已驗證的事實」「同一量測條件下的觀察」與'
             '「證據不足因此不作結論的部分」——把三者混為一談的案例，'
             '對讀者判斷沒有幫助。'),
    'schema': 'CollectionPage',
    'breadcrumb': [('AEO/GEO 知識中心', '/aeo'), ('實作案例', '/aeo/case-studies')],
    'cta': {'href': '/aeo/case-studies/cet-taiwan', 'label': '看師德文教 CET 案例'},
    'cta2': {'href': '/aeo-geo', 'label': 'AEO/GEO 代管服務'},
    'sections': [
        {
            'eyebrow': 'Published',
            'h2': '已發布的案例',
            'blocks': [
                ('h3', '師德文教 CET（cet-taiwan.com）— 專案進度紀錄'),
                ('p', '兒童英語檢定與英語教學專業機構。專案自 2026 年 8 月 5 日開始，'
                      '內容涵蓋四個目標頁的 AI 可讀性重構、站台層 AEO 檔案建置、'
                      'AI 爬蟲監測與能見度量測。'
                      + a('/aeo/case-studies/cet-taiwan', '閱讀完整紀錄') + '。'),
                ('note', '這是<strong>進度紀錄</strong>而非成效案例。專案期間量測工具'
                         '變更過兩次，跨期數字不可直接比較；頁內只呈現同一量測條件下的'
                         '觀測，並明列尚未改善的部分。'),
            ],
        },
        {
            'eyebrow': 'How we report',
            'h2': '案例怎麼寫',
            'blocks': [
                ('p', 'AEO 這個領域很容易寫出看起來很強、但無法查證的案例。'
                      'ShellFans 的案例頁遵守以下規則：'),
                ('ul', [
                    '每個數字都可回溯到爬蟲記錄、AI 能見度探測結果或線上 HTML 的實際解析',
                    '量測工具（模型、平台組合、題目）變更時明確標示，不做跨變更點的比較',
                    '爬蟲造訪、AI 引用、品牌提及三者分開呈現，不合併也不相除',
                    '列出仍未改善的部分——只寫成功的案例無法幫讀者判斷風險',
                    '不寫名次、市佔、招生數、營收或詢問量，除非該專案確實量測了它們',
                ]),
                ('p', '判定方法見' + a('/aeo-geo/methodology', 'ShellFans AI Readiness Score 方法論')
                      + '，服務範圍見' + a('/aeo-geo', 'AEO/GEO 代管') + '。'),
            ],
        },
    ],
    'faq': [
        ('案例中的數字可以驗證嗎？',
         '案例中的技術狀態（HTTP 狀態碼、標題結構、結構化資料、canonical、'
         'robots.txt/sitemap.xml/llms.txt）皆可由讀者自行對客戶網站查證。'
         'AI 爬蟲與能見度數據來自 ShellFans 的監測系統，頁內會標明量測期間與條件。'),
        ('為什麼案例會寫出還沒改善的部分？',
         'AEO 的成效鏈是「可抓取 → 被讀取 → 被引用 → 被歸因到品牌 → 被推薦」，'
         '各段速度不同。只呈現已改善的部分會讓讀者高估短期可得的結果。'),
    ],
    'related': [
        ('/aeo', 'AEO/GEO 知識中心'),
        ('/aeo-geo', 'AEO/GEO 代管服務'),
        ('/aeo-geo/methodology', '評分方法論'),
        ('/aeo/implementation', 'AEO 導入流程'),
    ],
    'disclaimer': ('案例內容經客戶同意公開品牌名稱與公開網址。所有數據為特定量測'
                   '條件下的觀測結果，不代表對其他網站或其他時間點的預測。'),
    'disclaimer_short': '案例數據為特定量測條件下的觀測，不構成對其他情境的預測。',
}


# ---------------------------------------------------------------------------
# CET 案例頁
# ---------------------------------------------------------------------------

CET_PAGE = {
    'url': '/aeo/case-studies/cet-taiwan',
    'content_source': 'scripts/build-case-studies.py',
    'title': '師德文教 CET AEO 專案進度紀錄｜ShellFans AI Technology',
    'h1': 'AEO 專案進度紀錄：師德文教 CET 的 AI 可讀性重構',
    'eyebrow': 'Case study · 進行中',
    'desc': ('師德文教 CET（cet-taiwan.com）AEO/GEO 專案的公開進度紀錄。'
             '涵蓋四個目標頁的 AI 可讀性重構、站台層 AEO 檔案、AI 爬蟲觀測與'
             '能見度量測，並標明量測條件變更與尚未改善的部分。'),
    'lede': ('這是一份<strong>進行中專案的進度紀錄</strong>，不是成效案例。'
             '專案自 2026 年 8 月 5 日開始，至本頁撰寫時約一個月。'
             '期間量測工具變更過兩次，因此本頁不做跨期比較，只呈現同一量測'
             '條件下的觀測，並完整列出尚未改善的部分。'),
    'schema': 'TechArticle',
    'breadcrumb': [('AEO/GEO 知識中心', '/aeo'), ('實作案例', '/aeo/case-studies'),
                   ('師德文教 CET', '/aeo/case-studies/cet-taiwan')],
    'about_entity': {
        '@type': 'Organization',
        '@id': 'https://www.cet-taiwan.com/#organization',
        'name': '師德文教',
        'alternateName': ['CET Taiwan', 'CET', '師德文教股份有限公司'],
        'url': 'https://www.cet-taiwan.com/',
        'description': '台灣的兒童英語檢定與英語教學專業服務機構。',
    },
    'cta': {'href': '/aeo-geo', 'label': '免費 AEO/GEO 現況評分'},
    'cta2': {'href': '/aeo/implementation', 'label': '了解導入流程'},
    'sections': [
        {
            'eyebrow': 'Summary',
            'id': 'summary',
            'h2': '一分鐘摘要',
            'blocks': [
                ('table', {
                    'caption': '專案概況',
                    'cols': ['項目', '內容'],
                    'rows': [
                        ['客戶', '師德文教 CET（' + ext(CET + '/', 'cet-taiwan.com') + '）'],
                        ['產業', '兒童英語檢定、英語教學專業服務'],
                        ['專案起始', '2026 年 8 月 5 日'],
                        ['本頁資料截止', '2026 年 9 月 7 日（最近一次能見度量測）'],
                        ['狀態', '<strong>進行中</strong>——尚未進入成效驗收階段'],
                        ['服務範圍', 'AI 可讀性重構、站台層 AEO 檔案、AI 爬蟲監測、能見度量測'],
                    ],
                }),
                ('note', '<strong>本頁刻意不呈現「導入前 vs 現在」的成效對比。</strong>'
                         '專案期間 AI 能見度的量測模型變更過兩次（見'
                         '<a href="#measurement">量測條件</a>一節），跨變更點的數字差異'
                         '同時包含網站改善與量測工具改變，無法拆解，因此不作為成效宣稱。'),
            ],
        },
        {
            'eyebrow': 'Client',
            'id': 'client',
            'h2': '客戶背景',
            'blocks': [
                ('p', '師德文教（CET Taiwan）是台灣的兒童英語檢定與英語教學專業服務機構，'
                      '網站內容涵蓋檢定說明、教學資源與教師專業發展。'),
                ('h3', '為什麼這類網站需要 AEO'),
                ('p', '家長與教師在選擇兒童英檢時，大量問題屬於「比較與選擇」——'
                      '「幼兒適合哪一種英文檢定」「STYLE/JET 和劍橋 YLE 有什麼不同」'
                      '「國小英文檢定該怎麼選」。這類問題現在很常直接問 AI，'
                      '而不是逐一開啟搜尋結果比對。'),
                ('p', '若官方網站的內容無法被 AI 正確讀取與歸因，'
                      '使用者得到的答案就會來自二手整理、討論區或競品內容——'
                      '即使官方網站上有更完整、更正確的資訊。'),
            ],
        },
        {
            'eyebrow': 'Scope',
            'id': 'scope',
            'h2': '實作範圍',
            'blocks': [
                ('p', '以下為本專案已完成並可由讀者自行查證的項目。'),
                ('h3', '四個目標頁的 AI 可讀性重構'),
                ('table', {
                    'caption': '目標頁與現況（2026-09-08 線上實測）',
                    'cols': ['頁面', '標題結構', '結構化資料', 'canonical'],
                    'rows': [
                        [ext(CET + '/about-cet-kite', '/about-cet-kite'),
                         'h1×1、h2×8、h3×9', 'JSON-LD 6 節點', '自我指向'],
                        [ext(CET + '/about-cet-style-jet', '/about-cet-style-jet'),
                         'h1×1、h2×9、h3×11', 'JSON-LD 6 節點', '自我指向'],
                        [ext(CET + '/kids-english-test-comparison', '/kids-english-test-comparison'),
                         'h1×1、h2×9、h3×9', 'JSON-LD 6 節點', '自我指向'],
                        [ext(CET + '/kids-english-exam', '/kids-english-exam'),
                         'h1×1、h2×10、h3×11', 'JSON-LD 6 節點', '自我指向'],
                    ],
                }),
                ('p', '結構化資料涵蓋 Organization、WebSite、WebPage、BreadcrumbList 與 FAQPage。'
                      '每頁採用「問題作為標題、答案緊接在下」的結構，讓 AI 能擷取到'
                      '獨立成立的答案段落，而不是必須讀完整頁才能推論。'),
                ('h3', '站台層 AEO 檔案'),
                ('ul', [
                    ext(CET + '/robots.txt', 'robots.txt') + '　AI 爬蟲存取政策',
                    ext(CET + '/sitemap.xml', 'sitemap.xml') + '　可索引網址清單',
                    ext(CET + '/llms.txt', 'llms.txt') + '　站台導覽與品牌實體說明',
                    ext(CET + '/llms-full.txt', 'llms-full.txt') + '　展開版',
                ]),
                ('note', '四份檔案於 2026-09-08 實測皆回 200 且中文編碼完整。'
                         '本專案早期曾出現 llms.txt 中文編碼損毀，已修復。'),
            ],
        },
        {
            'eyebrow': 'Crawler',
            'id': 'crawler',
            'h2': 'AI 爬蟲觀測',
            'blocks': [
                ('p', '<strong>爬蟲造訪不等於被引用。</strong>爬蟲到站只代表內容已被取得，'
                      '不代表 AI 一定會在回答中使用它、更不代表會提到品牌名稱。'
                      '因此本專案把爬蟲、引用、品牌提及三者分開觀測，不合併計算，'
                      '也不用其中一項推論另一項。'),
                ('h3', '目標頁的爬蟲活動'),
                ('p', '四個目標頁自 <strong>2026 年 8 月 28 日</strong>起開始被 AI 爬蟲抓取，'
                      '至 9 月 7 日止，每頁各被 <strong>6 至 7 種</strong>不同的 AI 爬蟲'
                      '抓取 <strong>9 至 12 次</strong>。'),
                ('p', '站台整體共觀察到 <strong>13 種</strong> AI 爬蟲身分：'
                      'GPTBot、OAI-SearchBot、ChatGPT-User、ClaudeBot、Claude-User、'
                      'Claude-SearchBot、PerplexityBot、Google-Extended、'
                      'Meta-ExternalAgent、Amazonbot、Bytespider、CCBot 與 cohere-ai。'),
                ('note', '本專案<strong>沒有</strong>「導入前」的爬蟲基準——'
                         '監測系統與專案同日（2026-08-05）啟用。因此無法宣稱'
                         '「爬蟲造訪較導入前增加」，本頁也不作此宣稱。'),
            ],
        },
        {
            'eyebrow': 'Measurement',
            'id': 'measurement',
            'h2': '量測條件（為什麼本頁不做跨期比較）',
            'blocks': [
                ('p', 'AI 能見度是用固定題組向各 AI 平台提問、再分析回答內容測得的。'
                      '這個方法有一個必須誠實面對的限制：'
                      '<strong>當量測用的模型或平台組合改變時，前後數字就不可比較。</strong>'),
                ('table', {
                    'caption': '本專案期間的量測條件變更',
                    'cols': ['量測日', 'Claude 側模型', 'ChatGPT 側模型'],
                    'rows': [
                        ['2026-08-07', 'claude-sonnet-5', 'gpt-4o-mini-search-preview'],
                        ['2026-08-12 ~ 08-24', 'claude-haiku-4-5', 'gpt-4o-mini-search-preview'],
                        ['2026-08-27 起', 'claude-haiku-4-5', 'gpt-5-search-api'],
                    ],
                }),
                ('p', '兩次變更的原因不同：Claude 側是成本與執行頻率的調整；'
                      'ChatGPT 側則是 OpenAI 於 8 月下架了原本使用的模型'
                      '（8 月 24 日該平台整輪 38 題全部失敗，已在紀錄中標記）。'),
                ('p', '因此「8 月 7 日 vs 9 月 7 日」的差異裡同時包含網站實際改善、'
                      '模型換代與平台組合變動。這三者無法拆解，'
                      '<strong>所以本頁不使用該對比作為成效宣稱</strong>。'),
            ],
        },
        {
            'eyebrow': 'Observation',
            'id': 'visibility',
            'h2': '同一量測條件下的觀測',
            'blocks': [
                ('p', '以下三次量測共用同一組條件（claude-haiku-4-5 + gpt-5-search-api、'
                      '同一題組、同一平台組合），彼此之間可以比較。'
                      '題目為不含品牌名的一般性問題，用以檢驗「使用者沒有指名品牌時，'
                      'AI 會不會主動提到或引用」。'),
                ('table', {
                    'caption': '不含品牌名問題的觀測結果（同一量測條件）',
                    'cols': ['量測日', 'AI 回答提到品牌', 'AI 引用官網', '歸因落差'],
                    'rows': [
                        ['2026-08-27', '13%', '16%', '3%'],
                        ['2026-08-31', '16%', '22%', '6%'],
                        ['2026-09-07', '19%', '28%', '9%'],
                    ],
                }),
                ('note', '<strong>這三個點呈上升，但不足以判定為穩定趨勢。</strong>'
                         '只有 3 個資料點、跨 11 天；以本專案的題組規模，'
                         '19% 與 13% 的差距約相當於 4 個題目。以這個樣本量無法區分'
                         '真實改善與一般波動。需要更多同條件的觀測點才能下結論。'),
                ('h3', '兩個平台的問題方向相反'),
                ('p', '同一次量測（2026-09-07）中：'),
                ('ul', [
                    '<strong>ChatGPT</strong>　提到品牌 37%、引用官網 24%'
                    '——提及多於引用，歸因落差為負',
                    '<strong>Claude</strong>　提到品牌 18%、引用官網 50%'
                    '——大量引用官網內容卻不說明來自誰，歸因落差 +32%',
                ]),
                ('p', '把兩者平均會得到一個對任何一邊都不成立的數字，'
                      '因此必須分平台呈現。這兩種情況需要的處理方式也不同。'),
                ('h3', '主題分類表現'),
                ('table', {
                    'caption': '各主題的觀測結果（2026-09-07 單次量測）',
                    'cols': ['主題分類', 'AI 提到品牌', 'AI 引用官網'],
                    'rows': [
                        ['檢定資訊查詢型', '33%', '58%'],
                        ['推薦與比較型', '33%', '33%'],
                        ['英語檢定選擇型', '20%', '60%'],
                        ['英語教師進修型', '17%', '8%'],
                        ['教材與教具需求型', '14%', '14%'],
                        ['學校與機構合作型', '0%', '0%'],
                    ],
                }),
                ('p', '「檢定資訊查詢型」與「英語檢定選擇型」的引用率明顯高於提及率'
                      '——AI 已在使用官網內容作答，但沒有說明來源是師德文教。'
                      '這類情況通常比「完全沒有能見度」更容易改善。'),
            ],
        },
        {
            'eyebrow': 'Evidence',
            'id': 'evidence',
            'h2': '實際被引用的內容',
            'blocks': [
                ('p', '2026-09-07 的量測中，AI 回答引用了師德文教官網的多個網址，'
                      '包含首頁、檢定說明、關於我們、教學資源，以及本專案新建的'
                      + code('/kids-english-test-comparison') + '。'),
                ('p', '同一輪中有 <strong>11 題</strong>屬於「引用了官網內容、'
                      '但回答中沒有提到師德文教」——全部來自 Claude。'
                      '典型的題目包括「幼兒適合參加哪種英文檢定」「兒童英檢有哪些種類」'
                      '「STYLE/JET、KITE 和劍橋 YLE 有什麼不同」。'),
                ('note', '完整題組屬 ShellFans 的量測方法論，本頁只公開主題分類與'
                         '代表性題目，不公開全部題目原文。'),
            ],
        },
        {
            'eyebrow': 'Gaps',
            'id': 'gaps',
            'h2': '尚未改善的部分',
            'blocks': [
                ('p', '一份只寫成功的案例，對讀者判斷風險沒有幫助。以下是本專案'
                      '目前確實存在、且已量測到的問題。'),
                ('h3', '約三分之一的 AI 爬蟲請求打到 404'),
                ('p', '專案期間的 AI 爬蟲請求中，<strong>36.2%</strong> 得到 404、'
                      '35.5% 得到 200。404 集中在舊版 '
                      + code('.asp') + ' 路徑——那些網址仍存在於 AI 的既有知識或外部連結中，'
                      '但網站早已改版。'),
                ('p', '這代表相當比例的爬取預算被消耗在取不到內容的請求上。'
                      '處理方向是為仍有外部連結的舊網址建立對應的轉址，'
                      '而不是單純讓它們繼續回 404。'),
                ('h3', 'Claude 上的歸因落差仍達 +32%'),
                ('p', 'Claude 大量引用官網內容但少提品牌名。這通常需要在內容中'
                      '更明確地建立「這份資料由誰提供」的訊號，'
                      '並強化可被第三方驗證的實體資訊。'),
                ('h3', '「學校與機構合作型」主題目前為 0%'),
                ('p', '該主題在 2026-09-07 的量測中，提及率與引用率皆為 0%。'
                      '這一類問題目前沒有對應的內容落點。'),
                ('h3', '推薦類問題仍需第三方佐證'),
                ('p', '當使用者問「推薦哪一個」時，AI 傾向引用被多個獨立來源提及的品牌。'
                      '自有網站的內容品質有其上限——這一段需要可驗證的外部提及，'
                      '屬於內容工程之外的工作。'),
            ],
        },
        {
            'eyebrow': 'Method',
            'id': 'method',
            'h2': '執行方法',
            'blocks': [
                ('ol', [
                    '<strong>建立基準</strong>——啟用 AI 爬蟲監測，記錄哪些 AI 系統來過、'
                    '抓了什麼、拿到什麼狀態碼',
                    '<strong>問題對應</strong>——把使用者實際會問的問題分類，'
                    '對應到應該回答它的頁面',
                    '<strong>技術整備</strong>——標題結構、結構化資料、canonical、'
                    '站台層 AEO 檔案',
                    '<strong>內容重構</strong>——問題作為標題、答案緊接在下，'
                    '讓答案能獨立被擷取',
                    '<strong>實體建立</strong>——讓 AI 能確定內容屬於哪一個組織',
                    '<strong>能見度量測</strong>——用固定題組定期向各 AI 平台提問並分析回答',
                    '<strong>迭代</strong>——依量測結果調整，而不是依猜測',
                ]),
                ('p', '各階段的速度不同：爬取權限的改變可在數日內生效，'
                      '而實體識別與引用習慣的改變需要更長時間，且不由網站單方面決定。'
                      '完整說明見' + a('/aeo/implementation', 'AEO 導入流程')
                      + '，評分方式見' + a('/aeo-geo/methodology', 'AI Readiness Score 方法論') + '。'),
            ],
        },
        {
            'eyebrow': 'Limitations',
            'id': 'limitations',
            'h2': '本頁數據的限制',
            'blocks': [
                ('ul', [
                    'AI 平台的回答是動態生成的，同一個問題在不同時間可能得到不同答案',
                    '爬蟲造訪不保證被引用；被引用不保證會提到品牌名稱',
                    'AI 能見度會隨平台、時間、問題措辭、地區與使用者的搜尋行為變動',
                    '本頁的觀測結果僅適用於所述的量測條件，不可外推到其他模型或平台組合',
                    '跨時間比較必須使用相同或等價的題組與模型，否則差異無法解讀',
                    '本專案未量測招生、詢問量、營收或任何商業成果，本頁亦不作此類宣稱',
                ]),
                ('note', 'ShellFans 不保證任何 AI 平台一定引用、提及或推薦特定網站。'
                         '技術整備能提高被正確理解與引用的機會，但最終決定權在各 AI 平台。'),
            ],
        },
        {
            'eyebrow': 'Next',
            'id': 'next',
            'h2': '下一階段',
            'blocks': [
                ('ul', [
                    '處理舊 <code>.asp</code> 路徑的 404，回收被浪費的爬取預算',
                    '針對 Claude 的歸因落差強化內容中的來源標示與實體訊號',
                    '為「學校與機構合作型」主題建立內容落點',
                    '持續累積同一量測條件下的觀測點，直到足以判定趨勢',
                ]),
                ('note', '下一次能見度量測預定為 <strong>2026 年 9 月 14 日</strong>'
                         '（每週一排程），將沿用與 08-27 起相同的題組與模型，'
                         '使結果可與本頁的三個觀測點併同比較。'),
            ],
        },
    ],
    'faq': [
        ('這個案例算成功嗎？',
         '目前還不能這樣說。專案進行約一個月，技術整備已完成並可查證，'
         'AI 爬蟲確實在抓取新建的頁面，同一量測條件下的三次觀測也呈上升——'
         '但資料點太少、期間太短，不足以判定為穩定趨勢。這是進度紀錄，不是成效驗收。'),
        ('為什麼不用「導入前 vs 現在」的對比？',
         '因為專案期間 AI 能見度的量測模型變更過兩次（Claude 側與 ChatGPT 側各一次）。'
         '跨變更點的數字差異同時包含網站改善與量測工具改變，無法拆解。'
         '用那個差值宣稱成效在方法上是不成立的。'),
        ('AI 爬蟲來得多，是不是就代表 AEO 有效？',
         '不是。爬蟲造訪只代表內容被取得。本專案的資料就是一個例子：'
         '爬蟲活動持續，但約三分之一的請求打到 404，而歸因落差在 Claude 上仍達 +32%。'
         '爬蟲、引用、品牌提及必須分開看。'),
        ('多久才會看到成效？',
         '各階段速度不同。爬取權限的改變可在數日內生效；'
         '內容被擷取與引用通常需要數週；而 AI 是否主動提到品牌，'
         '牽涉實體識別與外部佐證，時間更長且不由網站單方面決定。'
         'ShellFans 不對特定時程內的引用或推薦作保證。'),
    ],
    'related': [
        ('/aeo/case-studies', '其他實作案例'),
        ('/aeo-geo', 'AEO/GEO 代管服務'),
        ('/aeo/implementation', 'AEO 導入流程'),
        ('/aeo/ai-crawler-monitoring', 'AI 爬蟲監測'),
        ('/aeo-geo/methodology', '評分方法論'),
    ],
    'disclaimer': ('本頁經師德文教同意公開品牌名稱與公開網址。所有數據為 ShellFans 在'
                   '所述量測條件下的觀測結果，不代表對其他網站、其他時間點或其他 AI 平台的'
                   '預測。ShellFans 不保證任何 AI 平台一定引用、提及或推薦特定網站。'),
    'disclaimer_short': ('數據為特定量測條件下的觀測結果，不保證任何 AI 平台的引用或推薦。'),
}


def main():
    check = '--check' in sys.argv
    shell = extract_shell()
    out = []

    for page in (INDEX, CET_PAGE):
        html = build_page(page, shell)
        path = os.path.join(ROOT, page['url'].lstrip('/') + '.html')

        # 產出即驗證
        import json
        import re
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            json.loads(block)
        if html.count('<h1') != 1:
            raise SystemExit(f'{page["url"]}：h1 數量不是 1')
        # 禁用語彙——案例頁最容易滑向誇大
        for bad in ('保證', '第一名', '必然被', '一定會被引用', '大幅提升'):
            if bad in html and '不保證' not in html[max(0, html.find(bad) - 12):html.find(bad) + 8]:
                raise SystemExit(f'{page["url"]}：出現誇大用語「{bad}」')

        if not check:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, 'w', encoding='utf-8').write(html)
        out.append((page['url'], len(html) / 1024))

    print(f'{"待產生" if check else "已產生"} {len(out)} 頁')
    for u, kb in out:
        print(f'  {u:<36} {kb:.1f} KB')


if __name__ == '__main__':
    main()
