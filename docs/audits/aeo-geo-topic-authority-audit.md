# ShellFans AEO/GEO Topic Authority / Entity / Content Cluster Audit

日期：2026-08-21
範圍：shell.fans 靜態站（44 頁）+ saas_womm（AI Visibility、crawler monitoring、admin、portal）
性質：**唯讀稽核，未修改任何程式**

---

## 1. Executive Summary

### 直接回答最重要的問題

**ShellFans 缺的不是內容量，是三件內容以外的東西。**

Topic Architecture 已經建好了：30 個 AEO/GEO 頁面、完整 pillar-cluster 結構、
零 orphan、Schema 覆蓋 100%、15 支 AI 爬蟲全部可存取。
Cluster A（基礎認知）與 Cluster B（服務推薦）**覆蓋率已達 80% 以上**。

真正缺的是：

| 缺口 | 性質 |
|---|---|
| **Cluster C 的量測面內容** | 我們有 AI Visibility 產品，卻**沒有一頁在談它** |
| **Case Study** | 零。網站、資料模型、CMS 全無 |
| **第三方 citation 管理** | 零。沒有任何資料模型 |
| **AI referral 追蹤** | 零。全 repo 找不到 `chatgpt.com`／`claude.ai`／`gemini.google.com` |

### 三個 0% 的 Root Cause（依證據強度）

1. **語意歧義** —— AI 把「AEO」理解成 Authorized Economic Operator。已於 08-15 修正題目，**尚未重新探測驗證**。
2. **首頁沒有自我定位** —— 爬蟲 39% 的請求落在首頁，而首頁在 08-19 前完全沒提 AEO/GEO。已修，**尚未重新探測驗證**。
3. **無第三方佐證** —— 競品被 AI 描述為「有實績案例支撐」，我們沒有任何可公開案例。**未解，且無法用工程解決。**

### 明確不建議大量生文

理由見第 18 節。簡言之：**內容不是瓶頸，而且 08-12 之後的三批改動都還沒被量測過。**
在沒有新基準線的情況下再加內容，等於用更多變數去猜一個還沒觀測的結果。

---

## 2. Current Architecture

### 2.1 URL / Route Map

#### shell.fans 靜態站（44 頁，全部在 sitemap）

**AEO/GEO Pillar**

| URL | 角色 | Schema |
|---|---|---|
| `/aeo-geo` | 商業 pillar（BOFU） | WebApplication, Service, Organization, FAQPage, BreadcrumbList |
| `/aeo` | 知識 hub（TOFU–MOFU） | Organization, CollectionPage, BreadcrumbList, FAQPage |

**Cluster（26 頁，`/aeo/*`）**

定義比較（4）：`what-is-aeo`、`what-is-geo`、`aeo-vs-seo`、`aeo-vs-geo`
技術（12）：`ai-crawler`、`ai-crawler-monitoring`、`gptbot-oai-searchbot`、`claudebot`、`perplexitybot`、`llms-txt`、`llms-full-txt`、`schema`、`faq-schema`、`entity-clarity`、`answer-readiness`、`trust-signals`、`how-ai-search-works`
商業採購（8）：`managed-hosting`、`consulting`、`cost`、`implementation`、`taiwan-companies`、`how-to-choose-agency`、`aeo-agency-vs-seo-agency`、`do-i-need-aeo`

**既有 AEO 頁（4）**：`/aeo-geo/methodology`、`/aeo-geo/taiwan-aeo-tools`、`/tools/aeo-geo-checker`、`/what-is-shellfans`

**其餘 12 頁**：首頁、product、pricing、price、endurance、fans-analysis、social-media-backup、support、helpcenter、contact、co-founder、privacy/terms

#### saas_womm 後台與 API

| 功能 | Route |
|---|---|
| AEO/GEO 後台（含成長趨勢 tab） | `/_shellfans-admin712/aeo-geo` |
| AEO 業務 CRM | `/_shellfans-admin712/aeo-sales` |
| 系統監控（爬蟲監控 tab） | `/_shellfans-admin712/system-monitor` |
| 趨勢 API | `GET /api/admin/site-monitoring/trend` |
| 報告 PDF | `GET /api/admin/site-monitoring/report` |
| 免費檢測（公開） | `POST /api/site/aeo-geo/scan` |
| AI 能見度探測 cron | `POST /api/internal/cron/visibility-probe`（每週一 09:00） |
| 客戶入口 | `cs.shell.fans/portal`、`GET /api/portal/aeo` |

#### 資料模型

| 表 | 用途 |
|---|---|
| `ai_visibility_questions` | 探測題（site-scoped） |
| `ai_visibility_runs` | 每次探測 |
| `ai_visibility_results` | 逐題逐平台結果 |
| `ai_visibility_categories` | 逐站台分類 taxonomy（2026-08-15 新增） |
| `crawler_access_logs` | 爬蟲逐筆記錄 |
| `crawler_block_rules` / `crawler_verification_cache` | 防護與驗證 |
| `aeo_geo_scans` | 免費檢測結果 |
| `aeo_milestones` | 工程里程碑 |
| `monitored_sites` | 站台 + brand_entity + domains |
| `aeo_leads` / `aeo_conversations` / … | 業務 CRM |

---

## 3. Existing Topic Inventory

### Cluster A：基礎認知型

