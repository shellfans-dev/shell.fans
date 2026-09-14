#!/usr/bin/env python3
"""
Integration test for the initial-locale rendering fix (2026-09-13).

Starts a throw-away nginx (as the current user, ports 18080/18443) whose `map` and
`location` blocks are EXTRACTED VERBATIM from deploy/nginx/shell.fans.conf, with the repo
working tree as document root, then checks with raw HTTP requests — no browser, no JS —
that the very first response already has the right language:

  * no cookie / cookie=zh-TW / invalid cookie  →  zh-TW HTML (lang="zh-Hant", zh title & nav)
  * cookie shellfans_locale=en                 →  English HTML (lang="en", en title/nav/logo/footer/meta)
  * pages without an English variant           →  unchanged Chinese page
  * /index.en.html and friends                 →  404 (no duplicate-content URLs)
  * assets, markdown negotiation, cache headers, ETag separation, If-None-Match across variants

Usage
  python3 scripts/test-initial-locale.py              # start nginx, run checks, stop
  python3 scripts/test-initial-locale.py start        # leave nginx running (for the browser test)
  python3 scripts/test-initial-locale.py stop
  python3 scripts/test-initial-locale.py --base https://127.0.0.1:18443   # checks only, against a running server

Requires: nginx binary, openssl (self-signed cert is generated on first start), python3 stdlib.
"""

from __future__ import annotations

import os
import re
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONF = ROOT / 'deploy' / 'nginx' / 'shell.fans.conf'
RUN = Path(os.environ.get('SF_TEST_RUN_DIR', '/tmp/sf-locale-test'))
HTTP_PORT = int(os.environ.get('SF_TEST_HTTP_PORT', '18080'))
HTTPS_PORT = int(os.environ.get('SF_TEST_HTTPS_PORT', '18443'))

ENGINE_PAGES = {
    '/': 'index',
    '/aeo-geo': 'aeo-geo',
    '/aeo-geo/methodology': 'aeo-geo/methodology',
    '/aeo-geo/taiwan-aeo-tools': 'aeo-geo/taiwan-aeo-tools',
    '/social-media-backup': 'social-media-backup',
    '/tools/aeo-geo-checker': 'tools/aeo-geo-checker',
    '/what-is-shellfans': 'what-is-shellfans',
}

results: list[tuple[str, bool, str]] = []


def check(name: str, cond: bool, detail: str = '') -> None:
    results.append((name, bool(cond), detail))
    print(('  ✔ ' if cond else '  ✖ ') + name + ('' if cond else f'   {detail}'))


# ---------------------------------------------------------------------------
# nginx harness
# ---------------------------------------------------------------------------

def extract_block(text: str, header: str, must_contain: str | None = None) -> str:
    """Return the full `header { ... }` block (brace-matched) from an nginx config.

    `location /` exists in the :80 redirect server too; `must_contain` selects the block
    that carries the directive we are testing (the HTTPS server's try_files)."""
    # anchor at line start so a mention inside a comment ("... through `location /` ...")
    # can never be mistaken for the directive itself
    pat = re.compile(r'(?m)^[ \t]*' + re.escape(header) + r'[ \t]*\{')
    pos = 0
    while True:
        m = pat.search(text, pos)
        if not m:
            raise SystemExit(f'block not found in {CONF}: {header} (containing {must_contain!r})')
        i = m.start()
        j = m.end() - 1
        depth = 0
        for k in range(j, len(text)):
            if text[k] == '{':
                depth += 1
            elif text[k] == '}':
                depth -= 1
                if depth == 0:
                    block = text[i:k + 1]
                    if must_contain is None or must_contain in block:
                        return block
                    pos = k + 1
                    break
        else:
            raise SystemExit(f'unbalanced block: {header}')


