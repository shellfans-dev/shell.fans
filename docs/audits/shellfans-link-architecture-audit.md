# shell.fans Internal / External / Authority Link Architecture Audit

日期：2026-08-21
範圍：44 個可索引 HTML 頁、546 條正文連結、9 篇 Meet 報導、6 個外部來源
性質：**唯讀稽核，未修改任何檔案**
附件：`internal-link-graph.json`、`external-authority-map.json`

---

## 1. Executive Summary

**內鏈架構大致健康，外鏈架構幾乎不存在。**

| 面向 | 判定 |
|---|---|
| Internal linking | 🟢 良好 —— 無語意 anchor **0 次**、AEO 叢集雙向連結成立、pillar inbound 40 條 |
| Click depth | 🟡 7 個 AEO 頁在深度 4（目標 ≤3） |
| Orphan pages | 🔴 **2 頁**（`/price`、`/product`）—— 在 sitemap 但零 inbound、從首頁走不到 |
| External links | 🔴 **只有 3 個外部網域**（TIPO / FB / IG），全部只在 footer |
| External authority | 🔴 **LinkedIn、Medium、Meet、USPTO 全部沒有連結** |
| Entity 交叉佐證 | 🔴 **9 篇 Meet 報導中，提到 AEO/GEO 的：0 篇** |

**最重要的單一發現**：Meet 31048「從『數位佃農』到『有專利』：唄粉智能技術獲美國認證」
明確寫出 `US 12,657,246`、記載「美國專利商標局審查核准」，並回連 `shell.fans/` 與
`/what-is-shellfans`。這是**現成的、第三方的美國專利佐證**，而我們的網站到 08-21 之前
還在頁尾寫「申請中美國專利」。**這篇文章一直存在，我們卻沒有連過去。**

---

## 2. Crawled Pages

44 頁（排除 401/404/search/detail_news）。完整資料見 `internal-link-graph.json`。

| Page Type | 頁數 | 代表 URL |
|---|---|---|
| Pillar | 2 | `/aeo-geo`、`/aeo` |
| AEO Cluster | 26 | `/aeo/*` |
| AEO 既有 | 3 | `/aeo-geo/methodology`、`/aeo-geo/taiwan-aeo-tools`、`/tools/aeo-geo-checker` |
| 品牌／公司 | 3 | `/`、`/what-is-shellfans`、`/co-founder` |
| 產品／服務 | 5 | `/endurance`、`/fans-analysis`、`/social-media-backup`、`/product`、`/price` |
| 價格 | 1 | `/pricing` |
| 支援 | 3 | `/support`、`/helpcenter`、`/contact` |
| 法務 | 2 | `/privacy-policy`、`/terms-and-conditions` |
| **Case Study** | **0** | **不存在** |
| **Patent / Technology 專頁** | **0** | **不存在** |

連結總量：正文 546、nav 373、footer 748。

---

## 3. Internal Link Architecture

### 3.1 Internal Link Score（0–100）

計分：正文 inbound（≤30）+ nav/footer inbound（≤15）+ click depth（≤25）
+ 對外連結數（≤15）+ 是否回連 pillar（15）。orphan 上限 10。

**前段**

| URL | Score | 正文 inbound | depth |
|---|---|---|---|
| `/` | 100 | — | 0 |
| `/aeo-geo` | **99** | 40 | 1 |
| `/aeo` | 85 | 13 | 2 |
| `/tools/aeo-geo-checker` | 84 | **69** | 1 |
| `/aeo-geo/methodology` | 82 | 26 | 2 |
| `/what-is-shellfans` | 79 | 8 | 1 |

**後段（Score < 40，internal authority 過低）**

| URL | Score | 正文 inbound | depth |
|---|---|---|---|
| `/aeo/perplexitybot` | 39 | 3 | 4 |
| `/aeo/claudebot` | 36 | 2 | 4 |
| `/aeo/aeo-agency-vs-seo-agency` | 35 | 2 | 4 |
| `/aeo/llms-full-txt` | 33 | 2 | 4 |
| `/aeo/do-i-need-aeo` | 33 | 1 | 3 |

