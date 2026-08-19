# shell.fans 未被 AI 引用：Root Cause Audit

日期：2026-08-19
範圍：shell.fans（自家網站）+ saas_womm 的 AI Visibility 與 crawler 監控系統
證據基礎：2026-08-12 探測的 44 筆實際 AI 回答、近 30 天 crawler log、44 頁網站實測、15 支爬蟲的 live 存取測試

---

## 1. Executive Summary

**0% 是真的，而且問題不在 Crawlability。**

15 支 AI 爬蟲對 4 個核心 URL 全部拿到 200，robots.txt、llms.txt、sitemap 皆正常。
但爬蟲**幾乎只抓首頁**：ClaudeBot 30 天內抓首頁 291 次、`/aeo-geo` 2 次；
GPTBot 與 OAI-SearchBot 在 30 天內**從未抓過 `/aeo-geo`**。

而首頁在 2026-08-19 之前，`<title>`、description、正文完全沒有提到 AEO/GEO。
爬蟲對 ShellFans 的認識 = 首頁 = 一家社群備份公司。這與 AI 實際回答的內容完全吻合：
問「ShellFans 提供哪些服務？」時 Anthropic 完全沒提 AEO/GEO。

**最大問題在 Content relevance 與 Entity clarity 的交界**，不是技術可達性。

本次同時發現並修正兩個**產品層級的 bug**（見第 11、12 節），
其中一個是安全性問題：任何 GCP 客戶都能偽裝成 Googlebot 通過我們的驗證。

---

## 2. Data Reliability Check

### 2.1 0% 是否為 parser 漏判？

**否。** 對 36 筆未指名品牌回答做全文掃描：

| 檢查項 | 命中數 |
|---|---|
| 回答內文出現 ShellFans / 唄粉智能 / 唄粉 | **0** |
| 回答內文出現產品名（AEO Managed Hosting / AI Readiness Score / KOL.FANS / 續航引擎） | **0** |
| 回答內文出現 shell.fans / kol.fans | **0** |
| 引用清單出現 shell.fans / kol.fans | **0** |
| 探測失敗（會被排除分母，不計為 0） | 0 |

### 2.2 Scorer 陽性對照

用實際的 site entity 設定跑 12 個對照案例：

| 案例 | 提及 | 引用 | 判定 |
|---|---|---|---|
| 純品牌名 | ✅ | — | 正確 |
| 裸 URL 在內文 | ✅ | — | 正確 |
| 引用清單 | — | ✅ shell.fans | 正確 |
| **www 子網域** | — | ✅ shell.fans | 正確（正規化有效） |
| **深層路徑 + query** | — | ✅ shell.fans | 正確 |
| 生態系網域 kol.fans | — | ✅ kol.fans | 正確 |
| **Markdown 連結** | ✅ | — | 正確 |
| 法人全名 | ✅ | — | 正確 |
| 歧義簡稱單獨出現（唄粉） | ❌ | — | 正確（設計如此，需佐證） |
| 歧義簡稱 + 佐證 | ✅ | — | 正確 |
| 無關內容（陰性對照） | ❌ | ❌ | 正確 |

**結論：citation / mention 判定邏輯無漏判。0% 可信。**

### 2.3 Site entity 設定

```json
brand_entity: {
  canonicalName: "ShellFans",
  aliases: ["唄粉智能", "唄粉", "shell.fans"],
  legalNames: ["唄粉智能科技股份有限公司"],
  englishNames: ["ShellFans AI Technology"],
  products: ["AEO Managed Hosting", "AI Readiness Score", "KOL.FANS", "續航引擎"],
  ambiguousAliases: ["唄粉"]
}
domains: { corporate: ["shell.fans"], officialEcosystem: ["shell.fans","kol.fans"], includeSubdomains: true }
```

`brand_keywords` 為空是正常的 —— `brand_entity` 優先，空值不會 fallback 失敗。

> ✅ **已確認（2026-08-19）**：法人為**台灣**公司 —— 唄粉智能科技股份有限公司，
> 統一編號 83032387，臺北市內湖區瑞光路335號4樓。名稱前**不加任何國別前綴**。
> 全站已完成清查與修正（見第 17 節）。

---

## 3. Crawlability Audit

### 3.1 HTTP / Edge

