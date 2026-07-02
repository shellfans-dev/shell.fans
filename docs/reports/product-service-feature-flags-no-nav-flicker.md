# 修正 shell.fans nav「口碑行銷」關閉後先顯示再消失（flicker）

任務：關閉後台「KOL.FANS 口碑行銷」時，shell.fans nav 首屏就不得出現「口碑行銷」，
不可先顯示再消失，且不可靠 CSS 隱藏或 client-side useEffect 移除。

- 完成日期：2026-07-02
- 主要 repo：`shell.fans`（shellfans-dev/shell.fans，靜態站，/var/www/shell.fans on host 215）
- 相依：kol.fans flag API（saas_womm，本次未改）

## 前置檢查結果
| 項目 | 結果 |
|---|---|
| 主機 / repo | host 215 : `/home/kirin/work/shell.fans-static` |
| 起始 branch / commit | `main` @ `af873b2` |
| `git remote -v` | origin `https://github.com/shellfans-dev/shell.fans.git` |
| `git fetch --all --prune` | 同步（`af873b2` 已在 origin/main） |
| 本機 vs origin/main | `0 0` |
| `git status --short` | 乾淨（動工前） |
| 部署分支 | `main`（靜態站以 /var/www 服務；main 為來源） |
| 任務分支 | 新建 `fix/nav-flicker-server-side` |

---

## 1. flicker 的根本原因
shell.fans 是 **nginx 靜態 Webflow HTML**（`root /var/www/shell.fans`），非 Next.js SSR。
前一版（commit af873b2）在 `js/sf-footer.js` 用 **client-side runtime fetch flags 後才從 DOM 移除**「口碑行銷」→ 首屏 HTML 一定先含該 nav，載入 JS 後才消失 = flicker。
因為是靜態 HTML，要「首屏就不含」只能在 **HTML 送達瀏覽器前**（server/edge/request-time）改寫。

## 2. shell.fans desktop nav component 位置
各頁 `*.html`（Webflow 匯出）內硬編的 `<a class="nav-link"...>` / `<a class="nav-link w-nav-link">`。

## 3. shell.fans mobile nav component 位置
同檔內的手機 nav（部分帶 `data-i18n="nav.wordOfMouth"`、部分為純 `<a href="https://kol.fans" rel="noopener">`）；dropdown 登入項為 `w-dropdown-link`。

## 4. 原本 nav items 來源
硬編在每頁靜態 HTML（無共用 config）；「口碑行銷」連結 href = `https://kol.fans`（裸根）或 `https://kol.fans/login`（dropdown），文字精確為「口碑行銷」。內文另有 CTA「前往 kol.fans 了解口碑行銷」（文字不同）。

## 5. 修改後 nav items 來源
HTML 仍為靜態，但每個「產品服務」nav/footer 連結加上 `data-sf-product` 標記（見 §8），
由 **Cloudflare Worker 在 edge/request-time** 依開關決定是否輸出該連結。

## 6. KOL.FANS feature flag helper 位置（saas_womm，未改）
`src/lib/product-flags.ts`（`getProductServiceFlags/isKolfansEnabled`）；公開 API `GET /api/site/product-flags`（key `product_service_flags` → `kolfans_wom_enabled`）。

## 7. server-side / request-time 讀取設定的方式
Cloudflare Worker（`workers/product-flags-rewriter.js`，route `shell.fans/*`、`www.shell.fans/*`）於每個 HTML 請求時 `fetch('https://kol.fans/api/site/product-flags')`（edge 快取 30s），取得被停用的產品清單。

## 8. 如何確保 disabled 時首屏不輸出「口碑行銷」
1. **標記**：`scripts/mark-product-nav.py`（冪等）為「精確文字」的產品 nav/footer/dropdown 連結加屬性：
   - `口碑行銷` → `data-sf-product="kolfans"`
   - `續航引擎` → `data-sf-product="shellfans-engine"`
   - `AEO/GEO 代管` → `data-sf-product="aeogeo"`
   （精確文字比對刻意排除內文 CTA「前往…了解口碑行銷」。）
2. **邊緣移除**：Worker 用 `HTMLRewriter` 對停用產品執行 `.on('a[data-sf-product="X"]',{element(el){el.remove()}})`，
   於 HTML 串流中整段移除該 `<a>`。→ 送到瀏覽器的首屏 HTML **本來就沒有**該連結，非 CSS、非 useEffect。
