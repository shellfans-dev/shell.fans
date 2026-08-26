#!/usr/bin/env python3
"""
Agent 介面的端到端測試。針對線上站台執行，不需要憑證。

涵蓋本次 agentic readiness 工作改動的每一項行為：
  1. 未知路徑回真 404（含依 Accept 的三種變體）
  2. 既有路由沒有回歸
  3. Markdown 內容協商雙向正確，且 Vary 標頭存在
  4. openapi.json 可取得、合法、且每個宣告的端點實際回應符合 schema
  5. 公開 API 的錯誤是結構化 JSON
  6. 管理端點仍然關閉
  7. Organization JSON-LD 帶齊 address / contactPoint
  8. 信任錨點頁可達
  9. llms.txt 有 when-to-use 段落

用法：
    python3 scripts/test-agentic-surface.py            # 針對 https://shell.fans
    python3 scripts/test-agentic-surface.py --base http://127.0.0.1:8899
"""

import json
import re
import sys
import urllib.error
import urllib.request

BASE = 'https://shell.fans'
CONSOLE = 'https://console.shell.fans'
UA = 'ShellFansAgenticTest/1.0'

for i, arg in enumerate(sys.argv):
    if arg == '--base' and i + 1 < len(sys.argv):
        BASE = sys.argv[i + 1]

_failures = []
_passes = 0


def get(url, accept=None, method='GET'):
    req = urllib.request.Request(url, method=method)
    req.add_header('User-Agent', UA)
    if accept:
        req.add_header('Accept', accept)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def check(name, actual, expected):
    global _passes
    if actual == expected:
        _passes += 1
        print(f'  ✅ {name}')
    else:
        _failures.append((name, expected, actual))
        print(f'  ❌ {name}\n       期望 {expected!r}\n       實際 {actual!r}')


def check_true(name, cond, detail=''):
    check(name, bool(cond) or detail, True)


# --------------------------------------------------------------------------
print('\n### 1. 未知路徑回真 404')
for path in ['/some-path-that-does-not-exist', '/aeo/no-such-topic', '/aeo/', '/a/b/c']:
    st, _, _ = get(BASE + path)
    check(f'{path} → 404', st, 404)

st, h, body = get(BASE + '/nope', accept='application/json')
check('404 JSON 變體狀態碼', st, 404)
check('404 JSON 變體型別', h.get('Content-Type', '').split(';')[0], 'application/json')
try:
    doc = json.loads(body)
    check('404 JSON 有 error.code', doc['error']['code'], 'RESOURCE_NOT_FOUND')
    check_true('404 JSON 指向 sitemap', 'sitemap' in json.dumps(doc))
except Exception as e:
    check('404 JSON 可解析', str(e), '無例外')

st, h, _ = get(BASE + '/nope', accept='text/markdown')
check('404 Markdown 變體', (st, h.get('Content-Type', '')), (404, 'text/markdown; charset=utf-8'))

st, _, _ = get(BASE + '/404.json')
check('/404.json 不可直接取得', st, 404)

# --------------------------------------------------------------------------
print('\n### 2. 既有路由未回歸')
ROUTES_200 = [
    '/', '/aeo', '/aeo-geo', '/aeo-geo/methodology', '/aeo/cost', '/product',
    '/pricing', '/price', '/contact', '/privacy-policy', '/terms-and-conditions',
    '/what-is-shellfans', '/helpcenter', '/support', '/co-founder', '/endurance',
    '/fans-analysis', '/social-media-backup', '/tools/aeo-geo-checker',
    '/sitemap.xml', '/robots.txt', '/llms.txt', '/llms-full.txt',
    '/aeo/cost.md', '/manifest.webmanifest', '/about', '/developers', '/openapi.json',
]
bad = []
for path in ROUTES_200:
    st, _, _ = get(BASE + path)
    if st != 200:
        bad.append((path, st))
check(f'{len(ROUTES_200)} 條既有/新增路由皆 200', bad, [])

MIME = {
    '/': 'text/html', '/sitemap.xml': 'text/xml', '/robots.txt': 'text/plain',
    '/llms.txt': 'text/plain', '/aeo/cost.md': 'text/markdown',
    '/openapi.json': 'application/json', '/manifest.webmanifest': 'application/manifest+json',
    '/css/shellfans-v2.webflow.css': 'text/css',
    '/js/sf-footer.js': 'application/javascript',
    '/images/nav_logo.svg': 'image/svg+xml',
}
bad = []
for path, want in MIME.items():
    _, h, _ = get(BASE + path)
    got = h.get('Content-Type', '').split(';')[0]
    if got != want:
        bad.append((path, want, got))
check('靜態資產 MIME 型別正確', bad, [])

# --------------------------------------------------------------------------
print('\n### 3. Markdown 內容協商')
for path in ['/', '/aeo/cost', '/aeo-geo', '/what-is-shellfans']:
    st, h, body = get(BASE + path, accept='text/markdown')
    check(f'{path} markdown', (st, h.get('Content-Type', '')),
          (200, 'text/markdown; charset=utf-8'))
    check_true(f'{path} markdown 內容是 Markdown', body.decode('utf-8').lstrip().startswith('#'))

