# Unified footer (shell.fans static side)

Static-site half of the cross-site footer editor. Full report (kol.fans admin,
data model, APIs, security, deploy) lives in the `saas_womm` repo:
`docs/reports/uiux-footer-editor-shellfans-kolfans.md`.

Branch: `feat/unified-footer-shellfans` (off `main`). Status: implemented +
locally verified, **not deployed** (tar deploy to `/var/www/shell.fans` is
review-gated).

## What changed here
- `css/sf-footer.css` — self-contained, `sf-`-prefixed footer styles (works on
  the 14 legacy Webflow pages that lacked the modern footer CSS).
- `js/sf-footer.js` — renders the footer from `https://kol.fans/api/site/footer?site=shell`
  (CORS), with embedded defaults as fallback; locale-aware via `localStorage
  'shellfans_locale'` + the `shellfans-locale-changed` event; functional
  language toggle; HTML-escaped; href-guarded.
- `scripts/apply-unified-footer.py` — idempotent fixer. Unified the footer on
  all 17 pages (16 `<footer>` replaced, `search.html` inserted) and injected the
  CSS `<link>` + the JS `<script defer>`. Re-runnable (the `data-sf-footer`
  marker prevents double-injection).

## How content flows
Edits in the kol.fans admin (UIUX Design → Footer 頁尾, site = shell.fans) are
saved to `system_settings['footer_settings__shell']` and served by
`/api/site/footer?site=shell`. shell.fans pages fetch that at runtime — **no
redeploy needed for content changes**. A crawlable zh-TW default is baked into
each page's mount so no-JS clients/crawlers still see a full footer.

## Verify after deploy
- `/css/sf-footer.css` and `/js/sf-footer.js` are served (200) and world-readable
  (`chmod -R o+r` after the tar copy).
- Footer renders on a modern page (index.html) and a legacy page (contact.html),
  desktop + mobile; confirm full-bleed dark background on legacy pages.
- Language toggle switches zh-TW/en; editing in admin reflects on next load.
