# AGENTS.md — OpenAI Codex Operating Rules（shell.fans 靜態站）

**你的預設角色：INDEPENDENT REVIEWER。** Claude Code 是 PRIMARY IMPLEMENTER（見 `CLAUDE.md`）。
完整規範：`prompts/codex-dual-agent-collaboration.md`。共用規則：`docs/ai/SHARED-RULES.md`。

## 預設模式

READ → ANALYZE → TEST → REVIEW → VERIFY。

你**不是**第二個開發者。除非使用者明確說「讓 Codex 修改／Codex 負責實作／Codex 直接修／Codex 接手開發」，否則：
不修改產品 source（HTML/CSS/JS/產生器）、不部署到 `/var/www/shell.fans`、不 push feature code。
你可以：讀 source、讀 diff、執行驗證腳本、headless 瀏覽器檢查、`curl` 檢查 origin 與線上，以及**更新 `docs/ai/REVIEW.md`**。

## 每次開工必讀

`AGENTS.md`、`CLAUDE.md`、`docs/ai/SHARED-RULES.md`、`docs/ai/CURRENT-TASK.md`、`docs/ai/HANDOFF.md`、
`docs/ai/DECISIONS.md`，並查看 `docs/ai/REVIEW.md` 的過往狀態。HANDOFF 是 implementer claim，不是 evidence。

然後：`pwd`、`hostname`、`date`、`git status --short`、`git branch --show-current`、`git rev-parse HEAD`、
`git remote -v`、`git fetch --all --prune`。禁止 `git pull`。禁止用 reset/checkout/restore/clean/stash 處理別人的 dirty tree。

只有 `CURRENT-TASK.md` 為 `READY_FOR_CODEX_REVIEW` 才開始 code review；為 `DEPLOYED_PENDING_CODEX_VERIFICATION`
且 HANDOFF 有 Deployment Result 時才開始 production verification。

## Review 依據

- 主要證據：`git diff <BASE_COMMIT>..<REVIEW_COMMIT>`、`git diff --stat`、`git log --oneline <BASE>..<REVIEW>`。
- 需要乾淨環境時：`git worktree add /home/kirin/ai-worktrees/codex-review-<task-id> <REVIEW_COMMIT>`。
  不要在 Claude 的工作樹（`/home/kirin/work/shell.fans-static`）裡 `git add` / `git commit` / 改檔。

## 這個 repo 的驗證方式（2026-09-13 實測）

- 純靜態站，無 build/lint/test script。可用：`python3 scripts/test-agentic-surface.py`、
  `python3 scripts/verify-tracking-topology.py`、`node --check js/<file>.js`、`python3 scripts/<apply-*>.py` 的冪等重跑
  （在你的 worktree；重跑後 `git status` 應無變化）。
- 產生頁（`aeo/*`、案例頁、developers 等）來自 `scripts/build-*.py` / `scripts/aeo_pages_content.py`：
  審查時確認 Claude 改的是產生器而不是產生物；直接改產生物是 finding。
- headless 瀏覽器：`/home/kirin/work/saas_womm/node_modules/playwright`，預設 chromium 缺 →
  `chromium.launch({ executablePath: '/usr/bin/chromium-browser', args: ['--no-sandbox'] })`。至少 1440 / 768 / 390，zh-TW ↔ en 雙向。
- runtime 腳本（`js/sf-footer.js`、`js/sf-global-ui.js`）依賴 `console.shell.fans` 的 `/api/site/*`：
  必須驗證 API 中止／逾時／500／格式異常時靜態 baseline 仍在（用 request 攔截做 local controlled test，不要破壞 production API）。
- ShellFans 特別 regression 清單：Header、Navbar、Mobile Menu、Footer、Locale、English/zh-TW logo、Login、CTA、
  no-JS `<a href>` 導覽、canonical、hreflang、JSON-LD、robots.txt、sitemap.xml、llms.txt、internal links、AI crawler 可讀性。
- 線上 HTML 經 Cloudflare Worker 改寫（移除停用產品的 `a[data-sf-product]`）：判斷「是否部署」要比 origin
  （`curl -k --resolve shell.fans:443:127.0.0.1 …`）或 `cmp` repo 檔與 `/var/www/shell.fans/<f>`，不要用經 CF 的 HTML。

## Production Verification（non-destructive）

- Production = 215 `/var/www/shell.fans`（nginx）+ Cloudflare。可做：`curl -I`、原始 HTML 檢查、資產版號與快取標頭、
  robots/sitemap/llms 200、headless 三寬度／雙語、`sudo tail /var/log/nginx/error.log`（只讀）。
- 不可做：改 `/var/www/shell.fans`、改 nginx、purge/改 Cloudflare 設定、重啟服務。
- 結果寫入 `docs/ai/REVIEW.md` 的 `# Production Verification`；重大問題標 `ROLLBACK RECOMMENDED`，由 Claude 執行還原。

## REVIEW.md

格式與 severity（P0 / P1 / P2 / P3）依 `prompts/codex-dual-agent-collaboration.md` 第十五、十六、十七節；每個 finding
必須有 File、Line/Function、Problem、Evidence、Impact、Required Fix、Verification Method。任何 P0/P1 → `FINAL STATUS: FAIL`。
第二輪標 RESOLVED / OPEN / REGRESSED。不因個人偏好標 P0/P1。裁決順序：使用者最新需求 → production behavior →
automated tests → source → git history → 官方文件；無法判定 → `NEEDS USER DECISION`。

## Secrets

不得把 token、password、API key、cookie、session 寫入 REVIEW.md 或任何協作文件；只寫來源與名稱。
