# ShellFans Navigation First-Render / Old Navigation Flash Fix
# 修正 shell.fans 首屏先顯示舊 Navigation 再跳成新版 Navigation

目標網站：

https://shell.fans/

相關後台：

https://console.shell.fans/_shellfans-admin712/uiux-design?tab=global-ui&site=shell

==================================================
【問題說明】
==================================================

目前 shell.fans 有嚴重的 Navigation Initial Render 問題。

實際瀏覽器畫面：

頁面第一次顯示時，會先看到「舊 Navigation」：

- AEO/GEO 代管
- 續航引擎
- 粉絲分析
- 查看方案
- Klog

然後頁面載入一段時間後，
Navigation 才變成目前 Global UI 已設定的新版本：

- AI 社群方案
- AEO/GEO
- 查看方案
- Klog

這是不正確的。

使用者不應該看到任何一幀舊 Navigation。

正確行為：

Browser 第一次 Paint
↓
直接顯示目前 Published Global UI Navigation

不得：

Old Navigation
↓
JavaScript / API
↓
New Navigation

==================================================
0. 遵守雙 Agent Workflow
==================================================

如果 repository 存在：

CLAUDE.md
AGENTS.md
docs/ai/SHARED-RULES.md
docs/ai/CURRENT-TASK.md
docs/ai/HANDOFF.md
docs/ai/REVIEW.md
docs/ai/DECISIONS.md

先完整閱讀。

Claude Code 角色：

PRIMARY IMPLEMENTER

Codex：

INDEPENDENT REVIEWER

本次完成：

Inspect
→ Fix
→ Tests
→ Build
→ Commit
→ Push
→ HANDOFF

後停在：

READY_FOR_CODEX_REVIEW

除非既有流程另有明確規定，
不要自行略過 Codex Review Gate。

==================================================
1. Git / Host Safety
==================================================

先執行：

date
hostname
pwd
uptime
nproc
free -h
df -h

再：

git status
git status --short
git branch --show-current
git rev-parse HEAD
git remote -v
git fetch --all --prune
git log --oneline -10

禁止為了方便執行：

git reset --hard
git clean
git checkout .
git restore .
git stash
git pull
git rebase

保留所有 unrelated dirty changes。

==================================================
2. 建立 CURRENT TASK
==================================================

更新：

docs/ai/CURRENT-TASK.md

Task ID：

fix-navigation-first-render-flash

Goal：

讓 shell.fans 第一次 render 就直接顯示目前 Published Global UI Navigation，
完全不再顯示 legacy / old Navigation。

Acceptance Criteria：

1. 第一個可見 frame 就是目前新版 Navigation。
2. 舊 Navigation 不得出現在 first paint。
3. Hard Reload 不得閃舊 Navigation。
4. Slow Network 不得閃舊 Navigation。
5. JavaScript Disabled 時仍必須顯示正確 Navigation。
6. zh-TW 正確。
7. English 正確。
8. Desktop 正確。
9. Mobile Menu 正確。
10. Navigation hierarchy 正確。
11. Dropdown 正確。
12. SSR/static HTML 是目前 Published Navigation。
13. 不靠 CSS 隱藏舊 Navigation。
14. 不造成 CLS。
15. 不破壞 SEO/AEO/no-JS。
16. 不破壞 Global UI Draft / Publish / Rollback。

==================================================
3. 先找出真正 Root Cause
==================================================

不要先改 CSS。

搜尋：

sf-global-ui.js
global-ui
global-ui-settings
navigation
navbar
nav
header
published
baseline
fallback
default navigation
static navigation
legacy navigation

以及舊文案：

"AEO/GEO 代管"
"續航引擎"
"粉絲分析"

和新版：

"AI 社群方案"

使用 rg 搜尋，
排除：

node_modules
.next
dist
build
.git

必須找出：

1. 舊 Navigation 是在哪個 source/template 裡產生？
2. First HTML 為什麼仍是舊 Navigation？
3. 新 Navigation 是什麼時候載入？
4. 是否由 `/api/site/global-ui` 載入？
5. 是否由 `sf-global-ui.js` 在 DOM load 後替換？
6. 是否存在 hardcoded legacy Navigation？
7. 是否存在 static baseline Navigation？
8. Publish Global UI 時是否沒有同步更新 static baseline？
9. Header/Navbar 是否同時存在兩套 source of truth？

