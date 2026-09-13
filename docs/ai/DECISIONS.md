# Decisions — 長期有效的架構與流程決策

只記錄具長期效力的決策；短期 debugging 資訊不放這裡。每條附日期與依據。
（正本在 `shellfans-dev/saas_womm`，`shellfans-dev/shell.fans` 為同步副本。）

## D-001 雙 Agent 角色（2026-09-13）
Claude Code = PRIMARY IMPLEMENTER；OpenAI Codex = INDEPENDENT REVIEWER。Codex 預設不修改產品 source、不部署、
不 push feature code；改派需使用者明確指示。Claude 不得宣告 Codex PASS。依據：`prompts/*-dual-agent-collaboration.md`。

## D-002 Repo 佈局（2026-09-13）
| Repo | 內容 | 執行位置 |
|---|---|---|
| `shellfans-dev/saas_womm` | console.shell.fans（後台）、kol.fans、cs.shell.fans 的 Next.js app 與 API | coder1bot（pm2 `saas-womm`） |
| `shellfans-dev/shell.fans` | shell.fans 純靜態站（HTML/CSS/JS + python 產生器） | 215 `/var/www/shell.fans`（nginx） |

兩個 repo 各自有完整 `CLAUDE.md` / `AGENTS.md` / `docs/ai/`；`SHARED-RULES.md` 與本檔內容相同。

## D-003 Production dirty tree 不直接操作（2026-09-13）
coder1bot `~/saas_womm`（branch `review/spec-understanding`）含多個未提交修改，屬其他既有工作。任何 Agent 不得對它
pull / merge / rebase / checkout / reset / stash / clean，也不得把它當部署來源。

## D-004 部署採 clean worktree / release directory（2026-09-13）
saas_womm 由 GitHub exact commit 建 `~/shellfans-deployments/<timestamp>/saas_womm`（`git worktree add -b release/<ts>-<slug>`），
`npm ci` → lint/typecheck/test/build → 複製 `.env.local`、`public/uploads` symlink 到共用儲存 → 只切換 pm2 `saas-womm` 的 cwd
（`pm2 delete` + `pm2 start <release ecosystem> --only saas-womm` + `pm2 save`）。rollback = 指回前一個 release 目錄。
部署的 SHA 必須存在於 GitHub（release 分支）。

## D-005 Production branch（2026-09-13）
saas_womm：GitHub `review/spec-understanding` 代表目前 production（fast-forward 到已部署的 release 分支尖端）；
`main` 不是 production。shell.fans：`main` 即 production 內容，部署 = 複製到 `/var/www/shell.fans`。

## D-006 部署不跑 migration（既有決策，2026-06-15 記錄）
saas_womm 部署流程不執行 `drizzle-kit migrate`。新增資料表／欄位以冪等 DDL 放在 `src/db/manual/`，部署前手動套用；
設定類資料優先放 `system_settings`（jsonb）而非新表。

## D-007 Desktop / Mobile navigation 共用資料模型（2026-09-13）
導覽只有一份資料（`navigation[]`），desktop / mobile 是同一筆資料的兩個顯示旗標；禁止維護兩套選單 JSON。

## D-008 不建立重複的 Footer CMS（2026-09-13）
Footer 內容由既有「UIUX Design → Footer 頁尾」（`footer_settings__shell`）管理；Global UI 只補雙語 logo 與 draft/publish 之外的缺口。
新功能 reuse / extend 既有設定中心，不另造第二套。

## D-009 前台保留 no-JS baseline，runtime 只套用差異（2026-09-13）
shell.fans 每頁靜態 HTML 內建完整 header / nav / footer 與 `<a href>`，供爬蟲與無 JS 環境使用。
runtime（`js/sf-global-ui.js`、`js/sf-footer.js`）只依已發布設定就地調整；API 逾時／失敗／格式異常／後端 fallback 一律保留靜態版本。
不得把 canonical、hreflang、JSON-LD、robots.txt、sitemap.xml、llms.txt 交給 runtime 產生。

## D-010 前台只讀 published；後台 draft → preview → publish → rollback（2026-09-13）
公開 API 永不回 draft；至少保留上一個 published 供回復；發布前 server-side 驗證（協定白名單、必填、圖片路徑、排序）。

## D-011 CMS 化不得改變視覺（2026-09-13）
新的設定驅動功能，其程式碼預設值必須等於當時線上實況（「導入前視覺 ≈ 導入後視覺」）；首次發布不得造成內容變化。

## D-012 靜態資產以 query-string 版號更新（2026-09-13）
`/js/*.js`、`/css/*.css` 走 30 天 immutable 快取。改動後在 HTML 內升版號（`?v=YYYYMMDDx`）而非依賴 Cloudflare purge。
HTML 本身 no-cache。

## D-013 Cloudflare Worker 會改寫 shell.fans HTML（既有決策，2026-07-02）
Worker `shellfans-product-flags` 依產品開關在邊緣移除 `a[data-sf-product]`。比對 repo 與線上請用 origin
（`curl -k --resolve shell.fans:443:127.0.0.1`），不要用經 CF 的 HTML 判斷「是否部署」。

## D-014 協作文件不含 secrets（2026-09-13）
見 `SHARED-RULES.md` §9。憑證只記來源與名稱。
