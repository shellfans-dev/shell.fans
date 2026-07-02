/*!
 * shell.fans edge Worker — 產品服務開關 nav 移除（server-side / request-time）。
 *
 * 目的：修正「口碑行銷等 nav 先顯示再消失」的 flicker。改由 Cloudflare 邊緣在
 * HTML 送達瀏覽器「之前」就依 kol.fans 後台的產品服務開關移除對應 nav 連結，
 * 因此首屏 HTML 直接不含已停用產品的 nav item，非 CSS 隱藏、非 client useEffect。
 *
 * 對應標記（由 scripts/mark-product-nav.py 加在各頁 nav/footer 連結）：
 *   kolfans_wom_enabled            → a[data-sf-product="kolfans"]         (口碑行銷)
 *   shellfans_endurance_engine_... → a[data-sf-product="shellfans-engine"] (續航引擎)
 *   aeo_geo_managed_hosting_...    → a[data-sf-product="aeogeo"]           (AEO/GEO 代管)
 *
 * 安全性：passThroughOnException + 只處理 text/html + 讀取失敗/皆啟用時完全不改寫
 * （fallback = 顯示）。部署：route `shell.fans/*`、`www.shell.fans/*`。
 */
addEventListener('fetch', (event) => {
  event.passThroughOnException(); // 任何未捕捉例外 → 直接回源，不影響網站
  event.respondWith(handle(event.request));
});

const FLAGS_API = 'https://kol.fans/api/site/product-flags';

// 產品服務開關 flag → HTML 標記值
const FLAG_TO_ATTR = {
  kolfans_wom_enabled: 'kolfans',
  shellfans_endurance_engine_enabled: 'shellfans-engine',
  aeo_geo_managed_hosting_enabled: 'aeogeo',
};

// 讀取被停用的產品清單。邊緣快取 30s；讀取失敗或皆啟用 → 回空陣列（不移除任何項）。
async function getDisabledProducts() {
  try {
    const res = await fetch(FLAGS_API, { cf: { cacheTtl: 30, cacheEverything: true } });
    if (!res.ok) return [];
    const j = await res.json();
    const data = (j && j.data) || {};
    const disabled = [];
    for (const flag in FLAG_TO_ATTR) {
      if (data[flag] === false) disabled.push(FLAG_TO_ATTR[flag]); // 只有明確 false 才移除
    }
    return disabled;
  } catch (e) {
    return []; // fallback：讀不到 → 一律顯示
  }
}

async function handle(request) {
  const response = await fetch(request);

  // 只改寫 HTML；其他資源（JS/CSS/圖片/字型/JSON…）原樣直接回，開銷最小。
  const ct = response.headers.get('content-type') || '';
  if (!ct.includes('text/html')) return response;

  const disabled = await getDisabledProducts();
  if (disabled.length === 0) return response; // 常態（全啟用）：不改寫

  let rewriter = new HTMLRewriter();
  for (const attr of disabled) {
    rewriter = rewriter.on('a[data-sf-product="' + attr + '"]', {
      element(el) {
        el.remove(); // 從 HTML 串流整段移除該連結（含內容）→ 首屏就不存在
      },
    });
  }
  return rewriter.transform(response);
}
