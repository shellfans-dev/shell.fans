# ShellFans Initial Locale Rendering Fix
# 修正 shell.fans 首屏先中文再切英文的問題

**保存日期**：2026-09-13　**Task ID**：`fix-initial-locale-render`　**協作流程**：`CLAUDE.md` / `AGENTS.md` / `docs/ai/*`

目標網站：https://shell.fans/

---

## 任務背景

目前 shell.fans 有明確的語系初始渲染問題：當使用者的網站語系已經是 English 時，開啟 https://shell.fans/
會出現「繁體中文 → 頁面載入 / JavaScript 執行 → English」。這是不正確的 UX。

正確行為：如果最終 locale = English，第一個可見 Frame 就必須直接是 English；禁止「中文 → English」。
同樣地，locale = zh-TW 時第一個可見 Frame 就必須直接是繁體中文。

這次要解決的是「Initial locale / first render / SSR / static HTML / hydration」的根本問題，不是用 CSS 把中文畫面藏起來。

## 0. 遵守目前雙 Agent 開發流程

若 repository 已存在 `CLAUDE.md`、`AGENTS.md`、`docs/ai/SHARED-RULES.md`、`docs/ai/CURRENT-TASK.md`、`docs/ai/HANDOFF.md`、
`docs/ai/REVIEW.md`、`docs/ai/DECISIONS.md`，先完整閱讀。你目前角色：PRIMARY IMPLEMENTER；OpenAI Codex 是 INDEPENDENT REVIEWER。

本次正常流程：Claude Code → Inspect → Implement → Test → Build → Commit → Push → HANDOFF → READY_FOR_CODEX_REVIEW。
在 Codex `FINAL STATUS: PASS` 之前，不要自行進行新的 Production Deployment，除非目前 repository 的使用者指令明確要求跳過 Review Gate。

## 1. 修改前先檢查主機

先執行 `date`、`hostname`、`pwd`、`uptime`、`nproc`、`free -h`、`df -h`。目前主機預期約 CPU 16 Core、RAM 32 GB，但以實際結果為準。
若主機仍有極低 available memory、大量 swap thrashing、filesystem 空間不足、極高 load：停止 heavy build，先回報異常。

## 2. Git 安全檢查

修改前：`git status`、`git status --short`、`git branch --show-current`、`git rev-parse HEAD`、`git remote -v`、`git fetch --all --prune`、
`git log --oneline -10`。禁止 `git reset --hard`、`git clean`、`git checkout .`、`git restore .`、`git stash`、`git pull` 去處理目前 dirty working tree。
若有 unrelated 未提交修改：全部保留。先區分 A. 本任務相關 B. 其他既有修改 C. 不明來源修改；不可覆蓋 B / C。

## 3. 建立 CURRENT-TASK

更新 `docs/ai/CURRENT-TASK.md`。Task ID 建議 `fix-initial-locale-render`。Goal：修正 shell.fans 在 English locale 下第一個 Render
先出現繁體中文再切換英文的問題。Acceptance Criteria 至少包含：

1. English 使用者第一個可見 Frame 直接是 English。 2. zh-TW 第一個可見 Frame 直接是繁體中文。 3. 不再出現 incorrect-language flash。
4. 不用 visibility:hidden / opacity:0 掩蓋問題。 5. Server/static HTML 與 final locale 一致。 6. Header locale 正確。 7. Logo locale 正確。
8. Navbar locale 正確。 9. Mobile Menu locale 正確。 10. Hero / Body locale 正確。 11. Footer locale 正確。 12. html lang 正確。
13. SEO metadata 不產生 locale mismatch。 14. 不破壞 AEO/GEO / SSR / No-JS baseline。 15. 不造成 Hydration mismatch。 16. Reload 後 locale 保持正確。

## 4. 先找出真正 Root Cause

不要直接修改。完整搜尋 localStorage、sessionStorage、cookie、document.cookie、locale、language、lang、i18n、navigator.language、
navigator.languages、Accept-Language、DOMContentLoaded、hydrate、hydration、setLanguage、changeLanguage、applyLanguage、data-i18n、
document.documentElement.lang，以及 sf-global-ui、global-ui、Header、Navbar、MobileMenu、Footer、Logo。確認目前真正流程。

