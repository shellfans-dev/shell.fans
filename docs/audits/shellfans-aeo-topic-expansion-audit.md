# ShellFans AEO/GEO 主題頁擴增稽核

日期：2026-08-14
範圍：`shell.fans` 靜態站（repo `shellfans-dev/shell.fans`，部署於 215 `/var/www/shell.fans`）

---

## 1. 現況架構

| 項目 | 現況 |
|---|---|
| Framework | **無**。純靜態 HTML，無 build step、無 SSR/SSG 框架 |
| Routing | nginx `try_files $uri $uri/ $uri.html`，扁平無副檔名網址（`/pricing`、`/aeo-geo/methodology`） |
| Content source | 每頁一份獨立 `.html`，nav / footer / CSS **各自內嵌** |
| 共用 runtime | `js/sf-footer.js`（footer 渲染 + 產品開關隱藏 nav + 登入下拉）、`js/aeo-chat.js`（線上客服） |
| i18n | **實測 7 頁**有 i18n 引擎（`/`、`/aeo-geo`、`/aeo-geo/methodology`、`/aeo-geo/taiwan-aeo-tools`、`/tools/aeo-geo-checker`、`/social-media-backup`、`/what-is-shellfans`），其餘 15 頁為純中文。註：`js/sf-footer.js` 的註解寫「4 頁」，已過時，以實測為準 |
| 部署 | 複製檔案到 `/var/www/shell.fans`，nginx 直接服務 |
| Crawler 可讀性 | **完全 server-rendered**（靜態檔），無 client-side 內容注入。AEO 條件上是最佳形態 |

### 為什麼沒有導入框架

本次不引入 build step。理由：整站 22 頁、無互動狀態、目前 crawler 可讀性已是最佳；導入框架會把「零依賴、零建置、改完即上線」換成一套需要維護的 toolchain，對 AEO 沒有任何增益。改以**產生器腳本**（`scripts/build-aeo-pages.py`）解決重複問題——沿用既有 `scripts/*.py` 冪等修補器的慣例。

---

## 2. 現有 URL Inventory

### 已收錄於 sitemap（18 條，全部 200）

| URL | 主題 | JSON-LD |
|---|---|---|
| `/` | 首頁 | Organization, WebSite, WebPage |
| `/what-is-shellfans` | 品牌實體 hub | Organization, Service, SoftwareApplication, Service, WebPage, FAQPage |
| `/social-media-backup` | 社群備份服務 | Organization, Service, WebPage, FAQPage |
| `/aeo-geo` | **AEO/GEO 代管（商業 hub）** | WebApplication, Service, Organization, FAQPage, BreadcrumbList |
| `/pricing` | 方案價格 | Organization, WebSite, WebPage |
| `/tools/aeo-geo-checker` | **AEO/GEO 檢測工具** | WebApplication, FAQPage, BreadcrumbList |
| `/aeo-geo/methodology` | **AI Readiness Score 方法論** | TechArticle, BreadcrumbList |
| `/aeo-geo/taiwan-aeo-tools` | 台灣 AEO 工具比較 | Article, BreadcrumbList |
| `/co-founder` | 創辦人 | Organization, WebSite, WebPage |
| `/product` | 產品總覽 | Organization, WebSite, WebPage |
| `/price` | 價格（舊） | Organization, WebSite, WebPage |
| `/endurance` | 續航引擎 | Organization, WebSite, WebPage |
| `/fans-analysis` | 粉絲分析 | Organization, WebSite, WebPage |
| `/contact` | 聯繫 | Organization, WebSite, WebPage |
| `/support` | 客服支援 | Organization, WebSite, WebPage |
| `/helpcenter` | 幫助中心 | Organization, WebSite, WebPage |
| `/privacy-policy` | 隱私權 | Organization, WebSite, WebPage |
| `/terms-and-conditions` | 服務條款 | Organization, WebSite, WebPage |

### 未收錄（正確，不應收錄）

