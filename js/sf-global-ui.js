/*!
 * ShellFans Global UI runtime — 由 console.shell.fans 後台「UIUX Design → Global 共用元件」
 * 的已發布設定驅動 header / navigation / mobile menu / footer 品牌 logo。
 *
 * 來源：GET https://console.shell.fans/api/site/global-ui?site=shell（只回 published，不含草稿）
 *
 * ## 原則：靜態 baseline + 就地套用差異，而不是整段重繪
 *
 * shell.fans 是純靜態站。每一頁的 HTML 內建完整、正確的 header / nav / footer，
 * 爬蟲與不執行 JS 的環境看到的就是這份（<a href> 一律存在）。本腳本載入後才依
 * 已發布設定「就地」調整：以網址比對既有錨點，命中者只改文字／屬性並保留原本的
 * class 與結構；設定新增的項目才以既有錨點為範本建立；設定停用的才移除；最後依
 * 設定順序重排。任何失敗（API 逾時／非 200／格式異常／後端退回預設）都保留靜態版本。
 *
 * ## 支援的三種既有標記（全站共用同一支腳本，不為個別頁面另寫）
 *   1. 首頁型：<header class="nav"> nav.nav-menu > a.nav-link；#mobileMenu.mobile-menu；a.nav-cta
 *   2. Webflow 內容頁：.navbar.w-nav nav.nav-menu.w-nav-menu（項目間有分隔 div.footer-line-2、
 *      尾端有 .nav-button-wrapper 行動版按鈕——後者不動）
 *   3. Webflow 頁面上由 scripts/apply-unified-mobile-nav.py 注入的行動版：
 *      .sf-mob-header / #sfMobMenu.sf-mob-menu / a.sf-mob-cta
 *
 * ## 與其他腳本的分工
 *   · sf-footer.js 依 footer 設定渲染整個頁尾；本腳本只覆寫頁尾的雙語 logo，並在收到
 *     shellfans-footer-rendered 事件時重新套用（頁尾重繪會換掉 <img>）。
 *   · 頁面 i18n 引擎（data-i18n）：本腳本接手的 logo 與導覽錨點會移除 data-i18n，改由
 *     本腳本監聽 shellfans-locale-changed 自行切換，避免兩邊互相覆寫。
 *   · 只有具備 i18n 引擎的頁面才跟隨語系；純中文頁固定用中文（與訪客登入區塊同一規則）。
 */
