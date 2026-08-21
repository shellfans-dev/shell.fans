# llms.txt / AI Crawler Discoverability / Markdown Alternate / Entity 專項稽核

日期：2026-08-21
範圍：`/llms.txt`、`/llms-full.txt`、`/what-is-shellfans`、`/aeo-geo`、26 頁 AEO 知識叢集
性質：稽核 + 實作（每項修改皆附原因）

---

## 1. Before

| 項目 | 稽核前狀態 |
|---|---|
| `/llms.txt` | 200、text/plain、16,752 字、143 行 |
| `/llms-full.txt` | 200、text/plain、30,883 字、**Last-Updated 2026-07-02** |
| `.md` 檔案 | **完全不存在** |
| nginx 對 `.md` 的處理 | **`application/octet-stream`** + `nosniff` |
| `rel="describedby"` | **0 頁** |
| `rel="alternate" type="text/markdown"` | **0 頁** |
| 美國專利 US 12,657,246 B2 | **全站完全沒有** |
| 頁尾對美國專利的描述 | 「其他**申請中**美國、日本之專利保護」 |
| robots.txt | ✅ 無任何 Disallow |
| sitemap | ✅ 44 條，全部 200 |
| HTML canonical | ✅ 全部 self-canonical |

---

## 2. Issues Found

### 🔴 I-1　`.md` 會被當成二進位下載（最基礎的阻斷）

nginx 內建 `mime.types` 沒有 `.md`，回 `application/octet-stream`。
配上站台既有的 `X-Content-Type-Options: nosniff`，瀏覽器與多數 bot 會當成
**檔案下載**而不是文字。

> **這一項不修，後面所有 Markdown 工作都是白做的。**

### 🔴 I-2　專利資訊自相矛盾，且美國專利號從未出現

| 位置 | 說法 |
|---|---|
| 靜態站頁尾（41 頁 + i18n 字典） | 「其他**申請中**美國、日本之專利保護」 |
| 創辦人頁（DB milestone 2025/12） | 「**於美國取得**技術發明專利」 |

**同一個網站對同一件事有兩種說法**，而專利號 `US 12,657,246 B2` 全站搜尋 0 命中。

### 🟡 I-3　`llms-full.txt` 的 Last-Updated 停在 2026-07-02

該檔在 08-19、08-21 都被實質修改過（品牌定義句、法人名稱、Patents 區塊），
但 `Last-Updated` 從未更新。與 `llms.txt`（2026-08-19）不同步。

日期是**人工 hardcode**，沒有任何機制保證它跟得上內容。

### 🟡 I-4　無任何 AI discovery 標籤

44 頁全部沒有 `rel="describedby"`。AI agent 抓到任何一頁時，
沒有訊號指向 `/llms.txt` —— 只能猜根目錄有這個檔案。

### 🟡 I-5　llms.txt 的所有連結都指向 HTML

AI agent 拿到的是 34KB 的 HTML，其中約 93% 是 nav、footer、inline CSS、
20KB 的 i18n bootstrap 與 chat widget。正文只有約 2.3KB。

---

## 3. llms.txt Audit

### 章節篇幅分析

| 字數 | 章節 | 判定 |
|---|---|---|
| 939 | `# ShellFans AI Technology`（含定義句） | **KEEP** |
| 2,596 | `## Brand structure` | **KEEP** —— 這是實體定義的核心 |
| 852 | `## Social asset backup` | KEEP |
| 890 | `## About ShellFans` | KEEP |
| **1,402** | `## Word-of-mouth marketing product (口碑行銷)` | 🟡 **SHORTEN** —— 該產品線已封存（`kolfans_wom_enabled: false`、nav 入口已移除），篇幅卻大於兩條在營運的服務線 |
| 940 | `## AI technology direction` | KEEP |
| **1,717** | `## ShellFans AEO/GEO Checker` | 🟡 **可 SHORTEN** —— 部分規格細節與 llms-full 重複 |
| 706 | `## ShellFans AEO Managed Hosting` | KEEP |
| **4,461** | `## AEO/GEO knowledge cluster` | KEEP（本次改為指向 `.md`，是導覽的核心價值） |
| 426 | `## Resources` | KEEP |
| 183 | `## Contact` | KEEP |
| 461 | `## Optional` | KEEP |
| 1,167 | `## Citation hint` | KEEP |

**本次未執行 SHORTEN**（列為 P2）。理由：口碑行銷是否停止對外說明屬商業決定，
不由工程單方面裁剪；Checker 章節的精簡需與 llms-full 對照後一起做，
避免刪掉之後兩邊都沒有。

### 定位判定

llms.txt 目前 16.7KB —— 偏大但**尚未失去導覽性質**：
它沒有整段正文、沒有 pricing 明細、沒有重複的 FAQ 全文，
主要是逐頁的一行說明。與「巨大知識庫」的形態仍有距離。