必須回答：1. Server / static HTML 預設輸出哪個 locale？ 2. English preference 現在存在哪裡？ 3. localStorage？ 4. cookie？
5. database user preference？ 6. URL？ 7. navigator.language？ 8. client-side global state？ 9. JavaScript 何時開始切換語言？
10. 哪個 script / component 實際造成中文 → English？ 不要靠猜測修。

## 5. 檢查 Initial HTML

自行檢查 `curl -sL https://shell.fans/`，確認 raw HTML 的 `<html lang>`、title、meta description、Header、Navbar、Hero、Footer
第一次回傳的內容到底是哪個語系。若 production 使用 CDN / reverse proxy，同時研究 Nginx、Cloudflare、CDN、SSR cache、page cache、middleware 等實際 architecture。

## 6. 根本修正原則

核心要求：Locale 必須在「瀏覽器第一次把主要頁面畫出來之前」確定。

禁止現在這種：Server/static HTML = zh-TW ↓ Browser render ↓ Client JavaScript ↓ localStorage=en ↓ replace content ↓ English。
必須改為：Request ↓ resolve locale ↓ render correct locale ↓ browser first paint ↓ hydrate same locale。

## 7. Locale Resolution Priority

先研究現有 architecture，不要硬套全新系統。若現有系統沒有明確優先順序，建議：1. Explicit locale URL 2. Persisted locale cookie
3. Logged-in user locale preference 4. Accept-Language 5. Existing project default locale。但實際 implementation 必須遵守目前專案 architecture。
最重要：localStorage 不可以再成為「決定第一次 render 語系」的唯一依據，因為 server 無法在 response 前讀 localStorage。

## 8. URL Locale 策略

先確認目前 shell.fans 是否已存在 `/en`、`/en/`、`/en/xxx` 或其他 locale route architecture。若已經存在，優先使用既有 localized routes，
不要建立第二套（例如 `/` → zh-TW、`/en/` → English；preference = en 時可在 request / middleware 層 `/` → `/en/`）。
若專案目前沒有 localized routes，不要為了這一個 bug 直接大規模重構整個網站 URL；此時優先評估 Cookie + SSR / middleware locale 等最小且正確的 architecture。

## 9. Cookie Locale

若目前 English preference 只存在 localStorage，評估將 locale 同時寫入 server-readable cookie（例如概念 `shellfans_locale=en`，或依現有 naming convention）。
切換語言時：English → 更新 client state → 更新 server-readable locale cookie；zh-TW 同樣更新 cookie。下次 Request 時 Server / Middleware 可以直接 resolve locale。
Cookie 設定必須合理：Path=/、SameSite、Secure（HTTPS production）、Max-Age / Expires。不要把 locale cookie 設成 HttpOnly（client-side 切換需要更新），但依實際 architecture 判斷。Locale cookie 不包含敏感資料。

## 10. First Visit

若使用者從未設定語言：依現有 business rule 處理。若目前規則是預設 zh-TW，則保持。若目前設計是依 browser Accept-Language，
則 server/middleware 必須在第一個 response 前處理。不得先輸出中文，再靠 navigator.language 在 client 改英文。

## 11. Header / Logo 同步修正

這次不能只修 Hero 文案。locale = English 時第一個 Frame 必須已經是 English Header、English Logo、English Navbar；zh-TW 反之。
目前英文 Logo 已經有既有實作，先確認現有 asset 與 locale logic。不得重新建立第三套 Logo 系統。Global UI / Header CMS 如果存在，必須沿用。

## 12. Mobile Menu

確認 English locale 時 Mobile Header、Mobile Menu、CTA、Language selector 第一個 render 也不能先中文再英文。不要只測 desktop。

## 13. Footer

Footer 也必須符合 initial locale。若 Footer 已有獨立 footer-settings / Global UI / CMS，必須沿用現有資料，不要建立第二套 Footer locale system。

## 14. Global UI 相容性

若目前已存在 `/api/site/global-ui`、global-ui settings、`sf-global-ui.js`、Global UI CMS，確認它是不是造成「static Chinese baseline + runtime English replacement」。
若是，不得直接把 static baseline 移除（ShellFans 需要 No-JS / AEO / SEO / AI crawler 可讀）；應改成 server/static baseline 本身就是正確 locale，而不是所有內容等待 JS API 回來才出現。

