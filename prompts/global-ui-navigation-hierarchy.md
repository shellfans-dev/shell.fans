# ShellFans Global UI Navigation Hierarchy
# ShellFans Global 共用元件 — Navigation 分層管理

> 任務 ID：`global-ui-navigation-hierarchy`（2026-09-14）。中文在前，English 在後。
> 後台：`https://console.shell.fans/_shellfans-admin712/uiux-design?tab=global-ui&site=shell`。
> 目標：在既有 Global UI → Navigation 加入 Parent/Child 兩層，**不重做整套 Global UI**。實作結果見 `docs/ai/HANDOFF.md`。

## 需求重點（中文）

- **層數**：Level 1 主選單 → Level 2 子選單，`MAX_DEPTH = 2`；不開放第三層。若現況已超過兩層須先分析、不得直接截斷（本站現況為單層，正規化時攤平第三層以上）。
- **資料模型**：沿用既有 `NavItem.children`（nested children，單一 source of truth）；不同時維護 parentId 與 children 兩份。舊單層資料自動視為 Level 1（`children` 缺省），不得重置正式導覽。
- **Level 1**：enabled、中英文 label、URL（可選）、外部連結、新分頁、桌機/手機可見、排序；可為「可點擊父層（有 URL + 子選單）」或「純下拉父層（無 URL，只展開子選單）」。
- **Level 2**：enabled、中英文 label、URL（必填）、外部/新分頁、桌機/手機可見、排序；不可再有子選單。
- **Admin**：新增/編輯/刪除主選單與子選單、啟用停用、排序（↑↓，同層內）、將子選單移到其他主選單；清楚顯示主/子層級；刪除含子選單的主選單須確認（一併刪除或先搬移），不得留 orphan。
- **驗證（server-side，發布前）**：全樹 id 唯一、URL 安全（拒 `javascript:`/`data:`/暫時性路徑）、子選單必須有 URL、純下拉父層可無 URL、既無 URL 又無子選單的父層 → 錯誤、同層 order 不重複、層數 ≤ 2、桌機至少一個可顯示項目。因為是 nested children，天生不會有 parentId 迴圈；孫層在正規化即被攤平且驗證會再擋一次。
- **停用連動**：父層停用 → 父層與子項前台皆不顯示（子項自身 enabled 不變）；子項停用只隱藏該子項；純下拉父層若某裝置無可見子項 → 不顯示空下拉。
- **前台**：桌機 = 下拉選單（hover/focus + 鍵盤，`aria-haspopup`/`aria-expanded`/`aria-controls`、Escape 收合、純下拉父層以 `role="button"` 開合）；手機 = 手風琴（每個父層一個 toggle 按鈕 + 縮排子選單）；子選單一律真正的 `<a href>`（可被爬蟲讀取），非 onclick。
- **i18n / 首屏**：沿用既有 locale 架構（`label.{zh-TW,en}`），不建立第三套翻譯；英文首屏直接英文、中文首屏直接中文。
- **SSR / No-JS / AEO**：shell.fans 為純靜態站，前台導覽由 `js/sf-global-ui.js` 於 runtime 依 API 就地同步。**扁平資料下本次前台改動為 no-op（不動現有 navbar）**；有子選單時才建立下拉/手風琴。⚠️ 已知取捨：純由 CMS 新增、靜態 HTML 沒有的子連結，屬 JS 漸進增強層，若要進 no-JS/爬蟲 baseline 需一併更新靜態產生器；本站現況導覽為單層，故無立即影響。robots/sitemap/llms/canonical/hreflang/JSON-LD 不變動。
- **API**：`/api/site/global-ui` 一次回傳含 nested `children` 的樹（單一 contract，不維護兩份 hierarchy）。
- **Draft/Publish/Rollback**：hierarchy 修改先進 draft；正式 shell.fans 只讀 published；rollback 會連 parent-child/order/visibility/label 一起還原（record 快照整份 settings）。
- **卡片**：Navigation 卡片顯示「N 主選單 · M 子選單」摘要，展開才是階層編輯器，沿用現有 Admin Design System。
- **不要**：把 Prompt 範例（Products/ShellFans/KOL.FANS…）寫進正式資料；正式資料以現況 production Navigation 為準。
- **測試 / Git**：新增自動化測試（見下）；依 repo 真正 scripts 跑 lint/typecheck/test/build；只 commit 本任務修改（禁 `git add .`、禁 force push）；commit `feat(admin): add hierarchical global navigation editor`；push；雙 Agent workflow 下更新 HANDOFF，停在 `READY_FOR_CODEX_REVIEW`。

## English

Enhance the existing Global UI Navigation editor to support a **two-level hierarchy** (Level 1 → Level 2, `MAX_DEPTH = 2`);
do not implement unlimited nesting and do not redesign the whole Global UI. Extend the existing model, admin API, public API,
draft/publish/rollback, desktop navbar, mobile menu, locale system and server baseline.

Use the existing nested `children` model (single source of truth; never keep both parentId and children). Existing flat entries
stay valid as Level 1 automatically; never reset production navigation. Level 1 items: enabled, zh-TW + English labels, optional URL,
internal/external, new-tab, desktop/mobile visibility, order — and may be a clickable parent (URL + children) or a dropdown-only
parent (no URL). Level 2 items: enabled, both labels, required URL, link behavior, visibility, order; no further children.

Admin supports add/edit/delete of parents and children, enable/disable, sorting within a level, and moving a child to another
parent; deleting a parent with children requires confirmation; no orphans. Server-side validation enforces unique ids across the
tree, safe URLs (reject `javascript:`/`data:`), required child URLs, dropdown-only parents allowed, no empty pointless parents,
unique order within a level, max depth 2, and at least one visible desktop item. The nested model makes parent cycles structurally
impossible; grandchildren are flattened at normalization and rejected by validation.

Disabling a parent hides it and its children on the frontend (children keep their own enabled state); disabling a child hides only
that child; a dropdown-only parent with no visible children on a device is hidden. Desktop renders dropdowns (hover/focus + keyboard,
`aria-haspopup`/`aria-expanded`/`aria-controls`, Escape to close; dropdown-only parent is `role="button"`); mobile renders an
accordion (a toggle button per parent + indented children). Child links are always real `<a href>` (crawler-readable), never onclick.

zh-TW/English labels use the existing i18n system (no third translation system); initial server/static locale stays correct.
shell.fans is a static site whose nav is synced at runtime by `js/sf-global-ui.js`; the change is a **no-op for flat data** (the live
navbar is untouched) and only builds dropdown/accordion when a parent has children. Known trade-off: CMS-only children that are not in
the static HTML are a JS progressive-enhancement layer; to enter the no-JS/crawler baseline the static generators must also be updated
(the site's current nav is flat, so there is no immediate impact). robots/sitemap/llms/canonical/hreflang/JSON-LD are unchanged.

The public `/api/site/global-ui` returns the tree with nested `children` (one contract). Hierarchy edits go through
Edit → Save Draft → Preview → Publish; production reads Published only; Rollback restores the whole hierarchy (record snapshots the
full settings). Add automated tests for legacy migration, levels, locales, desktop/mobile, visibility, sorting, parent reassignment,
invalid/empty parents, depth > 2, URL validation, draft/publish/rollback and fallback. Run the repo's lint/typecheck/tests/build,
commit only the relevant changes (`feat(admin): add hierarchical global navigation editor`), push, and stop at `READY_FOR_CODEX_REVIEW`.
