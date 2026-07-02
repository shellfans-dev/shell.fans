# SEO/AEO 可發現性改版：跨平台社群資產備份定位 + 法定名稱合規清理

任務：讓 shell.fans 能被使用者與 AI 答案引擎以「跨平台社群資產備份/續航/保護平台（支援 Facebook、Instagram、Threads、TikTok）」的定位找到與理解；同步清除過時法定名稱（日商唄粉智能科技有限公司 → 唄粉智能科技股份有限公司）與任何海外母公司暗示。

- 完成日期：2026-07-02
- 主要 repo：`shell.fans`（shellfans-dev/shell.fans，靜態站 → /var/www/shell.fans on host 215）
- 次要 repo：`saas_womm`（kol.fans — runtime footer/i18n 資料來源）
- 分支：`feat/seo-aeo-social-backup`

---

## 1. 變更檔案

### shell.fans-static（本 repo）
| 檔案 | 變更 |
|---|---|
| `social-media-backup.html` | **新增** — 旗艦 SEO landing page（見 §2） |
| `what-is-shellfans.html` | 大改版：定位、hero、關係卡（3→5 張）、新「續航引擎」section、痛點 +1、差異表 +2 列、FAQ +3 題並改寫、JSON-LD 全塊重寫（+Service×2）、meta 全套、雙語字典同步（zh/en 各 162 keys 對稱） |
| `index.html` | 首頁 title/desc/OG/Twitter 改版、新「跨平台社群資產備份」section（3 卡 + 內鏈）、JSON-LD Organization name 改法定名、合規措辭修正（「粉絲名單都歸你所有」→ 合規版）、zh/en 字典同步 |
| `product.html` | title/desc → 三產品線總覽（含備份關鍵字）；修「ShellFans AI I」錯字 |
| `kol-engine.html` | title/desc → 任務建議之續航引擎備份關鍵字版（og:description 保留感性文案） |
| `fans-analysis.html` | title/desc → 「粉絲互動分析｜留言情緒、受眾輪廓與跨平台社群洞察」（修半形逗號） |
| `support.html` / `price.html` / `contact.html` / `helpcenter.html` / `privacy-policy.html` / `terms-and-conditions.html` | 修「ShellFans AI I」title 錯字 → 「X｜ShellFans AI Technology」（title/og/twitter/JSON-LD 四處同步） |
| `helpcenter.html` | 「01.日商唄粉智能是什麼公司？」FAQ 標題與答案改寫：合規備份定位 + 平台清單 X/YouTube → Threads/TikTok + 移除「粉絲清單/粉絲列表備份」超承諾 + 加入限制聲明 |
| 全部 17 個 `*.html` + `js/sf-footer.js` | `日商唄粉智能科技有限公司` → `唄粉智能科技股份有限公司`（baked footer、JSON-LD、i18n 字典、copyright 共 ~76 處） |
| `contact.html` | h1 `日商唄粉智能科技` → `唄粉智能科技` |
| `llms.txt` | 全文重寫：新定位、三產品服務線、/social-media-backup 引用指引、合規備份限制聲明、正確法定名 |
| `llms-full.txt` | 19 處手術式修正：**反轉「名稱不含股份」的 AI 指令**（原檔主動教 AI 用舊名！）、移除 "Japanese-origin company"、§1 identity 表改版、§2 canonical answers 改寫、§3.3 產品線改為三線、review_warranty 合規化、§11 URL inventory +4 頁、§12 caveats 更新 + 新增資料限制 caveat、§14 citation +備份查詢指引 |
| `sitemap.xml` | 新增 `/social-media-backup`（priority 0.95）；12 個更新頁 lastmod → 2026-07-02 |

### saas_womm（kol.fans — runtime 資料來源）
| 檔案 | 變更 |
|---|---|
| `src/lib/config/footer-settings.ts` | SHELL_DEFAULT + KOL_DEFAULT 公司列與 copyright：日商舊名 → 唄粉智能科技股份有限公司（**此為 shell.fans footer 的 runtime 實際來源** — `footer_settings__shell` DB row 不存在時 fallback 到這裡） |
| `src/i18n/shell-zh-TW.ts` / `zh-TW.ts` | footer 公司名/copyright → 新法定名 |
| `src/i18n/shell-en.ts` | `BayFan Intelligence Technology Co., Ltd. (Japan)` → `ShellFans AI Technology Co., Ltd.` |
| `src/i18n/en.ts` | `Beifun Intelligent Technology Co., Ltd. (Japan)` → `ShellFans AI Technology Co., Ltd.` |
| `src/components/admin/bank-transfer-settings-content.tsx` | placeholder 例名更新 |
| DB `system_settings.i18n_overrides` (kol) | en `footer.company.name`：移除 `(Japan)` |