| URL | 狀態 | 重導次數 | Content-Type |
|---|---|---|---|
| `https://shell.fans/` | 200 | 0 | text/html |
| `https://www.shell.fans/` | 200 | 1 → apex | text/html |
| `http://shell.fans/` | 200 | 1 → https | text/html |
| `/aeo-geo` | 200 | 0 | text/html |
| `/aeo` | 200 | 0 | text/html |
| `/llms.txt` | 200 | 0 | **text/plain** |
| `/robots.txt` | 200 | 0 | text/plain |
| `/sitemap.xml` | 200 | 0 | text/xml |

無 `X-Robots-Tag`，無意外 `noindex`（首頁為 `index, follow`）。

### 3.2 15 支 AI 爬蟲的 live 存取測試

GPTBot、OAI-SearchBot、ChatGPT-User、ClaudeBot、Claude-SearchBot、Claude-User、
Google-Extended、Googlebot、bingbot、PerplexityBot、Perplexity-User、Amazonbot、
meta-externalagent、CCBot、Bytespider

對 `/`、`/aeo-geo`、`/aeo`、`/llms.txt` —— **全部 60 個組合皆 200**。

**無 WAF 攔截、無 challenge、無 rate limit、無 bot-specific blocking。**

**判定：Crawlability = Pass（Confidence: Confirmed）**

---

## 4. AI Crawler Evidence

### 4.1 近 30 天 AI 爬蟲 × 核心頁（僅列已驗證者）

| Bot | 驗證 | 首頁 | `/aeo-geo` | `/aeo/*` | 總請求 |
|---|---|---|---|---|---|
| Google-Extended | verified | 171 | **0** | **0** | 261 |
| OAI-SearchBot | verified | 13 | **0** | 4 | 203 |
| ChatGPT-User | verified | 100 | 9 | 2 | 179 |
| GPTBot | verified | 11 | **0** | 25 | 95 |
| PerplexityBot | verified | **4** | **0** | 1 | **47** |
| Amazonbot | unsupported | 769 | 2 | 22 | 1510 |
| Meta-ExternalAgent | unsupported | 178 | 19 | 41 | 821 |
| ClaudeBot | unsupported | 291 | **2** | **1** | 722 |
| CCBot | unsupported | 138 | 3 | **0** | 353 |
| Claude-SearchBot | unsupported | 99 | 1 | **0** | 281 |

### 4.2 關鍵觀察

1. **首頁佔全部 AI 爬蟲請求的 39%**（2,169 / ~5,600）。
2. **`/aeo-geo` 在 30 天內只被抓 38 次**，其中已驗證爬蟲僅 9 次（全部來自 ChatGPT-User，
   即人為觸發 —— 很可能是我們自己測試時造成的）。
3. **GPTBot 與 OAI-SearchBot 從未抓過 `/aeo-geo`。** 這兩支正是餵養 ChatGPT 的爬蟲。
4. **PerplexityBot 30 天只來 47 次**，且從未抓 `/aeo-geo`。Perplexity 是最會標註來源的平台。
5. `/aeo` 叢集（26 頁）於 08-14 才上線，抓取量低屬正常，尚不足以判斷。

### 4.3 可用性事故

| 日期 | 521 次數 | 影響 |
|---|---|---|
| 2026-07-28 | 44 | 部分爬蟲 |
| **2026-08-01** | **319** | 幾乎所有主要爬蟲（含 GPTBot、OAI-SearchBot、PerplexityBot、ClaudeBot） |
| 2026-08-02 | 208 | 同上 |
| 2026-08-03 | 127 | 同上 |

**連續三天、近 700 次 521（origin 連不上）。** 這與 2026-08-01 的 nginx 啟動期 DNS 事故吻合。
爬蟲在三天內反覆拿到 5xx，通常會降低後續抓取頻率。

**判定：AI Crawler 到訪 = Pass；抓核心內容 = Fail（Confidence: Confirmed）**

---

## 5. 技術 SEO/AEO Audit

| 項目 | 狀態 | 證據 |
|---|---|---|
| robots.txt | ✅ Pass | 21 個 AI crawler 群組明確 Allow，無任何 Disallow |
| llms.txt | ✅ Pass | 200、text/plain、含實體與核心服務頁、25 個 `/aeo/` 連結 |
| llms-full.txt | ✅ Pass | 200 |
| sitemap.xml | ✅ Pass | 44 條全部 200，無重複、無 redirect、無 404 |
| canonical | ✅ Pass | 各頁指向自身，www → apex |
| HTTPS / viewport | ✅ Pass | — |
| Schema 覆蓋 | ✅ Pass | 44 頁**全部**有 JSON-LD，0 頁無 schema |
| FAQPage | 🟡 Warning | 31/44 有 FAQ 區塊，30/44 有 FAQPage；`fans-analysis.html` 有 FAQ 文案卻缺 schema |
| H1 | 🟡 Warning | `privacy-policy` 與 `terms-and-conditions` 全頁無 H1；`helpcenter` 的 H1 是錯字「仍有疑問麻?」且 0 個 H2 卻有 84 個 H3 |