### 3.2 只靠 nav/footer、正文 inbound 為 0

`/co-founder`、`/helpcenter`、`/support`、`/privacy-policy`、`/terms-and-conditions`

其中 **`/co-founder` 值得注意** —— 它是唯一承載創辦人 Entity 的頁面，
卻沒有任何一頁在正文中連向它。

---

## 4. Orphan Pages

| URL | Title | inbound | depth | sitemap | 優先 |
|---|---|---|---|---|---|
| `/product` | 產品總覽（69 個 H2） | **0** | ∞ | ✅ 收錄 | **P0** |
| `/price` | 價格（舊版） | **0** | ∞ | ✅ 收錄 | **P1** |

兩頁都在 sitemap 但**從首頁完全走不到**。

- `/product`：內容量大（69 個 H2）卻沒有任何入口 —— **P0**，應從 nav 或 `/what-is-shellfans` 連入
- `/price`：與 `/pricing`（Score 67、9 條正文 inbound）內容重疊 —— **P1**，
  建議判定何者為 canonical，另一者 301 或移出 sitemap

> AEO Knowledge pages、FAQ、technical pages、`/what-is-shellfans`
> **皆無 orphan**（規格特別要求檢查的項目）。

---

## 5. Click Depth

| 目標 | 現況 | 判定 |
|---|---|---|
| 核心服務頁 ≤ 2 | `/aeo-geo` 1、`/aeo/managed-hosting` 1 | ✅ |
| `/what-is-shellfans` ≤ 2 | **1** | ✅ |
| 重要 AEO Topic ≤ 3 | 19/26 在 ≤3 | 🟡 |
| Case Study ≤ 3 | 不存在 | ❌ |

**深度 4 的 7 頁**：`faq-schema`、`gptbot-oai-searchbot`、`trust-signals`、
`perplexitybot`、`aeo-agency-vs-seo-agency`、`claudebot`、`llms-full-txt`

成因：它們只被同層 cluster 頁引用，`/aeo` hub 的導覽清單未涵蓋全部 26 頁。

---

## 6. Anchor Text Audit

### 正文連結：✅ 通過

| 檢查 | 結果 |
|---|---|
| 「了解更多／查看更多／點這裡／Read more」 | **0 次** |
| 不重複 anchor | 136 種 / 537 條 |
| exact match 過度集中 | 無 —— 最高頻是 CTA 而非主題詞 |

最常用：`免費檢測我的網站`(27)、`免費檢測工具`(24)、`了解 AEO Managed Hosting`(21)、
`AI 爬蟲總覽`(15)、`實體清晰度`(12) —— **皆具語意**。

### 🟡 例外：`/helpcenter` 的佔位連結

| Anchor | 次數 | href |
|---|---|---|
| `❯` | 84 | `#` |
| `敬啟期待` | 45 | `#` |

全部指向 `#`，是未完成的 UI 佔位。不影響其他頁面，但該頁對爬蟲而言有 129 條無意義連結。

---

## 7. AEO/GEO Topic Cluster Connectivity

### `/aeo-geo`（Pillar）→ Cluster

正文 outbound 僅 **4 條**，inbound 卻有 **40 條**。
典型的「大家都連向它、它很少連出去」——pillar 應該是雙向樞紐。

### Cluster → Pillar：✅ 大致成立

26 頁中 **23 頁**有回連 `/aeo-geo` 或 `/aeo`。

**未回連任何 pillar 的 3 頁**：`/aeo/consulting`、`/aeo/cost`、`/aeo/do-i-need-aeo`

### 規格要求的連結是否存在

| `/aeo-geo` 應連到 | 現況 |
|---|---|
| What is AEO | 🟡 經由 `/aeo` hub 間接 |
| What is GEO | 🟡 間接 |
| SEO vs AEO vs GEO | ❌ **該頁不存在**（僅有 aeo-vs-seo、aeo-vs-geo 兩頁） |
| AI Visibility | ❌ **該頁不存在** |
| AI crawler | 🟡 間接 |
| structured data | 🟡 間接 |
| FAQ | ✅ 頁內 FAQPage |
| service | ✅ |
| **case studies** | ❌ **不存在** |