## 15. No-JS / AEO / SEO 保護

禁止修成「Empty HTML ↓ JavaScript ↓ English content」，也禁止「中文 HTML ↓ JavaScript ↓ English content」。
正確：English request / preference ↓ English HTML ↓ JavaScript enhancement；zh-TW 反之。
確認 crawler 在不執行 client JS 情況下仍能看到 Header、Navigation、Hero、主要正文、Footer、internal links；Navigation 必須保留 `<a href="...">`。

## 16. html lang

locale = English：`<html lang="en">`；locale = Traditional Chinese：使用現有專案正確值（例如 zh-TW 或 zh-Hant-TW），不要自行創造與現有 hreflang 不一致的 locale code。

## 17. Metadata

確認初始 response 的 title、meta description、OpenGraph locale、localized OpenGraph copy、localized structured data（如果原本就有）與實際 locale 一致。
不能 `<html lang="en">` 但 `<title>中文...</title>`，或英文畫面 + 中文 description。

## 18. canonical / hreflang

不要任意重新設計 SEO architecture，但必須檢查 canonical、hreflang 是否因 locale 修改產生錯誤。若目前已有 zh-TW / English alternate，保留並修正必要的一致性問題。
若目前完全沒有 localized URL，不要在本任務自行大規模建立新 SEO URL architecture，除非為解決根因確實必要。

## 19. Cache

若同一個 URL `/` 可能根據 cookie 回 zh-TW HTML 或 English HTML，一定要檢查 CDN cache、Nginx cache、SSR cache、application cache、browser cache，
避免中文 User 產生 cache 讓 English User 取得中文 HTML（或反過來）。若 architecture 使用 cookie variation，正確設計 Vary / Cache Key / private-public cache / revalidation，
依實際 stack 實作。不要盲目加入 `Vary: Cookie` 如果那會破壞整站 CDN cache。若 localized URL 已存在，優先使用 URL 做 cache separation。

## 20. Hydration

若是 React / Next.js / Vue / Nuxt 或其他 hydration architecture，Server locale 與 Client first locale 必須完全一致，避免 Hydration failed / Text content did not match。
Client-side store 初始化時應使用 server 已 resolve 的 locale，不要重新從另一個來源覆蓋 first render。

## 21. localStorage 可以保留，但降級角色

localStorage 可以保留作為 client-side preference cache / UI state helper / backward compatibility，但不能再是唯一 initial locale source。
若舊使用者目前只有 localStorage=en，考慮 migration strategy（首次 client hydration 發現舊 localStorage preference，同步寫入 cookie），但要避免再次造成中文 → English flash。
若無法在第一次 request 知道舊 localStorage，允許一次性的 legacy migration strategy，但最終穩定後後續 request 必須 server-readable。

## 22. 禁止 Fake Fix

嚴格禁止 `html { visibility: hidden; }`、opacity: 0、display: none、loading overlay、blank screen、等 locale loaded 再顯示、用 setTimeout 延遲 display 當正式解法。這些只是掩蓋問題，不得作為 PASS 條件。

## 23. 禁止 DOM Hack

不要用 document.querySelector(...)、innerHTML、手動遍歷 DOM、大量 replace text 來解決 initial locale。必須修 locale state / rendering architecture。

## 24. Language Switch UX

zh-TW → English 應立即正確切換；English → zh-TW 也應立即切換。若 architecture 採 localized URL，允許正常 navigation / redirect；
若採 cookie + SSR，切換後可以 client state update + cookie update。最重要：Reload 之後仍是正確 locale，且第一 Frame 正確。

## 25. Back / Forward

測試 Language switch、Reload、Back、Forward、New tab：locale 不應亂跳。

## 26. Direct URL

測試直接開 https://shell.fans/ 以及網站已有的 pricing、AEO/GEO、case studies、其他共用 Layout 頁。若它們共用 locale bootstrap，一起修正 shared root；不要只 patch Homepage。

## 27. Auth / Login 狀態

若登入用戶有 profile locale，檢查其優先權，但不要為本任務大幅修改 auth。Locale resolution 必須不破壞 login session。

## 28. Source Search

