# ShellFans Developer Resources

ShellFans 是內容與服務網站，不是 API 平台。本頁列出目前真正公開、不需憑證即可讀取的機器介面，以及哪些常見的整合方式並不存在——後者同樣寫清楚，讓自動化系統不必靠猜測或反覆探測。


## 現在就能用的公開資源

以下全部不需要 API 金鑰、不需要註冊、不需要 OAuth，直接 GET 即可。

*公開機器可讀資源*


## Markdown 內容協商

公開資訊頁支援內容協商。帶 `Accept: text/markdown` 請求任何一個公開頁面的網址，會拿到同一份內容的 Markdown 版本——沒有導覽列、沒有內嵌 CSS、沒有腳本，只有正文。

以 `/aeo/what-is-aeo` 為例，HTML 約 34 KB 但正文只有約 2.3 KB，其餘 93% 是版面與腳本。Markdown 版直接給正文。

- 網址不變，回應的 `Content-Type` 為 `text/markdown; charset=utf-8`
- 回應帶 `Vary: Accept, Accept-Encoding`
- HTML 版仍為 canonical；Markdown 版不參與搜尋索引
- 沒有 Markdown 版本的頁面會正常回傳 HTML，不會回 404
同一份內容也可以直接用 `.md` 副檔名取得，例如 `https://shell.fans/aeo/what-is-aeo.md`。


## 錯誤格式

所有機器導向的錯誤都是同一個結構。請依 `error.code` 分支，不要比對 `error.message`——後者的文字不保證穩定。

網站路徑不存在時，若請求帶 `Accept: application/json`，會得到帶 discovery 連結的 JSON 而不是 HTML 錯誤頁；帶 `Accept: text/markdown` 則得到 Markdown 版。一般瀏覽器請求仍是原本的 HTML 404 頁。

未知路徑一律回 404。ShellFans 不會把不存在的網址導向首頁，因此「拿到 200」即可視為該頁確實存在。


## 目前不存在的東西（以及為什麼）

這一段刻意寫得明確。對自動化系統而言，「確定沒有」和「有但找不到」是完全不同的兩件事。


### 沒有公開寫入 API

ShellFans 沒有任何可供第三方建立、修改或刪除資料的公開端點，也無法被當成工具呼叫來代替使用者執行工作。OpenAPI 描述中的每一個操作都是 GET。


### 沒有 OAuth 授權伺服器

ShellFans 是第三方 OAuth 的**用戶端**——使用者授權 ShellFans 存取自己的 Instagram、Facebook、Threads 帳號，走的是各平台自己的 OAuth。ShellFans 本身不簽發 OAuth 權杖，沒有 authorization endpoint、沒有 token endpoint，也因此沒有 `/.well-known/oauth-authorization-server`。

若在別處看到聲稱代表 ShellFans 的 OAuth 端點，那不是 ShellFans。


### 沒有 MCP server

ShellFans 目前沒有發布 Model Context Protocol server，也沒有 `/.well-known/mcp` 描述檔。內部產品在某些工作流中**使用** MCP 工具，但那是消費端，不對外提供服務。


### 沒有權限範圍（scopes）

既然沒有面向機器的授權機制，也就沒有可宣告的 scope。任何列出 ShellFans scope 名稱的文件都不是本站發布的。


### ShellFans Chat 不可程式化呼叫

網站上的對話功能只能從網站介面使用。它沒有公開的呼叫端點，因為每一次查詢都會實際觸發語言模型與外部資料來源的成本。匿名使用者的每日額度可以透過 `/api/dify/quota` 讀取（僅供說明，不代表可以自動化消耗）。


## 若你需要目前沒有的東西

上述缺口不是疏漏，是尚未做出的產品與安全決策。若你的整合情境需要其中任何一項，直接說明用途比等待更快——需求會決定優先順序。

- 電子郵件：[hello@shell.fans](mailto:hello@shell.fans)
- 聯絡表單：[聯絡我們](https://shell.fans/contact)
請在來信中說明你要解決的問題與預期的資料流向，不必先設計 API——那部分我們一起討論。


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
**Last-Updated:** 2026-08-26

本檔是 https://shell.fans/developers 的 Markdown 等價版本，供 AI agent 讀取。HTML 版為 canonical，本檔不參與搜尋索引。

> 本檔由 HTML 頁面抽取產生（該頁未使用內容模組）。若與 HTML 有出入，以 canonical HTML 為準。
