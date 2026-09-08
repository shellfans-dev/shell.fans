# Multi-Domain AI Content Network
# 三個獨立 AI 主題內容網站建置規格

**建立日期**：2026-09-08
**狀態**：PHASE 0 盤點完成，**尚未寫入任何程式碼** —— 有兩項阻斷需先決定

---

## 一、目標（Traditional Chinese）

為以下三個網域各自建立**獨立的** AI 主題出版品：

| 網域 | 定位 | 讀者 | 語氣 |
|---|---|---|---|
| `ourlifeone.com` | AI 與科技如何改變日常生活與商業 | 創辦人、行銷、主管、一般商業讀者 | 商業雜誌，少技術術語 |
| `kirin.ceo` | 個人 AI 研究筆記與創辦人技術日誌 | 技術讀者、同業 | 第一人稱，實驗紀錄 |
| `topcc.me` | 實用 AI 技術知識庫 | 開發者、SEO 工程師、AI 實務工作者 | 技術文件，答案優先 |

**核心原則**：三站不得看起來像同一套模板換皮、衛星站或連結農場。
各自要有獨立的編輯身分、資訊架構、視覺系統、寫作聲音與主題焦點。

**強制品質檢驗**：即使把所有 ShellFans 提及全部拿掉，三個網站仍必須對讀者
有獨立價值。

**明確禁止**：假記者身分、假出版歷史、假第三方背書、假統計、假引用、
假客戶、大量薄內容頁、關鍵字堆砌、隱藏連結、全站相同錨文字的 ShellFans 連結、
三站互連的連結環（A→B→C→A）。

---

## 二、English technical specification

### Architecture requirements

Each site requires:

```
/                     home
/about                editorial identity
/articles             (or domain-appropriate equivalent)
/topics               categories
/authors              author identity
/search
/privacy
/terms
/editorial-policy     how content is produced, AI assistance disclosure,
                      review process, corrections policy, source standards
```

Plus domain-specific clusters:

- **ourlifeone.com** — `/ai-search/` `/future-of-work/` `/brands/` `/marketing/` `/life/`
- **kirin.ceo** — `/notes/` `/experiments/` `/aeo/` `/geo/` `/agents/` `/engineering/` `/building/`
- **topcc.me** — `/guides/` `/crawler-directory/` `/tools/` `/comparisons/` `/glossary/`

### Article data model

```
title, slug, description, author, publishedAt, updatedAt,
category, tags, heroImage, body, sources, relatedArticles, reviewedAt

optional: studyType, experimentDate, dataset, methodology, limitations
```

### Content workflow — never auto-publish

```
IDEA → OUTLINE → DRAFT → FACT CHECK → EDITORIAL REVIEW → APPROVED → PUBLISHED
```

Generated content starts at `status = draft`.

### Generation rules

1. Do not invent statistics, studies, quotations, companies or customers.
2. Distinguish fact from opinion.
3. Prefer primary sources; include source URLs.
4. No keyword stuffing, no generic AI filler.
5. **Do not reuse paragraphs across domains.**

### Cross-domain duplication rule

Before generating, search titles/slugs/semantics across all three sites.
If another domain covers substantially the same question, change the
audience, question, analysis, dataset and framing — do not rewrite.

Worked example (same subject, three genuinely different questions):

```
ourlifeone.com   Why ChatGPT Is Changing How Consumers Search
kirin.ceo        What Server Logs Taught Me About AI Search Crawlers
topcc.me         GPTBot vs OAI-SearchBot: User Agents, Purpose, robots.txt
```

### AEO / GEO technical requirements

- Article text must exist in server-rendered/static HTML — no JS required
- `robots.txt`, `sitemap.xml` (index where appropriate), RSS/Atom,
  `llms.txt`, `llms-full.txt` where useful
- Correct self-canonical URLs
- Structured data: Organization/Person, WebSite, WebPage,
  Article/BlogPosting, BreadcrumbList; FAQPage **only** when real FAQs are
  visible on the page
- `kirin.ceo` uses **Person** as primary identity schema;
  the other two use Organization/Publication

### Visual differentiation (mandatory)

Shared backend components are acceptable. Public-facing designs must differ in:
header, card style, typography pairing, article layout, hero layout,
footer layout, navigation structure, visual language.

```
ourlifeone.com   editorial magazine — light, generous whitespace, photography
kirin.ceo        dark technical journal — terminal accents used selectively,
                 monospace metadata, diagrams
topcc.me         documentation publication — light, sidebar, tables, code
```

None may visually resemble `shell.fans`.