| Topic | 狀態 | 頁面 |
|---|---|---|
| AEO 是什麼 | ✅ 專頁 | `/aeo/what-is-aeo` |
| GEO 是什麼 | ✅ 專頁 | `/aeo/what-is-geo` |
| SEO vs AEO vs GEO | 🟡 **部分** | 有 `aeo-vs-seo`、`aeo-vs-geo`，**缺 geo-vs-seo 與三方合併比較** |
| AI Chat 如何產生答案 | 🟡 | `/aeo/how-ai-search-works` 的「三個環節」段落，非專頁 |
| AI Search 與傳統 Search 差異 | ✅ | `/aeo/aeo-vs-seo` 的逐項比較表 |
| Entity 是什麼 | ✅ 專頁 | `/aeo/entity-clarity` |
| AI 為什麼引用某些網站 | ✅ | `/aeo/what-is-aeo` 的「三個環節」+ `/aeo/answer-readiness` |
| 品牌如何進入 AI 答案 | ✅ | `/aeo/how-ai-search-works` |

**Cluster A 覆蓋率：6.5 / 8 ≈ 81%**

### Cluster B：服務推薦與比較型

| Topic | 狀態 | 頁面 |
|---|---|---|
| 台灣有哪些 AEO/GEO 服務 | ✅ 專頁 | `/aeo/taiwan-companies` |
| 如何選擇 AEO/GEO 公司 | ✅ 專頁 | `/aeo/how-to-choose-agency` |
| 服務包含哪些項目 | ✅ 專頁 | `/aeo/managed-hosting` |
| 適合哪些企業 | ✅ 專頁 | `/aeo/do-i-need-aeo` |
| 如何計價 | ✅ 專頁 | `/aeo/cost` |
| 專案如何驗收 | 🟡 **部分** | `/aeo/how-to-choose-agency` 有「合約中該確認的」段落，**無專頁** |
| ShellFans 提供什麼 | ✅ | `/aeo-geo` + `/what-is-shellfans`（08-19 已補對等 H2 區塊） |
| 與其他方案差異 | 🟡 | `/aeo/aeo-agency-vs-seo-agency` 是類型比較，**非 ShellFans vs 競品** |
| Before / After | ❌ **完全缺** | — |
| Case Study | ❌ **完全缺** | — |

**Cluster B 覆蓋率：6.5 / 10 = 65%**

### Cluster C：技術與檢測型

| Topic | 狀態 | 頁面 |
|---|---|---|
| robots.txt | ✅ | `/aeo/ai-crawler` |
| sitemap | 🟡 | 散在多頁，無專頁（影響小） |
| llms.txt | ✅ 專頁 | `/aeo/llms-txt` + `/aeo/llms-full-txt` |
| Schema / JSON-LD | ✅ 專頁 | `/aeo/schema` |
| FAQ structured data | ✅ 專頁 | `/aeo/faq-schema` |
| Organization structured data | 🟡 | `/aeo/schema` 內一段，**無專頁** |
| Article structured data | ❌ | — |
| AI crawler | ✅ 專頁 ×4 | `ai-crawler`、`gptbot-oai-searchbot`、`claudebot`、`perplexitybot` |
| AI crawler 到站紀錄 | ✅ 專頁 | `/aeo/ai-crawler-monitoring`（08-16 新增） |
| Entity signals | ✅ 專頁 | `/aeo/entity-clarity` |
| **AI Visibility 如何檢測** | ❌ **完全缺** | — |
| **如何知道 ChatGPT 是否知道品牌** | ❌ **完全缺** | — |
| **如何知道 AI 是否引用官網** | ❌ **完全缺** | — |
| **Citation signals** | ❌ **完全缺** | — |
| **Brand Mention** | ❌ **完全缺** | — |
| **Source Citation** | ❌ **完全缺** | — |
| **AI Referral Traffic / Attribution** | ❌ **完全缺** | — |

**Cluster C 覆蓋率：10 / 17 ≈ 59%**

> **這是最重要的發現。** 缺的七項全部集中在「**量測**」這一面 ——
> 而 ShellFans 的產品核心正是量測（AI Readiness Score、能見度探測、爬蟲監控、歸因落差）。
> 我們做了這個產品，卻沒有一頁在談它。

---

## 4. Topic Coverage Matrix

| Topic | Existing Page | Content Quality | AI Intent Coverage | Entity | Internal Links | Schema | External Citation | AI Mention | Official Citation | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| What is AEO | ✅ `/aeo/what-is-aeo` | Good（2.3k 字 + 4 FAQ + 誤解章節） | Informational | ✅ | in 6 / out 12 | Org+TechArticle+BC+FAQ | ❌ | 0% | 0% | 🟢 內容就緒 |
| What is GEO | ✅ `/aeo/what-is-geo` | Good | Informational | ✅ | in 5 / out 7 | 同上 | ❌ | 0% | 0% | 🟢 |
| SEO vs AEO vs GEO | 🟡 拆成兩頁 | Good | Comparison | ✅ | in 4+3 | 同上 | ❌ | 0% | 0% | 🟡 缺三方合併頁 |
| AEO/GEO service | ✅ `/aeo-geo` + `/aeo/managed-hosting` | Good | Commercial | ✅ | in 28 / 6 | Service+WebApp+FAQ | ❌ | 0% | 0% | 🟢 |
| AEO/GEO recommendation | ✅ `/aeo/taiwan-companies` | **Weak for intent** | Recommendation | ✅ | in 3 / out 9 | 同上 | ❌ | 0% | 0% | 🔴 標題對上但刻意不列名單 |
| AI Visibility 檢測 | ❌ | — | Technical | — | — | — | ❌ | 0% | 0% | 🔴 **完全缺** |
| AI crawler | ✅ ×5 頁 | Good | Technical | ✅ | in 13 / out 7 | 同上 | ❌ | 0% | 0% | 🟢 |
| AI citation 監測 | ❌ | — | Technical | — | — | — | ❌ | 0% | 0% | 🔴 **完全缺** |
| Case Study | ❌ | — | Commercial / Trust | — | — | — | ❌ | 0% | 0% | 🔴 **完全缺** |
| Before / After | ❌ | — | Trust | — | — | — | ❌ | 0% | 0% | 🔴 **完全缺** |
| 驗收方式 | 🟡 段落 | OK | Commercial | ✅ | — | — | ❌ | 0% | 0% | 🟡 |
| ShellFans vs 競品 | ❌ | — | Comparison | — | — | — | ❌ | 0% | 0% | 🔴 缺（見第 16 節警告） |

