#!/usr/bin/env python3
"""
為 shell.fans 各頁的「產品服務」nav / footer 連結加上 data-sf-product 標記，
供 Cloudflare Worker（edge, request-time）依產品服務開關於首屏 HTML 中移除，
避免 client-side 先顯示再消失的 flicker。

只標記「精確文字」的 <a>（nav / footer / dropdown 連結），刻意排除內文 CTA
（例如「前往 kol.fans 了解口碑行銷」文字不同 → 不標記）。冪等：已標記者略過。

用法：python3 scripts/mark-product-nav.py [repo_root]   （預設為腳本上層目錄）
"""
import re
import sys
import os
import glob

# 產品 → 標記值 : nav 顯示的「精確文字」
PRODUCTS = [
    ("kolfans", "口碑行銷"),
    ("shellfans-engine", "續航引擎"),
    ("aeogeo", "AEO/GEO 代管"),
]


def mark_file(path: str) -> dict:
    html = open(path, encoding="utf-8").read()
    counts = {}
    for key, text in PRODUCTS:
        # 尚未標記、且 <a>…</a> 內文恰為 text（允許前後空白）的連結
        pat = re.compile(
            r'<a\b(?![^>]*\bdata-sf-product=)([^>]*?)>(\s*' + re.escape(text) + r'\s*)</a>'
        )
        html, n = pat.subn(r'<a data-sf-product="' + key + r'"\1>\2</a>', html)
        if n:
            counts[key] = n
    if counts:
        open(path, "w", encoding="utf-8").write(html)
    return counts


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = [f for f in glob.glob(os.path.join(root, "*.html")) if ".bak" not in f]
    grand = {}
    for f in sorted(files):
        c = mark_file(f)
        if c:
            print(f"  {os.path.basename(f):28s} {c}")
            for k, v in c.items():
                grand[k] = grand.get(k, 0) + v
    print("合計標記：", grand or "（無新增，全部已標記）")


if __name__ == "__main__":
    main()