`401.html`、`404.html`、`detail_news.html`、`search.html` — 無 JSON-LD、非內容頁。

**sitemap 狀態：完整。** 22 個 HTML 檔扣掉上述 4 個 = 18，與 sitemap 條目數一致。

---

## 3. 缺漏分析

現有 AEO 資產只有 **4 頁**，全部集中在「工具 + 方法論 + 商業服務」。對 AI 模型而言缺的是**語意證據的廣度**：

| 意圖類型 | 現況 | 缺口 |
|---|---|---|
| 定義型（AEO 是什麼／GEO 是什麼） | ❌ 無 | 模型回答「什麼是 AEO」時，站上沒有可引用段落 |
| 比較型（AEO vs SEO／vs GEO） | ❌ 無 | 比較型查詢是 AEO 最高頻的入口 |
| 技術權威（llms.txt、各家 crawler、Schema 類型） | ❌ 無 | 這些是技術決策者實際搜尋的字串 |
| 採購型（費用、導入流程、如何選廠商） | ⚠️ 僅 `/aeo-geo` 段落 | 沒有可獨立被引用的專頁 |
| 在地採購（台灣 AEO 公司） | ⚠️ 僅工具比較頁 | 「台灣 AEO 公司」是最直接的商業查詢，無對應頁 |
| 產業解決方案 | ❌ 無 | 本次不做（見第 8 節） |

---

## 4. 重複與衝突風險

| 風險 | 判定 | 處置 |
|---|---|---|
| `/pricing` vs `/price` | 兩頁並存，皆在 sitemap | **本次不動**。屬產品方案價格，與 AEO 服務費用是不同意圖。新頁用 `/aeo/cost`，不叫 pricing，避免互相稀釋 |
| `/aeo-geo/methodology` vs 提案的 `/ai-readiness/methodology` | **會直接重複** | 見第 5 節決策 |
| `/aeo-geo/taiwan-aeo-tools` vs 提案的 `/aeo/taiwan-companies` | 主題相鄰但不同：**工具** vs **服務商** | 兩頁並存，互相 canonical 分明並雙向連結 |
| `/aeo-geo` vs 提案的 `/aeo/service` | 會重複 | `/aeo-geo` 已是商業 hub 且已被索引；**不建 `/aeo/service`** |
| `/what-is-shellfans` vs 提案的「ShellFans AEO/GEO 是什麼」 | 會重複 | 不新建，改為補強 `/aeo-geo` 與 `/what-is-shellfans` 之間的連結 |

---

## 5. URL 決策：不建立 `/ai-readiness/*` 叢集

Prompt 第二階段 C 提出 8 頁 `/ai-readiness/*`。**決定不建立**，理由：

1. `/aeo-geo/methodology` 已是 AI Readiness Score 方法論的 canonical 頁，已被索引、已在 sitemap、已被叢集內 5 條內部連結指向。搬移或並存都會拆散既有權重。
2. Prompt 明確允許二選一並說明理由。
3. C 群中真正有獨立主題價值的是各面向本身（crawlability、structured data、entity clarity、answer readiness、trust signals）——這些與第二階段 B 群**完全重疊**。改為在 `/aeo/` 下各建一頁，同時滿足 B 與 C，且不製造重複。

`/aeo-geo/methodology` 維持 canonical，不做 redirect。

### ⚠️ AI Readiness Score 權重：Prompt 與實作不符

Prompt 敘述的 8 面向與配分（15/10/10/10/15/15/15/10，含獨立的 Sitemap 與 Trust signals 面向）**與實際程式碼不一致**。實際實作（`saas_womm/src/lib/aeo-geo/scoring.ts`，`SCORING_VERSION = 'aeo_geo_score_v1'`）為：

| 面向 | 配分 |
|---|---|
| crawlability | 15 |
| technical | 15 |
| structuredData | 15 |
| aeoAnswerReadiness | 15 |
| geoEntitySignal | 15 |
| aiCrawlerReadiness | 10 |
| contentClarity | 10 |
| llmsTxt | 5 |
| **合計** | **100** |

