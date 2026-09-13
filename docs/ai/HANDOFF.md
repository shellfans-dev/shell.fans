# Claude → Codex Handoff

## Task ID
fix-initial-locale-render

## Task
Fix initial locale rendering flash（shell.fans 首屏先中文再切英文）

## Goal / Acceptance Criteria
見 `docs/ai/CURRENT-TASK.md`（19 項）。

## Root Cause（實測確認，2026-09-13）
1. shell.fans 是純靜態站（215 nginx + Cloudflare）。伺服器對每個 URL 只有一份 HTML，固定是繁體中文：`<html lang="zh-Hant">`、中文
   title / description / og:*、中文 header、nav、mobile menu、hero、footer（頁尾烘焙在 `#sf-footer-root` 內）。
2. English 偏好只存在 **localStorage** `shellfans_locale`（無 cookie、無 URL、無 Accept-Language、無使用者 profile）。伺服器在回應前讀不到它。
3. 7 個頁面（`index`、`aeo-geo`、`aeo-geo/methodology`、`aeo-geo/taiwan-aeo-tools`、`social-media-backup`、`tools/aeo-geo-checker`、
   `what-is-shellfans`）尾端的 inline i18n 引擎在 **DOMContentLoaded** 才 `applyTranslations()` 替換 146～180 個 `[data-i18n]` 元素、
   `document.title`、meta；`document.documentElement.lang` 也在那時才變。瀏覽器早已把中文畫出來。
4. `js/sf-footer.js`、`js/sf-global-ui.js`（defer）也各自讀 localStorage 決定語系。
5. 額外發現：首頁聊天框的模式切換腳本（inline，早於引擎執行）在載入時把 **中文 fallback 字面值**（「Chat 模式：開」「Chat 模式開啟時…」）
   寫進 DOM、引擎載入後才翻成英文——即使 HTML 已是英文，這兩行仍會閃中文（測試的 mutation 觀察器抓到）。
6. CDN 層：HTML 為 `Cache-Control: no-cache, must-revalidate` + `CDN-Cache-Control: no-store`，Cloudflare `cf-cache-status: DYNAMIC`；
   Cloudflare Worker `shellfans-product-flags` 以 `fetch(request)` 回源（轉送 Cookie），只對 flags API 用 `cacheTtl`。nginx 無 proxy_cache。

## Previous Behavior
```
GET / (任何人)  →  nginx 回 index.html（zh-Hant）
                →  瀏覽器繪出中文
                →  DOMContentLoaded：inline 引擎讀 localStorage=en → 逐元素替換成英文、改 lang/title/meta
                →  sf-footer.js / sf-global-ui.js 各自讀 localStorage 重繪
```

## New Architecture
```
切換語言（__setLocale / footer 切換鈕 / 舊使用者一次性遷移）
   → 寫 cookie shellfans_locale=en|zh-TW（Path=/、Max-Age=31536000、SameSite=Lax、https 下 Secure、非 HttpOnly）
   → 同步 localStorage（相容快取）

GET /  Cookie: shellfans_locale=en
   → nginx map $cookie_shellfans_locale → $sf_lang=".en"
   → try_files 先試 <page>.en.html（首頁 /index.en.html；/aeo-geo 也在 location = /aeo-geo 特別處理）
   → 回英文 HTML：<html lang="en">、英文 title/description/og:title/og:description/twitter:*、og:locale=en_US、
     英文 header/logo/nav/mobile menu/CTA/hero/body、英文烘焙頁尾（含 data-sf-product 標記）、語言切換器勾在 English
   → 瀏覽器第一個 frame 就是英文
   → 引擎以 <html lang> 初始化（currentLocale = servedLocale），applyTranslations() 對已正確的頁面是 no-op
   → sf-footer.js / sf-global-ui.js 解析順序 cookie → localStorage → <html lang>，結果一致

GET /  無 cookie / 值不合法
   → $sf_lang=".x-nolocale"（必定落空）→ try_files 順序與從前完全相同 → 中文（爬蟲與首次造訪不變）

沒有英文版的 44 頁 → 一律中文（與從前相同）
```
英文版 `<page>.en.html`（7 個，已 commit）由 `scripts/build-locale-pages.py` 從**同一份中文頁與頁內字典**產生，語義與 runtime
`applyTranslations()` 相同（attr / innerHTML / textContent 三種模式、缺鍵退回 zh），另處理 lang、og:locale(+alternate)、title、
description、og:*、twitter:*、切換器勾選狀態、烘焙頁尾（用 `js/sf-footer.js` SHELL_BASE 的雙語字串翻譯，保留 `data-sf-product`）。
產生後自我驗證每個 `[data-i18n]` 元素都等於英文值；`--check` 偵測過期。不是 CSS 隱藏、不是 setTimeout、不是 runtime DOM hack。