---

## 5. Entity Audit

### 5.1 名稱一致性 ✅（2026-08-19 已統一）

全站 41 個 Organization 宣告 **收斂為單一形態**：

```json
{ "@id": "https://shell.fans/#organization",
  "name": "ShellFans AI Technology",
  "legalName": "唄粉智能科技股份有限公司",
  "alternateName": ["ShellFans","ShellFans AI","唄粉智能科技股份有限公司","唄粉智能科技","shell.fans"],
  "taxID": "83032387" }
```

稽核前曾有三種形態（29 頁用法人中文名、11 頁用品牌名、1 頁無 `@id`）。
**日文法人**（シェルファンズ株式会社）已在創辦人頁明確標示為**另一個法人**，
由同一人分別擔任台灣負責人與日本代表取締役 —— 關係清楚，無矛盾。

### 5.2 服務 Entity 陳述

| 目標陳述 | 是否明確 | 依據 |
|---|---|---|
| ShellFans offers AEO services | ✅ | `Organization.makesOffer` + `Service` schema + 首頁 title/description |
| ShellFans offers GEO services | ✅ | 同上（服務名為「AEO/GEO 代管」） |
| ShellFans provides AI visibility analysis | 🟡 **僅暗示** | `/aeo-geo` 文案提到「定期量測能見度」，但**無 Service schema 節點、無專頁** |
| ShellFans provides AI citation monitoring | 🟡 **僅暗示** | 同上 |
| ShellFans provides brand entity optimization | 🟡 **僅暗示** | `/aeo/entity-clarity` 是知識頁，非服務宣告 |
| ShellFans provides digital asset management | ✅ | 續航引擎 Service schema |

> **三項「僅暗示」是實質缺口。** 網站有內容講「實體清晰度是什麼」，
> 但沒有一處明確陳述「ShellFans 提供實體優化服務」。
> AI 無法從知識文章推導出服務關係。

### 5.3 Schema 進階欄位覆蓋

| 欄位 | 頁數 / 44 | 評估 |
|---|---|---|
| `sameAs` | 41 | ✅ |
| `areaServed` | 6 | 🟡 只有 Service 節點有 |
| `serviceType` | 6 | 🟡 同上 |
| `contactPoint` | 2 | 🔴 **幾乎沒用** —— 聯絡資訊只在頁尾純文字 |
| `knowsAbout` | **1** | 🔴 **幾乎沒用** —— 這正是宣告「我們懂 AEO/GEO」的欄位 |
| `makesOffer` | 1 | 🟡 只在首頁 |
| `Person` | **0** | 🔴 有創辦人頁卻**完全沒有 Person schema** |
| `Article` / `BlogPosting` | 1 / 0 | 🟡 26 個知識頁用 `TechArticle`，合理但缺 `datePublished` |

---

## 6. Structured Data Audit

| 檢查 | 結果 |
|---|---|
| 出現在 SSR HTML | ✅ 靜態站無 client render，全部在原始 HTML |
| 44 頁 JSON-LD 可解析 | ✅ 0 錯誤 |
| Schema 與頁面內容一致 | ✅ FAQPage 的問答與 `<details>` 逐條對應 |
| 空資料 | ✅ 未發現 |
| 錯誤 URL | ✅ sitemap 44 條全部 200 |
| canonical 一致 | ✅ 各頁指向自身，www → apex |
| Organization name 統一 | ✅ 41 頁單一形態 |
| logo | ✅ `nav_logo.svg` |
| sameAs 有官方社群 | ✅ FB / IG / console / blog |
| Service 清楚描述 AEO/GEO | 🟡 有 `serviceType: "AEO Managed Hosting"`，但**未涵蓋量測服務** |
| **缺 `datePublished` / `dateModified`** | 🔴 26 個 TechArticle 全部沒有 —— AI 無法判斷內容新鮮度 |

---

## 7. Internal Linking Audit

### 7.1 連結圖（32 個 AEO 相關頁面）

```
                      /aeo-geo (in 28) ◄──── pillar，被引用最多
                          ▲
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
/aeo (in 12, out 20)  /tools/aeo-geo-checker  /aeo-geo/methodology
  hub                     (in 31) ◄── 全站最高      (in 16)
    │
    ├── 26 個 cluster 頁（in 1–13，out 5–12）
    └── 每頁皆有 related links 回連 hub 或同群頁面
```

### 7.2 檢查結果