沒有獨立的「Sitemap / discoverability」與「Trust signals」面向；sitemap 檢查併入 crawlability，trust 訊號併入 geoEntitySignal。

**依 Prompt 指示「既有程式碼已有權重設定，不要擅自改變」，一律以程式碼為準。** 所有新頁引用配分時使用上表。這點特別重要——網站自己的方法論頁若寫錯自家評分權重，是權威頁最嚴重的錯誤。

**需人工確認**：Prompt 的配分是否代表一個尚未實作的 v2 規劃。若是，應先改 `scoring.ts` 再改文件，不可反向。

---

## 6. 新增 URL 架構

沿用既有 convention（扁平、無副檔名、`/父/子`）。

### Hub

- `/aeo` — AEO/GEO 知識中心（**新 hub**）

與 `/aeo-geo` 的分工，避免 cannibalization：

| | `/aeo-geo` | `/aeo` |
|---|---|---|
| 意圖 | 商業 / 採購 | 知識 / 技術 |
| Funnel | BOFU | TOFU–MOFU |
| Schema | Service + WebApplication | CollectionPage |
| CTA | 立即檢測 / 聯繫 | 導向 `/aeo-geo`、`/tools/aeo-geo-checker` |

### P0（14 項）

| # | Prompt 項目 | URL | 動作 |
|---|---|---|---|
| 1 | AEO 是什麼 | `/aeo/what-is-aeo` | 新增 |
| 2 | GEO 是什麼 | `/aeo/what-is-geo` | 新增 |
| 3 | AEO vs SEO | `/aeo/aeo-vs-seo` | 新增 |
| 4 | AEO vs GEO | `/aeo/aeo-vs-geo` | 新增 |
| 5 | ShellFans AEO/GEO 是什麼 | `/aeo-geo` | **既有，補強連結** |
| 6 | AI Readiness Score | `/aeo-geo/methodology` | **既有，補強連結** |
| 7 | Score 方法論 | 同上 | 合併（同一頁） |
| 8 | AEO Managed Hosting | `/aeo/managed-hosting` | 新增 |
| 9 | AEO 顧問服務 | `/aeo/consulting` | 新增 |
| 10 | AEO 費用 | `/aeo/cost` | 新增 |
| 11 | AEO 導入流程 | `/aeo/implementation` | 新增 |
| 12 | 台灣 AEO 公司 | `/aeo/taiwan-companies` | 新增 |
| 13 | 如何選 AEO 公司 | `/aeo/how-to-choose-agency` | 新增 |
| 14 | AEO 公司 vs SEO 公司 | `/aeo/aeo-agency-vs-seo-agency` | 新增 |

### P1（11 項）

`/aeo/llms-txt`、`/aeo/llms-full-txt`、`/aeo/ai-crawler`、`/aeo/gptbot-oai-searchbot`、`/aeo/claudebot`、`/aeo/perplexitybot`、`/aeo/schema`、`/aeo/faq-schema`、`/aeo/entity-clarity`、`/aeo/answer-readiness`、`/aeo/trust-signals`

**新增合計：1 hub + 11 (P0) + 11 (P1) = 23 頁**

---

## 7. Routing 陷阱與根因修正

### 問題

nginx `try_files $uri $uri/ $uri.html` 中 `$uri/` 排在 `$uri.html` 之前。當同時存在 `foo.html` 與 `foo/` 目錄時，`/foo` 會先命中目錄；目錄沒有 `index.html` 就回 **403**。

這已經發生過一次——現行設定裡有一段專門的繞道：

```nginx
location = /aeo-geo { try_files /aeo-geo.html =404; }
```

本次要新增 `/aeo` hub 與 `/aeo/` 目錄，會複製同一個問題。

### 實測

| 方案 | 結果 |
|---|---|
| 目錄放 `index.html` | `/aeo` **301 → `/aeo/`**，與全站無斜線慣例不符，且多一跳 |
| `location =` 例外 | 可行，但每個 hub 都要加一條，是在累積技術債 |
| **調換 try_files 順序** | `$uri.html` 提前到 `$uri/` 之前，一次消除整類問題 |

