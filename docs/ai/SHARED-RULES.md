# Shared Rules — Claude Code × OpenAI Codex

兩個 Agent 共同遵守的規則。個別角色規則見 `CLAUDE.md`（Claude）與 `AGENTS.md`（Codex）。
規範原文：`prompts/claude-code-dual-agent-collaboration.md`、`prompts/codex-dual-agent-collaboration.md`。

**正本**：本檔與 `DECISIONS.md` 在 `shellfans-dev/saas_womm` 與 `shellfans-dev/shell.fans` 兩個 repo 各有一份，
內容必須相同；以 `saas_womm` 的版本為正本，修改時同一任務內同步另一份。

## 1. 角色

| Agent | 角色 | 可以 | 不可以 |
|---|---|---|---|
| Claude Code | PRIMARY IMPLEMENTER | 分析、實作、測試、build、commit、push、handoff、修 review findings、Codex PASS 後部署 | 宣告 Codex PASS、改 `REVIEW.md` 的 status |
| OpenAI Codex | INDEPENDENT REVIEWER | 讀、分析、在自己的 worktree 跑測試/build、審 exact diff、寫 `REVIEW.md`、production verification | 修改產品 source、migration、runtime config；部署；push feature code（除非使用者明確改派） |

## 2. 生命週期與狀態

Understand → Implement → Test → Build → Commit → Push → HANDOFF → Codex Review → (FAIL：修正 → 新 commit → 再審)
→ PASS → Deploy → Claude Smoke Test → Codex Production Verification → DEPLOYED。

`CURRENT-TASK.md` 的 Status 只能是：`PLANNING`、`IMPLEMENTING`、`TESTING`、`READY_FOR_CODEX_REVIEW`、
`CHANGES_REQUESTED`、`READY_FOR_DEPLOY`、`DEPLOYED_PENDING_CODEX_VERIFICATION`、`DEPLOYED`、`BLOCKED`。

Gate 規則：任何 P0 或 P1 → 不得部署；只有 `FINAL STATUS: PASS` 才進正常部署；只有 Code Review PASS 且
Production Verification PASS 才是 `DEPLOYED`。

## 3. 開工前必做

`pwd`、`hostname`、`date`、`git status --short`、`git branch --show-current`、`git rev-parse HEAD`、
`git remote -v`、`git fetch --all --prune`、`git log --oneline -10`。**禁止 `git pull`。**

涉及 build/test/deploy 時另加 `nproc`、`free -h`、`df -h`、`uptime`（必要時 `vmstat 1 5`）。
available RAM 過低、swap 持續 si/so、kswapd 高 CPU、磁碟不足、load 異常 → 停止 heavy job。

## 4. Git 安全

- 禁止：`git reset --hard`、`git checkout .`、`git restore .`、`git clean`、`git stash`（除非使用者明確授權且已證明安全）。
- 禁止：`git push --force`、`git push --force-with-lease`。
- 未提交修改分三類：A 本任務、B 其他既有任務、C 不明來源。只 stage A；混合檔用 `git add -p`。禁止未確認就 `git add .`。
- 兩個 Agent 不得同時在同一 working tree 修改／`git add`／`git commit`。平行工作用不同 worktree、不同 branch。
- 最後一定 push GitHub，並用 `git rev-parse HEAD` 與 remote 比對。

## 5. 修改原則

Minimum Necessary Change。不順便做：大規模 refactor、整 repo format、framework/dependency upgrade、
rename unrelated files、改 unrelated architecture。不從頭重寫已完成的功能。

## 6. Evidence

所有主張都要有證據：commit SHA、diff、測試輸出、HTTP 狀態、route、檔案、log。禁止「應該沒問題」「看起來可以」。
HANDOFF 是 implementer claim，不是 reviewer evidence；REVIEW 的 finding 沒有 evidence 不得列為 blocking。
**Trust evidence, not agent claims.**

## 7. 部署與 Production

- Production working tree 若有未提交修改：不 pull、不 merge、不 rebase、不 checkout、不 reset。
- 部署一律從 GitHub exact commit 建 clean worktree / release directory → install → lint/typecheck/test → build → 切換 → smoke。
- 只 restart 受影響 service；禁止 `pm2 restart all`、`docker restart all`、`killall node`、`killall python`。
- 每次部署前記錄 rollback target；部署後出現 5xx、crash loop、核心 API/認證壞掉、重大 regression → 立即 rollback。
- Production 不做破壞性測試：不刪資料、不改正式設定、不 restart 全部服務來「測試」。
- 不要求使用者自行驗證；Agent 自己驗證並提供證據。

## 8. 資源

heavy job 依序：lint → typecheck → targeted tests → full tests → build；每步前後 `free -h`；
結束確認沒有 orphan build/test/browser process。不因 RAM 大就平行跑多個 heavy job。

## 9. Secrets

`CLAUDE.md`、`AGENTS.md`、`docs/ai/*`、`prompts/*` 不得含 password、token、API key、private key、DB credential、
cookie、session 值。只能寫「憑證存在」「來源檔案路徑／環境變數名稱」。

## 10. 多 repo 慣例

ShellFans 由多個 repo 組成（見 `DECISIONS.md` D-002）。跨 repo 任務使用同一個 Task ID，各 repo 的
`CURRENT-TASK.md` / `HANDOFF.md` 都要列出對方 repo 的 Base / Review Commit。Codex 依各 repo 各自的 Review Commit 審查。
