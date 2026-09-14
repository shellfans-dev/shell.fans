#!/usr/bin/env python3
"""
Bake the *Published* Global UI navigation into the static pages so the FIRST paint (and the
no-JS / crawler baseline) already shows the current published nav — eliminating the
"old nav → new nav" flash caused by sf-global-ui.js swapping the hard-coded static nav at runtime.

Source of truth: GET https://console.shell.fans/api/site/global-ui?site=shell  (published only).
The generated markup mirrors sf-global-ui.js (same classes / dropdown structure / data-sf-nav-item),
so the runtime sync reconciles to the identical DOM → no visible change, no flash. `data-i18n` is
stripped from generated nav items so the in-page i18n engine does not overwrite the baked labels.

Per locale: `<page>.html` gets zh-TW labels, `<page>.en.html` gets English labels. Run this AFTER
scripts/build-locale-pages.py (which regenerates the .en.html from .html).

Containers handled (same as sf-global-ui.js):
  desktop: <nav class="… nav-menu …">   (plain 首頁型 and Webflow w-nav-menu both carry nav-menu)
  mobile:  #mobileMenu / .mobile-menu / #sfMobMenu / .sf-mob-menu

Auth links (/auth/(login|register|logout), data-sf-guest-login) and CTA anchors
(nav-cta / mobile-cta / sf-mob-cta) and Webflow .nav-button-wrapper are preserved untouched;
only the leading run of navigation items is replaced.

Usage:
  python3 scripts/apply-global-ui-nav.py [--check] [--api URL] [--snapshot FILE] [files...]
    --check      exit 3 if any page would change (CI staleness gate); writes nothing
    --api URL    override the published-config endpoint
    --snapshot   read the published config from a local JSON file instead of the API
    files        limit to specific files (default: all *.html except excluded dirs)
"""
from __future__ import annotations

import argparse
import html as _html
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = 'https://console.shell.fans/api/site/global-ui?site=shell'
EXCLUDE_DIR = {'node_modules', '.git', 'dist', 'build', 'partials', 'deploy', 'scripts', 'docs', 'prompts', '.claude'}
SAFE = re.compile(r'^(https?://|mailto:|tel:|/|#)', re.I)

MARK_OPEN = '<!--sf-gui-nav:start-->'
MARK_CLOSE = '<!--sf-gui-nav:end-->'


# ---------------------------------------------------------------------------
# published config
# ---------------------------------------------------------------------------

def load_config(api: str, snapshot: str | None) -> dict:
    if snapshot:
        return json.loads(Path(snapshot).read_text(encoding='utf-8')).get('data', {}) or json.loads(Path(snapshot).read_text(encoding='utf-8'))
    req = urllib.request.Request(api, headers={'User-Agent': 'apply-global-ui-nav'})
    with urllib.request.urlopen(req, timeout=20) as r:
        body = json.loads(r.read().decode('utf-8'))
    if body.get('fallback'):
        raise SystemExit('published config is a fallback (DB unavailable) — refusing to bake a fallback nav')
    return body.get('data') or {}


def loc_label(item: dict, locale: str) -> str:
    lab = item.get('label') or {}
    return lab.get(locale) or lab.get('zh-TW') or lab.get('en') or item.get('id', '')


def safe_href(h) -> bool:
    return isinstance(h, str) and h.strip() != '' and bool(SAFE.match(h.strip()))


def visible(items: list, device: str) -> list:
    out = []
    for it in items or []:
        if not it.get('enabled'):
            continue
        if not (it.get('desktop') if device == 'desktop' else it.get('mobile')):
            continue
        kids = []
        for c in it.get('children') or []:
            if not c.get('enabled'):
                continue
            if not (c.get('desktop') if device == 'desktop' else c.get('mobile')):
                continue
            if not safe_href(c.get('href')):
                continue
            kids.append(c)
        kids.sort(key=lambda x: x.get('order', 0))
        if not safe_href(it.get('href')) and not kids:
            continue
        cp = dict(it)
        cp['_kids'] = kids
        out.append(cp)
    out.sort(key=lambda x: x.get('order', 0))
    return out


# ---------------------------------------------------------------------------
# markup generation (mirrors sf-global-ui.js)
# ---------------------------------------------------------------------------