最後一定要指出實際 Root Cause，
不得只說「可能是」。

==================================================
4. 特別檢查目前 Global UI Runtime Architecture
==================================================

目前專案可能存在：

js/sf-global-ui.js

以及：

/api/site/global-ui

但必須自行確認。

如果目前架構類似：

Static HTML
= hardcoded legacy Navigation

然後：

sf-global-ui.js
→ fetch Published Global UI
→ 套用差異
→ replace Navigation

這就是本次必須修掉的架構問題。

不能只加快 JS。

不能只減少 API latency。

不能只 preload API。

根因是：

First HTML 本身使用錯誤 Navigation。

==================================================
5. Navigation 必須只有一個 Published Source of Truth
==================================================

目前 Global UI Published Navigation
必須成為 Navigation 的正式 Source of Truth。

不得同時存在：

Source A：
hardcoded old Navigation

Source B：
Global UI Published Navigation

然後靠 JavaScript 讓 B 覆蓋 A。

這會永遠存在 flash / mismatch / crawler inconsistency。

正確：

Global UI Published Navigation
↓
Server / build / static generator
↓
Initial HTML
↓
Browser first paint

Client JavaScript 只能：

hydration
interaction
dropdown
mobile behavior

不能負責把舊 Nav 換成新 Nav。

==================================================
6. 根據實際架構選擇正確方案
==================================================

先確認 shell.fans 真正架構。

如果是 SSR / Server Render：

Request
↓
Server 取得目前 Published Global UI
↓
Render Navbar
↓
回傳正確 HTML

如果是 Static Site：

Global UI Publish
↓
產生 / 更新 Published snapshot
↓
重新生成正確 Navigation static HTML
↓
deploy / revalidate
↓
Browser 直接取得新 Navigation

如果是 hybrid：

使用合理：

SSR
SSG
ISR
server cache
published snapshot

但核心原則不變：

First HTML 必須已經是 Current Published Navigation。

==================================================
7. 建議架構：Published Snapshot
==================================================

如果 shell.fans 不適合每個 request 都 query DB/API，

優先考慮：

Global UI Publish
↓
生成 Published Global UI Snapshot
↓
Server/static template 使用該 snapshot
↓
Navigation HTML 直接輸出最新 Published Navigation

例如概念：

published-global-ui.json
或現有 config/cache mechanism

但請依 repository 現有 architecture 實作。

不要為此建立不必要的新系統。

Published Snapshot 必須：

- atomic
- validated
- versioned 或至少可 rollback
- 只有 Publish 時更新
- Draft 不得影響 production

==================================================
8. Fail-safe 也不能顯示「舊 Navigation」
==================================================

目前可能把 hardcoded old Navigation
當成 fail-safe。

這就是現在 UX 問題來源之一。

Fail-safe 應改成：

Last Known Good Published Navigation

而不是：

Legacy Navigation from source code。

正確：

Current Published
↓ fail
Last Known Good Published Snapshot

不是：

Current Published
↓ fail
2016/舊版 hardcoded Navigation

除非從來沒有任何 Published config，
才可使用 repository default。

而 repository default 也必須與目前正式 Navigation architecture 一致。

==================================================
9. 禁止 Fake Fix
==================================================

嚴格禁止以下方式：

nav {
  visibility: hidden;
}

nav {
  opacity: 0;
}

display: none;

等待 JS 後再顯示。

禁止：

loading Navbar
Skeleton Navbar
blank Header
setTimeout
fade-in workaround

這些只會把：

舊 Nav → 新 Nav

變成：

空白 → 新 Nav

不是修正。

==================================================
10. 不得改成 Client-Only Navigation
==================================================

也禁止：

Initial HTML 沒有 Navbar
↓
JavaScript fetch API
↓
才建立 Navbar

因為 ShellFans 需要：

SEO
AEO
AI crawler
No-JS baseline

Navigation 必須存在於 raw HTML。