| 檢查項 | 結果 |
|---|---|
| orphan page | ✅ **0** —— 唯一 in=0 的是首頁本身（正常，首頁不需被子頁指向） |
| 無 outbound contextual link | ✅ 0 |
| anchor text 語意 | ✅ 每頁不同錨文字，無「了解更多」 |
| cluster 頁回連 pillar | 🟡 **3 頁未回連** —— `/aeo/consulting`、`/aeo/cost`、`/aeo/do-i-need-aeo` |
| Case Study → Service | ❌ N/A（無 Case Study） |
| Service → Case Study | ❌ N/A |
| FAQ → 延伸內容 | ✅ FAQ 答案內含內部連結 |

### 7.3 連結最弱的頁面（inbound = 1）

`/aeo/ai-crawler-monitoring`、`/aeo/do-i-need-aeo`、`/aeo/how-ai-search-works`、`/aeo/llms-full-txt`

前三者是 08-16 才新增，尚未被既有頁面充分引用。

---

## 8. FAQ Audit

全站 **151 條** FAQ 問句（`<summary>`），30/44 頁有 FAQPage schema。

| 目標問題 | 判定 | 依據 |
|---|---|---|
| 什麼是 AEO？ | ✅ 直接答案 | `/aeo/what-is-aeo` 導言 |
| 什麼是 GEO？ | ✅ | `/aeo/what-is-geo` |
| AEO 和 SEO 差別？ | ✅ | `/aeo/aeo-vs-seo` 逐項比較表 |
| GEO 和 SEO 差別？ | 🟡 **模糊** | 需從 `aeo-vs-geo` + `aeo-vs-seo` 自行推導 |
| AEO 和 GEO 差別？ | ✅ | `/aeo/aeo-vs-geo` |
| ShellFans 是什麼？ | ✅ | `/what-is-shellfans` + 首頁 FAQ |
| ShellFans 有提供 AEO/GEO 嗎？ | ✅ | 首頁 FAQ + `/aeo-geo` |
| ShellFans AEO/GEO 做什麼？ | ✅ | `/aeo/managed-hosting` 交付清單 |
| 哪些企業適合 AEO/GEO？ | ✅ | `/aeo/do-i-need-aeo` 四準則 + 不適用清單 |
| AEO/GEO 如何驗收？ | 🟡 **模糊** | `/aeo/how-to-choose-agency` 有段落，無直接標題 |
| **如何知道 ChatGPT 有沒有提到我的品牌？** | ❌ **完全沒有** | — |
| **如何知道 AI 有沒有引用我的官網？** | ❌ **完全沒有** | — |
| 如何增加 AI crawler 到訪？ | 🟡 **模糊** | `/aeo/ai-crawler` 講「怎麼設定不被擋」，非「怎麼增加」 |
| 如何提升 AI 品牌能見度？ | 🟡 | `/aeo/how-ai-search-works` 接近但標題不同 |
| 台灣有哪些 AEO/GEO 服務商？ | ✅ 標題匹配 | `/aeo/taiwan-companies`（但刻意不列名單） |

**直接答案 8 / 模糊 5 / 完全沒有 2。**

---

## 9. AI Question Set Audit

### 9.1 實際欄位 vs 需求概念

`ai_visibility_questions` 只有 **8 個欄位**：

```
id  siteId  category  question  unbranded  sortOrder  enabled  createdAt
```

| 需求概念 | 現況 |
|---|---|
| topic | ✅ `category`（2026-08-15 起 site-scoped） |
| question | ✅ |
| brand | 🟡 由 `unbranded` boolean 間接表達 |
| **intent** | ❌ **完全沒有** |
| **question_type** | ❌ 沒有（`category` 是主題不是意圖） |
| industry / target_audience / region / product / competitor | ❌ 全無 |
| priority | ❌ 只有 `sortOrder`（顯示順序，非優先度） |
| platform | 🟡 在 `runs.platforms`，非題目層 |
| baseline_result / latest_result | 🟡 由 `results` 逐次推導，非欄位 |
| brand_mentioned / official_site_cited | ✅ `results.brandMentioned` / `officialCited` |
| citation_url | ✅ `results.citations` (jsonb) |
| checked_at | ✅ `runs.startedAt` |
| **competitor_mentioned** | ❌ **完全沒有** |

### 9.2 Intent 區隔：**完全不存在**

現有 22 題只用 `category`（主題）與 `unbranded`（是否指名品牌）分類。
**沒有任何欄位區分 Informational / Commercial Investigation / Comparison / Recommendation / Technical / Transactional。**

實際檢視 22 題後的人工歸類：

| Intent | 題數 | 例 |
|---|---|---|
| Informational | 4 | 「AEO 和 SEO 有什麼不同？」 |
| Technical | 5 | 「llms.txt 是什麼？要怎麼寫？」 |
| Commercial Investigation | 3 | 「台灣有哪些提供 AEO 的服務公司？」 |
| Recommendation | 2 | 「台灣做 AEO 的公司推薦」 |
| Transactional | 2 | 「AEO 服務大概多少錢？」 |
| Branded | 4 | 「ShellFans 是什麼公司？」 |
| **Comparison（ShellFans vs 競品）** | **0** | **完全沒有** |

**結論：題目本身不是隨機 prompt（主題分佈合理），但系統無法依 intent 分析。**
「Recommendation intent 的表現如何」這種問題目前答不出來 —— 而那正是商業上最重要的一類。

### 9.3 競品追蹤：完全沒有

`ai_visibility_results` 不記錄「這次回答提到了哪些其他公司」。
2026-08-16 的稽核是我**人工閱讀回答原文**才發現 Shopto、Kairos Studio、
立仁世紀數位行銷、戰國策集團、零一行銷、可思科技被點名。
系統本身無法自動偵測或追蹤這件事。

