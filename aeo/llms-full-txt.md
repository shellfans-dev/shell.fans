# llms-full.txt 是什麼？

llms-full.txt 是 llms.txt 的延伸版本，放在同一個位置（`/llms-full.txt`），提供更完整的內容而非僅是索引。簡單的分法：**llms.txt 是目錄，llms-full.txt 是內容**。多數網站先做好前者即可，後者屬於選配。

## 兩者的分工

*llms.txt 與 llms-full.txt 的差異*

| 項目 | llms.txt | llms-full.txt |
|---|---|---|
| 角色 | 索引與導覽 | 完整內容 |
| 長度 | 數十行 | 數百行以上 |
| 內容 | 品牌定位 + 重要頁面連結與說明 | 關鍵頁面的實際內容、細節、規格、常見問答 |
| 維護成本 | 低，內容變動時才更新 | 較高，需與網站內容同步 |
| 優先順序 | **先做這個** | 有餘力再做 |

## 什麼情況值得做

不是所有網站都需要。以下情況投入才划算：

- **內容分散在很多頁**，模型要理解全貌得抓很多次。集中成一份可降低這個成本。
- **有大量規格、參數、條件**需要精確傳達，而這些散落在不同頁面。
- **常見誤解多**，需要在一個地方一次講清楚「我們不是什麼」。

反之，若網站只有十幾頁且結構清楚，llms.txt 加上良好的頁面結構就足夠了，多做一份 llms-full.txt 只是增加維護負擔。

## 維護成本與風險

> **最大的風險是內容過期。**llms-full.txt 與網站內容不同步時，你等於同時對外提供兩個版本的事實。模型讀到舊版本，可能產生比沒有這份檔案更糟的結果——因為錯誤資訊看起來很正式。

因此建議：

1. 在檔案開頭標註最後更新日期，讓讀取者能判斷時效。
2. 把「更新 llms-full.txt」納入內容變更的流程，而不是想到才改。
3. 若無法保證同步，**寧可不做**。一份準確的 llms.txt 勝過一份過期的 llms-full.txt。

## 常見問題

### 一定要兩個都做嗎？

不用。llms.txt 是基礎，llms-full.txt 是選配。若無法確保 llms-full.txt 與網站內容同步更新，建議只做 llms.txt——過期的完整版比沒有更糟。

### llms-full.txt 要多長？

沒有規定長度。原則是「讀完能正確理解這個網站」，而不是「越長越好」。把不重要的內容塞進去只會稀釋重點。

### 可以自動產生嗎？

技術上可以，但要小心。自動彙整容易把導覽列、頁尾、重複區塊一起帶入，產生大量雜訊。若要自動化，需要先定義好抽取規則並人工檢查結果。

## 說明

**說明：**本頁內容為 ShellFans 依公開技術文件與實務經驗整理，用於協助網站主理解 AI 搜尋的運作方式。各 AI 平台的實際演算法、資料來源策略與引用邏輯由該平台自行決定且可能隨時調整；任何技術整備都無法保證特定 AI 平台的引用、推薦或排名。

## 相關頁面

- [llms.txt](https://shell.fans/aeo/llms-txt.md)
- [AEO/GEO 知識中心](https://shell.fans/aeo.md)
- [AI Readiness Score 方法論](https://shell.fans/aeo-geo/methodology)
- [免費檢測工具](https://shell.fans/tools/aeo-geo-checker)
---

**Canonical:** https://shell.fans/aeo/llms-full-txt
**Brand:** ShellFans AI Technology（唄粉智能科技ShellFans）
**Publisher:** 唄粉智能科技股份有限公司（Taiwan, 統一編號 83032387）
**Last-Updated:** 2026-08-16

本檔是 https://shell.fans/aeo/llms-full-txt 的 Markdown 等價版本，供 AI agent 讀取。HTML 版為 canonical，本檔不參與搜尋索引。
