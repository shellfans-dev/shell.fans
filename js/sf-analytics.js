/*!
 * shell.fans AI referral attribution.
 *
 * 目的：量測「AI 回答引用 → 使用者點擊 → 落地 → 互動 → 轉換」這條鏈。
 *
 * ## 與爬蟲監測是兩件不同的事
 *
 * crawler_access_logs 記的是**機器**（GPTBot、ClaudeBot…）來抓頁面。
 * 本檔記的是**人**從 AI 回答點連結進來。兩者的分母、單位與意義都不同，
 * 報表上必須分開——把它們相加或相除會得出無意義的數字。
 *
 * ## 為什麼需要自訂事件，GA4 原生歸因不夠
 *
 * GA4 會把 utm_source=claude 記進 sessionSource，但：
 *   1. 各家 AI 的 referrer 與參數形式不一致，原生分類會散落在多個 channel
 *   2. 沒有 utm 參數時（使用者直接複製網址），referrer 是唯一線索
 *   3. 要在後續的轉換事件上帶著「這是 AI 來的」，必須自己保存 first-touch
 *
 * 因此：正規化成 ai_platform / traffic_channel 兩個自訂維度，
 * 存進 sessionStorage，之後的關鍵事件都附上。
 *
 * **不覆寫** GA4 原生的 source/medium——那是平台自己的歸因模型，
 * 動它會讓標準報表與自訂報表對不起來。
 *
 * ## 隱私
 *
 * 只送網址路徑、UTM 值、referrer 主機名與頁面標題。不送 email、電話、
 * 姓名、帳號 ID 或任何使用者輸入的文字。referrer 只取主機名，不取完整
 * 網址——AI 對話的網址常含 conversation id，那是可識別的。
 */
(function () {
  'use strict';

  var SS_KEY = 'sf_ai_attr';
  var FIRED_KEY = 'sf_ai_landing_fired';

  // 已知的 AI 答案引擎。值是正規化後的 ai_platform。
  // 鍵刻意同時涵蓋 utm_source 的常見寫法與 referrer 主機名。
  var PLATFORMS = {
    chatgpt: 'chatgpt',
    openai: 'chatgpt',
    'chat.openai.com': 'chatgpt',
    'chatgpt.com': 'chatgpt',
    claude: 'claude',
    anthropic: 'claude',
    'claude.ai': 'claude',
    perplexity: 'perplexity',
    'perplexity.ai': 'perplexity',
    'www.perplexity.ai': 'perplexity',
    gemini: 'gemini',
    'gemini.google.com': 'gemini',
    google_ai: 'gemini',
    bard: 'gemini',
    copilot: 'copilot',
    bing_chat: 'copilot',
    'copilot.microsoft.com': 'copilot'
  };

  function param(name) {
    try {
      return new URLSearchParams(window.location.search).get(name) || '';
    } catch (e) {
      return '';
    }
  }

  function norm(s) {
    return String(s || '').trim().toLowerCase();
  }

  function ss(op, key, val) {
    // sessionStorage 在隱私模式或第三方 cookie 封鎖下可能丟例外。
    // 失敗時降級成「不保存」而不是中斷——量測不該讓頁面壞掉。
    try {
      if (op === 'get') return window.sessionStorage.getItem(key);
      if (op === 'set') return window.sessionStorage.setItem(key, val);
    } catch (e) {
      return null;
    }
  }

  /**
   * 判定這次造訪是不是從 AI 回答來的。
   *
   * 兩條獨立的判準，任一成立即可：
   *   1. utm_medium == 'ai_answer'（我們自己在 llms.txt / 內容裡放的連結）
   *   2. utm_source 或 referrer 主機名在已知平台清單裡
   *
   * 第 2 條的存在理由：使用者常常是直接複製 AI 給的網址，那個網址不會帶
   * 我們的 utm。只靠 utm 會漏掉相當一部分真實的 AI 導流。
   */
  function detect() {
    var src = norm(param('utm_source'));
    var med = norm(param('utm_medium'));
    var host = '';
    try {
      host = document.referrer ? norm(new URL(document.referrer).hostname) : '';
    } catch (e) {
      host = '';
    }

    var platform = PLATFORMS[src] || PLATFORMS[host] || '';
    var isAi = med === 'ai_answer' || !!platform;
    if (!isAi) return null;

    return {
      ai_platform: platform || (src || 'unknown'),
      traffic_channel: 'ai_referral',
      utm_source: src,
      utm_medium: med,
      utm_campaign: norm(param('utm_campaign')),
      utm_content: norm(param('utm_content')),
      utm_term: norm(param('utm_term')),
      // 只存主機名。AI 對話的完整網址常帶 conversation id，屬可識別資訊。
      referrer_host: host,
      first_landing_path: window.location.pathname
    };
  }

  /** 本 session 的 first-touch 歸因；沒有就回 null。 */
  function stored() {
    var raw = ss('get', SS_KEY);
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  function gtagSafe() {
    return typeof window.gtag === 'function' ? window.gtag : null;
  }

  /**
   * 對外 API：取得目前 session 的 AI 歸因，供其他腳本在送轉換事件時附帶。
   * 沒有歸因時回空物件，呼叫端可以無條件展開。
   */
  function attribution() {
    var a = stored();
    if (!a) return {};
    return {
      ai_platform: a.ai_platform,
      traffic_channel: a.traffic_channel,
      utm_campaign: a.utm_campaign,
      first_landing_path: a.first_landing_path
    };
  }

  /**
   * 送一個帶 AI 歸因的事件。非 AI session 也會送，只是不帶那幾個欄位——
   * 這樣呼叫端不必自己判斷，且轉換率的分母（全部轉換）仍然完整。
   */
  function track(eventName, params) {
    var g = gtagSafe();
    if (!g || !eventName) return;
    var payload = {};
    var attr = attribution();
    for (var k in attr) if (Object.prototype.hasOwnProperty.call(attr, k)) payload[k] = attr[k];
    if (params) {
      for (var p in params) if (Object.prototype.hasOwnProperty.call(params, p)) payload[p] = params[p];
    }
    g('event', eventName, payload);
  }

  function init() {
    var g = gtagSafe();
    if (!g) return; // GA4 未載入（例如被擋）——靜默略過，不報錯

    // first-touch：已經有歸因就不覆寫。使用者在站內點第二頁時網址沒有 utm，
    // 若每頁重算會把歸因洗成 null，轉換事件就失去來源。
    var attr = stored();
    if (!attr) {
      attr = detect();
      if (attr) ss('set', SS_KEY, JSON.stringify(attr));
    }
    if (!attr) return;

    // 每個 session 只送一次 landing 事件。同一個 session 內重整或返回上一頁
    // 都不該再記一次落地——那會讓 AI 推薦流量的 session 數被灌水。
    if (ss('get', FIRED_KEY) === '1') return;
    ss('set', FIRED_KEY, '1');

    g('event', 'ai_referral_landing', {
      ai_platform: attr.ai_platform,
      traffic_channel: attr.traffic_channel,
      landing_path: attr.first_landing_path,
      utm_source: attr.utm_source,
      utm_medium: attr.utm_medium,
      utm_campaign: attr.utm_campaign,
      utm_content: attr.utm_content,
      referrer_host: attr.referrer_host,
      page_title: document.title
    });
  }

  // 對外命名空間。其他腳本（例如檢測工具、聯絡表單）用
  // window.sfAnalytics.track('aeo_scan_complete', {...}) 送事件即可，
  // AI 歸因會自動附上。
  window.sfAnalytics = {
    track: track,
    attribution: attribution,
    isAiReferral: function () {
      return !!stored();
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
