/**
 * ShellFans 客戶站台爬蟲監控 Worker
 * ---------------------------------------------------------------------------
 * 部署在「客戶自己的 Cloudflare zone」上，把 bot / crawler 流量以
 * event.waitUntil() fire-and-forget 上報到 console.shell.fans。
 *
 * 為什麼用 Worker 而不是在主機上裝 agent 讀 origin log：
 *   1. CF 快取命中的請求根本不會到 origin —— agent 讀 IIS/nginx log 會漏掉，
 *      而 robots.txt / sitemap.xml / llms.txt 這些 AEO 最該監控的路徑最常被快取。
 *   2. origin log 在 CDN 後方只看得到 CF 邊緣 IP，rDNS / IP-range 驗證會把所有
 *      爬蟲誤判成偽裝 —— 等於失去「分辨真假 GPTBot」這個核心能力。
 *   Worker 兩者都沒問題：看得到全部流量，也拿得到 cf-connecting-ip。
 *
 * 已知限制：被 WAF 擋掉的流量不會進到 Worker，因此不會出現在監控中。
 *
 * 必要 secret binding：
 *   SHELLFANS_INGEST_TOKEN  — 由 ShellFans 後台「站台管理」發放的 edge token
 *
 * 選用 var binding：
 *   SHELLFANS_INGEST_API    — 預設 https://console.shell.fans/api/site/crawler-ingest
 *
 * 部署（在客戶 zone 上）：
 *   wrangler deploy --name shellfans-crawler-monitor
 *   wrangler secret put SHELLFANS_INGEST_TOKEN
 *   路由設定為 example.com/* 與 www.example.com/*
 *
 * 這支 Worker 只做「觀察」：不改寫任何回應內容、不設 cookie、不影響快取行為。
 * 上報失敗一律靜默吞掉，絕不影響客戶站台的正常服務。
 */

const DEFAULT_INGEST_API = 'https://console.shell.fans/api/site/crawler-ingest';

// 寬鬆初篩：寧可多送一點讓後端分類器判斷，也不要在邊緣就漏掉新出現的 AI 爬蟲。
const BOT_UA_RE =
  /bot|crawl|spider|slurp|fetch|scan|monitor|GPTBot|OAI-SearchBot|ChatGPT-User|Claude|anthropic|Perplexity|Bytespider|meta-external|facebookexternalhit|Applebot|Amazonbot|Google-Extended|CCBot|Diffbot|cohere|YouBot|curl|wget|python|httpx|scrapy|go-http-client|okhttp|libwww|HeadlessChrome|Lighthouse/i;

// 這些路徑即使 UA 看起來像一般瀏覽器也一併上報 —— AEO 觀測的重點檔案。
const ALWAYS_REPORT_PATHS = new Set([
  '/robots.txt',
  '/sitemap.xml',
  '/sitemap_index.xml',
  '/llms.txt',
  '/llms-full.txt',
  '/.well-known/ai-plugin.json',
]);

function shouldReport(request, url) {
  const ua = request.headers.get('user-agent') || '';
  if (!ua) return true; // 空 UA 本身就是可疑訊號，交給後端分類
  if (ALWAYS_REPORT_PATHS.has(url.pathname.toLowerCase())) return true;
  return BOT_UA_RE.test(ua);
}

async function reportCrawler(env, request, url, status, responseTimeMs) {
  try {
    const token = env.SHELLFANS_INGEST_TOKEN;
    if (!token) return;
    const api = env.SHELLFANS_INGEST_API || DEFAULT_INGEST_API;
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
          status,
          userAgent: (request.headers.get('user-agent') || '').slice(0, 1024),
          // 真實 client IP：僅供 ingest 端做 hash / DNS 驗證，DB 不存明文
          ip: request.headers.get('cf-connecting-ip') || null,
          asn: cf.asn || null,
          country: cf.country || null,
          referer: (request.headers.get('referer') || '').slice(0, 512) || null,
          acceptLanguage: (request.headers.get('accept-language') || '').slice(0, 128) || null,
          responseTimeMs,
        },
      ],
    });

    await fetch(api, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-crawler-ingest-token': token,
        // 必須帶明確 UA：shell.fans zone 有一條「空 UA → managed_challenge」的
        // WAF 規則，沒帶 UA 的話上報會被我們自己的 WAF 擋成 403 挑戰頁，
        // 而且因為這裡靜默吞例外，症狀會是「Worker 有跑但完全沒資料」。
        'user-agent': 'ShellFansCrawlerMonitor/1.0 (+https://shell.fans/aeo-geo)',
      },
      body,
    });
  } catch (e) {
    /* 靜默：監控失敗絕不影響客戶站台 */
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const t0 = Date.now();

    // 先照常取得回應，監控完全不介入內容
    const response = await fetch(request);

    if (shouldReport(request, url)) {
      ctx.waitUntil(reportCrawler(env, request, url, response.status, Date.now() - t0));
    }

    return response;
  },
};