### 採用

```nginx
try_files $uri $uri.html $uri/ @home_redirect;
```

`/` 不受影響（`/.html` 不存在，落到 `$uri/` → `index.html`）。`/downloads/agent/` 同理。既有 `location = /aeo-geo` 保留不動——它同時承擔 cache header 職責，而 nginx 的 `add_header` 不是疊加的。

---

## 8. 本次不做的項目

| 項目 | 原因 |
|---|---|
| 產業解決方案 `/solutions/aeo/*`（7 頁） | Prompt 第八階段允許先做 P0+P1。產業頁若只換名詞就是薄內容，而真正有差異的 use case 需要真實客戶資料——目前只有 1 家 AEO 客戶（師德），寫 7 個產業會變成虛構 |
| `/aeo/geo-vs-seo`、`/aeo/how-ai-search-works`、`/aeo/answer-engine-optimization-guide` | A 群非 P0/P1 項目，第二批 |
| `/aeo/agency`、`/aeo/consultant`、`/aeo/in-house-vs-agency`、`/aeo/tools-vs-service` | E 群非 P0/P1 項目，第二批 |
| `/aeo/organization-schema`、`/aeo/product-schema`、`/aeo/service-schema` | B 群非 P0/P1，且與 `/aeo/schema` 有重疊風險，第二批時需先確認切分 |
| `/about/*`、`/research`、`/changelog` | 既有 `/contact`、`/co-founder`、`/what-is-shellfans` 已承擔 entity/trust 職責，新增會重複 |
| `/aeo/website-hosting` | 與 `/aeo/managed-hosting` 同義，只會 cannibalize |
| `/aeo/audit` | 與 `/tools/aeo-geo-checker` 重疊，第二批再評估是否需要「人工稽核 vs 自動檢測」的區隔頁 |

---

## 9. 需人工確認的商業資訊

以下在 repo 中查無可驗證來源，頁面一律以保守描述處理，**不捏造數字**：

1. **AEO 服務實際售價** — `/aeo/cost` 以「依網站規模與導入範圍評估」描述，並列出影響價格的變數。價格 placeholder 集中在產生器的 `PRICING_PLACEHOLDER`，日後填入即可。
2. **導入週期實際天數** — `/aeo/implementation` 以階段與交付物描述，不寫保證天數。
3. **台灣其他 AEO 服務商名單** — `/aeo/taiwan-companies` **不列競品名稱**，改為提供可驗證的評估準則。列名需人工確認後補。
4. **客戶案例** — 目前僅 1 家 AEO 客戶，未取得露出授權，全站不提及。
5. **AI Readiness Score 權重 v2** — 見第 5 節。

---

## 10. 實作結果

### 新增 URL（23 條，全部已上線並回應 200）

Hub：`/aeo`

A. 定義與比較（4）：`/aeo/what-is-aeo`、`/aeo/what-is-geo`、`/aeo/aeo-vs-seo`、`/aeo/aeo-vs-geo`

B. 技術權威（11）：`/aeo/ai-crawler`、`/aeo/gptbot-oai-searchbot`、`/aeo/claudebot`、`/aeo/perplexitybot`、`/aeo/llms-txt`、`/aeo/llms-full-txt`、`/aeo/schema`、`/aeo/faq-schema`、`/aeo/entity-clarity`、`/aeo/answer-readiness`、`/aeo/trust-signals`

D+E. 商業與採購（7）：`/aeo/managed-hosting`、`/aeo/consulting`、`/aeo/cost`、`/aeo/implementation`、`/aeo/taiwan-companies`、`/aeo/how-to-choose-agency`、`/aeo/aeo-agency-vs-seo-agency`

完整對照見 `docs/audits/shellfans-aeo-topic-map.md`。

### 修改的既有 URL（5 條，只加內部連結，未改內容）