---

## 8. Navigation / Footer

| 位置 | 連結數/頁 | 內容 |
|---|---|---|
| Header nav | 8–9 | AEO/GEO 代管、續航引擎、粉絲分析、口碑行銷（runtime 隱藏）、查看方案、Klog、登入 |
| Footer | 17 | 產品 4、資源 3、聯繫 3、法務 2、社群 2、專利 1、公司資訊 |
| Footer AEO 連結區 | 8 | 全部指向 `/aeo-geo` 及其 fragment |

| 檢查 | 結果 |
|---|---|
| AEO/GEO 在全站可見 | ✅ nav 有 |
| What is ShellFans 在 nav | ❌ **不在** —— 僅 8 條正文 inbound |
| About / Contact | ✅ footer |
| **Patent / Technology** | 🟡 footer 只有一行專利文字 + TIPO 連結，**無專頁** |
| 是否把 30 個 AEO 頁塞 footer | ✅ **否** —— footer 只有 8 條且都指向 hub |

> Footer 的 8 條 AEO 連結中有 3 條是 `/aeo-geo#dimensions`、`#managed-service`、`#plans`
> —— 同一頁的三個 fragment，稀釋了連結多樣性；且**沒有一條指向 `/aeo` 知識中心**。

---

## 9. External Links

**全站只有 3 個外部網域，且全部只出現在 footer。**

| 網域 | 次數 | 位置 | rel |
|---|---|---|---|
| `tiponet.tipo.gov.tw` | 44 | footer | `noopener noreferrer` |
| `www.facebook.com` | 44 | footer | `noopener noreferrer` |
| `www.instagram.com` | 44 | footer | `noopener noreferrer` |

子網域（同品牌，非第三方）：
`console.shell.fans` 104、`app.shell.fans` 95、`blog.shell.fans` 89。

### rel Audit

| 檢查 | 結果 |
|---|---|
| `noopener noreferrer` 於 `_blank` | ✅ 全部有 |
| 不當 `nofollow` | ✅ **0 次** —— editorial citation 未被 nofollow |
| `sponsored` / `ugc` 誤用 | ✅ 0 次 |

### 缺席的外部來源

| 來源 | 站上連結 | 實測狀態 |
|---|---|---|
| `blog.shell.fans` | ✅ 89 次 | 200「Home - ShellFans 官方部落格」 |
| **LinkedIn** | ❌ **完全沒有** | **200**「ShellFans AI Technology Co., Ltd.」 |
| **Medium（創辦人）** | ❌ 沒有 | 403（Cloudflare 擋伺服器端，**無法驗證**） |
| **Meet 創業小聚** | ❌ 沒有 | 9 篇皆 200 |
| **USPTO** | ❌ 沒有 | 未建立 |

---

## 10. Social Links

| 平台 | 站上使用的 URL | 使用者提供的 URL | 狀態 |
|---|---|---|---|
| Facebook | `facebook.com/profile.php?id=61581243232686` | `facebook.com/shellfans.fans` | 兩者伺服器端皆回 **400** |
| Instagram | `instagram.com/shell_fansai/` | — | footer 44 次 |
| LinkedIn | **無** | `linkedin.com/company/shellfans/` | **200 ✅** |

> ⚠️ **Facebook 的 400 不代表連結失效** —— Facebook 對非瀏覽器請求routinely 回 400。
> 兩個 URL 都需要**用瀏覽器人工確認**哪一個是官方頁面，我無法從伺服器端判定。
> 若 vanity URL 有效，它比 `profile.php?id=` 更適合作為 Entity source（可讀、穩定）。

### Organization `sameAs` 現況

```json
"sameAs": ["https://www.facebook.com/profile.php?id=61581243232686",
           "https://www.instagram.com/shell_fansai/",
           "https://console.shell.fans", "https://blog.shell.fans"]
```

**缺 LinkedIn** —— 那是 B2B 場景中最重要的公司身分來源，且實測 200。

---

## 11. Founder Medium

