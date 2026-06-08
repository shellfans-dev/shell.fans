# shell.fans AEO / Performance Optimization — Repo Memory

Persistent context for anyone (human or AI) maintaining this repo after 2026-06-08.

## What this repo is

- `shellfans-dev/shell.fans` — pure static HTML for `https://shell.fans`.
- No build step, no framework, no router. Edit `*.html` directly.
- Deploys to `/var/www/shell.fans/` on **125.227.138.215** (ssh -p 22022 kirin@125.227.138.215 — or via the 216 hop if the 215 host key isn't in your known_hosts).
- nginx config lives on the same host at `/etc/nginx/sites-enabled/shell.fans.conf`.
- Backed by Cloudflare zone `fa79ff868da4dca127105e16540502a3` (Full strict TLS).
- Live chat widget on every page is a Dify-backed chat; it calls cross-origin into kol.fans (`/api/auth/me`, `/api/chat-sso/issue`) and the shellfans-api bun proxy at `127.0.0.1:3081` via nginx `/api/dify/` rewrite.

## SEO / AEO implementation locations

| Concern | Where |
| --- | --- |
| Per-page metadata (title, canonical, OG, Twitter, theme-color) | inline in each HTML `<head>` — first `<meta charset>` is the anchor for new tags |
| JSON-LD | inline `<script type="application/ld+json">` before `</head>`. Pattern: `@graph` containing Organization + WebSite + WebPage. `@id` references for cross-page entity unification (Organization is always `https://shell.fans/#organization`) |
| Brand hub JSON-LD | `/what-is-shellfans` — full Organization + SoftwareApplication + WebPage + FAQPage. **Don't generalise FAQPage to other pages** — keep it as a brand-hub-only artefact (matches the user's "FAQ schema 不是主要策略" rule) |
| robots.txt | `/robots.txt`. Lists 21 explicitly-allowed AI crawler groups by name. Maintain when new crawlers emerge (e.g., new AI search engines) |
| sitemap.xml | `/sitemap.xml`. Hand-curated. Add a new `<url>` block when introducing a new public page; remove when noindex'ing one. `lastmod` is informational — update it when content changes meaningfully |
| llms.txt + llms-full.txt | `/llms.txt` (short version with brand structure + citation hint) and `/llms-full.txt` (deep version). Follows llmstxt.org. Keep them in sync with the brand structure on `/what-is-shellfans` |

## Performance optimization locations

| Concern | Where |
| --- | --- |
| Image lazy-loading | `loading="lazy" decoding="async"` on `<img>` tags. The `scripts/apply-seo-aeo-fixes.py` idempotently adds these to images beyond the first 3 (assumed above-the-fold) |
| Webflow CSS bundle | `css/shellfans-v2.webflow.css` is 303 KB and mostly unused. Pages that DON'T reference it (e.g., `index.html`, `aeo-geo.html`) load faster. Long-term: purge with a CSS-tree-shaking step |
| Google Fonts | preconnect + `display=swap` already on every page. Don't add more external font CSS without weighing the LCP cost |
| GTM / Google Analytics | `<script async data-shellfans-ga="1" src="https://www.googletagmanager.com/gtag/js?id=G-NE4639EL2B">` — keep `async`. Don't move it earlier in the page |
| HTML caching | `Cache-Control: no-cache, must-revalidate` + `CDN-Cache-Control: no-store` on HTML so edits go live immediately (Cloudflare honours the second header) |
| Static asset caching | `expires 30d` for css/js, `expires 90d` for images/fonts. The matching `add_header Cache-Control "public, immutable"` makes the browser fully cache them |

## Security headers (nginx)

Patched 2026-06-08. Each `location` block emits its own set because nginx `add_header` is **non-additive across blocks** (the well-known gotcha):

| location | headers |
| --- | --- |
| `/` (HTML) | Cache-Control, CDN-Cache-Control, CSP frame-ancestors, X-Content-Type-Options, Referrer-Policy, **HSTS preload**, **Permissions-Policy**, **X-Frame-Options** |
| `~* \.(css\|js)$` | Cache-Control, X-Content-Type-Options, **HSTS preload**, Referrer-Policy |
| `~* \.(jpg\|jpeg\|png\|gif\|svg\|webp\|ico\|woff\|woff2\|ttf\|eot\|json)$` | Cache-Control, X-Content-Type-Options, **HSTS preload**, Referrer-Policy |

After edits: `sudo nginx -t && sudo systemctl reload nginx`.

Backup before that patch: `/etc/nginx/sites-enabled/shell.fans.conf.bak-secopt-20260608`.

## Dify / Chat Mode notes

