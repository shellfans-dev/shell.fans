# shell.fans Pre-fix Audit — 2026-06-08

Captures the state of `https://shell.fans` *before* the 2026-06-08
SEO/AEO/A11y/Performance pass. Companion file: `shell-fans-score-optimization-results.md`.

## Architecture

- Static HTML at `/var/www/shell.fans/` on origin host **125.227.138.215**
  (hostname `kirin`, same machine as the Bun proxy `shellfans-api` at
  `127.0.0.1:3081`).
- Cloudflare in front (zone `fa79ff868da4dca127105e16540502a3`), Full strict
  TLS mode. Cloudflare Origin Certificate on `/etc/nginx/ssl/shell.fans.crt`.
- No build step, no framework, no client-side router — every page is a
  hand-written HTML document. Webflow-exported pages (`product.html`,
  `support.html`, `helpcenter.html`, `price.html`) still carry the Webflow
  CSS bundle (`css/shellfans-v2.webflow.css` 303 KB).
- Live chat widget (Dify-backed, calls kol.fans CORS API + shellfans-api
  on 215) inlined in every page that wants it.
- 17 public HTML pages (3 of which are auth/error landing pages).
- `robots.txt`, `sitemap.xml`, `llms.txt`, `llms-full.txt`, `manifest.webmanifest`
  all present at root.
- nginx config: `/etc/nginx/sites-enabled/shell.fans.conf`.
- This codebase is **not in any git repo prior to 2026-06-08** — file
  history only existed as numbered `*.bak.*` snapshots in the same directory.
  Initialised as `shellfans-dev/shell.fans` on GitHub today.

## Asset inventory

| Folder | Notes |
| --- | --- |
| `css/` | `normalize.css` 7.6K, `webflow.css` 38K, `shellfans-v2.webflow.css` 303K (Webflow legacy — flagged as mostly unused by Lighthouse) |
| `js/` | `webflow.js` 1.0 MB (!), `vendor/gsap-3.14.2.min.js` 72K, `vendor/jquery-3.5.1.min.js` 88K, `vendor/clarity-7.7.2.js` 318 bytes. Most pages reference webflow.js + jquery + gsap; `index.html` is self-contained (no external JS except GTM) |
| `images/` | Webflow-generated responsive variants (`-p-500.jpg`, `-p-800.jpg`, `-p-1080.jpg`, `-p-1600.jpg`, `-p-2000.jpg`) for every hero image. GIFs for 4 product-feature animations |
| `icons/` | SVG + WebP for category icons |
| `data/` | `globe.json` (used by webflow) |
| `documents/` | `an03.json` |
| `partials/` | Reusable HTML fragments (loaded server-side via SSI? — to verify) |

## Pre-fix per-page audit (key fields)

| File | canonical | og:title | twitter:card | meta desc | JSON-LD | h1 count |
| --- | :-: | :-: | :-: | :-: | :-: | :-: |
| 401.html | ✗ | ✓ | ✗ | ✗ | ✗ | 0 |
| 404.html | ✗ | ✓ | ✗ | ✗ | ✗ | 0 |
| aeo-geo.html | ✓ | ✓ | ✓ | ✓ | ✓ | 1 |
| co-founder.html | ✓ | ✓ | ✗ | ✓ | ✗ | 1 |
| contact.html | ✗ | ✓ | ✗ | ✗ | ✗ | **11** |
| detail_news.html | ✗ | ✓ | ✓ | ✓ | ✗ | 0 |
| fans-analysis.html | ✓ | ✓ | ✓ | ✓ | ✗ | 1 |
| helpcenter.html | ✗ | ✓ | ✗ | ✗ | ✗ | 1 |
| index.html | ✓ | ✓ | ✓ | ✓ | ✗ | 1 |
| kol-engine.html | ✗ | ✓ | ✓ | ✓ | ✗ | 1 |
| price.html | ✗ | ✓ | ✗ | ✗ | ✗ | 3 |
| privacy-policy.html | ✗ | ✓ | ✗ | ✗ | ✗ | 0 |
| product.html | ✗ | ✓ | ✗ | ✗ | ✗ | **64** |
| search.html | ✗ | ✓ | ✗ | ✗ | ✗ | 1 |
| support.html | ✗ | ✓ | ✗ | ✗ | ✗ | **21** |
| terms-and-conditions.html | ✗ | ✓ | ✗ | ✗ | ✗ | 0 |
| what-is-shellfans.html | ✓ | ✓ | ✓ | ✓ | ✓ | 1 |

Webflow-exported pages with extreme `<h1>` counts are the dominant pre-fix accessibility risk (each `<h1>` in product cards / pricing tiers).

## Pre-fix Lighthouse baseline (1 run, mobile)

- Performance: **77**
- Accessibility: **89**
- Best Practices: **96**
- SEO: **100**

Top items causing each loss are documented in `shell-fans-score-optimization-results.md`.

## Pre-fix nginx security header state

Server-level `add_header` block:

- `X-Content-Type-Options: nosniff`
- `Content-Security-Policy: frame-ancestors 'self' https://kol.fans https://www.kol.fans;`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`

⚠️ All shadowed by `location /` and `location ~* \.(css|js)$` / `location ~* \.(jpg|...)$` blocks that each have their own `add_header` directives. nginx's `add_header` is **not additive across `location` blocks** — if a child block has any `add_header`, the parent's `add_header` directives are dropped. In practice this meant the security headers were only emitted on responses from non-matching paths, which in this site is effectively nothing.

(Patched in this pass — see results doc.)

## Pre-fix Cloudflare zone state

- Security Level: `medium`
- Bot Management: mostly disabled (`sbfm_definitely_automated: allow`, `ai_bots_protection: disabled`, `crawler_protection: disabled`)
- Managed Rulesets enabled: OWASP Core, Exposed Credentials, Managed Free, Managed
- 2 custom firewall rules: `managed_challenge` on `/auth/register` and `/auth/login` (only when `host != app.shell.fans`)

## Existing AEO assets (already strong before today)

- `robots.txt` — 21 explicitly-allowed AI crawler groups (GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot, Google-Extended, Applebot-Extended, meta-externalagent, Bytespider, CCBot, cohere-ai, ...). Sitemap declared.
- `llms.txt` + `llms-full.txt` — full llmstxt.org compliant brand hub with explicit "cite this page" hint pointing to `/what-is-shellfans`.
- `/what-is-shellfans` page — 11 sections + 10 FAQ + complete Organization + SoftwareApplication + WebPage + FAQPage JSON-LD.

These were the strong baseline for AEO. Today's pass extended consistency to the rest of the site.