==================================================
11. Raw HTML 必須直接是新版 Navigation
==================================================

修正後：

curl https://shell.fans/

或實際 locale route/cookie request

raw HTML 必須直接包含目前 Published Navigation。

繁中目前預期看到的正式新版架構，
必須以 Global UI Published data 為準。

例如如果目前 Published 設定為：

AI 社群方案
AEO/GEO
查看方案
Klog

Raw HTML 就應直接包含這些內容。

不得再包含舊：

AEO/GEO 代管
續航引擎
粉絲分析

作為 first-render navigation。

注意：

以上名稱只是目前實際畫面證據。

真正測試必須讀 Current Published Global UI，
不要 hardcode prompt 內容當資料來源。

==================================================
12. Navigation Hierarchy
==================================================

目前 Global UI Navigation 正在支援：

Level 1
→ Level 2

修正 First Render 時必須完整保留 hierarchy。

如果 Published Navigation：

AI 社群方案
├── 社群續航
├── 粉絲洞察
└── ...

AEO/GEO
├── AEO/GEO 服務
├── 案例
└── ...

First HTML 必須直接輸出：

Parent
Children
URLs
Visibility
Order

不能只 SSR Level 1，
children 等 JavaScript 才建立。

==================================================
13. Desktop Navbar
==================================================

Desktop：

第一次 render：

- 正確 parent
- 正確順序
- 正確 labels
- 正確 dropdown children
- 正確 CTA
- 正確 locale
- 正確 Logo

JavaScript 只負責：

dropdown interaction

而不是：

建立/替換 Navigation structure。

==================================================
14. Mobile Menu
==================================================

Mobile Menu 使用同一份 Published Navigation。

不能：

Desktop = new Global UI
Mobile = old hardcoded nav

也不能：

Desktop first render 舊、新切換
Mobile 又另一套。

必須：

same source of truth
different presentation

==================================================
15. Locale
==================================================

這個問題與先前：

中文 → English initial flash

屬於同類型問題。

請確認新的 Navigation first render
與目前 locale bootstrap 修正相容。

English：

第一份 HTML
=
English Navigation
+
English Logo

zh-TW：

第一份 HTML
=
zh-TW Navigation
+
Chinese Logo

禁止：

Chinese old Nav
→ English new Nav

或：

Chinese new Nav
→ English new Nav

==================================================
16. Header / Logo
==================================================

確認 Header 整體不要有：

舊 Logo
→ 新 Logo

舊 Nav
→ 新 Nav

如果 Global UI Header 與 Navigation
現在由兩套不同 runtime 處理，

必須確認 initial render 使用一致 Published config。

==================================================
17. CTA
==================================================

例如：

登入
開始使用
Language selector

也必須在 initial HTML 使用目前 Published/現有正式設定。

不要造成：

old CTA
→ new CTA

==================================================
18. Global UI Draft / Published
==================================================

嚴格區分：

Draft
與
Published。

Admin：

Save Draft
不能直接影響 production Navbar。

只有：

Publish

才更新 Production Navigation / Published snapshot。

Preview：

讀 Draft。

Production：

只讀 Published。

==================================================
19. Publish 流程
==================================================

請特別檢查目前 Publish API。

當管理者：

Global UI
→ Navigation
→ Publish

是否有：

cache invalidation
snapshot regeneration
static revalidation
SSR cache clear

如果沒有，
補上必要流程。

目標：

Publish 完成後，
下一個 production page request
直接取得新版 Navigation HTML。

不是等待 client JS 覆蓋。

==================================================
20. Atomic Publish
==================================================

避免 Publish 過程：

一半 old
一半 new。

如果需要產生 snapshot：

先：

validate
→ build complete snapshot
→ atomic switch

不得：

逐項修改 production file
造成 transient inconsistent state。

==================================================
21. Cache
==================================================

檢查：

Cloudflare
Nginx
SSR cache
ISR
application cache
browser cache

Publication 後必須確保：

舊 Navigation HTML 不會因 cache
繼續存在。

但不要粗暴：

disable all cache

或：

cache-control: no-store 全站。

應精準處理：

Global UI Publish
→ revalidation/invalidation

