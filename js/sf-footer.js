/*!
 * shell.fans unified footer renderer.
 *
 * Renders the site footer into <div id="sf-footer-root"> from the live config
 * served by console.shell.fans (GET https://console.shell.fans/api/site/footer?site=shell, CORS),
 * falling back to the embedded SHELL_BASE defaults if the fetch fails. Edits
 * made in the console.shell.fans admin (UIUX Design → Footer 頁尾, site=shell.fans)
 * therefore appear on shell.fans on the next page load — no redeploy.
 *
 * Locale: reuses localStorage key 'shellfans_locale' and the
 * 'shellfans-locale-changed' CustomEvent shared with the page i18n engine, so
 * the footer stays in sync with the nav language switcher on pages that have
 * one, and provides its own toggle on pages that don't.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'shellfans_locale';
  var API = 'https://console.shell.fans/api/site/footer?site=shell';

  // Embedded defaults (mirror of saas_womm DEFAULT_FOOTER_SETTINGS.shell).
  var SHELL_BASE = {
    logo: { src: 'https://shell.fans/images/nav_logo.svg', alt: 'ShellFans AI' },
    description: {
      'zh-TW': '跨平台社群 AI 指揮中心。保存社群資產，看懂粉絲，同步經營與口碑成長。',
      en: 'Cross-platform Social AI Command. Preserve social assets, understand fans, grow engagement and reputation in sync.'
    },
    linkGroups: [
      { title: { 'zh-TW': '產品', en: 'Product' }, links: [
        { label: { 'zh-TW': '續航引擎', en: 'Engagement Engine' }, href: 'https://shell.fans/endurance' },
        { label: { 'zh-TW': '粉絲分析', en: 'Fans Analysis' }, href: 'https://shell.fans/fans-analysis' },
        { label: { 'zh-TW': '口碑行銷', en: 'Word-of-Mouth' }, href: 'https://console.shell.fans', external: true },
        { label: { 'zh-TW': '查看方案', en: 'Pricing' }, href: 'https://shell.fans/pricing', external: true }
      ] },
      { title: { 'zh-TW': '資源', en: 'Resources' }, links: [
        { label: { 'zh-TW': 'Klog 部落格', en: 'Klog Blog' }, href: 'https://blog.shell.fans/', external: true },
        { label: { 'zh-TW': '幫助中心', en: 'Help Center' }, href: 'https://shell.fans/helpcenter' },
        { label: { 'zh-TW': '客服支援', en: 'Support' }, href: 'https://shell.fans/support' }
      ] },
      { title: { 'zh-TW': '聯繫', en: 'Contact' }, links: [
        { label: { 'zh-TW': '關於我們', en: 'About Us' }, href: 'https://shell.fans/contact' },
        { label: { 'zh-TW': '歡迎聯繫', en: 'Contact Us' }, href: 'https://shell.fans/contact' },
        { label: { 'zh-TW': '創辦人', en: 'Co-Founder' }, href: 'https://shell.fans/co-founder' }
      ] }
    ],
    company: { lines: [
      { text: { 'zh-TW': '唄粉智能科技股份有限公司', en: 'ShellFans AI Technology Co., Ltd.' } },
      { text: { 'zh-TW': '地址：臺北市內湖區瑞光路335號4樓', en: 'Address: 4F, No. 335, Ruiguang Rd., Neihu Dist., Taipei' } },
      { text: { 'zh-TW': '信箱：hello@shell.fans', en: 'Email: hello@shell.fans' }, href: 'mailto:hello@shell.fans' },
      { text: { 'zh-TW': '電話：02-77143635', en: 'Phone: 02-77143635' }, href: 'tel:0277143635' },
      { text: { 'zh-TW': '統編：83032387', en: 'Business ID: 83032387' } }
    ] },
    patent: {
      before: { 'zh-TW': '唄粉智能科技及其產品受商標、', en: 'ShellFans AI Technology and its products are protected by trademark, ' },
      linkText: { 'zh-TW': '發明專利 I908295(臺灣)', en: 'Invention Patent I908295 (Taiwan)' },
      linkHref: 'https://tiponet.tipo.gov.tw/gpss2/gpsskmc/gpssbkm?!!FRURLTWI908295B',
      after: { 'zh-TW': '及其他申請中美國、日本之專利保護。', en: ', and other patents pending in the US and Japan.' }
    },
    copyright: {
      text: {
        'zh-TW': '© 2026 ShellFans AI. 唄粉智能科技股份有限公司. All rights reserved.',
        en: '© 2026 ShellFans AI. ShellFans AI Technology Co., Ltd. All rights reserved.'
      },
      html: ''
    },
    social: [
      { platform: 'Facebook', url: 'https://www.facebook.com/profile.php?id=61581243232686', iconUrl: 'https://shell.fans/images/facebook.svg' },
      { platform: 'Instagram', url: 'https://www.instagram.com/shell_fansai/', iconUrl: 'https://shell.fans/images/instagram.svg' }
    ],
    legal: [
      { label: { 'zh-TW': '隱私權政策', en: 'Privacy Policy' }, href: 'https://shell.fans/privacy-policy' },
      { label: { 'zh-TW': '服務條款', en: 'Terms of Service' }, href: 'https://shell.fans/terms-and-conditions' }
    ],
    display: {
      showFooter: true, showLogo: true, showDescription: true, showCompany: true,
      showPatent: true, showSocial: true, showCopyright: true, showLegal: true,
      showLanguageSwitcher: true, themeVariant: 'default'
    }
  };

  var lastCfg = SHELL_BASE;
  var SAFE = /^(https?:\/\/|mailto:|tel:|\/|#)/i;

  function getLocale() {
    try { return localStorage.getItem(STORAGE_KEY) === 'en' ? 'en' : 'zh-TW'; } catch (e) { return 'zh-TW'; }
  }
  function loc(ls, l) { return ls ? (ls[l] || ls['zh-TW'] || '') : ''; }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function safe(h) { if (h == null) return false; h = String(h).trim(); return h === '' || h === '#' || SAFE.test(h); }
  function linkAttrs(href, external) {
    var a = 'href="' + esc(href) + '"';
    if (external || /^https?:\/\//i.test(href)) a += ' target="_blank" rel="noopener noreferrer"';
    return a;
  }
  function globeSvg() {
    return '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"></circle><path d="M2 12h20"></path><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>';
  }

  function build(cfg, l) {
    var d = cfg.display || {};
    if (d.showFooter === false) return '';
    var h = '<div class="sf-container">';

    // top: brand + columns
    h += '<div class="sf-footer-top"><div><div class="sf-footer-brand">';
    if (d.showLogo !== false && cfg.logo && cfg.logo.src) {
      h += '<img decoding="async" loading="lazy" src="' + esc(cfg.logo.src) + '" alt="' + esc(cfg.logo.alt || '') + '" width="162" height="32">';
    }
    h += '</div>';
    if (d.showDescription !== false && loc(cfg.description, l)) {
      h += '<p class="sf-footer-desc">' + esc(loc(cfg.description, l)) + '</p>';
    }
    h += '</div>';
    (cfg.linkGroups || []).forEach(function (g) {
      if (g.enabled === false) return;
      h += '<div class="sf-footer-col"><h3>' + esc(loc(g.title, l)) + '</h3>';
      (g.links || []).forEach(function (lk) {
        if (lk.enabled === false || !safe(lk.href)) return;
        h += '<a ' + linkAttrs(lk.href, lk.external) + '>' + esc(loc(lk.label, l)) + '</a>';
      });
      h += '</div>';
    });
    h += '</div>';

    // company
    if (d.showCompany !== false && cfg.company && (cfg.company.lines || []).length) {
      h += '<div class="sf-footer-company" aria-label="' + (l === 'en' ? 'Company info' : '公司資訊') + '">';
      cfg.company.lines.forEach(function (ln) {
        var t = loc(ln.text, l);
        if (!t) return;
        if (ln.href && safe(ln.href)) h += '<span class="sf-footer-company-row"><a href="' + esc(ln.href) + '">' + esc(t) + '</a></span>';
        else h += '<span class="sf-footer-company-row">' + esc(t) + '</span>';
      });
      h += '</div>';
    }

    // patent
    if (d.showPatent !== false && cfg.patent) {
      var p = cfg.patent;
      h += '<div class="sf-footer-patent"><span>' + esc(loc(p.before, l)) + '</span>';
      if (safe(p.linkHref)) h += '<a href="' + esc(p.linkHref) + '" target="_blank" rel="noopener noreferrer">' + esc(loc(p.linkText, l)) + '</a>';
      h += '<span>' + esc(loc(p.after, l)) + '</span></div>';
    }

    // bottom row
    h += '<div class="sf-footer-bottom">';
    if (d.showCopyright !== false && cfg.copyright) {
      var ct = loc(cfg.copyright.text, l);
      if (ct) h += '<span class="sf-footer-copy">' + esc(ct) + '</span>';
    }
    if (d.showLanguageSwitcher !== false) {
      var other = l === 'zh-TW' ? 'English' : '繁體中文';
      h += '<button type="button" class="sf-footer-lang" data-sf-lang aria-label="' +
        (l === 'en' ? 'Switch language' : '切換語言') + '">' + globeSvg() + '<span>' + esc(other) + '</span></button>';
    }
    if (d.showSocial !== false && (cfg.social || []).length) {
      h += '<div class="sf-footer-social" aria-label="' + (l === 'en' ? 'Social links' : '社群連結') + '">';
      cfg.social.forEach(function (s) {
        if (s.enabled === false || !safe(s.url)) return;
        h += '<a href="' + esc(s.url) + '" target="_blank" rel="noopener noreferrer" aria-label="' + esc(s.platform) + '">' +
          '<img decoding="async" loading="lazy" src="' + esc(s.iconUrl) + '" alt="' + esc(s.platform) + '" width="14" height="14"></a>';
      });
      h += '</div>';
    }
    if (d.showLegal !== false && (cfg.legal || []).length) {
      h += '<div class="sf-footer-legal">';
      cfg.legal.forEach(function (lk) {
        if (lk.enabled === false || !safe(lk.href)) return;
        h += '<a ' + linkAttrs(lk.href, lk.external) + '>' + esc(loc(lk.label, l)) + '</a>';
      });
      h += '</div>';
    }
    // copyright.html is sanitized server-side on write; insert as-is.
    if (cfg.copyright && cfg.copyright.html) h += '<span class="sf-footer-extra">' + cfg.copyright.html + '</span>';
    h += '</div></div>';
    return h;
  }

  function render(cfg, l) {
    var mount = document.getElementById('sf-footer-root');
    if (!mount) return;
    mount.innerHTML = build(cfg, l);
    var btn = mount.querySelector('[data-sf-lang]');
    if (btn) {
      btn.addEventListener('click', function () {
        var next = getLocale() === 'zh-TW' ? 'en' : 'zh-TW';
        if (typeof window.__setLocale === 'function') {
          window.__setLocale(next); // page i18n engine persists + fires the event we listen to
        } else {
          try { localStorage.setItem(STORAGE_KEY, next); } catch (e) {}
          document.dispatchEvent(new CustomEvent('shellfans-locale-changed', { detail: { locale: next } }));
          render(lastCfg, next);
        }
      });
    }
  }

  function init() {
    // console.shell.fans 依賴已切斷（口碑行銷封存）— footer 僅由內建 SHELL_BASE 渲染，
    // 不再 runtime fetch console.shell.fans/api/site/footer。查看方案 = shell.fans/pricing。
    render(SHELL_BASE, getLocale());
    document.addEventListener('shellfans-locale-changed', function (e) {
      var nl = e && e.detail && e.detail.locale === 'en' ? 'en' : (e && e.detail && e.detail.locale ? 'zh-TW' : getLocale());
      render(lastCfg, nl);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

/*!
 * ShellFans 產品服務開關 — 依 console.shell.fans 後台設定隱藏 nav / footer 的產品入口。
 *
 * 讀取 GET https://console.shell.fans/api/site/product-flags（CORS）。當某產品開關為
 * false 時，實際從 DOM 移除對應的連結（桌機 nav、手機 nav、footer），而非
 * 只用 CSS 隱藏。讀取失敗一律維持顯示（fallback = 啟用），不影響其他 nav。
 *
 *   kolfans_wom_enabled            → 口碑行銷      (data-i18n="nav.wordOfMouth")
 *   shellfans_endurance_engine_...  → 續航引擎      (data-i18n="nav.engine")
 *   aeo_geo_managed_hosting_enabled → AEO/GEO 代管  (data-i18n="nav.aeoGeo")
 */