| 檢查 | 結果 |
|---|---|
| 站上連結 | ❌ 無 |
| 伺服器端驗證 | 403（Cloudflare），**無法確認內容** |
| `/co-founder` 是否有 Person schema | ❌ **完全沒有 Person schema** |

**建議放置**：`/co-founder` 的 `Person.sameAs`，**不放** `Organization.sameAs`
（個人技術 Blog 不是公司身分來源，混入會造成 Entity 混淆）。

前置條件：需先確認該 Medium 帳號確實是黃睿麒本人且身分一致 —— 我無法從伺服器端驗證。

---

## 12. Meet Media Citation Audit

9 篇全部 **HTTP 200**（需 cookie jar，否則會進入無限重導）。

| ID | Title | ShellFans | 唄粉 | 創辦人 | 專利 | AEO/GEO | 回連 | 分類 | 價值 |
|---|---|---|---|---|---|---|---|---|---|
| **31048** | 從「數位佃農」到「有專利」：唄粉智能技術獲美國認證 | 10 | 14 | 0 | **15** | 0 | **2** | **Patent Citation** | **最高** |
| **30453** | 社群帳號說沒就沒？…推 ShellFans AI | **36** | 12 | 0 | 0 | 0 | 1 | Product Citation | 高（**有風險**） |
| **30514** | 2025 停權潮升溫：創作者如何奪回內容所有權？ | 10 | 2 | 0 | 0 | 0 | 1 | Product Citation | 中高 |
| 30481 | 數位足跡，妥善守護：瞭解唄粉智能的創新策略 | 6 | 11 | 0 | 0 | 0 | 1 | Brand Citation | 中 |
| 19206 | 從零開始！「網紅學院」強勢登場 | 6 | 14 | **1** | 0 | 0 | 0 | Founder / Historical | 低 |
| 30377 | 暑假不打工…校園星探計畫精彩落幕 | 6 | 14 | 0 | 0 | 0 | 0 | Historical | 低 |
| 20354 | 「網紅學院」第三集課程上線 | 6 | 16 | 0 | 0 | 0 | 0 | Historical | 低 |
| 30463 | 洞悉AI時代新機遇！創作者分享會圓滿成功 | 6 | 10 | 0 | 0 | 0 | 0 | Historical | 低 |
| 19770 | 從一本60年代的縫紉書到國際品牌 | 6 | 2 | 0 | 0 | 0 | 0 | **Irrelevant** | 極低 |

`meet.bnext.com.tw/blog/list?page=31` —— 列表頁，**確認不應作為 citation**（使用者判斷正確）。

### 三個關鍵結論

**① 31048 是目前最有價值的第三方佐證，而我們沒有連過去**

明確寫出 `US 12,657,246`、記載「通過美國專利商標局審查核准——跨國雙重認證」，
並回連 `shell.fans/` 與 `/what-is-shellfans`。

**② 30453 帶有錯誤的實體宣稱**

ShellFans 提及最多（36 次），但**標題與內文含「日商唄粉智能科技」共 8 次** ——
正是我們在 08-19 全站移除的寫法。引用它等於把錯誤的國別宣稱一起帶進來。

> 這不代表不能引用，但如果要引用，**必須在自己的頁面上同時陳述正確的法人資訊**，
> 讓 AI 有對照依據。或先聯繫 Meet 請求更正。

**③ 9 篇全部 0 次提到 AEO/GEO**

**沒有任何第三方來源佐證「ShellFans 做 AEO/GEO」。** 這與 08-19 稽核的結論一致 ——
競品被 AI 描述為「有實績案例支撐」，我們沒有。

### Google redirect URL

✅ **站上目前沒有任何 `google.com/url?` 連結**（因為根本沒有 Meet 連結）。
未來加入時必須直接用 canonical URL。

---

## 13. Patent / Public Evidence Links

| 專利 | 站上文字 | 站上連結 | 第三方佐證 |
|---|---|---|---|
| TWI908295B | ✅ footer 44 頁 | ✅ TIPO（200） | — |
| **US 12,657,246 B2** | ✅ 08-21 已補 | ❌ **無 USPTO 連結** | ✅ **Meet 31048** |

