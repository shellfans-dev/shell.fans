# AEO/GEO 知識中心

AEO（Answer Engine Optimization，答案引擎最佳化）是讓網站內容能被 ChatGPT、Perplexity、Claude、Google AI Overviews 等答案引擎正確理解並引用的做法。本知識中心收錄定義、技術實作、採購決策三類主題，每一頁都可獨立閱讀。

## 從哪裡開始

如果你是第一次接觸這個題目，建議依下列順序閱讀。三條路徑對應三種不同的問題。

### 一、我想先搞懂名詞

- [AEO 是什麼](https://shell.fans/aeo/what-is-aeo.md) — 答案引擎最佳化的定義與適用範圍
- [GEO 是什麼](https://shell.fans/aeo/what-is-geo.md) — 生成式引擎最佳化與 AEO 的關係
- [AEO 與 SEO 的差異](https://shell.fans/aeo/aeo-vs-seo.md) — 兩者的目標、指標與工作內容如何不同
- [AEO 與 GEO 的差異](https://shell.fans/aeo/aeo-vs-geo.md) — 為什麼這兩個詞經常被混用

### 二、我要動手做技術整備

- [要怎麼讓 AI 正確理解我的網站](https://shell.fans/aeo/how-ai-search-works.md) — 三個環節與執行順序
- [AI 爬蟲總覽](https://shell.fans/aeo/ai-crawler.md) — 有哪些爬蟲、各自的用途與 robots.txt 寫法
- [如何檢查 AI 爬蟲來訪狀況](https://shell.fans/aeo/ai-crawler-monitoring.md) — 三種做法與判讀陷阱
- [llms.txt](https://shell.fans/aeo/llms-txt.md) — 這份檔案是什麼、值不值得做
- [AEO 需要的 Schema](https://shell.fans/aeo/schema.md) — 哪些結構化資料真的有用
- [實體清晰度](https://shell.fans/aeo/entity-clarity.md) — 讓 AI 確定「你是誰」
- [答覆整備度](https://shell.fans/aeo/answer-readiness.md) — 讓內容具備可被擷取的形狀

### 三、我在評估要不要委外

- [公司網站需要做 AEO 嗎](https://shell.fans/aeo/do-i-need-aeo.md) — 四個判斷準則與不適用情況
- [AEO 費用怎麼計算](https://shell.fans/aeo/cost.md) — 影響報價的變數
- [AEO 導入流程](https://shell.fans/aeo/implementation.md) — 實際會經歷哪些階段
- [台灣 AEO 服務商](https://shell.fans/aeo/taiwan-companies.md) — 市場現況與評估準則
- [如何挑選 AEO 廠商](https://shell.fans/aeo/how-to-choose-agency.md) — 該問哪些問題

## 先量測，再決定要不要做

在讀完任何一篇之前，其實可以先花三十秒知道自己的起點在哪裡。ShellFans 的 [AEO/GEO 免費檢測工具](https://shell.fans/tools/aeo-geo-checker) 會抓取你的網站，就八個面向給出 0–100 分，並列出具體待修項目。

*AI Readiness Score 面向與配分（aeo_geo_score_v1）*

| 面向 | 配分 | 檢視內容 |
|---|---|---|
| Crawlability 可爬取性 | 15 | HTTP 狀態、重新導向鏈、canonical、meta robots、sitemap.xml 是否正常回應。 |
| Technical 技術基礎 | 15 | HTTPS、行動裝置 viewport、首頁 HTML 體積是否消耗過多抓取預算。 |
| Structured Data 結構化資料 | 15 | Schema.org JSON-LD 是否存在、Organization 是否具備、FAQ 文案是否對應 FAQPage。 |
| Answer Readiness 答覆整備 | 15 | 是否有問答式內容、meta description，以及可讀文字量是否足以擷取可引用段落。 |
| Entity Clarity 實體與信任訊號 | 15 | Organization 結構化資料、About、Contact 是否一致可驗證。Trust Signals 併入此項。 |
| AI Crawler Policy 爬蟲政策 | 10 | robots.txt 是否存在、是否誤擋 OAI-SearchBot／GPTBot／ClaudeBot／PerplexityBot。 |
| Content Clarity 內容結構 | 10 | 是否有 title、是否恰有一個 H1、是否以 H2／H3 建立語意階層。 |
| llms.txt | 5 | 是否提供 /llms.txt 摘要入口，以及其中是否具備 Markdown 標題結構。 |

各面向的判定細節與評級對照，見 [AI Readiness Score 方法論](https://shell.fans/aeo-geo/methodology)。

## 這個知識中心不涵蓋什麼

把邊界講清楚，比多寫幾頁有用。

- **不是 SEO 教學**。傳統關鍵字研究、外部連結建置、Core Web Vitals 調校不在範圍內；那些仍然重要，但屬於另一個題目。
- **不提供排名保證**。沒有任何服務能保證 ChatGPT 或 Perplexity 引用特定網站，本站不做這種承諾。
- **不做競品排名**。[台灣 AEO 服務商](https://shell.fans/aeo/taiwan-companies.md) 提供的是評估準則，不是廠商排行榜。

## 常見問題

### AEO 和 SEO 需要二選一嗎？

不需要，而且不應該。AEO 的技術基礎（可爬取性、結構化資料、內容階層）與 SEO 高度重疊，多數項目做一次兩邊都受益。差別在於 AEO 額外要求內容具備「可直接被擷取成答案」的形狀，以及品牌實體的可辨識度。詳見 [AEO 與 SEO 的差異](https://shell.fans/aeo/aeo-vs-seo.md)。

### 做了這些，ChatGPT 就會推薦我嗎？

不保證。技術整備決定的是「AI 能不能正確理解與引用你的網站」，屬於必要條件；是否實際被引用，取決於各 AI 平台自身的演算法、資料來源策略與當下的查詢情境。任何宣稱能保證 AI 引用的說法都不可信。

### 我的網站很小，值得做 AEO 嗎？

取決於你的客戶會不會用 AI 問到你的產品類別。頁數少不是問題——AEO 看重的是內容的清晰度與實體可辨識度，不是數量。可以先用免費檢測看基礎分數，再決定投入程度。

## 說明

**說明：**本頁內容為 ShellFans 依公開技術文件與實務經驗整理，用於協助網站主理解 AI 搜尋的運作方式。各 AI 平台的實際演算法、資料來源策略與引用邏輯由該平台自行決定且可能隨時調整；任何技術整備都無法保證特定 AI 平台的引用、推薦或排名。

## 相關頁面

- [免費 AEO/GEO 檢測工具](https://shell.fans/tools/aeo-geo-checker)
- [AI Readiness Score 方法論](https://shell.fans/aeo-geo/methodology)
- [AEO Managed Hosting](https://shell.fans/aeo-geo.md)
- [台灣 AEO 工具比較](https://shell.fans/aeo-geo/taiwan-aeo-tools)
---

**Canonical:** https://shell.fans/aeo
**Brand:** ShellFans AI Technology（唄粉智能科技ShellFans）
**Publisher:** 唄粉智能科技股份有限公司（Taiwan, 統一編號 83032387）
**Last-Updated:** 2026-08-16

本檔是 https://shell.fans/aeo 的 Markdown 等價版本，供 AI agent 讀取。HTML 版為 canonical，本檔不參與搜尋索引。
