# CET 案例頁 — 內部驗證摘要與公開揭露分級

**日期**：2026-09-08
**目的**：在製作公開案例頁之前，先把「哪些能講、哪些不能講」定死。
**存放位置**：`docs/`（部署時由 rsync `--exclude='docs'` 排除，不會公開）

---

## 結論先講：這是「專案進度案例」，不是「成效案例」

任務允許在證據不足時改發進度案例。經查證，**證據確實不足以支撐一個乾淨的
before/after 成效宣稱**，主因是量測工具在期間內變動了兩次。

---

## 致命問題：量測工具三度變更，baseline 不可比

| 日期 | Claude 模型 | OpenAI 模型 | 平台組合 |
|---|---|---|---|
| 08-07（原始 baseline） | **claude-sonnet-5** | gpt-4o-mini-search-preview | +gemini(全失敗)、+google_aio |
| 08-12 | **claude-haiku-4-5** | gpt-4o-mini-search-preview | openai + anthropic |
| 08-17 | claude-haiku-4-5 | gpt-4o-mini-search-preview | openai + anthropic |
| 08-24 | claude-haiku-4-5 | **全部失敗 0/38**（模型下架） | 實質僅 anthropic |
| 08-27 | claude-haiku-4-5 | **gpt-5-search-api** | openai + anthropic |
| 08-31 | claude-haiku-4-5 | gpt-5-search-api | openai + anthropic |
| 09-07 | claude-haiku-4-5 | gpt-5-search-api | openai + anthropic |

**08-07 的 baseline 用的是 claude-sonnet-5**，之後全部改用能力較弱的
haiku-4-5；OpenAI 側則在 08-27 從 gpt-4o-mini-search-preview 換成
gpt-5-search-api（前者被 OpenAI 下架，08-24 那輪 38 題全失敗）。

**因此「9% → 19%」這種跨越 08-07 到 09-07 的說法不可發布。**
那個差值裡混合了三種東西：網站實際改善、模型換代、以及平台組合變動。
無法拆解，就不能宣稱。

### 唯一可比的區間

08-27、08-31、09-07 這三個點共用同一組量測條件
（claude-haiku-4-5 + gpt-5-search-api）：

| 日期 | 提及率 | 引用率 | 歸因缺口 |
|---|---|---|---|
| 08-27 | 13% | 16% | 3% |
| 08-31 | 16% | 22% | 6% |
| 09-07 | 19% | 28% | 9% |

三點單調上升。但**只有 3 個點、跨 11 天**，且 19% 對應約 14/76 題、
13% 對應約 10/76 題——差距約 4 題。以這個樣本量，不足以區分真實改善與
一般波動。可以說「觀察到上升」，不能說「已證實提升」。

---

## A. 已驗證事實（可公開）

| 事實 | 來源 | 揭露分級 |
|---|---|---|
| 專案起始日 2026-08-05 | `monitored_sites.aeo_project_start_date`（非推斷） | PUBLIC_EXACT |
| 四個 AEO 目標頁已上線並回 200 | 線上 curl | PUBLIC_EXACT |
| 各頁結構：1×h1、8–10×h2、9–11×h3 | 線上 HTML 解析 | PUBLIC_EXACT |
| 各頁具 JSON-LD：Organization、WebSite、WebPage、BreadcrumbList、FAQPage | 線上解析 | PUBLIC_EXACT |
| 各頁自我 canonical | 線上解析 | PUBLIC_EXACT |
| robots.txt / sitemap.xml / llms.txt / llms-full.txt 皆 200 且中文完整 | 線上 curl + 編碼檢查 | PUBLIC_EXACT |
| 目標頁自 2026-08-28 起被 AI 爬蟲抓取 | `crawler_access_logs` | PUBLIC_EXACT |
| 每頁被 6–7 種不同 AI 爬蟲抓取 9–12 次 | 同上 | PUBLIC_EXACT |
| 站台共觀察到 10 種 AI 爬蟲身分 | 同上 | PUBLIC_EXACT |
| AI 回答引用了官網多個網址，含新建的 `/kids-english-test-comparison` | AI 能見度探測 09-07 | PUBLIC_EXACT |
| 最新一輪有 11 題「引用官網但未提品牌」 | 同上 | PUBLIC_EXACT |
| AI 爬蟲請求 36.2% 得到 404、35.5% 得到 200 | `crawler_access_logs` | PUBLIC_PERCENTAGE |
| 404 集中於舊版 `.asp` 路徑 | 同上 | PUBLIC_DIRECTIONAL |

## B. 衍生計算（可公開，但必須標明條件）

| 計算 | 條件 | 揭露分級 |
|---|---|---|
| 同一量測條件下三次觀測：提及 13%→16%→19% | 僅 08-27～09-07，claude-haiku-4-5 + gpt-5-search-api | PUBLIC_PERCENTAGE（**必須同時標示模型與期間**） |
| 同上：引用 16%→22%→28% | 同上 | PUBLIC_PERCENTAGE（同上） |
| 各主題分類的提及／引用率 | 09-07 單輪 | PUBLIC_PERCENTAGE |
| 平台差異：ChatGPT 缺口 −13%、Claude +32% | 09-07 單輪 | PUBLIC_PERCENTAGE |

## C. 方向性觀察（可公開，需用「觀察到」措辭）

- 同一量測條件的三次觀測中，提及率與引用率皆呈上升
- 歸因缺口集中在 Claude；ChatGPT 為負值（提及多於引用），兩平台問題方向相反
- 新建目標頁自上線後持續被多種 AI 爬蟲抓取

## D. 證據不足（**不得**以正面主張發布）

| 項目 | 為什麼不足 |
|---|---|
| 08-07 → 09-07 的任何比較 | 跨越兩次模型變更＋一次平台組合變動 |
| 「AI 爬蟲造訪較專案前增加」 | **沒有專案前資料**——監測與專案同日（08-05）開始 |
| 四個新頁「造成」能見度提升 | 僅有時間相關性，11 天、3 個資料點，無法建立因果 |
| 任何名次、市佔、招生、營收、詢問量 | 完全未量測 |
| 「已被 ChatGPT 推薦」 | 探測看到的是引用，不是推薦；且不穩定 |

## PRIVATE（不公開）

- 完整探測題庫（38 題原文）——屬 ShellFans 的方法論資產，只公開分類
- 客戶後台識別碼、GA4/GSC 帳號識別碼
- 原始 access log（含 IP）
- 客戶內部業務數字（本專案未取得，亦不需要）

---

## 案例頁必須明說的三件事

1. **量測工具在期間內變更過**，因此不做跨期比較，只呈現同一條件下的三次觀測
2. **爬蟲造訪 ≠ 引用 ≠ 提及品牌**，三者分開呈現
3. **仍待改善**：36% 的 AI 爬蟲請求打到 404；歸因缺口在 Claude 上仍達 32%；
   「學校與機構合作型」主題目前提及與引用皆為 0%
