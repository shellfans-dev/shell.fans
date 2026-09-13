#!/usr/bin/env python3
"""
Wire the Global UI runtime (js/sf-global-ui.js) into every page that already
loads js/sf-footer.js, and bump the shared asset version so Cloudflare serves
the new sf-footer.js without a cache purge.

Idempotent: re-running is safe.

Why a query-string version instead of a purge: js/*.js is served with a long
immutable cache-control (see nginx shell.fans.conf); HTML is no-cache. Changing
the URL in the HTML makes every browser fetch the new file immediately.

Global UI runtime = console.shell.fans → UIUX Design → Global 共用元件.
The static header / nav / footer in each page stays as the no-JS + crawler
baseline; sf-global-ui.js only applies the published differences at runtime.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSET_VER = '20260913a'

FOOTER_TAG_RE = re.compile(r'<script src="/js/sf-footer\.js\?v=([0-9a-z]+)" defer></script>')
GLOBAL_UI_TAG = f'<script src="/js/sf-global-ui.js?v={ASSET_VER}" defer></script>'
GLOBAL_UI_RE = re.compile(r'<script src="/js/sf-global-ui\.js\?v=[0-9a-z]+" defer></script>')


def process(path: Path) -> str:
    html = path.read_text(encoding='utf-8')
    m = FOOTER_TAG_RE.search(html)
    if not m:
        return 'skip (no sf-footer.js)'
    new = html
    changes = []

    # 1) bump sf-footer.js version
    if m.group(1) != ASSET_VER:
        new = FOOTER_TAG_RE.sub(f'<script src="/js/sf-footer.js?v={ASSET_VER}" defer></script>', new)
        changes.append(f'footer v{m.group(1)}→{ASSET_VER}')

    # 2) ensure sf-global-ui.js is loaded right after sf-footer.js (defer keeps order:
    #    footer renders first, then Global UI applies the published differences)
    g = GLOBAL_UI_RE.search(new)
    if not g:
        new = new.replace(
            f'<script src="/js/sf-footer.js?v={ASSET_VER}" defer></script>',
            f'<script src="/js/sf-footer.js?v={ASSET_VER}" defer></script>\n{GLOBAL_UI_TAG}',
            1,
        )
        changes.append('add sf-global-ui.js')
    elif g.group(0) != GLOBAL_UI_TAG:
        new = GLOBAL_UI_RE.sub(GLOBAL_UI_TAG, new)
        changes.append('global-ui version bump')

    if new != html:
        path.write_text(new, encoding='utf-8')
        return ', '.join(changes)
    return 'ok (already wired)'


def main() -> int:
    pages = sorted(p for p in ROOT.rglob('*.html')
                   if not any(part in ('docs', 'node_modules', '.git', 'partials', 'deploy') for part in p.relative_to(ROOT).parts))
    touched = 0
    for p in pages:
        r = process(p)
        if r.startswith('skip'):
            continue
        if not r.startswith('ok'):
            touched += 1
        print(f'{p.relative_to(ROOT)}: {r}')
    print(f'--- {touched} page(s) changed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
