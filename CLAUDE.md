# CLAUDE.md — Claude Code Operating Rules（shell.fans 靜態站）

**你的角色：PRIMARY IMPLEMENTER。** OpenAI Codex 是 INDEPENDENT REVIEWER（見 `AGENTS.md`）。
完整規範：`prompts/claude-code-dual-agent-collaboration.md`。共用規則：`docs/ai/SHARED-RULES.md`。

## 每次開工必讀

1. `docs/ai/SHARED-RULES.md`
2. `docs/ai/CURRENT-TASK.md`（目前任務與 Status）
3. `docs/ai/HANDOFF.md`（上一次交接）
4. `docs/ai/REVIEW.md`（Codex 的審查結果；只讀，不得改 status）
5. `docs/ai/DECISIONS.md`（長期決策）
6. `docs/memory/shell-fans-aeo-performance-optimization-memory.md`（既有 SOP：新頁流程、header 慣例、Lighthouse 歷史）

然後執行 `pwd`、`hostname`、`date`、`git status --short`、`git branch --show-current`、`git rev-parse HEAD`、
`git remote -v`、`git fetch --all --prune`、`git log --oneline -10`。禁止 `git pull`。

## 你負責

Understand → Implement → Test → Build → Commit → Push → HANDOFF → 修正 Codex findings → Codex PASS 後 Deploy
→ Production Smoke Test → 交給 Codex Production Verification。

你不得：宣告 Codex PASS；修改 `docs/ai/REVIEW.md` 的 status；在 P0/P1 未解決時部署；要求使用者自行驗證。

## 這個 repo 的事實（2026-09-13 實測）

- **是什麼**：https://shell.fans 的純靜態站（HTML/CSS/JS），無 build、無 lint、無 test script。`aeo/` 知識叢集、
  案例頁、developers 頁等由 `scripts/build-*.py` 與 `scripts/aeo_pages_content.py` 產生——**改產生器再重跑，不要直接改產生的 HTML**。
  `scripts/apply-*.py`、`scripts/mark-product-nav.py`、`scripts/apply-global-ui.py` 等是冪等修補腳本。
- **驗證工具**：`python3 scripts/test-agentic-surface.py`、`python3 scripts/verify-tracking-topology.py`；
  headless 瀏覽器用 `/home/kirin/work/saas_womm/node_modules/playwright`（預設 chromium 缺，改
  `executablePath: '/usr/bin/chromium-browser'` + `--no-sandbox`），至少驗 1440 / 768 / 390 與 zh-TW ↔ en。
- **工作樹與部署**：215 `/home/kirin/work/shell.fans-static`（branch `main` = production 內容）。部署 = 複製到
  `/var/www/shell.fans`（nginx，www-data 可讀）：先 `git show HEAD:<f> | cmp - /var/www/shell.fans/<f>` 確認線上沒有未回寫的直接修改，
  再 `sudo install -o www-data -g www-data -m 644 -D <f> /var/www/shell.fans/<f>`。
  HTML 為 no-cache；`/js/*`、`/css/*` 為 30 天 immutable → 改動後升 HTML 內的 `?v=` 版號（D-012），不要靠 CF purge。
- **Cloudflare**：Worker `shellfans-product-flags` 在邊緣依產品開關移除 `a[data-sf-product]`；線上 HTML ≠ origin HTML。
  比對 origin 用 `curl -k --resolve shell.fans:443:127.0.0.1 https://shell.fans/<path>`。
- **runtime 對 console.shell.fans 的依賴**：`/api/site/i18n?site=shell`、`/api/site/footer?site=shell`、
  `/api/site/global-ui?site=shell`。任何 runtime 都必須先渲染內建 baseline，API 逾時／失敗／格式異常一律保留內建（D-009）。
- **三種既有 nav 標記**：首頁型 `header.nav` + `#mobileMenu`；Webflow 內容頁 `.navbar.w-nav` + `nav.w-nav-menu`；
  由 `scripts/apply-unified-mobile-nav.py` 注入的行動版 `#sfMobMenu`。改共用元件要三種都顧到，禁止為單頁另寫一份。
- **i18n**：`data-i18n` 字典（頁內 BASE + `/api/site/i18n` 覆寫）、`localStorage.shellfans_locale`、
  `shellfans-locale-changed` 事件；zh-TW logo `images/nav_logo.svg`、en logo `images/nav_logo_en.png`。純中文頁固定中文。
- **AEO/GEO 紅線**：`<a href>` 導覽、canonical、hreflang、JSON-LD、`robots.txt`、`sitemap.xml`、`llms.txt`、`llms-full.txt`
  非任務要求不得變動；diff 中若出現要說明理由。
- **GitHub**：`shellfans-dev/shell.fans`。215 沒有 `gh`；push 用 `~/.gh-token` 搭配 `git -c credential.helper=<helper>`。
- **對應的後台 repo**：`shellfans-dev/saas_womm`（console.shell.fans API 與後台）；跨 repo 任務見 SHARED-RULES §10。

## 部署（Codex PASS 之後）

1. 記錄 rollback target：目前 `git rev-parse HEAD`、`curl -I https://shell.fans/`、要覆蓋的檔案清單。
2. 逐檔 `cmp` 線上與 HEAD~1，確認無未回寫修改；`install` 覆蓋；`chmod o+r` / 目錄 `o+rx`。
3. Smoke：origin 與經 CF 的 200、新版號資產 200、原始 HTML 仍含 `<a href>` 導覽、robots/sitemap/llms 200、
   headless 三寬度與中英切換無 JS 錯誤。失敗 → 用 `git show <前一 SHA>:<f>` 還原檔案。
4. 更新 `docs/ai/HANDOFF.md` Deployment Result，`CURRENT-TASK.md` → `DEPLOYED_PENDING_CODEX_VERIFICATION`。

## 資源與 Git 安全

見 `docs/ai/SHARED-RULES.md` §3、§4、§8。禁止 `git reset --hard`、`git checkout .`、`git restore .`、`git clean`、
`git stash`、force push。

## 文件維護

- 新任務：先寫 `docs/ai/CURRENT-TASK.md`；Commit + Push 後寫 `docs/ai/HANDOFF.md`（evidence-based），Status → READY_FOR_CODEX_REVIEW。
- 需求 prompt 存 `prompts/`；不得把 secrets 寫入任何協作文件。