---

## 6. Content / Query Intent Audit

對 9 個未指名品牌意圖逐一檢查（狀態為 2026-08-19，已含 08-14～16 新增的 26 頁）：

| Query intent | 精確匹配頁 | title 匹配 | H1 匹配 | 首屏直接回答 | 明寫品牌名 |
|---|---|---|---|---|---|
| 台灣有哪些 AEO 服務公司？ | `/aeo/taiwan-companies` | ✅ | ✅ | 🟡 刻意不列名單 | ✅ 有事實欄位表 |
| 台灣做 AEO 優化的公司推薦 | 同上 | 🟡 | 🟡 | 🟡 | ✅ |
| 想讓網站被 ChatGPT 引用，該找誰協助？ | `/aeo/managed-hosting`、`/aeo/consulting` | 🟡 | ❌ 標題非此問法 | ✅ | ✅ |
| 台灣有哪些 GEO 生成式引擎優化服務？ | `/aeo/what-is-geo`、`/aeo/taiwan-companies` | 🟡 | 🟡 | ✅ | ✅ |
| 哪些公司有提供 AEO/GEO 服務？ | `/aeo/taiwan-companies` | 🟡 | 🟡 | 🟡 | ✅ |
| 有哪些台灣 AEO/GEO Checker？ | `/aeo-geo/taiwan-aeo-tools` | ✅ | ✅ | ✅ | ✅ |
| 哪些公司提供 AI-ready 網站代管？ | `/aeo/managed-hosting` | 🟡 | 🟡 | ✅ | ✅ |
| AEO Managed Hosting 是什麼？ | `/aeo/managed-hosting` | ✅ | ✅ | ✅ | ✅ |
| 如何讓網站更容易被 ChatGPT/Claude/Google AI 引用？ | `/aeo/how-ai-search-works` | ✅ | ✅ | ✅ | 🟡 |

### 核心張力

`/aeo/taiwan-companies` 的 H1 完全對上「台灣有哪些 AEO 服務商？」，
但內容**刻意不列廠商名單**（理由：無可驗證的公開資料，且在自家網站排名同業有利益衝突）。

這個編輯判斷本身正確，但代價是：當 AI 尋找「一份服務商清單」時，我們提供的是評估準則。
2026-08-16 已補上可查證的自我事實欄位表（公司全名、統編、服務內容、交付形式），
**但這份資料上線時間晚於最後一次探測，效果尚未被量測。**

---

## 7. Entity Audit

### 7.1 發現的 Entity Fragmentation（已修正）

稽核前，全站 41 個 Organization 宣告有**三種不同形態**：

| 頁數 | `name` | `@id` |
|---|---|---|
| 29 | `唄粉智能科技股份有限公司` | `https://shell.fans/#organization` |
| 11 | `ShellFans AI Technology` | 同上 |
| 1 | `ShellFans AI Technology` | **無 @id** |

**同一個 `@id` 底下有兩個互相衝突的 `name`。**

而 AI 證據直接印證了這個問題的後果：

> 「唄粉智能科技是做什麼的？」— OpenAI：「未能找到名為"唄粉智能科技"的公司……
> 市场上有多家专注于**粉体物料**自动化处理和智能化技术的公司」
> 然後推薦了浙江兆色科技（自動色粉機）、深圳丰年智达（超細粉體生產線）。

以法人中文名作為 `name`，在 AI 眼中「唄**粉**」的「粉」被理解成粉末。

### 7.2 已執行的修正

41 頁統一為單一宣告：

```json
{
  "@type": "Organization",
  "@id": "https://shell.fans/#organization",
  "name": "ShellFans AI Technology",
  "legalName": "唄粉智能科技股份有限公司",
  "alternateName": ["ShellFans", "ShellFans AI", "唄粉智能科技股份有限公司", "唄粉智能科技", "shell.fans"],
  "taxID": "83032387",
  "sameAs": [...]
}
```

產生器 `scripts/build-aeo-pages.py` 同步更新，重跑不會退回。

### 7.3 其他實體訊號