---

## 4. llms-full.txt Audit

| 檢查 | 結果 |
|---|---|
| Last-Updated 與 llms.txt 同步 | ❌ → ✅ **已修**（兩檔皆改為自動衍生） |
| 品牌描述一致 | ✅ 兩檔皆為「兩條並行的核心服務」 |
| AEO/GEO 定義一致 | ✅ |
| 法人名稱一致 | ✅ 唄粉智能科技股份有限公司（無國別前綴） |
| 專利號一致 | ❌ → ✅ **已修**（兩檔皆新增 Patents 區塊） |
| URL 失效 | ✅ 0 條 |
| pricing 過期 | ✅ 無明確價格數字 |
| 過度自我宣稱 | ✅ **未發現**「最好／第一名／AI 最推薦」等字樣 |
| ranking hack 措辭 | ✅ **未發現**「加 llms.txt 就能提升 ChatGPT 排名」這類說法 |

> `/aeo/llms-txt` 頁面反而主動寫著「**llms.txt 目前不是標準，沒有任何主要 AI
> 業者公開承諾會讀取它**」—— 立場正確，無須修改。

---

## 5. Entity Consistency

比對 8 個表面的核心定義：

| 表面 | 定義 | 一致 |
|---|---|---|
| Homepage `<title>` | AEO/GEO 代管與跨平台社群資產續航 | ✅ |
| Homepage description | 兩條並行的核心服務 | ✅ |
| `/what-is-shellfans` | 兩條並行的核心服務 | ✅ |
| `/aeo-geo` | AEO/GEO 代管 + 三項服務 Service schema | ✅ |
| `llms.txt` 定義句 | 唄粉智能科技ShellFans…兩條並行的核心服務 | ✅ |
| `llms-full.txt` canonical answer | 同上 | ✅ |
| Organization schema（41 頁） | `name` 統一、`alternateName` 6 種寫法、`knowsAbout` 13 項 | ✅ |
| Footer | 唄粉智能科技股份有限公司 + 統編 | ✅ |

**未發現「某頁說純備份平台、另一頁說純 AEO 公司」的矛盾。**
兩條服務線在所有表面皆並列。

---

## 6. robots.txt Audit

**Effective rules：無任何 `Disallow`。**

21 個 AI crawler 群組全部明確 `Allow: /`（robots.txt 的群組不繼承 `User-agent: *`，
因此逐一列出是正確作法）。

| 檢查 | 結果 |
|---|---|
| global Disallow | ✅ 0 |
| `/aeo` 被 wildcard 擋 | ✅ 否 |
| `/llms.txt`、`/llms-full.txt` | ✅ 可存取 |
| `.md` | ✅ 不受任何規則影響 |
| Sitemap 宣告 | ✅ 有 |

實測 5 支爬蟲抓 `/aeo/what-is-aeo.md`：**GPTBot / OAI-SearchBot / ClaudeBot /
PerplexityBot / Googlebot 全部 200。**

---

## 7. Sitemap Audit

| 檢查 | 結果 |
|---|---|
| 總條目 | 44，全部 200 |
| `/aeo-geo`、`/what-is-shellfans` | ✅ 收錄 |
| 26 個 `/aeo/*` | ✅ 全部收錄 |
| **`.md` 是否誤入** | ✅ **0 條** —— 刻意不收錄 |

`.md` 不進 sitemap 是刻意的：它與 HTML 是同一份內容，收錄會讓搜尋引擎
把兩者當成競爭頁面。AI agent 透過 `llms.txt` 與 HTML 的 `rel="alternate"`
即可發現，不需要 sitemap。

---

## 8. Markdown Alternate Architecture

### 產生方式

| 來源 | 頁數 | 方式 |
|---|---|---|
| `scripts/aeo_pages_content.py` | 26 | **從 content module 產生** —— HTML 與 .md 同源，不會出現「HTML 改了但 .md 忘了改」 |
| HTML 抽取 | 2（`what-is-shellfans`、`aeo-geo`） | 這兩頁沒有 content module，內容來源就是 HTML。只抽 `<main>` 內的語意元素，並在檔尾明確標記抽取來源 |

**共 28 份。**

### 內容規範

保留：title、lede、H2/H3、正文、清單、表格、FAQ、免責說明、相關連結、
canonical / brand / publisher / last-updated metadata。

排除（產生時以斷言檢查，違反即中止）：
`<script>`、`<nav>`、`<footer>`、`<header>`、`<style>`、`sf-footer`、`data-i18n`。

實測三份抽樣：**版面殘骸 0 處**。

### 體積對照

