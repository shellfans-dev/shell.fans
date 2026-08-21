# AEO 需要哪些 Schema？

對 AEO 而言真正關鍵的結構化資料只有少數幾種：**Organization**（你是誰）、**FAQPage**（可直接擷取的問答）、**BreadcrumbList**（內容層級）、以及依業務型態選用的 **Service** 或 **Product**。加上與頁面內容不符的 schema 不會加分，反而製造矛盾訊號。

## 優先順序

*AEO 相關 Schema 類型的優先順序*

| 類型 | 優先度 | 用途與注意事項 |
|---|---|---|
| Organization | **必要** | 定義品牌實體。應包含 name、url、logo，並盡量補上可驗證的 address、telephone、identifier。這是 [實體清晰度](https://shell.fans/aeo/entity-clarity.md) 的核心。 |
| WebSite | 建議 | 宣告站台層級的資訊，與 Organization 建立關聯。 |
| BreadcrumbList | 建議 | 讓模型理解頁面在網站結構中的位置。深層頁面尤其重要。 |
| FAQPage | **高價值** | 結構化的問答最容易被擷取為答案。但**必須與頁面上實際可見的內容一致**。詳見 [FAQ Schema](https://shell.fans/aeo/faq-schema.md)。 |
| Service | 視業務 | 服務型業務適用。可標註 serviceType、areaServed、provider。 |
| Product | 視業務 | 有明確商品時適用。不要為了加而加。 |
| TechArticle / Article | 視內容 | 知識型內容適用，可標註 author、publisher、datePublished。 |
| WebApplication | 視產品 | 線上工具適用。 |

## 實作原則

### 一、用 JSON-LD，不要用 Microdata

JSON-LD 與 HTML 內容分離，維護容易且不會影響版面。目前是主流建議做法。

### 二、用 @graph 把節點串起來

同一頁的多個 schema 節點放在一個 `@graph` 陣列中，並用 `@id` 建立引用關係，比散落成多個獨立 script 標籤更能表達「這些是同一件事的不同面向」。

### 三、標註的必須是頁面上真的有的東西

這是最容易出錯的地方。FAQPage 標了五個問題，但頁面上只看得到三個——這是不一致，不但沒有幫助，還可能被視為操弄。**結構化資料是既有內容的機器可讀版本，不是額外的宣傳欄位。**

### 四、驗證能否被解析

JSON 語法錯誤會讓整段 schema 完全失效，而且從頁面外觀上完全看不出來。每次修改後都應該實際 parse 一次確認。

## 常見錯誤

- **把 Organization 重複宣告在每一頁但內容不一致**。名稱、logo、地址應該完全相同，不一致會直接削弱實體訊號。
- **為了「多一點 schema」而加上不適用的類型**。例如純知識文章加 Product。
- **FAQPage 的答案寫得像廣告**。答案應該直接回答問題，不是行銷文案。
- **JSON 語法錯誤未被發現**。少一個逗號整段就失效，頁面外觀卻毫無異狀。
- **用 schema 描述頁面上沒有的內容**。這是最嚴重的一類，等同於對機器與對人說不同的話。

[AI Readiness Score](https://shell.fans/aeo-geo/methodology) 的 Structured Data 面向（15 分）會檢查 JSON-LD 是否存在、Organization 是否具備，以及頁面若含 FAQ 文案是否對應建立 FAQPage。

## 常見問題

### 加越多 schema 越好嗎？

不是。與頁面內容不符的 schema 不會加分，還可能產生矛盾訊號。原則是：頁面上有的東西才標註，且標註內容要與可見內容一致。

### JSON-LD 和 Microdata 選哪個？

建議 JSON-LD。它與 HTML 分離，維護容易、不影響版面，且是目前主流的建議做法。既有的 Microdata 不必急著移除，但新增時用 JSON-LD。

### Schema 加了就會被 AI 引用嗎？

不會。結構化資料的作用是讓模型更容易正確理解頁面內容，屬於必要條件之一。是否被引用還取決於內容本身的品質、可擷取性與該領域的其他來源。

### 怎麼確認 schema 沒寫錯？

最基本的是確認 JSON 可以被正確解析——語法錯誤會讓整段失效但外觀完全正常。之後再確認標註的內容與頁面可見內容一致。

## 說明

**說明：**本頁內容為 ShellFans 依公開技術文件與實務經驗整理，用於協助網站主理解 AI 搜尋的運作方式。各 AI 平台的實際演算法、資料來源策略與引用邏輯由該平台自行決定且可能隨時調整；任何技術整備都無法保證特定 AI 平台的引用、推薦或排名。

## 相關頁面

- [FAQ Schema](https://shell.fans/aeo/faq-schema.md)
- [實體清晰度](https://shell.fans/aeo/entity-clarity.md)
- [AI Readiness Score 方法論](https://shell.fans/aeo-geo/methodology)
- [免費檢測工具](https://shell.fans/tools/aeo-geo-checker)
---

**Canonical:** https://shell.fans/aeo/schema
**Brand:** ShellFans AI Technology（唄粉智能科技ShellFans）
**Publisher:** 唄粉智能科技股份有限公司（Taiwan, 統一編號 83032387）
**Last-Updated:** 2026-08-16

本檔是 https://shell.fans/aeo/schema 的 Markdown 等價版本，供 AI agent 讀取。HTML 版為 canonical，本檔不參與搜尋索引。
