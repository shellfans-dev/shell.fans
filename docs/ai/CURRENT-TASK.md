# Current Task

## Task ID
fix-initial-locale-render

## Goal
修正 shell.fans 在 English 偏好下第一個可見 frame 先出現繁體中文、JavaScript 執行後才切成英文的問題。
最終 locale 為 English 時，伺服器回的 HTML 就必須是英文（header、logo、navbar、mobile menu、hero/body、footer、
`<html lang>`、metadata）；zh-TW 反之。不得以 CSS 隱藏或延遲顯示掩蓋。

## Scope
shell.fans 靜態站的語系決定與初始渲染：語系偏好的伺服器可讀持久化（cookie）、nginx 依 cookie 回對應語系的
預先產生英文頁、頁內 i18n 引擎以伺服器已決定的語系初始化、runtime 腳本（footer / Global UI）讀同一來源、
產生器與測試。不改 URL 架構、不重做 SEO 架構、不改 Cloudflare Worker。

## Allowed Areas
- 7 個有 i18n 引擎的頁面（`index.html`、`aeo-geo.html`、`aeo-geo/methodology.html`、`aeo-geo/taiwan-aeo-tools.html`、
  `social-media-backup.html`、`tools/aeo-geo-checker.html`、`what-is-shellfans.html`）內的引擎 bootstrap／`__setLocale`
- 新產生的英文版 `<page>.en.html`（7 個）與其產生器 `scripts/build-locale-pages.py`
- `scripts/apply-locale-bootstrap.py`（冪等引擎修補）、`scripts/apply-global-ui.py` 的資產版號
- `js/sf-footer.js`、`js/sf-global-ui.js` 的語系解析（cookie → localStorage → `<html lang>`）
- `deploy/nginx/shell.fans.conf`（cookie → `.en.html` 的 map / try_files）
- 測試：`scripts/test-initial-locale.py`、`scripts/test-initial-locale-browser.cjs`
- `docs/ai/*`、`prompts/fix-initial-locale-render.md`、`CLAUDE.md`（語系架構事實）

## Forbidden Changes
`robots.txt`、`sitemap.xml`、`llms.txt`、`llms-full.txt`、JSON-LD、canonical／hreflang 值、`workers/**`、
無 i18n 引擎的 44 個頁面內容、`/var/www/shell.fans`、`/etc/nginx`（部署留待 Codex PASS 後）、任何 saas_womm 產品程式。

## Acceptance Criteria
1. English 使用者（cookie `shellfans_locale=en`）第一個可見 frame 直接是 English。
2. zh-TW（無 cookie 或 cookie=zh-TW）第一個可見 frame 直接是繁體中文。
3. 不再出現 incorrect-language flash（以 JS 關閉、Slow 3G、mutation 計數三種方式驗證）。
4. 不用 visibility:hidden / opacity:0 / display:none / overlay / setTimeout 掩蓋。
5. Server/static HTML 與 final locale 一致（raw HTML 驗證）。
6. Header locale 正確。 7. Logo locale 正確。 8. Navbar locale 正確。 9. Mobile Menu locale 正確。
10. Hero / Body locale 正確。 11. Footer locale 正確。 12. `html lang` 正確（en / zh-Hant，與既有 hreflang 一致）。
13. title / description / og:title / og:description / og:locale 與 locale 一致。
14. 不破壞 AEO/GEO / no-JS baseline：兩種語系的 raw HTML 都保有完整 `<a href>` 導覽與正文。
15. 不造成 hydration mismatch：引擎以 `<html lang>` 初始化，applyTranslations 對已正確的頁面為 no-op。
16. Reload / back / forward / new tab 後 locale 保持正確。
17. 快取：同 URL 依 cookie 變化不會互相污染（HTML 在 CF 與瀏覽器都不快取、ETag 不同），並有文件說明。
18. 舊使用者（只有 localStorage=en）一次性遷移到 cookie，之後首屏正確。
19. `scripts/build-locale-pages.py --check` 可偵測英文版過期。

## Repository
`shellfans-dev/shell.fans`（215 工作樹 `/home/kirin/work/shell.fans-static`）

## Branch
`main`

## Base Commit
`0d95c6eb9b5ceb42af30da2e3b6ddb0d34aa2a34`

## Review Commit
本檔所在的 commit（`git log -1 --format=%H -- docs/ai/CURRENT-TASK.md`）；HANDOFF.md 內以同法記錄。

## Production Branch
`main`（部署 = 複製檔案到 215 `/var/www/shell.fans` + 更新 `/etc/nginx/sites-enabled/shell.fans.conf` + `nginx -t` + reload）

## Sibling Repository
`shellfans-dev/saas_womm`：本任務只同步 `docs/ai/DECISIONS.md`（新增語系決策），無產品程式變更。

## Status
READY_FOR_CODEX_REVIEW
