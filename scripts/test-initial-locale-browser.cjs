#!/usr/bin/env node
/*
 * Browser-level test for the initial-locale rendering fix (2026-09-13).
 *
 * Runs against the throw-away nginx started by scripts/test-initial-locale.py:
 *   python3 scripts/test-initial-locale.py start
 *   node scripts/test-initial-locale-browser.cjs
 *   python3 scripts/test-initial-locale.py stop
 *
 * What it proves (per acceptance criteria of docs/ai/CURRENT-TASK.md):
 *   - the FIRST frame is already in the right language: verified with JavaScript disabled
 *     (what you see is exactly the server HTML), with Slow-3G throttling while polling the
 *     DOM from the moment it exists, and by counting text mutations on [data-i18n] nodes
 *     after the page was served in the right language (must be 0 → applyTranslations is a no-op)
 *   - header / logo / navbar / mobile menu / hero / footer / <html lang> / metadata
 *   - language switch both ways is immediate, writes the cookie, survives reload,
 *     back/forward and a new tab; invalid cookie falls back; legacy localStorage-only
 *     visitors are migrated once and then served correctly
 *   - desktop 1440 / tablet 768 / mobile 390, no console errors
 *
 * Playwright is taken from the sibling saas_womm checkout (no new dependency in this repo);
 * override with PLAYWRIGHT_MODULE. The bundled chromium is missing on 215, so the system
 * chromium is used as a fallback.
 */
const path = require('path');
const fs = require('fs');

const PW = process.env.PLAYWRIGHT_MODULE || '/home/kirin/work/saas_womm/node_modules/playwright';
const { chromium } = require(PW);
const BASE = process.env.SF_TEST_BASE || 'https://127.0.0.1:18443';
const HOST = new URL(BASE).hostname;
const OUT = process.env.SF_TEST_SHOTS || '/tmp/sf-locale-test/shots';
fs.mkdirSync(OUT, { recursive: true });

const EN_LOGO = 'https://shell.fans/images/nav_logo_en.png';
const ZH_LOGO = 'https://shell.fans/images/nav_logo.svg';

const results = [];
function check(name, cond, detail) {
  results.push({ name, ok: !!cond });
  console.log((cond ? '  ✔ ' : '  ✖ ') + name + (cond ? '' : '   ' + (detail || '')));
}

// Counts [data-i18n] text mutations that actually CHANGED the text after the node was
// parsed. On a page served in the right language this must stay 0.
const OBSERVER = `(() => {
  window.__sfChangedI18n = [];
  const seen = new WeakMap();
  function snapshot(el) { seen.set(el, el.textContent); }
  const obs = new MutationObserver((records) => {
    for (const r of records) {
      const el = r.target.nodeType === 3 ? r.target.parentElement : r.target;
      const host = el && el.closest ? el.closest('[data-i18n]') : null;
      if (!host || host.hasAttribute('data-i18n-attr')) continue;
      const before = seen.get(host);
      const after = host.textContent;
      if (before !== undefined && before !== after) window.__sfChangedI18n.push({ key: host.getAttribute('data-i18n'), before, after });
      seen.set(host, after);
    }
  });
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-i18n]').forEach(snapshot);
  }, { once: true });
  obs.observe(document, { subtree: true, childList: true, characterData: true });
  // snapshot as early as nodes appear (before DOMContentLoaded) so pre-DCL swaps are caught too
  const early = new MutationObserver(() => { document.querySelectorAll('[data-i18n]').forEach((el) => { if (!seen.has(el)) snapshot(el); }); });
  early.observe(document, { subtree: true, childList: true });
})();`;

