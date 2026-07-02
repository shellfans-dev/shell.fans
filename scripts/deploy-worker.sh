#!/usr/bin/env bash
# 部署 shell.fans edge Worker（shellfans-product-flags）到 Cloudflare。
#
# 用 multipart metadata 上傳（service-worker 格式）並掛 secret binding：
#   CRAWLER_INGEST_TOKEN ← ~/.crawler-ingest-token（爬蟲監控上報用；
#   同一 token 也設定在 coder1bot saas_womm .env.local）
#
# 需求：~/.cf-global-key（CF Global API Key, kirin@shell.fans）
# 用法：bash scripts/deploy-worker.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKER_JS="$SCRIPT_DIR/../workers/product-flags-rewriter.js"
WORKER_NAME="shellfans-product-flags"

KEY=$(cat ~/.cf-global-key)
EMAIL="kirin@shell.fans"
ACCT=$(curl -s -H "X-Auth-Email: $EMAIL" -H "X-Auth-Key: $KEY" \
  "https://api.cloudflare.com/client/v4/accounts" |
  python3 -c "import sys,json;print(json.load(sys.stdin)['result'][0]['id'])")

TOKEN_FILE="$HOME/.crawler-ingest-token"
if [[ -f "$TOKEN_FILE" ]]; then
  INGEST_TOKEN=$(tr -d '\n' < "$TOKEN_FILE")
  METADATA=$(python3 - "$INGEST_TOKEN" <<'PY'
import json, sys
print(json.dumps({
    "body_part": "script",
    "bindings": [
        {"type": "secret_text", "name": "CRAWLER_INGEST_TOKEN", "text": sys.argv[1]},
    ],
}))
PY
)
else
  echo "!! $TOKEN_FILE 不存在 — Worker 將在無上報 token 的狀態部署（爬蟲監控停用）" >&2
  METADATA='{"body_part":"script","bindings":[]}'
fi

RES=$(curl -s -X PUT \
  -H "X-Auth-Email: $EMAIL" -H "X-Auth-Key: $KEY" \
  -F "metadata=$METADATA;type=application/json" \
  -F "script=@$WORKER_JS;type=application/javascript" \
  "https://api.cloudflare.com/client/v4/accounts/$ACCT/workers/scripts/$WORKER_NAME")

echo "$RES" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if d.get('success'):
    print('worker deployed OK:', d['result'].get('id'))
else:
    print('DEPLOY FAILED:', json.dumps(d.get('errors'), ensure_ascii=False))
    sys.exit(1)
"