`/aeo-geo`、`/aeo-geo/methodology`、`/aeo-geo/taiwan-aeo-tools`、`/tools/aeo-geo-checker` 各在既有的
`sf-inline-links` 區塊追加一條指向 `/aeo` 的連結（錨文字每頁不同）。
`/what-is-shellfans` 原本沒有該區塊，改為在 `</main>` 前插入一個「延伸閱讀」區塊。

### 新增檔案

| 檔案 | 用途 |
|---|---|
| `scripts/aeo_pages_content.py` | 23 頁內容的單一事實來源 |
| `scripts/build-aeo-pages.py` | 從既有頁面抽取外殼並產生頁面（冪等） |
| `scripts/link-aeo-hub.py` | 既有頁面回指 hub（冪等） |
| `docs/audits/shellfans-aeo-topic-map.md` | Topic map（由內容模組產生） |

### Redirect / canonical 決策

**沒有建立任何 redirect。** 本次全部是新增 URL，沒有搬移既有頁面。
`/aeo-geo/methodology` 維持 canonical，未遷移至 `/ai-readiness/methodology`（理由見第 5 節）。
每頁 canonical 指向自身，並附 `hreflang="zh-Hant"` 與 `x-default`。

### sitemap 變更

新增 23 條，總數 18 → 41。優先度：hub 0.90、商業／採購頁 0.80、知識頁 0.70。
`lastmod` 一律 2026-08-14。XML 可解析，無重複 URL。

### llms.txt 變更

新增 `## AEO/GEO knowledge cluster` 章節，逐頁列出並說明各頁回答什麼問題，
並在 `## Citation hint` 補上知識叢集的指路。`Last-Updated` 更新為 2026-08-14。
102 → 140 行。`llms-full.txt` 本次未改動。

### Schema 變更

每個新頁的 JSON-LD 採 `@graph`，包含 4 個節點：

1. `Organization` — **與 `index.html` 的宣告逐欄一致**（含 taxID、alternateName、sameAs）
2. 主節點 — `CollectionPage`（hub）／`Service`（2 頁服務頁）／`TechArticle`（其餘 20 頁）
3. `BreadcrumbList`
4. `FAQPage` — 23 頁全部具備，且 schema 中的問答與頁面上 `<details>` 可見內容完全一致

`author` / `publisher` / `provider` 一律以 `@id` 指向 Organization 節點，不重複內嵌宣告。

### 內部連結變更

- hub → 22 個子頁（23 條連結）
- 每個子頁 → 4 條相關頁面 + 2 個 CTA
- 5 個既有頁面 → hub
- 新頁面內部連結總計 43 條不重複 URL，**全部驗證回應 200**

---

### ⚠️ 連帶修復：檢測工具的 `@graph` 解析 bug（saas_womm）

驗證新頁面時，用自家 checker 檢測 `/aeo/what-is-aeo`，回報「有 FAQ 文案但缺 FAQPage schema」——
但該頁確實有 FAQPage。追查後確認是 **產品 bug**，不是頁面問題。

`src/lib/aeo-geo/scanner.ts` 的 `analyzeHtml()` 只讀 JSON-LD 最上層的 `@type`，
**不會進入 `@graph`**。而 `@graph` 正是 schema.org 建議用來表達多個關聯節點的寫法，
使用極為普遍——shell.fans 自己 16 個頁面都是這樣寫的。

影響範圍：所有採用 `@graph` 的受檢網站，其 Structured Data（15 分）與
Entity Clarity（15 分）被系統性低估，且會收到「缺 Organization schema」這種與事實相反的建議。

修復：新增 `collectJsonLdTypes()` 遞迴進入 `@graph`。刻意**不**遍歷任意巢狀物件——
`publisher`、`author` 裡的 Organization 是「引用」而非「本頁宣告的實體」，
算進去會讓幾乎每頁都看起來有 Organization，反而失去鑑別力。