st, h, _ = get(BASE + '/aeo/cost', accept='text/html')
check('/aeo/cost html', (st, h.get('Content-Type', '')), (200, 'text/html; charset=utf-8'))

BROWSER = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,*/*;q=0.8'
_, h, _ = get(BASE + '/aeo/cost', accept=BROWSER)
check('瀏覽器 Accept 不誤觸協商', h.get('Content-Type', ''), 'text/html; charset=utf-8')

_, h, _ = get(BASE + '/aeo/cost')
vary = h.get('Vary', '')
check_true('Vary 含 Accept', 'Accept' in vary and 'Accept-Encoding' in vary, vary)

# 沒有 .md 的頁面必須回退到 HTML，不能 404
_, h, _ = get(BASE + '/product', accept='text/markdown')
check('無 .md 的頁面回退 HTML', h.get('Content-Type', ''), 'text/html; charset=utf-8')

# --------------------------------------------------------------------------
print('\n### 4. OpenAPI 與實際回應一致')
st, h, body = get(BASE + '/openapi.json')
check('openapi.json 可取得', st, 200)
spec = json.loads(body)
check('OpenAPI 版本', spec['openapi'], '3.1.0')

ops = [(p, m, o) for p, ms in spec['paths'].items() for m, o in ms.items()]
ids = [o['operationId'] for _, _, o in ops]
check('operationId 唯一', len(ids), len(set(ids)))
check_true('每個 operation 有 summary 與 description',
           all(o.get('summary') and o.get('description') for _, _, o in ops))
check_true('operationId 皆為簡短識別字（函式呼叫相容）',
           all(re.fullmatch(r'[a-z][A-Za-z0-9]{2,39}', i) for i in ids), ids)
check_true('公開端點不需授權', all(o.get('security') == [] for _, _, o in ops))
check_true('沒有任何寫入操作', all(m == 'get' for _, m, _ in ops))

for path, _, op in ops:
    server = op['servers'][0]['url']
    st, h, body = get(server + path)
    ctype = h.get('Content-Type', '').split(';')[0]
    ok = st == 200 and ctype == 'application/json'
    try:
        doc = json.loads(body)
    except Exception:
        ok = False
        doc = None
    check(f'{op["operationId"]} 實際回應 200 JSON', ok, True)
    # 宣告 required 的頂層欄位必須真的存在
    schema = op['responses']['200']['content']['application/json']['schema']
    ref = schema.get('$ref', '').split('/')[-1]
    resolved = spec['components']['schemas'].get(ref, {})
    req = resolved.get('required', [])
    if doc is not None and req:
        missing = [k for k in req if k not in doc]
        check(f'{op["operationId"]} required 欄位齊全', missing, [])

# --------------------------------------------------------------------------
print('\n### 5. 公開 API 的錯誤是結構化 JSON')
st, h, body = get(BASE + '/api/dify/definitely-not-a-route')
check('未知 API 路徑 404', st, 404)
check('錯誤型別為 JSON', h.get('Content-Type', '').split(';')[0], 'application/json')
doc = json.loads(body)
check('錯誤 code', doc['error']['code'], 'RESOURCE_NOT_FOUND')
check_true('錯誤含 hint', bool(doc['error'].get('hint')))

# --------------------------------------------------------------------------
print('\n### 6. 非公開端點仍然關閉')
for path, want in [('/api/dify/cache/stats', 401), ('/api/dify/admin/audit-log', 401)]:
    st, h, body = get(BASE + path)
    check(f'{path} → {want}', st, want)
    check(f'{path} 錯誤為 JSON', h.get('Content-Type', '').split(';')[0], 'application/json')
    check(f'{path} 未洩漏內容', b'hit_rate' in body or b'reason_counts' in body, False)

# --------------------------------------------------------------------------
print('\n### 7. Organization 結構化資料')
_, _, body = get(BASE + '/')
html = body.decode('utf-8')
org = None
for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
    data = json.loads(block)
    for node in (data.get('@graph', [data]) if isinstance(data, dict) else data):
        if isinstance(node, dict) and node.get('@type') == 'Organization':
            org = node
check_true('首頁有 Organization 節點', org is not None)
if org:
    for field in ('name', 'url', 'logo', 'sameAs', 'contactPoint', 'address', 'foundingDate'):
        check(f'Organization.{field} 存在', field in org, True)
    check('address 型別', org['address']['@type'], 'PostalAddress')
    check('contactPoint 型別', org['contactPoint'][0]['@type'], 'ContactPoint')

check('首頁恰有一個 h1', html.count('<h1'), 1)

# --------------------------------------------------------------------------
print('\n### 8. llms.txt')
_, h, body = get(BASE + '/llms.txt')
txt = body.decode('utf-8')
check_true('有 When to use 段落', '## When to use ShellFans' in txt)
check_true('有 Do not 段落', 'Do not recommend ShellFans when' in txt)
check_true('指向 /developers', '/developers' in txt)
check_true('指向 /openapi.json', 'openapi.json' in txt)

# --------------------------------------------------------------------------
print(f'\n{"=" * 58}')
print(f'通過 {_passes}｜失敗 {len(_failures)}')
if _failures:
    for name, exp, act in _failures:
        print(f'  ❌ {name}: 期望 {exp!r}, 實際 {act!r}')
    sys.exit(1)
print('全部通過')
