#!/usr/bin/env python3
"""
A11y fixes for shell.fans static HTML.

1. color-contrast: replace inline #94a3b8 → #475569 (slate-600 on white = 5.62
   contrast, passes WCAG AA). #94a3b8 is the legacy Tailwind slate-400 used
   widely in the chat widget inline styles.
2. landmark-one-main: wrap visible content in <main> if not present.
   Heuristic: pages with a <body> but no <main> → wrap content between </header>
   and <footer (or end of body) in <main>.
3. heading-order: footer <h4> in column headings → <h3> (sequence-friendly).
4. target-size: footer mailto:/tel: links → add padding for ≥24px tap target.
5. label-content-name-mismatch: shorten aria-label on #sfChatContextToggle
   so the visible "Chat 模式：關/開" text aligns. Move the long explanation
   into title (already present).
"""

import re
from pathlib import Path

ROOT = Path('/home/kirin/work/shell.fans-static')

OLD_GRAY = '#94a3b8'
NEW_GRAY = '#475569'


def fix_color_contrast(html: str) -> tuple[str, int]:
    count = html.count(OLD_GRAY)
    if count == 0:
        return html, 0
    return html.replace(OLD_GRAY, NEW_GRAY), count


def fix_chat_toggle_aria(html: str) -> tuple[str, bool]:
    """Drop the long aria-label so the visible label content matches."""
    pat = re.compile(
        r'(<button\s+id="sfChatContextToggle"[^>]*?)aria-label="[^"]*"\s*',
        re.IGNORECASE,
    )
    new = pat.sub(r'\1', html, count=1)
    return new, new != html


def fix_footer_h4_to_h3(html: str) -> tuple[str, int]:
    """Demote footer column h4 to h3 if site uses h2 for footer-top title.

    Webflow pattern: <div class="footer-col"><h4 class="footer-title">...</h4>
    We replace <h4 class=...> → <h3 class=...> inside footer-col only.
    """
    pat = re.compile(r'(<div[^>]*class="[^"]*footer-col[^"]*"[^>]*>\s*)<h4(\b[^>]*)>(.*?)</h4>', re.IGNORECASE | re.DOTALL)
    count = 0
    def sub(m):
        nonlocal count
        count += 1
        return m.group(1) + '<h3' + m.group(2) + '>' + m.group(3) + '</h3>'
    new = pat.sub(sub, html)
    return new, count


def fix_footer_target_size(html: str) -> tuple[str, bool]:
    """Insert a footer mailto/tel CSS rule to enlarge tap targets."""
    css = """
.footer-company-row a[href^="mailto:"],
.footer-company-row a[href^="tel:"]{display:inline-block;min-height:24px;padding:6px 4px;line-height:1.6;text-decoration:underline}
""".strip()
    if 'footer-company-row a[href^="mailto:"]' in html:
        return html, False
    # insert into the last <style>...</style> block in <head>
    last_style_close = html.rfind('</style>')
    if last_style_close == -1:
        return html, False
    new = html[:last_style_close] + '\n' + css + '\n' + html[last_style_close:]
    return new, True


def wrap_main_landmark(html: str) -> tuple[str, bool]:
    """Wrap <body> content in <main> if no <main> exists.

    Heuristic: look for the last </header> close and the first <footer> open.
    Wrap everything between them.
    """
    if re.search(r'<main\b', html, re.IGNORECASE):
        return html, False

    # Find the END of the last <header...>...</header> (close to top of body)
    header_close = None
    for m in re.finditer(r'</header>', html, re.IGNORECASE):
        header_close = m.end()
    # Find the start of <footer>
    footer_open = None
    for m in re.finditer(r'<footer\b', html, re.IGNORECASE):
        footer_open = m.start()
        break
    if header_close is None or footer_open is None or header_close >= footer_open:
        return html, False

    new = (
        html[:header_close]
        + '\n<main id="main">\n'
        + html[header_close:footer_open]
        + '\n</main>\n'
        + html[footer_open:]
    )
    return new, True


def main():
    for path in sorted(ROOT.glob('*.html')):
        html = path.read_text(encoding='utf-8')
        chs = []

        new, n = fix_color_contrast(html)
        if n:
            html = new
            chs.append(f'color({n})')

        new, did = fix_chat_toggle_aria(html)
        if did:
            html = new
            chs.append('chat_aria')

        new, n = fix_footer_h4_to_h3(html)
        if n:
            html = new
            chs.append(f'footer_h4→h3({n})')

        new, did = fix_footer_target_size(html)
        if did:
            html = new
            chs.append('footer_tap_size')

        new, did = wrap_main_landmark(html)
        if did:
            html = new
            chs.append('main_landmark')

        if chs:
            path.write_text(html, encoding='utf-8')
            print(f"  + {path.name}: {', '.join(chs)}")
        else:
            print(f"  - {path.name}: no changes")


if __name__ == '__main__':
    main()