(function () {
  'use strict';
  var FLAGS_API = 'https://console.shell.fans/api/site/product-flags';

  // flag key → { i18n: nav data-i18n 值, text: 精確顯示文字 }
  var PRODUCTS = [
    { flag: 'kolfans_wom_enabled', i18n: 'nav.wordOfMouth', text: '口碑行銷' },
    { flag: 'shellfans_endurance_engine_enabled', i18n: 'nav.engine', text: '續航引擎' },
    { flag: 'aeo_geo_managed_hosting_enabled', i18n: 'nav.aeoGeo', text: 'AEO/GEO 代管' }
  ];
  // 僅在導覽/頁尾容器內以「文字」比對移除，避免誤刪頁面內文中的連結。
  var CONTAINER_SEL = 'nav,header,footer,[role="banner"],[class*="nav"],[class*="footer"],#sf-footer-root';

  function removeProduct(p) {
    var seen = [];
    // 1) 現代 nav：data-i18n 精確命中（桌機 + 手機）
    var byI18n = document.querySelectorAll('a[data-i18n="' + p.i18n + '"]');
    for (var i = 0; i < byI18n.length; i++) seen.push(byI18n[i]);
    // 2) 舊版 nav / footer：文字精確等於且位於導覽/頁尾容器內
    var anchors = document.getElementsByTagName('a');
    for (var j = 0; j < anchors.length; j++) {
      var a = anchors[j];
      if ((a.textContent || '').trim() !== p.text) continue;
      if (a.closest && a.closest(CONTAINER_SEL) && seen.indexOf(a) === -1) seen.push(a);
    }
    for (var k = 0; k < seen.length; k++) {
      var el = seen[k];
      if (el && el.parentNode) el.parentNode.removeChild(el);
    }
  }

  function apply(flags) {
    for (var i = 0; i < PRODUCTS.length; i++) {
      if (flags[PRODUCTS[i].flag] === false) removeProduct(PRODUCTS[i]);
    }
  }

  function run() {
    // console.shell.fans 依賴已切斷（口碑行銷封存）— flags 就地烘焙，不再 runtime fetch
    // console.shell.fans/api/site/product-flags。口碑行銷封存 → kolfans 關（移除口碑行銷入口）。
    var d = {
      shellfans_endurance_engine_enabled: true,
      kolfans_wom_enabled: false,
      aeo_geo_managed_hosting_enabled: true
    };
    apply(d);
    // footer 由上方 sf-footer 非同步注入，稍後再掃兩次確保涵蓋。
    setTimeout(function () { apply(d); }, 400);
    setTimeout(function () { apply(d); }, 1200);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();

/*!
 * 續航(app.shell.fans)登入狀態 — 讀 .shell.fans 共用 cookie `sf_user`(由續航登入時
 * 寫入,只含顯示名)，在 nav 右上角顯示續航登入者、選單導向 app.shell.fans。
 * 取代對 console.shell.fans/api/auth/me 的依賴(封存中)。HTML 內 applyKolFansLoginUI
 * 已加守衛:有 sf_user 時 console 不覆蓋此顯示。
 */
(function () {
  'use strict';
  function getCookie(n) {
    var m = document.cookie.match('(?:^|; )' + n + '=([^;]*)');
    return m ? decodeURIComponent(m[1]) : '';
  }
  // 續航統一登出：清掉續航 session + sf_user cookie 後導回本站，
  // 讓 shell.fans 與 app.shell.fans 的登入狀態一致。
  function goLogout(e) {
    if (e) e.preventDefault();
    window.location.href =
      'https://app.shell.fans/auth/logout?next=' +
      encodeURIComponent(window.location.origin + '/');
  }
  function apply() {
    var name = getCookie('sf_user');
    if (!name) return;
    var d = name.length > 18 ? name.slice(0, 16) + '…' : name;
    var VAULT = 'https://app.shell.fans/console/vault';

    // 結構 1：index / aeo-geo 的 #navLoginToggle + #navLogin .nav-login-list
    var toggle = document.getElementById('navLoginToggle');
    if (toggle) {
      toggle.innerHTML = '<span>' + d + '</span><span class="caret">▾</span>';
      toggle.setAttribute('title', name);
    }
    var list = document.querySelector('#navLogin .nav-login-list');
    if (list) {
      list.innerHTML =
        '<a href="' + VAULT + '" target="_blank" rel="noopener" role="menuitem">會員中心</a>' +
        '<a href="#" id="sfEngineLogout" role="menuitem">登出</a>';
      var lo = document.getElementById('sfEngineLogout');
      if (lo) lo.addEventListener('click', goLogout);
    }

    // 結構 2：內容頁(pricing 等 14 頁)的 Webflow dropdown .login-dd-toggle / .login-dd-list
    var ddToggles = document.querySelectorAll('.login-dd-toggle');
    for (var i = 0; i < ddToggles.length; i++) {
      var sp = ddToggles[i].querySelector('span');
      if (sp) sp.textContent = d; else ddToggles[i].insertAdjacentHTML('afterbegin', '<span>' + d + '</span>');
      ddToggles[i].setAttribute('title', name);
    }
    var ddLists = document.querySelectorAll('.login-dd-list');
    for (var j = 0; j < ddLists.length; j++) {
      ddLists[j].innerHTML =
        '<a href="' + VAULT + '" target="_blank" rel="noopener" class="w-dropdown-link" style="padding:10px 18px;color:#292929;font-weight:500;">會員中心</a>' +
        '<a href="#" class="w-dropdown-link sf-engine-logout" style="padding:10px 18px;color:#292929;font-weight:500;cursor:pointer;">登出</a>';
    }

    // 結構 3：簡單 nav(co-founder / social-media-backup / what-is-shellfans)的 .nav-actions
    // 靜態「登入」「開始使用」按鈕 → 登入者姓名(→會員中心) + 登出
    var acts = document.querySelectorAll('.nav-actions');
    for (var k = 0; k < acts.length; k++) {
      var loginBtn = acts[k].querySelector('a.btn-secondary');
      if (loginBtn && /登入|login/i.test(loginBtn.textContent)) {
        loginBtn.textContent = d;
        loginBtn.setAttribute('href', VAULT);
        loginBtn.setAttribute('target', '_blank');
        loginBtn.setAttribute('title', name);
      }
      var cta = acts[k].querySelector('a.btn-primary');
      if (cta && /開始使用|start|sign ?up|register/i.test(cta.textContent)) {
        cta.textContent = '登出';
        cta.setAttribute('href', '#');
        cta.removeAttribute('target');
        cta.classList.add('sf-engine-logout');
      }
    }

    // 綁定所有登出鈕(結構 2/3 共用 class)
    var outs = document.querySelectorAll('.sf-engine-logout');
    for (var m = 0; m < outs.length; m++) outs[m].addEventListener('click', goLogout);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply);
  else apply();
})();

/*!
 * 訪客登入入口 — nav 上區分兩種身分的登入目的地：
 *   網紅登入 → app.shell.fans/auth/login      (Creator，續航引擎)
 *   企業登入 → business.shell.fans/auth/login (Business，商業主控台)
 *
 * 原本全站 nav 的登入入口一律指向 app.shell.fans，連結構 2 已有的
 * 「口碑行銷登入」也指到 app，企業用戶沒有入口。
 *
 * 只在「未登入」(無 sf_user cookie)時作用；已登入時交由上方的續航登入
 * 狀態區塊接管，兩者互斥，所以它看到的仍是原始 HTML。
 *
 * 三種 nav 結構(見上方 apply() 的註解)分別處理，另含各自的行動版選單。
 * 文案不走頁面的 data-i18n 字典 —— 只有 4 頁有 i18n 引擎，其餘 15 頁
 * 是純中文頁；改為自帶中英文並監聽 'shellfans-locale-changed'，在有
 * i18n 的頁面跟著切換，沒有的頁面固定中文。
 */
(function () {
  'use strict';

  var CREATOR_LOGIN = 'https://app.shell.fans/auth/login';
  var BUSINESS_LOGIN = 'https://business.shell.fans/auth/login';
  var T = {
    'zh-TW': { creator: '網紅登入', business: '企業登入', login: '登入' },
    en: { creator: 'Creator Login', business: 'Business Login', login: 'Log in' }
  };

  function getCookie(n) {
    var m = document.cookie.match('(?:^|; )' + n + '=([^;]*)');
    return m ? decodeURIComponent(m[1]) : '';
  }

  // 只有具備 i18n 引擎的頁面才跟隨語系；其餘頁面整頁都是中文，
  // 單獨把登入鈕切成英文反而不一致。
  function texts() {
    if (!document.querySelector('[data-i18n]')) return T['zh-TW'];
    var v = '';
    try { v = localStorage.getItem('shellfans_locale') || ''; } catch (e) { v = ''; }
    return v === 'en' ? T.en : T['zh-TW'];
  }

  var DD_LINK_STYLE = 'padding:10px 18px;color:#292929;font-weight:500;';

  // 結構 1：index / aeo-geo 的 #navLogin .nav-login-list
  // 填入項目後，HTML 內既有的 toggle 判斷(list.children.length > 0)會自動
  // 從「直接跳轉」切換成「展開下拉」，因此不需要改那兩頁的 inline script。
  function struct1(t) {
    var list = document.querySelector('#navLogin .nav-login-list');
    if (!list) return;
    list.innerHTML =
      '<a href="' + CREATOR_LOGIN + '" role="menuitem" data-sf-guest-login="creator">' + t.creator + '</a>' +
      '<a href="' + BUSINESS_LOGIN + '" role="menuitem" data-sf-guest-login="business">' + t.business + '</a>';
  }

  // 結構 1 的行動版選單：單一「登入」→ 拆成兩條
  function struct1Mobile(t) {
    var mm = document.querySelector('.mobile-menu');
    if (!mm) return;
    var done = mm.querySelectorAll('a[data-sf-guest-login]');
    if (done.length === 2) {
      done[0].textContent = t.creator;
      done[1].textContent = t.business;
      return;
    }
    var orig = mm.querySelector('a[href*="/auth/login"]');
    if (!orig) return;
    var creator = document.createElement('a');
    creator.setAttribute('href', CREATOR_LOGIN);
    creator.setAttribute('data-sf-guest-login', 'creator');
    creator.textContent = t.creator;
    var business = document.createElement('a');
    business.setAttribute('href', BUSINESS_LOGIN);
    business.setAttribute('data-sf-guest-login', 'business');
    business.textContent = t.business;
    orig.parentNode.replaceChild(business, orig);
    business.parentNode.insertBefore(creator, business);
  }

  // 結構 2：14 頁 Webflow dropdown .login-dd-list
  // 既有兩項「續航引擎 / 口碑行銷」都指向 app.shell.fans，改為身分別 + 正確目的地。
  function struct2(t) {
    var lists = document.querySelectorAll('.login-dd-list');
    for (var i = 0; i < lists.length; i++) {
      lists[i].innerHTML =
        '<a href="' + CREATOR_LOGIN + '" class="w-dropdown-link" style="' + DD_LINK_STYLE +
        '" data-sf-guest-login="creator">' + t.creator + '</a>' +
        '<a href="' + BUSINESS_LOGIN + '" class="w-dropdown-link" style="' + DD_LINK_STYLE +
        '" data-sf-guest-login="business">' + t.business + '</a>';
    }
  }

  // 結構 2 的行動版抽屜：兩顆按鈕文案是「續航引擎登入 / 口碑行銷登入」，
  // 但 href 兩條都是 app.shell.fans —— 企業那條修正為 business.shell.fans。
  function struct2Mobile(t) {
    var btns = document.querySelectorAll('.nav-button-wrapper.hide-desktop a[href*="/auth/login"]');
    if (btns.length < 2) return;
    setMobileBtn(btns[0], CREATOR_LOGIN, t.creator, 'creator');
    setMobileBtn(btns[1], BUSINESS_LOGIN, t.business, 'business');
  }

  function setMobileBtn(a, href, label, kind) {
    a.setAttribute('href', href);
    a.setAttribute('data-sf-guest-login', kind);
    a.removeAttribute('target');
    var txt = a.querySelector('.button-text');
    if (txt) txt.textContent = label; else a.textContent = label;
  }

  // 結構 3：co-founder / social-media-backup / what-is-shellfans 的
  // .nav-actions 內是兩顆扁平按鈕(登入 / 開始使用)，沒有下拉容器 —— 就地把
  // 「登入」換成一個自帶樣式的下拉。index / aeo-geo 也有 .nav-actions，
  // 但裡面的登入是 button.nav-login-toggle 而非 a.btn-secondary，不會誤傷。
  function struct3(t) {
    var acts = document.querySelectorAll('.nav-actions');
    for (var i = 0; i < acts.length; i++) {
      var built = acts[i].querySelector('[data-sf-guest-dd]');
      if (built) {
        var links = built.querySelectorAll('a[data-sf-guest-login]');
        if (links.length === 2) {
          links[0].textContent = t.creator;
          links[1].textContent = t.business;
        }
        var lbl = built.querySelector('.sf-guest-dd-label');
        if (lbl) lbl.textContent = t.login;
        continue;
      }
      var btn = acts[i].querySelector('a.btn-secondary');
      if (!btn || !/登入|log ?in/i.test(btn.textContent)) continue;

      var wrap = document.createElement('div');
      wrap.className = 'sf-guest-dd';
      wrap.setAttribute('data-sf-guest-dd', '');
      wrap.innerHTML =
        '<button type="button" class="btn-secondary sf-guest-dd-toggle" aria-haspopup="true" aria-expanded="false">' +
        '<span class="sf-guest-dd-label">' + t.login + '</span><span class="sf-guest-dd-caret">▾</span></button>' +
        '<div class="sf-guest-dd-list" role="menu">' +
        '<a href="' + CREATOR_LOGIN + '" role="menuitem" data-sf-guest-login="creator">' + t.creator + '</a>' +
        '<a href="' + BUSINESS_LOGIN + '" role="menuitem" data-sf-guest-login="business">' + t.business + '</a>' +
        '</div>';
      btn.parentNode.replaceChild(wrap, btn);

      bindDropdown(wrap);
    }
  }

  function bindDropdown(wrap) {
    var toggle = wrap.querySelector('.sf-guest-dd-toggle');
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = wrap.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function (e) {
      if (wrap.contains(e.target)) return;
      wrap.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  }

  // 結構 3 專用樣式(其餘結構沿用頁面既有的下拉樣式)
  function injectStyle() {
    if (document.getElementById('sf-guest-dd-style')) return;
    var s = document.createElement('style');
    s.id = 'sf-guest-dd-style';
    s.textContent =
      '.sf-guest-dd{position:relative;display:inline-block}' +
      '.sf-guest-dd-toggle{display:inline-flex;align-items:center;gap:6px;font-family:inherit}' +
      '.sf-guest-dd-caret{font-size:0.7rem;line-height:1}' +
      '.sf-guest-dd-list{display:none;position:absolute;top:100%;right:0;min-width:180px;' +
      'background:#fff;border-radius:10px;box-shadow:0 18px 42px -18px rgba(20,108,181,0.25);' +
      'padding:8px 0;margin-top:6px;border:1px solid rgba(0,0,0,0.08);z-index:1000}' +
      '.sf-guest-dd.open .sf-guest-dd-list{display:block}' +
      '.sf-guest-dd-list a{display:block;padding:10px 18px;font-size:0.9rem;color:#292929;font-weight:500;white-space:nowrap}' +
      '.sf-guest-dd-list a:hover{background:#f5f7fa}';
    document.head.appendChild(s);
  }

  function apply() {
    if (getCookie('sf_user')) return; // 已登入 → 由續航登入狀態區塊接管
    var t = texts();
    injectStyle();
    struct1(t);
    struct1Mobile(t);
    struct2(t);
    struct2Mobile(t);
    struct3(t);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply);
  else apply();
  window.addEventListener('shellfans-locale-changed', apply);
})();
