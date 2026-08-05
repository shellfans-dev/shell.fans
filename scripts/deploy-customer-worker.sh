#!/usr/bin/env bash
# 部署 ShellFans 客戶站台爬蟲監控 Worker 到「客戶自己的 Cloudflare zone」。
#
# 與 deploy-worker.sh（自家 shell.fans）的差別：
#   - 使用 ES module 格式上傳（main_module），因為客戶版 Worker 用 env binding
#   - 憑證與 zone 都來自客戶帳號，故以參數帶入，不寫死
#
# 用法：
#   CF_EMAIL_FILE=~/.cf-bearspace-email \
#   CF_KEY_FILE=~/.cf-bearspace-key \
#   INGEST_TOKEN_FILE=~/.cet-ingest-token \
#   bash scripts/deploy-customer-worker.sh cet-taiwan.com "cet-taiwan.com/*" "www.cet-taiwan.com/*"
#
# 安全提醒：Global API Key 權限涵蓋整個帳號。長期運作建議改用 scoped API token
# （僅 Workers Scripts:Edit + Workers Routes:Edit），把權限縮到最小。
set -euo pipefail

ZONE_NAME="${1:?請提供 zone 名稱，例：cet-taiwan.com}"
shift
ROUTES=("$@")
[[ ${#ROUTES[@]} -gt 0 ]] || { echo "請至少提供一條 route，例：'www.example.com/*'" >&2; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKER_JS="$SCRIPT_DIR/../workers/customer-crawler-monitor.js"
WORKER_NAME="${WORKER_NAME:-shellfans-crawler-monitor}"

EMAIL=$(tr -d '\n' < "${CF_EMAIL_FILE:?請設定 CF_EMAIL_FILE}")
KEY=$(tr -d '\n' < "${CF_KEY_FILE:?請設定 CF_KEY_FILE}")
INGEST_TOKEN=$(tr -d '\n' < "${INGEST_TOKEN_FILE:?請設定 INGEST_TOKEN_FILE}")

api() { curl -s -H "X-Auth-Email: $EMAIL" -H "X-Auth-Key: $KEY" "$@"; }

echo "→ 查詢 zone $ZONE_NAME"
ZONE_JSON=$(api "https://api.cloudflare.com/client/v4/zones?name=$ZONE_NAME")
ZONE_ID=$(python3 -c "import sys,json;r=json.load(sys.stdin)['result'];print(r[0]['id'] if r else '')" <<<"$ZONE_JSON")
ACCT_ID=$(python3 -c "import sys,json;r=json.load(sys.stdin)['result'];print(r[0]['account']['id'] if r else '')" <<<"$ZONE_JSON")
[[ -n "$ZONE_ID" ]] || { echo "找不到 zone $ZONE_NAME（憑證是否屬於該帳號？）" >&2; exit 1; }
echo "   zone_id=$ZONE_ID account_id=$ACCT_ID"

echo "→ 上傳 Worker $WORKER_NAME（ES module + secret binding）"
METADATA=$(python3 - "$INGEST_TOKEN" <<'PY'
import json, sys
print(json.dumps({
    "main_module": "worker.js",
    "compatibility_date": "2026-01-01",
    "bindings": [
        {"type": "secret_text", "name": "SHELLFANS_INGEST_TOKEN", "text": sys.argv[1]},
    ],
}))
PY
)

# 回應以 stdin 交給 python，避免內容含換行/引號時破壞字串內插
api -X PUT \
  "https://api.cloudflare.com/client/v4/accounts/$ACCT_ID/workers/scripts/$WORKER_NAME" \
  -F "metadata=$METADATA;type=application/json" \
  -F "worker.js=@$WORKER_JS;filename=worker.js;type=application/javascript+module" \
| python3 -c "
import sys, json
d = json.load(sys.stdin)
if not d.get('success'):
    print('❌ 上傳失敗:', json.dumps(d.get('errors'), ensure_ascii=False)); raise SystemExit(1)
print('   ✓ 已上傳')
"

for R in "${ROUTES[@]}"; do
  echo "→ 設定 route $R"
  api -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/workers/routes" \
    -H 'content-type: application/json' \
    --data "$(python3 -c "import json,sys;print(json.dumps({'pattern':sys.argv[1],'script':sys.argv[2]}))" "$R" "$WORKER_NAME")" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
if d.get('success'):
    print('   ✓ 已建立')
else:
    errs = d.get('errors') or []
    # 10020 = route 已存在（重跑腳本時視為正常）
    if any(e.get('code') == 10020 for e in errs):
        print('   ✓ 已存在，略過')
    else:
        print('   ❌', json.dumps(errs, ensure_ascii=False)); raise SystemExit(1)
"
done

echo
echo "✓ 部署完成。驗證："
echo "  curl -A 'GPTBot/1.0' https://${ROUTES[0]%/*}/robots.txt"
echo "  後台 → AEO/GEO → 爬蟲監控 → 選該站台"