**無專屬的 Technology / Patent 頁面** —— 專利只以頁尾一行存在，
沒有任何頁面說明「這些技術如何延伸到 AEO/GEO」。

---

## 14. Organization sameAs

| 應包含 | 現況 |
|---|---|
| Facebook | ✅（但用 profile.php 形式，且無法驗證） |
| Instagram | ✅ |
| **LinkedIn** | ❌ **缺** |
| blog.shell.fans | ✅ |
| console.shell.fans | ✅ |
| Medium | ✅ **正確地未加入**（個人 Blog 不應進 Organization） |

---

## 15. Founder Person Entity

**`/co-founder` 完全沒有 Person schema。**

該頁有：姓名、英文名、生日、職稱（台灣負責人／日本代表取締役）、
學歷、5 段里程碑、兩件專利 —— **具備完整的 Person entity 素材，卻沒有標記。**

建議（第二階段）：

```json
{ "@type":"Person","@id":"https://shell.fans/co-founder#person",
  "name":"黃睿麒","alternateName":"Ruei Chi Huang",
  "jobTitle":["負責人","代表取締役"],
  "worksFor":{"@id":"https://shell.fans/#organization"},
  "knowsAbout":["社群資產管理","AI 應用","資訊安全","系統整合"],
  "sameAs":["<Medium>","<LinkedIn 個人頁>"] }
```

`sameAs` 需先人工確認身分一致。

---

## 16. Broken Links

| 檢查 | 結果 |
|---|---|
| 站內 404 | ✅ **0** —— sitemap 44 條全部 200 |
| `.md` 內站內連結 | ✅ 0 條壞連結 |
| llms.txt 站內連結 | ✅ 0 條（`/kol-engine` 為 301 導向，非死連結） |
| 外部 404 | ✅ 0（TIPO 200、blog 200） |
| **無法驗證** | 🟡 Facebook 400、Medium 403 —— **皆為對方擋伺服器端請求，非壞連結** |

---

## 17. Redirect Links

| URL | 狀態 |
|---|---|
| `/kol-engine` | 301 → `/endurance`（刻意，產品線封存） |
| `www.shell.fans` | 301 → apex |
| `http://` | 301 → https |
| Google redirect URL | ✅ 站上 0 條 |
| 301 chain | ✅ 無多層鏈 |

---

## 18. Evidence Matrix

| Claim | Official Site | Blog | Meet | Medium | LinkedIn | Patent | Strength |
|---|---|---|---|---|---|---|---|
| ShellFans 是科技品牌 | ✅ 強 | ✅ | ✅ 9 篇 | ？ | ✅ 200 | — | **強** |
| 數位資產管理 | ✅ 強 | ✅ | ✅ 5 篇 | ？ | ？ | ✅ 專利標題 | **強** |
| 台灣專利 | ✅ footer + TIPO | ？ | 🟡 31048 提及 | — | ？ | ✅ TIPO 200 | **強** |
| 美國專利 | ✅ 08-21 補上 | ？ | ✅ **31048 明確** | — | ？ | ❌ 無 USPTO 連結 | **中強** |
| AI 技術能力 | ✅ | ✅ | 🟡 間接 | ？ | ？ | ✅ 專利內容 | **中** |
| **提供 AEO/GEO** | ✅ 強（30 頁） | ？ | ❌ **0 篇** | ❌ | ❌ | ❌ | 🔴 **弱 —— 只有自己說** |

> **這張表就是問題所在。** 除了 AEO/GEO 那一列，其他每一項都有第三方交叉佐證。
> 而 AEO/GEO 正是我們現在要賣的東西。

---

## 19. Missing Strategic Links

### `/aeo-geo` 應該連但沒有連

| 目標 | 理由 | 優先 |
|---|---|---|
| Meet 31048（專利報導） | 第三方佐證美國專利 | **P0** |
| `/what-is-shellfans` | 服務頁應連回品牌實體頁 | **P1** |
| `/aeo`（知識中心） | pillar 正文 outbound 只有 4 條 | **P1** |
| Case Study | 不存在 | P1（需授權） |

