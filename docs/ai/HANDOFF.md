# Claude → Codex Handoff

## Task ID
ai-collab-init-20260913

## Task
雙 Agent 協作架構初始化（shell.fans 靜態站 repo）

## Goal
見 `docs/ai/CURRENT-TASK.md`。

## Acceptance Criteria
見 `docs/ai/CURRENT-TASK.md`（6 項）。

## Base Commit
`bec00c31a0b616c751f586c1664188c32f4adacc`

## Review Commit
本檔所在 commit（`git log -1 --format=%H -- docs/ai/HANDOFF.md`）。Codex 請以 `git log --oneline bec00c3..HEAD` 確認只有一個 commit。

## Branch
`main`

## Production Branch
`main`；本任務不部署。

## Modified Files
新增：`CLAUDE.md`、`AGENTS.md`、`docs/ai/SHARED-RULES.md`、`docs/ai/CURRENT-TASK.md`、`docs/ai/HANDOFF.md`、
`docs/ai/REVIEW.md`、`docs/ai/DECISIONS.md`、`prompts/claude-code-dual-agent-collaboration.md`。
修改：無。未追蹤且未納入：`prompts/codex-dual-agent-collaboration.md`（root 擁有、kirin 不可讀，屬 Codex／使用者；未動）。

## Architecture Changes
無（協作流程文件）。

## Database Changes
無。

## Migration Changes
無。

## API Changes
無。

## Frontend Changes
無。

## Admin Changes
無。

## Security Considerations
協作文件不含任何 secret 值；只記錄憑證來源路徑。`AGENTS.md` 限制 Codex 預設不得改產品 source／部署／push。

## Tests Executed

### Lint
NOT AVAILABLE（repo 無 lint；純 Markdown）

### Typecheck
NOT AVAILABLE

### Targeted Tests
NOT RUN（無程式碼變更）

### Full Tests
NOT RUN（無程式碼變更）

### Build
NOT AVAILABLE（靜態站無 build）

## Known Risks
- `SHARED-RULES.md` 與 `DECISIONS.md` 在兩個 repo 各一份，需同步維護（正本 saas_womm）。

## Existing Unrelated Dirty Files
`prompts/codex-dual-agent-collaboration.md`（untracked，root:root 640，2026-09-13 18:08 建立）。不屬本任務，未 stage。

## Areas Codex Must Review
1. `CLAUDE.md` / `AGENTS.md` 角色定義是否符合 `prompts/*-dual-agent-collaboration.md`。
2. `docs/ai/*` 之間的狀態詞彙、Gate 規則、secrets 規則是否一致，且與 saas_womm 的副本相同。
3. `git diff --stat bec00c3..HEAD` 是否只含協作文件。

## Deployment Notes
不部署。

## Rollback Plan
不適用（必要時 `git revert <Review Commit>`）。

## Production Verification Plan
不適用。

## Status
READY_FOR_CODEX_REVIEW

---

# 待審查的前一任務（協作流程建立前完成並已部署；建議作為 Codex 的第一個正式 Review 對象）

## Task ID
global-ui-editor-20260913

## 摘要
shell.fans 全站掛載 Global UI runtime（`js/sf-global-ui.js`）、恢復 `js/sf-footer.js` 對 console.shell.fans footer 設定的
runtime fetch、`scripts/apply-global-ui.py` 冪等注入 52 頁並升版號 `?v=20260913a`。後台端在 `shellfans-dev/saas_womm`
（commit `ef80336`，部署 `b70883d`）。

## Commits
| Repo | Base | Review Commit | 說明 |
|---|---|---|---|
| shell.fans | `fa5ec6a084a35755d10e75622b76eead2d9f35fa` | `bec00c31a0b616c751f586c1664188c32f4adacc` | 55 檔：52 HTML（只動 script 標籤）、2 JS、1 腳本 |
| saas_womm | `1d45c296a0b74bd040c8cf470ec753053f54c898` | `ef80336db76f5fb5e9e6b3f88f04aaefd117d31c` | Global UI 編輯器（後台／API／模型／測試） |

## 已執行的驗證（Claude claim，待 Codex 獨立確認）
- 本機 headless（request 攔截、mock API）78 項：CMS 順序／改名／新增／停用、三種 nav 標記、1440/768/390、中英雙向與 logo、
  API abort／500／fallback 旗標／格式異常／逾時五種情境皆保留靜態、`javascript:` 略過、標籤文字不注入、預設設定＝靜態頁逐項相同。
- 線上 61 項：三寬度、雙向語系、footer 內容來自 API 且與對齊後預設一致、Webflow 頁桌機與 overlay 選單、無 JS 錯誤。
- 原始 HTML（無 JS）：桌機 nav 5 條、行動版 7 條 `<a href>`；robots／sitemap／llms.txt／llms-full.txt 200；canonical 未變；
  `git show bec00c3 -- '*.html'` 除 script 標籤外無其他變更行。

## Deployment Result（2026-09-13 18:2x CST）
- 53 檔 `install -m 644` 到 `/var/www/shell.fans`（`aeo/case-studies/cet-taiwan.html` 線上本無此檔，未部署）；部署前逐檔 `cmp` 確認線上＝前一 commit。
- origin（`--resolve 127.0.0.1`）與 Cloudflare 皆 200；`/js/sf-global-ui.js?v=20260913a` 200，`cache-control: public, max-age=2592000, immutable`。
- Rollback：`git show fa5ec6a:<f>` 還原對應檔案。

## 該任務狀態
DEPLOYED_PENDING_CODEX_VERIFICATION（未經 Codex code review 即部署，因協作流程當時尚未建立）。