## Locale Resolution Priority（實際）
伺服器端：1. cookie `shellfans_locale`（`en` → 英文版；其他 → 中文）。沒有 URL locale route（站上本來就沒有，未新增）；不依 Accept-Language
（既有規則：首次造訪預設 zh-TW，維持）；靜態站無登入 profile locale。
客戶端：初始狀態 = `<html lang>`（伺服器已決定）；偏好 = cookie → localStorage；只有「偏好 ≠ 伺服器所給」（舊使用者只有 localStorage、
或伺服器端尚未部署）才在客戶端切換並寫 cookie（一次性）。cookie 存在時 localStorage 會被同步成 cookie 值。

## Modified Files（`git diff --stat` 見 commit）
- 7 個引擎頁：`scripts/apply-locale-bootstrap.py` 冪等修補（bootstrap v2、`__setLocale` 寫 cookie、zh 的 lang 值統一 `zh-Hant`）
- `index.html`：聊天框模式切換靜態標記改為 runtime 預設的 ON 狀態（鍵 `chat.contextModeOn` / `chat.modeHintOn`），初始重繪延後到引擎就緒
- 新增 7 個 `*.en.html`（`index`、`aeo-geo`、`aeo-geo/methodology`、`aeo-geo/taiwan-aeo-tools`、`social-media-backup`、
  `tools/aeo-geo-checker`、`what-is-shellfans`）
- `js/sf-footer.js`（`getLocale` cookie 優先、切換鈕寫 cookie）、`js/sf-global-ui.js`（`locale()` 同順序）
- 52 頁 script 標籤版號 `?v=20260913a` → `20260913b`（`scripts/apply-global-ui.py` ASSET_VER）
- `deploy/nginx/shell.fans.conf`：`map $cookie_shellfans_locale $sf_lang`、`location = /aeo-geo` 與 `location /` 的 try_files、
  `location ~ \.en\.html$ { return 404; }`
- 新增 `scripts/build-locale-pages.py`、`scripts/apply-locale-bootstrap.py`、`scripts/test-initial-locale.py`、
  `scripts/test-initial-locale-browser.cjs`
- 文件：`docs/ai/CURRENT-TASK.md`、`docs/ai/HANDOFF.md`、`docs/ai/DECISIONS.md`（D-015，saas_womm 同步）、`CLAUDE.md`、
  `prompts/fix-initial-locale-render.md`

## Tests Executed

### Lint
NOT AVAILABLE（repo 無 lint script）。等價檢查：`python3 -m py_compile` 4 支腳本、`node --check` 2 支 runtime + 瀏覽器測試：PASS。

### Typecheck
NOT AVAILABLE（純靜態站）。

