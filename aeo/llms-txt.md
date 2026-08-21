# llms.txt 是什麼？該不該做？

llms.txt 是一份放在網站根目錄的 Markdown 檔案（`/llms.txt`），用簡潔的結構告訴大型語言模型「這個網站是什麼、重要頁面在哪裡」。它由 llmstxt.org 提出，**目前是社群提案而非正式標準**，也沒有任何主要 AI 業者公開承諾一定會讀取它。

## 先講最重要的一件事

> **llms.txt 目前不是標準。**它是 llmstxt.org 提出的社群提案，尚未有任何主要 AI 業者公開承諾會讀取或依此調整行為。任何宣稱「做了 llms.txt 就會被 ChatGPT 引用」的說法都不成立。

把這點先說清楚，是因為這個主題目前充斥著誇大宣稱。以下的建議都建立在「它可能有用、成本很低」這個前提上，而不是「它一定有用」。

## 它實際長什麼樣子

llms.txt 是一份 Markdown 檔案，慣例的結構是：

- `#` 一級標題：網站或品牌名稱
- `>` 引言區塊：一段話說清楚這個網站是什麼
- `##` 二級標題分區：核心服務、重要頁面、常見問題等
- 每個項目以 `[標題](網址)` 加一句說明，讓模型知道該頁回答什麼問題

可以直接看 shell.fans 自己的 [/llms.txt](https://shell.fans/llms.txt) 作為範例，以及延伸版本 [/llms-full.txt](https://shell.fans/llms-full.txt)（見 [llms-full.txt 說明](https://shell.fans/aeo/llms-full-txt.md)）。

## 為什麼還是建議做

即使不確定 AI 業者是否讀取，仍有三個實際理由：

1. **成本極低。**一份檔案、幾十行，一次寫完長期受用。與其他 AEO 工作相比，投入幾乎可以忽略。
2. **撰寫過程本身有價值。**要寫出這份摘要，你必須先想清楚「我們到底是什麼、哪些頁面最重要、每頁回答什麼問題」。這個釐清過程通常會直接暴露網站結構上的問題。
3. **下檔風險為零。**它不影響 SEO、不影響使用者、不佔資源。即使最終沒有任何模型讀取，也沒有損失。

在 [AI Readiness Score](https://shell.fans/aeo-geo/methodology) 中，llms.txt 面向配分 5 分——這個相對低的權重正反映了它「有用但非決定性」的定位。

## 怎麼寫才有意義

### 該寫的

- **實體關係要明確**：品牌、法人、產品線之間是什麼關係。這是模型最容易搞混的部分。
- **每個連結要說明它回答什麼問題**，而不只是列出標題。
- **寫出「不是什麼」**。明確排除常見誤解（例如「這不是 XX 平台」）比只講自己是什麼更有幫助。
- **標註更新日期**，讓讀取者知道資訊的時效。

### 不該寫的

- **關鍵字堆疊**。這份檔案是給模型讀的摘要，不是關鍵字清單。
- **把整站內容複製進來**。那是 llms-full.txt 的用途，兩者要分工。
- **誇大或無法驗證的宣稱**。若與網站實際內容不符，反而製造矛盾訊號。

## 常見問題

### llms.txt 是官方標準嗎？

不是。它是 llmstxt.org 提出的社群提案，尚未成為正式標準，也沒有主要 AI 業者公開承諾遵循。應該把它視為「低成本、可能有幫助」的選項，而非必要條件。

### 做了 llms.txt，ChatGPT 就會讀嗎？

沒有任何業者公開保證會讀取。建議做的理由是成本極低、撰寫過程能釐清網站結構，以及沒有下檔風險，而不是因為有明確效果保證。

### llms.txt 和 robots.txt 有什麼不同？

robots.txt 規範「能不能抓」，是有明確規格且被主要業者遵循的協定；llms.txt 提供「這個網站是什麼」的摘要，是尚未標準化的提案。兩者用途不同，不能互相取代。

### 放在哪裡？

網站根目錄，也就是 https://你的網域/llms.txt。與 robots.txt 相同層級。

## 說明

**說明：**本頁內容為 ShellFans 依公開技術文件與實務經驗整理，用於協助網站主理解 AI 搜尋的運作方式。各 AI 平台的實際演算法、資料來源策略與引用邏輯由該平台自行決定且可能隨時調整；任何技術整備都無法保證特定 AI 平台的引用、推薦或排名。

## 相關頁面

- [llms-full.txt](https://shell.fans/aeo/llms-full-txt.md)
- [AI 爬蟲總覽](https://shell.fans/aeo/ai-crawler.md)
- [AI Readiness Score 方法論](https://shell.fans/aeo-geo/methodology)
- [免費檢測工具](https://shell.fans/tools/aeo-geo-checker)
---

**Canonical:** https://shell.fans/aeo/llms-txt
**Brand:** ShellFans AI Technology（唄粉智能科技ShellFans）
**Publisher:** 唄粉智能科技股份有限公司（Taiwan, 統一編號 83032387）
**Last-Updated:** 2026-08-16

本檔是 https://shell.fans/aeo/llms-txt 的 Markdown 等價版本，供 AI agent 讀取。HTML 版為 canonical，本檔不參與搜尋索引。
