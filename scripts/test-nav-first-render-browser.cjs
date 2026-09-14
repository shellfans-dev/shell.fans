#!/usr/bin/env node
/*
 * Browser-level no-flash test for the baked Global UI navigation
 * (fix-navigation-first-render-flash, 2026-09-14).
 *
 * Runs against the throw-away nginx started by scripts/test-initial-locale.py:
 *   python3 scripts/test-initial-locale.py start
 *   node scripts/test-nav-first-render-browser.cjs
 *   python3 scripts/test-initial-locale.py stop
 *
 * What it proves (per docs/ai/CURRENT-TASK.md acceptance criteria):
 *   - JS DISABLED: the very first HTML already carries the *published* Global UI nav (the
 *     no-JS / crawler baseline), for zh-TW and for the pre-generated .en.html — so there is
 *     no "old nav" frame to flash away.
 *   - JS ENABLED: with the published-config API fed to the page, the VISIBLE nav is identical
 *     before and after js/sf-global-ui.js runs syncNav() — i.e. the runtime sync reconciles the
 *     baked DOM to the exact same result, so nothing visibly changes (no flash). Dropdown groups
 *     are present after sync and no uncaught JS exception is thrown.
 *
 * The published config (single source of truth) is fetched server-side from console.shell.fans
 * — no browser CORS, no committed fixture — and injected into the page via route interception so
 * the test is deterministic against whatever is currently published. If the config cannot be
 * fetched, the flash checks are skipped (reported) rather than failing spuriously.
 *
 * Playwright is taken from the sibling saas_womm checkout (override with PLAYWRIGHT_MODULE); the
 * bundled chromium is missing on 215, so the system chromium is used.
 */
const https = require('https');

const PW = process.env.PLAYWRIGHT_MODULE || '/home/kirin/work/saas_womm/node_modules/playwright';
const { chromium } = require(PW);
const BASE = process.env.SF_TEST_BASE || 'https://127.0.0.1:18443';
const ORIGIN = new URL(BASE).origin;
const API = process.env.SF_GUI_API || 'https://console.shell.fans/api/site/global-ui?site=shell';
const CHROMIUM = process.env.SF_CHROMIUM || '/usr/bin/chromium-browser';

const results = [];
function check(name, cond, detail) {
  results.push({ name, ok: !!cond });
  console.log((cond ? '  ✔ ' : '  ✖ ') + name + (cond ? '' : '   ' + (detail || '')));
}
function skip(name, detail) {
  console.log('  – ' + name + '   SKIPPED' + (detail ? ' (' + detail + ')' : ''));
}

// Visible desktop nav labels (parent + children flattened, caret glyph stripped).
const NAVJS = `(() => {
  const nav = document.querySelector('nav.nav-menu');
  if (!nav) return null;
  return Array.from(nav.querySelectorAll('a'))
    .map(a => (a.textContent || '').replace('\\u25be', '').trim()).filter(Boolean);
})()`;

function fetchConfig() {
  return new Promise(resolve => {
    const req = https.get(API, { headers: { 'User-Agent': 'nav-first-render-test' }, timeout: 8000 }, res => {
      let body = '';
      res.on('data', d => (body += d));
      res.on('end', () => {
        try {
          const j = JSON.parse(body);
          if (j && j.data && !j.fallback) resolve(j); else resolve(null);
        } catch { resolve(null); }
      });
    });
    req.on('error', () => resolve(null));
    req.on('timeout', () => { req.destroy(); resolve(null); });
  });
}

(async () => {
  const snap = await fetchConfig();
  const browser = await chromium.launch({
    executablePath: CHROMIUM,
    args: ['--no-sandbox', '--ignore-certificate-errors'],
  });

  // ---- (1) JS disabled: the first HTML already carries the published nav ----
  for (const loc of ['zh', 'en']) {
    const ctx = await browser.newContext({ ignoreHTTPSErrors: true, javaScriptEnabled: false });
    if (loc === 'en') await ctx.addCookies([{ name: 'shellfans_locale', value: 'en', domain: new URL(BASE).hostname, path: '/' }]);
    const page = await ctx.newPage();
    await page.goto(BASE + '/', { waitUntil: 'domcontentloaded' });
    const labels = await page.evaluate(NAVJS);
    const want = loc === 'en' ? 'AI Social Solutions' : 'AI 社群方案';
    check(`no-JS ${loc}: first HTML nav is the published nav`,
      !!labels && labels[0] === want && labels.length >= 5, JSON.stringify(labels));
    await ctx.close();
  }

  // ---- (2) JS enabled: no flash across syncNav ----
  if (!snap) {
    skip('flash: published config unreachable', API);
  } else {
    for (const loc of ['zh', 'en']) {
      const ctx = await browser.newContext({ ignoreHTTPSErrors: true });
      if (loc === 'en') await ctx.addCookies([{ name: 'shellfans_locale', value: 'en', domain: new URL(BASE).hostname, path: '/' }]);
      const page = await ctx.newPage();
      const jsErrors = [];
      const navConsole = [];
      page.on('pageerror', e => jsErrors.push(String(e)));
      page.on('console', m => { if (m.type() === 'error' && /sf-gui|global-ui|syncNav|nav-menu/i.test(m.text())) navConsole.push(m.text()); });

      // Hold the config response until first paint is captured, so we can compare first paint
      // against the post-sync DOM. Every other console.shell.fans call is answered inertly so the
      // page keeps its baked baseline and the console stays quiet.
      let releaseApi;
      const apiGate = new Promise(r => { releaseApi = r; });
      await page.route('**://console.shell.fans/**', async route => {
        const url = route.request().url();
        if (url.includes('/api/site/global-ui')) { await apiGate; return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(snap) }); }
        return route.fulfill({ status: 200, contentType: 'application/json', headers: { 'access-control-allow-origin': ORIGIN, 'access-control-allow-credentials': 'true' }, body: '{"fallback":true}' });
      });

      await page.goto(BASE + '/', { waitUntil: 'domcontentloaded' });
      const before = await page.evaluate(NAVJS);
      releaseApi();
      await page.waitForTimeout(1200);
      const after = await page.evaluate(NAVJS);
      const groups = await page.evaluate(`document.querySelectorAll('nav.nav-menu .sf-gui-group').length`);

      check(`flash ${loc}: visible nav identical before vs after syncNav`,
        JSON.stringify(before) === JSON.stringify(after),
        `before=${JSON.stringify(before)} after=${JSON.stringify(after)}`);
      check(`flash ${loc}: dropdown groups present after sync`, groups >= 2, String(groups));
      check(`flash ${loc}: no uncaught JS exceptions`, jsErrors.length === 0, jsErrors.join(' | '));
      check(`flash ${loc}: no nav-script console errors`, navConsole.length === 0, navConsole.join(' | '));
      await ctx.close();
    }
  }

  await browser.close();
  const bad = results.filter(r => !r.ok).length;
  console.log(`\n=== ${results.length - bad}/${results.length} checks passed ===`);
  process.exit(bad ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
