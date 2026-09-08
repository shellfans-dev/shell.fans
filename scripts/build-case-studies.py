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
                         '觀測。'),
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
#
# 敘事順序刻意不是「技術報告」的順序。主要讀者是企業主與行銷負責人，
# 不是 AEO 工程師：先講背景與做了什麼，再講 AI 的行為出現什麼變化，
# 最後才是方法與判讀方式。精確的技術數值仍然保留，但收進「技術驗證」
# 的可摺疊區塊，不打斷主線。
# ---------------------------------------------------------------------------

CARDS = '''<div class="sf-obs-cards" style="display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));margin:8px 0 20px">
  <div style="border:1px solid var(--border,#E8E5DE);border-radius:12px;padding:20px">
    <p style="margin:0;font-size:0.85rem;color:var(--text-secondary)">AI 回答提到品牌</p>
    <p style="margin:6px 0 0;font-size:1.6rem;font-weight:600;line-height:1.3">13%<span style="opacity:.45;margin:0 6px">→</span>19%</p>
    <p style="margin:4px 0 0;font-size:0.8rem;color:var(--text-secondary)">8/27 → 9/7</p>
  </div>
  <div style="border:1px solid var(--border,#E8E5DE);border-radius:12px;padding:20px">
    <p style="margin:0;font-size:0.85rem;color:var(--text-secondary)">AI 引用官方網站</p>
    <p style="margin:6px 0 0;font-size:1.6rem;font-weight:600;line-height:1.3">16%<span style="opacity:.45;margin:0 6px">→</span>28%</p>
    <p style="margin:4px 0 0;font-size:0.8rem;color:var(--text-secondary)">8/27 → 9/7</p>
  </div>
  <div style="border:1px solid var(--border,#E8E5DE);border-radius:12px;padding:20px">
    <p style="margin:0;font-size:0.85rem;color:var(--text-secondary)">AI 爬蟲抓取</p>
    <p style="margin:6px 0 0;font-size:1.15rem;font-weight:600;line-height:1.5">四個核心頁<br>皆已被多種 AI 爬蟲抓取</p>
    <p style="margin:4px 0 0;font-size:0.8rem;color:var(--text-secondary)">8/28 起</p>
  </div>
</div>'''

MODEL_DETAILS = '''<details style="margin:14px 0;border:1px solid var(--border,#E8E5DE);border-radius:10px;padding:14px 18px">
  <summary data-not-heading="1" style="cursor:pointer;font-weight:600">查看量測條件與模型版本</summary>
  <div style="margin-top:12px">
    <table class="sf-dim-table"><caption>本專案期間的量測條件</caption>
      <thead><tr><th scope="col">量測日</th><th scope="col">Claude 側</th><th scope="col">ChatGPT 側</th></tr></thead>
      <tbody>
        <tr><th scope="row">2026-08-07</th><td>claude-sonnet-5</td><td>gpt-4o-mini-search-preview</td></tr>
        <tr><th scope="row">2026-08-12 ~ 08-24</th><td>claude-haiku-4-5</td><td>gpt-4o-mini-search-preview</td></tr>
        <tr><th scope="row">2026-08-27 起</th><td>claude-haiku-4-5</td><td>gpt-5-search-api</td></tr>
      </tbody>
    </table>
    <p style="margin-top:12px;font-size:0.92rem;line-height:1.9">兩次調整的原因不同：Claude 側是執行頻率與成本的取捨；ChatGPT 側則是 OpenAI 於八月下架了原本使用的模型（8 月 24 日該平台整輪 38 題全部失敗，已在紀錄中標記）。本頁比較的 8/27、8/31、9/7 三次量測，使用的是同一組模型與同一份題組。</p>
  </div>
</details>'''