(function () {
  'use strict';

  var API = 'https://console.shell.fans/api/site/global-ui?site=shell';
  var TIMEOUT_MS = 2500;   // 逾時就放棄本次結果，不讓後台拖慢前台
  var STORAGE_KEY = 'shellfans_locale';
  var CACHE_KEY = 'shellfans_global_ui_v2';
  var STYLE_ID = 'sf-global-ui-css';
  var HIDE = 'sf-gui-hidden';
  // 與後端 isSafeHref() 同一組協定白名單；javascript: / data: 一律不套用
  var SAFE = /^(https?:\/\/|mailto:|tel:|\/|#)/i;

  // 除錯／驗證用的唯讀狀態（不影響行為）
  var state = { version: 2, source: 'static', applied: 0, current: null };
  window.__sfGlobalUi = state;

  // -------------------------------------------------------------------------
  // 小工具
  // -------------------------------------------------------------------------

  function pageHasI18n() { return !!document.querySelector('[data-i18n]'); }

  // 與頁內 i18n 引擎、sf-footer.js 同一順序：cookie（伺服器也讀這個）→ localStorage → <html lang>
  function locale() {
    if (!pageHasI18n()) return 'zh-TW';
    var m = document.cookie.match(/(?:^|;\s*)shellfans_locale=(en|zh-TW)(?:;|$)/);
    if (m) return m[1];
    try { var s = localStorage.getItem(STORAGE_KEY); if (s === 'en' || s === 'zh-TW') return s; } catch (_) {}
    return document.documentElement.lang === 'en' ? 'en' : 'zh-TW';
  }

  function loc(ls, l) {
    if (typeof ls === 'string') return ls;
    if (!ls || typeof ls !== 'object') return '';
    return ls[l] || ls['zh-TW'] || '';
  }

  function safeHref(h) { return typeof h === 'string' && h.trim() !== '' && SAFE.test(h.trim()); }

  /** 比對用：絕對化、去尾斜線、小寫。相對路徑（Webflow 頁）與絕對網址視為同一項。 */
  function normHref(h) {
    try {
      var u = new URL(String(h || ''), window.location.href);
      return (u.origin + u.pathname).replace(/\/+$/, '').toLowerCase() + u.search;
    } catch (_) { return String(h || '').replace(/\/+$/, '').toLowerCase(); }
  }

  function toArray(list) { var out = []; for (var i = 0; i < list.length; i++) out.push(list[i]); return out; }
  function qsa(sel, root) { return toArray((root || document).querySelectorAll(sel)); }
  function hasClass(el, c) { return !!el && (' ' + (el.className || '') + ' ').indexOf(' ' + c + ' ') !== -1; }

  function visible(items, device) {
    var out = [];
    for (var i = 0; i < (items || []).length; i++) {
      var it = items[i];
      if (!it || !it.enabled) continue;
      if (device === 'desktop' ? !it.desktop : !it.mobile) continue;
      if (!safeHref(it.href)) continue;
      out.push(it);
    }
    out.sort(function (a, b) { return (a.order || 0) - (b.order || 0); });
    return out;
  }

  function ensureStyle() {
    if (document.getElementById(STYLE_ID)) return;
    var s = document.createElement('style');
    s.id = STYLE_ID;
    s.textContent =
      '.' + HIDE + '{display:none !important}' +
      'html.sf-gui-header-off header.nav,html.sf-gui-header-off .navbar.w-nav,html.sf-gui-header-off .sf-mob-header,' +
      'html.sf-gui-header-off #mobileMenu,html.sf-gui-header-off .sf-mob-menu{display:none !important}' +
      'html.sf-gui-nosticky header.nav,html.sf-gui-nosticky .sf-mob-header{position:absolute !important}' +
      'html.sf-gui-mobile-off #navHamburger,html.sf-gui-mobile-off #mobileMenu,' +
      'html.sf-gui-mobile-off .sf-mob-hamburger,html.sf-gui-mobile-off .sf-mob-menu{display:none !important}' +
      'html.sf-gui-nolang #langSwitcher,html.sf-gui-nolang .lang-switcher,html.sf-gui-nolang .home-header_location{display:none !important}' +
      '@media (max-width:991px){html.sf-gui-mobile-nolang #langSwitcher,html.sf-gui-mobile-nolang .lang-switcher{display:none !important}}';
    document.head.appendChild(s);
  }

  function flag(cls, on) {
    var h = document.documentElement;
    if (on) h.classList.add(cls); else h.classList.remove(cls);
  }

  function setHidden(el, hidden) { if (hidden) el.classList.add(HIDE); else el.classList.remove(HIDE); }

  function setLabel(a, text) {
    // Webflow 的 Klog 錨點內含 <div class="text-block-42">：有單一元素子節點時改它的文字，保留結構
    if (a.children.length === 1 && a.childNodes.length === 1) a.children[0].textContent = text;
    else a.textContent = text;
  }

  function setLink(a, it) {
    // 文字一律走 textContent，網址先過白名單；label 帶標記也不會被當成 HTML
    a.removeAttribute('data-i18n'); a.removeAttribute('data-i18n-attr');
    if (a.getAttribute('href') !== it.href) a.setAttribute('href', it.href);
    if (it.newTab) a.setAttribute('target', '_blank'); else a.removeAttribute('target');
    if (it.external || it.newTab) a.setAttribute('rel', 'noopener noreferrer'); else a.removeAttribute('rel');
  }

  function isAuthLink(a) {
    var h = a.getAttribute('href') || '';
    return a.hasAttribute('data-sf-guest-login') || /\/auth\/(login|register|logout)/.test(h) || hasClass(a, 'sf-engine-logout');
  }
  function isLoginLink(a) {
    return a.hasAttribute('data-sf-guest-login') || /\/auth\/login/.test(a.getAttribute('href') || '');
  }
  function isCtaEl(a) { return hasClass(a, 'nav-cta') || hasClass(a, 'mobile-cta') || hasClass(a, 'sf-mob-cta'); }

  // -------------------------------------------------------------------------
  // Logo（header 與 footer 各自雙語）
  // -------------------------------------------------------------------------

  function applyImgs(imgs, asset, l) {
    if (!asset) return;
    var src = loc(asset.src, l), alt = loc(asset.alt, l);
    if (!safeHref(src)) return;
    for (var i = 0; i < imgs.length; i++) {
      var img = imgs[i];
      // 接手後不再讓 i18n 引擎改寫（它會把 src 換回字典值）；語系切換由本腳本處理
      img.removeAttribute('data-i18n'); img.removeAttribute('data-i18n-attr');
      if (img.getAttribute('src') !== src) img.setAttribute('src', src);
      if (alt) img.setAttribute('alt', alt);
    }
  }

  function applyHeaderLogo(cfg, l) {
    var h = cfg.header || {};
    applyImgs(qsa('.nav-brand img, .nav-logo-wrapper img, .sf-mob-brand img, [data-sf-header-logo]'), h.logo, l);
    if (safeHref(h.logoHref)) {
      var links = qsa('a.nav-brand, a.nav-logo-wrapper, a.sf-mob-brand');
      for (var i = 0; i < links.length; i++) {
        if (links[i].getAttribute('href') !== h.logoHref) links[i].setAttribute('href', h.logoHref);
      }
    }
  }

  function applyFooterLogo(cfg, l) {
    if (!cfg.footerBrand) return;
    applyImgs(qsa('#sf-footer-root .sf-footer-brand img'), cfg.footerBrand.logo, l);
  }

  // -------------------------------------------------------------------------
  // 導覽：就地同步一組錨點
  // -------------------------------------------------------------------------

  /**
   * container：錨點所在容器；anchors：目前視為「導覽項目」的直屬錨點；
   * before：新序列要插在哪個節點之前（null = 尾端）；sep：Webflow 分隔線範本（可為 null）。
   * 設定為空時直接返回、保留靜態版本——避免後台誤存空清單就讓全站無法導航。
   */
  function syncNav(container, anchors, items, l, before, sep) {
    if (!container || items.length === 0) return;
    var byHref = {};
    for (var i = 0; i < anchors.length; i++) {
      var k = normHref(anchors[i].getAttribute('href'));
      if (!byHref[k]) byHref[k] = anchors[i];
    }
    var template = anchors[0] || null;
    var used = [];
    var frag = document.createDocumentFragment();

    for (var j = 0; j < items.length; j++) {
      var it = items[j];
      var a = byHref[normHref(it.href)];
      if (a && used.indexOf(a) !== -1) a = null;   // 設定裡同一網址出現兩次 → 第二個新建
      if (a) {
        used.push(a);
      } else {
        a = template ? template.cloneNode(false) : document.createElement('a');
        if (!template && container.tagName === 'NAV') a.className = 'nav-link';
        a.removeAttribute('data-sf-product'); a.removeAttribute('data-aeo-geo-link');
        a.removeAttribute('id'); a.removeAttribute('data-sf-gui-bound');
      }
      setLink(a, it);
      a.setAttribute('data-sf-nav-item', String(it.id || ''));
      setLabel(a, loc(it.label, l));
      setHidden(a, false);
      frag.appendChild(a);
      if (sep) frag.appendChild(sep.cloneNode(true));
    }

    // 設定中沒有的既有項目移除；舊分隔線整批移除（上面已重新產生）
    for (var m = 0; m < anchors.length; m++) {
      if (used.indexOf(anchors[m]) === -1 && anchors[m].parentNode) anchors[m].parentNode.removeChild(anchors[m]);
    }
    if (sep) {
      var kids = toArray(container.children);
      for (var n = 0; n < kids.length; n++) {
        if (kids[n].tagName === 'DIV' && hasClass(kids[n], 'footer-line-2')) container.removeChild(kids[n]);
      }
    }
    if (before && before.parentNode === container) container.insertBefore(frag, before);
    else container.appendChild(frag);
  }

  function applyDesktopNav(cfg, l) {
    var items = visible(cfg.navigation, 'desktop');
    var navs = qsa('nav.nav-menu');
    for (var n = 0; n < navs.length; n++) {
      var nav = navs[n];
      var kids = toArray(nav.children);
      var anchors = [], before = null, sep = null;
      for (var i = 0; i < kids.length; i++) {
        var k = kids[i];
        if (k.tagName === 'A') {
          if (!isAuthLink(k) && !isCtaEl(k)) anchors.push(k);
          else if (!before) before = k;
        } else if (hasClass(k, 'nav-button-wrapper')) {
          if (!before) before = k;               // Webflow 行動版按鈕群：新序列插在它之前
        } else if (k.tagName === 'DIV' && hasClass(k, 'footer-line-2')) {
          if (!sep) sep = k;
        }
      }
      syncNav(nav, anchors, items, l, before, sep);
    }
  }

  function bindClose(menu) {
    var hamb = document.getElementById(menu.id === 'sfMobMenu' ? 'sfMobHamburger' : 'navHamburger');
    var as = qsa('a', menu);
    for (var i = 0; i < as.length; i++) {
      if (as[i].getAttribute('data-sf-gui-bound')) continue;
      as[i].setAttribute('data-sf-gui-bound', '1');
      as[i].addEventListener('click', function () {
        menu.classList.remove('active');
        if (hamb) hamb.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    }
  }

  function applyMobileMenus(cfg, l) {
    var items = visible(cfg.navigation, 'mobile');
    var showLogin = !(cfg.mobile && cfg.mobile.showLogin === false);
    var menus = qsa('#mobileMenu, .mobile-menu, #sfMobMenu, .sf-mob-menu');
    var seen = [];
    for (var n = 0; n < menus.length; n++) {
      var menu = menus[n];
      if (seen.indexOf(menu) !== -1) continue;
      seen.push(menu);
      var kids = toArray(menu.children);
      var anchors = [], before = null;
      for (var i = 0; i < kids.length; i++) {
        var k = kids[i];
        if (k.tagName !== 'A') continue;
        if (!isAuthLink(k) && !isCtaEl(k)) anchors.push(k);
        else if (!before) before = k;             // 登入／CTA 區塊：導覽項目插在它之前，本身不動
      }
      syncNav(menu, anchors, items, l, before, null);
      var all = qsa('a', menu);
      for (var j = 0; j < all.length; j++) {
        if (isLoginLink(all[j])) setHidden(all[j], !showLogin);
      }
      bindClose(menu);
    }
  }

  // -------------------------------------------------------------------------
  // CTA（header 右側與行動選單底部）
  // -------------------------------------------------------------------------

  function syncCta(existing, items, l) {
    for (var i = 0; i < Math.max(existing.length, items.length); i++) {
      var a = existing[i], it = items[i];
      if (!it) { if (a) setHidden(a, true); continue; }
      if (!a) {
        var last = existing[existing.length - 1];
        if (!last || !last.parentNode) break;      // 頁面本來就沒有 CTA 位置 → 不憑空插入
        a = last.cloneNode(false);
        a.removeAttribute('id'); a.removeAttribute('data-sf-gui-bound');
        last.parentNode.insertBefore(a, last.nextSibling);
        existing.push(a);
      }
      setLink(a, it);
      a.setAttribute('data-sf-cta-item', String(it.id || ''));
      setLabel(a, loc(it.label, l));
      setHidden(a, false);
    }
  }

  function applyCtas(cfg, l) {
    var list = cfg.header && cfg.header.cta;
    if (!Array.isArray(list)) return;              // 缺欄位視為格式異常 → 保留靜態 CTA
    syncCta(qsa('.nav-actions a.nav-cta'), visible(list, 'desktop'), l);
    var m = visible(list, 'mobile');
    var menus = qsa('#mobileMenu, .mobile-menu, #sfMobMenu, .sf-mob-menu');
    var seen = [];
    for (var i = 0; i < menus.length; i++) {
      if (seen.indexOf(menus[i]) !== -1) continue;
      seen.push(menus[i]);
      syncCta(qsa('a.mobile-cta, a.sf-mob-cta', menus[i]), m, l);
    }
  }

  // -------------------------------------------------------------------------
  // 套用
  // -------------------------------------------------------------------------

  function validConfig(cfg) {
    return !!(cfg && typeof cfg === 'object' && cfg.header && typeof cfg.header === 'object' && Array.isArray(cfg.navigation));
  }

  function apply(cfg, source) {
    if (!validConfig(cfg)) return;
    ensureStyle();
    var l = locale();
    var h = cfg.header, m = cfg.mobile || {};
    try { applyHeaderLogo(cfg, l); } catch (_) {}
    try { applyFooterLogo(cfg, l); } catch (_) {}
    try { applyDesktopNav(cfg, l); } catch (_) {}
    try { applyMobileMenus(cfg, l); } catch (_) {}
    try { applyCtas(cfg, l); } catch (_) {}
    try {
      flag('sf-gui-header-off', h.enabled === false);
      flag('sf-gui-nosticky', h.sticky === false);
      flag('sf-gui-nolang', h.showLanguageSwitcher === false);
      flag('sf-gui-mobile-off', m.enabled === false);
      flag('sf-gui-mobile-nolang', m.showLanguageSwitcher === false);
    } catch (_) {}
    state.current = cfg;
    state.source = source || state.source;
    state.applied++;
  }

  // -------------------------------------------------------------------------
  // 取得設定
  // -------------------------------------------------------------------------

  function cached() {
    try { var raw = sessionStorage.getItem(CACHE_KEY); return raw ? JSON.parse(raw) : null; } catch (_) { return null; }
  }
  function cache(cfg) {
    try { sessionStorage.setItem(CACHE_KEY, JSON.stringify(cfg)); } catch (_) {}
  }

  function load() {
    // 先用本次瀏覽階段的快取即時套用，避免每頁都閃一下；之後仍向 API 取最新已發布版本
    var c = cached();
    if (validConfig(c)) apply(c, 'cache');

    if (!window.fetch) return;
    var late = false;
    var ctrl = (typeof AbortController === 'function') ? new AbortController() : null;
    var timer = setTimeout(function () { late = true; if (ctrl) ctrl.abort(); }, TIMEOUT_MS);

    fetch(API, ctrl ? { credentials: 'omit', signal: ctrl.signal } : { credentials: 'omit' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        clearTimeout(timer);
        if (late || !d || !d.data) return;
        // fallback:true 代表後端讀 DB 失敗、回的是內建預設值；那份預設值與靜態 HTML 相同，略過
        if (d.fallback) return;
        if (!validConfig(d.data)) return;
        cache(d.data);
        apply(d.data, 'api');
      })
      .catch(function () { clearTimeout(timer); /* 保留靜態版本 */ });
  }

  function init() {
    load();
    document.addEventListener('shellfans-locale-changed', function () {
      if (state.current) apply(state.current, state.source);
    });
    // sf-footer.js 每次重繪頁尾都會換掉 logo <img>，收到通知就補回雙語 logo
    document.addEventListener('shellfans-footer-rendered', function () {
      if (state.current) { try { applyFooterLogo(state.current, locale()); } catch (_) {} }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