| 項目 | 狀態 |
|---|---|
| WebSite schema | ✅ 有 |
| Service schema（AEO/GEO + 續航引擎） | ✅ 兩條並列，Organization 加了 `makesOffer` |
| WebApplication（Checker） | ✅ 有 |
| FAQPage | ✅ 30/44 |
| sameAs | ✅ FB / IG / console / blog |
| taxID | ✅ 83032387 |
| contactPoint | 🟡 未使用 `contactPoint`，聯絡資訊在頁尾純文字 |

---

## 8. Internal Linking Audit

| 檢查 | 結果 |
|---|---|
| 首頁 nav → `/aeo-geo` | ✅ 1 條（「AEO/GEO 代管」） |
| 首頁正文 → `/aeo*` | ✅ 3 條 |
| 首頁頁尾 AEO 連結區 → `/aeo*` | ✅ 8 條 |
| `/aeo-geo` 是否 orphan | ❌ 否，被多處連結 |
| `/aeo` 知識中心是否被首頁連結 | 🟡 頁尾連結區的 8 條**沒有一條指向 `/aeo` hub** |
| anchor text 語意 | ✅ 含 AEO/GEO、AI 搜尋整備度、AI-ready 網站代管 |
| breadcrumb | ✅ 30/44 有 BreadcrumbList |

**判定：Internal linking = Pass（`/aeo-geo` 不是 orphan）**

但頁尾連結區有 3 條指向 `/aeo-geo#dimensions`、`#managed-service`、`#plans`——
同一頁的三個 fragment，稀釋了連結多樣性。

---

## 9. External Authority Gap

**`Unknown — external authority dataset not available`**

repo 與資料庫中**沒有任何** backlink、referral domain、第三方提及的資料來源。
不虛構 Domain Authority 或 backlink 數字。

唯一可觀察的外部訊號來自 AI 回答本身：

- OpenAI 在回答「ShellFans 是什麼公司？」時**引用了 `tw.linkedin.com/company/shellfans`**，
  並據此陳述「成立於 2023 年」（需人工確認正確性）。
- 未指名品牌的 36 筆回答中，**0 筆**引用任何提及 ShellFans 的第三方來源。

這是目前**最大的未知數，也可能是最大的實際瓶頸**：
只有自家網站說自己是 AEO 服務商，訊號強度遠低於被多個獨立來源提及的競品。

---

## 10. Competitor Citation Comparison

從實際 AI 回答中擷取（問題：「台灣做 AEO 優化的公司推薦」）：

| 平台 | 被點名的公司 | 被引用的網域 |
|---|---|---|
| OpenAI | Shopto、Kairos Studio、立仁世紀數位行銷 | `shopto.tw`、`kairossite.com` |
| Anthropic | 戰國策集團、零一行銷、可思科技 | （未附網址） |

**6 家同業被點名，ShellFans 0 次。**

AI 對它們的描述模式（直接引自回答原文）：

- **Shopto**：「台灣**首家**同時具備 SEO 和 AEO 雙引擎的**電商平台**，協助品牌在 Google 和 AI 問答引擎中獲得免費流量」
- **Kairos Studio**：「提供 AI 驅動的**建站平台**，透過自動生成結構化資料和 AEO 優化」
- **戰國策集團**：「提供整合 SEO、GEO 及 AEO 的**一站式解決方案**……**有實績案例支撐**」
- **零一行銷**：「從 SEO 出發、延伸至 GEO 與 AEO……**2026 年的服務項目已明確納入**『如何讓品牌被 ChatGPT、Google AI Overview 引用』」

### 為什麼 AI 選它們而非 ShellFans

依證據可歸納三點（非推測，皆有回答原文支持）：

1. **它們有一句話可以被複述的自我定位**（「台灣首家雙引擎」「一站式解決方案」）。
   ShellFans 的首頁到 2026-08-19 之前完全沒有 AEO/GEO 的自我定位句。
2. **它們被描述為「公司／平台／服務商」**，ShellFans 被描述為「社群備份平台」。
3. **戰國策被特別提到「有實績案例支撐」** —— 我們沒有任何可公開的案例。

> ⚠️ 未對競品網站做技術面比較（title / schema / word count / page age）。
> 那需要實際抓取第三方網站，不在本次自我稽核範圍內，標記為後續工作。

---

## 11. Probe / Scoring Logic Audit

### 11.1 已於 2026-08-15 修正：Category mapping 異常（**High priority bug，已修**）

本任務指定要檢查的「AEO 網站卻出現英語檢定選擇型、教材與教具需求型」**確實存在**，
且已在 2026-08-15 修正並記錄於 `docs/audits/aeo-report-taxonomy-tenant-isolation-audit.md`。

