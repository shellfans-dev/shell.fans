# AI 爬蟲有哪些？robots.txt 該怎麼設定

AI 爬蟲不是只有一種。同一家公司通常有多支爬蟲，分別負責「訓練資料收集」與「即時搜尋索引」，兩者用途不同，擋錯的後果也不同。更關鍵的是：robots.txt 中特定 user-agent 的規則**不會**繼承 `User-agent: *`，這是最常見也最致命的設定錯誤。

## 主要 AI 爬蟲一覽

*主要 AI 爬蟲與用途*

| User-agent | 所屬 | 用途 |
|---|---|---|
| GPTBot | OpenAI | 訓練資料收集 |
| OAI-SearchBot | OpenAI | ChatGPT 搜尋索引 —— 擋掉會直接影響 ChatGPT 搜尋結果 |
| ChatGPT-User | OpenAI | 使用者當下要求時的即時抓取 |
| ClaudeBot | Anthropic | 訓練資料收集 |
| Claude-SearchBot | Anthropic | 搜尋索引 |
| Claude-User | Anthropic | 使用者當下要求時的即時抓取 |
| PerplexityBot | Perplexity | 搜尋索引 |
| Perplexity-User | Perplexity | 使用者當下要求時的即時抓取 |
| Googlebot | Google | 搜尋索引 —— **AI Overviews 也使用這支** |
| Google-Extended | Google | Gemini 訓練用途的控制項，**不影響 AI Overviews** |
| Applebot-Extended | Apple | Apple Intelligence 訓練控制項 |
| CCBot | Common Crawl | 公開語料庫，被多個模型間接使用 |
| Bytespider | ByteDance | 訓練資料收集 |

> **特別注意 Google 這兩支的區別。**擋掉 `Google-Extended` 只會退出 Gemini 的訓練用途，**不會**讓你從 AI Overviews 消失——AI Overviews 走的是 Googlebot。反過來說，擋掉 Googlebot 會同時失去一般搜尋與 AI Overviews，代價極大。

## 最常見的致命錯誤

### robots.txt 的群組不會繼承

這是規格中明確定義但最常被誤解的一點：當 robots.txt 中存在針對特定 user-agent 的群組時，**該群組完全不繼承 `User-agent: *` 的規則**。

也就是說，下面這段設定的實際效果，可能與作者的預期完全相反：

- `User-agent: *` 下寫 `Allow: /`
- 另外為 `GPTBot` 開一個群組，只寫了 `Disallow: /private`
- 結果：GPTBot 的群組沒有 `Allow: /`，但因為只有 Disallow 特定路徑，其餘仍可抓 —— 這個例子還好。
- **但如果** GPTBot 群組寫成 `Disallow: /`，就是全站封鎖，而 `*` 的 Allow 完全不會救它。

因此建議**對每一支要開放的爬蟲明確寫出規則**，不要依賴繼承。shell.fans 自己的 [robots.txt](https://shell.fans/robots.txt) 就是這樣寫的，可以直接參考。

### 其他常見問題

- **用 WAF 或 CDN 規則擋掉 AI 爬蟲卻忘了。**robots.txt 寫了 Allow，但 Cloudflare 的 Bot Fight Mode 直接回 403 —— 爬蟲根本讀不到 robots.txt。這種情況檢測工具只會看到連線失敗。
- **只擋訓練爬蟲，卻連搜尋爬蟲一起擋。**想退出訓練是合理的商業決定，但 GPTBot 與 OAI-SearchBot 要分開處理，否則會連 ChatGPT 搜尋的曝光一起失去。
- **robots.txt 回 404 或 500。**沒有 robots.txt 通常視為全部允許，但伺服器錯誤的行為則不一定，應該確保它穩定回 200。

## 怎麼驗證設定真的生效

1. 直接以該 user-agent 送出請求，確認回應是 200 而非 403。
2. 檢查 CDN／WAF 層是否有獨立的 bot 規則覆蓋了 robots.txt 的意圖。
3. 查看伺服器 access log，確認這些爬蟲實際有來訪、取得什麼狀態碼。
4. 用 [AEO/GEO 檢測工具](https://shell.fans/tools/aeo-geo-checker) 做一次整體檢查，其中 AI Crawler Policy 面向（10 分）會列出被誤擋的爬蟲。

> **log 比設定檔誠實。**robots.txt 寫什麼是意圖，access log 記錄的才是實際發生的事。兩者不一致時，永遠以 log 為準去找中間哪一層攔截了。

## 常見問題

### 擋掉 AI 爬蟲會影響一般搜尋排名嗎？

要看擋哪一支。擋 GPTBot、ClaudeBot、PerplexityBot 不影響 Google 搜尋排名。但擋 Googlebot 會同時失去一般搜尋與 AI Overviews。Google-Extended 是獨立的訓練控制項，擋掉不影響搜尋或 AI Overviews。

### 我不想被拿去訓練，但想被 AI 搜尋引用，可以嗎？

可以。多數業者把訓練與搜尋分成不同的 user-agent，例如 OpenAI 的 GPTBot（訓練）與 OAI-SearchBot（搜尋）、Anthropic 的 ClaudeBot（訓練）與 Claude-SearchBot（搜尋）。分別設定即可。

### robots.txt 擋了，AI 就一定抓不到嗎？

不保證。robots.txt 是一項自願遵循的協定，主要業者公開表示遵守，但不排除有不遵守的爬蟲。若有嚴格需求，需要在伺服器或 WAF 層做實際的存取控制，而非只靠 robots.txt。

### 要不要開放 CCBot？

取決於你對「內容被納入公開語料庫」的態度。CCBot 蒐集的 Common Crawl 語料被多個模型間接使用，開放有助於被更多系統認識，但也意味著內容進入一份公開資料集。這是商業判斷，沒有技術上的標準答案。

## 說明

**說明：**本頁內容為 ShellFans 依公開技術文件與實務經驗整理，用於協助網站主理解 AI 搜尋的運作方式。各 AI 平台的實際演算法、資料來源策略與引用邏輯由該平台自行決定且可能隨時調整；任何技術整備都無法保證特定 AI 平台的引用、推薦或排名。

## 相關頁面

- [AEO/GEO 知識中心](https://shell.fans/aeo.md)
- [GPTBot 與 OAI-SearchBot](https://shell.fans/aeo/gptbot-oai-searchbot.md)
- [ClaudeBot](https://shell.fans/aeo/claudebot.md)
- [PerplexityBot](https://shell.fans/aeo/perplexitybot.md)
---

**Canonical:** https://shell.fans/aeo/ai-crawler
**Brand:** ShellFans AI Technology（唄粉智能科技ShellFans）
**Publisher:** 唄粉智能科技股份有限公司（Taiwan, 統一編號 83032387）
**Last-Updated:** 2026-08-16

本檔是 https://shell.fans/aeo/ai-crawler 的 Markdown 等價版本，供 AI agent 讀取。HTML 版為 canonical，本檔不參與搜尋索引。