def write_test_conf() -> Path:
    src = CONF.read_text(encoding='utf-8')
    maps = ''.join(extract_block(src, h) + '\n\n' for h in (
        'map $http_accept $md_suffix', 'map $uri $md_base', 'map $http_accept $notfound_doc',
        'map $cookie_shellfans_locale $sf_lang'))
    locations = ''.join(extract_block(src, h, c) + '\n\n' for h, c in (
        ('location ~ \\.en(\\.html)?$', None), ('location ~ /\\.(?!well-known)', None),
        ('location ~ "^(/(?:aeo-geo(?:/(?:methodology|taiwan-aeo-tools))?|social-media-backup|what-is-shellfans|tools/aeo-geo-checker))\\.html$"', None),
        ('location = /aeo-geo', 'try_files'), ('location /', 'try_files')))
    # sanity: the directives this fix depends on must be present verbatim in the deploy conf
    for needle in ('$uri$sf_lang.html', '/aeo-geo$sf_lang.html', '"~^en$"  ".en"', 'return 301 $1$is_args$args'):
        if needle not in src:
            raise SystemExit(f'deploy conf is missing: {needle}')
    for d in ('cb', 'px', 'fc', 'uw', 'sc', 'logs'):
        (RUN / d).mkdir(parents=True, exist_ok=True)
    cert, key = RUN / 'cert.pem', RUN / 'key.pem'
    if not cert.exists():
        subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-keyout', str(key),
                        '-out', str(cert), '-days', '30', '-subj', '/CN=shell.fans'], check=True,
                       capture_output=True)
    conf = f'''
worker_processes 1;
error_log {RUN}/logs/error.log warn;
pid {RUN}/nginx.pid;
events {{ worker_connections 64; }}
http {{
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    access_log off;
    client_body_temp_path {RUN}/cb; proxy_temp_path {RUN}/px; fastcgi_temp_path {RUN}/fc;
    uwsgi_temp_path {RUN}/uw; scgi_temp_path {RUN}/sc;
    gzip on; gzip_vary on;

{maps}
    server {{
        listen 127.0.0.1:{HTTP_PORT};
        listen 127.0.0.1:{HTTPS_PORT} ssl;
        ssl_certificate {cert};
        ssl_certificate_key {key};
        server_name shell.fans localhost;
        root {ROOT};
        index index.html;
        error_page 404 $notfound_doc;

{locations}
    }}
}}
'''
    path = RUN / 'nginx.conf'
    path.write_text(conf, encoding='utf-8')
    return path


def nginx_start() -> None:
    conf = write_test_conf()
    subprocess.run(['nginx', '-t', '-c', str(conf), '-p', str(RUN)], check=True, capture_output=True)
    subprocess.run(['nginx', '-c', str(conf), '-p', str(RUN)], check=True)
    for _ in range(50):
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{HTTP_PORT}/', timeout=1).read()
            return
        except urllib.error.HTTPError:
            return          # any HTTP answer means the server is up
        except Exception:
            time.sleep(0.1)
    nginx_stop()
    raise SystemExit('test nginx did not come up')


def nginx_stop() -> None:
    pid = RUN / 'nginx.pid'
    if pid.exists():
        subprocess.run(['nginx', '-s', 'quit', '-c', str(RUN / 'nginx.conf'), '-p', str(RUN)], capture_output=True)
        for _ in range(30):
            if not pid.exists():
                break
            time.sleep(0.1)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def get(base: str, path: str, cookie: str | None = None, accept: str | None = None,
        extra: dict | None = None):
    req = urllib.request.Request(base + path)
    if cookie is not None:
        req.add_header('Cookie', cookie)
    if accept:
        req.add_header('Accept', accept)
    for k, v in (extra or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=10, context=CTX) as r:
            return r.status, dict((k.lower(), v) for k, v in r.headers.items()), r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, dict((k.lower(), v) for k, v in e.headers.items()), e.read().decode('utf-8', 'replace')


_NR = type('NR', (urllib.request.HTTPRedirectHandler,), {'redirect_request': lambda self, *a, **k: None})
_noredir = urllib.request.build_opener(_NR(), urllib.request.HTTPSHandler(context=CTX))


def get_raw(base: str, path: str, cookie: str | None = None):
    """Request WITHOUT following redirects → (status, Location header)."""
    req = urllib.request.Request(base + path)
    if cookie is not None:
        req.add_header('Cookie', cookie)
    try:
        with _noredir.open(req, timeout=10) as r:
            return r.status, r.headers.get('Location')
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get('Location')


def nav_labels(page: str) -> list[str]:
    m = re.search(r'<nav class="nav-menu[^>]*>(.*?)</nav>', page, re.S)
    if not m:
        return []
    return [re.sub(r'<[^>]+>', '', a).strip() for a in re.findall(r'<a [^>]*>(.*?)</a>', m.group(1), re.S)]


def mobile_labels(page: str) -> list[str]:
    m = re.search(r'<div class="mobile-menu" id="mobileMenu">(.*?)</div>', page, re.S)
    if not m:
        return []
    return [re.sub(r'<[^>]+>', '', a).strip() for a in re.findall(r'<a [^>]*>(.*?)</a>', m.group(1), re.S)]