- **Root cause**：key→label 的對應只有一份 global 常數，內容是第一個客戶（師德文教）的分類。
- **修正**：改為逐站台 `ai_visibility_categories` 表，UNIQUE `(site_id, category_key)`。
- **驗證**：ShellFans 報告 PDF 全文中「英語檢定」「教材與教具」「學校與機構」各 **0 次**；
  師德報告的分類完整保留且未混入 ShellFans 分類。

### 11.2 已於 2026-08-15 修正：AEO 語意歧義

**這是本次稽核中對「為何 0%」解釋力最強的單一發現。**

實際 AI 回答顯示：

| 題目 | 平台 | AI 理解成 |
|---|---|---|
| 台灣有哪些 AEO 服務公司？ | OpenAI | **Authorized Economic Operator**（報關行：飛運、捷盛報關） |
| 台灣有哪些 AEO 服務公司？ | Anthropic | **海關 AEO 認證**（基隆關 91 家廠商、長榮國際儲運） |
| AEO 顧問怎麼選？ | OpenAI | **American Eagle Outfitters**（美國服飾品牌） |
| AEO 顧問怎麼選？ | Anthropic | 海關 AEO 認證顧問（SGS、湯森路透） |

全部未指名題的引用網域中，**`aeo.customs.gov.tw`（財政部關務署）以 13 次居冠**。

也就是說：**有相當比例的 0%，是因為 AI 根本在回答另一個 AEO。**

已於 08-15 對 8 題補上「答案引擎優化」脈絡，但**新題目尚未被探測過**
（最後一次探測為 08-12），效果未知。

### 11.3 Probe 方法本身

| 檢查 | 結果 |
|---|---|
| Provider | OpenAI `gpt-4o-mini-search-preview`、Anthropic `claude-haiku-4-5` |
| Search mode | ✅ 兩者皆啟用（回答中有實際搜尋行為與 citations） |
| API vs consumer 差異 | 🟡 **已知限制**，schema 註解已明載：打的是 API，不等於使用者在網頁版看到的答案 |
| Google AI Overview | ⚠️ 已停用（SerpApi 額度限制），不影響本次結論 |
| Citation parser 各 provider 格式 | ✅ 陽性對照 12/12 通過 |
| probe failure 誤算為未引用 | ✅ 不會 —— `if (r.error) continue`，失敗不計入分母 |

**判定：Probe/scoring bug = 曾存在兩個，皆已修正（Confidence: Confirmed）**

---

## 12. 本次新發現並修正的 Bug：Crawler 驗證可被偽裝（**Critical**）

### Root cause

`src/lib/crawler/verification.ts`：

```ts
google: ['.googlebot.com', '.google.com', '.googleusercontent.com'],
```

`.googleusercontent.com` 是 **Google Cloud 虛擬機**的 rDNS 後綴 ——
任何人租一台 GCP 機器就拿得到。把它當成 Googlebot 的驗證依據，
等於任何 GCP 客戶都能偽裝成 Googlebot 通過驗證。

### Evidence

| ASN | 擁有者 | 請求數 | 其中 404 | 判定 |
|---|---|---|---|---|
| **396982** | **Google Cloud（租用 VM）** | **3,665** | **1,488** | 被標成 `verified` |
| 15169 | Google LLC（真 Googlebot） | 3,124 | 1,272 | `verified` |

GCP 那批抓的路徑：`/.boto`、`/.continue/config.json`、`/.codex/config.toml`、
`/firebase-adminsdk.json`、`/.htpasswd`、`/admin/.env`。**真正的 Googlebot 不會掃憑證檔案。**

**超過一半（54%）的「已驗證 Googlebot」流量其實是偽裝的攻擊掃描。**

### Impact

1. 客戶的爬蟲監控報告灌水 —— 把攻擊流量算成搜尋引擎抓取
2. 掩蓋了一組持續進行的憑證掃描攻擊
3. `AI Bot Coverage` 等指標失真

### Fix

移除 `.googleusercontent.com`。Google 官方文件：common crawlers（Googlebot、
Google-Extended、GoogleOther）與 special-case crawlers 的 rDNS 是 `*.googlebot.com`
或 `*.google.com`；只有 user-triggered fetchers（Feedfetcher、Site Verifier）
會用 `*.googleusercontent.com`，而那些不在本系統的分類範圍內。

已清除 `crawler_verification_cache` 中 234 筆 google 快取強制重新驗證，
並新增 3 個測試把界線釘住（含「後綴不得是可租用的雲端網域」的通則檢查）。

