# Refine CET Taiwan AEO Case Study
# 師德文教 CET AEO Case Study 文案與閱讀體驗重構

Target page: https://shell.fans/aeo/case-studies/cet-taiwan

PRIMARY OBJECTIVE: Rewrite and restructure this page so it reads like a
professional, evidence-based AEO case study rather than a technical audit report.

（完整 prompt 內容見 git 歷史；本檔為 2026-09-08 執行的重構任務指示。
核心約束：所有已驗證數值不得變動、不得捏造流量／招生／營收／轉換數據、
敘事順序改為 context → what we changed → what AI started doing → evidence →
interpretation → remaining gap → methodology／limitations。）

主要步驟：
 1  檢查現有實作，保留 canonical／JSON-LD／sitemap／內部連結／analytics
 2  改變敘事：從技術報告改為給企業主與行銷負責人閱讀
 3  新 Hero：師德文教 CET：從 AI 可讀性整備到 AI 引用的 AEO 專案紀錄
 4  頂部加「目前觀察到的變化」指標卡（僅同一量測條件的數據）
 5  移除裝飾性英文區塊標籤
 6  重排章節為十段敘事流程
 7  技術細節（h1/h2/h3 計數、JSON-LD 節點數）收進「技術驗證」
 8  凸顯核心洞察：第一階段能不能取得 → 第二階段會不會歸因
 9  平台比較改用「不同的品牌歸因模式」而非「方向相反」
10  模型變更說明壓縮，細節收進 <details>
11  指標首次出現時給簡短定義
12  爬蟲語句改寫得更清楚
13  404 宣稱必須查證並補上脈絡，否則移除
14  說明目標頁進入引用來源的意義
15  加回「下一階段：從被引用走向被歸因」
16  減少免責聲明重複，集中到「怎麼解讀這些數據」
17  精簡 FAQ
18  語氣：專業、有把握、易讀，避免生硬用語
19  自然涵蓋 AEO 相關查詢意圖，不堆砌關鍵字
20  JSON-LD 與可見內容一致，FAQPage 需與實際 FAQ 相符
21  最終以讀者視角通讀並修正

驗證：HTTP 200、單一 H1、title／meta／canonical、原始 HTML 可讀、
JSON-LD、FAQ schema 一致、內部連結、行動版、無內容退化、
所有數值與驗證來源相符。
