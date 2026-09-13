# Current Task

## Task ID
ai-collab-init-20260913

## Goal
建立 Claude Code（Primary Implementer）× OpenAI Codex（Independent Reviewer）的永久協作架構：
`CLAUDE.md`、`AGENTS.md`、`docs/ai/{SHARED-RULES,CURRENT-TASK,HANDOFF,REVIEW,DECISIONS}.md`、
`prompts/claude-code-dual-agent-collaboration.md`。

## Scope
只新增協作文件。不修改任何頁面、腳本、資產、nginx、Cloudflare 或 `/var/www/shell.fans`。

## Allowed Areas
`CLAUDE.md`、`AGENTS.md`、`docs/ai/*`、`prompts/claude-code-dual-agent-collaboration.md`。

## Forbidden Changes
`*.html`、`js/**`、`css/**`、`scripts/**`、`workers/**`、`docs/memory/**`、`prompts/codex-dual-agent-collaboration.md`
（Codex 的檔案，root 擁有，未追蹤）；production 任何變更。

## Acceptance Criteria
1. 上述 8 個檔案存在，內容一致（角色、生命週期、狀態詞彙、Gate 規則、secrets 規則）。
2. `CLAUDE.md` 明確定義 Claude = PRIMARY IMPLEMENTER 並要求每次讀 `docs/ai/*`。
3. `AGENTS.md` 明確定義 Codex = INDEPENDENT REVIEWER，預設不改產品 source、不部署、不 push feature code。
4. `git diff --stat` 只含協作文件。
5. Commit `chore(ai): initialize Claude and Codex collaboration workflow` 已 push，remote 含該 SHA。
6. 同一套結構同步建立在 `shellfans-dev/saas_womm`，Task ID 相同。

## Repository
`shellfans-dev/shell.fans`（215 工作樹 `/home/kirin/work/shell.fans-static`）

## Branch
`main`

## Base Commit
`bec00c31a0b616c751f586c1664188c32f4adacc`（feat: Global UI runtime 掛載全站，並恢復由 CMS 驅動的頁尾）

## Review Commit
本檔所在的 commit（`git log -1 --format=%H -- docs/ai/CURRENT-TASK.md`）；HANDOFF.md 內以 SHA 記錄。

## Production Branch
`main`（部署 = 複製到 215 `/var/www/shell.fans`）。本任務為文件變更，不部署。

## Sibling Repository
`shellfans-dev/saas_womm` `feat/shellfans-crawler-monitor`：Base `ef80336db76f5fb5e9e6b3f88f04aaefd117d31c`，同 Task ID 的對應 commit 見該 repo 的 `docs/ai/HANDOFF.md`。

## Status
READY_FOR_CODEX_REVIEW