def _attrs(it: dict) -> str:
    a = ''
    if it.get('newTab'):
        a += ' target="_blank"'
    if it.get('external') or it.get('newTab'):
        a += ' rel="noopener noreferrer"'
    return a


def _anchor(it: dict, locale: str, cls: str, extra: str = '') -> str:
    href = it.get('href') or ''
    hattr = f' href="{_html.escape(href, quote=True)}"' if href else ''
    return (f'<a{hattr} class="{cls}"{_attrs(it)}{extra} data-sf-nav-item="{_html.escape(str(it.get("id","")), True)}">'
            f'{_html.escape(loc_label(it, locale))}')


def _submenu(kids: list, locale: str) -> str:
    sub = '<div class="sf-gui-submenu" role="menu">'
    for c in kids:
        sub += _anchor(c, locale, 'sf-gui-subitem', ' role="menuitem"') + '</a>'
    sub += '</div>'
    return sub


def render_desktop(items: list, locale: str) -> str:
    parts = []
    for it in items:
        kids = it.get('_kids') or []
        if kids:
            parent = _anchor(it, locale, 'nav-link sf-gui-parent', ' aria-haspopup="true" aria-expanded="false"')
            parent += '<span class="sf-gui-caret" aria-hidden="true">▾</span></a>'
            parts.append(f'<div class="sf-gui-group" data-sf-nav-group="{_html.escape(str(it.get("id","")),True)}">'
                         f'{parent}{_submenu(kids, locale)}</div>')
        else:
            parts.append(_anchor(it, locale, 'nav-link') + '</a>')
    return '\n        '.join(parts)


def render_mobile(items: list, locale: str) -> str:
    parts = []
    for it in items:
        kids = it.get('_kids') or []
        if kids:
            parent = _anchor(it, locale, 'sf-gui-parent', ' aria-haspopup="true" aria-expanded="false"') + '</a>'
            toggle = ('<button type="button" class="sf-gui-toggle" aria-expanded="false" '
                      f'aria-label="{_html.escape(loc_label(it, locale))}">▾</button>')
            parts.append(f'<div class="sf-gui-group sf-gui-acc" data-sf-nav-group="{_html.escape(str(it.get("id","")),True)}">'
                         f'{parent}{toggle}{_submenu(kids, locale)}</div>')
        else:
            parts.append(_anchor(it, locale, '') + '</a>')
    return '\n  '.join(parts)


# ---------------------------------------------------------------------------
# page surgery
# ---------------------------------------------------------------------------

AUTH_RE = re.compile(r'/auth/(login|register|logout)')


def is_keep_anchor(tag: str) -> bool:
    """auth / CTA anchors are preserved (they are not navigation items)."""
    if 'data-sf-guest-login' in tag:
        return True
    if AUTH_RE.search(tag):
        return True
    if re.search(r'class="[^"]*\b(nav-cta|mobile-cta|sf-mob-cta)\b', tag):
        return True
    return False


def replace_items(inner: str, generated: str) -> str | None:
    """Replace the leading run of navigation <a>/groups in a container's inner HTML with `generated`,
    preserving auth/CTA anchors, Webflow separators and .nav-button-wrapper. Idempotent via markers."""
    # strip any previously generated block
    inner = re.sub(re.escape(MARK_OPEN) + r'.*?' + re.escape(MARK_CLOSE), '', inner, flags=re.S)
    # tokens: anchors, previously-generated groups already stripped above
    tokens = list(re.finditer(r'<a\b[^>]*>.*?</a>|<div class="sf-gui-group.*?</div>\s*</div>', inner, re.S))
    if not tokens:
        return None
    first_keep = None
    last_item_end = None
    for m in tokens:
        t = m.group(0)
        if t.startswith('<a') and is_keep_anchor(t):
            first_keep = m.start()
            break
        last_item_end = m.end()
    # remove the leading nav-item run
    if first_keep is not None:
        cut_end = first_keep
    elif last_item_end is not None:
        cut_end = last_item_end
    else:
        return None
    start = tokens[0].start()
    block = f'{MARK_OPEN}\n        {generated}\n        {MARK_CLOSE}'
    return inner[:start] + block + inner[cut_end:]