---

## 13. Root Cause Matrix

| Layer | Finding | Evidence | Severity | Confidence | Impact on AI citation | Fix |
|---|---|---|---|---|---|---|
| Probe | AEO 語意歧義 → AI 回答海關認證／美國服飾品牌 | 4/8 服務商類題目答錯主題；`aeo.customs.gov.tw` 為最高引用網域（13 次） | **Critical** | Confirmed | 直接造成部分 0% | ✅ 已修（08-15，8 題補脈絡）；待重新探測驗證 |
| Content | 首頁完全沒有 AEO/GEO 自我定位 | 08-19 前 title/description/正文皆無；爬蟲 39% 請求集中在首頁 | **Critical** | Confirmed | AI 對品牌的認知 = 社群備份公司 | ✅ 已修（08-19 雙服務線改版 + 首頁 FAQ） |
| Entity | Organization `name` 全站不一致（29 頁法人中文名 vs 11 頁品牌名） | 三種宣告共用同一 `@id` | **High** | Confirmed | OpenAI 查「唄粉智能科技」找不到，誤判為粉體產業 | ✅ 已修（41 頁統一） |
| Retrievability | 核心服務頁幾乎未被抓 | GPTBot/OAI-SearchBot 30 天內 `/aeo-geo` **0 次** | **High** | Confirmed | 內容存在但未進入檢索候選 | 🟡 已推 IndexNow；需持續觀察 |
| Availability | 08-01～03 連續三天近 700 次 521 | crawler log；對應 nginx 啟動期 DNS 事故 | **High** | Confirmed | 爬蟲可能因此降低抓取頻率 | ✅ 事故已修（nginx resolver + Restart=on-failure） |
| External | 無任何第三方來源佐證 | 36 筆未指名回答中 0 筆引用提及 ShellFans 的外部來源 | **High** | **Unknown**（無資料集） | 競品被描述為「有實績案例支撐」 | ❌ 未解，需商業動作 |
| Probe | Category mapping 跨站台污染 | ShellFans 報告出現英語檢定選擇型等 | **High** | Confirmed | 不影響引用率，影響報告可信度 | ✅ 已修（08-15） |
| Product | Crawler 驗證可被 GCP 偽裝 | ASN 396982 的 3,665 筆被標 verified，1,488 筆掃憑證 | **Critical** | Confirmed | 不影響引用率，但灌水監控數據並掩蓋攻擊 | ✅ 已修（本次） |
| Crawlability | robots / WAF / rate limit | 15 支爬蟲 × 4 URL 全部 200 | — | Confirmed | 無影響 | ✅ Pass |
| Structure | 舊頁面缺 H1、階層斷裂、FAQ 與 schema 不一致 | `privacy-policy`/`terms` 無 H1；`helpcenter` H1 錯字且 0 H2/84 H3 | Medium | Confirmed | 次要 | ❌ 未修 |
| Linking | 頁尾 AEO 區無連結指向 `/aeo` hub | 8 條連結中 0 條 | Low | Confirmed | 次要 | ❌ 未修 |

---

## 14. 最後必答

### A. 0% citation 是否可信？

**Yes。**

36 筆未指名回答的全文掃描：品牌名、產品名、網域在內文與引用清單中**全部 0 命中**，
且 0 筆探測失敗。Scorer 的 12 個對照案例全數正確（含 www 正規化、深層路徑帶 query、
Markdown 連結、歧義簡稱需佐證、陰性對照）。

但**必須加上時間限定**：這份 0% 反映的是 **2026-08-12** 的狀態，
早於 26 頁 AEO 叢集（08-14/16）、題目去歧義（08-15）與品牌定位改版（08-19）。

### B. AI crawler 是否有抓到 shell.fans？

**有抓到網站，但沒抓到核心內容。**

- **哪些**：GPTBot、OAI-SearchBot、ChatGPT-User、PerplexityBot、Google-Extended（已驗證）；
  ClaudeBot、Claude-SearchBot、Claude-User、Amazonbot、Meta-ExternalAgent、CCBot、Bytespider（無驗證方法）
- **抓哪些頁**：壓倒性集中在首頁（占 39%），其次 robots.txt、sitemap.xml
- **是否抓核心 AEO/GEO 頁**：**否。GPTBot 與 OAI-SearchBot 在 30 天內從未抓過 `/aeo-geo`。**

### C. 最大問題在哪一層？

**8. Multiple factors** —— 但若必須指出主因，依證據強度排序是：

