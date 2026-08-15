#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AEO 知識叢集內容定義。

## 撰寫原則（違反其中任何一條的內容都不該進來）

1. **不捏造**。沒有可驗證來源的價格、天數、客戶名稱、競品名單、引用率，一律
   不寫。需要但查不到的，用保守描述並在稽核文件標記「需人工確認」。
2. **不保證第三方行為**。llms.txt 或 Schema 都不能保證 ChatGPT 會引用你。
   任何頁面都不得暗示相反的事。
3. **前 100–150 字要直接回答標題的問題**，不鋪陳。AI 擷取的通常就是這一段。
4. **要寫限制與常見錯誤**。只寫優點的頁面對讀者沒用，對 AI 也沒有引用價值 ——
   可引用的往往正是「什麼情況下不適用」。
5. **每頁至少 3 條內部連結 + 1 個往服務／工具的 CTA**。

## 資料正確性註記

AI Readiness Score 的面向與配分以 saas_womm/src/lib/aeo-geo/scoring.ts 為準
（SCORING_VERSION = 'aeo_geo_score_v1'）：
crawlability 15、technical 15、structuredData 15、aeoAnswerReadiness 15、
geoEntitySignal 15、aiCrawlerReadiness 10、contentClarity 10、llmsTxt 5。
不要憑印象改寫這組數字 —— 網站自己的方法論頁寫錯自家配分，是權威頁最嚴重的錯誤。
"""

ORG_NAME = 'ShellFans AI Technology'
ORG_LOGO = 'https://shell.fans/images/nav_logo.svg'

# 共用連結
HUB = '/aeo'
CHECKER = '/tools/aeo-geo-checker'
SERVICE = '/aeo-geo'
METHOD = '/aeo-geo/methodology'
TOOLS = '/aeo-geo/taiwan-aeo-tools'
CONTACT = '/contact'
BRAND = '/what-is-shellfans'

CRUMB = [('AEO/GEO 知識中心', HUB)]

DISCLAIMER = (
    '<strong>說明：</strong>本頁內容為 ShellFans 依公開技術文件與實務經驗整理，'
    '用於協助網站主理解 AI 搜尋的運作方式。各 AI 平台的實際演算法、資料來源策略與'
    '引用邏輯由該平台自行決定且可能隨時調整；任何技術整備都無法保證特定 AI 平台的'
    '引用、推薦或排名。'
)

DISCLAIMER_SHORT = (
    '技術整備可提升網站被 AI 系統理解與引用的基礎條件，但不構成任何第三方 AI 平台的'
    '引用、推薦或排名保證。'
)

CTA_CHECK = {'href': CHECKER, 'label': '免費檢測我的網站'}
CTA_SERVICE = {'href': SERVICE, 'label': '了解 AEO Managed Hosting'}
CTA_CONTACT = {'href': CONTACT, 'label': '聯繫顧問討論'}
CTA_HUB = {'href': HUB, 'label': '回到 AEO 知識中心'}


def page(url, title, h1, eyebrow, desc, lede, schema, sections, faq, related,
         breadcrumb=None, cta=None, cta2=None, service_type=None):
    d = {
        'url': url, 'title': title, 'h1': h1, 'eyebrow': eyebrow, 'desc': desc,
        'lede': lede, 'schema': schema, 'sections': sections, 'faq': faq,
        'related': related, 'breadcrumb': breadcrumb if breadcrumb is not None else CRUMB,
        'cta': cta or CTA_CHECK, 'cta2': cta2 or CTA_SERVICE,
        'disclaimer': DISCLAIMER, 'disclaimer_short': DISCLAIMER_SHORT,
    }
    if service_type:
        d['service_type'] = service_type
    return d


def sec(eyebrow, h2, blocks):
    return {'eyebrow': eyebrow, 'h2': h2, 'blocks': blocks}


def a(url, text):
    return '<a href="https://shell.fans%s">%s</a>' % (url, text)


# 八個評分面向 —— 以程式碼為準，多處引用，集中定義避免各頁抄歪
SCORE_DIMENSIONS = [
    ['Crawlability<br><span style="font-weight:400;color:var(--text-tertiary);font-size:0.86rem">可爬取性</span>', '15',
     'HTTP 狀態、重新導向鏈、canonical、meta robots、sitemap.xml 是否正常回應。'],
    ['Technical<br><span style="font-weight:400;color:var(--text-tertiary);font-size:0.86rem">技術基礎</span>', '15',
     'HTTPS、行動裝置 viewport、首頁 HTML 體積是否消耗過多抓取預算。'],
    ['Structured Data<br><span style="font-weight:400;color:var(--text-tertiary);font-size:0.86rem">結構化資料</span>', '15',
     'Schema.org JSON-LD 是否存在、Organization 是否具備、FAQ 文案是否對應 FAQPage。'],
    ['Answer Readiness<br><span style="font-weight:400;color:var(--text-tertiary);font-size:0.86rem">答覆整備</span>', '15',
     '是否有問答式內容、meta description，以及可讀文字量是否足以擷取可引用段落。'],
    ['Entity Clarity<br><span style="font-weight:400;color:var(--text-tertiary);font-size:0.86rem">實體與信任訊號</span>', '15',
     'Organization 結構化資料、About、Contact 是否一致可驗證。Trust Signals 併入此項。'],
    ['AI Crawler Policy<br><span style="font-weight:400;color:var(--text-tertiary);font-size:0.86rem">爬蟲政策</span>', '10',
     'robots.txt 是否存在、是否誤擋 OAI-SearchBot／GPTBot／ClaudeBot／PerplexityBot。'],
    ['Content Clarity<br><span style="font-weight:400;color:var(--text-tertiary);font-size:0.86rem">內容結構</span>', '10',
     '是否有 title、是否恰有一個 H1、是否以 H2／H3 建立語意階層。'],
    ['llms.txt', '5', '是否提供 /llms.txt 摘要入口，以及其中是否具備 Markdown 標題結構。'],
]

SCORE_TABLE = ('table', {
    'caption': 'AI Readiness Score 面向與配分（aeo_geo_score_v1）',
    'cols': ['面向', '配分', '檢視內容'],
    'rows': SCORE_DIMENSIONS,
})


PAGES = []

# ---------------------------------------------------------------------------
# Hub
# ---------------------------------------------------------------------------
PAGES.append(page(
    url=HUB,
    title='AEO/GEO 知識中心｜答案引擎最佳化完整指南 - ShellFans',
    h1='AEO/GEO 知識中心',
    eyebrow='Knowledge Hub',
    desc='AEO（答案引擎最佳化）與 GEO（生成式引擎最佳化）的完整知識庫：定義、與 SEO 的差異、llms.txt、AI 爬蟲、Schema、實體清晰度，以及導入流程與費用結構。',
    lede='AEO（Answer Engine Optimization，答案引擎最佳化）是讓網站內容能被 ChatGPT、Perplexity、Claude、Google AI Overviews 等答案引擎正確理解並引用的做法。本知識中心收錄定義、技術實作、採購決策三類主題，每一頁都可獨立閱讀。',
    schema='CollectionPage',
    breadcrumb=[],
    sections=[
        sec('Start Here', '從哪裡開始', [
            ('p', '如果你是第一次接觸這個題目，建議依下列順序閱讀。三條路徑對應三種不同的問題。'),
            ('h3', '一、我想先搞懂名詞'),
            ('ul', [
                a('/aeo/what-is-aeo', 'AEO 是什麼') + ' — 答案引擎最佳化的定義與適用範圍',
                a('/aeo/what-is-geo', 'GEO 是什麼') + ' — 生成式引擎最佳化與 AEO 的關係',
                a('/aeo/aeo-vs-seo', 'AEO 與 SEO 的差異') + ' — 兩者的目標、指標與工作內容如何不同',
                a('/aeo/aeo-vs-geo', 'AEO 與 GEO 的差異') + ' — 為什麼這兩個詞經常被混用',
            ]),
            ('h3', '二、我要動手做技術整備'),
            ('ul', [
                a('/aeo/how-ai-search-works', '要怎麼讓 AI 正確理解我的網站') + ' — 三個環節與執行順序',
                a('/aeo/ai-crawler', 'AI 爬蟲總覽') + ' — 有哪些爬蟲、各自的用途與 robots.txt 寫法',
                a('/aeo/ai-crawler-monitoring', '如何檢查 AI 爬蟲來訪狀況') + ' — 三種做法與判讀陷阱',
                a('/aeo/llms-txt', 'llms.txt') + ' — 這份檔案是什麼、值不值得做',
                a('/aeo/schema', 'AEO 需要的 Schema') + ' — 哪些結構化資料真的有用',
                a('/aeo/entity-clarity', '實體清晰度') + ' — 讓 AI 確定「你是誰」',
                a('/aeo/answer-readiness', '答覆整備度') + ' — 讓內容具備可被擷取的形狀',
            ]),
            ('h3', '三、我在評估要不要委外'),
            ('ul', [
                a('/aeo/do-i-need-aeo', '公司網站需要做 AEO 嗎') + ' — 四個判斷準則與不適用情況',
                a('/aeo/cost', 'AEO 費用怎麼計算') + ' — 影響報價的變數',
                a('/aeo/implementation', 'AEO 導入流程') + ' — 實際會經歷哪些階段',
                a('/aeo/taiwan-companies', '台灣 AEO 服務商') + ' — 市場現況與評估準則',
                a('/aeo/how-to-choose-agency', '如何挑選 AEO 廠商') + ' — 該問哪些問題',
            ]),
        ]),
        sec('Measure First', '先量測，再決定要不要做', [
            ('p', '在讀完任何一篇之前，其實可以先花三十秒知道自己的起點在哪裡。'
                  'ShellFans 的 %s 會抓取你的網站，就八個面向給出 0–100 分，並列出具體待修項目。'
                  % a(CHECKER, 'AEO/GEO 免費檢測工具')),
            SCORE_TABLE,
            ('p', '各面向的判定細節與評級對照，見 %s。' % a(METHOD, 'AI Readiness Score 方法論')),
        ]),
        sec('Scope', '這個知識中心不涵蓋什麼', [
            ('p', '把邊界講清楚，比多寫幾頁有用。'),
            ('ul', [
                '<strong>不是 SEO 教學</strong>。傳統關鍵字研究、外部連結建置、Core Web Vitals 調校不在範圍內；那些仍然重要，但屬於另一個題目。',
                '<strong>不提供排名保證</strong>。沒有任何服務能保證 ChatGPT 或 Perplexity 引用特定網站，本站不做這種承諾。',
                '<strong>不做競品排名</strong>。%s 提供的是評估準則，不是廠商排行榜。' % a('/aeo/taiwan-companies', '台灣 AEO 服務商'),
            ]),
        ]),
    ],
    faq=[
        ('AEO 和 SEO 需要二選一嗎？',
         '不需要，而且不應該。AEO 的技術基礎（可爬取性、結構化資料、內容階層）與 SEO 高度重疊，多數項目做一次兩邊都受益。差別在於 AEO 額外要求內容具備「可直接被擷取成答案」的形狀，以及品牌實體的可辨識度。詳見 <a href="https://shell.fans/aeo/aeo-vs-seo">AEO 與 SEO 的差異</a>。'),
        ('做了這些，ChatGPT 就會推薦我嗎？',
         '不保證。技術整備決定的是「AI 能不能正確理解與引用你的網站」，屬於必要條件；是否實際被引用，取決於各 AI 平台自身的演算法、資料來源策略與當下的查詢情境。任何宣稱能保證 AI 引用的說法都不可信。'),
        ('我的網站很小，值得做 AEO 嗎？',
         '取決於你的客戶會不會用 AI 問到你的產品類別。頁數少不是問題——AEO 看重的是內容的清晰度與實體可辨識度，不是數量。可以先用免費檢測看基礎分數，再決定投入程度。'),
    ],
    related=[(CHECKER, '免費 AEO/GEO 檢測工具'), (METHOD, 'AI Readiness Score 方法論'),
             (SERVICE, 'AEO Managed Hosting'), (TOOLS, '台灣 AEO 工具比較')],
    cta=CTA_CHECK, cta2={'href': '/aeo/what-is-aeo', 'label': '從「AEO 是什麼」開始讀'},
))


# ---------------------------------------------------------------------------
# A. 定義與比較
# ---------------------------------------------------------------------------
PAGES.append(page(
    url='/aeo/what-is-aeo',
    title='AEO 是什麼？答案引擎最佳化完整說明 - ShellFans',
    h1='AEO 是什麼？',
    eyebrow='Definition',
    desc='AEO（Answer Engine Optimization，答案引擎最佳化）是讓網站內容能被 ChatGPT、Perplexity、Claude、Google AI Overviews 等答案引擎理解並引用的做法。本頁說明定義、運作方式、適用情境與限制。',
    lede='AEO 是 Answer Engine Optimization 的縮寫，中文稱「答案引擎最佳化」。指的是讓網站內容能被 ChatGPT、Perplexity、Claude、Google AI Overviews 這類會「直接給答案」的系統正確理解、擷取並引用的一整套做法。它關心的不是排名第幾，而是你的內容有沒有成為那個答案的一部分。',
    schema='TechArticle',
    sections=[
        sec('Why', '為什麼會出現這個題目', [
            ('p', '傳統搜尋給你十條藍色連結，使用者自己點進去看。答案引擎不同——它直接生成一段回答，並在旁邊標註幾個來源。'
                  '這個轉變帶來一個很具體的後果：<strong>沒有被引用，就等於不存在</strong>。使用者不會往下捲去找第十一個結果，因為根本沒有列表。'),
            ('p', '所以工作重心從「排到前面」變成「成為答案的材料」。這兩件事需要的技術準備有重疊，但不完全一樣。'),
        ]),
        sec('How', '答案引擎怎麼決定要引用誰', [
            ('p', '各家系統細節不同，但公開資訊與實務觀察指向三個共通環節：'),
            ('ol', [
                '<strong>取得</strong> — 爬蟲能不能順利抓到你的頁面。被 robots.txt 擋住、回 403、或內容要等 JavaScript 執行才出現，這一關就過不了。',
                '<strong>理解</strong> — 抓到之後，能不能判斷這頁在講什麼、是誰寫的、可不可信。結構化資料與清楚的標題階層在這裡發揮作用。',
                '<strong>擷取</strong> — 能不能從中切出一段「可以直接當答案」的文字。冗長、繞圈子、把重點藏在第五段的寫法，在這一關會吃虧。',
            ]),
            ('p', '這三關對應到 %s 的八個評分面向，可以用 %s 直接看自己卡在哪一關。'
                  % (a(METHOD, 'AI Readiness Score'), a(CHECKER, '免費檢測工具'))),
        ]),
        sec('Scope', 'AEO 實際包含哪些工作', [
            ('table', {
                'caption': 'AEO 的工作項目分類',
                'cols': ['層面', '具體工作', '參考'],
                'rows': [
                    ['爬蟲可達性', 'robots.txt 對 AI 爬蟲的規則、伺服器回應狀態、重新導向鏈、sitemap',
                     a('/aeo/ai-crawler', 'AI 爬蟲總覽')],
                    ['機器可讀性', 'Schema.org JSON-LD、Organization／FAQPage／BreadcrumbList',
                     a('/aeo/schema', 'AEO Schema')],
                    ['實體清晰度', '品牌名稱一致性、公司資訊可驗證、跨站提及一致',
                     a('/aeo/entity-clarity', '實體清晰度')],
                    ['答覆整備', '問答式段落、定義先行、比較表、限制說明',
                     a('/aeo/answer-readiness', '答覆整備度')],
                    ['摘要入口', 'llms.txt／llms-full.txt', a('/aeo/llms-txt', 'llms.txt')],
                ],
            }),
        ]),
        sec('Limits', '限制與常見誤解', [
            ('h3', '誤解一：做了 AEO 就會被 ChatGPT 推薦'),
            ('p', '不會。AEO 處理的是必要條件，不是充分條件。你可以把技術面做到滿分，但如果該領域已有更權威、更常被引用的來源，模型仍可能不選你。'
                  '任何宣稱能保證 AI 引用的服務，都應該直接排除。'),
            ('h3', '誤解二：AEO 是 SEO 的替代品'),
            ('p', '不是。兩者高度重疊且互補，多數技術項目做一次兩邊都受益。詳見 %s。' % a('/aeo/aeo-vs-seo', 'AEO 與 SEO 的差異')),
            ('h3', '誤解三：多發文章就是 AEO'),
            ('p', '大量薄內容對答案引擎沒有幫助，甚至有反效果——它會稀釋你的實體訊號，讓模型更難判斷你到底專精什麼。'
                  '一頁把一個問題講清楚，勝過十頁各講三成。'),
            ('h3', '誤解四：效果可以即時看到'),
            ('p', '不能。模型的知識更新有延遲，索引重抓也有週期。技術整備完成到觀察得到變化，通常以週為單位而非天。'
                  '這也是為什麼需要固定的觀測基準，而不是憑感覺判斷。'),
        ]),
    ],
    faq=[
        ('AEO 和 GEO 是同一件事嗎？',
         '不完全相同。AEO（答案引擎最佳化）著重內容能否被擷取成答案；GEO（生成式引擎最佳化）著重品牌實體在生成式模型中的可辨識度與被提及的方式。實務上兩者的工作大量重疊，多數服務會一起處理。詳見 <a href="https://shell.fans/aeo/aeo-vs-geo">AEO 與 GEO 的差異</a>。'),
        ('AEO 需要多久才看得到效果？',
         '沒有保證天數。影響變數包括網站原本的整備程度、內容更新頻率、各 AI 平台的重新抓取週期，以及該主題領域的競爭來源數量。技術整備本身通常數週內可完成，但要觀察到 AI 回答中的變化，需要以週為單位持續量測。'),
        ('小型網站也適用嗎？',
         '適用。AEO 的核心是清晰度而非規模——十頁把主題講清楚的網站，比一百頁模糊內容的網站更容易被正確引用。反而是大型網站常見的重複內容與模糊實體訊號會造成困擾。'),
        ('自己做得來嗎？',
         '技術基礎（robots.txt、Schema、標題階層、llms.txt）具備前端或 SEO 經驗的團隊多半可自行完成，本站的技術頁面都有具體做法。需要外部協助的通常是持續量測與內容結構調整。可先用免費檢測確認缺口大小再決定。'),
    ],
    related=[(HUB, 'AEO/GEO 知識中心'), ('/aeo/what-is-geo', 'GEO 是什麼'),
             ('/aeo/aeo-vs-seo', 'AEO 與 SEO 的差異'), (CHECKER, '免費檢測工具')],
))

PAGES.append(page(
    url='/aeo/what-is-geo',
    title='GEO 是什麼？生成式引擎最佳化完整說明 - ShellFans',
    h1='GEO 是什麼？',
    eyebrow='Definition',
    desc='GEO（Generative Engine Optimization，生成式引擎最佳化）指的是讓品牌與產品在生成式 AI 的回答中被正確辨識與提及。本頁說明定義、與 AEO 的分工、可量測的訊號與限制。',
    lede='GEO 是 Generative Engine Optimization 的縮寫，中文稱「生成式引擎最佳化」。重點在於：當使用者向 ChatGPT、Gemini、Claude 這類生成式模型詢問某個產品類別時，你的品牌會不會被主動列入候選，以及模型對你的描述是否正確。它處理的是「實體」層次的問題，而非單一頁面。',
    schema='TechArticle',
    sections=[
        sec('Distinction', 'GEO 與 AEO 的分工', [
            ('p', '兩者常被混用，但關心的對象不同。一個看頁面，一個看品牌。'),
            ('table', {
                'caption': 'AEO 與 GEO 的關注對象',
                'cols': ['項目', 'AEO', 'GEO'],
                'rows': [
                    ['最小單位', '頁面／段落', '品牌實體'],
                    ['典型問題', '「這個問題的答案是什麼」', '「這類產品有哪些選擇」'],
                    ['成功樣態', '你的段落被引用為答案來源', '你的品牌被列入候選名單'],
                    ['主要訊號', '內容結構、可擷取性、Schema', '實體一致性、跨來源提及、可驗證資訊'],
                    ['失敗樣態', '有被抓到但沒被引用', '模型知道你，但描述錯誤或不主動提及'],
                ],
            }),
            ('p', '完整比較見 %s。' % a('/aeo/aeo-vs-geo', 'AEO 與 GEO 的差異')),
        ]),
        sec('Signals', 'GEO 實際看什麼訊號', [
            ('h3', '一、實體是否唯一且一致'),
            ('p', '模型必須能把「你」和其他同名的東西分開。品牌名稱在各處寫法不一（有時加空格、有時用英文、有時用簡稱），'
                  '或公司名稱與品牌名稱關係不明，都會讓實體訊號散掉。做法見 %s。' % a('/aeo/entity-clarity', '實體清晰度')),
            ('h3', '二、資訊是否可驗證'),
            ('p', '統一編號、地址、電話、專利號這類可對外查證的資訊，會提高模型對該實體的信心。'
                  '相對地，只有形容詞沒有事實的自我描述幾乎沒有作用。見 %s。' % a('/aeo/trust-signals', '信任訊號')),
            ('h3', '三、跨來源的一致提及'),
            ('p', '只有自己的網站說自己是什麼，訊號很弱。當多個獨立來源以一致的方式描述同一個實體時，模型的判斷會穩定得多。'
                  '這一項無法靠技術設定達成，只能靠時間累積。'),
        ]),
        sec('Measure', '怎麼知道 GEO 有沒有進展', [
            ('p', 'GEO 的難處在於它沒有像排名那樣現成的名次可看。可用的做法是<strong>固定問題、固定平台、定期觀測</strong>：'),
            ('ul', [
                '準備一組代表真實採購情境的問題（例如「台灣有哪些 X 服務商」）。',
                '在固定的模型上定期詢問，記錄品牌是否被提及、是否附上網址、描述是否正確。',
                '比較的是自己的時間序列，不是跟別人比 —— 換模型、換問法都會讓數字不可比。',
            ]),
            ('note', '<strong>量測的陷阱：</strong>生成式模型本身有隨機性，同一個問題連問三次可能得到三種答案。'
                     '單次結果不足以判斷趨勢，必須固定條件並累積足夠的觀測點。中途更換模型或問題組，'
                     '歷史數據就失去可比性——這一點在解讀任何 GEO 報告時都要先確認。'),
        ]),
        sec('Limits', '限制', [
            ('ul', [
                '<strong>無法保證被提及。</strong>模型是否列出某個品牌，取決於其訓練資料、檢索來源與當下情境，非任何服務可控制。',
                '<strong>見效慢。</strong>實體訊號的累積以月為單位，比技術整備慢得多。',
                '<strong>錯誤資訊難以立即修正。</strong>若模型對品牌的既有描述有誤，能做的是讓正確資訊在各處一致且可驗證，'
                '但更新到模型回答中需要時間，沒有「送出更正」的管道。',
            ]),
        ]),
    ],
    faq=[
        ('GEO 和 AEO 要分開做嗎？',
         '不必分開。兩者的技術基礎大量重疊——結構化資料、內容清晰度、爬蟲可達性都同時服務兩邊。差異主要在內容策略：AEO 需要可擷取的答案段落，GEO 需要一致可驗證的實體資訊。實務上會一起規劃。'),
        ('GEO 可以量化嗎？',
         '可以量測趨勢，但沒有絕對分數。做法是固定一組問題、固定模型，定期記錄品牌是否被提及與描述是否正確，比較自己的時間序列。任何宣稱能給出「GEO 分數」並跨品牌比較的說法，都需要先確認其量測條件是否固定。'),
        ('模型講錯我的產品怎麼辦？',
         '沒有直接更正的管道。可行的做法是確保正確資訊在自家網站、結構化資料與各外部來源上一致且可驗證，並提高該資訊的可擷取性。模型後續更新時有機會採用正確版本，但不保證時程。'),
    ],
    related=[(HUB, 'AEO/GEO 知識中心'), ('/aeo/what-is-aeo', 'AEO 是什麼'),
             ('/aeo/entity-clarity', '實體清晰度'), ('/aeo/trust-signals', '信任訊號')],
))

PAGES.append(page(
    url='/aeo/aeo-vs-seo',
    title='AEO 與 SEO 有什麼不同？完整比較 - ShellFans',
    h1='AEO 與 SEO 有什麼不同？',
    eyebrow='Comparison',
    desc='AEO 追求成為 AI 答案的來源，SEO 追求搜尋結果排名。兩者技術基礎重疊但目標、指標與內容寫法不同。本頁逐項比較並說明哪些工作可以共用。',
    lede='最短的答案：SEO 讓人找到你的連結，AEO 讓 AI 引用你的內容。兩者的技術基礎有七成重疊——可爬取性、結構化資料、標題階層做一次兩邊都受益。真正的差異在內容的寫法，以及成功的判定方式完全不同。',
    schema='TechArticle',
    sections=[
        sec('Side by side', '逐項比較', [
            ('table', {
                'caption': 'AEO 與 SEO 的差異',
                'cols': ['面向', 'SEO', 'AEO'],
                'rows': [
                    ['目標', '在搜尋結果頁取得較前的排名', '成為 AI 生成答案的引用來源'],
                    ['使用者行為', '瀏覽多個結果後點擊', '直接讀取生成的答案，未必點擊'],
                    ['主要指標', '排名、曝光、點擊率、自然流量', '是否被提及、是否被引用、描述是否正確'],
                    ['內容偏好', '完整、深入、涵蓋關鍵字變體', '定義先行、段落自足、可直接擷取'],
                    ['連結價值', '外部連結是重要排名因素', '外部提及影響實體可信度，但機制不同'],
                    ['回饋速度', '數週至數月，有現成排名可查', '較慢，且需自行建立觀測機制'],
                    ['失敗樣態', '排在第二頁', '被抓取了但從未被引用'],
                ],
            }),
        ]),
        sec('Overlap', '哪些工作兩邊共用', [
            ('p', '這是最實際的部分——先做重疊的，投資報酬最高。'),
            ('ul', [
                '<strong>可爬取性</strong>：正確的 HTTP 狀態、乾淨的重新導向、canonical、sitemap。兩邊都是前提。',
                '<strong>結構化資料</strong>：Organization、BreadcrumbList、FAQPage。SEO 用於複合式摘要，AEO 用於實體理解。',
                '<strong>標題階層</strong>：一個 H1、清楚的 H2／H3。SEO 用於主題判定，AEO 用於段落切分。',
                '<strong>行動裝置與 HTTPS</strong>：基本衛生條件，兩邊都會檢查。',
            ]),
            ('p', '以 %s 為例，八個面向中的 crawlability（15 分）、technical（15 分）、'
                  'structuredData（15 分）、contentClarity（10 分）都是與 SEO 共用的基礎，合計 55 分。'
                  % a(METHOD, 'AI Readiness Score')),
        ]),
        sec('Divergence', '哪些工作只有 AEO 需要', [
            ('h3', '一、段落要能單獨成立'),
            ('p', 'SEO 可以接受「讀完整頁才懂」的文章。AEO 不行——AI 擷取的是段落，不是整頁。'
                  '每個段落要在脫離上下文的情況下仍然正確且完整。'),
            ('h3', '二、定義要放在最前面'),
            ('p', '傳統寫法常見「先鋪陳背景、最後給結論」。對答案引擎來說，前 100–150 字沒有給出直接回答，'
                  '這頁就很難被擷取。詳見 %s。' % a('/aeo/answer-readiness', '答覆整備度')),
            ('h3', '三、要主動寫限制與不適用情境'),
            ('p', '這與 SEO 的直覺相反。但「什麼情況下不該用」正是使用者會問 AI 的問題，'
                  '也是最容易被引用的段落類型之一。'),
            ('h3', '四、AI 爬蟲政策要獨立設定'),
            ('p', 'robots.txt 中針對 GPTBot、ClaudeBot、PerplexityBot 的規則與 Googlebot 是分開的，'
                  '且不會從 <code>User-agent: *</code> 繼承。詳見 %s。' % a('/aeo/ai-crawler', 'AI 爬蟲總覽')),
        ]),
        sec('Decision', '該怎麼分配資源', [
            ('p', '不需要二選一，但順序有差。建議：'),
            ('ol', [
                '<strong>先補齊共用基礎</strong>。這 55 分的部分同時提升兩邊，沒有取捨問題。',
                '<strong>再處理 AI 爬蟲政策</strong>。成本極低（改一個檔案），但誤擋的代價是全部歸零。',
                '<strong>接著調整既有主力頁面的內容結構</strong>。不必重寫全站，先處理最重要的幾頁。',
                '<strong>最後才是新增知識型內容</strong>。這部分成本最高，應該在前三項完成後再投入。',
            ]),
            ('p', '不確定自己在哪一步，可以先跑 %s 看八個面向的分佈。' % a(CHECKER, '免費檢測')),
        ]),
    ],
    faq=[
        ('做了 SEO 就等於做了 AEO 嗎？',
         '不等於，但已經完成了相當部分。可爬取性、結構化資料、標題階層這些 SEO 基礎同時是 AEO 的基礎。缺的通常是三塊：AI 爬蟲的 robots.txt 規則、內容的段落自足性，以及品牌實體的一致性。'),
        ('AEO 會取代 SEO 嗎？',
         '不會。只要搜尋結果頁還存在、使用者還會點擊連結，SEO 就仍然有價值。實際情況是兩者並存，且共用大部分技術基礎。把資源全部從 SEO 移到 AEO 是過度反應。'),
        ('該先做哪一個？',
         '先做兩者重疊的技術基礎，那部分沒有取捨問題。之後依你的客戶實際怎麼找到你來決定——如果你的目標客群已經習慣用 AI 查詢產品類別，AEO 的優先度就會提高。'),
        ('AEO 的成效怎麼證明？',
         '需要自行建立觀測機制：固定一組問題與模型，定期記錄品牌是否被提及與引用。這比 SEO 的排名查詢麻煩，但沒有捷徑——目前沒有像搜尋排名那樣的公開查詢介面。'),
    ],
    related=[(HUB, 'AEO/GEO 知識中心'), ('/aeo/what-is-aeo', 'AEO 是什麼'),
             ('/aeo/answer-readiness', '答覆整備度'), (METHOD, 'AI Readiness Score 方法論')],
))

PAGES.append(page(
    url='/aeo/aeo-vs-geo',
    title='AEO 與 GEO 有什麼不同？名詞釐清 - ShellFans',
    h1='AEO 與 GEO 有什麼不同？',
    eyebrow='Comparison',
    desc='AEO 關注頁面內容能否被擷取成答案，GEO 關注品牌實體在生成式模型中的辨識度。本頁釐清兩個名詞的差異、重疊處，以及為什麼實務上多半一起處理。',
    lede='AEO 的最小單位是「段落」，GEO 的最小單位是「品牌」。AEO 問的是「這個問題的答案有沒有引用我的內容」，GEO 問的是「使用者問這類產品時，我的品牌會不會被列出來」。兩者技術基礎大量重疊，但內容策略與量測方式不同。',
    schema='TechArticle',
    sections=[
        sec('Why confusing', '為什麼這兩個詞經常被混用', [
            ('p', '三個原因。第一，兩者都是近年才出現的說法，業界尚未形成統一定義。'
                  '第二，實務上的工作項目重疊超過一半，分開講反而累。'
                  '第三，同一批服務商往往兩者都提供，行銷上就合併成「AEO/GEO」一個詞。'),
            ('p', '本站的用法：需要精確區分時分開講，泛指整個題目時寫作 AEO/GEO。'),
        ]),
        sec('Compare', '差異對照', [
            ('table', {
                'caption': 'AEO 與 GEO 的差異',
                'cols': ['面向', 'AEO', 'GEO'],
                'rows': [
                    ['關注單位', '頁面、段落', '品牌實體'],
                    ['核心問題', '內容能否被擷取為答案', '品牌能否被辨識並列入候選'],
                    ['主要施力點', '內容結構、Schema、可擷取性', '實體一致性、可驗證資訊、跨來源提及'],
                    ['量測方式', '特定問題的回答是否引用本站', '品牌在類別問題中的出現率與描述正確性'],
                    ['見效時間', '較快（技術整備完成後數週）', '較慢（實體訊號以月累積）'],
                    ['可控程度', '較高，多為自家網站可調整項', '較低，受外部來源影響大'],
                ],
            }),
        ]),
        sec('Together', '重疊的部分', [
            ('p', '以下項目同時服務兩者，是投資報酬最高的起點：'),
            ('ul', [
                '%s — 爬不到就兩邊都沒有。' % a('/aeo/ai-crawler', 'AI 爬蟲可達性'),
                '%s — Organization 供 GEO 辨識實體，FAQPage 供 AEO 擷取答案。' % a('/aeo/schema', '結構化資料'),
                '%s — 同時是實體訊號與答案來源的可信度依據。' % a('/aeo/trust-signals', '信任訊號'),
                '清楚的標題階層 — 讓兩者都能正確切分內容。',
            ]),
        ]),
        sec('Practice', '實務上怎麼安排', [
            ('ol', [
                '<strong>共用基礎先做完</strong>，這部分沒有取捨。',
                '<strong>AEO 先於 GEO</strong>。AEO 的可控程度高、回饋快，先做能較早驗證方向是否正確。',
                '<strong>GEO 需要持續投入</strong>。實體訊號無法一次做完，要靠內容與外部提及長期累積。',
            ]),
            ('note', '<strong>常見錯誤：</strong>把 GEO 當成可以短期衝的專案。實體辨識度來自長期一致性，'
                     '三個月的密集投入若之後停止，訊號會逐漸稀釋。若預算只夠短期，把資源集中在 AEO 的技術面會實際得多。'),
        ]),
    ],
    faq=[
        ('只做其中一個可以嗎？',
         '可以，但要清楚取捨。只做 AEO：內容較容易被引用，但使用者問「這類服務有哪些」時仍可能不被列出。只做 GEO 而忽略內容結構：品牌可能被提及，但描述容易不精確，因為模型找不到清楚的段落可引用。'),
        ('哪一個比較重要？',
         '取決於你的客戶怎麼找你。若多數查詢是具體問題（「X 怎麼設定」），AEO 較重要；若多數是類別探索（「有哪些 X 服務商」），GEO 較重要。多數 B2B 服務兩種都有。'),
        ('GEO 有標準做法嗎？',
         '目前沒有公認標準。各家 AI 平台未公開其實體判定機制，業界的做法多由公開文件與實測歸納而來。因此對任何宣稱有「GEO 標準流程」的說法，都應該要求對方說明其依據與量測方式。'),
    ],
    related=[(HUB, 'AEO/GEO 知識中心'), ('/aeo/what-is-geo', 'GEO 是什麼'),
             ('/aeo/what-is-aeo', 'AEO 是什麼'), ('/aeo/entity-clarity', '實體清晰度')],
))


# ---------------------------------------------------------------------------
# B. 技術權威
# ---------------------------------------------------------------------------
PAGES.append(page(
    url='/aeo/ai-crawler',
    title='AI 爬蟲有哪些？robots.txt 設定完整指南 - ShellFans',
    h1='AI 爬蟲有哪些？robots.txt 該怎麼設定',
    eyebrow='Technical',
    desc='OpenAI、Anthropic、Perplexity、Google 各自使用不同的 AI 爬蟲，用途也不同。本頁整理主要爬蟲的 user-agent、用途差異，以及 robots.txt 設定時最常見的致命錯誤。',
    lede='AI 爬蟲不是只有一種。同一家公司通常有多支爬蟲，分別負責「訓練資料收集」與「即時搜尋索引」，兩者用途不同，擋錯的後果也不同。更關鍵的是：robots.txt 中特定 user-agent 的規則<strong>不會</strong>繼承 <code>User-agent: *</code>，這是最常見也最致命的設定錯誤。',
    schema='TechArticle',
    sections=[
        sec('Inventory', '主要 AI 爬蟲一覽', [
            ('table', {
                'caption': '主要 AI 爬蟲與用途',
                'cols': ['User-agent', '所屬', '用途'],
                'rows': [
                    ['GPTBot', 'OpenAI', '訓練資料收集'],
                    ['OAI-SearchBot', 'OpenAI', 'ChatGPT 搜尋索引 —— 擋掉會直接影響 ChatGPT 搜尋結果'],
                    ['ChatGPT-User', 'OpenAI', '使用者當下要求時的即時抓取'],
                    ['ClaudeBot', 'Anthropic', '訓練資料收集'],
                    ['Claude-SearchBot', 'Anthropic', '搜尋索引'],
                    ['Claude-User', 'Anthropic', '使用者當下要求時的即時抓取'],
                    ['PerplexityBot', 'Perplexity', '搜尋索引'],
                    ['Perplexity-User', 'Perplexity', '使用者當下要求時的即時抓取'],
                    ['Googlebot', 'Google', '搜尋索引 —— <strong>AI Overviews 也使用這支</strong>'],
                    ['Google-Extended', 'Google', 'Gemini 訓練用途的控制項，<strong>不影響 AI Overviews</strong>'],
                    ['Applebot-Extended', 'Apple', 'Apple Intelligence 訓練控制項'],
                    ['CCBot', 'Common Crawl', '公開語料庫，被多個模型間接使用'],
                    ['Bytespider', 'ByteDance', '訓練資料收集'],
                ],
            }),
            ('note', '<strong>特別注意 Google 這兩支的區別。</strong>擋掉 <code>Google-Extended</code> 只會退出 Gemini 的訓練用途，'
                     '<strong>不會</strong>讓你從 AI Overviews 消失——AI Overviews 走的是 Googlebot。'
                     '反過來說，擋掉 Googlebot 會同時失去一般搜尋與 AI Overviews，代價極大。'),
        ]),
        sec('Pitfall', '最常見的致命錯誤', [
            ('h3', 'robots.txt 的群組不會繼承'),
            ('p', '這是規格中明確定義但最常被誤解的一點：當 robots.txt 中存在針對特定 user-agent 的群組時，'
                  '<strong>該群組完全不繼承 <code>User-agent: *</code> 的規則</strong>。'),
            ('p', '也就是說，下面這段設定的實際效果，可能與作者的預期完全相反：'),
            ('ul', [
                '<code>User-agent: *</code> 下寫 <code>Allow: /</code>',
                '另外為 <code>GPTBot</code> 開一個群組，只寫了 <code>Disallow: /private</code>',
                '結果：GPTBot 的群組沒有 <code>Allow: /</code>，但因為只有 Disallow 特定路徑，其餘仍可抓 —— 這個例子還好。',
                '<strong>但如果</strong> GPTBot 群組寫成 <code>Disallow: /</code>，就是全站封鎖，而 <code>*</code> 的 Allow 完全不會救它。',
            ]),
            ('p', '因此建議<strong>對每一支要開放的爬蟲明確寫出規則</strong>，不要依賴繼承。'
                  'shell.fans 自己的 <a href="https://shell.fans/robots.txt">robots.txt</a> 就是這樣寫的，可以直接參考。'),
            ('h3', '其他常見問題'),
            ('ul', [
                '<strong>用 WAF 或 CDN 規則擋掉 AI 爬蟲卻忘了。</strong>robots.txt 寫了 Allow，但 Cloudflare 的 Bot Fight Mode 直接回 403 —— 爬蟲根本讀不到 robots.txt。這種情況檢測工具只會看到連線失敗。',
                '<strong>只擋訓練爬蟲，卻連搜尋爬蟲一起擋。</strong>想退出訓練是合理的商業決定，但 GPTBot 與 OAI-SearchBot 要分開處理，否則會連 ChatGPT 搜尋的曝光一起失去。',
                '<strong>robots.txt 回 404 或 500。</strong>沒有 robots.txt 通常視為全部允許，但伺服器錯誤的行為則不一定，應該確保它穩定回 200。',
            ]),
        ]),
        sec('Verify', '怎麼驗證設定真的生效', [
            ('ol', [
                '直接以該 user-agent 送出請求，確認回應是 200 而非 403。',
                '檢查 CDN／WAF 層是否有獨立的 bot 規則覆蓋了 robots.txt 的意圖。',
                '查看伺服器 access log，確認這些爬蟲實際有來訪、取得什麼狀態碼。',
                '用 %s 做一次整體檢查，其中 AI Crawler Policy 面向（10 分）會列出被誤擋的爬蟲。' % a(CHECKER, 'AEO/GEO 檢測工具'),
            ]),
            ('note', '<strong>log 比設定檔誠實。</strong>robots.txt 寫什麼是意圖，access log 記錄的才是實際發生的事。'
                     '兩者不一致時，永遠以 log 為準去找中間哪一層攔截了。'),
        ]),
    ],
    faq=[
        ('擋掉 AI 爬蟲會影響一般搜尋排名嗎？',
         '要看擋哪一支。擋 GPTBot、ClaudeBot、PerplexityBot 不影響 Google 搜尋排名。但擋 Googlebot 會同時失去一般搜尋與 AI Overviews。Google-Extended 是獨立的訓練控制項，擋掉不影響搜尋或 AI Overviews。'),
        ('我不想被拿去訓練，但想被 AI 搜尋引用，可以嗎？',
         '可以。多數業者把訓練與搜尋分成不同的 user-agent，例如 OpenAI 的 GPTBot（訓練）與 OAI-SearchBot（搜尋）、Anthropic 的 ClaudeBot（訓練）與 Claude-SearchBot（搜尋）。分別設定即可。'),
        ('robots.txt 擋了，AI 就一定抓不到嗎？',
         '不保證。robots.txt 是一項自願遵循的協定，主要業者公開表示遵守，但不排除有不遵守的爬蟲。若有嚴格需求，需要在伺服器或 WAF 層做實際的存取控制，而非只靠 robots.txt。'),
        ('要不要開放 CCBot？',
         '取決於你對「內容被納入公開語料庫」的態度。CCBot 蒐集的 Common Crawl 語料被多個模型間接使用，開放有助於被更多系統認識，但也意味著內容進入一份公開資料集。這是商業判斷，沒有技術上的標準答案。'),
    ],
    related=[(HUB, 'AEO/GEO 知識中心'), ('/aeo/gptbot-oai-searchbot', 'GPTBot 與 OAI-SearchBot'),
             ('/aeo/claudebot', 'ClaudeBot'), ('/aeo/perplexitybot', 'PerplexityBot')],
))

PAGES.append(page(
    url='/aeo/gptbot-oai-searchbot',
    title='GPTBot 與 OAI-SearchBot 差在哪？OpenAI 爬蟲設定 - ShellFans',
    h1='GPTBot 與 OAI-SearchBot 差在哪？',
    eyebrow='Technical',
    desc='OpenAI 有三支爬蟲：GPTBot 負責訓練資料、OAI-SearchBot 負責 ChatGPT 搜尋索引、ChatGPT-User 負責使用者即時抓取。用途不同，擋錯的後果也完全不同。',
    lede='OpenAI 目前有三支主要爬蟲，用途各不相同：<strong>GPTBot</strong> 收集訓練資料、<strong>OAI-SearchBot</strong> 建立 ChatGPT 搜尋索引、<strong>ChatGPT-User</strong> 在使用者當下要求時即時抓取頁面。想被 ChatGPT 搜尋引用卻擋掉 OAI-SearchBot，是最常見也最可惜的設定錯誤。',
    schema='TechArticle',
    sections=[
        sec('Compare', '三支爬蟲的分工', [
            ('table', {
                'caption': 'OpenAI 爬蟲用途對照',
                'cols': ['User-agent', '用途', '擋掉的後果'],
                'rows': [
                    ['GPTBot', '收集訓練資料，用於改進模型', '內容不進入訓練語料。不影響 ChatGPT 搜尋能否引用你'],
                    ['OAI-SearchBot', '建立 ChatGPT 搜尋索引', '<strong>ChatGPT 搜尋時無法引用你的網站</strong>'],
                    ['ChatGPT-User', '使用者在對話中要求開啟某網址時的即時抓取', '使用者主動貼上你的網址也讀不到'],
                ],
            }),
        ]),
        sec('Config', '常見的三種設定意圖', [
            ('h3', '一、全部開放（多數網站適用）'),
            ('p', '希望最大化 AI 搜尋曝光，且不介意內容進入訓練語料。三支都明確 Allow。'),
            ('h3', '二、要曝光但不要被訓練'),
            ('p', '擋 GPTBot，開放 OAI-SearchBot 與 ChatGPT-User。這是內容型網站常見的選擇——'
                  '保留在 ChatGPT 搜尋中被引用的機會，同時退出訓練語料。'),
            ('h3', '三、全部封鎖'),
            ('p', '三支都 Disallow。適用於會員制、內部系統或有明確法規限制的站台。'
                  '要清楚代價：ChatGPT 使用者將無法從搜尋中找到你。'),
            ('note', '<strong>務必記得：</strong>robots.txt 中特定 user-agent 的群組<strong>不繼承</strong> '
                     '<code>User-agent: *</code> 的規則。每一支都要明確寫出自己的 Allow／Disallow，'
                     '不要假設它會沿用預設群組。詳見 %s。' % a('/aeo/ai-crawler', 'AI 爬蟲總覽')),
        ]),
        sec('Verify', '驗證方式', [
            ('ol', [
                '以 <code>OAI-SearchBot</code> 作為 user-agent 送出請求，確認回應為 200。',
                '確認 CDN／WAF 沒有在 robots.txt 之外另行攔截 —— 這是最常見的「設定寫了但沒生效」原因。',
                '檢視 access log 中這三支的實際到訪紀錄與狀態碼。',
                '用 %s 檢查，AI Crawler Policy 面向會直接指出誤擋。' % a(CHECKER, '免費檢測工具'),
            ]),
        ]),
    ],
    faq=[
        ('擋掉 GPTBot 會讓 ChatGPT 找不到我嗎？',
         '不會。GPTBot 負責的是訓練資料收集；ChatGPT 搜尋使用的是 OAI-SearchBot。只要 OAI-SearchBot 保持開放，ChatGPT 搜尋仍可引用你的網站。'),
        ('已經被訓練過的內容，現在擋還有用嗎？',
         '擋住的是後續的抓取，已納入既有模型的內容無法回溯移除。若目的是控制未來版本的訓練資料，現在設定仍然有意義。'),
        ('ChatGPT-User 需要開放嗎？',
         '建議開放。它代表使用者在對話中主動要求讀取你的網址——這是意圖最明確的一種造訪。擋掉等於拒絕一個主動想了解你的使用者。'),
    ],
    related=[('/aeo/ai-crawler', 'AI 爬蟲總覽'), ('/aeo/claudebot', 'ClaudeBot'),
             ('/aeo/perplexitybot', 'PerplexityBot'), (CHECKER, '免費檢測工具')],
))

PAGES.append(page(
    url='/aeo/claudebot',
    title='ClaudeBot 是什麼？Anthropic 爬蟲與 robots.txt - ShellFans',
    h1='ClaudeBot 是什麼？',
    eyebrow='Technical',
    desc='ClaudeBot 是 Anthropic 用於收集訓練資料的爬蟲。Anthropic 另有 Claude-SearchBot 負責搜尋索引、Claude-User 負責即時抓取。本頁說明差異與 robots.txt 設定方式。',
    lede='ClaudeBot 是 Anthropic 用來收集公開網頁作為訓練資料的爬蟲。它與負責搜尋索引的 <strong>Claude-SearchBot</strong>、負責使用者即時要求的 <strong>Claude-User</strong> 是不同的 user-agent，用途各異。若目的是被 Claude 引用而非被訓練，需要分開設定。',
    schema='TechArticle',
    sections=[
        sec('Family', 'Anthropic 的爬蟲家族', [
            ('table', {
                'caption': 'Anthropic 爬蟲用途對照',
                'cols': ['User-agent', '用途', '備註'],
                'rows': [
                    ['ClaudeBot', '收集訓練資料', '最常見於 access log'],
                    ['Claude-SearchBot', '搜尋索引', '影響 Claude 能否在回答中引用你的網站'],
                    ['Claude-User', '使用者當下要求時的即時抓取', '意圖最明確的一種造訪'],
                    ['anthropic-ai', '早期使用的識別字串', '部分站台仍會在 robots.txt 中一併列出'],
                ],
            }),
            ('p', '若不確定站上實際來過哪幾支，最直接的方式是查 access log 而非猜測。'),
        ]),
        sec('Config', 'robots.txt 設定', [
            ('p', '與 OpenAI 的情況相同，三種常見意圖：'),
            ('ul', [
                '<strong>全部開放</strong> — 最大化被 Claude 理解與引用的機會。',
                '<strong>要引用不要訓練</strong> — 擋 ClaudeBot，開放 Claude-SearchBot 與 Claude-User。',
                '<strong>全部封鎖</strong> — 需清楚理解代價：Claude 使用者將無法從搜尋中找到你。',
            ]),
            ('note', '再次提醒：特定 user-agent 群組<strong>不繼承</strong> <code>User-agent: *</code>。'
                     '每一支都要明確寫出規則。詳見 %s。' % a('/aeo/ai-crawler', 'AI 爬蟲總覽')),
        ]),
        sec('Check', '確認設定生效', [
            ('ol', [
                '以 <code>ClaudeBot</code> 與 <code>Claude-SearchBot</code> 分別測試，確認回應狀態。',
                '檢查 CDN／WAF 層是否另有 bot 攔截規則覆蓋了 robots.txt。',
                '比對 access log 與 robots.txt —— 兩者不一致時以 log 為準。',
                '執行 %s，AI Crawler Policy 面向會列出實際被擋的爬蟲。' % a(CHECKER, 'AEO/GEO 檢測'),
            ]),
        ]),
    ],
    faq=[
        ('ClaudeBot 和 Claude-SearchBot 一定要分開設定嗎？',
         '如果你的意圖是「可以被引用但不想被訓練」，就必須分開。若兩者都要開放或都要封鎖，則規則相同，但仍建議各自明確寫出，避免依賴繼承而出錯。'),
        ('我沒有在 log 裡看到 ClaudeBot，是被擋了嗎？',
         '不一定。爬蟲的造訪頻率取決於網站規模、更新頻率與既有的抓取排程，新站或小站可能本來就少被造訪。先確認 robots.txt 與 WAF 沒有攔截，再觀察一段時間。'),
        ('開放 ClaudeBot 對我有什麼好處？',
         '直接好處是內容有機會進入後續模型版本的訓練語料，讓模型對你的品牌與產品有基礎認識。但這與「被即時引用」是兩件事——後者取決於 Claude-SearchBot。'),
    ],
    related=[('/aeo/ai-crawler', 'AI 爬蟲總覽'), ('/aeo/gptbot-oai-searchbot', 'GPTBot 與 OAI-SearchBot'),
             ('/aeo/perplexitybot', 'PerplexityBot'), (HUB, 'AEO/GEO 知識中心')],
))

PAGES.append(page(
    url='/aeo/perplexitybot',
    title='PerplexityBot 是什麼？Perplexity 爬蟲設定 - ShellFans',
    h1='PerplexityBot 是什麼？',
    eyebrow='Technical',
    desc='PerplexityBot 是 Perplexity 用於建立搜尋索引的爬蟲，Perplexity-User 則負責使用者當下要求的即時抓取。Perplexity 的回答會標註來源連結，被索引與否直接影響曝光。',
    lede='PerplexityBot 是 Perplexity 用於建立搜尋索引的爬蟲。由於 Perplexity 的回答會明確標註來源連結並可點擊，被不被索引對實際流量的影響比其他答案引擎更直接——擋掉它，等於放棄這個管道的全部曝光。',
    schema='TechArticle',
    sections=[
        sec('Why matters', '為什麼 Perplexity 值得單獨關注', [
            ('p', 'Perplexity 的產品形態與其他答案引擎有一個明顯差異：它在回答旁邊列出編號來源，使用者可以直接點擊前往。'
                  '這代表被引用不只是品牌曝光，還可能帶來實際的造訪。'),
            ('p', '相對地，若 PerplexityBot 被擋，損失是完整的——不會有「雖然沒被索引但還是被提到」的中間狀態。'),
        ]),
        sec('Agents', '兩支爬蟲', [
            ('table', {
                'caption': 'Perplexity 爬蟲對照',
                'cols': ['User-agent', '用途', '擋掉的後果'],
                'rows': [
                    ['PerplexityBot', '建立搜尋索引', '無法出現在 Perplexity 的來源清單中'],
                    ['Perplexity-User', '使用者當下要求時的即時抓取', '使用者主動指定你的網址也讀不到'],
                ],
            }),
        ]),
        sec('Optimize', '除了開放之外還能做什麼', [
            ('p', '被抓到只是最低門檻。要提高被列為來源的機會，內容形狀比爬蟲設定更關鍵：'),
            ('ul', [
                '<strong>段落要能單獨成立</strong>——Perplexity 引用的是段落而非整頁。詳見 %s。' % a('/aeo/answer-readiness', '答覆整備度'),
                '<strong>事實要具體可查證</strong>——含有明確數字、日期、規格的段落比形容詞堆疊更容易被選為來源。',
                '<strong>標題要直接對應問題</strong>——「AEO 費用怎麼算」比「關於我們的服務」更容易對上使用者的查詢。',
                '<strong>實體要清楚</strong>——來源標註需要能辨識出「這是誰說的」。見 %s。' % a('/aeo/entity-clarity', '實體清晰度'),
            ]),
        ]),
    ],
    faq=[
        ('被 Perplexity 引用會帶來流量嗎？',
         '有機會，因為 Perplexity 的來源標註是可點擊的連結。但實際點擊率取決於回答是否已充分滿足使用者、你的來源排在第幾個等因素，無法保證。'),
        ('要怎麼知道自己有沒有被 Perplexity 引用？',
         '目前沒有官方的查詢介面。可行做法是固定一組代表真實查詢情境的問題，定期在 Perplexity 上詢問並記錄來源清單中是否出現你的網域。單次結果不足以判斷，需累積觀測。'),
        ('Perplexity 和 Google AI Overviews 的爬蟲一樣嗎？',
         '不一樣。Perplexity 使用 PerplexityBot，Google AI Overviews 使用 Googlebot。兩者是獨立的系統，robots.txt 需分別設定。'),
    ],
    related=[('/aeo/ai-crawler', 'AI 爬蟲總覽'), ('/aeo/answer-readiness', '答覆整備度'),
             ('/aeo/gptbot-oai-searchbot', 'GPTBot 與 OAI-SearchBot'), (CHECKER, '免費檢測工具')],
))

PAGES.append(page(
    url='/aeo/llms-txt',
    title='llms.txt 是什麼？該不該做？ - ShellFans',
    h1='llms.txt 是什麼？該不該做？',
    eyebrow='Technical',
    desc='llms.txt 是一份放在網站根目錄的 Markdown 檔案，用來向大型語言模型提供網站的結構化摘要。本頁說明它的用途、目前的採用現況，以及誠實評估值不值得投入。',
    lede='llms.txt 是一份放在網站根目錄的 Markdown 檔案（<code>/llms.txt</code>），用簡潔的結構告訴大型語言模型「這個網站是什麼、重要頁面在哪裡」。它由 llmstxt.org 提出，<strong>目前是社群提案而非正式標準</strong>，也沒有任何主要 AI 業者公開承諾一定會讀取它。',
    schema='TechArticle',
    sections=[
        sec('Honest', '先講最重要的一件事', [
            ('note', '<strong>llms.txt 目前不是標準。</strong>它是 llmstxt.org 提出的社群提案，'
                     '尚未有任何主要 AI 業者公開承諾會讀取或依此調整行為。'
                     '任何宣稱「做了 llms.txt 就會被 ChatGPT 引用」的說法都不成立。'),
            ('p', '把這點先說清楚，是因為這個主題目前充斥著誇大宣稱。以下的建議都建立在「它可能有用、成本很低」這個前提上，'
                  '而不是「它一定有用」。'),
        ]),
        sec('What', '它實際長什麼樣子', [
            ('p', 'llms.txt 是一份 Markdown 檔案，慣例的結構是：'),
            ('ul', [
                '<code>#</code> 一級標題：網站或品牌名稱',
                '<code>&gt;</code> 引言區塊：一段話說清楚這個網站是什麼',
                '<code>##</code> 二級標題分區：核心服務、重要頁面、常見問題等',
                '每個項目以 <code>[標題](網址)</code> 加一句說明，讓模型知道該頁回答什麼問題',
            ]),
            ('p', '可以直接看 shell.fans 自己的 <a href="https://shell.fans/llms.txt">/llms.txt</a> 作為範例，'
                  '以及延伸版本 <a href="https://shell.fans/llms-full.txt">/llms-full.txt</a>（見 %s）。'
                  % a('/aeo/llms-full-txt', 'llms-full.txt 說明')),
        ]),
        sec('Value', '為什麼還是建議做', [
            ('p', '即使不確定 AI 業者是否讀取，仍有三個實際理由：'),
            ('ol', [
                '<strong>成本極低。</strong>一份檔案、幾十行，一次寫完長期受用。與其他 AEO 工作相比，投入幾乎可以忽略。',
                '<strong>撰寫過程本身有價值。</strong>要寫出這份摘要，你必須先想清楚「我們到底是什麼、哪些頁面最重要、'
                '每頁回答什麼問題」。這個釐清過程通常會直接暴露網站結構上的問題。',
                '<strong>下檔風險為零。</strong>它不影響 SEO、不影響使用者、不佔資源。即使最終沒有任何模型讀取，也沒有損失。',
            ]),
            ('p', '在 %s 中，llms.txt 面向配分 5 分——這個相對低的權重正反映了它「有用但非決定性」的定位。'
                  % a(METHOD, 'AI Readiness Score')),
        ]),
        sec('Write', '怎麼寫才有意義', [
            ('h3', '該寫的'),
            ('ul', [
                '<strong>實體關係要明確</strong>：品牌、法人、產品線之間是什麼關係。這是模型最容易搞混的部分。',
                '<strong>每個連結要說明它回答什麼問題</strong>，而不只是列出標題。',
                '<strong>寫出「不是什麼」</strong>。明確排除常見誤解（例如「這不是 XX 平台」）比只講自己是什麼更有幫助。',
                '<strong>標註更新日期</strong>，讓讀取者知道資訊的時效。',
            ]),
            ('h3', '不該寫的'),
            ('ul', [
                '<strong>關鍵字堆疊</strong>。這份檔案是給模型讀的摘要，不是關鍵字清單。',
                '<strong>把整站內容複製進來</strong>。那是 llms-full.txt 的用途，兩者要分工。',
                '<strong>誇大或無法驗證的宣稱</strong>。若與網站實際內容不符，反而製造矛盾訊號。',
            ]),
        ]),
    ],
    faq=[
        ('llms.txt 是官方標準嗎？',
         '不是。它是 llmstxt.org 提出的社群提案，尚未成為正式標準，也沒有主要 AI 業者公開承諾遵循。應該把它視為「低成本、可能有幫助」的選項，而非必要條件。'),
        ('做了 llms.txt，ChatGPT 就會讀嗎？',
         '沒有任何業者公開保證會讀取。建議做的理由是成本極低、撰寫過程能釐清網站結構，以及沒有下檔風險，而不是因為有明確效果保證。'),
        ('llms.txt 和 robots.txt 有什麼不同？',
         'robots.txt 規範「能不能抓」，是有明確規格且被主要業者遵循的協定；llms.txt 提供「這個網站是什麼」的摘要，是尚未標準化的提案。兩者用途不同，不能互相取代。'),
        ('放在哪裡？',
         '網站根目錄，也就是 https://你的網域/llms.txt。與 robots.txt 相同層級。'),
    ],
    related=[('/aeo/llms-full-txt', 'llms-full.txt'), ('/aeo/ai-crawler', 'AI 爬蟲總覽'),
             (METHOD, 'AI Readiness Score 方法論'), (CHECKER, '免費檢測工具')],
))

PAGES.append(page(
    url='/aeo/llms-full-txt',
    title='llms-full.txt 是什麼？與 llms.txt 的分工 - ShellFans',
    h1='llms-full.txt 是什麼？',
    eyebrow='Technical',
    desc='llms-full.txt 是 llms.txt 的延伸版本，提供更完整的網站內容供大型語言模型讀取。本頁說明兩者的分工、什麼情況下需要它，以及維護成本的取捨。',
    lede='llms-full.txt 是 llms.txt 的延伸版本，放在同一個位置（<code>/llms-full.txt</code>），提供更完整的內容而非僅是索引。簡單的分法：<strong>llms.txt 是目錄，llms-full.txt 是內容</strong>。多數網站先做好前者即可，後者屬於選配。',
    schema='TechArticle',
    sections=[
        sec('Split', '兩者的分工', [
            ('table', {
                'caption': 'llms.txt 與 llms-full.txt 的差異',
                'cols': ['項目', 'llms.txt', 'llms-full.txt'],
                'rows': [
                    ['角色', '索引與導覽', '完整內容'],
                    ['長度', '數十行', '數百行以上'],
                    ['內容', '品牌定位 + 重要頁面連結與說明', '關鍵頁面的實際內容、細節、規格、常見問答'],
                    ['維護成本', '低，內容變動時才更新', '較高，需與網站內容同步'],
                    ['優先順序', '<strong>先做這個</strong>', '有餘力再做'],
                ],
            }),
        ]),
        sec('When', '什麼情況值得做', [
            ('p', '不是所有網站都需要。以下情況投入才划算：'),
            ('ul', [
                '<strong>內容分散在很多頁</strong>，模型要理解全貌得抓很多次。集中成一份可降低這個成本。',
                '<strong>有大量規格、參數、條件</strong>需要精確傳達，而這些散落在不同頁面。',
                '<strong>常見誤解多</strong>，需要在一個地方一次講清楚「我們不是什麼」。',
            ]),
            ('p', '反之，若網站只有十幾頁且結構清楚，llms.txt 加上良好的頁面結構就足夠了，'
                  '多做一份 llms-full.txt 只是增加維護負擔。'),
        ]),
        sec('Risk', '維護成本與風險', [
            ('note', '<strong>最大的風險是內容過期。</strong>llms-full.txt 與網站內容不同步時，'
                     '你等於同時對外提供兩個版本的事實。模型讀到舊版本，可能產生比沒有這份檔案更糟的結果——'
                     '因為錯誤資訊看起來很正式。'),
            ('p', '因此建議：'),
            ('ol', [
                '在檔案開頭標註最後更新日期，讓讀取者能判斷時效。',
                '把「更新 llms-full.txt」納入內容變更的流程，而不是想到才改。',
                '若無法保證同步，<strong>寧可不做</strong>。一份準確的 llms.txt 勝過一份過期的 llms-full.txt。',
            ]),
        ]),
    ],
    faq=[
        ('一定要兩個都做嗎？',
         '不用。llms.txt 是基礎，llms-full.txt 是選配。若無法確保 llms-full.txt 與網站內容同步更新，建議只做 llms.txt——過期的完整版比沒有更糟。'),
        ('llms-full.txt 要多長？',
         '沒有規定長度。原則是「讀完能正確理解這個網站」，而不是「越長越好」。把不重要的內容塞進去只會稀釋重點。'),
        ('可以自動產生嗎？',
         '技術上可以，但要小心。自動彙整容易把導覽列、頁尾、重複區塊一起帶入，產生大量雜訊。若要自動化，需要先定義好抽取規則並人工檢查結果。'),
    ],
    related=[('/aeo/llms-txt', 'llms.txt'), (HUB, 'AEO/GEO 知識中心'),
             (METHOD, 'AI Readiness Score 方法論'), (CHECKER, '免費檢測工具')],
))

PAGES.append(page(
    url='/aeo/schema',
    title='AEO 需要哪些 Schema？結構化資料實作指南 - ShellFans',
    h1='AEO 需要哪些 Schema？',
    eyebrow='Technical',
    desc='並非所有 Schema.org 類型對 AEO 都有幫助。本頁說明哪幾種結構化資料真的有用、如何正確實作，以及亂加 schema 會造成什麼問題。',
    lede='對 AEO 而言真正關鍵的結構化資料只有少數幾種：<strong>Organization</strong>（你是誰）、<strong>FAQPage</strong>（可直接擷取的問答）、<strong>BreadcrumbList</strong>（內容層級）、以及依業務型態選用的 <strong>Service</strong> 或 <strong>Product</strong>。加上與頁面內容不符的 schema 不會加分，反而製造矛盾訊號。',
    schema='TechArticle',
    sections=[
        sec('Priority', '優先順序', [
            ('table', {
                'caption': 'AEO 相關 Schema 類型的優先順序',
                'cols': ['類型', '優先度', '用途與注意事項'],
                'rows': [
                    ['Organization', '<strong>必要</strong>',
                     '定義品牌實體。應包含 name、url、logo，並盡量補上可驗證的 address、telephone、identifier。'
                     '這是 %s 的核心。' % a('/aeo/entity-clarity', '實體清晰度')],
                    ['WebSite', '建議', '宣告站台層級的資訊，與 Organization 建立關聯。'],
                    ['BreadcrumbList', '建議', '讓模型理解頁面在網站結構中的位置。深層頁面尤其重要。'],
                    ['FAQPage', '<strong>高價值</strong>',
                     '結構化的問答最容易被擷取為答案。但<strong>必須與頁面上實際可見的內容一致</strong>。詳見 %s。'
                     % a('/aeo/faq-schema', 'FAQ Schema')],
                    ['Service', '視業務', '服務型業務適用。可標註 serviceType、areaServed、provider。'],
                    ['Product', '視業務', '有明確商品時適用。不要為了加而加。'],
                    ['TechArticle / Article', '視內容', '知識型內容適用，可標註 author、publisher、datePublished。'],
                    ['WebApplication', '視產品', '線上工具適用。'],
                ],
            }),
        ]),
        sec('Practice', '實作原則', [
            ('h3', '一、用 JSON-LD，不要用 Microdata'),
            ('p', 'JSON-LD 與 HTML 內容分離，維護容易且不會影響版面。目前是主流建議做法。'),
            ('h3', '二、用 @graph 把節點串起來'),
            ('p', '同一頁的多個 schema 節點放在一個 <code>@graph</code> 陣列中，並用 <code>@id</code> 建立引用關係，'
                  '比散落成多個獨立 script 標籤更能表達「這些是同一件事的不同面向」。'),
            ('h3', '三、標註的必須是頁面上真的有的東西'),
            ('p', '這是最容易出錯的地方。FAQPage 標了五個問題，但頁面上只看得到三個——這是不一致，'
                  '不但沒有幫助，還可能被視為操弄。<strong>結構化資料是既有內容的機器可讀版本，不是額外的宣傳欄位。</strong>'),
            ('h3', '四、驗證能否被解析'),
            ('p', 'JSON 語法錯誤會讓整段 schema 完全失效，而且從頁面外觀上完全看不出來。'
                  '每次修改後都應該實際 parse 一次確認。'),
        ]),
        sec('Mistakes', '常見錯誤', [
            ('ul', [
                '<strong>把 Organization 重複宣告在每一頁但內容不一致</strong>。名稱、logo、地址應該完全相同，'
                '不一致會直接削弱實體訊號。',
                '<strong>為了「多一點 schema」而加上不適用的類型</strong>。例如純知識文章加 Product。',
                '<strong>FAQPage 的答案寫得像廣告</strong>。答案應該直接回答問題，不是行銷文案。',
                '<strong>JSON 語法錯誤未被發現</strong>。少一個逗號整段就失效，頁面外觀卻毫無異狀。',
                '<strong>用 schema 描述頁面上沒有的內容</strong>。這是最嚴重的一類，等同於對機器與對人說不同的話。',
            ]),
            ('p', '%s 的 Structured Data 面向（15 分）會檢查 JSON-LD 是否存在、Organization 是否具備，'
                  '以及頁面若含 FAQ 文案是否對應建立 FAQPage。' % a(METHOD, 'AI Readiness Score')),
        ]),
    ],
    faq=[
        ('加越多 schema 越好嗎？',
         '不是。與頁面內容不符的 schema 不會加分，還可能產生矛盾訊號。原則是：頁面上有的東西才標註，且標註內容要與可見內容一致。'),
        ('JSON-LD 和 Microdata 選哪個？',
         '建議 JSON-LD。它與 HTML 分離，維護容易、不影響版面，且是目前主流的建議做法。既有的 Microdata 不必急著移除，但新增時用 JSON-LD。'),
        ('Schema 加了就會被 AI 引用嗎？',
         '不會。結構化資料的作用是讓模型更容易正確理解頁面內容，屬於必要條件之一。是否被引用還取決於內容本身的品質、可擷取性與該領域的其他來源。'),
        ('怎麼確認 schema 沒寫錯？',
         '最基本的是確認 JSON 可以被正確解析——語法錯誤會讓整段失效但外觀完全正常。之後再確認標註的內容與頁面可見內容一致。'),
    ],
    related=[('/aeo/faq-schema', 'FAQ Schema'), ('/aeo/entity-clarity', '實體清晰度'),
             (METHOD, 'AI Readiness Score 方法論'), (CHECKER, '免費檢測工具')],
))

PAGES.append(page(
    url='/aeo/faq-schema',
    title='FAQ Schema 怎麼寫？FAQPage 實作與常見錯誤 - ShellFans',
    h1='FAQ Schema 怎麼寫？',
    eyebrow='Technical',
    desc='FAQPage 結構化資料是 AEO 中價值最高的 schema 類型之一，因為問答格式最接近答案引擎需要的形狀。本頁說明實作方式、內容原則與常見錯誤。',
    lede='FAQPage 是 AEO 中投報率最高的結構化資料類型，原因很簡單：答案引擎要找的就是「問題—答案」這個形狀，而 FAQ 天然就是這個形狀。但前提是 <strong>schema 標註的問答必須與頁面上實際可見的內容完全一致</strong>，否則不但無效，還可能被視為操弄。',
    schema='TechArticle',
    sections=[
        sec('Why', '為什麼 FAQ 特別有效', [
            ('p', '答案引擎在處理內容時，最理想的材料是「一個明確的問題 + 一段自足的回答」。'
                  '一般文章需要模型自己判斷哪一段在回答什麼；FAQ 則是直接把這個對應關係標示出來。'),
            ('p', '這也是為什麼 FAQ 段落經常成為被引用的部分——它省去了模型猜測的步驟。'),
        ]),
        sec('Write', '問題怎麼挑', [
            ('h3', '用使用者真的會問的說法'),
            ('p', '「本服務之計費機制為何」不是使用者會打的字。「AEO 一個月要多少錢」才是。'
                  '問題的措辭應該貼近實際查詢，而不是內部術語。'),
            ('h3', '一個問題只回答一件事'),
            ('p', '把三個問題塞進一個答案，會讓這段變得無法單獨引用。寧可拆成三組。'),
            ('h3', '答案要能脫離上下文成立'),
            ('p', '答案中不要出現「如上所述」「詳見上一節」。被擷取出來時，那些指涉全部失效。'),
            ('h3', '誠實回答，包括負面的'),
            ('p', '「這個服務適合誰」之外，也要有「不適合誰」。後者往往更容易被引用，'
                  '因為使用者實際上很常問「我這種情況適不適用」。'),
        ]),
        sec('Implement', '實作要點', [
            ('ul', [
                '使用 JSON-LD，型別為 <code>FAQPage</code>，內含 <code>mainEntity</code> 陣列。',
                '每個項目型別為 <code>Question</code>，其 <code>acceptedAnswer</code> 型別為 <code>Answer</code>。',
                '<strong>答案文字應與頁面上可見的文字一致</strong>。若頁面用 HTML 呈現，schema 中放去除標籤的純文字版本。',
                '頁面上的 FAQ 建議用 <code>&lt;details&gt;/&lt;summary&gt;</code> 或標題結構呈現，讓人與機器讀到相同內容。',
            ]),
            ('note', '<strong>最常見的錯誤：</strong>schema 裡有十個問答，頁面上只顯示三個。'
                     '這種不一致沒有好處——搜尋引擎與答案引擎都會比對可見內容，'
                     '且這種做法在搜尋引擎的政策上通常被歸類為不當標記。'),
        ]),
        sec('Mistakes', '其他常見錯誤', [
            ('ul', [
                '<strong>把行銷文案寫進答案</strong>。「我們擁有業界最強的團隊」不回答任何問題，也不會被引用。',
                '<strong>問題全部都是自己想推的</strong>。FAQ 的價值來自它回答真實疑問，不是產品介紹的變形。',
                '<strong>答案太短</strong>。一句話的答案通常缺乏可引用的資訊量，建議 2–4 句並包含具體條件。',
                '<strong>每一頁都放同一組 FAQ</strong>。重複內容會稀釋訊號，應該讓每頁的 FAQ 對應該頁主題。',
            ]),
        ]),
    ],
    faq=[
        ('FAQ schema 標的問答一定要顯示在頁面上嗎？',
         '是。schema 是可見內容的機器可讀版本，不是額外欄位。標註了但頁面上看不到的問答，屬於不一致標記，不會帶來好處。'),
        ('一頁可以放幾個問答？',
         '沒有硬性限制，但建議聚焦。五到十組切題的問答，勝過二十組泛泛而談。重點是每一組都要對應該頁的主題。'),
        ('FAQ 要放在頁面哪個位置？',
         '通常放在主要內容之後、頁尾之前。位置本身不是關鍵，重要的是內容可見、可被爬蟲讀取，且不需要點擊或互動才會出現。'),
        ('用 details/summary 摺疊起來會影響擷取嗎？',
         '不會。details/summary 的內容存在於 HTML 原始碼中，爬蟲可以讀取。真正有問題的是需要 JavaScript 執行後才載入的內容。'),
    ],
    related=[('/aeo/schema', 'AEO 需要哪些 Schema'), ('/aeo/answer-readiness', '答覆整備度'),
             (METHOD, 'AI Readiness Score 方法論'), (CHECKER, '免費檢測工具')],
))

PAGES.append(page(
    url='/aeo/entity-clarity',
    title='實體清晰度是什麼？讓 AI 確定你是誰 - ShellFans',
    h1='實體清晰度：讓 AI 確定「你是誰」',
    eyebrow='Technical',
    desc='實體清晰度指的是 AI 系統能否唯一且正確地辨識你的品牌。名稱寫法不一致、公司與品牌關係不明、資訊無法驗證，都會讓實體訊號散掉。',
    lede='實體清晰度（Entity Clarity）指的是 AI 系統能否把「你」與其他同名或相似的東西區分開，並正確描述你是什麼。這是 GEO 的核心——如果模型無法確定你是誰，它就不會在回答中主動提到你，即使你的內容寫得再好。',
    schema='TechArticle',
    sections=[
        sec('Problem', '實體訊號是怎麼散掉的', [
            ('p', '多數網站不是「沒有實體資訊」，而是「同一件事有好幾種寫法」。常見的散射來源：'),
            ('ul', [
                '<strong>品牌名稱寫法不一</strong>：有時加空格、有時全大寫、有時中英夾雜、有時用簡稱。對人來說是同一個，對機器來說是四個字串。',
                '<strong>品牌與法人的關係不明</strong>：網站上是品牌名，發票與合約上是公司名，兩者從未在同一處被連結起來。',
                '<strong>產品線與品牌混用</strong>：把產品名當品牌用，或反過來。模型無法判斷層級關係。',
                '<strong>聯絡資訊只有表單</strong>：沒有可驗證的地址、電話、統編，實體就缺乏錨點。',
                '<strong>各平台簡介不一致</strong>：官網、社群、目錄各寫各的，彼此矛盾。',
            ]),
        ]),
        sec('Fix', '怎麼收斂', [
            ('ol', [
                '<strong>先決定唯一的正式寫法</strong>，包含中文名、英文名、簡稱。寫下來，全站統一。',
                '<strong>在一個地方把關係講清楚</strong>：品牌屬於哪個法人、旗下有哪些產品線、彼此是什麼關係。'
                '這正是 %s 這類頁面的作用。' % a(BRAND, '品牌說明頁'),
                '<strong>用 Organization 結構化資料把它機器可讀化</strong>，包含 name、url、logo，'
                '以及可驗證的 address、telephone、identifier（例如統一編號）。見 %s。' % a('/aeo/schema', 'Schema 指南'),
                '<strong>在 llms.txt 中重述一次實體關係</strong>。見 %s。' % a('/aeo/llms-txt', 'llms.txt'),
                '<strong>把各外部平台的簡介統一</strong>。這一步最花時間但影響最大——跨來源的一致性是實體訊號的主要來源。',
            ]),
        ]),
        sec('Ambiguity', '同名問題特別難處理', [
            ('p', '如果你的品牌名是常見詞彙，或與其他公司同名，模型判斷錯誤的機率會顯著提高。'),
            ('p', '可行的做法是<strong>提供足夠的佐證脈絡</strong>：讓品牌名總是與特定的產品類別、地區、法人名稱一起出現。'
                  '單獨的品牌名很難消歧義，但「品牌名 + 產業 + 台灣 + 統編」的組合就相當獨特。'),
            ('note', '<strong>這也是量測時的陷阱。</strong>用可能同名的簡稱去量測 AI 是否提及你的品牌，'
                     '很容易把別人的提及算成自己的。可靠的做法是要求佐證——例如同時出現全名、產品名、'
                     '或你的網域——否則不計為有效提及。'),
        ]),
        sec('Score', '在評分中的位置', [
            ('p', '%s 的 Entity Clarity 面向配分 15 分，是最高的一級。'
                  '它檢視 Organization 結構化資料、About／關於我們區段、Contact 聯絡方式是否具備且一致。'
                  '信任訊號（Trust Signals）也併入此面向計算——詳見 %s。'
                  % (a(METHOD, 'AI Readiness Score'), a('/aeo/trust-signals', '信任訊號'))),
        ]),
    ],
    faq=[
        ('公司名和品牌名不一樣，會有問題嗎？',
         '本身不是問題，很常見。問題出在兩者從未被明確連結。應該在網站上至少一個地方清楚寫出「品牌 X 是公司 Y 旗下的品牌」，並在 Organization 結構化資料與 llms.txt 中一致呈現。'),
        ('一定要公開地址和電話嗎？',
         '不是必要，但有幫助。可驗證的資訊會提高模型對實體的信心。若有隱私考量，至少提供可查證的法人資訊（例如統一編號）與有效的聯絡管道。'),
        ('改了名稱之後怎麼辦？',
         '需要時間收斂。做法是全站統一為新名稱、在結構化資料中保留 alternateName、並在一個頁面明確說明更名事實。模型更新到新名稱需要時間，無法立即生效。'),
        ('社群帳號的簡介也要一致嗎？',
         '要。跨來源的一致性是實體訊號的主要來源之一。官網、社群、產業目錄的描述若彼此矛盾，會削弱整體訊號。'),
    ],
    related=[('/aeo/trust-signals', '信任訊號'), ('/aeo/what-is-geo', 'GEO 是什麼'),
             ('/aeo/schema', 'AEO 需要哪些 Schema'), (BRAND, 'ShellFans 是什麼')],
))

PAGES.append(page(
    url='/aeo/answer-readiness',
    title='答覆整備度：讓內容具備可被擷取的形狀 - ShellFans',
    h1='答覆整備度：讓內容具備可被擷取的形狀',
    eyebrow='Technical',
    desc='答覆整備度指的是內容能否被答案引擎切出可直接引用的段落。本頁說明段落自足、定義先行、比較表與限制說明等具體寫法。',
    lede='答覆整備度（Answer Readiness）指的是內容能不能被答案引擎切出「可以直接拿來當答案」的段落。同樣的資訊，寫成鋪陳式的長文與寫成定義先行的段落，被擷取的機率差很多。這與內容品質是兩件事——好文章不一定好擷取。',
    schema='TechArticle',
    sections=[
        sec('Principle', '四個具體原則', [
            ('h3', '一、段落要能單獨成立'),
            ('p', '假設讀者只會看到這一段，沒有前後文。這段是否仍然正確且完整？'
                  '出現「如前所述」「見上表」「這個做法」這類指涉，被擷取後就失去意義。'),
            ('h3', '二、定義放在最前面'),
            ('p', '標題問「X 是什麼」，前 100–150 字就要給出直接回答，不要先鋪陳背景。'
                  '這一段通常就是被擷取的內容。鋪陳可以放在回答之後。'),
            ('h3', '三、用結構表達結構'),
            ('p', '比較關係用表格，步驟用有序清單，並列項目用無序清單。'
                  '把比較寫成一大段文字，模型要自己還原出結構，容易出錯。'),
            ('h3', '四、主動寫限制與不適用情境'),
            ('p', '「什麼情況下不該用」是使用者實際會問的問題，也是最容易被引用的段落類型之一。'
                  '只寫優點的內容，可引用的部分反而很少。'),
        ]),
        sec('Rewrite', '改寫範例', [
            ('p', '同一個資訊的兩種寫法：'),
            ('table', {
                'caption': '鋪陳式與定義先行的差異',
                'cols': ['寫法', '內容', '可擷取性'],
                'rows': [
                    ['鋪陳式',
                     '「隨著 AI 技術的快速發展，企業面臨前所未有的挑戰⋯⋯在這樣的背景下，'
                     '我們認為有必要重新思考網站的角色⋯⋯因此 AEO 應運而生。」',
                     '低。前 150 字沒有回答任何問題'],
                    ['定義先行',
                     '「AEO 是 Answer Engine Optimization 的縮寫，指讓網站內容能被 ChatGPT、'
                     'Perplexity 等答案引擎理解並引用的做法。它關心的不是排名，而是是否成為答案的一部分。」',
                     '高。第一句就是完整答案'],
                ],
            }),
        ]),
        sec('Structure', '整頁的結構', [
            ('ol', [
                '<strong>一個 H1</strong>，直接對應使用者會問的問題。',
                '<strong>導言段</strong>，100–150 字給出直接回答。',
                '<strong>H2 分段</strong>，每段處理一個子問題。',
                '<strong>表格或清單</strong>，用於比較與步驟。',
                '<strong>限制與常見錯誤</strong>，獨立成段。',
                '<strong>FAQ</strong>，處理導言未涵蓋的具體疑問。見 %s。' % a('/aeo/faq-schema', 'FAQ Schema'),
            ]),
            ('p', '%s 的 Answer Readiness 面向配分 15 分，檢視是否有問答式內容、'
                  '是否設定 meta description，以及可讀文字量是否足以擷取出可引用段落。'
                  % a(METHOD, 'AI Readiness Score')),
        ]),
        sec('Mistakes', '常見錯誤', [
            ('ul', [
                '<strong>把重點藏在文章中段</strong>。讀者可能會讀完，模型通常只取前面。',
                '<strong>大量使用代名詞</strong>。「它」「這個」在脫離上下文後無法解析。',
                '<strong>一段講太多件事</strong>。一段一個重點，才切得乾淨。',
                '<strong>全部是形容詞</strong>。「業界領先的解決方案」不含任何可引用的事實。',
                '<strong>內容需要互動才出現</strong>。要點擊分頁、要捲動載入、要 JavaScript 執行的內容，爬蟲多半讀不到。',
            ]),
        ]),
    ],
    faq=[
        ('文章要寫多長？',
         '沒有標準長度。關鍵是每個段落都有明確的單一重點且能獨立成立。硬把短內容拉長只會稀釋重點，讓可擷取的段落變少。'),
        ('用條列會不會顯得不專業？',
         '不會，而且對答案引擎更友善。條列與表格明確表達了項目之間的關係，模型不需要自己從文字中還原結構，出錯機率較低。'),
        ('已經寫好的文章要全部重寫嗎？',
         '不必。優先處理最重要的幾頁，方法是把結論移到最前面、拆開過長的段落、把比較關係改成表格。這三個調整成本低但效果明顯。'),
        ('答覆整備度和內容品質是同一件事嗎？',
         '不是。好文章不一定好擷取——文學性強、需要通篇閱讀才理解的內容，對人有價值但對答案引擎不友善。兩者要分開看待，並依內容目的取捨。'),
    ],
    related=[('/aeo/faq-schema', 'FAQ Schema'), ('/aeo/aeo-vs-seo', 'AEO 與 SEO 的差異'),
             (METHOD, 'AI Readiness Score 方法論'), (CHECKER, '免費檢測工具')],
))

PAGES.append(page(
    url='/aeo/trust-signals',
    title='信任訊號是什麼？AI 如何判斷網站可不可信 - ShellFans',
    h1='信任訊號：AI 如何判斷你可不可信',
    eyebrow='Technical',
    desc='信任訊號是可對外驗證的事實，用來讓 AI 系統判斷網站與品牌的可信度。本頁說明哪些訊號真的有作用、哪些只是自我宣稱。',
    lede='信任訊號指的是<strong>可以對外驗證的事實</strong>——統一編號、註冊地址、專利號、可查證的聯絡方式。它們的共同點是「不能自己說了算」。相對地，「業界領先」「專業團隊」這類自我描述無法驗證，對 AI 判斷可信度幾乎沒有作用。',
    schema='TechArticle',
    sections=[
        sec('Types', '哪些算是信任訊號', [
            ('table', {
                'caption': '可驗證與不可驗證的資訊',
                'cols': ['類型', '例子', '是否可驗證'],
                'rows': [
                    ['法人資訊', '公司全名、統一編號、註冊地址', '✅ 可對政府登記查證'],
                    ['聯絡管道', '市話、實體地址、公司網域的信箱', '✅ 可測試是否有效'],
                    ['智慧財產', '專利號、商標註冊號', '✅ 可對專利／商標資料庫查證'],
                    ['法遵文件', '隱私權政策、服務條款', '✅ 存在與否可直接確認'],
                    ['明確的方法說明', '評分怎麼算、資料怎麼來', '✅ 可對照實際行為'],
                    ['自我形容', '「業界領先」「最專業」', '❌ 無法驗證'],
                    ['無來源的數字', '「服務超過千家企業」（無佐證）', '❌ 無法驗證'],
                    ['未經授權的客戶名稱', '列出品牌 logo 但無合作證明', '❌ 且有法律風險'],
                ],
            }),
        ]),
        sec('Why', '為什麼「可驗證」是關鍵', [
            ('p', '答案引擎在選擇引用來源時，需要降低給出錯誤資訊的風險。'
                  '一個能對外交叉比對的事實，比一句無法查證的形容詞有用得多。'),
            ('p', '這也解釋了一個常見的困惑：為什麼把首頁寫得很有氣勢，AEO 分數卻沒有提升。'
                  '因為那些文字對機器而言不含任何可驗證的資訊。'),
        ]),
        sec('Do', '具體該做什麼', [
            ('ol', [
                '<strong>在頁尾放完整法人資訊</strong>：公司全名、統一編號、地址、電話。這是成本最低、效益最直接的一步。',
                '<strong>用 Organization 結構化資料把它機器可讀化</strong>，欄位與頁面上顯示的完全一致。見 %s。' % a('/aeo/schema', 'Schema 指南'),
                '<strong>提供真實可用的聯絡方式</strong>，不要只有表單。',
                '<strong>把方法說清楚</strong>。如果你提供評分、報告或分析，說明它怎麼算、資料哪裡來、限制是什麼。',
                '<strong>誠實標註限制</strong>。主動寫出「我們不能保證什麼」，比全是承諾更可信。',
            ]),
            ('note', '<strong>反過來說，這些會扣分：</strong>沒有授權就列出客戶 logo、'
                     '引用無來源的統計數字、宣稱與知名品牌合作但無法佐證。'
                     '除了可信度問題，這些做法本身也有法律風險。'),
        ]),
        sec('Score', '在評分中的位置', [
            ('p', '在 %s 中，信任訊號<strong>沒有獨立的面向</strong>，而是併入 Entity Clarity（15 分）計算，'
                  '與 Organization 結構化資料、About、Contact 一起評估。'
                  '這個設計反映的是：信任訊號與實體辨識本來就是同一件事的兩面——'
                  '模型要先確定你是誰，才談得上你可不可信。' % a(METHOD, 'AI Readiness Score')),
        ]),
    ],
    faq=[
        ('小公司沒有專利也沒有獎項，怎麼建立信任訊號？',
         '專利與獎項不是必要條件。完整且可查證的法人資訊（公司全名、統一編號、地址、有效聯絡方式）、清楚的服務說明、誠實標註的限制，這些對任何規模的公司都做得到，而且是最基本也最有效的訊號。'),
        ('可以寫「服務超過一千家企業」嗎？',
         '如果數字真實且必要時可提出佐證，可以。若無法佐證，建議改為可驗證的描述方式。無來源的數字對 AI 判斷沒有幫助，且一旦被質疑會反過來損害可信度。'),
        ('客戶 logo 牆有幫助嗎？',
         '前提是取得授權。未經授權使用客戶商標有法律風險，且圖片本身對機器可讀性的幫助有限。若有授權，搭配可查證的文字說明會比純圖片有效。'),
        ('隱私權政策和服務條款真的會影響嗎？',
         '會，但方式是間接的。它們的存在代表這是一個正常運作的商業實體，屬於基礎的可信度指標。缺少這些文件在多數評估框架中都會被視為警訊。'),
    ],
    related=[('/aeo/entity-clarity', '實體清晰度'), ('/aeo/what-is-geo', 'GEO 是什麼'),
             (METHOD, 'AI Readiness Score 方法論'), (CHECKER, '免費檢測工具')],
))


# ---------------------------------------------------------------------------
# D. 商業服務 / BOFU
# ---------------------------------------------------------------------------
PAGES.append(page(
    url='/aeo/managed-hosting',
    title='AEO Managed Hosting 是什麼？AI-ready 網站代管 - ShellFans',
    h1='AEO Managed Hosting 是什麼？',
    eyebrow='Service',
    desc='AEO Managed Hosting 是把網站代管與 AI 搜尋整備結合的服務：主機維運之外，同時持續維護 robots.txt、結構化資料、llms.txt 與內容結構，並定期量測。',
    lede='AEO Managed Hosting 是把「網站代管」與「AI 搜尋整備」合併的服務形態。一般代管只負責主機能不能跑；AEO 代管在此之上，持續維護 robots.txt 對 AI 爬蟲的規則、結構化資料、llms.txt 與內容結構，並定期量測 AI 搜尋中的能見度變化。',
    schema='Service',
    service_type='AEO Managed Hosting',
    sections=[
        sec('Difference', '與一般網站代管的差別', [
            ('table', {
                'caption': '一般代管與 AEO 代管的差異',
                'cols': ['項目', '一般網站代管', 'AEO Managed Hosting'],
                'rows': [
                    ['主機維運', '✅ 可用性、備份、憑證', '✅ 相同'],
                    ['AI 爬蟲政策', '❌ 不涉及', '✅ 持續維護並驗證實際生效'],
                    ['結構化資料', '❌ 不涉及', '✅ 建立並隨內容變更維護'],
                    ['llms.txt', '❌ 不涉及', '✅ 建立並與網站內容同步'],
                    ['內容結構', '❌ 不涉及', '✅ 依答覆整備原則調整'],
                    ['能見度量測', '❌ 不涉及', '✅ 定期觀測並提供趨勢'],
                ],
            }),
            ('p', '關鍵差異在「持續」二字。AEO 不是一次性設定——網站改版、內容更新、CDN 規則調整都可能'
                  '在無人察覺的情況下破壞既有整備。詳見 %s。' % a('/aeo/implementation', '導入流程')),
        ]),
        sec('Fit', '適合誰、不適合誰', [
            ('h3', '適合'),
            ('ul', [
                '網站是主要的獲客管道，且客戶會用 AI 查詢你的產品類別。',
                '內部沒有專責的技術或 SEO 人力，或有但已滿載。',
                '網站需要持續更新內容，且每次更新都可能影響既有整備。',
                '希望有可追蹤的量測基準，而不是憑感覺判斷成效。',
            ]),
            ('h3', '不適合'),
            ('ul', [
                '<strong>網站幾乎不更新</strong>。這種情況做一次性整備即可，長期代管的價值有限。',
                '<strong>內部已有能持續維護的技術團隊</strong>。本站的技術頁面已公開具體做法，可自行實作。',
                '<strong>期待短期內看到 AI 引用率明顯變化</strong>。這不是這個服務能承諾的事。',
                '<strong>網站以會員內容為主</strong>。不對外公開的內容，AI 爬蟲本來就抓不到。',
            ]),
        ]),
        sec('Deliver', '交付內容', [
            ('ol', [
                '<strong>現況評估</strong>：以 %s 產出基準分數與具體待修清單。' % a(CHECKER, 'AI Readiness Score'),
                '<strong>技術整備</strong>：robots.txt、結構化資料、llms.txt、內容結構調整。',
                '<strong>驗證</strong>：確認設定在 CDN／WAF 之後仍實際生效，而非只寫在設定檔裡。',
                '<strong>持續維護</strong>：內容或架構變更時同步更新整備項目。',
                '<strong>定期量測</strong>：固定條件觀測 AI 搜尋中的能見度，提供趨勢而非單次快照。',
            ]),
        ]),
        sec('Pricing', '費用', [
            ('p', '費用依網站規模、頁面數量、既有整備程度與需要的維護頻率而定，'
                  '沒有適用所有情況的固定價格。影響報價的變數與計算邏輯，'
                  '詳見 %s。' % a('/aeo/cost', 'AEO 費用怎麼計算')),
            ('p', '若想先確認自己的起點，可以直接跑一次 %s——'
                  '免費、不需註冊，會列出八個面向的分數與具體缺口。' % a(CHECKER, '免費檢測')),
        ]),
    ],
    faq=[
        ('可以只做整備不要代管嗎？',
         '可以。技術整備與主機代管是可分開的。合併的好處是設定變更能立即驗證、網站改版時整備不會被覆蓋；分開則保留既有主機安排。適合哪一種取決於你的既有架構與內部維護能力。'),
        ('會保證 ChatGPT 引用我的網站嗎？',
         '不會，也不應該有服務做這種保證。能承諾的是技術整備的完成度與量測的持續性，也就是讓網站具備被正確理解與引用的基礎條件。實際是否被引用由各 AI 平台自行決定。'),
        ('多久會看到效果？',
         '技術整備通常數週內完成並可立即驗證（例如爬蟲能否正常存取、結構化資料是否可解析）。但 AI 搜尋中的能見度變化需要更長時間，且需累積足夠觀測點才能判斷趨勢，無法承諾具體天數。'),
        ('已經有網站了，要重做嗎？',
         '多數情況不需要。整備工作以既有網站為基礎進行調整，包含 robots.txt、結構化資料、內容結構。只有在既有架構讓爬蟲無法讀取核心內容時（例如內容完全依賴 JavaScript 載入），才需要討論架構調整。'),
    ],
    related=[(SERVICE, 'AEO/GEO 代管服務'), ('/aeo/cost', 'AEO 費用怎麼計算'),
             ('/aeo/implementation', '導入流程'), ('/aeo/consulting', 'AEO 顧問服務')],
    cta=CTA_CHECK, cta2=CTA_CONTACT,
))

PAGES.append(page(
    url='/aeo/consulting',
    title='AEO 顧問服務：範圍、產出與適用情境 - ShellFans',
    h1='AEO 顧問服務',
    eyebrow='Service',
    desc='AEO 顧問服務適合已有技術團隊、需要方向與稽核而非代工的組織。本頁說明服務範圍、實際產出、與代管服務的差異，以及不適用的情況。',
    lede='AEO 顧問服務提供的是<strong>判斷與方法</strong>，不是代工。適合已有技術或行銷團隊、能自行執行，但需要確認方向是否正確、缺口在哪裡的組織。若你需要的是有人把事情做完，%s 會更合適。' % a('/aeo/managed-hosting', 'Managed Hosting'),
    schema='Service',
    service_type='AEO Consulting',
    sections=[
        sec('Scope', '服務範圍', [
            ('ol', [
                '<strong>現況稽核</strong>：以 %s 為基準，加上人工檢視，產出具體缺口清單與優先順序。' % a(METHOD, 'AI Readiness Score'),
                '<strong>優先順序建議</strong>：依投入成本與預期影響排序，明確指出哪些先做、哪些可以不做。',
                '<strong>實作規格</strong>：提供你的團隊可直接施工的具體規格，而非原則性建議。',
                '<strong>量測機制設計</strong>：協助建立固定條件的觀測方式，讓後續成效有基準可比。',
                '<strong>成果複查</strong>：實作完成後驗證是否真的生效——寫在設定檔裡與實際生效是兩回事。',
            ]),
        ]),
        sec('Fit', '適合誰、不適合誰', [
            ('h3', '適合'),
            ('ul', [
                '已有前端或 SEO 團隊，缺的是 AEO 特定的判斷。',
                '想先確認值不值得投入，再決定要不要大規模執行。',
                '網站架構特殊（例如大型電商、多語系、複雜的 CDN 配置），需要客製化判斷。',
                '內部對「該做什麼」有分歧，需要外部依據來收斂。',
            ]),
            ('h3', '不適合'),
            ('ul', [
                '<strong>沒有執行資源</strong>。顧問給的是規格，需要有人施工。這種情況直接選代管服務更實際。',
                '<strong>只想要一份報告</strong>。免費的 %s 已能產出現況分數與缺口清單，不需要付費。' % a(CHECKER, '檢測工具'),
                '<strong>期待保證成效</strong>。顧問能保證的是稽核的完整性與建議的依據，不是第三方 AI 平台的行為。',
            ]),
        ]),
        sec('Differ', '與代管服務的差別', [
            ('table', {
                'caption': '顧問服務與代管服務的差異',
                'cols': ['項目', '顧問服務', 'Managed Hosting'],
                'rows': [
                    ['產出形式', '稽核報告、實作規格、優先順序', '完成的整備 + 持續維護'],
                    ['誰執行', '你的團隊', 'ShellFans'],
                    ['期間', '專案制', '持續'],
                    ['適合的前提', '有執行資源', '沒有或已滿載'],
                    ['主機', '不涉及', '包含'],
                ],
            }),
        ]),
        sec('Price', '費用', [
            ('p', '顧問服務依網站規模、稽核深度與是否包含複查而定。'
                  '影響費用的變數見 %s。實際範圍需要先了解你的網站狀況才能評估，'
                  '可以先 %s 說明需求。' % (a('/aeo/cost', 'AEO 費用怎麼計算'), a(CONTACT, '聯繫我們'))),
        ]),
    ],
    faq=[
        ('顧問服務和免費檢測有什麼不同？',
         '免費檢測是自動化的技術面掃描，產出八個面向的分數與可自動判定的缺口。顧問服務加上人工判讀：哪些缺口對你的業務真正重要、以什麼順序處理、你的特殊架構該怎麼處理，這些自動化工具無法給出。'),
        ('可以只做一次稽核嗎？',
         '可以。單次稽核適合用來確認方向與規模，再決定後續投入。但要留意 AEO 的整備會因網站改版或內容更新而失效，單次稽核的有效期取決於網站的變動頻率。'),
        ('顧問會幫忙寫程式嗎？',
         '顧問服務提供的是規格而非施工。若需要有人直接執行，適合的是 Managed Hosting。兩者可以搭配——先顧問確認方向，再決定自行執行或委外。'),
    ],
    related=[('/aeo/managed-hosting', 'AEO Managed Hosting'), ('/aeo/cost', 'AEO 費用怎麼計算'),
             ('/aeo/how-to-choose-agency', '如何挑選 AEO 廠商'), (CHECKER, '免費檢測工具')],
    cta=CTA_CONTACT, cta2=CTA_CHECK,
))

PAGES.append(page(
    url='/aeo/cost',
    title='AEO 費用怎麼計算？影響報價的變數 - ShellFans',
    h1='AEO 費用怎麼計算？',
    eyebrow='Pricing',
    desc='AEO 服務沒有統一定價，費用取決於網站規模、既有整備程度、內容調整範圍與維護頻率。本頁拆解影響報價的變數，以及如何判斷報價是否合理。',
    lede='AEO 服務沒有業界統一定價，因為工作量差異極大——同樣是「做 AEO」，一個十頁的形象網站與一個上千頁的電商網站，投入可能差十倍以上。與其比較總價，更實際的做法是<strong>先看報價包含哪些項目、由誰執行、如何驗收</strong>。',
    schema='TechArticle',
    sections=[
        sec('Variables', '影響費用的五個變數', [
            ('table', {
                'caption': '影響 AEO 報價的變數',
                'cols': ['變數', '為什麼影響費用'],
                'rows': [
                    ['網站頁數與模板數', '結構化資料與內容調整需逐模板處理。頁數多但模板少，成本不會等比增加'],
                    ['既有整備程度', '已有良好 SEO 基礎的網站，AEO 的增量工作較少。可先用免費檢測確認起點'],
                    ['是否需要內容改寫', '技術整備成本相對固定；內容結構調整則與頁數直接相關，通常是最大的變數'],
                    ['架構複雜度', '多語系、多網域、複雜 CDN 或 WAF 配置會顯著增加驗證工作'],
                    ['是否包含持續維護', '一次性整備與長期維護是不同的計價基礎'],
                ],
            }),
        ]),
        sec('Structure', '常見的計價方式', [
            ('ul', [
                '<strong>一次性專案</strong>：範圍明確的整備工作，驗收後結案。適合網站更新頻率低的情況。',
                '<strong>月費制</strong>：包含持續維護與定期量測。適合網站持續更新、需要確保整備不被改版破壞的情況。',
                '<strong>稽核制</strong>：只做評估與規格，不含執行。適合有內部執行資源者，見 %s。' % a('/aeo/consulting', '顧問服務'),
            ]),
            ('note', '<strong>ShellFans 的實際報價</strong>依網站規模與導入範圍評估，'
                     '需先了解網站現況才能提出。可以先跑一次 %s 取得基準分數與缺口清單，'
                     '再 %s 討論。' % (a(CHECKER, '免費檢測'), a(CONTACT, '聯繫我們'))),
        ]),
        sec('Judge', '怎麼判斷報價合不合理', [
            ('p', '不要只比總價。以下幾個問題比價格本身更能區分服務品質：'),
            ('ol', [
                '<strong>「這個報價包含哪些具體項目？」</strong>要求列出可驗收的交付物，而非「AEO 優化」這種籠統描述。',
                '<strong>「怎麼驗證設定真的生效？」</strong>好的答案會提到實際測試爬蟲存取、檢查 CDN 層，'
                '而不只是「我們會設定 robots.txt」。',
                '<strong>「成效怎麼量測？」</strong>如果對方答不出固定的量測條件，那就沒有辦法驗收。',
                '<strong>「你們保證什麼？」</strong>承諾「保證被 ChatGPT 引用」的直接排除——沒有人能保證第三方平台的行為。',
                '<strong>「內容改寫是誰做？」</strong>這通常是最大的成本項目，必須事先講清楚範圍。',
            ]),
            ('p', '更完整的評估準則見 %s。' % a('/aeo/how-to-choose-agency', '如何挑選 AEO 廠商')),
        ]),
        sec('DIY', '自己做要多少成本', [
            ('p', '技術整備的部分，具備前端或 SEO 經驗的團隊多半可自行完成。本站已公開具體做法：'),
            ('ul', [
                '%s — robots.txt 的設定與驗證' % a('/aeo/ai-crawler', 'AI 爬蟲'),
                '%s — 該加哪些結構化資料' % a('/aeo/schema', 'Schema'),
                '%s — 摘要入口怎麼寫' % a('/aeo/llms-txt', 'llms.txt'),
                '%s — 內容結構怎麼調整' % a('/aeo/answer-readiness', '答覆整備度'),
            ]),
            ('p', '真正難以自行處理的通常是兩件事：<strong>持續量測</strong>（需要固定的觀測機制與時間序列）'
                  '與<strong>改版後的回歸驗證</strong>（整備很容易在無人察覺時被破壞）。'
                  '這也是委外服務主要的價值所在。'),
        ]),
    ],
    faq=[
        ('AEO 一個月要多少錢？',
         '沒有統一價格。費用取決於網站規模、既有整備程度、是否包含內容調整與持續維護。同樣是「做 AEO」，十頁的形象網站與上千頁的電商網站投入可能差十倍以上。建議先確認需求範圍再取得報價。'),
        ('為什麼不同廠商報價差那麼多？',
         '通常是範圍不同而非單價不同。要比較的是交付項目：是否包含內容改寫、是否包含持續維護、是否包含量測、驗收標準是什麼。只比總價很容易買到範圍縮水的版本。'),
        ('可以先做一部分嗎？',
         '可以，而且建議如此。技術整備（robots.txt、結構化資料、llms.txt）成本相對固定且效益明確，適合先做。內容結構調整成本較高，可以先處理最重要的幾頁再評估。'),
        ('免費檢測和付費服務差在哪？',
         '免費檢測提供自動化的技術面掃描與缺口清單，不需註冊即可使用。付費服務的差異在於執行、人工判讀、持續維護與量測——也就是把清單上的項目真的做完並確保它不會退回去。'),
    ],
    related=[('/aeo/implementation', 'AEO 導入流程'), ('/aeo/managed-hosting', 'AEO Managed Hosting'),
             ('/aeo/how-to-choose-agency', '如何挑選 AEO 廠商'), (CHECKER, '免費檢測工具')],
    cta=CTA_CHECK, cta2=CTA_CONTACT,
))

PAGES.append(page(
    url='/aeo/implementation',
    title='AEO 導入流程：實際會經歷哪些階段 - ShellFans',
    h1='AEO 導入流程',
    eyebrow='Process',
    desc='AEO 導入分為現況評估、技術整備、驗證、內容調整與持續量測五個階段。本頁說明每個階段的工作、產出與常見卡點。',
    lede='AEO 導入通常分五個階段：<strong>現況評估 → 技術整備 → 驗證 → 內容調整 → 持續量測</strong>。前三階段成本相對固定且可快速驗收；第四階段成本最高、變數最大；第五階段是唯一沒有終點的部分——也是最常被省略、然後在改版後付出代價的部分。',
    schema='TechArticle',
    sections=[
        sec('Stages', '五個階段', [
            ('h3', '階段一：現況評估'),
            ('p', '取得基準分數與具體缺口清單。這一步必須在任何施工之前完成——沒有基準，之後就無法判斷改動有沒有效。'
                  '可用 %s 取得八個面向的分數。' % a(CHECKER, '免費檢測工具')),
            ('p', '<strong>產出</strong>：基準分數、缺口清單、優先順序。'),
            ('h3', '階段二：技術整備'),
            ('p', 'robots.txt 的 AI 爬蟲規則、結構化資料、llms.txt、sitemap、canonical。'
                  '這些項目成本相對固定，且與網站頁數關係不大。'),
            ('p', '<strong>產出</strong>：可驗收的技術設定。'),
            ('h3', '階段三：驗證'),
            ('p', '<strong>這一步最常被跳過，但省略的代價最高。</strong>'
                  '設定寫在檔案裡不等於實際生效——CDN 的 bot 規則、WAF、快取都可能讓 robots.txt 的意圖失效。'),
            ('p', '<strong>產出</strong>：以實際 user-agent 測試的回應記錄、access log 佐證。'),
            ('h3', '階段四：內容調整'),
            ('p', '依 %s 的原則調整內容結構。這是成本最高的階段，且與頁數直接相關。'
                  '務實的做法是先處理流量或商業價值最高的幾頁，而非全站一次到位。'
                  % a('/aeo/answer-readiness', '答覆整備度')),
            ('p', '<strong>產出</strong>：調整後的頁面。'),
            ('h3', '階段五：持續量測'),
            ('p', '固定問題、固定平台、定期觀測。這個階段沒有終點，但它是唯一能回答「有沒有用」的方式。'),
            ('p', '<strong>產出</strong>：可比較的時間序列。'),
        ]),
        sec('Pitfalls', '常見卡點', [
            ('table', {
                'caption': '各階段的常見卡點',
                'cols': ['階段', '常見卡點', '處理方式'],
                'rows': [
                    ['評估', '沒有先取得基準就開始改', '任何改動前先跑一次檢測並保留結果'],
                    ['技術整備', 'robots.txt 群組不繼承導致誤擋', '每支爬蟲明確寫出規則，見 %s' % a('/aeo/ai-crawler', 'AI 爬蟲')],
                    ['驗證', '只看設定檔，沒測實際回應', '以真實 user-agent 測試並核對 access log'],
                    ['內容調整', '想一次改完全站', '先做商業價值最高的頁面，驗證有效再擴大'],
                    ['量測', '換模型或換問題導致數據不可比', '固定量測條件；條件變更時明確標記為新的基準'],
                ],
            }),
        ]),
        sec('Regression', '為什麼需要持續維護', [
            ('note', '<strong>AEO 整備很容易在無人察覺的情況下失效。</strong>'
                     '網站改版覆蓋了結構化資料、新的 CDN 規則擋掉了爬蟲、內容更新後 llms.txt 沒跟著改——'
                     '這些都不會報錯，只會安靜地讓分數退回去。'),
            ('p', '因此「做完了」是個危險的想法。可行的做法是把檢測納入例行流程：'
                  '每次改版後重跑一次、定期排程檢查，或直接採用包含持續維護的 %s。'
                  % a('/aeo/managed-hosting', 'Managed Hosting')),
        ]),
        sec('Time', '需要多久', [
            ('p', '各階段的時間差異很大，且高度取決於網站規模與內部配合速度，'
                  '因此本頁<strong>不提供保證天數</strong>。可以說的是相對關係：'),
            ('ul', [
                '階段一到三（評估、技術整備、驗證）的工作量相對固定，與頁數關係不大。',
                '階段四（內容調整）的時間與要處理的頁數成正比，是總時程的主要變數。',
                '階段五（量測）需要累積足夠的觀測點才能判斷趨勢，這部分無法壓縮——'
                '這是資料本身的性質，不是執行速度的問題。',
            ]),
        ]),
    ],
    faq=[
        ('可以跳過某些階段嗎？',
         '評估與驗證不建議跳過。沒有基準就無法判斷成效，沒有驗證則可能整套設定其實沒生效。內容調整可以分批進行，量測可以簡化但不建議完全省略。'),
        ('多久會看到效果？',
         '技術整備的效果可以立即驗證（爬蟲能否存取、結構化資料能否解析）。但 AI 搜尋能見度的變化需要更長時間，且需累積足夠觀測點才能區分趨勢與雜訊。任何承諾具體天數的說法都應該要求說明依據。'),
        ('改版後要重做嗎？',
         '需要重新驗證，但通常不必重做。重點是確認改版有沒有覆蓋既有的結構化資料、robots.txt 或內容結構。把檢測納入改版後的例行檢查，是成本最低的做法。'),
    ],
    related=[('/aeo/cost', 'AEO 費用怎麼計算'), ('/aeo/managed-hosting', 'AEO Managed Hosting'),
             ('/aeo/ai-crawler', 'AI 爬蟲總覽'), (CHECKER, '免費檢測工具')],
    cta=CTA_CHECK, cta2=CTA_SERVICE,
))


# ---------------------------------------------------------------------------
# E. 採購與比較
# ---------------------------------------------------------------------------
PAGES.append(page(
    url='/aeo/taiwan-companies',
    title='台灣有哪些 AEO 服務商？市場現況與評估準則 - ShellFans',
    h1='台灣有哪些 AEO 服務商？',
    eyebrow='Market',
    desc='台灣的 AEO/GEO 服務市場仍在形成中，提供者來自 SEO 代理商、網站開發商與專門服務商三類。本頁說明市場結構與可驗證的評估準則，不提供廠商排名。',
    lede='台灣的 AEO/GEO 服務市場仍在形成階段，目前的提供者大致來自三類：既有 SEO 代理商延伸、網站開發商加值、以及專門服務商。<strong>本頁不提供廠商排名或名單</strong>——沒有公開且可驗證的市場資料支持這種排名，任何自稱第一的說法都缺乏依據。以下提供的是你可以自己驗證的評估準則。',
    schema='TechArticle',
    sections=[
        sec('Landscape', '市場結構', [
            ('table', {
                'caption': '台灣 AEO 服務提供者的三種類型',
                'cols': ['類型', '通常擅長', '通常較弱'],
                'rows': [
                    ['SEO 代理商延伸',
                     '關鍵字研究、內容策略、既有的量測習慣',
                     'AI 爬蟲的技術細節、結構化資料的深度實作'],
                    ['網站開發商加值',
                     '技術實作、能直接改動網站、驗證設定是否生效',
                     '內容策略、持續量測機制'],
                    ['專門服務商',
                     '對 AEO 特定議題較深入、通常有自建的量測工具',
                     '市場較新，可參考的長期案例少'],
                ],
            }),
            ('p', '這個分類是為了幫你判斷「對方的強項在哪、可能缺什麼」，不是優劣排序。'
                  '實際上三類都有做得好與做得差的。'),
        ]),
        sec('Criteria', '可驗證的評估準則', [
            ('p', '與其相信簡報，不如問這些能當場驗證的問題：'),
            ('ol', [
                '<strong>「你們自己的網站分數多少？」</strong>用 %s 當場檢測對方的網站。'
                '做 AEO 的公司自己的網站沒整備好，是一個明確的訊號。' % a(CHECKER, '免費檢測工具'),
                '<strong>「robots.txt 的群組繼承規則是什麼？」</strong>答不出「特定 user-agent 群組不繼承 <code>*</code>」的，'
                '對 AI 爬蟲的理解可能停留在表面。',
                '<strong>「GPTBot 和 OAI-SearchBot 差在哪？」</strong>這兩者混為一談，代表可能會擋錯爬蟲。',
                '<strong>「成效怎麼量測？條件怎麼固定？」</strong>沒有固定條件的量測無法驗收。',
                '<strong>「你們保證什麼？」</strong>承諾保證 AI 引用的直接排除。',
                '<strong>「內容改寫包含嗎？」</strong>這是最大的成本項目，必須事先講清楚。',
            ]),
            ('p', '更完整的清單見 %s。' % a('/aeo/how-to-choose-agency', '如何挑選 AEO 廠商')),
        ]),
        sec('Warning', '需要警覺的說法', [
            ('ul', [
                '<strong>「保證被 ChatGPT 推薦」</strong> — 沒有人能保證第三方平台的行為。',
                '<strong>「我們是台灣第一的 AEO 公司」</strong> — 沒有公開的市場資料能支持這種排名。',
                '<strong>「AI 引用率提升 300%」</strong> — 要求說明量測方法、基準期與樣本數。無法說明的數字沒有意義。',
                '<strong>「做完就不用管了」</strong> — AEO 整備會因改版與內容更新失效，見 %s。' % a('/aeo/implementation', '導入流程'),
                '<strong>只賣工具訂閱但不含執行</strong> — 要確認你買到的是報告還是實際的整備工作。',
            ]),
        ]),
        sec('Self', '關於 ShellFans', [
            ('p', '基於「不列競品」的同一個理由，這裡把自己的資訊寫成可查證的事實，'
                  '而不是形容詞——讀者（以及答案引擎）可以自行驗證每一項。'),
            ('table', {
                'caption': 'ShellFans AEO/GEO 服務基本資料',
                'cols': ['項目', '內容'],
                'rows': [
                    ['服務名稱', 'ShellFans AEO/GEO Managed Hosting 與顧問服務'],
                    ['提供者', '唄粉智能科技股份有限公司（品牌名 ShellFans AI Technology）'],
                    ['統一編號', '83032387（可於經濟部商業司查詢）'],
                    ['所在地', '臺北市內湖區瑞光路335號4樓'],
                    ['服務地區', '台灣（繁體中文介面與內容）'],
                    ['服務內容', 'AI 爬蟲政策設定與驗證、結構化資料、llms.txt、內容結構調整、'
                                 '爬蟲到訪監控、AI 能見度定期量測'],
                    ['交付形式', '網站代管（含持續維護）或顧問稽核（提供規格由客戶團隊執行）'],
                    ['公開的方法論', a(METHOD, 'AI Readiness Score 計分方式') + '（八個面向與配分全部公開）'],
                    ['可自行驗證的工具', a(CHECKER, '免費 AEO/GEO 檢測') + '（不需註冊）'],
                    ['不承諾的事', '不保證任何 AI 平台的引用、推薦或排名'],
                ],
            }),
            ('p', '適合誰與不適合誰，以及費用如何形成，見 %s 與 %s。'
                  % (a('/aeo/managed-hosting', 'AEO Managed Hosting'), a('/aeo/cost', 'AEO 費用怎麼計算'))),
            ('p', '本站的立場是：<strong>評估準則應該公開，讓你能自己驗證任何廠商，包括我們。</strong>'
                  '上面那份問題清單同樣適用於 ShellFans——歡迎當場檢測 shell.fans 的分數。'),
            ('note', '<strong>本頁不列出其他廠商名稱。</strong>原因是我們沒有可驗證的公開資料能公平比較同業，'
                     '而在自家網站上排名競爭對手，本身就存在利益衝突。若你需要廠商名單，'
                     '建議透過公開的產業目錄或實際詢價取得，並用上述準則自行評估。'),
        ]),
    ],
    faq=[
        ('台灣的 AEO 市場成熟嗎？',
         '仍在形成階段。相較於發展多年的 SEO 市場，AEO 的服務標準、驗收方式與定價模式都還沒有共識。這代表選擇廠商時更需要自己具備判斷力，不能只看包裝。'),
        ('為什麼這頁不列出其他公司？',
         '兩個原因。第一，沒有公開且可驗證的資料能支持公平的比較或排名。第二，在自家網站上評價競爭對手存在明顯的利益衝突。我們提供的是可自行驗證的評估準則，包括用來檢驗我們自己。'),
        ('找國外廠商可以嗎？',
         '技術面沒有障礙。需要考量的是中文內容的處理能力、對台灣市場查詢習慣的理解，以及時區與溝通成本。若你的目標客群主要在台灣，這些因素會影響內容策略的品質。'),
        ('怎麼確認廠商真的懂？',
         '最快的方式是問技術細節並當場驗證：用檢測工具測對方自己的網站、詢問 robots.txt 群組繼承規則、詢問 GPTBot 與 OAI-SearchBot 的差異。這些問題無法靠簡報回答。'),
    ],
    related=[('/aeo/how-to-choose-agency', '如何挑選 AEO 廠商'),
             ('/aeo/aeo-agency-vs-seo-agency', 'AEO 公司與 SEO 公司的差別'),
             (TOOLS, '台灣 AEO 工具比較'), (CHECKER, '免費檢測工具')],
))

PAGES.append(page(
    url='/aeo/how-to-choose-agency',
    title='如何挑選 AEO 廠商？該問的問題清單 - ShellFans',
    h1='如何挑選 AEO 廠商？',
    eyebrow='Buying Guide',
    desc='挑選 AEO 廠商時，技術問題比簡報更能區分優劣。本頁提供可當場驗證的問題清單、合約中該確認的條款，以及需要警覺的說法。',
    lede='挑 AEO 廠商最有效的方法不是比價，而是<strong>問幾個無法靠簡報回答的技術問題</strong>，並當場用免費工具檢測對方自己的網站。這個市場還新，包裝與實力的落差比成熟市場大得多，而技術細節是最難假裝的部分。',
    schema='TechArticle',
    sections=[
        sec('Questions', '當場可驗證的問題', [
            ('h3', '技術理解'),
            ('ol', [
                '<strong>「robots.txt 中特定 user-agent 群組會繼承 <code>User-agent: *</code> 的規則嗎？」</strong><br>'
                '正確答案是<strong>不會</strong>。答錯的廠商很可能會寫出誤擋爬蟲的設定。',
                '<strong>「GPTBot 和 OAI-SearchBot 差在哪？」</strong><br>'
                '前者收集訓練資料，後者建立 ChatGPT 搜尋索引。混為一談代表可能擋錯。見 %s。'
                % a('/aeo/gptbot-oai-searchbot', 'GPTBot 與 OAI-SearchBot'),
                '<strong>「擋掉 Google-Extended 會影響 AI Overviews 嗎？」</strong><br>'
                '不會——AI Overviews 走的是 Googlebot。這題能篩掉相當多只讀過二手資料的廠商。',
                '<strong>「robots.txt 寫了 Allow 但爬蟲還是拿不到，可能是什麼原因？」</strong><br>'
                '好的答案會提到 CDN／WAF 的 bot 規則、伺服器層攔截，而不是只說「再檢查一次設定」。',
            ]),
            ('h3', '交付與驗收'),
            ('ol', [
                '<strong>「交付物具體是什麼？」</strong>要能列出可驗收的項目，而非「AEO 優化」。',
                '<strong>「怎麼證明設定真的生效？」</strong>應該提到實際 user-agent 測試與 access log 佐證。',
                '<strong>「成效怎麼量測？量測條件怎麼固定？」</strong>沒有固定條件就沒有可比性。',
                '<strong>「內容改寫包不包含？範圍到哪裡？」</strong>這通常是最大的成本項目。',
                '<strong>「改版之後怎麼辦？」</strong>整備很容易被改版覆蓋，好的廠商會主動提到回歸驗證。',
            ]),
        ]),
        sec('Test', '最直接的一招', [
            ('note', '<strong>用免費工具檢測對方自己的網站。</strong>'
                     '一家做 AEO 的公司，自己的網站若缺少結構化資料、robots.txt 沒有 AI 爬蟲規則、'
                     '或內容結構混亂，那是很難解釋的。這一招花三十秒，比看一小時簡報有用。'),
            ('p', '可以直接用 %s。同樣的標準也適用於 ShellFans，歡迎檢測 shell.fans。' % a(CHECKER, 'AEO/GEO 免費檢測工具')),
        ]),
        sec('Contract', '合約中該確認的', [
            ('ul', [
                '<strong>驗收標準</strong>：以什麼為準判定完成。「提升 AI 能見度」不是可驗收的標準。',
                '<strong>量測條件</strong>：問題組、平台、頻率是否明確定義且不會中途變更。',
                '<strong>資料歸屬</strong>：量測產生的歷史資料在合約結束後是否可帶走。',
                '<strong>網站存取權限範圍</strong>：對方需要什麼權限、能改動哪些部分。',
                '<strong>持續維護的界線</strong>：哪些變更包含在月費內，哪些另計。',
            ]),
        ]),
        sec('Red flags', '需要警覺的說法', [
            ('ul', [
                '「保證被 ChatGPT／Perplexity 引用」——<strong>直接排除</strong>。沒有人能保證第三方平台行為。',
                '「我們是台灣第一」——要求提出可驗證的依據。',
                '「AI 引用率提升 N%」——要求說明量測方法、基準期、樣本數。',
                '「做完就不用管」——與 AEO 的實際運作方式不符。',
                '「用我們的工具就好」——要確認買到的是報告還是實際的整備工作。',
                '無法解釋自家網站分數為何偏低——這比任何答案都說明問題。',
            ]),
        ]),
    ],
    faq=[
        ('一定要找專門做 AEO 的公司嗎？',
         '不一定。既有的 SEO 代理商或網站開發商若具備 AI 爬蟲與結構化資料的實作能力，同樣做得好。關鍵是技術理解與驗收機制，不是公司的分類標籤。'),
        ('報價差很多，該選便宜的嗎？',
         '先確認範圍是否相同。價差通常來自交付項目不同——是否包含內容改寫、是否包含持續維護、是否包含量測。相同範圍下再比價才有意義。'),
        ('可以先小規模試做嗎？',
         '建議如此。先做技術整備（成本相對固定、效果可立即驗證），確認合作品質後再擴大到內容調整。這也讓你有機會驗證對方的驗收與溝通方式。'),
        ('自己做和委外怎麼選？',
         '技術整備若團隊有能力，自行完成是合理的——本站已公開具體做法。真正難自行處理的是持續量測與改版後的回歸驗證。可以先自行整備，再視需要委外處理持續維護的部分。'),
    ],
    related=[('/aeo/taiwan-companies', '台灣 AEO 服務商'),
             ('/aeo/aeo-agency-vs-seo-agency', 'AEO 公司與 SEO 公司的差別'),
             ('/aeo/cost', 'AEO 費用怎麼計算'), (CHECKER, '免費檢測工具')],
))

PAGES.append(page(
    url='/aeo/aeo-agency-vs-seo-agency',
    title='AEO 公司和 SEO 公司差在哪？該找誰 - ShellFans',
    h1='AEO 公司和 SEO 公司差在哪？',
    eyebrow='Comparison',
    desc='AEO 與 SEO 服務商的能力重疊但重心不同。本頁比較兩者的工作內容、量測方式與常見盲點，並說明什麼情況下該找誰。',
    lede='能力上兩者重疊超過一半——可爬取性、結構化資料、內容結構是共同基礎。差異在三個地方：<strong>AI 爬蟲的技術細節、內容的可擷取性、以及成效的量測方式</strong>。多數傳統 SEO 代理商在前兩項需要補課，在第三項則往往低估了難度。',
    schema='TechArticle',
    sections=[
        sec('Compare', '工作內容比較', [
            ('table', {
                'caption': 'AEO 服務商與 SEO 服務商的差異',
                'cols': ['項目', 'SEO 服務商', 'AEO 服務商'],
                'rows': [
                    ['共同基礎', '可爬取性、結構化資料、標題階層、行動裝置', '相同'],
                    ['爬蟲處理', '主要針對 Googlebot、Bingbot',
                     '額外處理 GPTBot、OAI-SearchBot、ClaudeBot、PerplexityBot 等，且需理解群組不繼承'],
                    ['內容重心', '關鍵字涵蓋、主題深度、內部連結', '段落自足性、定義先行、限制說明'],
                    ['量測', '排名、曝光、點擊率（有現成工具）',
                     '固定問題組的提及率與引用率（需自建觀測機制）'],
                    ['外部訊號', '外部連結建置', '跨來源的實體提及一致性'],
                    ['回饋速度', '較快，有公開的排名可查', '較慢，且需累積觀測點'],
                ],
            }),
        ]),
        sec('Blind spots', '各自的常見盲點', [
            ('h3', 'SEO 背景的常見盲點'),
            ('ul', [
                '<strong>把 AI 爬蟲當成一般爬蟲</strong>。沒有意識到 robots.txt 群組不繼承，或不知道訓練爬蟲與搜尋爬蟲要分開。',
                '<strong>沿用「內容越長越好」的習慣</strong>。長文對排名可能有利，但若重點藏在中段，對擷取不利。',
                '<strong>用排名代替 AEO 成效</strong>。排名上升不等於被 AI 引用，兩者需要分開量測。',
            ]),
            ('h3', '純技術背景的常見盲點'),
            ('ul', [
                '<strong>只做技術整備，忽略內容結構</strong>。八個面向中內容相關的佔了不小比重。',
                '<strong>不建立量測機制</strong>。設定做完就結案，無法回答「有沒有用」。',
                '<strong>低估回歸風險</strong>。沒有把改版後的重新驗證納入流程。',
            ]),
        ]),
        sec('Choose', '該找誰', [
            ('table', {
                'caption': '依需求選擇服務商類型',
                'cols': ['你的情況', '建議'],
                'rows': [
                    ['已有 SEO 廠商且合作良好', '先要求對方補齊 AI 爬蟲與內容結構的部分，用本站的問題清單驗證其理解程度'],
                    ['網站技術問題較多', '偏向能直接改動網站的服務商，技術整備與驗證是第一優先'],
                    ['內容量大且需重整', '內容能力比技術能力更關鍵，這部分是最大的成本項目'],
                    ['需要可驗收的量測', '確認對方能定義固定的量測條件，這是最容易被含糊帶過的部分'],
                ],
            }),
            ('p', '判斷對方能力的具體問題清單見 %s。' % a('/aeo/how-to-choose-agency', '如何挑選 AEO 廠商')),
        ]),
    ],
    faq=[
        ('現有的 SEO 廠商可以直接做 AEO 嗎？',
         '有機會，取決於他們對 AI 爬蟲與內容可擷取性的理解程度。建議用具體技術問題驗證：robots.txt 群組是否繼承、GPTBot 與 OAI-SearchBot 的差異、Google-Extended 是否影響 AI Overviews。這三題能相當有效地區分理解深度。'),
        ('要同時找兩家嗎？',
         '通常不必，而且容易產生權責不清。較實際的做法是選一家並明確定義 AEO 相關的交付項目與驗收標準。若既有 SEO 廠商無法補齊，再考慮更換或增加 AEO 的專項合作。'),
        ('AEO 服務會不會傷害既有的 SEO 成效？',
         '正常執行不會，因為技術基礎大量重疊且方向一致。需要留意的是內容改寫——若把原本排名良好的頁面大幅改動，可能影響既有表現。合理做法是先在次要頁面驗證，再處理主力頁面。'),
    ],
    related=[('/aeo/how-to-choose-agency', '如何挑選 AEO 廠商'),
             ('/aeo/taiwan-companies', '台灣 AEO 服務商'),
             ('/aeo/aeo-vs-seo', 'AEO 與 SEO 的差異'), (CHECKER, '免費檢測工具')],
))


# ---------------------------------------------------------------------------
# 第二批：補齊探測題的內容缺口
#
# 依 2026-08-16 的「探測題 × 內容涵蓋度」盤點，以下三題沒有任何頁面以其為標題。
# 標題直接對上問題，是被答案引擎擷取的前提之一 —— 內容散在別頁的段落裡，
# 模型要自己拼湊，命中率會低很多。
# ---------------------------------------------------------------------------

PAGES.append(page(
    url='/aeo/ai-crawler-monitoring',
    title='如何檢查網站的 AI 爬蟲來訪狀況？完整做法 - ShellFans',
    h1='如何檢查網站的 AI 爬蟲來訪狀況？',
    eyebrow='Technical',
    desc='要知道 GPTBot、ClaudeBot、PerplexityBot 有沒有來抓你的網站，可以查 access log、比對 user-agent、驗證 rDNS。本頁說明三種做法與各自的限制。',
    lede='最直接的方法是查伺服器的 access log，比對 user-agent 中的爬蟲名稱。但只看 user-agent 會被冒名的請求誤導——實測顯示相當比例自稱 GPTBot、PerplexityBot 的流量無法通過反向 DNS 驗證。因此可靠的做法需要兩層：先辨識自稱身分，再驗證它是否屬實。',
    schema='TechArticle',
    sections=[
        sec('Methods', '三種做法', [
            ('h3', '一、直接查 access log（成本最低）'),
            ('p', 'nginx、Apache 的 access log 已經記錄了每一次請求的 user-agent。'
                  '用 grep 過濾爬蟲名稱即可得到粗略的到訪次數。'),
            ('ul', [
                '<strong>優點</strong>：不需要任何額外建置，資料本來就在。',
                '<strong>限制</strong>：只看得到自稱身分，無法辨別冒名；log 通常會輪替，看不到長期趨勢；'
                '若網站在 CDN 之後，log 裡的來源 IP 是 CDN 邊緣節點而非真實爬蟲 IP。',
            ]),
            ('h3', '二、在 CDN 邊緣收集'),
            ('p', '若網站走 Cloudflare 這類 CDN，可以在邊緣層收集請求資訊。'
                  '好處是拿得到真實的 client IP，而那是驗證身分的必要條件。'),
            ('h3', '三、用工具持續監控'),
            ('p', 'ShellFans 的 %s 屬於這一類：在邊緣收集請求，記錄自稱身分與驗證結果，'
                  '並保留逐日趨勢。適合需要長期觀察、而不只是查一次的情況。'
                  % a(SERVICE, 'AEO Managed Hosting')),
        ]),
        sec('Verify', '為什麼必須驗證身分', [
            ('note', '<strong>自稱不等於身分。</strong>任何人都可以把 user-agent 設成 '
                     '<code>GPTBot</code>。實務上確實有相當比例自稱知名 AI 爬蟲的流量'
                     '無法通過驗證——把這些算成「AI 有來抓」，會讓你以為能見度不錯，'
                     '而實際上真正的爬蟲根本沒來。'),
            ('h3', '兩種驗證方式'),
            ('ol', [
                '<strong>反向 DNS（rDNS）</strong>：把來源 IP 反查主機名，確認它屬於該業者的網域'
                '（例如 OpenAI 的爬蟲應解析到 openai 的網域），再正查回去確認一致。這是最通用的做法。',
                '<strong>官方 IP 清單比對</strong>：部分業者公布爬蟲的 IP 範圍，直接比對即可。'
                '準確但需要定期更新清單。',
            ]),
            ('p', '兩者都做不到時，該筆請求只能標記為「未驗證」，不該當成已確認的到訪。'),
        ]),
        sec('What to look', '該看哪些指標', [
            ('p', '「來訪次數」單看沒有意義——爬蟲流量會因為新內容上線後的密集抓取、'
                  '以及抓完之後回到正常頻率而劇烈起伏。次數下降不等於能見度變差。'),
            ('table', {
                'caption': '比次數更有意義的指標',
                'cols': ['指標', '為什麼重要'],
                'rows': [
                    ['不重複 URL 數', '爬蟲是抓遍全站，還是只重複抓首頁'],
                    ['成功抓取率', '來了有沒有真的拿到內容，還是被擋掉或撞到 404'],
                    ['429 次數', '被速率限制或 WAF 擋下 —— 這是<strong>你這端</strong>的問題，最該優先處理'],
                    ['5xx 次數', '伺服器錯誤，爬蟲拿到的是錯誤頁'],
                    ['有幾家 AI 爬蟲來過', '涵蓋面比單一家的次數更能代表整體能見度'],
                ],
            }),
            ('p', '各面向的完整定義見 %s。' % a(METHOD, 'AI Readiness Score 方法論')),
        ]),
        sec('Pitfalls', '常見的判讀錯誤', [
            ('ul', [
                '<strong>拿今天的半天跟完整日比</strong>。今天還沒過完，數字必然偏低，'
                '看起來像暴跌。任何比較都應該只用已結束的完整日。',
                '<strong>把冒名流量算進來</strong>。見上一節。',
                '<strong>只看總量不看成功率</strong>。爬蟲來了一萬次但全部 404，等於沒來。',
                '<strong>用單日判斷趨勢</strong>。爬蟲流量的日間波動極大，至少要看 7 日移動平均。',
                '<strong>擋掉 Googlebot</strong>。Google AI Overviews 走的也是 Googlebot，'
                '擋掉會同時失去一般搜尋與 AI 摘要。詳見 %s。' % a('/aeo/ai-crawler', 'AI 爬蟲總覽'),
            ]),
        ]),
    ],
    faq=[
        ('看不到任何 AI 爬蟲來訪，是被擋住了嗎？',
         '先確認三件事：robots.txt 是否誤擋（特定 user-agent 群組不會繼承 <code>User-agent: *</code> 的規則）、CDN 或 WAF 是否在 robots.txt 之外另行攔截、以及網站是否夠新或內容太少而尚未被發現。前兩者可以用該 user-agent 實際送出請求測試，看回應是 200 還是 403。'),
        ('access log 裡的 IP 是 CDN 的，還能驗證嗎？',
         '不能。反向 DNS 驗證需要真實的 client IP，而 CDN 之後的 log 記錄的是邊緣節點位址。要驗證身分必須在 CDN 邊緣層收集，或使用 CDN 提供的真實 IP 標頭。'),
        ('爬蟲來訪次數下降代表 AEO 變差嗎？',
         '不一定，多數情況下不是。新內容上線後會有一波密集抓取，抓完之後回到正常頻率，次數自然下降——那是正常化不是衰退。判斷應該看成功抓取率、不重複 URL 數與涵蓋的爬蟲家數，並以 7 日移動平均觀察，而非單日次數。'),
        ('多久檢查一次比較合理？',
         '若只是確認設定有沒有生效，改動後查一次即可。若要觀察趨勢，需要持續收集——爬蟲行為的變化以週為單位才看得出來，臨時查一次的資料無法區分趨勢與雜訊。'),
    ],
    related=[('/aeo/ai-crawler', 'AI 爬蟲總覽'), ('/aeo/gptbot-oai-searchbot', 'GPTBot 與 OAI-SearchBot'),
             (SERVICE, 'AEO Managed Hosting'), (CHECKER, '免費檢測工具')],
    cta=CTA_CHECK, cta2=CTA_SERVICE,
))

PAGES.append(page(
    url='/aeo/how-ai-search-works',
    title='要怎麼讓 AI 搜尋引擎正確理解我的網站？ - ShellFans',
    h1='要怎麼讓 AI 搜尋引擎正確理解我的網站？',
    eyebrow='Guide',
    desc='讓 AI 正確理解網站需要三個條件：爬得到、看得懂、切得出可引用的段落。本頁把技術面的各項工作串成一條可執行的順序。',
    lede='要讓 AI 搜尋引擎正確理解你的網站，需要同時滿足三個條件：<strong>爬得到</strong>（爬蟲能存取）、<strong>看得懂</strong>（結構化資料與清楚的實體訊號）、<strong>切得出可引用的段落</strong>（內容形狀適合被擷取）。三者缺一，後面的努力都到不了使用者眼前。',
    schema='TechArticle',
    sections=[
        sec('Chain', '三個環節，順序不能顛倒', [
            ('p', '這三件事是串聯的。爬不到就談不上理解，理解不了就談不上引用。'
                  '因此投入順序應該照著這個鏈條走，而不是先做最容易看到成果的那一項。'),
            ('table', {
                'caption': '三個環節與對應的工作',
                'cols': ['環節', '要做什麼', '怎麼確認做到了'],
                'rows': [
                    ['① 爬得到',
                     'robots.txt 對各 AI 爬蟲的規則、伺服器回應狀態、sitemap、避免內容只在 JavaScript 執行後出現',
                     '以該 user-agent 實際請求，確認回應 200；查 access log 看真的有來'],
                    ['② 看得懂',
                     'Organization 結構化資料、品牌名稱一致、可驗證的公司資訊、清楚的標題階層',
                     '結構化資料可被解析；全站品牌寫法一致'],
                    ['③ 切得出段落',
                     '定義先行、段落自足、比較用表格、主動寫限制與不適用情境',
                     '把任一段落單獨抽出來看，是否仍然正確且完整'],
                ],
            }),
        ]),
        sec('Order', '建議的執行順序', [
            ('ol', [
                '<strong>先確認爬蟲進得來</strong>。成本最低但代價最高——擋錯一支爬蟲，'
                '後面所有內容工作都歸零。詳見 %s。' % a('/aeo/ai-crawler', 'AI 爬蟲總覽'),
                '<strong>補上 Organization 結構化資料</strong>。讓模型能確定「你是誰」，'
                '這是所有品牌相關回答的前提。詳見 %s。' % a('/aeo/entity-clarity', '實體清晰度'),
                '<strong>把最重要的幾頁改成定義先行</strong>。不必重寫全站，'
                '先處理商業價值最高的頁面。詳見 %s。' % a('/aeo/answer-readiness', '答覆整備度'),
                '<strong>為有問答內容的頁面加上 FAQPage</strong>。投報率最高的結構化資料類型。'
                '詳見 %s。' % a('/aeo/faq-schema', 'FAQ Schema'),
                '<strong>建立 llms.txt</strong>。成本極低，且撰寫過程會逼你想清楚網站結構。'
                '詳見 %s。' % a('/aeo/llms-txt', 'llms.txt'),
                '<strong>建立量測機制</strong>。沒有基準就無法判斷後續改動有沒有效。',
            ]),
        ]),
        sec('Common blockers', '最常見的三個卡點', [
            ('h3', '一、內容要等 JavaScript 執行才出現'),
            ('p', '爬蟲抓到的是初始 HTML。若核心內容是前端渲染後才注入，等於沒有內容。'
                  '這是單一最致命的問題，而且從瀏覽器完全看不出來——'
                  '要用 <code>curl</code> 取得原始 HTML 才會發現。'),
            ('h3', '二、robots.txt 寫了 Allow 但被 CDN 擋掉'),
            ('p', 'robots.txt 是意圖，CDN 或 WAF 的 bot 規則才是實際發生的事。'
                  '兩者不一致時，爬蟲拿到的是 403。應該用實際的 user-agent 送出請求驗證。'),
            ('h3', '三、品牌實體訊號散掉'),
            ('p', '品牌名稱在各處寫法不一、公司名與品牌名從未被連結、聯絡資訊只有表單——'
                  '這些會讓模型無法確定「你」是誰，於是不會在回答中主動提到你。'),
        ]),
        sec('Verify', '怎麼確認真的做到了', [
            ('ul', [
                '用 <code>curl</code> 取得原始 HTML，確認核心內容在裡面（不是空的 div）。',
                '以 GPTBot、OAI-SearchBot、ClaudeBot、PerplexityBot 的 user-agent 分別請求，確認回應 200。',
                '把結構化資料實際 parse 一次——JSON 少一個逗號整段就失效，而頁面外觀毫無異狀。',
                '把任一段落單獨抽出來讀，確認脫離上下文仍然成立。',
                '用 %s 做一次整體檢查，八個面向會直接指出缺口。' % a(CHECKER, 'AEO/GEO 免費檢測工具'),
            ]),
        ]),
    ],
    faq=[
        ('做完這些，AI 就會引用我的網站嗎？',
         '不保證。這些工作處理的是必要條件——讓 AI 能夠正確理解與引用你的內容。是否實際被引用，取決於各 AI 平台的演算法、資料來源策略，以及該主題領域是否已有更常被引用的來源。任何宣稱能保證 AI 引用的說法都不可信。'),
        ('要先做哪一項？',
         '先確認爬蟲進得來。這一項成本最低但代價最高——擋錯一支爬蟲，後面所有內容工作都到不了使用者眼前。確認方式是用該 user-agent 實際送出請求，看回應是 200 還是 403。'),
        ('網站是用 React／Vue 做的，會有問題嗎？',
         '取決於是否有伺服器端渲染。若核心內容只在瀏覽器執行 JavaScript 後才出現，爬蟲抓到的是空殼。用 curl 取得原始 HTML 檢查即可確認。多數現代框架都支援 SSR 或靜態產生，改用即可解決。'),
        ('多久會看到效果？',
         '技術面的改動可以立即驗證（爬蟲能否存取、結構化資料能否解析），但 AI 回答中的變化需要更長時間，且需累積足夠觀測才能區分趨勢與隨機波動。沒有可保證的天數。'),
    ],
    related=[('/aeo/ai-crawler', 'AI 爬蟲總覽'), ('/aeo/entity-clarity', '實體清晰度'),
             ('/aeo/answer-readiness', '答覆整備度'), (CHECKER, '免費檢測工具')],
))

PAGES.append(page(
    url='/aeo/do-i-need-aeo',
    title='公司網站需要做 AEO 嗎？判斷準則 - ShellFans',
    h1='公司網站需要做 AEO 嗎？',
    eyebrow='Decision',
    desc='不是每個網站都值得投入 AEO。本頁提供四個可自行驗證的判斷準則，以及明確不適用的情況。',
    lede='判斷準則只有一個：<strong>你的客戶會不會用 AI 問到你的產品類別</strong>。如果會，AEO 值得做；如果你的生意來自既有客戶轉介、實體通路或指名採購，投入的優先度就低很多。頁數多寡、公司規模都不是判斷依據。',
    schema='TechArticle',
    sections=[
        sec('Criteria', '四個判斷準則', [
            ('ol', [
                '<strong>客戶會不會用 AI 查你的產品類別？</strong>最直接的驗證方式：'
                '把你認為客戶會問的問題，實際去 ChatGPT、Perplexity 問一次，看回答裡有沒有你、有沒有同業。'
                '如果連同業都沒有，代表這個類別目前不是 AI 的強項，優先度可以往後排。',
                '<strong>你的採購決策是否有「先研究再詢價」的階段？</strong>'
                'B2B 服務、專業服務、高單價商品通常有；便利品通常沒有。',
                '<strong>網站是不是主要的獲客管道？</strong>'
                '如果生意主要來自轉介或既有客戶，網站的角色是「查證」而非「發現」，'
                'AEO 的價值會集中在品牌認知型的問題上。',
                '<strong>內容能不能持續更新？</strong>'
                'AEO 的整備會因改版與內容變更而失效。若完全沒有維護能量，'
                '做一次性整備即可，不必投入長期方案。',
            ]),
        ]),
        sec('Not for you', '明確不適用的情況', [
            ('p', '把這些先講清楚，比列一堆好處有用：'),
            ('ul', [
                '<strong>內容以會員制為主</strong>。不對外公開的內容，AI 爬蟲本來就抓不到。',
                '<strong>純實體通路、網站只放地址電話</strong>。這種情況做好 Organization 結構化資料'
                '與正確的聯絡資訊即可，不需要完整的 AEO 方案。',
                '<strong>期待短期見效</strong>。技術整備可以快，但 AI 回答中的變化需要時間累積，'
                '且無法保證。若目標是本季業績，這不是對的工具。',
                '<strong>產品資訊高度變動</strong>。若價格、規格每週都變，'
                'AI 引用到的很可能是過期資訊，反而造成困擾。',
                '<strong>沒有人能回答客戶後續詢問</strong>。被 AI 引用會帶來詢問，'
                '沒有接應的人反而傷害品牌。',
            ]),
        ]),
        sec('Minimum', '如果只做最低限度', [
            ('p', '判斷後決定不投入完整方案，仍建議做這三件成本極低的事：'),
            ('ol', [
                '<strong>確認沒有誤擋 AI 爬蟲</strong>。改一個檔案，但擋錯的代價是完全消失。'
                '詳見 %s。' % a('/aeo/ai-crawler', 'AI 爬蟲總覽'),
                '<strong>補上 Organization 結構化資料</strong>，含公司全名、統編、地址、聯絡方式。'
                '讓 AI 至少能正確描述你是誰。詳見 %s。' % a('/aeo/entity-clarity', '實體清晰度'),
                '<strong>確認首頁的核心內容不需要 JavaScript 才出現</strong>。'
                '用 <code>curl</code> 看原始 HTML 即可確認。',
            ]),
            ('p', '這三件事加起來通常一天內可以完成，且不需要持續維護。'),
        ]),
        sec('Check', '先量測再決定', [
            ('p', '在決定投入程度之前，先知道自己的起點。'
                  '%s 會就八個面向給出 0–100 分並列出具體待修項目，免費、不需註冊。'
                  % a(CHECKER, 'AEO/GEO 檢測工具')),
            ('p', '若分數已經不低，代表基礎大致齊備，剩下的是內容工作；'
                  '若分數偏低且缺的都是技術項目，那部分成本固定且效果可立即驗證，'
                  '通常是最值得先做的部分。'),
        ]),
    ],
    faq=[
        ('小公司值得做嗎？',
         '規模不是判斷依據，客戶行為才是。十頁把主題講清楚的網站，比一百頁模糊內容的網站更容易被正確引用。真正的判準是：你的客戶會不會用 AI 查你的產品類別。'),
        ('已經做了 SEO，還需要做 AEO 嗎？',
         '已經完成了相當部分——可爬取性、結構化資料、標題階層都是共用基礎。通常缺的是三塊：AI 爬蟲的 robots.txt 規則、內容的段落自足性、品牌實體的一致性。可以先檢測看缺口大小再決定。'),
        ('怎麼知道客戶有沒有在用 AI 查？',
         '最直接的方式是自己去問一次。把你認為客戶會問的問題實際輸入 ChatGPT 或 Perplexity，看回答的品質與是否列出同業。若回答具體且列出了同業，代表這個類別已經有 AI 流量；若回答含糊或找不到來源，代表還早。'),
        ('決定不做會怎樣？',
         '短期通常沒有立即影響。風險在於：當客戶開始習慣用 AI 查詢時，你的同業若已被納入回答，你會在使用者的候選名單之外，而且不會有任何訊號告訴你這件事正在發生。建議至少做最低限度的三件事，成本很低。'),
    ],
    related=[('/aeo/what-is-aeo', 'AEO 是什麼'), ('/aeo/cost', 'AEO 費用怎麼計算'),
             ('/aeo/implementation', 'AEO 導入流程'), (CHECKER, '免費檢測工具')],
    cta=CTA_CHECK, cta2={'href': '/aeo/cost', 'label': '了解費用如何形成'},
))
