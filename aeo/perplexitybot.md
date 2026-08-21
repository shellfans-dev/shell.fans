# PerplexityBot 是什麼？

PerplexityBot 是 Perplexity 用於建立搜尋索引的爬蟲。由於 Perplexity 的回答會明確標註來源連結並可點擊，被不被索引對實際流量的影響比其他答案引擎更直接——擋掉它，等於放棄這個管道的全部曝光。

## 為什麼 Perplexity 值得單獨關注

Perplexity 的產品形態與其他答案引擎有一個明顯差異：它在回答旁邊列出編號來源，使用者可以直接點擊前往。這代表被引用不只是品牌曝光，還可能帶來實際的造訪。

相對地，若 PerplexityBot 被擋，損失是完整的——不會有「雖然沒被索引但還是被提到」的中間狀態。

## 兩支爬蟲

*Perplexity 爬蟲對照*

| User-agent | 用途 | 擋掉的後果 |
|---|---|---|
| PerplexityBot | 建立搜尋索引 | 無法出現在 Perplexity 的來源清單中 |
| Perplexity-User | 使用者當下要求時的即時抓取 | 使用者主動指定你的網址也讀不到 |

## 除了開放之外還能做什麼

被抓到只是最低門檻。要提高被列為來源的機會，內容形狀比爬蟲設定更關鍵：

- **段落要能單獨成立**——Perplexity 引用的是段落而非整頁。詳見 [答覆整備度](https://shell.fans/aeo/answer-readiness.md)。
- **事實要具體可查證**——含有明確數字、日期、規格的段落比形容詞堆疊更容易被選為來源。
- **標題要直接對應問題**——「AEO 費用怎麼算」比「關於我們的服務」更容易對上使用者的查詢。
- **實體要清楚**——來源標註需要能辨識出「這是誰說的」。見 [實體清晰度](https://shell.fans/aeo/entity-clarity.md)。

## 常見問題

### 被 Perplexity 引用會帶來流量嗎？

有機會，因為 Perplexity 的來源標註是可點擊的連結。但實際點擊率取決於回答是否已充分滿足使用者、你的來源排在第幾個等因素，無法保證。

### 要怎麼知道自己有沒有被 Perplexity 引用？

目前沒有官方的查詢介面。可行做法是固定一組代表真實查詢情境的問題，定期在 Perplexity 上詢問並記錄來源清單中是否出現你的網域。單次結果不足以判斷，需累積觀測。

### Perplexity 和 Google AI Overviews 的爬蟲一樣嗎？

不一樣。Perplexity 使用 PerplexityBot，Google AI Overviews 使用 Googlebot。兩者是獨立的系統，robots.txt 需分別設定。

## 說明

**說明：**本頁內容為 ShellFans 依公開技術文件與實務經驗整理，用於協助網站主理解 AI 搜尋的運作方式。各 AI 平台的實際演算法、資料來源策略與引用邏輯由該平台自行決定且可能隨時調整；任何技術整備都無法保證特定 AI 平台的引用、推薦或排名。

## 相關頁面

- [AI 爬蟲總覽](https://shell.fans/aeo/ai-crawler.md)
- [答覆整備度](https://shell.fans/aeo/answer-readiness.md)
- [GPTBot 與 OAI-SearchBot](https://shell.fans/aeo/gptbot-oai-searchbot.md)
- [免費檢測工具](https://shell.fans/tools/aeo-geo-checker)
---

**Canonical:** https://shell.fans/aeo/perplexitybot
**Brand:** ShellFans AI Technology（唄粉智能科技ShellFans）
**Publisher:** 唄粉智能科技股份有限公司（Taiwan, 統一編號 83032387）
**Last-Updated:** 2026-08-16

本檔是 https://shell.fans/aeo/perplexitybot 的 Markdown 等價版本，供 AI agent 讀取。HTML 版為 canonical，本檔不參與搜尋索引。
