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

  function byOrder(a, b) { return (a.order || 0) - (b.order || 0); }

  function visible(items, device) {
    var out = [];
    for (var i = 0; i < (items || []).length; i++) {
      var it = items[i];
      if (!it || !it.enabled) continue;
      if (device === 'desktop' ? !it.desktop : !it.mobile) continue;
      if (!safeHref(it.href)) continue;
      out.push(it);
    }
    out.sort(byOrder);
    return out;
  }

  /**
   * 兩層導覽的「有效可見」樹（與後端 visibleNavTree 同規則）：
   *   父層停用 → 整組不顯示；子項依自己 enabled + 裝置 + 安全網址過濾、排序；
   *   純下拉父層（無安全網址）若沒有可見子項 → 不顯示空下拉。
   * 回傳的父層物件多帶 __kids（可見子項；可能為空陣列，代表「有 href 的一般連結」）。
   */
  function visibleTree(items, device) {
    var out = [];
    for (var i = 0; i < (items || []).length; i++) {
      var it = items[i];
      if (!it || !it.enabled) continue;
      if (device === 'desktop' ? !it.desktop : !it.mobile) continue;
      var kids = [];
      var ch = it.children || [];
      for (var j = 0; j < ch.length; j++) {
        var c = ch[j];
        if (!c || !c.enabled) continue;
        if (device === 'desktop' ? !c.desktop : !c.mobile) continue;
        if (!safeHref(c.href)) continue;
        kids.push(c);
      }
      kids.sort(byOrder);
      if (!safeHref(it.href) && kids.length === 0) continue;   // 空的純下拉 → 略過
      var copy = {}; for (var key in it) { if (Object.prototype.hasOwnProperty.call(it, key)) copy[key] = it[key]; }
      copy.__kids = kids;
      out.push(copy);
    }
    out.sort(byOrder);
    return out;
  }

  function anyHierarchy(items) {
    for (var i = 0; i < (items || []).length; i++) {
      var c = items[i] && items[i].children;
      if (c && c.length) return true;
    }
    return false;
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
      '@media (max-width:991px){html.sf-gui-mobile-nolang #langSwitcher,html.sf-gui-mobile-nolang .lang-switcher{display:none !important}}' +
      // --- 兩層導覽：桌機下拉 / 手機手風琴（只在有子選單時才會建立這些節點）---
      '.sf-gui-group{position:relative;display:inline-flex;align-items:center}' +
      '.sf-gui-parent{cursor:pointer}' +
      '.sf-gui-caret{font-size:.72em;margin-left:.15em;opacity:.7}' +
      '.sf-gui-submenu{display:none;position:absolute;top:100%;left:0;min-width:180px;background:#fff;' +
      'border:1px solid #e6e6e6;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.10);padding:6px;z-index:1200}' +
      '.sf-gui-group:hover>.sf-gui-submenu,.sf-gui-group:focus-within>.sf-gui-submenu,' +
      '.sf-gui-group.sf-gui-open>.sf-gui-submenu{display:block}' +
      '.sf-gui-submenu>.sf-gui-subitem{display:block;white-space:nowrap;padding:7px 12px;border-radius:6px;color:inherit;text-decoration:none}' +
      '.sf-gui-submenu>.sf-gui-subitem:hover,.sf-gui-submenu>.sf-gui-subitem:focus{background:#f4f4f5}' +
      '.sf-gui-toggle{background:none;border:0;padding:4px 10px;cursor:pointer;font:inherit;color:inherit;line-height:1}' +
      // 手機：手風琴改為 block、submenu 靜態展開
      '.sf-gui-acc{display:block;position:static;width:100%}' +
      '.sf-gui-acc>.sf-gui-submenu{position:static;display:none;min-width:0;border:0;box-shadow:none;padding:0 0 4px 16px}' +
      '.sf-gui-acc.sf-gui-open>.sf-gui-submenu{display:block}';
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
  // 把先前建立的下拉／手風琴群組還原成扁平錨點，讓每次 apply() 都能重新計算（locale 切換會重跑）。
  function unwrapGroups(container) {
    var groups = qsa('.sf-gui-group', container);
    for (var i = 0; i < groups.length; i++) {
      var g = groups[i];
      var parentA = g.querySelector('a.sf-gui-parent') || g.querySelector('a');
      if (parentA) {
        var caret = parentA.querySelector('.sf-gui-caret');
        if (caret) parentA.removeChild(caret);
        parentA.classList.remove('sf-gui-parent');
        parentA.removeAttribute('aria-haspopup'); parentA.removeAttribute('aria-expanded');
        parentA.removeAttribute('role'); parentA.removeAttribute('tabindex');
        parentA.removeAttribute('data-sf-gui-bound');
        if (g.parentNode) g.parentNode.insertBefore(parentA, g);   // 移回扁平位置供 href 比對
      }
      if (g.parentNode) g.parentNode.removeChild(g);                // 連同 submenu、toggle、複製的子錨點一起丟棄
    }
  }

  function buildSubItem(template, kid, l) {
    var ca = template ? template.cloneNode(false) : document.createElement('a');
    ca.className = 'sf-gui-subitem';
    ca.removeAttribute('id'); ca.removeAttribute('data-sf-product'); ca.removeAttribute('data-aeo-geo-link');
    ca.removeAttribute('data-sf-gui-bound'); ca.removeAttribute('aria-haspopup'); ca.removeAttribute('aria-expanded');
    setLink(ca, kid);
    ca.setAttribute('role', 'menuitem');
    ca.setAttribute('data-sf-nav-item', String(kid.id || ''));
    setLabel(ca, loc(kid.label, l));
    setHidden(ca, false);
    return ca;
  }

  // 鍵盤 / aria：Escape 收合並回到父層；純下拉父層 Enter/Space 開合；手機 caret 為真正的 toggle 按鈕。
  function wireGroup(group, mode, parentA, toggleEl) {
    function open(v) {
      if (v) group.classList.add('sf-gui-open'); else group.classList.remove('sf-gui-open');
      parentA.setAttribute('aria-expanded', v ? 'true' : 'false');
      if (toggleEl && toggleEl !== parentA) toggleEl.setAttribute('aria-expanded', v ? 'true' : 'false');
    }
    function toggle() { open(!group.classList.contains('sf-gui-open')); }
    group.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' || e.keyCode === 27) { open(false); if (parentA.focus) parentA.focus(); }
    });
    var noHref = !parentA.getAttribute('href');
    if (mode === 'mobile') {
      if (toggleEl) toggleEl.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); toggle(); });
      if (noHref) parentA.addEventListener('click', function (e) { e.preventDefault(); toggle(); });
    } else {
      // 桌機：hover / focus-within 由 CSS 顯示；純下拉父層再加上點擊與鍵盤開合
      if (noHref) {
        parentA.addEventListener('click', function (e) { e.preventDefault(); toggle(); });
        parentA.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ' || e.keyCode === 13 || e.keyCode === 32) { e.preventDefault(); toggle(); }
        });
      }
      group.addEventListener('focusout', function (e) {
        if (!group.contains(e.relatedTarget)) open(false);
      });
    }
  }

  function makeGroup(a, it, l, mode) {
    var group = document.createElement('div');
    group.className = 'sf-gui-group' + (mode === 'mobile' ? ' sf-gui-acc' : '');
    group.setAttribute('data-sf-nav-group', String(it.id || ''));
    a.classList.add('sf-gui-parent');
    a.setAttribute('aria-haspopup', 'true');
    a.setAttribute('aria-expanded', 'false');
    if (!safeHref(it.href)) { a.removeAttribute('href'); a.setAttribute('role', 'button'); a.setAttribute('tabindex', '0'); }

    var sub = document.createElement('div');
    sub.className = 'sf-gui-submenu';
    sub.setAttribute('role', 'menu');
    var subId = 'sf-gui-sub-' + String(it.id || Math.random().toString(36).slice(2));
    sub.id = subId;
    a.setAttribute('aria-controls', subId);
    for (var k = 0; k < it.__kids.length; k++) sub.appendChild(buildSubItem(a.cloneNode(false), it.__kids[k], l));

    var toggleEl = null;
    if (mode === 'mobile') {
      toggleEl = document.createElement('button');
      toggleEl.type = 'button';
      toggleEl.className = 'sf-gui-toggle';
      toggleEl.setAttribute('aria-expanded', 'false');
      toggleEl.setAttribute('aria-controls', subId);
      toggleEl.setAttribute('aria-label', loc(it.label, l) + ' 子選單');
      toggleEl.textContent = '▾';
      group.appendChild(a);
      group.appendChild(toggleEl);
    } else {
      var caret = document.createElement('span');
      caret.className = 'sf-gui-caret'; caret.setAttribute('aria-hidden', 'true'); caret.textContent = '▾';
      a.appendChild(caret);
      group.appendChild(a);
    }
    group.appendChild(sub);
    wireGroup(group, mode, a, toggleEl || a);
    return group;
  }

  function syncNav(container, anchors, items, l, before, sep, mode) {
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
      var a = safeHref(it.href) ? byHref[normHref(it.href)] : null;
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
      // 有可見子選單 → 包成下拉／手風琴群組；否則維持扁平錨點（扁平資料下與原行為完全相同）
      if (it.__kids && it.__kids.length) {
        frag.appendChild(makeGroup(a, it, l, mode || 'desktop'));
      } else {
        frag.appendChild(a);
      }
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
    var items = visibleTree(cfg.navigation, 'desktop');
    var navs = qsa('nav.nav-menu');
    for (var n = 0; n < navs.length; n++) {
      var nav = navs[n];
      unwrapGroups(nav);                       // 還原上一次建立的群組，讓 re-apply 冪等
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
      syncNav(nav, anchors, items, l, before, sep, 'desktop');
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
    var items = visibleTree(cfg.navigation, 'mobile');
    var showLogin = !(cfg.mobile && cfg.mobile.showLogin === false);
    var menus = qsa('#mobileMenu, .mobile-menu, #sfMobMenu, .sf-mob-menu');
    var seen = [];
    for (var n = 0; n < menus.length; n++) {
      var menu = menus[n];
      if (seen.indexOf(menu) !== -1) continue;
      seen.push(menu);
      unwrapGroups(menu);                      // re-apply 冪等
      var kids = toArray(menu.children);
      var anchors = [], before = null;
      for (var i = 0; i < kids.length; i++) {
        var k = kids[i];
        if (k.tagName !== 'A') continue;
        if (!isAuthLink(k) && !isCtaEl(k)) anchors.push(k);
        else if (!before) before = k;             // 登入／CTA 區塊：導覽項目插在它之前，本身不動
      }
      syncNav(menu, anchors, items, l, before, null, 'mobile');
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