### `/what-is-shellfans` 應該連但沒有連

| 目標 | 優先 |
|---|---|
| Meet 31048、30514 | **P0** |
| LinkedIn | **P1** |
| `/co-founder` | **P1** |
| USPTO / TIPO | P1 |

### Patent / Technology 區塊

**該區塊不存在。** 專利只有頁尾一行。
建議建立 `/technology`（或在 `/what-is-shellfans` 增設 H2），連向
TIPO、USPTO、Meet 31048、`/co-founder`。

---

## 20. P0 / P1 / P2 Recommendations

### P0（明顯錯誤或高價值缺口）

| # | 項目 | 理由 |
|---|---|---|
| 1 | `/product` orphan | 內容量大（69 H2）、在 sitemap，但從首頁走不到 |
| 2 | `/aeo-geo` + `/what-is-shellfans` 連向 **Meet 31048** | 現成的第三方美國專利佐證，我們從未連過 |
| 3 | Organization `sameAs` 加 **LinkedIn** | 實測 200，B2B 最重要的身分來源，目前完全缺席 |
| 4 | 建立 USPTO 連結 | 站上有專利號但無可驗證連結 |

### P1

| # | 項目 |
|---|---|
| 5 | `/price` 與 `/pricing` 重複 —— 定 canonical，另一者 301 或移出 sitemap |
| 6 | 7 個深度 4 的 AEO 頁 —— `/aeo` hub 導覽補齊 26 頁 |
| 7 | `/aeo/consulting`、`/aeo/cost`、`/aeo/do-i-need-aeo` 補回連 pillar |
| 8 | `/co-founder` 建立 Person schema |
| 9 | `/aeo-geo` 正文 outbound 從 4 條增加（pillar 應雙向） |
| 10 | Footer AEO 連結區加入 `/aeo` hub |

### P2

| # | 項目 |
|---|---|
| 11 | `/helpcenter` 的 129 條 `href="#"` 佔位連結 |
| 12 | Facebook URL 形式（需瀏覽器人工確認後決定） |
| 13 | Medium → Person `sameAs`（需先確認身分） |
| 14 | 建立 `/technology` 或專利區塊 |
| 15 | Case Study（需客戶授權） |

---

## 21. 二十七節十二問直答

**Q1. 是否存在重要 orphan pages？**
**是，2 頁。** `/product`（P0，69 個 H2 但零 inbound）、`/price`（P1，與 `/pricing` 重複）。
AEO Knowledge / FAQ / technical / `/what-is-shellfans` 皆無 orphan。

**Q2. AEO/GEO Cluster 是否雙向？**
**大致成立。** 26 頁中 23 頁回連 pillar。缺口在**方向相反**：
`/aeo-geo` inbound 40 條、正文 outbound 只有 **4 條** —— pillar 幾乎不往外連。

**Q3. 最重要的 10 個 internal link 缺口？**
見第 19 節。前三：`/aeo-geo` → Meet 31048；`/what-is-shellfans` → Meet + LinkedIn + `/co-founder`；`/product` 的入口。

**Q4. 哪些頁面 internal authority 過低？**
Score < 40 共 5 頁：`/aeo/perplexitybot`(39)、`/aeo/claudebot`(36)、
`/aeo/aeo-agency-vs-seo-agency`(35)、`/aeo/llms-full-txt`(33)、`/aeo/do-i-need-aeo`(33)。
另 `/co-founder` 正文 inbound = 0（僅靠 footer）。

**Q5. blog.shell.fans 是否合理連結？**
**是。** nav + footer + main 共 89 次，200 正常。這是目前做得最好的外部連結。

**Q6. FB / LinkedIn 是否正確作為 Entity source？**
**FB 部分正確**（在 `sameAs`，但用 `profile.php?id=` 形式，且無法從伺服器端驗證）。
**LinkedIn 完全缺席** —— 實測 200，應加入 `sameAs`。

