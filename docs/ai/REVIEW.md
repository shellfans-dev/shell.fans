# Codex Review — docs/ai/REVIEW.md

> 由 Claude 以 OpenAI Codex CLI（`codex exec --sandbox read-only`, ChatGPT 認證）驅動的獨立審查記錄。
>    Reviewer = OpenAI Codex；Claude 不得竄改此 verdict。

## Task under review
`fix-initial-locale-render` — commit `f28dcfd`（parent `0d95c6e`）「fix(i18n): render correct locale on initial page load」。
審查時該 commit **已部署到 production**（2026-09-14，隨 nav 兩層一起）。審查的變更集為 `f28dcfd` 相對其 parent 的 diff，
排除 7 個由 `scripts/build-locale-pages.py` 產生的 `*.en.html`（改為審查產生器；Codex 有 in-memory 重新產生並比對，7 頁全部相符）。
審查日期：2026-09-14。Auth: ChatGPT。Model: default。

## Verdict: **FAIL**
（gate 規則：任何 P0/P1/P2 → FAIL。本次 findings：{'P2': 3}）

### Summary
The commit implements genuine pre-rendered English HTML and cookie-first client initialization. In-memory regeneration matched all seven committed English pages and passed the generator's verification. However, nginx leaves duplicate English URLs accessible and still serves Chinese first for supported .html URLs with an English cookie. Production HTTP verification was unavailable because the origin connection failed.

### Residual risk
Browser and nginx integration suites were not executed in the read-only sandbox. Production cache behavior remains unverified.

## Findings（全部經 Claude 在 live origin 實測確認為真）

### 1. [P2] Block extensionless English variant URLs too  （confidence 0.99）
- **位置**：`deploy/nginx/shell.fans.conf:147-149`
- **描述**：The block matches only URLs ending in .en.html. A request to /index.en bypasses it and reaches location /, where the $uri.html candidate at line 372 resolves to /index.en.html. The same bypass exposes all seven variants without a cookie, defeating the explicit requirement to prevent direct duplicate-content URLs. Tests check only the .en.html spelling.
- **建議**：Reject both .en and .en.html public URL forms while retaining internal cookie selection. Add no-cookie and English-cookie tests for extensionless variant URLs.

### 2. [P2] Apply locale selection to existing .html page URLs  （confidence 0.99）
- **位置**：`deploy/nginx/shell.fans.conf:372-372`
- **描述**：For /social-media-backup.html with shellfans_locale=en, $md_suffix is empty and the first candidate $md_base$md_suffix is the existing Chinese /social-media-backup.html file. It wins before locale selection. Other engine .html URLs behave the same way, apart from /index.html which redirects. These requests therefore still display Chinese before the cookie-first client engine switches to English. The tests exercise only extensionless engine URLs.
- **建議**：Redirect supported .html URLs to their extensionless equivalents, or normalize the page stem and select its locale variant before the existing HTML file. Add raw-response tests for all seven .html entry points.

### 3. [P2] Use consistent cookie value matching on server and client  （confidence 0.99）
- **位置**：`deploy/nginx/shell.fans.conf:58-61`
- **描述**：The nginx string map accepts EN case-insensitively, whereas every client cookie regex accepts only lowercase en. With shellfans_locale=EN and localStorage.shellfans_locale=zh-TW, nginx serves English, but the bootstrap rejects the cookie, selects stored Chinese, and switches the page back to Chinese. This also violates the specified invalid-value Chinese fallback. The raw test explicitly accepts EN but does not test its client behavior with stale storage.
- **建議**：Use a case-sensitive nginx match for the exact supported value en, or normalize cookie values consistently across every resolver. Test mixed-case cookies with conflicting localStorage preferences.

## Claude 的實測確認（evidence）
於 live origin（`curl -sk --resolve shell.fans:443:127.0.0.1`）逐項驗證：

- **F1 確認**：`GET /index.en`（無副檔名、無 cookie）→ `200` + `<html lang="en">`；`/social-media-backup.en` → `200`。
  `location ~ \.en\.html$ { return 404; }` 只擋 `.en.html`，`/index.en` 走 `location /` 的 `$uri.html` 命中 `/index.en.html`。
  重複內容 URL 曝光；canonical 標籤可降低 SEO 影響，但「阻擋直接英文變體 URL」的意圖被繞過。