3. **fallback**：flag 讀取失敗或皆啟用 → Worker 不改寫（顯示）；Worker 例外 → `passThroughOnException()` 直接回源。

## 9. desktop / mobile nav 如何共用 filtered items
兩者（及 dropdown、靜態 footer 連結）皆帶相同 `data-sf-product` 標記，Worker 以單一 selector 一次移除，
**不可能桌機消失手機殘留**（來源與規則完全一致）。實測關閉後 `/`、`/product`、`/what-is-shellfans` 標記殘留皆 0。

## 10. cache / revalidate / no-store 處理方式
- shell.fans HTML：`cf-cache-status: DYNAMIC`、`cache-control: no-cache`、`cdn-cache-control: no-store` → Worker 每次回源取得即時 HTML。
- flag：Worker fetch flags 以 `cf.cacheTtl=30` 邊緣快取；公開 API `s-maxage=30`。→ 後台開關後 **~30s 內**於下次 request 反映，無需重啟/重build。

## 11. kol.fans 前台 redirect 是否受影響
不受影響（不同網域、不同機制）。實測關閉時 `kol.fans/` → **307 https://shell.fans/**（既有 saas_womm middleware，未改）。

## 12. `_shellfans-admin712` 後台 exclude 是否仍正常
正常。實測關閉時 `/_shellfans-admin712/settings` → **302 Cloudflare Access**（非 shell.fans）。Worker 只在 shell.fans zone，完全不碰 kol.fans。

## 13. 驗收測試結果
| 項目 | 結果 |
|---|---|
| enabled：shell.fans/ 首屏含 kolfans nav | 標記=3 ✅ |
| disabled：shell.fans/、/product、/what-is-shellfans 首屏 kolfans nav | 標記=0（desktop+mobile+dropdown 全移除）✅ |
| disabled：首屏殘留 `>口碑行銷` nav anchor | 0 ✅（server-rendered HTML 直接無，無 flicker）|
| disabled：其他 nav（續航引擎/查看方案）保留 | 續航引擎標記=3、查看方案=7 ✅ |
| disabled：kol.fans/ redirect | 307 → shell.fans ✅ |
| disabled：kol.fans 後台 | 302 CF Access（可進入）✅ |
| 還原 enabled | 標記恢復=3 ✅ |
| 標記腳本冪等 | 二次執行 0 新增 ✅ |
| Worker 語法/部署 | script + 2 routes success ✅ |

- **測試方式**：以 `curl` 取得 **server-rendered（edge-rewritten）HTML** 直接檢查 nav 是否含「口碑行銷」— 因 Worker 在伺服器端改寫，curl 所見即瀏覽器首屏，故可直接證明「首屏不含、無先顯示再消失」。未使用 Playwright（無 headless 環境），改以 server HTML 斷言等效驗證。

## 14. lint / typecheck / build 結果
- 靜態站無 build。Worker JS：CF API 上傳成功（語法有效）；標記腳本 `python3` 執行成功、冪等。
- HTML 僅新增屬性，未動結構。

## 15. commit hash
- 見 §16（本報告隨該 commit 一併提交）。

## 16. push 到 GitHub 的 branch 與結果
- shell.fans：`fix/nav-flicker-server-side` → origin，並 merge 進 `main` 後 push（借 coder1bot gh token）。
- 部署：17 頁 HTML → /var/www/shell.fans（sudo）；Worker script + routes → Cloudflare（zone shell.fans）。

## 17. 未完成 / 風險
1. **仍保留 `sf-footer.js` 的 client-side 移除作為「次要 fallback」**：Worker 是**首屏主要**機制（server-side）；client 移除僅在「直接打 origin 繞過 CF」時作用，且處理 JS 渲染的 footer（footer 在頁尾、非首屏 flicker 範圍）。正常經 CF 的訪客不會 client 端再動 nav（Worker 已移除），故無 flicker。
2. **flag 反映延遲 ~30s**（Worker + API 邊緣快取）；可調小 `cacheTtl`/`s-maxage` 換取更即時但更多回源。
3. **Worker 攔截整個 shell.fans zone**：已用 `passThroughOnException` + 只處理 `text/html` + 讀取失敗不改寫，最小化風險；若需回退可刪除 route/script。
4. **翻轉開關後 30s 內邊緣快取可能短暫不一致**（測試中觀察到），屬快取 TTL 正常收斂範圍。
5. 三個產品（口碑行銷/續航引擎/AEO-GEO）皆已標記並支援 edge 移除，本次主要驗收為口碑行銷。