新增 5 個單元測試（`src/lib/aeo-geo/__tests__/scanner-jsonld.test.ts`）涵蓋：
最上層 `@type` 回歸、`@graph` 內節點、巢狀引用不計、`@type` 為陣列、JSON 損壞不拋例外。

**⚠️ 這是量測工具的變更。** 採用 `@graph` 的網站，本次修復後分數會上升，
與修復前的歷史分數<strong>不可直接比較</strong>。任何跨此時間點的趨勢圖都需標記此變更。

---

## 11. 驗證結果

| 項目 | 結果 |
|---|---|
| 產生器自檢（每頁 H1 恰 1 個、JSON-LD 可 parse、無 `data-i18n` 殘留） | ✅ 23/23 |
| 每頁內部連結 ≥3 | ✅ 23/23 |
| 新頁面內部連結可達性（43 條不重複 URL） | ✅ 全部 200 |
| 新增 URL 線上回應 | ✅ 23/23 皆 200 |
| 既有 URL 回歸（18 條基準矩陣，nginx 改動前後比對） | ✅ 完全一致，零回歸 |
| 線上 server-rendered 內容（不依賴 JS） | ✅ 抽驗 4 頁，正文 1,992–2,905 字皆在 HTML 原始碼中 |
| 線上 JSON-LD 可解析 | ✅ 抽驗 3 頁，節點型別正確 |
| sitemap.xml XML 驗證 | ✅ 41 條，無重複 |
| `nginx -t` | ✅ syntax ok |
| saas_womm `npm test` | ✅ 69 passed / 0 failed |
| saas_womm `tsc --noEmit` | ✅ exit 0 |
| saas_womm `eslint`（本次異動檔案） | ✅ 無新增問題（scanner.ts 既有 3 個 `prefer-const` 錯誤在 HEAD 即存在，未一併處理以免混淆 diff） |
| saas_womm `npm run build` | ✅ Compiled successfully |
| 自家 checker 實測新頁面 | ✅ `/aeo/what-is-aeo` 與 `/aeo/managed-hosting` 皆 **100 分、0 待修** |

### 關於那個 100 分

先前曾移除「自家網域直接滿分」的捷徑。本次已確認該捷徑確實不存在——
`isSelfDomain` / `SELF_DOMAINS` 在 `scoring.ts` 中已無任何符合，
`perfectScore()` 函式雖仍留著但**沒有任何呼叫者**（死碼）。因此 100 分是實際計分結果。

### 未執行的驗證

| 項目 | 原因 |
|---|---|
| Playwright / Cypress smoke test | 本 repo 為純靜態站，未安裝任何測試框架 |
| 行動版版面實測 | 無瀏覽器環境。已確認新頁沿用 donor 的 `<style>` 與 `viewport` meta，CSS 與既有 RWD 頁面完全相同 |
| 對照組網域檢測 | 檢測時撞到匿名每日 5 次額度（額度機制本身運作正常） |

## 12. 品質與風險控制自查

| 禁止項目 | 自查 |
|---|---|
| 只換關鍵字的薄頁 | ✅ 每頁內容獨立撰寫，正文 2,000–2,900 字，含各自的限制與常見錯誤章節 |
| 捏造客戶案例／數據／品牌／獎項 | ✅ 全站無任何客戶名稱、數據或案例 |
| 捏造 AI 平台引用率 | ✅ 無任何引用率數字 |
| 宣稱 llms.txt／Schema 保證 AI 推薦 | ✅ 相反——`/aeo/llms-txt` 明文寫出「目前不是標準，無任何主要 AI 業者公開承諾讀取」 |
| 重複 canonical 頁 | ✅ 刻意不建 `/ai-readiness/*` 與 `/aeo/service`（見第 4、5 節） |
| 破壞既有功能 | ✅ 18 條 URL 基準矩陣零回歸；checker 為修復非破壞 |
| 捏造價格 | ✅ `/aeo/cost` 不列數字，僅說明影響報價的變數 |
| 列出競品／排名 | ✅ `/aeo/taiwan-companies` 明文說明不列名單的兩個理由 |