- **F2 確認**：`/social-media-backup.html` + `Cookie: shellfans_locale=en` → `<html lang="zh-Hant">`（首屏中文）；
  但正規（無副檔名）`/social-media-backup` + en cookie → `<html lang="en">`（正確）。`.html` 明確網址非正規入口，
  但若被連結/書籤/爬取，英文使用者會看到中文首屏（正是本任務要修的問題，發生在 `.html` 拼法上）。`/index.html` 有 redirect 不受影響。
- **F3 確認**：`Cookie: shellfans_locale=EN`（大寫）→ `<html lang="en">`。nginx `map` 字串比對預設 case-insensitive，
  但 `js/sf-footer.js`/`sf-global-ui.js`/頁內引擎的 cookie regex 只接受小寫 `en` → 伺服器與客戶端不一致。
  影響有限：本站客戶端寫 cookie 一律小寫 `en`，此不一致只在外部/手動設定大小寫混合值時觸發。

## Status
FAIL（3 × P2，皆已確認）。任務已在 production；上述為部署後的補審查。是否修正（擋 `.en` 無副檔名變體、
`.html` 網址的語系選擇、cookie 值大小寫一致）並重新部署，待 kirin 決定——修正 nginx 需再走一次備份→`nginx -t`→reload。

---

## Remediation（2026-09-14，Claude 依 findings 修正）
三項皆為 nginx 設定層修正（`deploy/nginx/shell.fans.conf`），並補上回歸測試（`scripts/test-initial-locale.py`）：
- **F1**：`location ~ \.en\.html$` → `location ~ \.en(\.html)?$`，一併擋無副檔名的 `/index.en` 等變體。
- **F2**：新增 regex location 把 6 個有英文版的引擎頁 `.html` 明確網址 `301` 到扁平 canonical 網址（相對導向），
  之後由 `location /` 的 `try_files` 依 cookie 選語系；`.en`/`.en.html` 由 F1 block 先擋，不進此規則。
- **F3**：cookie map key `"en"` → case-sensitive regex `"~^en$"`，只認小寫 `en`，與客戶端一致；`EN`/`En` → 中文。

驗證：`scripts/test-initial-locale.py` 118/118（含新增的 F1 無副檔名 404、F2 `.html`→301→英文首屏、F3 大小寫）；
部署後於 live origin 實測三項皆修復、且中文/爬蟲/canonical 行為不變（見 HANDOFF / 部署記錄）。

---

## Re-review of the fix — commit `73c04c3` (2026-09-14): **PASS**
以 OpenAI Codex CLI（read-only，ChatGPT 認證）重新審查修正 commit `73c04c3`（parent `1c1aabb`）。
**Verdict: PASS，0 findings。** 三項（F1/F2/F3）皆確認修復，regex location 順序安全、無 redirect loop、
第 7 頁（index.html）由既有 redirect 涵蓋、測試涵蓋各案例。

> Codex summary: Reviewed 73c04c3 against its parent; all three findings are resolved with no new actionable issue identified. F1: deploy/nginx/shell.fans.conf:150–152 blocks both variant spellings, no tracked legitimate .en file exists, and successful try_files candidates remain in their current location. F2: lines 157–158 match exactly the six intended .html routes, preserve query arguments in the same-host redirect, exclude .en.html and flat URLs, and introduce no loop; the existing index.html redirect at lines 291–293 covers the seventh page. F3: lines 60–63 use case-sensitive ~ matching, accepting lowercase en and sending mixed-case or invalid values to the Chinese fallback; the variant block and redirect precede location / in safe order. Tests cover direct .en.html URLs, representative extensionless variants with both cookie states, all six no-follow 301 responses and canonical locale responses, plus EN/En/eN and lowercase en; independent in-memory route assertions and Python syntax validation passed.

> Codex residual risk: Production verification remains unconfirmed: the origin connection failed. The nginx integration suite was not rerun in the read-only environment; tests do not explicitly assert query preservation, exact redirect authority, or the existing index.html redirect.

備註：Codex 的 residual risk 是「沙箱內無法連線 origin 做 production HTTP 驗證」——該項已由 Claude 於 live origin 實測補足
（F1 /*.en→404、F2 引擎 .html→301→英文、F3 EN→中文、無回歸；見上方 Remediation 與部署記錄）。
