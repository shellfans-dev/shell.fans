# OAuth / 權限範圍 Gap Analysis

**日期**：2026-08-26（2026-08-27 更新：補 API 金鑰／sandbox／scopes 現況）
**觸發**：Is Agentic 稽核（shell.fans，51/100）
**結論**：**不實作**。ShellFans 目前沒有 OAuth 授權伺服器，也不應該為了通過稽核而蓋一個。

---

## 稽核怎麼說

| 項目 | 層級 | 結果 | 稽核原文 |
|---|---|---|---|
| OAuth 2.0 support | Essential | Partial | "OAuth mentioned on homepage but no standard endpoints found" |
| Scoped permissions | Essential | Failed | "No declared OAuth scopes, security schemes, or documentation" |

兩項合計約佔 Essential 分數的 13 分，是目前最大的單一失分來源。

## 「首頁提到 OAuth」是誤判

掃描器抓到的字串來自首頁流程說明的第一步：

```
'flow.step1.tag1': '官方 OAuth' / 'Official OAuth'
'flow.step1.body': '以官方授權連接 IG、Facebook、Threads 等帳號…'
```

語意是：**使用者透過各平台自己的 OAuth 授權 ShellFans 存取其社群帳號**。
ShellFans 在這個關係裡是 **OAuth 用戶端（client）**，不是授權伺服器。

程式碼佐證——全部程式庫中唯一的 OAuth 端點常數是對外部平台的：

```
saas_womm/src/lib/social/threads-graph.ts:16
  const THREADS_OAUTH_BASE = 'https://threads.net/oauth/authorize';
```

沒有任何 `authorization_endpoint`、`token_endpoint`、`jwks_uri` 的實作。

## ShellFans 目前實際的認證模型

| 場景 | 機制 | 面向 |
|---|---|---|
| 使用者登入 console.shell.fans | 帳號密碼 + session（`src/app/api/auth/*`：login / callback / email-verify / forgot-password / change-password） | 人 |
| 使用者連接社群帳號 | 各平台 OAuth，ShellFans 為 client | 人 → 第三方 |
| shellfans-api 管理端點 | 共用密鑰 Bearer（`ADMIN_BEARER_TOKEN`，比對相等） | 機器（內部） |
| kol.fans ↔ shellfans-api 的 chat SSO | HMAC 簽章的 chat token + 跨網域 cookie | 機器（內部） |
| 公開唯讀端點 | 無認證 | 機器（公開） |

這五種都不是 OAuth 授權伺服器。稽核把它們視為等價是錯的——
共用密鑰、session、HMAC token 與 OAuth 的安全模型完全不同。

## 為什麼不現在做

**1. 沒有要授權的東西。**
OAuth 授權伺服器的用途是：讓第三方應用代表使用者存取受保護資源。
ShellFans 目前沒有任何面向第三方的產品資料 API。先蓋授權伺服器，
等於為一扇不存在的門裝鎖。

**2. 假的 scope 比沒有 scope 更危險。**
稽核建議宣告 `profile:read` / `analysis:read` / `reports:read` 之類的範圍。
但後端沒有任何依 scope 做的授權檢查——宣告了卻不強制執行，
會讓整合方以為存取被限縮，實際上沒有。這正是稽核自己寫的
「DO NOT fabricate scopes unsupported by backend authorization」。

**3. 資料本身高度敏感。**
ShellFans 保管的是使用者的社群平台存取權與備份內容。
一個設計不良的授權伺服器等於把這些暴露給第三方應用。
這需要的不只是端點，還有：同意畫面、權杖撤銷、refresh token 輪替、
client 註冊與審核、稽核日誌、資料處理者合約。這是產品專案，不是設定。

**4. 平台條款的限制。**
Meta 與 Threads 的平台政策限制取得的資料能否再轉授權給第三方。
在釐清這一點之前，任何「讓第三方 app 代表使用者讀取 ShellFans 備份」
的設計都可能違反上游條款。

## 若未來要做，最小可行架構

不是現在的工作項，僅記錄方向，避免日後從零討論。

**第一步：唯讀個人資料 API + PKCE Authorization Code**

- 授權伺服器：以 saas_womm 現有 session 為身分來源，新增
  `/oauth/authorize`、`/oauth/token`、`/oauth/revoke`，
  以及 `/.well-known/oauth-authorization-server`（RFC 8414）
- 強制 PKCE（RFC 7636），不支援 implicit flow
- Client 需事前註冊並人工審核；不開放動態註冊
- 存取權杖短效（≤ 15 分鐘）+ refresh token 輪替與重用偵測