async function ctxFor(browser, opts = {}) {
  const ctx = await browser.newContext({
    viewport: { width: opts.width || 1440, height: 900 },
    ignoreHTTPSErrors: true,
    javaScriptEnabled: opts.js !== false,
    locale: 'zh-TW',
  });
  if (opts.cookie) {
    await ctx.addCookies([{ name: 'shellfans_locale', value: opts.cookie, domain: HOST, path: '/', secure: BASE.startsWith('https'), sameSite: 'Lax' }]);
  }
  if (opts.localStorage) {
    await ctx.addInitScript((v) => { try { localStorage.setItem('shellfans_locale', v); } catch (e) {} }, opts.localStorage);
  }
  if (opts.js !== false) await ctx.addInitScript(OBSERVER);
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error' && !/Failed to load resource|ERR_|blocked by CORS policy/.test(m.text())) errors.push('console: ' + m.text()); });
  return { ctx, page, errors };
}

const state = (page) => page.evaluate(() => ({
  lang: document.documentElement.lang,
  title: document.title,
  h1: (document.querySelector('.hero h2, h1') || {}).textContent?.trim() || '',
  nav: [...document.querySelectorAll('header.nav nav.nav-menu > a')].filter((a) => getComputedStyle(a).display !== 'none').map((a) => a.textContent.trim()),
  mobile: [...document.querySelectorAll('#mobileMenu > a')].map((a) => a.textContent.trim()),
  logo: document.querySelector('.nav-brand img')?.getAttribute('src'),
  footerLogo: document.querySelector('#sf-footer-root .sf-footer-brand img')?.getAttribute('src'),
  footerLegal: [...document.querySelectorAll('#sf-footer-root .sf-footer-legal a')].map((a) => a.textContent.trim()),
  cta: document.querySelector('.nav-actions a.nav-cta')?.textContent.trim(),
  switcher: document.querySelector('#langSwitcherLabel')?.textContent.trim(),
  desc: document.querySelector('meta[name="description"]')?.getAttribute('content') || '',
  changed: window.__sfChangedI18n || null,
  cookie: document.cookie,
}));

const isEnglish = (s) => s.lang === 'en' && s.nav[0] === 'AEO/GEO Hosting' && s.logo === EN_LOGO && s.footerLogo === EN_LOGO && s.footerLegal[0] === 'Privacy Policy' && /^ShellFans \| AEO/.test(s.title) && !/[一-鿿]/.test(s.desc);
const isChinese = (s) => (s.lang === 'zh-Hant' || s.lang === 'zh-TW') && s.nav[0] === 'AEO/GEO 代管' && s.logo === ZH_LOGO && s.footerLogo === ZH_LOGO && s.footerLegal[0] === '隱私權政策' && /^ShellFans｜/.test(s.title);