- Chat widget code is inlined in `index.html` (`<script data-cfasync="false">` block around line 797). DO NOT externalize this script without first verifying SameSite cookie behaviour — it relies on `credentials: 'include'` cross-origin calls into kol.fans and on a same-origin call into `/api/dify/`.
- The chat widget makes 2 cross-origin fetches to `kol.fans` on every load: `/api/auth/me` and `/api/chat-sso/issue`. Both return 401 for anonymous visitors. This is **intentional** and a known Best Practices score hit (logged in `errors-in-console`). Don't try to "fix" by suppressing — the 401 contract is depended on by other clients. The right long-term fix is to teach kol.fans to return `200 { authenticated: false }` for anon, but that's a kol.fans repo change, not shell.fans.
- `chat-mode.svg` in `icons/` is the toggle button asset.

## shell.fans / kol.fans differences

| | shell.fans | kol.fans |
| --- | --- | --- |
| Repo | this one — static HTML | `shellfans-dev/saas_womm` — Next.js |
| Deploy host | 215 nginx static | coder1bot pm2 saas-womm |
| Domain role | brand / landing / AEO hub / chat experience | authenticated product (KOL.FANS) |
| Auth | none on shell.fans HTML itself; chat widget reads kol.fans session via cross-origin fetch | own login at kol.fans/login |
| API surface | `/api/dify/` proxied to bun shellfans-api on 215 | `/api/*` Next.js API routes |
| robots | this repo's `/robots.txt` | kol.fans serves its own `/robots.txt` from saas_womm |

Don't try to share JSON-LD blocks across the two — each domain has its own Organization `@id` even though they share the same legal entity. The brand hub JSON-LD on shell.fans points at `https://shell.fans/#organization`; kol.fans pages should reference their own `https://kol.fans/#organization` for entity unification within the product.

## Maintenance SOP

- **Adding a new public page**: copy an existing simple page (e.g. `co-founder.html`) as the starting template. Run `python3 scripts/apply-seo-aeo-fixes.py` (after adding a `PAGE_META` entry for the new file) to populate canonical + OG + JSON-LD. Add a `<url>` block to `sitemap.xml`. Then `scp` to 215.
- **Adding a new image to a page**: include `width`, `height`, `alt`, `loading="lazy"`, `decoding="async"` (except hero / above-fold images).
- **Editing nginx**: always test with `sudo nginx -t` before `sudo systemctl reload nginx`. Keep a backup with `.bak-purpose-YYYYMMDD` suffix.
- **Running Lighthouse**: from 216, `npx lighthouse https://shell.fans/ --form-factor=mobile --chrome-flags="--headless --no-sandbox --disable-gpu"`. Cloudflare may 403 from data-centre IPs — temporarily lower `security_level` to `essentially_off` via CF API if needed, restore to `medium` after.
- **Deploying changes from local working tree** (`/home/kirin/work/shell.fans-static`) to 215:
  ```bash
  tar c --exclude=.git --exclude=docs --exclude=scripts --exclude='*.bak*' . | \
    ssh -p 22022 chatshellfans-216 'ssh -p 22022 kirin@125.227.138.215 "cd /var/www/shell.fans && sudo -u kirin tar x"'
  ssh -p 22022 chatshellfans-216 'ssh -p 22022 kirin@125.227.138.215 "sudo chmod -R o+r /var/www/shell.fans/ && sudo chmod o+x /var/www/shell.fans/ /var/www/shell.fans/*/"'
  ```
  The chmod step is required — tar preserves source owner perms (660 by default here) and nginx (www-data) can't read those.

## Commands executed during the 2026-06-08 optimization pass

```bash
# Pulled live tree to local working dir
tar c --exclude='*.bak*' --exclude='og' . | tar x  # via SSH chain

# Created GitHub repo (from coder1bot which has gh auth)
gh repo create shellfans-dev/shell.fans --public --description "..."

# Baseline
npx lighthouse https://shell.fans/ ... --output-path=docs/audits/lighthouse-shell-fans-before-1.json

# Apply fixes
python3 scripts/apply-seo-aeo-fixes.py
python3 scripts/apply-a11y-fixes.py

# Sitemap rewrite
# (manual edit of sitemap.xml)

# nginx patch + reload (on 215, via ssh chain)
sudo cp /etc/nginx/sites-enabled/shell.fans.conf /etc/nginx/sites-enabled/shell.fans.conf.bak-secopt-20260608
sudo python3 ...patch script...
sudo nginx -t && sudo systemctl reload nginx

# Deploy
tar c --exclude=.git --exclude=docs --exclude=scripts ... | ssh ... tar x
sudo chmod -R o+r /var/www/shell.fans/

# After-Lighthouse (3 runs, median)
for i in 1 2 3; do npx lighthouse ... after-$i.json; sleep 5; done

# Commit + push (after this file)
git add -A
git commit -m "..."
git push origin main
```

## Score history

| Date | Performance | Accessibility | Best Practices | SEO | Mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2026-06-08 (pre) | 77 | 89 | 96 | 100 | 90.5 |
| 2026-06-08 (post, median of 3) | 80 | 96 | 96 | 100 | 93.0 |

When extending: append a new row, don't rewrite history.
