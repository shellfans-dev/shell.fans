/*!
 * shell.fans edge Worker — 產品服務開關 nav 移除（server-side / request-time）
 *                        + 爬蟲訪問記錄（crawler access logging）。
 *
 * 目的一：修正「口碑行銷等 nav 先顯示再消失」的 flicker。改由 Cloudflare 邊緣在
 * HTML 送達瀏覽器「之前」就依 kol.fans 後台的產品服務開關移除對應 nav 連結，
 * 因此首屏 HTML 直接不含已停用產品的 nav item，非 CSS 隱藏、非 client useEffect。
 *
 * 對應標記（由 scripts/mark-product-nav.py 加在各頁 nav/footer 連結）：
 *   kolfans_wom_enabled            → a[data-sf-product="kolfans"]         (口碑行銷)
 *   shellfans_endurance_engine_... → a[data-sf-product="shellfans-engine"] (續航引擎)
 *   aeo_geo_managed_hosting_...    → a[data-sf-product="aeogeo"]           (AEO/GEO 代管)
 *
 * 目的二：bot / crawler 流量以 event.waitUntil() fire-and-forget 上報到 kol.fans
 * ingest API（token 保護），供後台 system-monitor「爬蟲監控」使用。上報完全在
 * response 送出之後執行，不增加訪客延遲；上報失敗不影響網站。
 * 需要 secret binding：CRAWLER_INGEST_TOKEN（無 binding 時自動停用上報）。
 *
 * 安全性：passThroughOnException + 只處理 text/html + 讀取失敗/皆啟用時完全不改寫
 * （fallback = 顯示）。部署：route `shell.fans/*`、`www.shell.fans/*`。
 */
addEventListener('fetch', (event) => {
  event.passThroughOnException(); // 任何未捕捉例外 → 直接回源，不影響網站
  event.respondWith(handle(event));
});

const FLAGS_API = 'https://kol.fans/api/site/product-flags';
const CRAWLER_INGEST_API = 'https://kol.fans/api/site/crawler-ingest';

// 產品服務開關 flag → HTML 標記值
const FLAG_TO_ATTR = {
  kolfans_wom_enabled: 'kolfans',
  shellfans_endurance_engine_enabled: 'shellfans-engine',
  aeo_geo_managed_hosting_enabled: 'aeogeo',
};

// 疑似 bot 的 UA（寬鬆初篩；精確分類由 ingest 端 classifier 做）。
const BOT_UA_RE = /bot|crawl|spider|slurp|fetch|scan|monitor|GPTBot|OAI-SearchBot|ChatGPT-User|Claude|anthropic|Perplexity|Bytespider|meta-external|facebookexternalhit|curl|wget|python|httpx|scrapy|go-http-client|okhttp|libwww|HeadlessChrome|Lighthouse/i;

// 無論 UA 為何都上報的 SEO/AEO 關鍵路徑
const ALWAYS_LOG_PATHS = /^\/(robots\.txt|sitemap\.xml|llms\.txt|llms-full\.txt|ai\.txt)$/;

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

function shouldLog(request, url) {
  const ua = request.headers.get('user-agent') || '';
  if (ALWAYS_LOG_PATHS.test(url.pathname)) return true;
  if (!ua) return true; // 空 UA 本身就可疑
  return BOT_UA_RE.test(ua);
}

// fire-and-forget 上報。任何錯誤靜默吞掉 — logging 絕不影響前台。
async function reportCrawler(request, url, status, responseTimeMs) {
  try {
    if (typeof CRAWLER_INGEST_TOKEN === 'undefined' || !CRAWLER_INGEST_TOKEN) return;
    const cf = request.cf || {};
    const body = JSON.stringify({
      events: [
        {
          ts: new Date().toISOString(),
          source: 'edge_worker',
          host: url.hostname,
          method: request.method,
          path: url.pathname,
          query: url.search ? url.search.slice(1, 512) : null,
          status: status,
          userAgent: (request.headers.get('user-agent') || '').slice(0, 1024),
          // 真實 client IP：僅傳給 ingest 做 hash/驗證，DB 不存明文
          ip: request.headers.get('cf-connecting-ip') || null,
          asn: cf.asn || null,
          country: cf.country || null,
          referer: (request.headers.get('referer') || '').slice(0, 512) || null,
          acceptLanguage: (request.headers.get('accept-language') || '').slice(0, 128) || null,
          responseTimeMs: responseTimeMs,
        },
      ],
    });
    await fetch(CRAWLER_INGEST_API, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-crawler-ingest-token': CRAWLER_INGEST_TOKEN,
      },
      body,
    });
  } catch (e) {
    /* 靜默：上報失敗不得影響任何流程 */
  }
}

async function handle(event) {
  const request = event.request;
  const url = new URL(request.url);
  const t0 = Date.now();
  const response = await fetch(request);
  const responseTimeMs = Date.now() - t0;

  // 爬蟲上報：在 response 回傳前排入 waitUntil，實際執行在回應送出後（不阻塞）。
  if (request.method === 'GET' || request.method === 'HEAD') {
    if (shouldLog(request, url)) {
      event.waitUntil(reportCrawler(request, url, response.status, responseTimeMs));
    }
  }

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