# Each entry: (kind, priority, open-tag regex whose group(1) is the container tag name). The container
# body is delimited by the BALANCED matching close tag (regex cannot match nesting; our baked dropdowns
# contain nested <div>s, so a non-greedy `.*?</div>` would stop at the first inner </div> and corrupt the
# page on re-run — see _find_close).
CONTAINER_PATTERNS = [
    ('desktop', 0, re.compile(r'<(nav)\b[^>]*class="[^"]*\bnav-menu\b[^"]*"[^>]*>', re.S)),
    ('mobile', 1, re.compile(r'<(div|nav)\b[^>]*id="(?:mobileMenu|sfMobMenu)"[^>]*>', re.S)),
    ('mobile', 2, re.compile(r'<(div|nav)\b[^>]*class="[^"]*\b(?:mobile-menu|sf-mob-menu)\b[^"]*"[^>]*>', re.S)),
]


def _find_close(text: str, after: int, tag: str) -> int:
    """Return the index of the start of the balanced closing </tag> for a container whose open tag
    ended at `after`, accounting for nested <tag ...> elements. -1 if unbalanced/not found."""
    depth = 1
    for m in re.compile(r'<(/?)' + re.escape(tag) + r'\b[^>]*>', re.I).finditer(text, after):
        if m.group(1):
            depth -= 1
            if depth == 0:
                return m.start()
        else:
            depth += 1
    return -1


def process_html(text: str, locale: str, desk: str, mob: str) -> tuple[str, list]:
    changed = []
    # 1) locate every container with its balanced close
    found = []  # (open_start, body_start, close_start, close_end, kind, prio)
    for kind, prio, pat in CONTAINER_PATTERNS:
        for m in pat.finditer(text):
            tag = m.group(1)
            close_start = _find_close(text, m.end(), tag)
            if close_start < 0:
                continue
            cm = re.compile(r'</' + re.escape(tag) + r'\s*>', re.I).match(text, close_start)
            close_end = cm.end() if cm else close_start
            found.append((m.start(), m.end(), close_start, close_end, kind, prio))
    # 2) drop overlaps, keeping the higher-priority (lower prio number) container
    found.sort(key=lambda c: (c[0], c[5]))
    kept = []
    for c in found:
        if any(not (c[0] >= k[3] or c[2] <= k[0]) for k in kept):
            continue
        kept.append(c)
    # 3) splice from the end so earlier indices stay valid
    for open_start, body_start, close_start, close_end, kind, prio in sorted(kept, key=lambda c: c[0], reverse=True):
        inner = text[body_start:close_start]
        gen = desk if kind == 'desktop' else mob
        new_inner = replace_items(inner, gen)
        if new_inner is None or new_inner == inner:
            continue
        changed.append(kind)
        text = text[:body_start] + new_inner + text[close_start:]
    return text, changed


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--api', default=API)
    ap.add_argument('--snapshot')
    ap.add_argument('files', nargs='*')
    args = ap.parse_args(argv)

    cfg = load_config(args.api, args.snapshot)
    nav = cfg.get('navigation') or []
    if not nav:
        raise SystemExit('published navigation is empty — refusing to blank the site nav')

    variants = {
        'zh-TW': (render_desktop(visible(nav, 'desktop'), 'zh-TW'), render_mobile(visible(nav, 'mobile'), 'zh-TW')),
        'en': (render_desktop(visible(nav, 'desktop'), 'en'), render_mobile(visible(nav, 'mobile'), 'en')),
    }

    if args.files:
        files = [ROOT / f for f in args.files]
    else:
        files = [p for p in ROOT.rglob('*.html')
                 if not any(part in EXCLUDE_DIR for part in p.relative_to(ROOT).parts)]

    stale, wrote = [], 0
    for p in sorted(files):
        locale = 'en' if p.name.endswith('.en.html') else 'zh-TW'
        desk, mob = variants[locale]
        src = p.read_text(encoding='utf-8')
        out, changed = process_html(src, locale, desk, mob)
        if out != src:
            stale.append(str(p.relative_to(ROOT)) + (' [' + ','.join(sorted(set(changed))) + ']' if changed else ''))
            if not args.check:
                p.write_text(out, encoding='utf-8')
                wrote += 1
    if args.check:
        if stale:
            print('stale (nav not baked / outdated):')
            for s in stale:
                print('  ' + s)
            return 3
        print('all pages have the current published nav baked in')
        return 0
    print(f'baked published nav into {wrote} page(s)')
    for s in stale:
        print('  ' + s)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
