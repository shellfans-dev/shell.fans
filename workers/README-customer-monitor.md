# 客戶站台爬蟲監控 — 部署說明

把 `customer-crawler-monitor.js` 部署到**客戶自己的 Cloudflare zone**，
爬蟲到訪資料會回到 `console.shell.fans` 後台的
`/_shellfans-admin712/aeo-geo?tab=crawler`。

## 為什麼是 Worker 而不是主機 agent

| | Worker（邊緣） | agent 讀 origin log |
|---|---|---|
| CF 快取命中的請求 | 看得到 | **看不到**（請求沒到 origin） |
| 真實 client IP | `cf-connecting-ip` | 只有 CF 邊緣 IP |
| 能否驗證真假爬蟲 | 可以（rDNS / IP-range） | **不行**，全部只能標 unsupported |
| 客戶主機負擔 | 零 | 需常駐服務 |

`robots.txt`、`sitemap.xml`、`llms.txt` 這些 AEO 最該監控的路徑最常被 CDN 快取，
所以 origin-side 採集會系統性低估。主機 agent 的定位是採集**主機層指標**
（憑證到期、磁碟、服務存活…），不是取代這支 Worker。

若客戶站台沒有掛任何 CDN，agent 讀 origin log 才是唯一選項；此時 origin log
有真實 IP，驗證層反而可以正常運作。

## 前置作業

1. 在 ShellFans 後台 → AEO/GEO → 爬蟲監控 → 站台管理，新增站台
   （`site_key`、主要網域、採集模式選 `edge`、CDN 選 `cloudflare`）
2. 發一張 **edge** 憑證，複製明文（只會顯示這一次）

## 需要客戶提供什麼

只需要**客戶 Cloudflare 帳號的 Workers 部署權限**，不需要 DNS 或 WAF 權限。
兩種做法：

- 請客戶把 ShellFans 加為該帳號成員（角色至少含 Workers 編輯）
- 或請客戶自行執行下列指令，我們只提供程式碼與 token

## 部署指令

```bash
# 在客戶的 CF 帳號下
npx wrangler init shellfans-crawler-monitor --no-git
# 以 customer-crawler-monitor.js 覆蓋 src/index.js

npx wrangler secret put SHELLFANS_INGEST_TOKEN   # 貼上後台發的 edge 憑證
npx wrangler deploy
```

`wrangler.toml` 路由設定：

```toml
name = "shellfans-crawler-monitor"
main = "src/index.js"
compatibility_date = "2026-01-01"

[[routes]]
pattern = "example.com/*"
zone_name = "example.com"

[[routes]]
pattern = "www.example.com/*"
zone_name = "example.com"
```

## 驗證

部署後打一次站台，後台應在數秒內出現紀錄：

```bash
curl -A 'GPTBot/1.0' https://www.example.com/robots.txt
```

後台 → AEO/GEO → 爬蟲監控 → 切到該站台，應看到一筆
`declared_bot_name=GPTBot`、`verification_status=spoof_suspected`
（因為來源不是 OpenAI 官方 IP —— 這是正確行為，代表驗證層有在運作）。

## 注意事項

- **CF 免費方案的 Workers 為每日 10 萬次請求**。部署前先確認客戶流量規模，
  超量會影響 Worker 執行。
- 被 WAF 規則擋掉的流量不會進到 Worker，因此不會出現在監控中。
- 這支 Worker 只觀察不改寫：不動回應內容、不設 cookie、不影響快取行為。
  上報失敗一律靜默，不影響客戶站台服務。
- token 外洩時，後端會擋掉 host 不屬於該站的事件，但仍應盡快到後台撤銷並重發。