修改前至少搜尋：`rg -n "localStorage|sessionStorage|navigator.language|navigator.languages|locale|language|setLanguage|changeLanguage|applyLanguage|document.documentElement.lang|data-i18n|global-ui|sf-global-ui" .`
（依專案實際工具調整；不要掃 node_modules、.next、dist、build、.git 等大型 generated directories。）

## 29. Automated Tests

新增或更新針對本 bug 的測試，至少覆蓋：A. zh-TW initial locale B. English initial locale C. English persisted preference D. zh-TW persisted preference
E. language switch F. reload persistence G. Header logo locale H. Navbar locale I. Footer locale J. html lang K. fallback locale L. invalid locale
M. hydration consistency（如適用）。若 architecture 有 middleware，測 middleware locale resolution。

## 30. Raw HTML Verification

不只用 Browser 看，需要驗證 server/raw HTML（例如 curl）。English request / route / cookie 的 response HTML 中應有 `<html lang="en">`、English Header、
English content、English Footer，且不應包含「第一個 Render 用的繁體中文主要 UI」；zh-TW 反向驗證。

## 31. Browser Verification

若 repository 已有 Playwright / Puppeteer / Browser test，用現有工具；不要為了本任務引入大型新 Browser dependency。至少驗證 Desktop 1440px、Tablet 768px、Mobile 390px。
English：Hard reload 第一 Frame 不可出現繁體中文；zh-TW：第一 Frame 不可短暫出現 English。

## 32. Slow Network 測試

若現有 browser tooling 支援，測試 Slow 3G / network throttle——正常高速網路可能看不出 flash。在 JavaScript 較晚執行時，English 頁面仍不能先露出中文。這是判斷是否真正修好的重要測試。

## 33. JavaScript Disabled Test

如現有測試工具合理支援，關閉 JavaScript 測試：English locale 仍應看到 English baseline；zh-TW 仍應看到 zh-TW baseline。
若 current architecture 無法支援 JS-disabled locale persistence，至少確保 canonical localized route / server-rendered route 可以被 crawler 正確取得。

## 34. Performance

不要為了 locale 修正增加多支 blocking API、先 fetch locale 再 render、造成更慢 TTFB、造成額外 layout shift。Locale resolution 應盡量在 request / middleware / server render / routing 階段完成。

## 35. CLS

確認 Logo、Navbar、Hero、Footer 語言不同時不會產生明顯 layout shift。特別是英文 Logo 與中文 Logo：保持現有尺寸 / max-height / aspect ratio 規則。

## 36. Build / Test

先看 package.json、CI、README、deployment scripts 找出真正 command。依序執行 lint、typecheck、targeted tests、full tests、build。不要同時平行跑大量 heavy jobs。

## 37. Git Diff Review

完成後 `git status`、`git diff`、`git diff --stat`。檢查是否意外修改 robots.txt、sitemap、llms.txt、schema、unrelated AEO pages、unrelated backend、unrelated admin。
若不是必要修改，不得納入本任務；但不得覆蓋別人原本的 dirty change。

## 38. Prompt 保存

把本次完整工作規範保存為 `prompts/fix-initial-locale-render.md`，需要保存中英文雙語版本。若 prompts/ 已有 naming convention，依既有 convention 微調檔名即可。

## 39. Commit

只有在 Implementation PASS、Tests PASS、Build PASS、Self-review PASS 後才 Commit。建議 commit message：`fix(i18n): render correct locale on initial page load`
（若實際 architecture 更適合其他 wording，可合理調整）。只 commit 本任務檔案；若某檔案混有 unrelated changes，使用 `git add -p`。

## 40. Push GitHub

Commit 後 `git push`，必須 push GitHub，禁止 force push，確認 remote branch 已包含 exact commit。

## 41. Handoff 給 Codex

更新 `docs/ai/HANDOFF.md`，至少包含：Task（Fix initial locale rendering flash）、Root Cause（必須寫實際找到的 root cause）、Previous Behavior、
New Architecture（URL / Cookie / Middleware / SSR / Static generation / Client hydration 如何協作）、Locale Resolution Priority、Modified Files、Tests、
Raw HTML Verification、Browser Verification、Slow Network Verification、No-JS / Crawler Verification、SEO / AEO Verification、Cache Verification、
Known Risks、Review Commit、Branch，Status: READY_FOR_CODEX_REVIEW。