TECH_DETAILS = '''<details style="margin:14px 0;border:1px solid var(--border,#E8E5DE);border-radius:10px;padding:14px 18px">
  <summary data-not-heading="1" style="cursor:pointer;font-weight:600">查看技術驗證細節</summary>
  <div style="margin-top:12px">
    <table class="sf-dim-table"><caption>四個核心頁的實測結果（2026-09-08）</caption>
      <thead><tr><th scope="col">頁面</th><th scope="col">標題結構</th><th scope="col">結構化資料</th><th scope="col">canonical</th></tr></thead>
      <tbody>
        <tr><th scope="row"><a href="https://www.cet-taiwan.com/about-cet-kite" target="_blank" rel="noopener">/about-cet-kite</a></th><td>h1×1、h2×8、h3×9</td><td>JSON-LD 6 節點</td><td>自我指向</td></tr>
        <tr><th scope="row"><a href="https://www.cet-taiwan.com/about-cet-style-jet" target="_blank" rel="noopener">/about-cet-style-jet</a></th><td>h1×1、h2×9、h3×11</td><td>JSON-LD 6 節點</td><td>自我指向</td></tr>
        <tr><th scope="row"><a href="https://www.cet-taiwan.com/kids-english-test-comparison" target="_blank" rel="noopener">/kids-english-test-comparison</a></th><td>h1×1、h2×9、h3×9</td><td>JSON-LD 6 節點</td><td>自我指向</td></tr>
        <tr><th scope="row"><a href="https://www.cet-taiwan.com/kids-english-exam" target="_blank" rel="noopener">/kids-english-exam</a></th><td>h1×1、h2×10、h3×11</td><td>JSON-LD 6 節點</td><td>自我指向</td></tr>
      </tbody>
    </table>
    <p style="margin-top:12px;font-size:0.92rem;line-height:1.9">結構化資料涵蓋 Organization、WebSite、WebPage、BreadcrumbList 與 FAQPage。站台層的 robots.txt、sitemap.xml、llms.txt、llms-full.txt 四份檔案於同日實測皆正常回應。</p>
  </div>
</details>'''