(async () => {
  let browser;
  try { browser = await chromium.launch({ headless: true }); }
  catch (e) { browser = await chromium.launch({ headless: true, executablePath: '/usr/bin/chromium-browser', args: ['--no-sandbox'] }); }

  // ---------- A/B: first frame with JavaScript DISABLED (server HTML only) ----------
  for (const [label, cookie, expect] of [['zh (no cookie)', null, 'zh'], ['zh (cookie=zh-TW)', 'zh-TW', 'zh'], ['en (cookie=en)', 'en', 'en'], ['invalid cookie=xx', 'xx', 'zh']]) {
    console.log(`\n[JS disabled] ${label}`);
    const { ctx, page } = await ctxFor(browser, { js: false, cookie });
    await page.goto(BASE + '/', { waitUntil: 'load' });
    const s = await page.evaluate(() => ({
      lang: document.documentElement.lang, title: document.title,
      nav: [...document.querySelectorAll('header.nav nav.nav-menu > a')].map((a) => a.textContent.trim()),
      mobile: [...document.querySelectorAll('#mobileMenu > a')].map((a) => a.textContent.trim()),
      logo: document.querySelector('.nav-brand img')?.getAttribute('src'),
      footerLogo: document.querySelector('#sf-footer-root .sf-footer-brand img')?.getAttribute('src'),
      footerLegal: [...document.querySelectorAll('#sf-footer-root .sf-footer-legal a')].map((a) => a.textContent.trim()),
      desc: document.querySelector('meta[name="description"]')?.getAttribute('content') || '',
      cta: document.querySelector('.nav-actions a.nav-cta')?.textContent.trim(),
      hero: document.querySelector('[data-i18n="hero.h2.line1"]')?.textContent.trim() || '',
    }));
    if (expect === 'en') {
      check('no-JS first frame is English (lang/nav/logo/footer/title/desc)', isEnglish(s), JSON.stringify(s));
      check('no-JS mobile menu English', s.mobile[0] === 'AEO/GEO Hosting' && s.mobile.includes('Get Started'), JSON.stringify(s.mobile));
      check('no-JS CTA English', s.cta === 'Get Started', s.cta);
      check('no-JS hero English', s.hero === 'Turn social into', s.hero);
    } else {
      check('no-JS first frame is Chinese', isChinese(s), JSON.stringify(s));
      check('no-JS mobile menu Chinese', s.mobile[0] === 'AEO/GEO 代管', JSON.stringify(s.mobile));
    }
    await page.screenshot({ path: path.join(OUT, `nojs-${label.replace(/[^a-z]+/gi, '-')}.png`) });
    await ctx.close();
  }

  // ---------- C/D: JS enabled, served locale must be final (0 changed data-i18n texts) ----------
  for (const [label, cookie, expect, width] of [['zh 1440', null, 'zh', 1440], ['en 1440', 'en', 'en', 1440], ['en 768', 'en', 'en', 768], ['en 390', 'en', 'en', 390], ['zh 390', null, 'zh', 390]]) {
    console.log(`\n[JS enabled] ${label}`);
    const { ctx, page, errors } = await ctxFor(browser, { cookie, width });
    await page.goto(BASE + '/', { waitUntil: 'load' });
    await page.waitForTimeout(1500);
    const s = await state(page);
    check(`${label}: final state ${expect}`, expect === 'en' ? isEnglish(s) : isChinese(s), JSON.stringify({ lang: s.lang, nav: s.nav, logo: s.logo, footerLogo: s.footerLogo, title: s.title }));
    check(`${label}: 0 data-i18n texts changed after parse (no flash)`, Array.isArray(s.changed) && s.changed.length === 0, JSON.stringify((s.changed || []).slice(0, 3)));
    check(`${label}: switcher label ${expect === 'en' ? 'English' : '繁體中文'}`, s.switcher === (expect === 'en' ? 'English' : '繁體中文'), s.switcher);
    if (width <= 991) {
      await page.click('#navHamburger'); await page.waitForTimeout(300);
      const mob = await page.$$eval('#mobileMenu > a', (as) => as.filter((a) => getComputedStyle(a).display !== 'none').map((a) => a.textContent.trim()));
      check(`${label}: mobile menu ${expect}`, mob[0] === (expect === 'en' ? 'AEO/GEO Hosting' : 'AEO/GEO 代管'), JSON.stringify(mob));
      check(`${label}: no horizontal overflow`, await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1));
      await page.screenshot({ path: path.join(OUT, `js-${label.replace(/\s+/g, '-')}-menu.png`) });
    } else {
      await page.screenshot({ path: path.join(OUT, `js-${label.replace(/\s+/g, '-')}.png`) });
    }
    check(`${label}: no page errors`, errors.length === 0, errors.join(' || '));
    await ctx.close();
  }

  // ---------- E/F: language switch both ways, cookie, reload ----------
  console.log('\n[switch zh → en → reload → en → zh → reload]');
  {
    const { ctx, page, errors } = await ctxFor(browser, {});
    await page.goto(BASE + '/', { waitUntil: 'load' });
    await page.click('#langSwitcherToggle'); await page.click('#langSwitcherList [data-locale="en"]'); await page.waitForTimeout(300);
    let s = await state(page);
    check('switch → English immediately (no reload)', s.lang === 'en' && s.nav[0] === 'AEO/GEO Hosting' && s.logo === EN_LOGO && s.footerLogo === EN_LOGO && s.footerLegal[0] === 'Privacy Policy', JSON.stringify({ lang: s.lang, nav: s.nav[0], logo: s.logo, footerLogo: s.footerLogo }));
    check('switch → cookie shellfans_locale=en written', /shellfans_locale=en/.test(s.cookie), s.cookie);
    const cookies = await ctx.cookies(BASE);
    const c = cookies.find((x) => x.name === 'shellfans_locale');
    check('cookie attributes: Path=/, Secure, SameSite=Lax, ~1 year', c && c.path === '/' && c.secure === true && c.sameSite === 'Lax' && c.expires > Date.now() / 1000 + 360 * 86400, JSON.stringify(c));
    await page.reload({ waitUntil: 'load' }); await page.waitForTimeout(1200);
    s = await state(page);
    check('reload → served English, 0 changed texts', isEnglish(s) && s.changed.length === 0, JSON.stringify({ lang: s.lang, changed: s.changed.slice(0, 2) }));
    await page.click('#langSwitcherToggle'); await page.click('#langSwitcherList [data-locale="zh-TW"]'); await page.waitForTimeout(300);
    s = await state(page);
    check('switch back → Chinese immediately', s.nav[0] === 'AEO/GEO 代管' && s.logo === ZH_LOGO && s.footerLogo === ZH_LOGO && s.lang === 'zh-Hant', JSON.stringify({ lang: s.lang, nav: s.nav[0], logo: s.logo }));
    check('switch back → cookie zh-TW', /shellfans_locale=zh-TW/.test(s.cookie), s.cookie);
    await page.reload({ waitUntil: 'load' }); await page.waitForTimeout(1200);
    s = await state(page);
    check('reload → served Chinese, 0 changed texts', isChinese(s) && s.changed.length === 0, JSON.stringify({ lang: s.lang, changed: s.changed.slice(0, 2) }));
    check('no page errors (switch)', errors.length === 0, errors.join(' || '));
    await ctx.close();
  }

  // ---------- G: back / forward / new tab ----------
  console.log('\n[back / forward / new tab]');
  {
    const { ctx, page, errors } = await ctxFor(browser, { cookie: 'en' });
    await page.goto(BASE + '/', { waitUntil: 'load' });
    await page.goto(BASE + '/aeo-geo', { waitUntil: 'load' }); await page.waitForTimeout(800);
    let s = await state(page);
    check('/aeo-geo served English', s.lang === 'en' && s.nav[0] === 'AEO/GEO Hosting' && s.changed.length === 0, JSON.stringify({ lang: s.lang, nav: s.nav[0], changed: s.changed.slice(0, 3) }));
    await page.goBack({ waitUntil: 'load' }); await page.waitForTimeout(800);
    s = await state(page);
    check('back → still English', s.lang === 'en' && s.nav[0] === 'AEO/GEO Hosting', JSON.stringify({ lang: s.lang, nav: s.nav[0] }));
    await page.goForward({ waitUntil: 'load' }); await page.waitForTimeout(800);
    s = await state(page);
    check('forward → still English', s.lang === 'en' && s.nav[0] === 'AEO/GEO Hosting', JSON.stringify({ lang: s.lang, nav: s.nav[0] }));
    const tab = await ctx.newPage(); await tab.addInitScript(OBSERVER);
    await tab.goto(BASE + '/what-is-shellfans', { waitUntil: 'load' }); await tab.waitForTimeout(800);
    const t = await tab.evaluate(() => ({ lang: document.documentElement.lang, logo: document.querySelector('.nav-brand img')?.getAttribute('src'), changed: (window.__sfChangedI18n || []).length }));
    check('new tab /what-is-shellfans → English, 0 changed', t.lang === 'en' && t.logo === EN_LOGO && t.changed === 0, JSON.stringify(t));
    check('no page errors (history)', errors.length === 0, errors.join(' || '));
    await ctx.close();
  }

  // ---------- H: legacy visitor (localStorage=en, no cookie) → one-time migration ----------
  console.log('\n[legacy localStorage=en, no cookie]');
  {
    const { ctx, page, errors } = await ctxFor(browser, { localStorage: 'en' });
    await page.goto(BASE + '/', { waitUntil: 'load' }); await page.waitForTimeout(800);
    let s = await state(page);
    check('legacy: page ends up English (client-side, once)', s.lang === 'en' && s.nav[0] === 'AEO/GEO Hosting' && s.logo === EN_LOGO, JSON.stringify({ lang: s.lang, nav: s.nav[0] }));
    check('legacy: cookie migrated to en', /shellfans_locale=en/.test(s.cookie), s.cookie);
    await page.reload({ waitUntil: 'load' }); await page.waitForTimeout(1000);
    s = await state(page);
    check('legacy: second load served English with 0 changed texts', isEnglish(s) && s.changed.length === 0, JSON.stringify({ lang: s.lang, changed: s.changed.slice(0, 2) }));
    check('no page errors (legacy)', errors.length === 0, errors.join(' || '));
    await ctx.close();
  }

  // ---------- I: stale localStorage but cookie wins ----------
  console.log('\n[cookie=en, stale localStorage=zh-TW]');
  {
    const { ctx, page } = await ctxFor(browser, { cookie: 'en', localStorage: 'zh-TW' });
    await page.goto(BASE + '/', { waitUntil: 'load' }); await page.waitForTimeout(800);
    const s = await state(page);
    check('cookie wins over stale localStorage; no flash', isEnglish(s) && s.changed.length === 0, JSON.stringify({ lang: s.lang, changed: s.changed.slice(0, 5) }));
    check('localStorage resynced to en', (await page.evaluate(() => localStorage.getItem('shellfans_locale'))) === 'en');
    await ctx.close();
  }

  // ---------- J: Slow 3G — poll the DOM from the first moment it exists ----------
  for (const [label, cookie, expect] of [['en', 'en', 'en'], ['zh', null, 'zh']]) {
    console.log(`\n[Slow 3G, JS enabled] ${label}`);
    const { ctx, page, errors } = await ctxFor(browser, { cookie });
    const cdp = await ctx.newCDPSession(page);
    await cdp.send('Network.enable');
    await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 400, downloadThroughput: 50 * 1024, uploadThroughput: 20 * 1024 });
    const samples = [];
    const nav = page.goto(BASE + '/', { waitUntil: 'load', timeout: 120000 });
    const t0 = Date.now();
    while (Date.now() - t0 < 60000) {
      try {
        const s = await page.evaluate(() => ({ lang: document.documentElement.lang, nav: document.querySelector('header.nav nav.nav-menu > a')?.textContent.trim() || '', ready: document.readyState }));
        if (s.nav) samples.push(s);
        if (s.ready === 'complete') break;
      } catch (e) { /* navigation in flight */ }
      await new Promise((r) => setTimeout(r, 40));
    }
    await nav.catch(() => {});
    const wrong = samples.filter((s) => expect === 'en' ? (s.nav !== 'AEO/GEO Hosting' || s.lang !== 'en') : (s.nav !== 'AEO/GEO 代管'));
    check(`slow 3G ${label}: every observed frame in the right language (${samples.length} samples)`, samples.length > 0 && wrong.length === 0, JSON.stringify(wrong.slice(0, 3)));
    const s = await state(page);
    check(`slow 3G ${label}: 0 changed data-i18n texts`, s.changed && s.changed.length === 0, JSON.stringify((s.changed || []).slice(0, 2)));
    check(`slow 3G ${label}: no page errors`, errors.length === 0, errors.join(' || '));
    await ctx.close();
  }

  await browser.close();
  const fails = results.filter((r) => !r.ok);
  console.log(`\n=== ${results.length - fails.length}/${results.length} browser checks passed ===`);
  fails.forEach((f) => console.log(' -', f.name));
  process.exit(fails.length ? 1 : 0);
})().catch((e) => { console.error('FATAL', e); process.exit(2); });