### Targeted Tests
PASS — `python3 scripts/test-initial-locale.py`：**88/88**。內容：起一個只給測試用的 nginx（127.0.0.1:18080/18443，`map` 與
`location` 區塊**逐字抽自** `deploy/nginx/shell.fans.conf`，root = 工作樹），以 raw HTTP 驗證：無 cookie / cookie=zh-TW / 無效值 /
夾雜其他 cookie → 中文（lang zh-Hant、中文 title、nav、logo、頁尾）；cookie=en → `lang="en"`、英文 title / description / og:title /
og:description / twitter:title、`og:locale=en_US`、nav 6 項英文、mobile menu 英文含 Get Started、header 與 footer logo 皆
`nav_logo_en.png`、頁尾英文（Privacy Policy / Terms / 公司英文名 / Site navigation / 專利）且保留 `data-sf-product`、hero 英文、
切換器勾在 English、無 hide-until-JS、引擎與雙語字典仍在、bootstrap v2；nav/mobile/footer 的 `<a href>` 數 zh=en=(6,8,18)；
canonical 與 JSON-LD 逐位元未變；7 頁英文版皆 200 + lang en、無 cookie 皆 zh-Hant；7 個 `/<page>.en.html` 直接存取 404；
`/pricing` `/about` `/aeo/what-is-aeo` `/developers` 有無 cookie 回應逐位元相同；`/js/sf-footer.js` 帶 cookie 仍是 JS；
`Accept: text/markdown` 仍優先回 .md；未知路徑 404；快取標頭與 ETag（見下）；`build-locale-pages.py --check` 全部 OK。

PASS — `node scripts/test-initial-locale-browser.cjs`（playwright + 系統 chromium，對同一個測試 nginx）：**61/61**，見下方三節。

### Full Tests
NOT RUN（repo 無其他自動測試套件；`scripts/test-agentic-surface.py` 針對線上站台，部署後再跑）。

### Build
PASS — `python3 scripts/build-locale-pages.py` 產生 7 個英文版並自我驗證；`--check` 全部 OK。`apply-locale-bootstrap.py` 重跑冪等（7 個 already v2）。

## Raw HTML Verification
測試 nginx（等同 deploy conf）：
- `GET /`（無 cookie）→ 200，`<html lang="zh-Hant">`，`<title>ShellFans｜AEO/GEO 代管與跨平台社群資產續航</title>`，nav 第一項「AEO/GEO 代管」，
  logo `nav_logo.svg`，頁尾「隱私權政策」。
- `GET /` + `Cookie: shellfans_locale=en` → 200，`<html lang="en">`，`<title>ShellFans | AEO/GEO Managed Hosting &amp; Cross-platform Social Asset Continuity</title>`，
  `og:locale=en_US`，nav `AEO/GEO Hosting | Engagement Engine | Fans Analysis | Word-of-Mouth | Pricing | Klog`，mobile menu 英文 + `Get Started`，
  header/footer logo `nav_logo_en.png`，頁尾 `Privacy Policy` / `Terms of Service` / `ShellFans AI Technology Co., Ltd.`，且**不含**中文版主要 UI。
- 另外 6 頁同樣驗證（lang / nav / logo）。無英文版的頁面兩種請求回應相同。
- 注意：nginx `map` 字串比對不分大小寫，`Cookie: shellfans_locale=EN` 也回英文（引擎仍以 `<html lang>` 初始化，無不一致）。

## Browser Verification（1440 / 768 / 390）
- **JS 關閉**（所見即伺服器 HTML）：cookie=en 首幀英文（lang / nav / logo / 頁尾 / title / description / mobile menu / CTA / hero）；
  無 cookie、cookie=zh-TW、cookie=xx 首幀中文。截圖 `/tmp/sf-locale-test/shots/`。
- **JS 開啟**：五個組合（zh 1440、en 1440、en 768、en 390、zh 390）最終狀態正確，且從 document start 起以 MutationObserver 監看
  所有文字型 `[data-i18n]` 元素，**變更數 = 0**（applyTranslations 為 no-op，等同 hydration 一致）；切換器標籤正確；390 的
  hamburger 選單語系正確、無橫向溢位；無 page error（測試 origin 是 127.0.0.1，對 console.shell.fans 的跨域 fetch 被 CORS 擋是預期，
  各 runtime 皆退回內建 baseline）。
- **切換**：zh→en 立即（nav / logo / 頁尾 logo / 法律連結 / lang），cookie 寫入（Path=/、Secure、SameSite=Lax、≈1 年）；reload 後伺服器直接回英文、
  0 變更；en→zh 立即、cookie=zh-TW；reload 回中文、0 變更。