def header_logo(page: str) -> str:
    m = re.search(r'class="nav-brand"[^>]*>\s*<img[^>]*src="([^"]+)"', page)
    return m.group(1) if m else ''


def footer_logo(page: str) -> str:
    m = re.search(r'<div class="sf-footer-brand"><img[^>]*src="([^"]+)"', page)
    return m.group(1) if m else ''


def lang(page: str) -> str:
    m = re.search(r'<html lang="([^"]+)">', page)
    return m.group(1) if m else ''


def title(page: str) -> str:
    m = re.search(r'<title>([^<]*)</title>', page)
    return m.group(1) if m else ''


def meta(page: str, sel: str) -> str:
    m = re.search(r'<meta %s content="([^"]*)"' % re.escape(sel), page)
    return m.group(1) if m else ''


def has_cjk(s: str) -> bool:
    return re.search(r'[一-鿿]', s) is not None


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def run_checks(base: str) -> None:
    print(f'\n[raw HTML locale checks against {base}]')

    # --- homepage: zh baseline (no cookie), explicit zh cookie, garbage cookie
    for label, cookie in (('no cookie', None), ('cookie=zh-TW', 'shellfans_locale=zh-TW'),
                          ('cookie=xx (invalid)', 'shellfans_locale=xx'),
                          ('cookie=zh-TW; junk', 'shellfans_locale=zh-TW; other=1')):
        st, h, body = get(base, '/', cookie)
        check(f'/ {label}: 200 + lang zh-Hant', st == 200 and lang(body) == 'zh-Hant', f'{st} {lang(body)}')
        check(f'/ {label}: zh title', has_cjk(title(body)), title(body))
        check(f'/ {label}: zh nav', nav_labels(body)[:1] == ['AEO/GEO 代管'], str(nav_labels(body)))
        check(f'/ {label}: zh logo', header_logo(body).endswith('nav_logo.svg'), header_logo(body))
        check(f'/ {label}: zh footer', '隱私權政策' in body and 'Privacy Policy' not in body.split('id="sf-footer-root"')[1][:4000])

    # --- homepage: English
    st, h, en = get(base, '/', 'shellfans_locale=en')
    check('/ cookie=en: 200', st == 200, str(st))
    check('/ cookie=en: lang en', lang(en) == 'en', lang(en))
    check('/ cookie=en: English title', title(en).startswith('ShellFans | AEO/GEO'), title(en))
    check('/ cookie=en: description en', not has_cjk(meta(en, 'name="description"')), meta(en, 'name="description"')[:60])
    check('/ cookie=en: og:title en', not has_cjk(meta(en, 'property="og:title"')), meta(en, 'property="og:title"'))
    check('/ cookie=en: og:description en', not has_cjk(meta(en, 'property="og:description"')))
    check('/ cookie=en: twitter:title en', not has_cjk(meta(en, 'name="twitter:title"')))
    check('/ cookie=en: og:locale en_US', meta(en, 'property="og:locale"') == 'en_US', meta(en, 'property="og:locale"'))
    check('/ cookie=en: nav English', nav_labels(en) == ['AEO/GEO Hosting', 'Engagement Engine', 'Fans Analysis', 'Word-of-Mouth', 'Pricing', 'Klog'], str(nav_labels(en)))
    check('/ cookie=en: mobile menu English', mobile_labels(en)[:3] == ['AEO/GEO Hosting', 'Engagement Engine', 'Fans Analysis'] and 'Get Started' in mobile_labels(en), str(mobile_labels(en)))
    check('/ cookie=en: header logo en', header_logo(en).endswith('nav_logo_en.png'), header_logo(en))
    check('/ cookie=en: footer logo en', footer_logo(en).endswith('nav_logo_en.png'), footer_logo(en))
    foot = en.split('id="sf-footer-root"')[1].split('</footer>')[0]
    check('/ cookie=en: footer English (links/legal/company)', all(x in foot for x in ('Privacy Policy', 'Terms of Service', 'ShellFans AI Technology Co., Ltd.', 'Site navigation', 'Invention Patent I908295')), foot[:200])
    check('/ cookie=en: footer keeps data-sf-product markers', 'data-sf-product="kolfans"' in foot and 'data-sf-product="shellfans-engine"' in foot)
    check('/ cookie=en: hero English', '<h2' in en and 'Turn social into' in en)
    check('/ cookie=en: language switcher shows English active', 'data-check-for="en"' in en and re.search(r'data-check-for="zh-TW"[^>]*display:none', en) is not None and re.search(r'data-check-for="en"[^>]*display:none', en) is None)
    check('/ cookie=en: no hide-until-JS hack', not re.search(r'html\s*\{[^}]*(visibility\s*:\s*hidden|opacity\s*:\s*0)', en))
    check('/ cookie=en: engine + dictionary still present (client switch back works)', "window.__setLocale = function" in en and "'zh-TW': {" in en)
    check('/ cookie=en: bootstrap v2 (server locale wins)', 'sf-locale-bootstrap v2' in en)
    st_up, _, up = get(base, '/', 'shellfans_locale=EN')
    check('/ cookie=EN (uppercase): case-sensitive map → Chinese (only lowercase en counts; Codex F3)', st_up == 200 and lang(up) == 'zh-Hant', f'{st_up} {lang(up)}')
    st0, h0, zh = get(base, '/', None)
    zh_chrome = (len(nav_labels(zh)), len(mobile_labels(zh)), zh.split('id="sf-footer-root"')[1].split('</footer>')[0].count('<a '))
    en_chrome = (len(nav_labels(en)), len(mobile_labels(en)), foot.count('<a '))
    check('/ nav + mobile menu + footer keep the same number of <a href> in zh and en', zh_chrome == en_chrome and zh_chrome[0] >= 5, f'{zh_chrome} vs {en_chrome}')
    check('/ en baseline has at least 40 crawlable links', en.count('<a href=') >= 40, str(en.count('<a href=')))
    check('/ canonical unchanged in en', '<link rel="canonical" href="https://shell.fans">' in en)
    check('/ JSON-LD untouched in en', zh[zh.find('application/ld+json'):zh.find('application/ld+json') + 3000] == en[en.find('application/ld+json'):en.find('application/ld+json') + 3000])
    check('/ cookie with other cookies present still en', lang(get(base, '/', 'a=1; shellfans_locale=en; b=2')[2]) == 'en')

    # --- cache separation
    check('/ HTML no-cache both variants', 'no-cache' in h0.get('cache-control', '') and 'no-cache' in h.get('cache-control', ''), f"{h0.get('cache-control')} | {h.get('cache-control')}")
    check('/ CDN-Cache-Control no-store both variants', h0.get('cdn-cache-control') == 'no-store' and h.get('cdn-cache-control') == 'no-store')
    check('/ ETag differs between zh and en', h0.get('etag') and h.get('etag') and h0.get('etag') != h.get('etag'), f"{h0.get('etag')} vs {h.get('etag')}")
    st304, _, _ = get(base, '/', 'shellfans_locale=en', extra={'If-None-Match': h0.get('etag', '')})
    check('/ zh ETag + en cookie → 200 (not a stale 304)', st304 == 200, str(st304))
    st304b, _, _ = get(base, '/', 'shellfans_locale=en', extra={'If-None-Match': h.get('etag', '')})
    check('/ en ETag + en cookie → 304', st304b == 304, str(st304b))
    check('/ Vary is unchanged (no Vary: Cookie on the asset-serving location)', 'cookie' not in h.get('vary', '').lower(), h.get('vary'))

    # --- every engine page has a working English variant
    for path, name in ENGINE_PAGES.items():
        st, _, body = get(base, path, 'shellfans_locale=en')
        check(f'{path} cookie=en: 200 + lang en', st == 200 and lang(body) == 'en', f'{st} {lang(body)}')
        check(f'{path} cookie=en: English nav + en logo', nav_labels(body)[:1] == ['AEO/GEO Hosting'] and header_logo(body).endswith('nav_logo_en.png'), f'{nav_labels(body)[:2]} {header_logo(body)}')
        st, _, body = get(base, path, None)
        check(f'{path} no cookie: lang zh-Hant', st == 200 and lang(body) == 'zh-Hant', f'{st} {lang(body)}')
        # direct variant URL must not exist
        stv, _, _ = get(base, f'/{name}.en.html', None)
        check(f'/{name}.en.html direct → 404', stv == 404, str(stv))

    # --- Chinese-only pages are unaffected by the cookie
    for path in ('/pricing', '/about', '/aeo/what-is-aeo', '/developers'):
        st1, _, b1 = get(base, path, None)
        st2, _, b2 = get(base, path, 'shellfans_locale=en')
        check(f'{path}: identical with and without en cookie', st1 == st2 == 200 and b1 == b2, f'{st1}/{st2} len {len(b1)}/{len(b2)}')

    # --- assets and negotiation unaffected
    st, hh, _ = get(base, '/js/sf-footer.js?v=20260913b', 'shellfans_locale=en')
    check('/js/sf-footer.js with en cookie: 200 JS', st == 200 and 'javascript' in hh.get('content-type', ''), f"{st} {hh.get('content-type')}")
    if (ROOT / 'index.md').exists():
        st, hh, _ = get(base, '/', 'shellfans_locale=en', accept='text/markdown')
        st, hh, md_body = get(base, '/', 'shellfans_locale=en', accept='text/markdown')
        check('/ Accept: text/markdown still negotiates the .md file first (precedence unchanged)', st == 200 and not md_body.lstrip().startswith('<!DOCTYPE') and '<html' not in md_body[:200], f"{st} {md_body[:60]!r}")
    st, _, _ = get(base, '/this-page-does-not-exist', 'shellfans_locale=en')
    check('unknown path with en cookie → 404', st == 404, str(st))
    # --- Codex remediation 2026-09-14 ---
    # F1: extensionless .en variants must 404 too (not just .en.html)
    for p in ('/index.en', '/social-media-backup.en', '/aeo-geo.en', '/what-is-shellfans.en'):
        stf, _, _ = get(base, p, None)
        check(f'F1 {p} (extensionless .en) → 404', stf == 404, str(stf))
        stf2, _, _ = get(base, p, 'shellfans_locale=en')
        check(f'F1 {p} with en cookie → 404', stf2 == 404, str(stf2))
    # F2: engine .html URLs 301 to their flat canonical form so cookie-locale applies
    for base_path in ('/social-media-backup', '/what-is-shellfans', '/aeo-geo', '/aeo-geo/methodology',
                      '/aeo-geo/taiwan-aeo-tools', '/tools/aeo-geo-checker'):
        stc, loc = get_raw(base, base_path + '.html', 'shellfans_locale=en')
        check(f'F2 {base_path}.html → 301 flat', stc == 301 and (loc or '').rstrip('/').endswith(base_path), f'{stc} {loc}')
        # after redirect, the flat URL with en cookie serves English (first frame en)
        stflat, _, bflat = get(base, base_path, 'shellfans_locale=en')
        check(f'F2 {base_path} (flat) + en cookie → en first frame', stflat == 200 and lang(bflat) == 'en', f'{stflat} {lang(bflat)}')
        # no cookie → the flat page stays Chinese
        check(f'F2 {base_path} (flat) no cookie → zh', lang(get(base, base_path)[2]) == 'zh-Hant')
    # F3: cookie value matching is case-sensitive (only lowercase en); mixed case → Chinese, like the client
    for badcookie in ('shellfans_locale=EN', 'shellfans_locale=En', 'shellfans_locale=eN'):
        check(f'F3 {badcookie} → zh (case-sensitive)', lang(get(base, '/', badcookie)[2]) == 'zh-Hant', badcookie)
    check('F3 exact lowercase en still → en', lang(get(base, '/', 'shellfans_locale=en')[2]) == 'en')

    st, _, b = get(base, '/aeo-geo/', 'shellfans_locale=en')
    check('/aeo-geo/ (directory form) unchanged behaviour (404 or same as before)', st in (403, 404), str(st))

    # --- generated variants are current
    r = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build-locale-pages.py'), '--check'], capture_output=True, text=True)
    check('build-locale-pages.py --check: all variants current', r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])


def main(argv: list[str]) -> int:
    if argv[:1] == ['start']:
        nginx_start(); print(f'test nginx up: http://127.0.0.1:{HTTP_PORT} https://127.0.0.1:{HTTPS_PORT} (pid {RUN}/nginx.pid)'); return 0
    if argv[:1] == ['stop']:
        nginx_stop(); print('test nginx stopped'); return 0
    base = None
    if '--base' in argv:
        base = argv[argv.index('--base') + 1]
    started = False
    if base is None:
        nginx_start(); started = True
        base = f'https://127.0.0.1:{HTTPS_PORT}'
    try:
        run_checks(base)
    finally:
        if started:
            nginx_stop()
    fails = [r for r in results if not r[1]]
    print(f'\n=== {len(results) - len(fails)}/{len(results)} checks passed ===')
    for name, _, detail in fails:
        print(' -', name, detail)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