==================================================
22. API
==================================================

如果：

/api/site/global-ui

仍保留，

可以用於：

client enhancement
future live config
diagnostic

但第一個 Navigation Render
不能依賴 API request 完成。

如果 API 慢：

頁面仍應直接顯示 Current Published Nav。

==================================================
23. No-JS
==================================================

停用 JavaScript後：

https://shell.fans/

仍應看到：

目前 Published Navigation。

不是 old Navigation。

不是空 Navigation。

這是本次的重要 PASS 條件。

==================================================
24. Slow Network
==================================================

使用現有 Browser tooling
進行：

Slow 3G / throttle

或者合理模擬 client JS 延遲。

觀察第一個 frame。

整段載入期間：

任何時間都不得出現舊 Navigation。

如果 JS 永遠不執行：

仍然是正確新版 Navigation。

==================================================
25. Hard Reload
==================================================

測試：

Ctrl+Shift+R / no cache equivalent

至少多次驗證：

不能偶發出現：

old → new

尤其第一次沒有 browser cache 時。

==================================================
26. View Source / Raw Response
==================================================

不要只用 browser DOM after JS。

必須比對：

View Source / curl raw response

vs

Final DOM。

Navigation 的：

items
order
labels
links

應一致。

如果 Raw HTML 和 Final DOM 不一致：

本任務仍然 FAIL。

==================================================
27. JavaScript 不應重建同一 Navigation
==================================================

如果目前 sf-global-ui.js：

每次 mount 都：

remove old nav
createElement
replaceChildren
innerHTML

請重新評估。

已經由 Server / Static HTML
輸出正確 Navigation 後，

client runtime 應：

hydrate
attach interaction
必要時 reconcile

而不是：

無條件重建一次完全相同的 Nav。

避免：

layout shift
event duplication
visual flash。

==================================================
28. 不要使用 DOM Text Replacement
==================================================

禁止以大量：

querySelector
innerText
replaceWith

來修 first render。

這類做法只能作為 legacy migration 暫時相容，
不可成為正式 initial-render architecture。

==================================================
29. Accessibility
==================================================

SSR / Static Navigation
仍應有：

<nav>
<a href>
button for dropdown trigger where appropriate
aria-expanded
aria-haspopup

JavaScript 只提升 interaction。

無 JavaScript：

主要 navigation links
仍可存取。

==================================================
30. SEO / AEO
==================================================

這個修正非常重要。

AI crawler / Search crawler
不應看到：

Legacy Navigation

而使用者看到：

New Navigation。

Raw HTML 與實際網站資訊架構
必須一致。

確認不破壞：

canonical
hreflang
structured data
internal links
robots.txt
sitemap.xml
llms.txt

本任務不需要任意修改上述檔案。

==================================================
31. 測試舊文字不存在
==================================================

針對 production current Published config：

建立 regression test。

例如：

raw HTML Navigation
不得包含已被 Published Navigation 移除的 legacy item。

不要硬編碼所有歷史 label，
但至少本次 known regression 可加入適當 assertion。

更好的方式：

assert:

initial nav == normalized published nav

而不是：

initial nav != "續航引擎"

讓未來改 Nav 不需要一直改測試。

==================================================
32. Automated Tests
==================================================

至少涵蓋：

A.
Published navigation
→ initial HTML navigation 相同

B.
Draft navigation
→ production initial HTML 不受影響

C.
Publish
→ 下一版 initial HTML 更新

D.
Rollback
→ initial HTML 回上一版

E.
No-JS
→ current Published Nav

F.
Desktop
→ current Published hierarchy

G.
Mobile
→ current Published hierarchy

H.
zh-TW

I.
English

J.
No hydration mismatch

K.
No duplicate nav items

L.
Fallback
→ last known good Published

M.
API failure
→ initial nav 不消失

==================================================
33. 其他頁面
==================================================

不要只修：

Homepage。

如果 Header/Nav 是 Global Component，

檢查至少：

/
AEO/GEO pages
Case Studies
Pricing /方案
登入前 public pages

只要共用同一 Header：

第一 Render 都不能舊 → 新。

應修 shared architecture，
不是逐頁 patch。

