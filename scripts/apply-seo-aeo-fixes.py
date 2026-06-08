#!/usr/bin/env python3
"""
Apply SEO/AEO/A11y/Perf fixes to /var/www/shell.fans/*.html.

Idempotent: re-running is safe. Each fix checks current state before mutating.

Fixes applied:
  1. canonical link (if missing)
  2. meta description (if missing — uses page-specific text)
  3. og: title/description/url/image/type (top-up if missing)
  4. twitter:card / twitter:title / twitter:description / twitter:image
  5. theme-color
  6. JSON-LD WebPage referencing the canonical Organization @id (skipped on
     pages that already have JSON-LD)
  7. noindex meta on 401/404/search
  8. Add loading="lazy" + decoding="async" to <img> below the first 3
  9. Demote excess <h1> to <h2> (preserve attributes; first H1 kept)
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path('/home/kirin/work/shell.fans-static')

# Map filename → page meta. None values are kept-from-existing-or-default.
PAGE_META = {
    'index.html': {
        'canonical': 'https://shell.fans',
        'noindex': False,
        'jsonld_skip': False,
        'desc': None,  # already has
    },
    'what-is-shellfans.html': {
        'canonical': 'https://shell.fans/what-is-shellfans',
        'noindex': False,
        'jsonld_skip': True,
    },
    'aeo-geo.html': {
        'canonical': 'https://shell.fans/aeo-geo',
        'noindex': False,
        'jsonld_skip': True,
    },
    'co-founder.html': {
        'canonical': 'https://shell.fans/co-founder',
        'noindex': False,
        'jsonld_skip': False,
        'desc': '黃睿麒（Kirin Huang）創辦人介紹：ShellFans AI Technology 創辦人、KOL.FANS 產品設計者，分享品牌故事、技術路線與經歷時間軸。',
    },
    'contact.html': {
        'canonical': 'https://shell.fans/contact',
        'noindex': False,
        'jsonld_skip': False,
        'desc': '聯繫 ShellFans AI Technology：產品需求、合作洽談、媒體採訪與技術支援。Email hello@shell.fans，電話 +886-2-7714-3635。',
    },
    'price.html': {
        'canonical': 'https://shell.fans/price',
        'noindex': False,
        'jsonld_skip': False,
        'desc': 'KOL.FANS 與 ShellFans Chat 方案價格說明：B2C 創作者方案、B2B 企業方案、續航引擎、MAP 口碑行銷、Shell Chat 等五大產品線價目。',
    },
    'product.html': {
        'canonical': 'https://shell.fans/product',
        'noindex': False,
        'jsonld_skip': False,
        'desc': 'KOL.FANS 產品介紹：AI-powered KOL/KOC marketing management platform，提供名單管理、活動追蹤、成效分析與跨平台社群整合。',
    },
    'support.html': {
        'canonical': 'https://shell.fans/support',
        'noindex': False,
        'jsonld_skip': False,
        'desc': 'ShellFans 客戶支援：技術問題、帳號設定、付款協助、教學文件與聯繫窗口一站式查詢。',
    },
    'helpcenter.html': {
        'canonical': 'https://shell.fans/helpcenter',
        'noindex': False,
        'jsonld_skip': False,
        'desc': 'ShellFans / KOL.FANS 幫助中心：常見問題、操作教學、平台政策、付費方案說明、API 文件與聯絡資訊。',
    },
    'privacy-policy.html': {
        'canonical': 'https://shell.fans/privacy-policy',
        'noindex': False,
        'jsonld_skip': False,
        'desc': 'ShellFans 隱私權政策：說明日商唄粉智能科技有限公司如何收集、使用、保存與保護用戶個人資料。',
    },
    'terms-and-conditions.html': {
        'canonical': 'https://shell.fans/terms-and-conditions',
        'noindex': False,
        'jsonld_skip': False,
        'desc': 'ShellFans 服務條款：使用 KOL.FANS 與相關服務之權利義務、付費規則、智慧財產權與爭議解決條款。',
    },
    'kol-engine.html': {
        'canonical': 'https://shell.fans/kol-engine',
        'noindex': False,
        'jsonld_skip': False,
        'desc': 'KOL 引擎：KOL.FANS 內建的 AI 推薦與媒合系統，協助品牌主、代理商與行銷團隊根據活動需求快速鎖定合適網紅。',
    },
    'fans-analysis.html': {
        'canonical': 'https://shell.fans/fans-analysis',
        'noindex': False,
        'jsonld_skip': False,
    },
    'detail_news.html': {
        'canonical': 'https://shell.fans/detail_news',
        'noindex': True,  # individual news placeholder
        'jsonld_skip': True,
    },
    'search.html': {
        'canonical': None,
        'noindex': True,
        'jsonld_skip': True,
    },
    '401.html': {
        'canonical': None,
        'noindex': True,
        'jsonld_skip': True,
    },
    '404.html': {
        'canonical': None,
        'noindex': True,
        'jsonld_skip': True,
    },
}


def extract_existing_meta(html: str, name_or_property: str, attr: str = 'content'):
    pat = re.compile(
        rf'<meta[^>]*(?:name|property)=["\']{re.escape(name_or_property)}["\'][^>]*\b{attr}=["\']([^"\']*)["\']',
        re.IGNORECASE,
    )
    m = pat.search(html)
    if m:
        return m.group(1)
    # try reverse attr order
    pat2 = re.compile(
        rf'<meta[^>]*\b{attr}=["\']([^"\']*)["\'][^>]*(?:name|property)=["\']{re.escape(name_or_property)}["\']',
        re.IGNORECASE,
    )
    m2 = pat2.search(html)
    return m2.group(1) if m2 else None


def extract_title(html: str):
    m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else None


def insertion_anchor_idx(html: str):
    """Find index right after <meta charset> (or after <head> if absent)."""
    m = re.search(r'<meta\s+charset=[^>]*>', html, re.IGNORECASE)
    if m:
        return m.end()
    m = re.search(r'<head[^>]*>', html, re.IGNORECASE)
    if m:
        return m.end()
    return 0


WEBPAGE_JSONLD_TEMPLATE = """
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Organization",
      "@id": "https://shell.fans/#organization",
      "name": "ShellFans AI Technology",
      "alternateName": ["ShellFans", "ShellFans AI", "唄粉智能科技"],
      "legalName": "日商唄粉智能科技有限公司",
      "url": "https://shell.fans",
      "logo": "https://shell.fans/images/nav_logo.svg",
      "sameAs": ["https://www.facebook.com/profile.php?id=61581243232686", "https://www.instagram.com/shell_fansai/", "https://kol.fans", "https://blog.shell.fans"],
      "taxID": "83032387"
    }},
    {{
      "@type": "WebSite",
      "@id": "https://shell.fans/#website",
      "url": "https://shell.fans",
      "name": "ShellFans AI Technology",
      "publisher": {{"@id": "https://shell.fans/#organization"}},
      "inLanguage": ["zh-Hant", "en"]
    }},
    {{
      "@type": "WebPage",
      "@id": "{canonical}#webpage",
      "url": "{canonical}",
      "name": "{title_escaped}",
      "description": "{desc_escaped}",
      "inLanguage": "zh-Hant",
      "isPartOf": {{"@id": "https://shell.fans/#website"}},
      "about": {{"@id": "https://shell.fans/#organization"}}
    }}
  ]
}}
</script>
""".strip()


def js_escape(s: str) -> str:
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ').replace('\r', '').strip()


def add_or_keep_meta(html: str, tag_html: str, marker: str) -> tuple[str, bool]:
    """Insert tag_html after <meta charset> if marker not in html."""
    if marker in html:
        return html, False
    idx = insertion_anchor_idx(html)
    new = html[:idx] + '\n' + tag_html + html[idx:]
    return new, True


def fix_file(path: Path):
    name = path.name
    if name not in PAGE_META:
        return {'name': name, 'skipped': True, 'reason': 'no rule'}

    meta = PAGE_META[name]
    html = path.read_text(encoding='utf-8')
    changes = []

    # ---- 1. canonical
    if meta.get('canonical') and 'rel="canonical"' not in html and "rel='canonical'" not in html:
        tag = f'<link rel="canonical" href="{meta["canonical"]}">'
        html, did = add_or_keep_meta(html, tag, 'rel="canonical"')
        if did:
            changes.append('canonical')

    # ---- 2. noindex
    if meta.get('noindex'):
        if 'name="robots"' not in html:
            tag = '<meta name="robots" content="noindex,nofollow">'
            html, did = add_or_keep_meta(html, tag, 'name="robots"')
            if did:
                changes.append('noindex')

    # ---- 3. meta description
    if meta.get('desc') and not extract_existing_meta(html, 'description'):
        tag = f'<meta name="description" content="{meta["desc"]}">'
        html, did = add_or_keep_meta(html, tag, 'name="description"')
        if did:
            changes.append('description')

    # ---- 4. og: + twitter top-up
    title = extract_title(html) or 'ShellFans AI Technology'
    description = extract_existing_meta(html, 'description') or meta.get('desc') or 'ShellFans AI Technology — AI 行銷科技品牌'
    og_url = meta.get('canonical') or 'https://shell.fans'
    og_image = extract_existing_meta(html, 'og:image') or 'https://shell.fans/og/cba6b96a33cf4730.jpg'

    if not extract_existing_meta(html, 'og:title'):
        html, did = add_or_keep_meta(html, f'<meta property="og:title" content="{js_escape(title)}">', 'og:title')
        if did:
            changes.append('og:title')
    if not extract_existing_meta(html, 'og:description'):
        html, did = add_or_keep_meta(html, f'<meta property="og:description" content="{js_escape(description)}">', 'og:description')
        if did:
            changes.append('og:description')
    if not extract_existing_meta(html, 'og:url'):
        html, did = add_or_keep_meta(html, f'<meta property="og:url" content="{og_url}">', 'og:url')
        if did:
            changes.append('og:url')
    if not extract_existing_meta(html, 'og:image'):
        html, did = add_or_keep_meta(html, f'<meta property="og:image" content="{og_image}">', 'og:image')
        if did:
            changes.append('og:image')
    if not extract_existing_meta(html, 'og:type'):
        html, did = add_or_keep_meta(html, '<meta property="og:type" content="website">', 'og:type')
        if did:
            changes.append('og:type')
    if not extract_existing_meta(html, 'og:site_name'):
        html, did = add_or_keep_meta(html, '<meta property="og:site_name" content="ShellFans AI Technology">', 'og:site_name')
        if did:
            changes.append('og:site_name')
    if not extract_existing_meta(html, 'og:locale'):
        html, did = add_or_keep_meta(html, '<meta property="og:locale" content="zh_TW">', 'og:locale')
        if did:
            changes.append('og:locale')

    # twitter cards
    if not extract_existing_meta(html, 'twitter:card'):
        html, did = add_or_keep_meta(html, '<meta name="twitter:card" content="summary_large_image">', 'twitter:card')
        if did:
            changes.append('twitter:card')
    if not extract_existing_meta(html, 'twitter:title'):
        html, did = add_or_keep_meta(html, f'<meta name="twitter:title" content="{js_escape(title)}">', 'twitter:title')
        if did:
            changes.append('twitter:title')
    if not extract_existing_meta(html, 'twitter:description'):
        html, did = add_or_keep_meta(html, f'<meta name="twitter:description" content="{js_escape(description)}">', 'twitter:description')
        if did:
            changes.append('twitter:description')
    if not extract_existing_meta(html, 'twitter:image'):
        html, did = add_or_keep_meta(html, f'<meta name="twitter:image" content="{og_image}">', 'twitter:image')
        if did:
            changes.append('twitter:image')

    # ---- 5. theme-color
    if not extract_existing_meta(html, 'theme-color'):
        html, did = add_or_keep_meta(html, '<meta name="theme-color" content="#1A1D21">', 'theme-color')
        if did:
            changes.append('theme-color')

    # ---- 6. JSON-LD WebPage (if missing and not skipped)
    if not meta.get('jsonld_skip') and not meta.get('noindex'):
        if 'application/ld+json' not in html and meta.get('canonical'):
            block = WEBPAGE_JSONLD_TEMPLATE.format(
                canonical=meta['canonical'],
                title_escaped=js_escape(title),
                desc_escaped=js_escape(description),
            )
            # insert before </head>
            html2 = re.sub(r'</head>', block + '\n</head>', html, count=1, flags=re.IGNORECASE)
            if html2 != html:
                html = html2
                changes.append('jsonld_webpage')

    # ---- 7. Demote excess <h1> to <h2> (keep first)
    h1_positions = [m for m in re.finditer(r'<h1\b', html, re.IGNORECASE)]
    if len(h1_positions) > 1:
        # rewrite all but the first <h1...> → <h2...>, and </h1> → </h2> at matching depth
        # simplest: walk through and replace 2nd+ <h1 ...> openings, then mirror close tags in order
        new_html = []
        last = 0
        seen_h1 = 0
        for m in re.finditer(r'<(/?)h1\b([^>]*)>', html, re.IGNORECASE):
            new_html.append(html[last:m.start()])
            slash, attrs = m.group(1), m.group(2)
            if slash == '':
                seen_h1 += 1
                if seen_h1 > 1:
                    new_html.append(f'<h2{attrs}>')
                else:
                    new_html.append(m.group(0))
            else:
                if seen_h1 > 1:
                    new_html.append('</h2>')
                    seen_h1 -= 1  # decrement so subsequent close matches
                else:
                    new_html.append(m.group(0))
            last = m.end()
        new_html.append(html[last:])
        html2 = ''.join(new_html)
        if html2 != html:
            html = html2
            changes.append(f'h1_demote(-{len(h1_positions) - 1})')

    # ---- 8. Add loading="lazy" + decoding="async" to images beyond the first
    # Webflow img tags often look like <img src="..." loading="lazy" sizes="..." ...>
    img_iter = list(re.finditer(r'<img\b[^>]*?>', html, re.IGNORECASE))
    if len(img_iter) > 3:
        out = []
        last = 0
        added_lazy = 0
        added_decoding = 0
        for i, m in enumerate(img_iter):
            out.append(html[last:m.start()])
            tag = m.group(0)
            # skip first 3 images (likely above-fold)
            if i >= 3:
                if 'loading=' not in tag:
                    tag = tag.replace('<img', '<img loading="lazy"', 1)
                    added_lazy += 1
                if 'decoding=' not in tag:
                    tag = tag.replace('<img', '<img decoding="async"', 1)
                    added_decoding += 1
            out.append(tag)
            last = m.end()
        out.append(html[last:])
        html2 = ''.join(out)
        if html2 != html:
            html = html2
            if added_lazy or added_decoding:
                changes.append(f'img_lazy(+{added_lazy})_decoding(+{added_decoding})')

    if changes:
        path.write_text(html, encoding='utf-8')

    return {'name': name, 'changes': changes}


def main():
    results = []
    for path in sorted(ROOT.glob('*.html')):
        if path.is_file():
            r = fix_file(path)
            results.append(r)

    for r in results:
        if r.get('skipped'):
            print(f"  - skip {r['name']}: {r.get('reason')}")
        elif not r.get('changes'):
            print(f"  - {r['name']}: no changes")
        else:
            print(f"  + {r['name']}: {', '.join(r['changes'])}")


if __name__ == '__main__':
    main()
