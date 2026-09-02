# ShellFans Developer Documentation

ShellFans 是內容與服務網站，不是 API 平台。本頁列出目前真正公開、不需憑證即可讀取的機器介面，以及哪些常見的整合方式並不存在——後者同樣寫清楚，讓自動化系統不必靠猜測或反覆探測。

整理者：**ShellFans AI Technology**（唄粉智能科技股份有限公司）　·　更新於 2026-08-27


## 公開 API（v1）

四個唯讀端點，全部 GET、不需要憑證、不回傳任何個人資料，基底網址 `https://shell.fans/api/v1`。完整機器可讀描述見 [openapi.json](https://shell.fans/openapi.json)（OpenAPI 3.1，所有回應型別完整展開，可直接轉成 LLM 工具定義）。

*公開 API v1 操作*

先前這些資料分散在 shell.fans 與 console.shell.fans 兩個網域，靠 OpenAPI 的 operation-level `servers` 描述。該欄位在工具鏈中支援度很差——多數轉換器直接取頂層 `servers[0]`，導致六個操作有四個會打錯主機拿到 404。v1 收斂到單一主機與單一版本前綴之後不再有這個問題。


## 認證

**公開 API 不需要也不接受任何認證。**沒有 API 金鑰、沒有 OAuth 授權伺服器、沒有權限範圍（scopes）。送 `Authorization` 標頭不會有任何作用。


### ShellFans 在認證關係中的角色

- **第三方 OAuth 的用戶端**——使用者授權 ShellFans 存取自己的 Instagram、Facebook、Threads 帳號，走的是各平台自己的 OAuth。
- **Session 認證的網頁應用**——console.shell.fans 用帳號密碼加 session。
- **共用密鑰**——內部管理端點用 Bearer 權杖，不對外開放。
ShellFans **不是** OAuth 授權伺服器，也不是 OIDC provider，不對第三方簽發權杖。因此沒有 `/.well-known/oauth-authorization-server`——發布一份描述不存在端點的中繼資料，只會讓照著做的整合方全部失敗。

若在別處看到聲稱代表 ShellFans 的 OAuth 端點或 API 金鑰發放頁，那不是 ShellFans。目前沒有自助申請金鑰的流程，因為公開 API 不需要金鑰。


## 速率限制

每個呼叫端位址每 60 秒 120 次請求。每一個回應（含錯誤）都會帶標頭：

- `RateLimit-Limit`　視窗內允許的請求數
- `RateLimit-Remaining`　本視窗剩餘次數
- `RateLimit-Reset`　距離視窗重置的秒數
- `RateLimit-Policy`　政策，格式為 `120;w=60`
超過額度回 `429`，帶 `Retry-After` 標頭與 RFC 9457 錯誤主體，其中 `retry_after` 欄位是同一個秒數。

這個額度與網站對話功能的每日額度是分開的兩個桶子。讀取公開資料不會消耗使用者的對話次數——兩者是語意不同的資源。


## 錯誤格式

所有錯誤都是 **RFC 9457 Problem Details**，媒體型別 `application/problem+json`。公開 API 路徑永遠不會回傳 HTML 錯誤頁。

*錯誤欄位*

可能出現的 `code` 值：`BAD_REQUEST`、`UNAUTHORIZED`、`FORBIDDEN`、`RESOURCE_NOT_FOUND`、`METHOD_NOT_ALLOWED`、`VALIDATION_FAILED`、`RATE_LIMIT_EXCEEDED`、`UPSTREAM_UNAVAILABLE`、`INTERNAL_ERROR`。

網站頁面（非 API 路徑）的 404 仍然是給人看的 HTML，但若請求帶 `Accept: application/json` 或 `Accept: text/markdown`，會改回對應格式的結構化回應。


## 版本政策

目前的穩定版本是 **v1**，路徑前綴 `/api/v1/`。


### 什麼算是破壞性變更

- 移除端點，或移除回應中的既有欄位
- 改變既有欄位的型別或語意
- 把選填的請求參數改成必填
- 為既有錯誤情境改用不同的 `code`

### 什麼不算

- 新增端點
- 在回應中新增欄位——請以「未知欄位可忽略」的方式解析
- 新增可選的請求參數
- 修正 `title` 或 `detail` 的措辭

### 破壞性變更如何處理

- 推出新的主要版本（`/api/v2/`），舊版繼續運作
- 舊版回應開始帶 `Deprecation: true` 與 `Sunset: <HTTP-date>` 標頭，以及 `Link: <…>; rel="successor-version"`
- 自公告日起舊版至少維持 **180 天**
- 公告會同步更新 openapi.json、本頁與 llms.txt
目前**沒有任何端點被標示為 deprecated**。v1 的回應不帶 `Deprecation` 或 `Sunset` 標頭——沒有實際要淘汰的東西就不該送出淘汰訊號。


## 其他機器可讀資源

*不需憑證即可讀取*


### Markdown 內容協商

帶 `Accept: text/markdown` 請求任何公開頁面的網址，會拿到同一份內容的 Markdown 版本——沒有導覽列、沒有內嵌 CSS、沒有腳本。網址不變，回應帶 `Vary: Accept, Accept-Encoding`。也可以直接加 `.md` 副檔名。


## 目前不存在的東西（以及為什麼）

這一段刻意寫得明確。對自動化系統而言，「確定沒有」和「有但找不到」是完全不同的兩件事。


### 沒有公開寫入 API

沒有任何可供第三方建立、修改或刪除資料的公開端點，也無法被當成工具呼叫來代替使用者執行工作。OpenAPI 中每一個操作都是 GET。


### 沒有 API 金鑰或自助申請流程

公開 API 不需要金鑰，因此也沒有申請、輪替或撤銷的流程。若未來出現需要授權的端點，會先建立完整的憑證生命週期管理再開放，不會先發金鑰再補機制。


### 沒有沙箱環境

公開 API 全部唯讀且不會改變任何狀態，正式環境本身就可以安全試打。未來若有寫入端點，會一併提供沙箱。


### 沒有 OAuth 授權伺服器與 scopes

見上方[認證](https://shell.fans/developers#auth)一節。沒有面向機器的授權機制，就沒有可宣告的權限範圍。任何列出 ShellFans scope 名稱的文件都不是本站發布的。


### 沒有 MCP server

ShellFans 沒有發布 Model Context Protocol server，也沒有 `/.well-known/mcp` 描述檔。內部產品在某些工作流中**使用** MCP 工具，但那是消費端，不對外提供服務。

npm 上的 `@shell-mcp/core` **不是 ShellFans 的套件**。它屬於 psdlabs，是一個 shell/terminal session 的 MCP server，與本公司無關。名稱相近純屬巧合。


### ShellFans Chat 不可程式化呼叫

網站上的對話功能只能從網站介面使用。它沒有公開的呼叫端點，因為每一次查詢都會實際觸發語言模型與外部資料來源的成本。


## 若你需要目前沒有的東西

上述缺口不是疏漏，是尚未做出的產品與安全決策。若你的整合情境需要其中任何一項，直接說明用途比等待更快。

- 電子郵件：[hello@shell.fans](mailto:hello@shell.fans)
- 聯絡表單：[聯絡我們](https://shell.fans/contact)

## 常見問題


### ShellFans 有 API 可以串接嗎？

有少數公開唯讀端點，描述於 /openapi.json，不需授權即可讀取，內容是站台設定、方案資料與公司識別資訊。但沒有產品資料 API，也沒有任何寫入端點。


### 可以用 OAuth 登入 ShellFans 取得資料嗎？

不行。ShellFans 沒有 OAuth 授權伺服器，不對第三方簽發權杖。ShellFans 只在使用者授權存取其社群帳號時，作為各平台 OAuth 的用戶端。


### ShellFans 有 MCP server 嗎？

沒有。ShellFans 目前未發布任何 Model Context Protocol server，也沒有 /.well-known/mcp。內部工作流會使用 MCP 工具，但不對外提供。


### 要怎麼取得頁面的純文字版本？

對任何公開頁面的網址加上 Accept: text/markdown 標頭，或直接在網址後面加 .md。回傳的是去除版面與腳本的正文，HTML 版仍為 canonical。


### 未知的網址會回什麼？

404。ShellFans 不會把不存在的路徑導向首頁。若請求帶 Accept: application/json，回應會是含 sitemap、llms.txt 等指引連結的 JSON。

本頁描述的是撰寫當下實際存在的公開介面。ShellFans 不保證這些端點的長期穩定性或版本相容性，內容欄位屬編輯資料，可能隨時調整。

相關頁面：[關於 ShellFans](https://shell.fans/about.md)　·　[ShellFans 是什麼](https://shell.fans/what-is-shellfans.md)　·　[llms.txt 是什麼](https://shell.fans/aeo/llms-txt.md)　·　[AI 爬蟲總覽](https://shell.fans/aeo/ai-crawler.md)　·　[聯絡我們](https://shell.fans/contact)

---

**Canonical:** https://shell.fans/developers
**Brand:** ShellFans AI Technology（唄粉智能科技ShellFans）
**Publisher:** 唄粉智能科技股份有限公司（Taiwan, 統一編號 83032387）
**Last-Updated:** 2026-08-27

本檔是 https://shell.fans/developers 的 Markdown 等價版本，供 AI agent 讀取。HTML 版為 canonical，本檔不參與搜尋索引。

> 本檔由 HTML 頁面抽取產生（該頁未使用內容模組）。若與 HTML 有出入，以 canonical HTML 為準。