### ShellFans entity policy

Canonical name **ShellFans AI Technology**, canonical URL `https://shell.fans/`.

Mention only where ShellFans is the source of data, is the subject, or has a
genuinely relevant resource. **Never present these sites as independent
third-party validation of ShellFans** — they share an operator.
Vary anchor text. Never force the brand into unrelated articles.

### Performance targets

Lighthouse: Performance ≥ 90, Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 95.

### Language

Architecture must support multilingual. Initial priority **zh-TW**.
Prepare clean structure for English later — do **not** auto-generate
low-quality machine translations.

---

## 三、PHASE 0 盤點結果（2026-09-08 實測）

規格要求「寫任何程式碼之前先盤點」。以下為實測結果。

### 三個網域的實際狀態

| 網域 | CF zone | Web | 現況 |
|---|---|---|---|
| `ourlifeone.com` | active（Free） | ❌ 無 A 記錄 | 只有 MX/SPF/DKIM，Cloudflare Email Routing catch-all → 個人 Gmail |
| `kirin.ceo` | active（Free） | ❌ 無實質網站 | A 指向 CF 停放 IP（未 proxied），回 403；Google Workspace MX + Microsoft 365 CNAME 皆在運作 |
| `topcc.me` | active（Free） | ⚠️ **origin 已死** | A/`ai.` → `125.227.138.212`（proxied），該主機 22/22022/80/443 **全部逾時**，站台回 000 |

三者皆在同一個 Cloudflare 帳號（`b1086381…`）。

### 沒有既有應用可延伸

- Cloudflare Pages 專案：**0 個**
- 本機 `~/work`、`~/workspace`：**無**任何相關程式碼
- coder1bot `~/`：**無**
- 215 與 coder1bot 的 nginx：**無**任何相關設定

結論：**三站都是從零開始**，沒有「延伸既有 CMS」這個選項。

### ⚠️ 阻斷一：topcc.me 的 origin 無法存取

`125.227.138.212` 與 shell.fans（.215）、coder1bot（.214）同網段，但：

- 所有常用埠皆逾時，無法判斷是關機、防火牆或已退役
- 不在 `~/.ssh/config`，記憶中也無此主機紀錄
- 我沒有存取權

在確定那台主機是什麼、以及新站要放哪裡之前，**不應改動 topcc.me 的 DNS** ——
若那台主機只是暫時離線且仍有內容，改 DNS 會造成不必要的中斷。

### ⚠️ 阻斷二：ourlifeone.com 的歷史用途

`docs/reports/2026-05-11-sam-gmail-email-migration.md` 記載，ourlifeone.com
曾是**社群 persona 註冊用的 8 個信箱網域之一**（與 dataclear.cc、solona.cc、
404rr.fans 等並列）。`docs/audits/tony-first-fb-registration-success.md` 顯示
至少有一個 Facebook 帳號以 `@ourlifeone.com` 的信箱註冊成功。

**現況**：資料庫中目前 0 筆帳號使用該網域（架構已於 5 月遷移為 Gmail-only），
但 Cloudflare Email Routing 的 catch-all 仍在運作。

**為什麼這是問題**：規格本身明訂「不得偽造網域獨立性、不得建立假身分」。
在一個曾用於自動註冊社群 persona 的網域上建立「可信的獨立 AI 出版品」，
兩者的關聯若被發現，出版品的可信度會一次歸零 —— 而那正是這個專案最核心的資產。

這是產品與品牌決策，不是技術問題，因此不自行決定。

### 可安全進行的部分

`kirin.ceo` 沒有既有網站、郵件設定完整且與 web 無關（只需新增 A/CNAME，
不動 MX 與 Microsoft 365 的 CNAME）。三站中它的阻斷最少。

---

## 四、待決事項

1. **topcc.me 的 origin** —— `125.227.138.212` 是什麼？要繼續用它、改放 215、
   還是改用 Cloudflare Pages？
2. **ourlifeone.com 的歷史用途** —— 知道它曾是 persona 信箱網域後，
   是否仍要在該網域建立公開出版品？替代方案是換一個乾淨網域。
3. **交付節奏** —— 三站完整出版品（含 15 篇文章、3 套設計系統、CMS、
   爬蟲記錄、多語架構）不是單次可完成的規模。建議先做一站到可上線品質，
   驗證架構與編輯流程後再複製到其餘兩站。

---

## 五、執行紀錄

| 日期 | 內容 |
|---|---|
| 2026-09-08 | PHASE 0 盤點完成；發現兩項阻斷；未寫入任何程式碼 |