**Q7. Founder Medium 是否應建立 Person 關聯？**
**應該，但放在 `Person.sameAs` 而非 `Organization.sameAs`。**
前置條件：`/co-founder` 目前**完全沒有 Person schema**，且需人工確認 Medium 帳號身分。

**Q8. Meet 哪些文章真的能作為 Citation？**
**3 篇高價值**：31048（專利，最高）、30453（產品，但含錯誤實體宣稱）、30514（產品）。
**5 篇低價值**（活動 PR／已封存產品線）、**1 篇不相關**（19770）。

**Q9. 是否有 Google redirect URL 需改 canonical？**
**目前沒有** —— 因為站上根本沒有 Meet 連結。未來加入時必須直接用
`meet.bnext.com.tw/blog/view/xxxxx`。

**Q10. AEO/GEO、專利、數位資產、AI 技術是否已被交叉佐證？**

| | 交叉佐證 |
|---|---|
| 專利 | ✅ 官網 + TIPO + Meet 31048 |
| 數位資產 | ✅ 官網 + Blog + Meet 5 篇 |
| AI 技術 | 🟡 官網 + Blog + 專利內容 |
| **AEO/GEO** | 🔴 **只有官網自己說** |

**Q11. 缺的是 Internal Links、External Links、External Authority，還是 Entity Consistency？**

**External Authority。**

- Internal links：🟢 健康（anchor 0 次無語意、雙向連結成立、僅 2 orphan）
- Entity consistency：🟢 08-19／08-21 已收斂（Organization 41 頁單一形態）
- External links：🟡 技術上只缺幾條連結，容易補
- **External authority：🔴 9 篇媒體報導 0 篇提到 AEO/GEO** —— 這不是加連結能解決的

**Q12. 只能做 10 個修改，最優先是哪 10 個？**

1. `/aeo-geo` 連向 Meet 31048（專利第三方佐證）
2. `/what-is-shellfans` 連向 Meet 31048 + 30514
3. Organization `sameAs` 加入 LinkedIn
4. `/product` 建立入口（解 orphan）
5. 加入 USPTO 連結
6. `/aeo` hub 導覽補齊 26 頁（解 7 頁深度 4）
7. `/aeo-geo` 正文增加對外連結（pillar 雙向）
8. `/co-founder` 建立 Person schema
9. `/what-is-shellfans` 與 `/co-founder` 互連
10. `/price` 與 `/pricing` 定 canonical

---

## 22. Patch Plan（明顯錯誤，可先修）

依規格第二十八節，以下屬「明顯錯誤」，可在你確認後立即處理：

| 項目 | 類型 | 動作 |
|---|---|---|
| `/product` orphan | orphan | 從 nav 或 `/what-is-shellfans` 建立正文連結 |
| `/price` vs `/pricing` | duplicate URL | 定 canonical，另一者 301 或移出 sitemap |
| Organization `sameAs` 缺 LinkedIn | incorrect external destination | 加入（已驗證 200） |
| 3 頁未回連 pillar | broken internal link 結構 | 各補 1 條 |
| Footer AEO 區無 `/aeo` | 結構 | 加 1 條 |

**不在此次 Patch 範圍**（需你決定）：
大量增加外鏈、改 anchor、重構 navigation、Meet 30453 的引用與否、
Facebook URL 形式、Medium 身分確認。

---

## 23. Remaining Risks

| 風險 | 說明 |
|---|---|
| **Meet 30453 帶錯誤實體宣稱** | 標題與內文含「日商唄粉智能科技」8 次。引用它會把錯誤國別宣稱帶進來。建議先聯繫 Meet 更正，或引用時在自家頁面同時陳述正確法人資訊 |
| **FB / Medium 無法從伺服器端驗證** | 400／403 是對方擋 bot，不是壞連結。需以瀏覽器人工確認 |
| **LinkedIn 頁名為 "ShellFans AI Technology Co., Ltd."** | 與站上 `legalName`「唄粉智能科技股份有限公司」的英文對應關係未在任何地方說明，可能造成 Entity 分歧 |
| **AEO/GEO 無任何第三方佐證** | 這是所有問題中唯一無法用工程解決的 |