## 42. Codex Review 重點

要求 Codex 特別 Review：1. Initial HTML locale 是否真的正確 2. 是否只是 CSS hide workaround 3. localStorage 是否仍主導 first render 4. Cookie / locale priority
5. Cache pollution 6. hydration mismatch 7. Header / Logo 8. Navbar 9. Mobile 10. Footer 11. html lang 12. metadata 13. SEO / AEO 14. no-JS baseline 15. security 16. regression。

## 43. 完成狀態

本輪 Claude Code 完成後，若雙 Agent Protocol 正常啟用，不要直接宣告 Production 完成。最後狀態：READY_FOR_CODEX_REVIEW，並回報：
1. Root cause 2. Old locale flow 3. New locale flow 4. Persistence mechanism 5. Cookie / URL / server implementation 6. Cache implementation 7. Header result
8. Logo result 9. Navbar result 10. Mobile result 11. Footer result 12. html lang result 13. raw HTML verification 14. slow network result
15. JavaScript-disabled/crawler result 16. lint 17. typecheck 18. tests 19. build 20. modified files 21. prompt file 22. commit SHA 23. branch 24. push result 25. HANDOFF status。

---

# ENGLISH TASK SPECIFICATION

Fix the initial locale rendering problem on https://shell.fans/.

Current behavior: a user whose effective locale is English can initially see Traditional Chinese content before client-side JavaScript
changes the page to English. This is incorrect. If the effective locale is English, the first visible frame must already be English.

Do not solve this by hiding the document until JavaScript runs. Do not use visibility:hidden, opacity:0, blank loading screens, setTimeout,
or manual DOM text replacement as the primary fix.

Determine the actual root cause first. Inspect localStorage, cookies, locale state, browser language, routing, middleware, SSR, static
generation, hydration, Global UI runtime, Header, Navbar, Mobile Menu, Footer, Logo. Determine how the initial HTML locale is currently
selected and how the final client locale is selected.

The correct architecture is: request → resolve locale before first render → generate/render the correct localized HTML → browser first
paint → hydrate using the same locale. The server-rendered or statically served HTML and the client's first locale must match.

If the current implementation stores locale only in localStorage, introduce or reuse a server-readable persistence mechanism, normally a
locale cookie or an existing localized URL architecture. Do not create a second i18n system. If localized routes already exist, reuse them.
If they do not exist, do not redesign the entire URL architecture unless necessary to solve the root cause.

When the same URL can serve different locales, inspect CDN, reverse-proxy, SSR and application caching carefully to prevent cross-locale
cache pollution. Do not blindly add Vary: Cookie without understanding the impact on existing caching.

Preserve the existing no-JavaScript / server-rendered baseline required by ShellFans SEO and AEO/GEO architecture. Do not change the site
into an empty HTML shell that waits for JavaScript to fetch localized content.

For English, the initial response should already contain the appropriate html lang, Header, English logo, Navbar, Hero/content, Footer,
and localized metadata where applicable. For Traditional Chinese, the inverse must be true. Preserve crawlable semantic anchor links.
Prevent hydration mismatch.

Test: English initial render, Traditional Chinese initial render, persisted locale, language switching, reload, back/forward, desktop,
tablet, mobile, English logo, Chinese logo, Header, Navbar, Mobile Menu, Footer, html lang, metadata, invalid locale fallback, raw response
HTML, slow network behavior, crawler/no-JS behavior where supported.

Use existing repository browser tooling if available. Do not add a large browser-testing dependency solely for this task.
Run the real repository lint, typecheck, targeted tests, full tests, build in a safe sequence. Preserve unrelated dirty working-tree changes.
Never use destructive Git commands to simplify the task.

Save the full bilingual task specification to `prompts/fix-initial-locale-render.md`. Commit only the changes required for this bug.
Suggested commit: `fix(i18n): render correct locale on initial page load`. Push the commit to GitHub.

Then update `docs/ai/HANDOFF.md` with exact evidence and set the task status to READY_FOR_CODEX_REVIEW.
Do not mark the production task complete until the independent Codex review gate has passed.
