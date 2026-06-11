#!/usr/bin/env python3
"""
Inject a unified shellfans-style mobile nav overlay into 14 HTML pages.

The overlay sits at the top of the page on screens ≤991px wide, hides any
existing site header (Webflow's `.navbar.w-nav` or the custom `<header class="nav">`),
and provides a working hamburger button + side drawer with the standard
shellfans navigation items + login + CTA.

Idempotent: re-running is safe. Each fix checks current state before mutating.

CSS classes are prefixed `sf-mob-` to avoid collisions with Webflow's `.nav-menu`
and the custom pages' `.mobile-menu`.

The fix is OPT-IN per page through the PAGES list below. Pages already using the
homepage-style hamburger (index.html, aeo-geo.html) are NOT touched.
"""

import re
from pathlib import Path

ROOT = Path('/home/kirin/work/shell.fans-static')

# 14 pages that need the unified overlay. Excludes index.html (canonical) and
# aeo-geo.html (already fixed with a different in-place pattern).
PAGES = [
    '401.html',
    '404.html',
    'co-founder.html',
    'contact.html',
    'detail_news.html',
    'fans-analysis.html',
    'helpcenter.html',
    'kol-engine.html',
    'price.html',
    'privacy-policy.html',
    'product.html',
    'search.html',
    'support.html',
    'terms-and-conditions.html',
    'what-is-shellfans.html',
]

INJECT_MARKER = 'sf-mob-nav-bootstrap'

INJECT_HTML = """
<!-- ===== shellfans unified mobile nav (sf-mob-nav-bootstrap) ===== -->
<header class="sf-mob-header" aria-hidden="false">
  <a href="https://shell.fans/" class="sf-mob-brand" aria-label="ShellFans">
    <img src="https://shell.fans/images/nav_logo.svg" alt="ShellFans" width="120" height="26">
  </a>
  <button type="button" class="sf-mob-hamburger" id="sfMobHamburger" aria-label="開啟選單" aria-expanded="false" aria-controls="sfMobMenu">
    <span></span><span></span><span></span>
  </button>
</header>
<div class="sf-mob-menu" id="sfMobMenu" role="dialog" aria-modal="true" aria-label="主選單">
  <a href="https://shell.fans/aeo-geo">AEO/GEO 代管</a>
  <a href="https://shell.fans/kol-engine">續航引擎</a>
  <a href="https://shell.fans/fans-analysis">粉絲分析</a>
  <a href="https://kol.fans" target="_blank" rel="noopener">口碑行銷</a>
  <a href="https://kol.fans/pricing" target="_blank" rel="noopener">查看方案</a>
  <a href="https://blog.shell.fans/" target="_blank" rel="noopener">Klog</a>
  <a href="https://kol.fans/login?next=https%3A%2F%2Fshell.fans%2F">登入</a>
  <a href="https://kol.fans/signup" target="_blank" rel="noopener" class="sf-mob-cta">開始使用</a>
</div>
<style id="sf-mob-nav-css">
.sf-mob-header,.sf-mob-menu{display:none}
.sf-mob-header{align-items:center;justify-content:space-between;position:fixed;top:0;left:0;right:0;height:60px;padding:0 18px;background:rgba(255,255,255,0.97);border-bottom:1px solid #E8E5DE;z-index:9000;-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);box-sizing:border-box}
.sf-mob-brand{display:flex;align-items:center;text-decoration:none}
.sf-mob-brand img{height:26px;width:auto;display:block}
.sf-mob-hamburger{flex-direction:column;gap:5px;background:none;border:0;cursor:pointer;padding:8px;display:flex}
.sf-mob-hamburger span{display:block;width:22px;height:2px;background:#101214;border-radius:2px;transition:transform 200ms,opacity 200ms}
.sf-mob-hamburger[aria-expanded="true"] span:nth-child(1){transform:translateY(7px) rotate(45deg)}
.sf-mob-hamburger[aria-expanded="true"] span:nth-child(2){opacity:0}
.sf-mob-hamburger[aria-expanded="true"] span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
.sf-mob-menu{position:fixed;top:60px;left:0;right:0;bottom:0;background:#fff;padding:1.5rem 1.5rem 2rem;flex-direction:column;z-index:8999;overflow-y:auto}
.sf-mob-menu.active{display:flex}
.sf-mob-menu a{font-size:1.05rem;font-weight:500;padding:1rem 0;border-bottom:1px solid #E8E5DE;color:#101214;text-decoration:none}
.sf-mob-menu .sf-mob-cta{display:inline-flex;align-items:center;justify-content:center;margin-top:1.5rem;padding:14px 24px;background:#E96F5E;color:#fff;border-radius:8px;font-weight:600;border:none}
@media (max-width:991px){
  .sf-mob-header{display:flex}
  /* Hide every known existing site header on mobile so only sf-mob-header shows */
  .navbar.w-nav,header.nav,#nav.nav{display:none !important}
  /* shellfans body content typically starts with padding-top:72px to clear the
     desktop nav; on mobile the sf-mob-header is 60px so adjust if needed */
  body.sf-mob-active{padding-top:60px}
}
</style>
<script id="sf-mob-nav-js">
(function(){
  var hamb = document.getElementById('sfMobHamburger');
  var menu = document.getElementById('sfMobMenu');
  if (!hamb || !menu) return;
  function setExpanded(state){
    hamb.setAttribute('aria-expanded', state ? 'true' : 'false');
    if (state) menu.classList.add('active'); else menu.classList.remove('active');
    document.body.style.overflow = state ? 'hidden' : '';
  }
  hamb.addEventListener('click', function(){
    setExpanded(!menu.classList.contains('active'));
  });
  menu.querySelectorAll('a').forEach(function(a){
    a.addEventListener('click', function(){ setExpanded(false); });
  });
  // ESC closes the menu
  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape' && menu.classList.contains('active')) setExpanded(false);
  });
})();
</script>
<!-- ===== /shellfans unified mobile nav ===== -->
""".strip()


def inject_one(path: Path):
    html = path.read_text(encoding='utf-8')
    if INJECT_MARKER in html:
        return {'name': path.name, 'skipped': True, 'reason': 'already injected'}

    # Insert just before </body>
    m = re.search(r'</body>', html, re.IGNORECASE)
    if not m:
        return {'name': path.name, 'skipped': True, 'reason': 'no </body>'}

    new = html[:m.start()] + '\n' + INJECT_HTML + '\n' + html[m.start():]
    path.write_text(new, encoding='utf-8')
    return {'name': path.name, 'injected': True}


def main():
    results = []
    for name in PAGES:
        path = ROOT / name
        if not path.exists():
            results.append({'name': name, 'skipped': True, 'reason': 'file missing'})
            continue
        results.append(inject_one(path))

    for r in results:
        if r.get('skipped'):
            print(f"  - {r['name']}: skipped ({r.get('reason')})")
        elif r.get('injected'):
            print(f"  + {r['name']}: injected")
        else:
            print(f"  ? {r['name']}: {r}")


if __name__ == '__main__':
    main()