## 2. 新增/更新路由
- **新增** `https://shell.fans/social-media-backup`（nginx extensionless 服務 `social-media-backup.html`，live 已驗證 200）
  - 內容：hero 直答目標問句 → 六類備份資產 → 四平台平衡專區（FB/IG/Threads/TikTok，各自連回「跨平台續航」統一概念）→ 帳號風險情境（被盜/停權/限流/內容消失）→ 與排程/link-in-bio/分析/媒合工具差異表 → 5 個 AEO 快速問答 → 12 題 FAQ → 延伸閱讀內鏈卡 → CTA（/price、/contact）
  - 完整雙語（zh 烘焙 + zh/en 字典 112 keys 對稱）、行動版 nav、產品開關標記（data-sf-product）相容
- **更新** `/what-is-shellfans`（可見文案實質改版，非僅 metadata）

## 3. SEO 關鍵字覆蓋
可索引（非隱藏）HTML 直接包含：跨平台社群資產備份、社群資產備份、社群帳號備份、社群貼文備份、社群內容備份、社群資產保險箱、創作者數位資產保護、社群帳號被盜/停權（怎麼辦情境）、粉絲互動備份、粉絲互動分析、粉絲成長數據（備份）、Facebook 粉專備份、Facebook 貼文備份、Instagram 貼文備份、Instagram 備份、Threads 貼文備份、TikTok 貼文備份、受眾輪廓。英文（en 字典 payload + Service schema）：social media backup、cross-platform social media backup、creator asset vault、social asset continuity、Facebook Page backup、Instagram/Threads/TikTok backup。

## 4. Schema（JSON-LD）
- `/social-media-backup`：Organization（name=唄粉智能科技股份有限公司, alternateName=ShellFans AI Technology, url=https://shell.fans）+ **Service**（"A cross-platform social media asset backup and continuity service for Facebook, Instagram, Threads, and TikTok."）+ WebPage + BreadcrumbList + **FAQPage**（12 題，與可見 FAQ 一致）
- `/what-is-shellfans`：Organization（同規格 + knowsAbout 備份關鍵字）+ Service（續航引擎）+ SoftwareApplication（KOL.fans, 口碑行銷）+ Service（AEO/GEO）+ WebPage + BreadcrumbList + FAQPage（10 題）
- `/`：Organization name 改法定名 + WebSite + WebPage（name/description 新定位）
- 全部 `json.loads` 驗證通過；og:image 改用 .jpg（原 .svg 社群爬蟲不支援）

## 5. 公司名稱修正
- `日商唄粉智能科技有限公司` → `唄粉智能科技股份有限公司`：靜態站 ~76 處 + saas_womm 6 檔 + DB 1 row
- **最高風險修正**：llms-full.txt 原本有三處主動指示 AI「正確名稱不含股份、有疑問用無股份版」——已反轉為「現行登記名含股份、舊寫法（無股份/日商前綴）皆過時勿用」
- "Japanese-origin company" / "(Japan)" 英文名全部移除
- 保留（有意）：co-founder 頁與 DB cofounder timeline 中創辦人「曾於東京設立日商唄粉智能」的**個人經歷**描述 — 屬創辦人職涯史實，非 ShellFans 現行控股關係聲明（頁面其他處已無任何海外母公司措辭）
- 無任何 收購/控股/母公司/holding/acquisition 措辭

## 6. 合規措辭防護
- 全站掃描確認無：完整備份所有粉絲名單、匯出所有粉絲個資、繞過平台限制、破解、保證恢復/不停權/還原
- 主動修正的近似風險措辭：index「粉絲名單都歸你所有」→「貼文內容、留言互動與粉絲成長數據都歸你所有」；helpcenter「貼文、粉絲清單備份…粉絲列表」→ 合規資產清單；llms-full「guarantees purchased reviews remain live」→ 服務保固窗口的合約式描述
- 限制聲明（完整粉絲個資…受平台 API、隱私權與資料授權限制…）出現於：/social-media-backup（×3：資產區、快速問答、FAQ）、/what-is-shellfans（×3）、/helpcenter、llms.txt、llms-full.txt