| | HTML | Markdown |
|---|---|---|
| `/aeo/what-is-aeo` | 34.4 KB | **2.8 KB** |
| `/what-is-shellfans` | 113 KB | 約 8 KB |

### Metadata 格式

刻意**不用 YAML front matter**（站台原本沒有這個慣例），改用檔尾的粗體鍵值：

```
**Canonical:** https://shell.fans/aeo/what-is-aeo
**Brand:** ShellFans AI Technology（唄粉智能科技ShellFans）
**Publisher:** 唄粉智能科技股份有限公司（Taiwan, 統一編號 83032387）
**Last-Updated:** 2026-08-16
```

---

## 9. HTML Discovery Tags

```html
<link rel="describedby" href="https://shell.fans/llms.txt">
<link rel="alternate" type="text/markdown"
      href="https://shell.fans/aeo/what-is-aeo.md"
      title="Markdown version for AI agents">
```

| 標籤 | 覆蓋 | 實作位置 |
|---|---|---|
| `describedby` | **44 頁**（除 401/404/search/detail_news） | 26 頁在 `build-aeo-pages.py`；18 頁由 `apply-ai-discovery-tags.py` 冪等插入 |
| `alternate markdown` | **28 頁**（只有真的有 .md 的） | 同上 |

> 站台無共用 layout（純靜態 HTML），因此無法「從 shared head 統一加入」。
> 折衷是把插入邏輯集中在兩支腳本裡，而不是散落在各檔案 —— 冪等，可重複執行。

`alternate` **只在該 `.md` 確實存在時才加**。指向不存在的檔案會產生 404，
比沒有這個標籤更糟。

---

## 10. Indexing / Canonical Strategy

```
HTML  →  self-canonical、進 sitemap、可被索引
 .md  →  X-Robots-Tag: noindex、不進 sitemap、AI 可正常抓取
```

nginx `location ~* \.md$`：

```nginx
default_type text/markdown;
charset_types text/markdown;   # charset 預設不涵蓋 text/markdown
charset utf-8;
add_header X-Robots-Tag "noindex" always;
add_header Cache-Control "public, max-age=3600" always;
```

**刻意不加 `nofollow` 與 `noarchive`：**

- `nofollow` 會讓 `.md` 內的連結不被跟隨 —— 那正是我們要的導流路徑
- `noarchive` 沒有必要，且部分 AI 檢索會參考快取

`noindex` 只影響「是否列入搜尋結果」，**不影響 AI 抓取**。
實測 5 支爬蟲全部 200 確認。

HTML canonical **未因加入 alternate 而變動** —— 8 頁抽驗全部仍為 self-canonical。

---

## 11. Changes Implemented

| # | 修改 | 原因 |
|---|---|---|
| 1 | nginx 新增 `location ~* \.md$`（MIME + charset + noindex） | `.md` 原本回 `application/octet-stream`，會被當二進位下載 |
| 2 | `scripts/build-markdown-alternates.py`（新增） | 從 content module 產生 28 份 .md，與 HTML 同源 |
| 3 | `scripts/apply-ai-discovery-tags.py`（新增） | 為 18 個非產生器頁面冪等插入 discovery 標籤 |
| 4 | `build-aeo-pages.py` 加入兩個 link 標籤 | 26 頁由產生器統一輸出，重跑不會退回 |
| 5 | llms.txt 知識叢集 26 條連結改指 `.md` | AI 拿到 2.8KB 正文而非 34KB HTML |
| 6 | 兩檔 `Last-Updated` 改為**從 git 衍生** | 用內容實際修改日，不用 build timestamp —— 後者會產生假的 freshness |
| 7 | 兩檔新增 `## Patents` 區塊 | 補上遺漏的 US 12,657,246 B2，並明確聲明**這不是 AEO/GEO 專利** |
| 8 | 49 個檔案的頁尾專利文字更正 | 「申請中美國」與創辦人頁「已取得」自相矛盾 |

### Last-Updated 的衍生方式

```
Last-Updated = max(git log -1 --format=%cs -- <來源檔>)
```

`llms.txt` 取自 sitemap、content module、首頁、品牌頁、服務頁；
`llms-full.txt` 取自品牌頁、服務頁、首頁與自身。

**不用 build timestamp** —— 每次部署都更新日期會讓 AI 看到「今天更新」
但內容其實三個月沒動，反而降低可信度。

---

## 12. URLs Tested

### 規格指定的四條

| URL | Status | Content-Type | X-Robots-Tag |
|---|---|---|---|
| `/llms.txt` | 200 | text/plain; charset=utf-8 | — |
| `/llms-full.txt` | 200 | text/plain; charset=utf-8 | — |
| `/what-is-shellfans` | 200 | text/html; charset=utf-8 | — |
| `/what-is-shellfans.md` | 200 | **text/markdown; charset=utf-8** | **noindex** |