---

## 10. AI Visibility Logic Audit

### 10.1 「建議優先處理」的實際判定

`src/lib/ai-visibility/scorecard.ts:188` `opportunityAdvice()`：

```ts
if (m.attributionGap >= t.gapSignificant && m.entityMentionRate < t.highRate) {
  return 'AI 已使用官方資料，但品牌歸因不足 —— 補強實體關係即可見效';
}
if (m.entityMentionRate === 0 && m.ecosystemCitationRate === 0) {
  return '此主題尚未建立 AI 能見度，需先建立主題內容';   // ← 就是這一行
}
...
```

**確認：判定確實只用 `mention === 0 && citation === 0`。**

排序用的 `priorityScore()` 也只看四個量：
`gap × 1.5 + mentionDeficit × 1.0 + citationDeficit × 0.6 + volume × 0.3`

### 10.2 系統無法區分的情況

「0% → 需先建立主題內容」這句話，在以下**六種完全不同的情況下都會出現**：

| 實際情況 | 系統能否區分 | 正確建議應該是 |
|---|---|---|
| 真的沒有內容 | ❌ | 建立內容 |
| **有內容但 AI 沒抓到** | ❌ | 檢查爬蟲到訪與 sitemap |
| **有內容但 AI 不理解我們是 AEO 公司** | ❌ | 補強 Entity 與服務宣告 |
| **有內容但無第三方 citation** | ❌ | 取得外部提及 |
| **競品權威度更高** | ❌ | 差異化定位 |
| **爬蟲被擋** | ❌ | 檢查 robots/WAF |
| **內容沒回答 Recommendation intent** | ❌ | 調整內容形狀 |

**而 ShellFans 目前的實況正好是第 2、3、4 種 —— 系統卻建議「建立內容」。**
這會直接導致做錯事：加更多內容，而真正的瓶頸在別處。

### 10.3 系統其實已經有的資料（只是沒接起來）

| 判斷所需 | 資料是否存在 | 是否被 opportunityAdvice 使用 |
|---|---|---|
| Crawler Accessibility | ✅ `crawler_access_logs` | ❌ |
| Indexability | ✅ `aeo_geo_scans`（八面向分數） | ❌ |
| Schema | ✅ 同上 | ❌ |
| Internal Linking | ❌ 無資料 | ❌ |
| Content Exists | ❌ 無「主題 ↔ 頁面」對應表 | ❌ |
| External Citation | ❌ 無資料模型 | ❌ |
| Competitor Visibility | ❌ 無資料 | ❌ |

> **最可惜的一點**：`crawler_access_logs` 與 `aeo_geo_scans` 都在同一個資料庫裡，
> 完全有能力回答「這個主題有沒有頁面、爬蟲有沒有抓到、schema 有沒有」，
> 但 `opportunityAdvice()` 一個都沒用到。

---

## 11. Crawler Audit

### 11.1 User-agent 辨識 ✅

`src/lib/crawler/classifier.ts` 涵蓋需求清單全部：
GPTBot、ChatGPT-User、OAI-SearchBot、ClaudeBot、Claude-SearchBot、Claude-User、
anthropic-ai、Google-Extended、Googlebot、GoogleOther、Google-InspectionTool、
Bingbot、PerplexityBot、Perplexity-User、Applebot、Applebot-Extended、
Bytespider、Meta-ExternalAgent、CCBot、Amazonbot、DuckAssistBot、YouBot、cohere-ai

### 11.2 檢查結果

| 檢查 | 結果 |
|---|---|
| user agent mapping | ✅ 正確 |
| bot 誤分類 | ✅ 已於 2026-08-19 修正（GCP VM 偽裝 Googlebot 的驗證漏洞） |
| site / tenant isolation | ✅ `site_key` 欄位 + 所有查詢皆帶條件 |
| crawler trend 統計 | ✅ `crawler-analytics.ts`（完整日、MA7、7D vs 7D、Bot×狀態診斷） |
| 對照工程起始日 | ✅ `monitored_sites.aeoProjectStartDate` + `aeo_milestones` |
| **對照 Content Publish Date** | ❌ **無法** —— 沒有任何地方記錄頁面發布日期 |
| **某篇內容發布後 crawler 是否增加** | ❌ **無法** —— 同上 |

> 這是一個具體且可修的缺口：`aeo_milestones` 已經有「日期 + 標題」的結構，
> 若每次發布內容時新增一筆里程碑，趨勢圖上就能對照。目前只有 2 筆里程碑。

---

## 12. Citation / Referral Audit

### 12.1 第三方 Citation 管理：**完全不存在**

搜尋 `case_study`、`testimonial`、`external_citation`、`backlink`、
`media_mention`、`press` —— **schema 檔案數皆為 0**。

沒有任何地方管理：媒體報導、Meet 創業小聚、Medium、LinkedIn、
外部訪談、Partner mention、backlinks。

唯一可觀察的外部訊號是 AI 回答中出現過 `tw.linkedin.com/company/shellfans`
（OpenAI 在回答品牌題時引用），但這是**被動觀察到的**，系統沒有管理它。

### 12.2 AI Referral Traffic：**完全不存在**

全 repo 搜尋 `chatgpt.com`、`chat.openai.com`、`perplexity.ai`、`claude.ai`、
`gemini.google.com`、`copilot.microsoft.com`：