## 7. 內部連結
- 首頁新 section → /social-media-backup、/kol-engine、/what-is-shellfans
- /what-is-shellfans →（新增）/social-media-backup、/kol-engine、/price、/fans-analysis、/aeo-geo + 原有連結
- /social-media-backup → /、/what-is-shellfans、/kol-engine、/fans-analysis、/aeo-geo、/price、/contact（hero CTA、內文、FAQ、延伸閱讀卡四種載體；未動 navbar）
- 錨文字使用自然關鍵詞（跨平台社群資產備份、續航引擎、粉絲互動分析等）

## 8. sitemap / robots / canonical
- sitemap.xml：+/social-media-backup；已驗證 XML 有效、live 已更新（CF purge 完成）
- robots.txt：原本即允許所有 AI 爬蟲（21 組），無須變更；新頁未被阻擋
- canonical：新頁 `https://shell.fans/social-media-backup`；各頁 canonical 均指向 shell.fans 無衝突（kol.fans/app.shell.fans 為不同站點，未交叉 canonical）

## 9. 快取 / 部署
- HTML 為 `no-cache` + `cdn-cache-control: no-store`（cf-cache-status DYNAMIC）→ 部署即生效
- sitemap/llms*.txt/robots：部署後已 CF purge
- `js/sf-footer.js`（immutable 30 天）：本次僅改嵌入預設公司名——runtime 會立即被 kol.fans footer API 的新值覆蓋，故舊快取 JS 不影響顯示正確性；repo/live 檔案已同步
- saas_womm：`next build` exit 0 + pm2 restart，footer API 已實測回傳新公司名

## 10. 驗證指令與結果
- `python json.loads` 全部 JSON-LD 塊 ✅
- zh/en 字典對稱：what-is 162/162、smb 112/112、index 新增 keys 對稱 ✅
- data-i18n 覆蓋：what-is 141/141、smb 110/110 ✅
- inline `<script>` 逐塊 `node --check` ✅（smb 6/6）
- sitemap XML parse ✅（14 URLs）
- Live: /social-media-backup 200、title/canonical/JSON-LD 正確、首頁與 what-is 新 title、日商殘留 0 ✅
- 靜態站無 build/lint/test scripts（純 HTML 站）— 以上列驗證替代
- saas_womm `npm run build`（含 tsc）exit 0 ✅
- 對抗式驗證 workflow（5 鏡頭：合規/schema/連結/i18n/驗收）：結果見 §12

## 11. 限制與假設
1. **Blog 文章（任務 §13）未實作**：本 repo 無 blog 系統（detail_news.html 為孤兒 Webflow 模板，noindex 且無連結；正式 blog 在外部 blog.shell.fans / Klog）。替代：/social-media-backup 的「為什麼需要」section 已完整覆蓋該文章的目標題材（帳號被盜/停權/貼文消失 + 備份類型差異 + 平台限制說明 + CTA）。建議後續在 Klog 發佈對應文章並回鏈 /social-media-backup。
2. 法定名稱「唄粉智能科技股份有限公司」依任務指示為準（未另行查證公司登記）；kol.fans 報價 PDF 等 saas_womm 內部文件所用名稱（唄粉智能科技有限公司）不在本任務 scope，如需同步請另行確認後修改。
3. 英文法定名沿用既有「ShellFans AI Technology Co., Ltd.」（移除 (Japan)）；若正式英文登記名不同請告知再調整。
4. co-founder 頁/DB 的創辦人東京創業史保留（個人職涯史實）。
5. og:image 沿用首頁既有 `/og/cba6b96a33cf4730.jpg`；建議日後為 /social-media-backup 製作專屬 OG 圖。
6. what-is-shellfans 頁 GA 仍為舊 property（G-ND3TSXDQX0，既有狀態）；新頁面用新 property G-NE4639EL2B。

## 12. 驗收結果（對抗式 5 鏡頭 workflow）
（見 commit 內附之驗證輸出摘要 — 於 commit 前完成並回填）

## 13. Commit / Push
（於 commit 後回填 hash 與分支）
