#!/usr/bin/env python3
"""
apply-unified-footer.py — idempotent fixer that gives every shell.fans page the
ONE unified, admin-editable footer.

For each *.html page it:
  1. ensures  <link rel="stylesheet" href="/css/sf-footer.css">  in <head>
  2. replaces the page's existing <footer>...</footer> (any of the drifted
     generations) with the unified mount:
         <footer class="sf-footer" role="contentinfo" data-sf-footer>
           <div id="sf-footer-root">…crawlable zh-TW default…</div>
         </footer>
     (pages with no <footer> — e.g. search.html — get it inserted before </body>)
  3. ensures  <script src="/js/sf-footer.js" defer></script>  before </body>

The crawlable default inside the mount keeps the footer visible for no-JS
clients and crawlers; /js/sf-footer.js then re-renders it from the live config
(kol.fans /api/site/footer?site=shell), locale-aware.

Idempotent: the <footer> carries a data-sf-footer marker; re-running skips
already-unified footers and never double-injects the link/script.

Usage:
    python3 scripts/apply-unified-footer.py            # apply in place
    python3 scripts/apply-unified-footer.py --dry-run  # report only
    python3 scripts/apply-unified-footer.py --page index.html [...]  # subset
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CSS_LINK = '<link rel="stylesheet" href="/css/sf-footer.css">'
JS_TAG = '<script src="/js/sf-footer.js" defer></script>'

_GLOBE = (
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<circle cx="12" cy="12" r="10"></circle><path d="M2 12h20"></path>'
    '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'
)

# Crawlable zh-TW default — must match /js/sf-footer.js build() output for the
# embedded SHELL_BASE so there is no visible jump when JS re-renders.
DEFAULT_INNER = (
    '<div class="sf-container">'
    '<div class="sf-footer-top"><div><div class="sf-footer-brand">'
    '<img decoding="async" loading="lazy" src="https://shell.fans/images/nav_logo.svg" alt="ShellFans AI" width="162" height="32"></div>'
    '<p class="sf-footer-desc">跨平台社群 AI 指揮中心。保存社群資產，看懂粉絲，同步經營與口碑成長。</p></div>'
    '<div class="sf-footer-col"><h3>產品</h3>'
    '<a href="https://shell.fans/kol-engine">續航引擎</a>'
    '<a href="https://shell.fans/fans-analysis">粉絲分析</a>'
    '<a href="https://kol.fans" target="_blank" rel="noopener noreferrer">口碑行銷</a>'
    '<a href="https://kol.fans/pricing" target="_blank" rel="noopener noreferrer">查看方案</a></div>'
    '<div class="sf-footer-col"><h3>資源</h3>'
    '<a href="https://blog.shell.fans/" target="_blank" rel="noopener noreferrer">Klog 部落格</a>'
    '<a href="https://shell.fans/helpcenter">幫助中心</a>'
    '<a href="https://shell.fans/support">客服支援</a></div>'
    '<div class="sf-footer-col"><h3>聯繫</h3>'
    '<a href="https://shell.fans/contact">關於我們</a>'
    '<a href="https://shell.fans/contact">歡迎聯繫</a>'
    '<a href="https://shell.fans/co-founder">創辦人</a></div></div>'
    '<div class="sf-footer-company" aria-label="公司資訊">'
    '<span class="sf-footer-company-row">日商唄粉智能科技有限公司</span>'
    '<span class="sf-footer-company-row">地址：臺北市內湖區瑞光路335號4樓</span>'
    '<span class="sf-footer-company-row"><a href="mailto:hello@shell.fans">信箱：hello@shell.fans</a></span>'
    '<span class="sf-footer-company-row"><a href="tel:0277143635">電話：02-77143635</a></span>'
    '<span class="sf-footer-company-row">統編：83032387</span></div>'
    '<div class="sf-footer-patent"><span>唄粉智能科技及其產品受商標、</span>'
    '<a href="https://tiponet.tipo.gov.tw/gpss2/gpsskmc/gpssbkm?!!FRURLTWI908295B" target="_blank" rel="noopener noreferrer">發明專利 I908295(臺灣)</a>'
    '<span>及其他申請中美國、日本之專利保護。</span></div>'
    '<div class="sf-footer-bottom">'
    '<span class="sf-footer-copy">© 2026 ShellFans AI. 日商唄粉智能科技有限公司. All rights reserved.</span>'
    '<button type="button" class="sf-footer-lang" data-sf-lang aria-label="切換語言">' + _GLOBE + '<span>English</span></button>'
    '<div class="sf-footer-social" aria-label="社群連結">'
    '<a href="https://www.facebook.com/profile.php?id=61581243232686" target="_blank" rel="noopener noreferrer" aria-label="Facebook">'
    '<img decoding="async" loading="lazy" src="https://shell.fans/images/facebook.svg" alt="Facebook" width="14" height="14"></a>'
    '<a href="https://www.instagram.com/shell_fansai/" target="_blank" rel="noopener noreferrer" aria-label="Instagram">'
    '<img decoding="async" loading="lazy" src="https://shell.fans/images/instagram.svg" alt="Instagram" width="14" height="14"></a></div>'
    '<div class="sf-footer-legal">'
    '<a href="https://shell.fans/privacy-policy">隱私權政策</a>'
    '<a href="https://shell.fans/terms-and-conditions">服務條款</a></div></div>'
    '</div>'
)

UNIFIED_FOOTER = (
    '<footer class="sf-footer" role="contentinfo" data-sf-footer>'
    '<div id="sf-footer-root">' + DEFAULT_INNER + '</div></footer>'
)

FOOTER_RE = re.compile(r"<footer\b[^>]*>.*?</footer>", re.IGNORECASE | re.DOTALL)
HEAD_CLOSE_RE = re.compile(r"</head>", re.IGNORECASE)
BODY_CLOSE_RE = re.compile(r"</body>", re.IGNORECASE)


def process(text: str):
    """Return (new_text, list_of_actions)."""
    actions = []

    # 1) CSS link
    if "/css/sf-footer.css" not in text:
        if HEAD_CLOSE_RE.search(text):
            text = HEAD_CLOSE_RE.sub("  " + CSS_LINK + "\n</head>", text, count=1)
            actions.append("css-link")
        else:
            actions.append("WARN:no </head>")

    # 2) footer mount
    if "data-sf-footer" in text:
        actions.append("footer-already-unified")
    elif FOOTER_RE.search(text):
        text = FOOTER_RE.sub(lambda _m: UNIFIED_FOOTER, text, count=1)
        actions.append("footer-replaced")
    elif BODY_CLOSE_RE.search(text):
        text = BODY_CLOSE_RE.sub(UNIFIED_FOOTER + "\n</body>", text, count=1)
        actions.append("footer-inserted")
    else:
        actions.append("WARN:no <footer>/</body>")

    # 3) JS tag (before the LAST </body>)
    if "/js/sf-footer.js" not in text:
        matches = list(BODY_CLOSE_RE.finditer(text))
        if matches:
            m = matches[-1]
            text = text[: m.start()] + JS_TAG + "\n" + text[m.start():]
            actions.append("js-tag")
        else:
            actions.append("WARN:no </body> for js")

    return text, actions


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    pages = [a for a in args if not a.startswith("--")]
    if pages:
        files = [ROOT / p for p in pages]
    else:
        files = sorted(ROOT.glob("*.html"))

    changed = 0
    for f in files:
        if not f.exists():
            print(f"  MISSING  {f.name}")
            continue
        original = f.read_text(encoding="utf-8")
        new, actions = process(original)
        if new != original:
            changed += 1
            if not dry:
                f.write_text(new, encoding="utf-8")
            tag = "DRY" if dry else "WROTE"
            print(f"  {tag:6} {f.name:30} {', '.join(actions)}")
        else:
            print(f"  skip   {f.name:30} {', '.join(actions) or 'no-op'}")

    print(f"\n{'Would change' if dry else 'Changed'}: {changed}/{len(files)} files")
    warned = False
    print("(re-run is idempotent; data-sf-footer marker prevents double-injection)")


if __name__ == "__main__":
    main()