**Scope 設計（least privilege，每一個都必須有對應的後端檢查才能宣告）**

| Scope | 涵蓋 | 前置條件 |
|---|---|---|
| `profile:read` | 使用者的帳號基本資料與方案層級 | 需先有使用者資料 API |
| `backup:list` | 列出備份工作與其狀態，不含內容 | 需確認不含第三方個資 |
| `backup:read` | 讀取備份的貼文內容 | **需先釐清 Meta / Threads 平台條款** |
| `aeo:read` | 讀取該使用者網站的 AEO/GEO 掃描結果 | 需先有掃描結果 API |

刻意不設計任何 `:write` scope。第一階段不開放第三方寫入。

**必須先做出的產品決策**

1. 誰可以成為 OAuth client？公開註冊、申請審核、或僅限合作夥伴？
2. 備份內容可否經由 API 交給第三方應用？（法遵問題，非技術問題）
3. 由誰負責 client 審核與權杖濫用的處理流程？
4. 願意承擔的維運成本：授權伺服器是長期資產，不是一次性專案。

## 現況如何對外說明

不假裝有，也不留白讓人猜。`/developers` 明文寫出：

> ShellFans 是第三方 OAuth 的**用戶端**——使用者授權 ShellFans 存取自己的
> Instagram、Facebook、Threads 帳號，走的是各平台自己的 OAuth。ShellFans
> 本身不簽發 OAuth 權杖，沒有 authorization endpoint、沒有 token endpoint，
> 也因此沒有 `/.well-known/oauth-authorization-server`。
>
> 若在別處看到聲稱代表 ShellFans 的 OAuth 端點，那不是 ShellFans。

同樣的聲明也寫進 `/llms.txt` 與 `/openapi.json` 的說明欄位。
對 agent 而言，「明確知道沒有」比「找不到」有價值——前者可以停止探測。

## 對分數的影響

這兩項會**繼續失分**（約 13 分）。這是刻意的取捨：
稽核衡量的是「是否具備 agent 可用的授權機制」，而 ShellFans 的正確答案
目前是「沒有，因為沒有要授權的資源」。用假端點換分數會讓稽核結果變好看，
同時讓真實的整合方被誤導。

---

## 2026-08-27 補充：API 金鑰、scopes 與 sandbox 的現況

新一輪稽核另外指出三項，一併記錄，避免日後被誤讀成「文件說有」。

### API 金鑰：不存在，且目前不需要

稽核寫「free tier and self-service API key generation described but not
fully live-verified」。查證後確認：**ShellFans 從未描述過自助申請 API
金鑰的流程**，站上也沒有任何金鑰申請頁。掃描器可能是把定價頁的「免費版」
與開發者頁的存在合併推論出來的。

現況是公開 API v1 完全不需要憑證，因此沒有金鑰、沒有申請流程、沒有輪替
或撤銷機制。這已明文寫在 `/developers#auth`。

**刻意不先發金鑰。** 發出憑證就等於承擔它的完整生命週期：安全儲存、輪替、
撤銷、洩漏處理、稽核紀錄。在沒有任何端點需要授權的情況下建立這套機制，
只會多出一組要保護的秘密，換不到任何安全性。若未來出現需要授權的端點，
順序會是「先建立生命週期管理，再開放發放」。

### Scopes：沒有可宣告的

沒有面向機器的授權機制，就沒有後端會強制檢查的權限範圍。在 OpenAPI 的
`securitySchemes` 裡宣告 `profile:read` 之類的 scope，而後端完全不檢查，
會讓整合方以為存取被限縮——那是比沒有 scope 更危險的狀態。

`components.securitySchemes` 目前是空物件，`security` 是空陣列。這是準確的
描述，不是遺漏。

### Sandbox：沒有，且目前不需要

公開 API v1 的四個操作全部唯讀、不改變任何狀態、不需憑證。正式環境本身
就可以安全試打，沒有「怕打壞東西」的情境需要沙箱隔離。

建一個假的沙箱網域指回同一份唯讀資料，只是多一個要維護的網址與一個會
過期的說明。若未來有寫入端點，會一併提供沙箱——那時它才有意義。

### 這三項在稽核上的預期

都會**繼續失分**。這是刻意的：稽核衡量的是「是否具備 agent 可用的授權與
上手路徑」，而 ShellFans 目前的正確答案是「不需要，因為公開的東西全部
免憑證唯讀」。用假金鑰、假 scope、假 sandbox 換分數，會讓真實的整合方
被誤導。
