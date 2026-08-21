# ClaudeBot 是什麼？

ClaudeBot 是 Anthropic 用來收集公開網頁作為訓練資料的爬蟲。它與負責搜尋索引的 **Claude-SearchBot**、負責使用者即時要求的 **Claude-User** 是不同的 user-agent，用途各異。若目的是被 Claude 引用而非被訓練，需要分開設定。

## Anthropic 的爬蟲家族

*Anthropic 爬蟲用途對照*

| User-agent | 用途 | 備註 |
|---|---|---|
| ClaudeBot | 收集訓練資料 | 最常見於 access log |
| Claude-SearchBot | 搜尋索引 | 影響 Claude 能否在回答中引用你的網站 |
| Claude-User | 使用者當下要求時的即時抓取 | 意圖最明確的一種造訪 |
| anthropic-ai | 早期使用的識別字串 | 部分站台仍會在 robots.txt 中一併列出 |

若不確定站上實際來過哪幾支，最直接的方式是查 access log 而非猜測。

## robots.txt 設定

與 OpenAI 的情況相同，三種常見意圖：

- **全部開放** — 最大化被 Claude 理解與引用的機會。
- **要引用不要訓練** — 擋 ClaudeBot，開放 Claude-SearchBot 與 Claude-User。
- **全部封鎖** — 需清楚理解代價：Claude 使用者將無法從搜尋中找到你。

> 再次提醒：特定 user-agent 群組**不繼承** `User-agent: *`。每一支都要明確寫出規則。詳見 [AI 爬蟲總覽](https://shell.fans/aeo/ai-crawler.md)。

## 確認設定生效

1. 以 `ClaudeBot` 與 `Claude-SearchBot` 分別測試，確認回應狀態。
2. 檢查 CDN／WAF 層是否另有 bot 攔截規則覆蓋了 robots.txt。
3. 比對 access log 與 robots.txt —— 兩者不一致時以 log 為準。
4. 執行 [AEO/GEO 檢測](https://shell.fans/tools/aeo-geo-checker)，AI Crawler Policy 面向會列出實際被擋的爬蟲。

## 常見問題

### ClaudeBot 和 Claude-SearchBot 一定要分開設定嗎？

如果你的意圖是「可以被引用但不想被訓練」，就必須分開。若兩者都要開放或都要封鎖，則規則相同，但仍建議各自明確寫出，避免依賴繼承而出錯。

### 我沒有在 log 裡看到 ClaudeBot，是被擋了嗎？

不一定。爬蟲的造訪頻率取決於網站規模、更新頻率與既有的抓取排程，新站或小站可能本來就少被造訪。先確認 robots.txt 與 WAF 沒有攔截，再觀察一段時間。

### 開放 ClaudeBot 對我有什麼好處？

直接好處是內容有機會進入後續模型版本的訓練語料，讓模型對你的品牌與產品有基礎認識。但這與「被即時引用」是兩件事——後者取決於 Claude-SearchBot。

## 說明

**說明：**本頁內容為 ShellFans 依公開技術文件與實務經驗整理，用於協助網站主理解 AI 搜尋的運作方式。各 AI 平台的實際演算法、資料來源策略與引用邏輯由該平台自行決定且可能隨時調整；任何技術整備都無法保證特定 AI 平台的引用、推薦或排名。

## 相關頁面

- [AI 爬蟲總覽](https://shell.fans/aeo/ai-crawler.md)
- [GPTBot 與 OAI-SearchBot](https://shell.fans/aeo/gptbot-oai-searchbot.md)
- [PerplexityBot](https://shell.fans/aeo/perplexitybot.md)
- [AEO/GEO 知識中心](https://shell.fans/aeo.md)
---

**Canonical:** https://shell.fans/aeo/claudebot
**Brand:** ShellFans AI Technology（唄粉智能科技ShellFans）
**Publisher:** 唄粉智能科技股份有限公司（Taiwan, 統一編號 83032387）
**Last-Updated:** 2026-08-16

本檔是 https://shell.fans/aeo/claudebot 的 Markdown 等價版本，供 AI agent 讀取。HTML 版為 canonical，本檔不參與搜尋索引。