**唯一命中是 `verification.ts` 裡的 Perplexity IP 範圍 JSON 網址**，與 referral 無關。

| 需求 | 現況 |
|---|---|
| 儲存 referrer | 🟡 `crawler_access_logs.referer` 有欄位，但**只記錄爬蟲請求**，不是真人流量 |
| UTM | 🟡 `aeo_leads` 有 utm_*（業務 CRM），與 AI referral 無關 |
| landing page / source / session / conversion | ❌ 全無 |

### 12.3 五個指標的區分能力

| 指標 | 是否可量測 |
|---|---|
| AI Crawler Visibility | ✅ 完整（含驗證、狀態碼、涵蓋面） |
| AI Brand Mention | ✅ `results.brandMentioned` |
| AI Citation | ✅ `results.officialCited` + `citations` |
| **AI Referral Traffic** | ❌ **完全無法量測** |
| **Conversion** | ❌ 業務 CRM 有 lead，但**無法歸因到 AI referral** |

**前三個分得很清楚，後兩個完全是黑洞。**

---

## 13. Case Study Audit

**完全不存在** —— 網站、資料模型、CMS 皆無。

| 檢查 | 結果 |
|---|---|
| 網站有 case study 頁 | ❌（`/case-studies` 回 302） |
| 資料模型 | ❌ |
| CMS 管理 | ❌ |

### 但資料其實已經有了

現有系統已能產出 Case Study 所需的**全部欄位**：

| Case Study 欄位 | 資料來源 | 有無 |
|---|---|---|
| Client / Industry | `monitored_sites.displayName` / `customerName` | ✅ |
| Baseline | `ai_visibility_runs`（最早一次） | ✅ |
| Question Set | `ai_visibility_questions` | ✅ |
| Optimization Actions | `aeo_milestones` | ✅ |
| AI Bot / Search Bot Visits | `crawler_access_logs` | ✅ |
| Brand Mention | `results.brandMentioned` | ✅ |
| Official Citation | `results.officialCited` | ✅ |
| Before / After | 趨勢 API 已計算 | ✅ |
| Time Range | ✅ | ✅ |
| Target | ❌ 無「目標值」欄位 | ❌ |
| Competitor comparison | ❌ | ❌ |

> **師德文教目前已有 4 次探測、10 天爬蟲資料、完整的 before/after。**
> Case Study 缺的不是資料，是**客戶露出授權**與一個公開頁面。
> 授權屬商業決定，不在工程範圍。

---

## 14. Content Gap Analysis

### Gap 1 — AI Visibility 檢測（P0）

| 項目 | 內容 |
|---|---|
| **Target Topic** | 如何檢測品牌在 AI 中的能見度 |
| **Target User Intent** | Technical + Commercial Investigation |
| **Target AI Question** | 「如何知道 ChatGPT 有沒有提到我的品牌？」「如何知道 AI 有沒有引用我的官網？」 |
| **Existing Content** | 無。`/aeo/ai-crawler-monitoring` 談的是爬蟲**到訪**，不是**提及與引用** |
| **Why Insufficient** | 爬蟲來過 ≠ 被提及 ≠ 被引用。這三件事我們的產品分得很清楚，但網站上沒有一頁解釋差別 |
| **Recommended Page** | `/aeo/ai-visibility-check` |
| **Recommended Internal Links** | ← `/aeo` hub、`/aeo/ai-crawler-monitoring`、`/aeo-geo/methodology`；→ `/tools/aeo-geo-checker`、`/aeo-geo` |
| **Recommended Entity** | 明確宣告 `Service: AI Visibility Analysis`（目前只有暗示） |
| **Recommended Schema** | TechArticle + FAQPage + Service |
| **Expected KPI** | 「如何知道 ChatGPT 是否提到品牌」類問題的提及率 0% → 有數字 |

### Gap 2 — Case Study（P0）

| 項目 | 內容 |
|---|---|
| **Target Topic** | 實際客戶的 AEO 成效 |
| **Target User Intent** | Trust / Commercial Investigation |
| **Target AI Question** | 「AEO 服務真的有效嗎？」「有沒有實際案例？」 |
| **Existing Content** | **零** |
| **Why Insufficient** | 競品被 AI 描述為「**有實績案例支撐**」（戰國策），我們完全沒有 |
| **Recommended Page** | `/aeo/case-studies` + 至少 1 篇個案 |
| **Recommended Internal Links** | ↔ `/aeo-geo`、`/aeo/managed-hosting`、`/aeo/cost` |
| **Recommended Entity** | `Organization` + 客戶 `Organization`（需授權） |
| **Recommended Schema** | Article + FAQPage |
| **Expected KPI** | 服務推薦類問題的提及率 |
| **⚠️ 前置條件** | **需客戶露出授權。無授權則不可做** —— 捏造或匿名化到無法驗證的案例，反而傷害可信度 |

### Gap 3 — 服務 Entity 明確宣告（P0，非新增頁面）

| 項目 | 內容 |
|---|---|
| **Target Topic** | ShellFans 提供哪些 AEO/GEO 服務 |
| **Existing Content** | `/aeo-geo` 文案有提到「定期量測能見度」 |
| **Why Insufficient** | **只有文案，沒有 Service schema 節點。** AI 無法從知識文章推導出服務關係。第 5.2 節列出三項「僅暗示」 |
| **Recommended Action** | **不新增頁面** —— 在既有 `/aeo-geo` 補 `Service` 節點：AI Visibility Analysis、AI Citation Monitoring、Brand Entity Optimization；並在 `Organization` 補 `knowsAbout` |
| **Expected KPI** | Entity 辨識正確率（品牌題中 AI 是否提到 AEO/GEO） |