1. **Probe（AEO 語意歧義）** —— 有直接的回答原文為證
2. **Content relevance（首頁無自我定位）** —— 爬蟲行為與 AI 回答內容互相印證
3. **External authority** —— 標記 Unknown，但競品的差異點指向這裡

### D. Top 5 Root Causes

| # | Root cause | 影響 × 證據 |
|---|---|---|
| 1 | **AEO 語意歧義**：AI 把問題理解成海關認證或美國服飾品牌 | Critical × Confirmed |
| 2 | **首頁與品牌定義句完全沒有 AEO/GEO**，而爬蟲 39% 的請求集中在首頁 | Critical × Confirmed |
| 3 | **核心服務頁未進入檢索候選**：GPTBot/OAI-SearchBot 從未抓過 `/aeo-geo` | High × Confirmed |
| 4 | **無外部來源佐證**，競品被描述為「有實績案例支撐」 | High × Unknown |
| 5 | **Entity fragmentation**：法人中文名當 `name`，OpenAI 誤判為粉體產業 | High × Confirmed |

### E. Top 10 修正項目

| # | 項目 | 優先 | 預期效果 | 難度 | 影響檔案 |
|---|---|---|---|---|---|
| 1 | 題目去歧義（8 題補「答案引擎優化」脈絡） | **P0** | 高 —— 直接消除答錯主題 | 低 | ✅ 已完成（migration 2026-08-15） |
| 2 | 首頁與所有品牌定義句改為雙服務線並列 | **P0** | 高 —— 爬蟲最常抓的就是首頁 | 中 | ✅ 已完成（index.html、what-is-shellfans、llms.txt、llms-full.txt） |
| 3 | Organization `name` 全站統一為品牌名 | **P0** | 中高 —— 修正實體辨識失敗 | 低 | ✅ 已完成（41 頁 + 產生器） |
| 4 | Crawler 驗證移除 googleusercontent | **P0** | 監控資料正確性（不影響引用率） | 低 | ✅ 已完成（verification.ts + 3 測試） |
| 5 | 首頁 FAQ（6 題收合式，涵蓋兩條服務線） | **P0** | 中高 —— 提供可擷取的問答 | 低 | ✅ 已完成（08-19） |
| 6 | **重新探測建立新基準線** | **P1** | 必要 —— 否則無法驗證上述五項 | 低 | 每週排程（週一 09:00）或手動觸發 |
| 7 | 取得可公開的客戶案例／第三方提及 | **P1** | **可能最高**，但非技術工作 | 高 | 商業動作 |
| 8 | 修補舊頁面結構（缺 H1、helpcenter 階層與錯字、fans-analysis 缺 FAQPage） | **P1** | 中 | 低 | `privacy-policy`、`terms`、`helpcenter`、`fans-analysis` |
| 9 | 頁尾 AEO 連結區加入 `/aeo` hub | **P2** | 低中 | 極低 | 全站頁尾區塊 |
| 10 | 競品網站的技術面比較（title/schema/word count/page age） | **P2** | 診斷用，非修正 | 中 | 新增分析腳本 |

---

## 15. Verification Plan

### 已驗證（本次）

| 項目 | 結果 |
|---|---|
| `npm test` | ✅ **130 passed / 0 failed**（新增 3） |
| `tsc --noEmit` | ✅ exit 0 |
| `eslint` | ✅ 無問題 |
| `npm run build` | ✅ Compiled successfully |
| 15 支爬蟲 × 4 核心 URL | ✅ 60/60 皆 200 |
| sitemap 44 條 | ✅ 全部 200 |
| 全站 JSON-LD | ✅ 全部可解析 |
| Organization 一致性 | ✅ 41 頁單一宣告 |
| Citation scorer 陽性對照 | ✅ 12/12 |
| Category mapping | ✅ ShellFans PDF 中其他客戶分類 0 次 |

### 待驗證（需下次探測）

1. **題目去歧義是否讓 AI 回答正確主題** —— 檢查回答中是否仍出現報關行／American Eagle
2. **首頁改版後 AI 是否提到 AEO/GEO** —— 重問「ShellFans 提供哪些服務？」
3. **Entity 統一後 OpenAI 是否找得到唄粉智能科技** —— 重問該題
4. **引用率是否脫離 0%** —— 需累積至少 2 個觀測點才能談趨勢