- **Back / Forward / New tab**：`/` → `/aeo-geo` → back → forward 皆英文；新分頁 `/what-is-shellfans` 英文、0 變更。
- **舊使用者**（localStorage=en、無 cookie）：第一次載入客戶端切成英文（一次性）且 cookie 已寫入；第二次載入伺服器直接回英文、0 變更。
- **cookie=en 但 localStorage 過期為 zh-TW**：以 cookie 為準、0 變更，localStorage 被同步為 en。

## Slow Network Verification
CDP `Network.emulateNetworkConditions`（latency 400ms、50 KB/s）＋ JS 開啟，從 navigation 一開始每 40ms 取樣 `documentElement.lang`
與第一個 nav 文字直到 `readyState=complete`：en 183 個取樣全部 `en` / `AEO/GEO Hosting`；zh 526 個取樣全部 `AEO/GEO 代管`；兩者 0 變更。

## No-JS / Crawler Verification
兩種語系的 raw HTML 都保有完整 header、`<nav>` 6 條 `<a href>`、mobile menu 8 條、頁尾 18 條、hero 與正文、內部連結；
canonical 不變（`https://shell.fans`）；JSON-LD 逐位元不變；`robots.txt`、`sitemap.xml`、`llms.txt`、`llms-full.txt` 未動（commit 不含）。
英文版全文 45 條 `<a href>`（中文 47）：差的 2 條在 FAQ 兩則答案的內文連結——英文字典本身沒有那兩個連結，與修正前 JS 切換後看到的一樣，屬既有內容差異。

## SEO / AEO Verification
- canonical、hreflang 值未改（`aeo-geo.html` 原本就宣告 `hreflang="en"` 指向同一 URL，與「同 URL 依 cookie 出語系」一致）；沒有新增 localized URL。
- Google 等不帶 cookie 的爬蟲行為與從前完全相同（中文）。
- `<html lang>`：英文版 `en`；中文維持 `zh-Hant`（引擎的 runtime 值也統一為 `zh-Hant`，先前 index 變體會改成 `zh-TW`）。
- 12 個 Webflow legacy 頁（pricing、contact…）原本就 `lang="en"` 但內容中文——既有問題，未在本任務更動（不在 scope）。

## Cache Verification
- 同一 URL 依 cookie 出不同語系。HTML 回應（兩版）皆 `Cache-Control: no-cache, must-revalidate` + `CDN-Cache-Control: no-store`；
  線上 Cloudflare 對 HTML 為 `DYNAMIC`（不快取）；nginx 無 proxy_cache。
- 兩版 ETag 不同（不同檔案）；`If-None-Match: <zh ETag>` + cookie=en → 200 英文（不會拿到過期 304）；`If-None-Match: <en ETag>` + cookie=en → 304。
- **刻意不加 `Vary: Cookie`**：`location /` 同時服務 js/css/圖片等 30 天 immutable 資產，Vary: Cookie 會讓 Cloudflare 對這些資產的快取失效；
  HTML 本身已 no-store，不需要。理由寫在 nginx conf 註解與 D-015。
- Cloudflare Worker `workers/product-flags-rewriter.js`：`fetch(request)` 原樣回源（含 Cookie），未動。

## Security Considerations
- cookie 只含 `en` / `zh-TW`，nginx map 只對 `en` 產生後綴，其餘值一律中文；客戶端 regex 只接受這兩個值。
- 英文版內容全部來自既有頁內字典，產生器對文字模式做 HTML escape（與 runtime `textContent` 同義）；無新的 API、無新輸入面。
- `.en.html` 不可直接存取（404），避免重複內容 URL。