==================================================
34. 視覺不能被重新設計
==================================================

本次：

Fix first-render source。

不是：

Redesign Navbar。

不要改：

字體
顏色
高度
spacing
button style
logo size
dropdown visual

除非解決 regression 必須。

==================================================
35. Performance
==================================================

改善後不應變成：

每次 request
→ slow DB query
→ slow API
→ Navbar render

如果 Published config 適合 cache：

使用：

server cache
static snapshot
ISR/revalidation
memory cache

依現有 architecture。

目標：

Correct first render
+
Fast TTFB。

==================================================
36. Debug Old Navigation Source
==================================================

修完後不要只是把 old Nav source 留著但永遠不用。

如果確認某一份：

hardcoded legacy Navigation

已經完全被 Global UI Published Source 取代，

可以安全移除或降級為：

repository default fallback

但該 fallback 必須更新成目前 schema，
不能保留一套過時 Navigation。

不要刪除仍被其他頁面使用的 template。

先做 reference search。

==================================================
37. Browser Verification
==================================================

如果 repo 已有：

Playwright
Puppeteer
E2E

使用現有工具。

不要因本任務新增大型 browser framework。

測：

1440px
768px
390px

確認：

Desktop Navbar
Tablet
Mobile Menu

都沒有舊 Nav flash。

==================================================
38. Browser Screenshot / Video
==================================================

如果現有工具支援：

可以用：

filmstrip
video
screenshots

在：

initial
100ms
500ms
loaded

比較。

任何 frame 都不能顯示 legacy Navbar。

如果無既有工具，
不必新增新 dependency。

==================================================
39. Console
==================================================

確認沒有：

Hydration failed
Text content mismatch
duplicate key
undefined navigation
failed global-ui fetch
runtime error

==================================================
40. Prompt 保存
==================================================

保存完整中英文任務：

prompts/fix-navigation-first-render-flash.md

不得包含 secrets。

==================================================
41. Lint / Tests / Build
==================================================

先讀 repository scripts。

依序執行：

lint
typecheck
targeted tests
full tests
build

不要平行開大量 heavy jobs。

==================================================
42. Git
==================================================

完成後：

git status
git diff
git diff --stat

只 commit 本任務。

如果檔案混有 unrelated changes：

git add -p

禁止未確認就：

git add .

Commit 建議：

fix(navigation): render published nav on first paint

然後：

git push

必須 Push GitHub。

禁止 force push。

==================================================
43. Codex Handoff
==================================================

更新：

docs/ai/HANDOFF.md

至少：

# Claude → Codex Handoff

## Task
Navigation First Render Flash Fix

## Root Cause

## Old Architecture

明確說明：

Initial HTML source
Client runtime
Global UI API
為什麼造成 old → new。

## New Architecture

## Published Source of Truth

## Fallback Strategy

## Publish/Revalidation Flow

## Cache Strategy

## Navigation Hierarchy

## Desktop

## Mobile

## zh-TW

## English

## Raw HTML Verification

## No-JS Verification

## Slow Network Verification

## Hydration Verification

## SEO/AEO Verification

## Modified Files

## Tests

## Review Commit

## Branch

Status:

READY_FOR_CODEX_REVIEW

要求 Codex 特別檢查：

1. 是否真的修 First HTML
2. 是否只是 CSS hiding
3. 是否還存在 legacy → new replacement
4. Published source 是否 single source of truth
5. Draft 是否不會外洩到 production
6. rollback
7. cache invalidation
8. no-JS
9. SEO/AEO
10. locale
11. hierarchy
12. mobile
13. hydration
14. performance
15. unrelated regression

==================================================
44. 最終回報
==================================================

完成後回報：

1. Root Cause
2. 舊 Navigation 真正來源
3. 新 Navigation 真正來源
4. sf-global-ui.js 原本扮演什麼角色
5. sf-global-ui.js 修正後角色
6. Published source of truth
7. Initial HTML 是否直接為 Published Navigation
8. Legacy Navigation 是否仍存在以及用途
9. Fallback strategy
10. Publish flow
11. Cache invalidation
12. Desktop result
13. Mobile result
14. zh-TW result
15. English result
16. hierarchy result
17. raw HTML result
18. No-JS result
19. Slow Network result
20. hydration result
21. console result
22. SEO/AEO regression
23. lint
24. typecheck
25. tests
26. build
27. modified files
28. prompt file
29. commit SHA
30. branch
31. push result
32. HANDOFF status

