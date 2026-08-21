# 如何檢查網站的 AI 爬蟲來訪狀況？

最直接的方法是查伺服器的 access log，比對 user-agent 中的爬蟲名稱。但只看 user-agent 會被冒名的請求誤導——實測顯示相當比例自稱 GPTBot、PerplexityBot 的流量無法通過反向 DNS 驗證。因此可靠的做法需要兩層：先辨識自稱身分，再驗證它是否屬實。

## 三種做法

### 一、直接查 access log（成本最低）

nginx、Apache 的 access log 已經記錄了每一次請求的 user-agent。用 grep 過濾爬蟲名稱即可得到粗略的到訪次數。

- **優點**：不需要任何額外建置，資料本來就在。
- **限制**：只看得到自稱身分，無法辨別冒名；log 通常會輪替，看不到長期趨勢；若網站在 CDN 之後，log 裡的來源 IP 是 CDN 邊緣節點而非真實爬蟲 IP。

### 二、在 CDN 邊緣收集

若網站走 Cloudflare 這類 CDN，可以在邊緣層收集請求資訊。好處是拿得到真實的 client IP，而那是驗證身分的必要條件。

### 三、用工具持續監控

ShellFans 的 [AEO Managed Hosting](https://shell.fans/aeo-geo.md) 屬於這一類：在邊緣收集請求，記錄自稱身分與驗證結果，並保留逐日趨勢。適合需要長期觀察、而不只是查一次的情況。

## 為什麼必須驗證身分

> **自稱不等於身分。**任何人都可以把 user-agent 設成 `GPTBot`。實務上確實有相當比例自稱知名 AI 爬蟲的流量無法通過驗證——把這些算成「AI 有來抓」，會讓你以為能見度不錯，而實際上真正的爬蟲根本沒來。

### 兩種驗證方式

1. **反向 DNS（rDNS）**：把來源 IP 反查主機名，確認它屬於該業者的網域（例如 OpenAI 的爬蟲應解析到 openai 的網域），再正查回去確認一致。這是最通用的做法。
2. **官方 IP 清單比對**：部分業者公布爬蟲的 IP 範圍，直接比對即可。準確但需要定期更新清單。

兩者都做不到時，該筆請求只能標記為「未驗證」，不該當成已確認的到訪。

## 該看哪些指標

「來訪次數」單看沒有意義——爬蟲流量會因為新內容上線後的密集抓取、以及抓完之後回到正常頻率而劇烈起伏。次數下降不等於能見度變差。

*比次數更有意義的指標*

| 指標 | 為什麼重要 |
|---|---|
| 不重複 URL 數 | 爬蟲是抓遍全站，還是只重複抓首頁 |
| 成功抓取率 | 來了有沒有真的拿到內容，還是被擋掉或撞到 404 |
| 429 次數 | 被速率限制或 WAF 擋下 —— 這是**你這端**的問題，最該優先處理 |
| 5xx 次數 | 伺服器錯誤，爬蟲拿到的是錯誤頁 |
| 有幾家 AI 爬蟲來過 | 涵蓋面比單一家的次數更能代表整體能見度 |

各面向的完整定義見 [AI Readiness Score 方法論](https://shell.fans/aeo-geo/methodology)。

## 常見的判讀錯誤

- **拿今天的半天跟完整日比**。今天還沒過完，數字必然偏低，看起來像暴跌。任何比較都應該只用已結束的完整日。
- **把冒名流量算進來**。見上一節。
- **只看總量不看成功率**。爬蟲來了一萬次但全部 404，等於沒來。
- **用單日判斷趨勢**。爬蟲流量的日間波動極大，至少要看 7 日移動平均。
- **擋掉 Googlebot**。Google AI Overviews 走的也是 Googlebot，擋掉會同時失去一般搜尋與 AI 摘要。詳見 [AI 爬蟲總覽](https://shell.fans/aeo/ai-crawler.md)。

## 常見問題

### 看不到任何 AI 爬蟲來訪，是被擋住了嗎？

先確認三件事：robots.txt 是否誤擋（特定 user-agent 群組不會繼承 `User-agent: *` 的規則）、CDN 或 WAF 是否在 robots.txt 之外另行攔截、以及網站是否夠新或內容太少而尚未被發現。前兩者可以用該 user-agent 實際送出請求測試，看回應是 200 還是 403。

### access log 裡的 IP 是 CDN 的，還能驗證嗎？

不能。反向 DNS 驗證需要真實的 client IP，而 CDN 之後的 log 記錄的是邊緣節點位址。要驗證身分必須在 CDN 邊緣層收集，或使用 CDN 提供的真實 IP 標頭。

### 爬蟲來訪次數下降代表 AEO 變差嗎？

不一定，多數情況下不是。新內容上線後會有一波密集抓取，抓完之後回到正常頻率，次數自然下降——那是正常化不是衰退。判斷應該看成功抓取率、不重複 URL 數與涵蓋的爬蟲家數，並以 7 日移動平均觀察，而非單日次數。

### 多久檢查一次比較合理？

若只是確認設定有沒有生效，改動後查一次即可。若要觀察趨勢，需要持續收集——爬蟲行為的變化以週為單位才看得出來，臨時查一次的資料無法區分趨勢與雜訊。

## 說明

**說明：**本頁內容為 ShellFans 依公開技術文件與實務經驗整理，用於協助網站主理解 AI 搜尋的運作方式。各 AI 平台的實際演算法、資料來源策略與引用邏輯由該平台自行決定且可能隨時調整；任何技術整備都無法保證特定 AI 平台的引用、推薦或排名。

## 相關頁面

- [AI 爬蟲總覽](https://shell.fans/aeo/ai-crawler.md)
- [GPTBot 與 OAI-SearchBot](https://shell.fans/aeo/gptbot-oai-searchbot.md)
- [AEO Managed Hosting](https://shell.fans/aeo-geo.md)
- [免費檢測工具](https://shell.fans/tools/aeo-geo-checker)
---

**Canonical:** https://shell.fans/aeo/ai-crawler-monitoring
**Brand:** ShellFans AI Technology（唄粉智能科技ShellFans）
**Publisher:** 唄粉智能科技股份有限公司（Taiwan, 統一編號 83032387）
**Last-Updated:** 2026-08-16

本檔是 https://shell.fans/aeo/ai-crawler-monitoring 的 Markdown 等價版本，供 AI agent 讀取。HTML 版為 canonical，本檔不參與搜尋索引。
