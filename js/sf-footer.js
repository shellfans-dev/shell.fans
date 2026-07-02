/*!
 * shell.fans unified footer renderer.
 *
 * Renders the site footer into <div id="sf-footer-root"> from the live config
 * served by kol.fans (GET https://kol.fans/api/site/footer?site=shell, CORS),
 * falling back to the embedded SHELL_BASE defaults if the fetch fails. Edits
 * made in the kol.fans admin (UIUX Design → Footer 頁尾, site=shell.fans)
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
  var API = 'https://kol.fans/api/site/footer?site=shell';

  // Embedded defaults (mirror of saas_womm DEFAULT_FOOTER_SETTINGS.shell).
  var SHELL_BASE = {
    logo: { src: 'https://shell.fans/images/nav_logo.svg', alt: 'ShellFans AI' },
    description: {
      'zh-TW': '跨平台社群 AI 指揮中心。保存社群資產，看懂粉絲，同步經營與口碑成長。',
      en: 'Cross-platform Social AI Command. Preserve social assets, understand fans, grow engagement and reputation in sync.'
    },
    linkGroups: [
      { title: { 'zh-TW': '產品', en: 'Product' }, links: [
        { label: { 'zh-TW': '續航引擎', en: 'Engagement Engine' }, href: 'https://shell.fans/kol-engine' },
        { label: { 'zh-TW': '粉絲分析', en: 'Fans Analysis' }, href: 'https://shell.fans/fans-analysis' },
        { label: { 'zh-TW': '口碑行銷', en: 'Word-of-Mouth' }, href: 'https://kol.fans', external: true },
        { label: { 'zh-TW': '查看方案', en: 'Pricing' }, href: 'https://kol.fans/pricing', external: true }
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
      { text: { 'zh-TW': '日商唄粉智能科技有限公司', en: 'ShellFans AI Technology Co., Ltd.' } },
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
        'zh-TW': '© 2026 ShellFans AI. 日商唄粉智能科技有限公司. All rights reserved.',
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
    render(SHELL_BASE, getLocale());
    fetch(API, { credentials: 'omit' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) { if (j && j.data) { lastCfg = j.data; render(lastCfg, getLocale()); } })
      .catch(function () { /* keep embedded defaults */ });
    document.addEventListener('shellfans-locale-changed', function (e) {
      var nl = e && e.detail && e.detail.locale === 'en' ? 'en' : (e && e.detail && e.detail.locale ? 'zh-TW' : getLocale());
      render(lastCfg, nl);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

/*!
 * ShellFans 產品服務開關 — 依 kol.fans 後台設定隱藏 nav / footer 的產品入口。
 *
 * 讀取 GET https://kol.fans/api/site/product-flags（CORS）。當某產品開關為
 * false 時，實際從 DOM 移除對應的連結（桌機 nav、手機 nav、footer），而非
 * 只用 CSS 隱藏。讀取失敗一律維持顯示（fallback = 啟用），不影響其他 nav。
 *
 *   kolfans_wom_enabled            → 口碑行銷      (data-i18n="nav.wordOfMouth")
 *   shellfans_endurance_engine_...  → 續航引擎      (data-i18n="nav.engine")
 *   aeo_geo_managed_hosting_enabled → AEO/GEO 代管  (data-i18n="nav.aeoGeo")
 */
(function () {
  'use strict';
  var FLAGS_API = 'https://kol.fans/api/site/product-flags';

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
    fetch(FLAGS_API, { credentials: 'omit' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) {
        var d = j && j.data;
        if (!d) return;
        // 若三者皆啟用則不動作（常態）。
        if (d.kolfans_wom_enabled !== false &&
            d.shellfans_endurance_engine_enabled !== false &&
            d.aeo_geo_managed_hosting_enabled !== false) return;
        apply(d);
        // footer 由 sf-footer.js 非同步注入，稍後再掃兩次確保涵蓋。
        setTimeout(function () { apply(d); }, 400);
        setTimeout(function () { apply(d); }, 1200);
      })
      .catch(function () { /* 讀取失敗：維持顯示，不影響其他 nav */ });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();