不要要求使用者自行驗證。

==================================================
【ENGLISH SPECIFICATION】
==================================================

Fix the ShellFans navigation first-render flash.

Current production behavior:

The browser initially renders an old legacy navigation such as:

AEO/GEO managed service
Endurance Engine
Fan Analytics
Plans
Klog

and then, after client-side JavaScript/global UI processing,
replaces it with the currently published navigation such as:

AI Social Solutions
AEO/GEO
Plans
Klog

The exact current labels must be read from the real Published Global UI
configuration rather than hardcoded from this prompt.

This behavior is incorrect.

At no point should the user see the previous/legacy navigation.

The first HTML response and the first visible browser frame must already
contain the current Published Global UI Navigation.

Do not solve this by hiding the navbar until JavaScript loads.

Do not use:

visibility:hidden,
opacity:0,
display:none,
skeleton navbar,
blank header,
loading overlay,
setTimeout,
or similar visual masking.

Do not solve it by making the navigation client-only.

The navigation must remain server-rendered or statically rendered for:

SEO,
AEO/GEO,
AI crawlers,
and no-JavaScript accessibility.

Determine the real root cause first.

Inspect:

legacy/static navigation,
Global UI Published configuration,
the public Global UI API,
sf-global-ui.js,
server/static templates,
SSR/SSG/ISR,
cache,
publish behavior,
and revalidation.

If the current architecture is:

legacy static HTML
→ browser paint
→ fetch Global UI
→ replace navigation

replace this architecture.

Published Global UI Navigation must become the single source of truth
for the initial navigation HTML.

Depending on the real application architecture:

SSR:
resolve the current Published Navigation before rendering the response.

Static/SSG:
generate the static navigation from the Published Global UI snapshot
and regenerate/revalidate it when Global UI is published.

Hybrid:
use an appropriate server-side/static published snapshot and cache.

Client JavaScript may provide interaction and enhancement,
but it must not be responsible for replacing an obsolete navigation
after first paint.

The fail-safe must not be an obsolete legacy navigation.

Prefer:

Current Published
→ Last Known Good Published Snapshot

rather than:

Current Published
→ old hardcoded legacy menu.

Preserve the existing:

Draft
→ Preview
→ Publish
→ Rollback

workflow.

Draft navigation must never appear in production.

Publishing navigation should trigger any necessary:

snapshot regeneration,
cache invalidation,
revalidation,
or release update

so that the next production page request directly contains the newly
published navigation.

Preserve navigation hierarchy.

Both Level 1 and Level 2 items must be present in the initial semantic HTML
where appropriate.

Desktop and Mobile must use the same Published Navigation source.

Traditional Chinese and English must render the correct localized
navigation from the first HTML response.

The fix must be compatible with the separate initial-locale rendering fix.

Verify raw source HTML, not only the post-JavaScript DOM.

Raw HTML navigation and final rendered navigation must represent the
same Published configuration.

With JavaScript disabled,
the current Published Navigation must still be usable.

With a slow network/client JavaScript delay,
no frame may show the old navigation.

Test hard reload/no-cache behavior repeatedly.

Do not redesign the navbar visually.

Preserve:

logo,
spacing,
height,
CTA,
dropdown style,
responsive behavior,
SEO,
AEO,
canonical,
hreflang,
structured data,
robots,
sitemap,
llms,
and internal-link crawlability.

Use the repository's existing tests and browser tooling where available.

Save this bilingual specification to:

prompts/fix-navigation-first-render-flash.md

Run:

lint,
typecheck,
targeted tests,
full tests,
build

using the actual repository scripts.

Commit only relevant changes.

Suggested commit:

fix(navigation): render published nav on first paint

Push GitHub.

If the dual-agent workflow is active,
update HANDOFF and stop at:

READY_FOR_CODEX_REVIEW.