CET_PAGE = {
    'url': '/aeo/case-studies/cet-taiwan',
    'content_source': 'scripts/build-case-studies.py',
    'title': '師德文教 CET：從 AI 可讀性整備到 AI 引用｜ShellFans AEO 案例',
    'h1': '師德文教 CET：從 AI 可讀性整備到 AI 引用的 AEO 專案紀錄',
    'eyebrow': 'AEO 案例 · 進行中',
    'desc': ('師德文教 CET 自 2026 年 8 月起進行 AEO 優化，重構四個兒童英語檢定核心頁面。'
             '本頁記錄技術整備完成後，AI 爬蟲、官網引用與品牌提及三種訊號的階段性觀測。'),
    'lede': ('師德文教自 2026 年 8 月開始進行 AEO 優化，第一階段聚焦於讓兒童英語檢定'
             '相關內容更容易被 AI 搜尋系統讀取、理解與引用。技術整備完成後，'
             '我們開始分別觀察 AI 爬蟲、官方網站引用與品牌提及三種訊號。'
             '專案仍在進行中，以下是階段性觀測。'),
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
            'eyebrow': None,
            'id': 'observation',
            'h2': '目前觀察到的變化',
            'blocks': [
                ('html', CARDS),
                ('p', '以上為<strong>相同模型、相同題組、相同量測方式</strong>下的三次觀測結果，'
                      '不代表最終專案成效。三個指標的定義如下：'),
                ('ul', [
                    '<strong>品牌提及率</strong>——AI 回答中是否主動出現「師德文教」或「CET」等品牌名稱',
                    '<strong>官方引用率</strong>——AI 回答的引用來源中是否包含 cet-taiwan.com',
                    '<strong>歸因落差</strong>——AI 用了官方資料、卻沒有同時說出品牌名稱的差距',
                ]),
                ('p', '提問時<strong>不含品牌名</strong>，用意是檢驗「使用者沒有指名師德時，'
                      'AI 會不會主動提到或引用」——那才是新客戶真正會問的方式。'),
            ],
        },
        {
            'eyebrow': None,
            'id': 'background',
            'h2': '專案背景',
            'blocks': [
                ('p', '師德文教（CET Taiwan）是台灣的兒童英語檢定與英語教學專業服務機構，'
                      '網站內容涵蓋檢定說明、教學資源與教師專業發展。'
                      '專案自 2026 年 8 月 5 日啟動，本頁資料截至 9 月 7 日的最近一次量測。'),
                ('h3', '為什麼兒童英語檢定網站需要 AEO'),
                ('p', '家長與教師在選擇兒童英檢時，問的多半是比較與選擇型的問題——'
                      '「幼兒適合哪一種英文檢定」「STYLE/JET 和劍橋 YLE 有什麼不同」'
                      '「國小英文檢定該怎麼選」。這類問題現在很常直接問 AI，'
                      '而不是逐一開啟搜尋結果比對。'),
                ('p', '如果官方網站的內容無法被 AI 正確讀取與歸因，'
                      '使用者拿到的答案就會來自二手整理、討論區或同業內容——'
                      '即使官方網站上有更完整、更正確的資訊。'),
            ],
        },
        {
            'eyebrow': None,
            'id': 'what-we-did',
            'h2': '我們實際做了什麼',
            'blocks': [
                ('p', '我們不是大量新增文章，而是先針對家長與教師實際會詢問的主題，'
                      '重構四個核心頁面，讓每個重要問題都有清楚、可獨立擷取的答案。'),
                ('ul', [
                    '<strong>問題式標題</strong>——把使用者會問的問題直接寫成標題，'
                    '而不是用行銷標語',
                    '<strong>答案緊接在下</strong>——每個問題下方先給一段可獨立成立的答案，'
                    '讀者與 AI 都不必讀完整頁才能得到結論',
                    '<strong>純 HTML 可讀</strong>——主要內容存在於原始 HTML 中，'
                    '不依賴 JavaScript 才顯示',
                    '<strong>結構化資料</strong>——讓 AI 能確定這頁在講什麼、由誰發布',
                    '<strong>canonical 與內部連結</strong>——避免同一份內容有多個網址競爭',
                    '<strong>站台層檔案</strong>——robots.txt、sitemap.xml、llms.txt、llms-full.txt',
                ]),
                ('html', TECH_DETAILS),
            ],
        },
        {
            'eyebrow': None,
            'id': 'ai-behaviour',
            'h2': '一個月後，AI 的行為出現哪些變化',
            'blocks': [
                ('h3', 'AI 爬蟲開始抓取新的核心頁'),
                ('p', '自 8 月 28 日起，四個核心頁面都開始出現 AI 爬蟲的實際抓取紀錄。'
                      '依頁面不同，目前各頁可觀察到 6 至 7 種 AI 爬蟲，累計抓取約 9 至 12 次。'
                      '站台整體共觀察到 13 種 AI 爬蟲身分，包含 GPTBot、OAI-SearchBot、'
                      'ChatGPT-User、ClaudeBot、Claude-User、Claude-SearchBot、PerplexityBot、'
                      'Google-Extended、Meta-ExternalAgent、Amazonbot、Bytespider、CCBot 與 cohere-ai。'),
                ('p', '不過<strong>爬蟲來過不等於會被引用</strong>。爬蟲到站只代表內容被取得，'
                      'AI 是否在回答中使用它、是否說出來源，是另外兩件事。'
                      '因此我們把三者分開觀測，不用其中一項推論另一項。'),
                ('h3', '被引用的比例上升，但提及品牌的比例上升得比較慢'),
                ('table', {
                    'caption': '同一量測條件下的三次觀測（不含品牌名的提問）',
                    'cols': ['量測日', 'AI 回答提到品牌', 'AI 引用官方網站', '歸因落差'],
                    'rows': [
                        ['2026-08-27', '13%', '16%', '3%'],
                        ['2026-08-31', '16%', '22%', '6%'],
                        ['2026-09-07', '19%', '28%', '9%'],
                    ],
                }),
                ('p', '引用率從 16% 上升到 28%，提及率從 13% 上升到 19%——'
                      '兩者都往上，但引用跑得比提及快，因此歸因落差也跟著從 3% 擴大到 9%。'
                      '這個現象在下一節會更明顯。'),
                ('p', '專案早期曾調整 AI 能見度的量測模型，因此八月初與現在的結果'
                      '不適合直接當作 Before / After。本頁只比較 8/27、8/31、9/7 這三次'
                      '使用相同模型、相同題組與相同量測方式的結果。'),
                ('html', MODEL_DETAILS),
            ],
        },
        {
            'eyebrow': None,
            'id': 'platforms',
            'h2': 'ChatGPT 與 Claude 呈現不同的品牌歸因模式',
            'blocks': [
                ('p', '同一次量測（2026-09-07）中，兩個平台的表現差異很明顯：'),
                ('table', {
                    'caption': '2026-09-07 各平台觀測',
                    'cols': ['平台', 'AI 回答提到品牌', 'AI 引用官方網站', '歸因落差'],
                    'rows': [
                        ['ChatGPT', '37%', '24%', '−13%'],
                        ['Claude', '18%', '50%', '+32%'],
                    ],
                }),
                ('p', '<strong>ChatGPT</strong> 提到品牌的比例較高，但引用官網的比例較低——'
                      '它比較常憑既有知識回答，較少附上來源連結。'),
                ('p', '<strong>Claude</strong> 剛好相反：一半的回答引用了師德官網作為來源，'
                      '但只有 18% 的回答提到師德這個品牌名稱。'
                      '這代表 Claude 已經大量使用師德官網內容作為回答依據，'
                      '但仍有不少回答沒有明確說出資訊來自師德。'),
                ('p', '兩者的差異很大，因此分平台解讀比直接平均更有意義——'
                      '平均之後得到的數字，對哪一邊都不準確。'),
            ],
        },
        {
            'eyebrow': None,
            'id': 'cited',
            'h2': 'AI 已經引用哪些師德內容',
            'blocks': [
                ('p', '2026-09-07 的量測中，AI 回答引用了師德官網的多個網址，'
                      '包含首頁、檢定說明、關於我們、教學資源，'
                      '以及本專案優化的目標頁之一 '
                      + code('/kids-english-test-comparison') + '。'),
                ('p', '目標頁進入 AI 的引用來源，代表新的 AEO 內容已經被實際採用，'
                      '而不只是被抓取而已。'),
                ('h3', '主題別的表現差異很大'),
                ('table', {
                    'caption': '各主題的觀測結果（2026-09-07 單次量測）',
                    'cols': ['主題', 'AI 提到品牌', 'AI 引用官網'],
                    'rows': [
                        ['檢定資訊查詢型', '33%', '58%'],
                        ['推薦與比較型', '33%', '33%'],
                        ['英語檢定選擇型', '20%', '60%'],
                        ['英語教師進修型', '17%', '8%'],
                        ['教材與教具需求型', '14%', '14%'],
                        ['學校與機構合作型', '0%', '0%'],
                    ],
                }),
                ('p', '「檢定資訊查詢型」與「英語檢定選擇型」的引用率明顯高於提及率——'
                      'AI 已經在用官網內容作答，只是沒說是誰提供的。'
                      '這種情況通常比「完全沒有能見度」更容易改善。'
                      '「學校與機構合作型」目前兩項都是 0%，這一類問題還沒有對應的內容落點。'),
            ],
        },
        {
            'eyebrow': None,
            'id': 'crawler-health',
            'h2': '爬蟲健康度：AI 要的東西，有沒有拿到',
            'blocks': [
                ('p', '除了「有沒有來」，也要看「來了有沒有拿到東西」。'),
                ('p', '<strong>四個核心頁的表現是乾淨的</strong>：至今累計 40 次 AI 爬蟲抓取，'
                      '全部正常回應，沒有任何一次失敗。'),
                ('p', '整站層面則有一個待處理的項目：約 <strong>15%</strong> 的 AI 爬蟲請求'
                      '指向已經下架的舊網址——主要是舊版 '
                      + code('.asp') + ' 頁面與早期的電子報 PDF。'
                      '那些網址還留在 AI 的既有知識或外部連結中，但網站早已改版。'),
                ('p', '處理方向是為仍有外部連結的舊網址建立對應的轉址，'
                      '把這部分抓取量導回現有內容，而不是讓它繼續落空。'),
                ('note', '另有一部分請求是掃描常見敏感路徑的探測行為（例如設定檔、金鑰檔），'
                         '那不是內容請求，也不影響網站的內容可讀性，因此不列入上述比例。'),
            ],
        },
        {
            'eyebrow': None,
            'id': 'next',
            'h2': '下一階段：從「被引用」走向「被歸因」',
            'blocks': [
                ('p', '第一階段要回答的問題是：<strong>AI 能不能取得並理解這些內容？</strong>'
                      '從爬蟲紀錄與引用率來看，這一段已經在發生。'),
                ('p', '第二階段的問題不同：<strong>AI 使用這些內容時，'
                      '會不會把答案正確歸因給師德？</strong>'
                      'Claude 的 50% 引用率配上 18% 提及率，就是這個問題最清楚的例子。'),
                ('p', '因此下一階段的重點不再是增加爬蟲造訪，而是：'),
                ('ul', [
                    '強化「師德文教 / CET」的品牌實體訊號，讓 AI 更容易確定內容出自誰',
                    '針對引用率高於提及率的主題，調整答案段落中的來源標示方式',
                    '補強站內的實體關聯，讓品牌名與檢定名之間的關係更明確',
                    '累積可被驗證的第三方提及——推薦類問題特別依賴這一項，'
                    '單靠自有網站的內容品質有其上限',
                    '為「學校與機構合作型」等目前無覆蓋的主題建立內容落點',
                    '持續以相同條件量測，累積足夠的觀測點',
                ]),
                ('p', '這些做法能提高被正確理解與歸因的機會，但不保證特定的結果——'
                      '最終是否引用、是否提及品牌，由各 AI 平台決定。'),
            ],
        },
        {
            'eyebrow': None,
            'id': 'method',
            'h2': 'ShellFans 的執行方法',
            'blocks': [
                ('ol', [
                    '<strong>建立基準</strong>——啟用 AI 爬蟲監測，記錄哪些 AI 系統來過、'
                    '抓了什麼、拿到什麼',
                    '<strong>問題對應</strong>——把使用者實際會問的問題分類，'
                    '對應到應該回答它的頁面',
                    '<strong>技術整備</strong>——標題結構、結構化資料、canonical、站台層檔案',
                    '<strong>內容重構</strong>——問題作為標題、答案緊接在下',
                    '<strong>實體建立</strong>——讓 AI 能確定內容屬於哪一個組織',
                    '<strong>能見度量測</strong>——用固定題組定期向各 AI 平台提問並分析回答',
                    '<strong>依結果迭代</strong>——調整依據是量測結果，不是猜測',
                ]),
                ('p', '各階段的速度差很多：爬取權限的改變可在數日內生效，'
                      '內容被擷取通常要數週，而 AI 是否主動提到品牌牽涉實體識別與外部佐證，'
                      '時間更長。完整說明見' + a('/aeo/implementation', 'AEO 導入流程')
                      + '，評分方式見' + a('/aeo-geo/methodology', 'AI Readiness Score 方法論') + '。'),
            ],
        },
        {
            'eyebrow': None,
            'id': 'how-to-read',
            'h2': '怎麼解讀這些數據',
            'blocks': [
                ('p', '這是進行中專案的階段性紀錄，不是最終成效驗收。'
                      '判讀時有幾點需要留意：'),
                ('ul', [
                    '<strong>三個訊號要分開看。</strong>爬蟲造訪不等於被引用，'
                    '被引用也不等於會提到品牌名稱。三者的變化速度不同。',
                    '<strong>量測條件必須一致才能比較。</strong>本頁只比較使用相同模型與'
                    '相同題組的三次觀測；跨模型的數字差異無法單獨歸因於網站優化。',
                    '<strong>AI 的回答是動態的。</strong>同一個問題在不同時間、'
                    '不同措辭、不同地區都可能得到不同答案。',
                    '<strong>目前的觀測點還不多。</strong>三次量測、跨 11 天，'
                    '足以看出方向，但要判定為穩定趨勢仍需持續累積。',
                    '<strong>本案例沒有追蹤招生或營收成效。</strong>那些指標本專案未量測，'
                    '因此頁面上不會出現相關數字。',
                ]),
                ('p', 'ShellFans 不保證任何 AI 平台一定引用、提及或推薦特定網站。'
                      '技術整備能提高被正確理解與引用的機會，最終決定權在各 AI 平台。'),
            ],
        },
    ],
    'faq_eyebrow': None,
    'faq': [
        ('AI 爬蟲來得多，就代表 AEO 有效嗎？',
         '不是。爬蟲造訪只代表內容被取得，不代表 AI 會在回答中使用它，'
         '更不代表會提到品牌名稱。本專案就把三者分開觀測——'
         '同一時間點，爬蟲活動穩定、引用率 28%、提及率 19%，三個數字並不同步。'),
        ('為什麼不能直接比較導入第一天與現在？',
         '因為專案早期調整過 AI 能見度的量測模型。跨模型的數字差異裡同時包含'
         '網站優化與量測工具改變，無法把差異單獨歸因於網站優化。'
         '本頁只比較使用相同模型與相同題組的三次觀測。'),
        ('AEO 通常要觀察多久？',
         '各階段速度不同。爬取權限的改變可在數日內生效；內容被擷取與引用通常需要數週；'
         '而 AI 是否主動提到品牌，牽涉實體識別與外部佐證，時間更長且不由網站單方面決定。'),
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
                   '預測。'),
    'disclaimer_short': '數據為特定量測條件下的階段性觀測。',
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
