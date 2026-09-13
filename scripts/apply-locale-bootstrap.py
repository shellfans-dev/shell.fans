#!/usr/bin/env python3
"""
Make the inline i18n engine (7 pages) initialise from the SERVER-resolved locale.

Root cause of the "Chinese first, then English" flash (2026-09-13): the static HTML is
always zh-TW, the preference lived only in localStorage (which the server cannot read),
and the engine swapped texts after DOMContentLoaded.

New contract (see deploy/nginx/shell.fans.conf and scripts/build-locale-pages.py):
  request + cookie shellfans_locale=en  →  nginx serves <page>.en.html  →  <html lang="en">
  the engine starts from <html lang> (= what the server rendered), so applyTranslations()
  is a no-op on a correctly served page. The preference is persisted in a same-name cookie
  (Path=/, 1 year, SameSite=Lax, Secure on https); localStorage is kept only as a
  backwards-compatible cache. Legacy visitors who only have localStorage=en get a one-time
  client-side switch that also writes the cookie, after which the server renders correctly.

Idempotent: a page carrying the "sf-locale-bootstrap v2" marker is left untouched.
Run this BEFORE scripts/build-locale-pages.py so the English variants inherit the patch.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARK = 'sf-locale-bootstrap v2'
ENGINE_MARK = 'window.__setLocale = function'

OLD_BOOTSTRAP = (
    "  var currentLocale = 'zh-TW';\n"
    "  try { currentLocale = localStorage.getItem(STORAGE_KEY) || 'zh-TW'; } catch (_) {}\n"
    "  if (currentLocale !== 'zh-TW' && currentLocale !== 'en') currentLocale = 'zh-TW';\n"
)

NEW_BOOTSTRAP = (
    "  // --- sf-locale-bootstrap v2 ---\n"
    "  // 初始語系以伺服器已決定的 HTML 為準：nginx 依 cookie shellfans_locale 回中文版或 .en 版，\n"
    "  // 結果反映在 <html lang>。偏好由同名 cookie 持久化（伺服器讀得到）；localStorage 只是相容用的\n"
    "  // 快取，不再決定首次渲染——伺服器在回應前讀不到它。舊使用者只有 localStorage 偏好時，\n"
    "  // 這一次在客戶端切換並寫入 cookie，之後首屏就由伺服器直接給對。\n"
    "  var COOKIE_KEY = 'shellfans_locale';\n"
    "  function readLocaleCookie() {\n"
    "    var m = document.cookie.match(/(?:^|;\\s*)shellfans_locale=(en|zh-TW)(?:;|$)/);\n"
    "    return m ? m[1] : '';\n"
    "  }\n"
    "  function writeLocaleCookie(l) {\n"
    "    try {\n"
    "      document.cookie = COOKIE_KEY + '=' + l + '; Path=/; Max-Age=31536000; SameSite=Lax' +\n"
    "        (location.protocol === 'https:' ? '; Secure' : '');\n"
    "    } catch (_) {}\n"
    "  }\n"
    "  var servedLocale = document.documentElement.lang === 'en' ? 'en' : 'zh-TW';\n"
    "  var cookieLocale = readLocaleCookie();\n"
    "  var storedLocale = '';\n"
    "  try { storedLocale = localStorage.getItem(STORAGE_KEY) || ''; } catch (_) {}\n"
    "  if (storedLocale !== 'zh-TW' && storedLocale !== 'en') storedLocale = '';\n"
    "  var preferredLocale = cookieLocale || storedLocale;\n"
    "  var currentLocale = servedLocale;\n"
    "  // 伺服器已依 cookie 給對語系時這裡不會改變任何東西；只有偏好尚未進 cookie（舊使用者）\n"
    "  // 或伺服器端尚未部署時，才退回客戶端切換。\n"
    "  if (preferredLocale && preferredLocale !== servedLocale) currentLocale = preferredLocale;\n"
    "  if (!cookieLocale && storedLocale) writeLocaleCookie(storedLocale);\n"
    "  try { if (storedLocale !== currentLocale) localStorage.setItem(STORAGE_KEY, currentLocale); } catch (_) {}\n"
    "  window.__sfWriteLocaleCookie = writeLocaleCookie;\n"
)

OLD_SET = "    try { localStorage.setItem(STORAGE_KEY, locale); } catch (_) {}\n"
NEW_SET = (
    "    try { localStorage.setItem(STORAGE_KEY, locale); } catch (_) {}\n"
    "    writeLocaleCookie(locale);\n"
)

OLD_LANG = "document.documentElement.lang = currentLocale === 'en' ? 'en' : 'zh-TW';"
NEW_LANG = "document.documentElement.lang = currentLocale === 'en' ? 'en' : 'zh-Hant';"


def engine_pages():
    for p in sorted(ROOT.rglob('*.html')):
        parts = p.relative_to(ROOT).parts
        if any(x in ('docs', 'node_modules', '.git', 'partials', 'deploy') for x in parts):
            continue
        if p.name.endswith('.en.html'):
            continue
        if ENGINE_MARK in p.read_text(encoding='utf-8'):
            yield p


def process(p: Path) -> str:
    s = p.read_text(encoding='utf-8')
    if MARK in s:
        return 'ok (already v2)'
    if s.count(OLD_BOOTSTRAP) != 1:
        return f'SKIP: bootstrap block not found exactly once ({s.count(OLD_BOOTSTRAP)})'
    if s.count(OLD_SET) != 1:
        return f'SKIP: __setLocale localStorage line not found exactly once ({s.count(OLD_SET)})'
    s = s.replace(OLD_BOOTSTRAP, NEW_BOOTSTRAP, 1)
    s = s.replace(OLD_SET, NEW_SET, 1)
    # the static markup declares zh-Hant; keep the runtime value identical to the served value
    s = s.replace(OLD_LANG, NEW_LANG)
    p.write_text(s, encoding='utf-8')
    return 'patched'


def main() -> int:
    bad = 0
    for p in engine_pages():
        r = process(p)
        print(f'{p.relative_to(ROOT)}: {r}')
        if r.startswith('SKIP'):
            bad += 1
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