### Gap 4 — Recommendation Intent 的答案形狀（P1）

| 項目 | 內容 |
|---|---|
| **Target AI Question** | 「台灣做 AEO 的公司推薦」「推薦台灣 AEO/GEO 服務商」 |
| **Existing Content** | `/aeo/taiwan-companies` —— 標題完全對上，但**刻意不列名單** |
| **Why Insufficient** | 這是**編輯原則與 AI 答案形狀的直接衝突**。AI 找的是「一份清單」，我們給的是「評估準則」。08-16 已補可查證的自我事實欄位表，但**尚未被探測驗證** |
| **Recommended Action** | **先不動。** 等下次探測看該表格是否生效，再決定是否調整 —— 現在改等於在沒有量測的情況下推翻一個有理由的編輯判斷 |

### Gap 5 — GEO vs SEO / 三方比較（P2）

| 項目 | 內容 |
|---|---|
| **Existing Content** | `/aeo/aeo-vs-seo` + `/aeo/aeo-vs-geo`，需讀者自行推導 |
| **Why Insufficient** | 「SEO vs AEO vs GEO」是常見搜尋句，但目前需拼兩頁 |
| **Recommended Page** | `/aeo/seo-vs-aeo-vs-geo`（三方對照表） |
| **⚠️ Cannibalization 風險** | **中高** —— 與既有兩頁高度重疊。若建，必須是**三方對照表**而非重述定義，並在既有兩頁加 canonical 導引 |

### Gap 6 — 驗收方式（P2）

現有 `/aeo/how-to-choose-agency` 的「合約中該確認的」段落已涵蓋八成。
**建議不新增頁面**，改為在該頁加一個 H2「專案如何驗收」讓標題直接對上問題。

---

## 15. Root Cause Analysis

### 三個 0% 的成因（依證據強度排序）

| # | Root Cause | 證據 | 狀態 |
|---|---|---|---|
| 1 | **AEO 語意歧義** | 問「台灣有哪些 AEO 服務公司」兩家 AI 都答成報關行；引用最多網域是財政部關務署（13 次） | ✅ 08-15 已修題目，**未驗證** |
| 2 | **首頁無自我定位** | 爬蟲 39% 請求在首頁；首頁 08-19 前完全沒提 AEO/GEO | ✅ 08-19 已修，**未驗證** |
| 3 | **核心頁未被抓** | GPTBot / OAI-SearchBot 30 天內**從未抓過 `/aeo-geo`** | 🟡 已推 IndexNow，需觀察 |
| 4 | **無第三方 citation** | 36 筆未指名回答中 0 筆引用提及 ShellFans 的外部來源 | ❌ **未解，非工程可解** |
| 5 | **Entity fragmentation** | OpenAI 查「唄粉智能科技」誤判為粉體產業 | ✅ 08-19 已修，**未驗證** |
| 6 | **服務 Entity 只暗示不宣告** | 三項服務無 Service schema 節點 | ❌ 未解 |
| 7 | **建議演算法誤導** | `mention===0 && citation===0 → 建議建立內容`，而實際瓶頸在 2/3/4 | ❌ 未解 |

**關鍵觀察：1、2、5 都已修但都還沒被量測過**（最後一次探測 2026-08-12）。

---

## 16. P0 / P1 / P2 Priority

### P0（做這些之前不要新增其他內容）

| # | 項目 | 類型 | 難度 |
|---|---|---|---|
| 1 | **重新探測建立新基準線** | 驗證 | 極低（排程已存在） |
| 2 | **補服務 Entity 宣告**（Service schema × 3 + `knowsAbout`） | 改既有頁 | 低 |
| 3 | **`/aeo/ai-visibility-check`** | 新增 1 頁 | 中 |
| 4 | **修正 `opportunityAdvice()` 判定** | 程式 | 中 |

### P1

| # | 項目 | 類型 | 前置條件 |
|---|---|---|---|
| 5 | Case Study 頁 + 1 篇個案 | 新增 | **需客戶授權** |
| 6 | Question Set 加 `intent` 欄位 | 資料模型 | — |
| 7 | 競品提及追蹤 | 程式 | — |
| 8 | 內容發布日 → `aeo_milestones` | 流程 | — |
| 9 | Person schema（創辦人頁） | 改既有頁 | — |
| 10 | `datePublished` / `dateModified` | 改產生器 | — |

### P2

| # | 項目 | 備註 |
|---|---|---|
| 11 | `/aeo/seo-vs-aeo-vs-geo` | **有 cannibalization 風險** |
| 12 | 「專案如何驗收」H2 | 加在既有頁，不新增頁 |
| 13 | AI Referral 追蹤 | 需前端埋點，範圍較大 |
| 14 | 外部 citation 管理模型 | 需先有外部提及才有意義 |
| 15 | 3 頁補回連 pillar | 極小 |

---

## 17. Minimum Recommended Content Set

**第一階段最少需要新增的頁面：1 頁。**

```
/aeo/ai-visibility-check   —— 回答「如何知道 AI 有沒有提到／引用我」
```

理由：這是 Cluster C 唯一一個「**我們有產品、有資料、有方法論，卻沒有任何一頁在談**」的主題，
而且它同時服務 Technical 與 Commercial Investigation 兩種 intent。