### 抽驗 8 頁（規格要求至少 5 頁）

| HTML | HTML | .md | .md Content-Type | XRT | alternate | describedby | canonical |
|---|---|---|---|---|---|---|---|
| `/aeo/what-is-aeo` | 200 | 200 | text/markdown; charset=utf-8 | noindex | ✓ | ✓ | self |
| `/aeo/what-is-geo` | 200 | 200 | 同上 | noindex | ✓ | ✓ | self |
| `/aeo/aeo-vs-seo` | 200 | 200 | 同上 | noindex | ✓ | ✓ | self |
| `/aeo/ai-crawler` | 200 | 200 | 同上 | noindex | ✓ | ✓ | self |
| `/aeo/managed-hosting` | 200 | 200 | 同上 | noindex | ✓ | ✓ | self |
| `/aeo-geo` | 200 | 200 | 同上 | noindex | ✓ | ✓ | self |
| `/what-is-shellfans` | 200 | 200 | 同上 | noindex | ✓ | ✓ | self |
| `/aeo` | 200 | 200 | 同上 | noindex | ✓ | ✓ | self |

### 其他驗證

- nginx 改動前後 12 條 URL 基準矩陣：**零回歸**
- llms.txt 站內連結：**0 條 404**（`/kol-engine` 為 301 導向，非死連結）
- 所有 `.md` 內的站內連結：**0 條壞連結**
- sitemap 44 條：全部 200，`.md` 條目 0

---

## 13. Remaining Risks

| 風險 | 說明 |
|---|---|
| **`what-is-shellfans.md` / `aeo-geo.md` 由 HTML 抽取** | 這兩頁沒有 content module。HTML 改版後需重跑產生器，否則 .md 會落後。已在檔尾明確標記抽取來源與「以 canonical HTML 為準」 |
| **無自動重生機制** | 改內容後必須手動跑 `build-markdown-alternates.py`。建議納入部署流程 |
| **llms.txt 仍偏大（16.7KB）** | 未執行 SHORTEN。口碑行銷章節（1,402 字，已封存產品線）篇幅大於兩條在營運的服務線 —— 是否精簡屬商業決定 |
| **`.md` 未進 sitemap 是刻意的** | 若日後希望 AI 更快發現，可考慮獨立的 `sitemap-md.xml`，但需評估重複索引風險 |
| **Markdown 標題層級來自 HTML 抽取時可能不完美** | `what-is-shellfans.md` 的 `<summary>` 被轉為 `###`，語意接近但非完全等價 |

---

## 14. Recommended Next Steps

| 優先 | 項目 |
|---|---|
| P1 | 把 `build-markdown-alternates.py` 納入部署流程，避免 .md 落後 |
| P1 | 為 `/aeo-geo`、`/what-is-shellfans` 建立 content module，讓兩者也從單一來源產生 |
| P2 | 精簡 llms.txt：口碑行銷章節縮短、Checker 細節移入 llms-full（需商業確認） |
| P2 | 評估其餘頁面（`/endurance`、`/social-media-backup`、`/pricing`）是否需要 .md |
| P2 | 若要更快被發現，評估 `sitemap-md.xml` |

---

## 15. Before / After 對照

| Item | Before | After | Status |
|---|---|---|---|
| llms.txt fetchable | 200 text/plain | 200 text/plain，26 條連結指向 `.md` | ✅ 改善 |
| llms-full freshness | **hardcode 2026-07-02**（落後 50 天） | **從 git 衍生**，與 llms.txt 同步 | ✅ 已修 |
| Entity consistency | 8 個表面已一致 | 維持一致，新增 Patents 區塊 | ✅ 維持 |
| describedby | **0 頁** | **44 頁** | ✅ 已修 |
| Markdown alternate | **0 頁** | **28 頁** | ✅ 已修 |
| AEO pages `.md` | **不存在** | **26 頁 + 2 頁**，2.8KB vs 34KB HTML | ✅ 已修 |
| `.md` Content-Type | **application/octet-stream** | **text/markdown; charset=utf-8** | ✅ 已修 |
| robots access | ✅ 無 Disallow | 維持；5 支爬蟲實測 .md 皆 200 | ✅ 維持 |
| canonical strategy | HTML self-canonical | **未變動**，.md 不參與 canonical | ✅ 維持 |
| duplicate-index protection | 無（無 .md） | `X-Robots-Tag: noindex` + 不進 sitemap | ✅ 已建立 |
| 美國專利號 | **全站 0 次** | llms 兩檔 + 41 頁頁尾 | ✅ 已修 |
| 專利誤稱風險 | 無誤稱，但美國狀態過時 | 明確聲明**非 AEO/GEO 專利** | ✅ 強化 |