下次排程探測：**每週一 09:00**（`0 9 * * 1`）。
建議在該次結果出來後，與 2026-08-12 這份基準做對照 ——
但須注意題目文字已於 08-15 變更，屬**量測工具變更**，
已在 `aeo_milestones` 標記，趨勢圖上會看到轉折點。

---

## 16. 需人工確認

1. ~~**法人所在國**~~ —— 已於 2026-08-19 確認為台灣公司，全站清查完成（見第 17 節）。
2. **成立年份**：OpenAI 引用 LinkedIn 稱「成立於 2023 年」，是否正確？若否需更正 LinkedIn。
3. **支援平台清單**：AI 曾稱支援 YouTube／Twitter／小紅書，均不正確。
   08-19 已在首頁 FAQ 明確否定，但各外部平台的簡介是否一致仍需人工檢查。
4. **是否要取得可公開的客戶案例**：這是 Top 5 中唯一無法由工程解決的項目。


---

## 17. 法人名稱清查（2026-08-19）

確認結論：**唄粉智能科技股份有限公司，台灣公司，名稱前不加任何國別前綴。**

### 對外表面：全部清除

| 位置 | 改前 | 改後 |
|---|---|---|
| 18 個公開頁面 | 0 處 | 0 處（先前已清乾淨） |
| `llms-full.txt` | **2 處** | 0 |
| `console.shell.fans/api/site/cofounder` | **1 處** | 0 |

`llms-full.txt` 的兩處原本是「請勿使用某某前綴」的糾正句 —— 用意正確，
但為了寫出這句話就必須寫出那個詞，而 AI 讀到否定句仍可能把詞學進去。
改為**正面陳述**：明確寫出台灣註冊、統編、地址，並說明沒有海外母公司，
糾正功能保留而不出現該字串。

### 兩顆會把舊名寫回去的地雷（已拆）

| 檔案 | 風險 |
|---|---|
| `scripts/apply-unified-footer.py` | 會把 footer 公司名寫進**全站每一頁**，其中寫的是舊名 |
| `scripts/apply-seo-aeo-fixes.py` | 會把 `legalName` 寫進 JSON-LD，其中是舊名 |
| `saas_womm/scripts/deploy-shellfans-pages.sh` + `scripts/shellfans-pages/*.html` | **最危險** —— 直接部署到正式站，而那兩個 HTML 是 2026-04-27 的舊快照 |

三者都已修正名稱，並在檔案頂端加註警告說明正確名稱與後果。
deploy 腳本另加註：shell.fans 的正式來源自 2026-06-08 起已改為獨立 repo，
執行該腳本會用 4 月版本覆蓋正式站並回退之後所有變更。

### 創辦人經歷：保留事實，移除國別前綴

DB `system_settings.cofounder_content` 有 2 處描述創辦人於東京設立法人並擔任代表取締役。
**未刪除任何事實**，僅改用該法人的正式名稱：

- 「現為日商唄粉智能（英語：ShellFans AI，日語：シェルファンズ株式会社）創辦人與負責人、代表取締役」
  → 「現為 ShellFans AI（日語：シェルファンズ株式会社）創辦人與負責人、代表取締役」
- 「於日本東京都設立日商唄粉智能公司（日語：シェルファンズ株式会社）」
  → 「於日本東京都設立シェルファンズ株式会社（ShellFans AI）」

修改前已備份至 `/tmp/cofounder-backup-20260819-121654.json`。

> ⚠️ **仍需你判斷的一點**：創辦人於 2025 年在東京設立 **シェルファンズ株式会社**（與台灣品牌同名）
> 是事實，而本文第 3 節新寫的 llms-full.txt 聲明「台灣公司沒有海外母公司」。
> 兩者不衝突（台灣公司不是被日本公司持有），但**同名**這件事正是 AI 實體辨識容易出錯的來源。
> 若要進一步降低混淆，需要在創辦人頁明確說明兩個法人的關係 —— 那是商業陳述，不由工程決定。

### 未修改：歷史工程紀錄

以下檔案仍含該字串，**刻意不改**：

- `shell.fans-static/docs/reports/seo-aeo-social-backup-discoverability.md`
- `saas_womm/docs/audits/2026-06-06-cofounder-page.md`
- `saas_womm/docs/deploy-reports/shellfans-production-admin-seo-update-20260511-2150.md`

這些是記錄「當時把舊名改成新名」的工程紀錄，內容必然要提到舊名。
改掉等於竄改稽核軌跡，日後就無法得知曾修過什麼。
已確認 `docs/` **未部署到 `/var/www`**（`https://shell.fans/docs/audits/` 回 302），
不會被爬蟲讀到。