## Known Risks
1. 瀏覽器停用 cookie：退回修正前行為（伺服器出中文、客戶端切換有閃現）。
2. 引擎頁或 `js/sf-footer.js` 的 SHELL_BASE 變更後必須重跑 `scripts/build-locale-pages.py`；`--check` 可擋，但沒有 CI 強制（已寫進 CLAUDE.md）。
3. 44 個無英文版的頁面：英文偏好者看到中文頁 + 依偏好的英文頁尾（與從前相同）。
4. `/api/site/i18n?site=shell` 的覆寫字典（目前每種語言各 1 個鍵）在載入後套用——既有行為，非語系閃現。
5. 部署需要 nginx 設定更新 + reload（`sudo cp deploy/nginx/shell.fans.conf /etc/nginx/sites-enabled/shell.fans.conf && sudo nginx -t && sudo systemctl reload nginx`）
   與檔案複製；只 reload nginx。**尚未部署**（等 Codex PASS）。
6. 產生的 7 個 `.en.html` 是已 commit 的產物，diff 較大（每個約等於原頁大小）。

## Existing Unrelated Dirty Files
`prompts/codex-dual-agent-collaboration.md`（untracked，root 擁有；Codex 的檔案，未 stage）。

## Areas Codex Must Review
1. Initial HTML locale 是否真的正確（raw HTML，非瀏覽器） 2. 是否只是 CSS hide workaround（不是：無 visibility/opacity/overlay/setTimeout）
3. localStorage 是否仍主導 first render（否：只在無 cookie 的舊使用者一次性遷移） 4. cookie / 語系優先順序 5. cache pollution（見 Cache Verification）
6. hydration mismatch（引擎以 `<html lang>` 初始化；0 變更） 7. Header / Logo 8. Navbar 9. Mobile 10. Footer 11. `html lang`（en / zh-Hant）
12. metadata 13. SEO / AEO 14. no-JS baseline 15. security 16. regression（52 頁版號、7 頁引擎修補、首頁聊天框靜態狀態、nginx try_files 順序）。

## Deployment Notes（Codex PASS 後）
1. 記錄 rollback target：目前 `/var/www/shell.fans` 檔案 = commit `0d95c6e` 的版本；`/etc/nginx/sites-enabled/shell.fans.conf` 備份到 `~/shell.fans.conf.bak-<ts>`。
2. 逐檔 `cmp` 線上與 `0d95c6e`，確認無未回寫修改；`sudo install -m 644 -o www-data -g www-data` 52 個 HTML、7 個 `.en.html`、2 個 JS。
3. `sudo cp deploy/nginx/shell.fans.conf /etc/nginx/sites-enabled/shell.fans.conf && sudo nginx -t && sudo systemctl reload nginx`。
4. Smoke：`curl -k --resolve shell.fans:443:127.0.0.1 https://shell.fans/ -H 'Cookie: shellfans_locale=en'` → `lang="en"`；不帶 cookie → `zh-Hant`；
   經 Cloudflare 同樣兩種；`/index.en.html` 404；`python3 scripts/test-initial-locale-browser.cjs`（`SF_TEST_BASE=https://shell.fans`）。

## Rollback Plan
還原 nginx 設定備份 + `nginx -t` + reload；`git show 0d95c6e:<f>` 還原檔案。沒有 DB、沒有 Worker 變更。

## Production Verification Plan
見 Deployment Notes 第 4 點，另加 `scripts/test-agentic-surface.py`（線上）。

## Review Commit
本檔所在 commit（`git log -1 --format=%H -- docs/ai/HANDOFF.md`）；Base `0d95c6eb9b5ceb42af30da2e3b6ddb0d34aa2a34`。

## Branch
`main`

## Status
READY_FOR_CODEX_REVIEW

---

# 其他待 Codex 處理（未變）
- `ai-collab-init-20260913`：協作架構初始化（commit `0d95c6e`）— READY_FOR_CODEX_REVIEW。
- `global-ui-editor-20260913`：Global UI 編輯器（本 repo `bec00c3`；saas_womm `ef80336`，部署 `b70883d`）— DEPLOYED_PENDING_CODEX_VERIFICATION，
  細節見 commit `0d95c6e` 版本的 `docs/ai/HANDOFF.md`（`git show 0d95c6e:docs/ai/HANDOFF.md`）。
