#!/usr/bin/env python3
"""
驗證各網域的分析追蹤拓撲符合預期。可重複執行。

## 為什麼需要這支

追蹤設定散在四個地方——靜態 HTML、Next.js layout、saas_womm 的 DB 設定、
WordPress 的 Site Kit——沒有任何單一位置能看出「誰在追蹤、送到哪」。
2026-09-04 盤點時就發現三個問題：29 個 /aeo 頁面沒有追蹤、13 頁送到帳戶外
的 property、以及我自己一度誤判 console 有追蹤（其實是首頁轉址造成的）。

這支腳本把「應該是什麼樣子」寫成可執行的斷言。日後有人改動追蹤設定時，
偏離預期會立刻被抓到，而不是等到報表數字不對才發現。

## 預期拓撲（2026-09-04 與使用者確認）

    shell.fans          追蹤 → G-NE4639EL2B（properties/410150889）
    app.shell.fans      追蹤 → 同一個 property（行銷→產品漏斗需要連續）
    console.shell.fans  **不追蹤** —— 管理者後臺
    blog.shell.fans     **獨立追蹤** —— 自己的 GTM/Google Tag，不得混入上面的 property

用法：python3 scripts/verify-tracking-topology.py
"""

import re
import sys
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (compatible; ShellFansTopologyCheck/1.0)"
SHELLFANS_ID = "G-NE4639EL2B"

_fail = []
_pass = 0


def fetch(url, follow=True):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    try:
        opener = urllib.request.build_opener()
        if not follow:
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, *a, **k):
                    return None
            opener = urllib.request.build_opener(NoRedirect)
        with opener.open(req, timeout=25) as r:
            return r.status, r.geturl(), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, url, e.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, url, f"__ERROR__{e}"


def check(name, ok, detail=""):
    global _pass
    if ok:
        _pass += 1
        print(f"  ✅ {name}")
    else:
        _fail.append((name, detail))
        print(f"  ❌ {name}{'  — ' + detail if detail else ''}")


def ga_ids(html):
    return set(re.findall(r"G-[A-Z0-9]{8,}", html))


print("\n### shell.fans —— 應追蹤，且用 ShellFans 自管的 property")
for path in ["/", "/aeo/what-is-aeo", "/aeo/gptbot-oai-searchbot", "/contact", "/about"]:
    st, _, html = fetch("https://shell.fans" + path)
    ids = ga_ids(html)
    check(f"{path} 含 {SHELLFANS_ID}", st == 200 and SHELLFANS_ID in ids,
          f"status={st} ids={sorted(ids)}")

st, _, html = fetch("https://shell.fans/js/sf-analytics.js")
check("AI 歸因腳本可取得", st == 200 and "ai_referral_landing" in html, f"status={st}")

# 同一頁不得對同一個 property 重複 config——那會讓 page_view 灌水
st, _, html = fetch("https://shell.fans/")
n = len(re.findall(r'gtag\(["\']config["\'],\s*["\']' + SHELLFANS_ID, html))
check("首頁未重複 config 同一 property", n == 1, f"config 次數={n}")

print("\n### app.shell.fans —— 應追蹤，且與 shell.fans 同一 property")
st, final, html = fetch("https://app.shell.fans/auth/login")
ids = ga_ids(html)
check("app 含 ShellFans property", st == 200 and SHELLFANS_ID in ids,
      f"status={st} ids={sorted(ids)}")
check("app 標記為自管標籤", "data-shellfans-ga" in html)

print("\n### console.shell.fans —— 管理者後臺，不應追蹤")
for path in ["/portal", "/login"]:
    st, final, html = fetch("https://console.shell.fans" + path, follow=False)
    # 只檢查真正由 console 提供的頁面；轉址到 shell.fans 的不算
    if "shell.fans" in final and "console" not in final:
        print(f"  ⏭  {path} 轉址到 {final}，非 console 自身頁面")
        continue
    has = bool(re.search(r"googletagmanager|gtag\(", html))
    check(f"{path} 無追蹤程式碼", not has,
          "偵測到 gtag/GTM —— 管理後臺不應追蹤")

print("\n### blog.shell.fans —— 獨立追蹤，不得混入 ShellFans property")
st, _, html = fetch("https://blog.shell.fans/")
ids = ga_ids(html)
check("blog 可取得", st == 200, f"status={st}")
check(f"blog 不含 {SHELLFANS_ID}", SHELLFANS_ID not in ids,
      f"blog 的資料混進了 shell.fans 的 property：{sorted(ids)}")
own = re.findall(r"GTM-[A-Z0-9]+|GT-[A-Z0-9]+", html)
check("blog 有自己的追蹤容器", bool(own), "blog 完全沒有追蹤")
if own:
    print(f"       blog 自有容器：{sorted(set(own))}")

print("\n" + "=" * 58)
print(f"通過 {_pass}｜失敗 {len(_fail)}")
if _fail:
    for n, d in _fail:
        print(f"  ❌ {n}  {d}")
    sys.exit(1)
print("追蹤拓撲符合預期")