**其餘 P0 都不是新增頁面**：補 Service schema、修演算法、重新探測。

**Case Study 若拿得到授權，是第 2 頁** —— 但那是商業前提，不是內容工作。

---

## 18. Should We Mass Generate Content? — **No**

### 理由一：內容不是瓶頸

Cluster A 覆蓋 81%、Cluster B 65%、Cluster C 59%。
30 個 AEO 頁面、zero orphan、Schema 100%、151 條 FAQ。
**這已經超過多數同業的內容量。**

而競品用**更少的內容**被 AI 點名（Shopto、Kairos Studio、戰國策、零一行銷）——
差別不在量。

### 理由二：三批改動都還沒被量測

最後一次探測是 **2026-08-12**，而之後有三批重大改動：

| 日期 | 改動 |
|---|---|
| 08-14 / 08-16 | 26 頁知識叢集上線 |
| 08-15 | 題目去歧義（8 題） |
| 08-19 | 品牌定位改版 + Entity 統一 |

**在沒有新基準線的情況下再加內容，等於用更多變數去猜一個還沒觀測的結果。**
下週一探測完，我們才會知道前三批做對了多少。

### 理由三：大量生文會直接踩到我們自己寫的原則

`/aeo/what-is-aeo` 的「誤解三」寫著：

> 大量薄內容對答案引擎沒有幫助，甚至有反效果——它會稀釋你的實體訊號，
> 讓模型更難判斷你到底專精什麼。一頁把一個問題講清楚，勝過十頁各講三成。

自己違反自己公開的方法論，是可被 AI 直接看見的矛盾。

### 理由四：真正的瓶頸是工程解不了的

第三方 citation。競品被描述為「有實績案例支撐」，我們沒有。
再寫一百頁自己說自己好，也補不上這一項。

---

## 19. Recommended Implementation Plan

### 階段一：驗證（本週）

1. 等 **2026-08-24（週一）09:00** 的排程探測完成
2. 對照 08-12 基準，確認三件事：
   - AI 是否還把 AEO 答成報關行（驗證 08-15 的題目修正）
   - 品牌題中 AI 是否提到 AEO/GEO（驗證 08-19 的定位改版）
   - OpenAI 是否找得到「唄粉智能科技」（驗證 Entity 統一）
3. ⚠️ 題目文字已於 08-15 變更，屬**量測工具變更**，已在 `aeo_milestones` 標記。
   趨勢比較須注意此轉折點。

### 階段二：補 Entity 與量測內容（驗證後）

4. `/aeo-geo` 補三個 Service 節點 + `Organization.knowsAbout`
5. 新增 `/aeo/ai-visibility-check`
6. 3 頁補回連 pillar
7. 內容發布時同步寫入 `aeo_milestones`

### 階段三：修正判定邏輯

8. `opportunityAdvice()` 接上既有資料（`crawler_access_logs`、`aeo_geo_scans`），
   讓「0%」能區分「沒內容」與「有內容但沒被抓 / 沒被理解 / 沒有外部佐證」
9. Question Set 加 `intent` 欄位；`results` 加競品提及偵測

### 階段四：商業前提（非工程）

10. 取得客戶露出授權 → Case Study
11. 外部提及（媒體、目錄、社群）—— 這是唯一能真正動搖第 4 個 root cause 的事

---

## 附：第十七節七問直答

**Q1. 缺的是內容量還是 Topic Architecture？**
**兩者都不是。** Architecture 已完整，內容量已足夠。缺的是「服務 Entity 的明確宣告」、
「量測面的內容」、「第三方佐證」。

**Q2. 現有內容是否足以形成 Topical Authority？**
**技術面足夠，權威面不足。** Topical authority 需要「內容 + 實體清晰 + 外部佐證」三者，
我們有前兩項（第三項為零）。

**Q3. 三個 0% 的主要 Root Cause？**
語意歧義（已修未驗證）、首頁無定位（已修未驗證）、無第三方佐證（未解）。
**不是「沒有內容」。**

**Q4. 什麼都不新增、只調整既有內容，能解決多少？**
**約 60–70%。** 補 Service schema、修回連、加驗收 H2、修演算法都不需新頁面。
剩下的 30–40% 是量測面內容（1 頁）與 Case Study（需授權）。

**Q5. 最少需要新增哪些頁面？**
**1 頁**：`/aeo/ai-visibility-check`。若拿到授權，加 Case Study。

**Q6. 第一階段最少幾篇？**
**1 篇。** 不是 10 篇，不是 30 篇。

**Q7. 哪些文章不該建立？**

| 不該建 | 原因 |
|---|---|
| 「AEO 是什麼」的第二篇 | 與 `/aeo/what-is-aeo` 直接重複 |
| `/aeo/geo-vs-seo` 單獨頁 | 與 `aeo-vs-seo` + `aeo-vs-geo` 重疊，若要做應是**三方合併頁**取代而非並存 |
| 各家 AI 平台的個別介紹頁（如「什麼是 ChatGPT」） | 非我們的主題，稀釋實體訊號 |
| 產業別 landing page（電商 AEO、B2B AEO…） | 目前僅 1 家 AEO 客戶，無真實 use case，會變成換名詞的薄內容 |
| `/aeo/organization-schema`、`/aeo/product-schema` 等 schema 分頁 | 與 `/aeo/schema` 重疊 |
| 「AEO 費用」的第二篇 | 與 `/aeo/cost` 重複 |

---

**本稽核未修改任何程式或內容。** 待 review 後再進入第二階段。
