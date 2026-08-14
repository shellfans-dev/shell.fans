# ShellFans AEO Topic Map

日期：2026-08-14　·　產生方式：`scripts/aeo_pages_content.py` 為單一事實來源，本表由該檔產生

狀態說明：**已上線** = 檔案已部署且線上回應 200。

| URL | Topic Cluster | Primary Intent | Funnel | Main Entity | Parent Hub | Related Pages | CTA Target | Schema | 狀態 |
|---|---|---|---|---|---|---|---|---|---|
| `/aeo` | Hub | 導覽 | TOFU | AEO/GEO | — | `/tools/aeo-geo-checker` · `/aeo-geo/methodology` · `/aeo-geo` | `/tools/aeo-geo-checker` | Organization + CollectionPage + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/what-is-aeo` | A. 定義與比較 | 定義 | TOFU | AEO | `/aeo` | `/aeo` · `/aeo/what-is-geo` · `/aeo/aeo-vs-seo` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/what-is-geo` | A. 定義與比較 | 定義 | TOFU | GEO | `/aeo` | `/aeo` · `/aeo/what-is-aeo` · `/aeo/entity-clarity` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/aeo-vs-seo` | A. 定義與比較 | 比較 | TOFU | AEO / SEO | `/aeo` | `/aeo` · `/aeo/what-is-aeo` · `/aeo/answer-readiness` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/aeo-vs-geo` | A. 定義與比較 | 比較 | TOFU | AEO / GEO | `/aeo` | `/aeo` · `/aeo/what-is-geo` · `/aeo/what-is-aeo` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/ai-crawler` | B. 技術權威 | 技術 | MOFU | AI Crawler | `/aeo` | `/aeo` · `/aeo/gptbot-oai-searchbot` · `/aeo/claudebot` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/gptbot-oai-searchbot` | B. 技術權威 | 技術 | MOFU | GPTBot / OAI-SearchBot | `/aeo` | `/aeo/ai-crawler` · `/aeo/claudebot` · `/aeo/perplexitybot` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/claudebot` | B. 技術權威 | 技術 | MOFU | ClaudeBot | `/aeo` | `/aeo/ai-crawler` · `/aeo/gptbot-oai-searchbot` · `/aeo/perplexitybot` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/perplexitybot` | B. 技術權威 | 技術 | MOFU | PerplexityBot | `/aeo` | `/aeo/ai-crawler` · `/aeo/answer-readiness` · `/aeo/gptbot-oai-searchbot` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/llms-txt` | B. 技術權威 | 技術 | MOFU | llms.txt | `/aeo` | `/aeo/llms-full-txt` · `/aeo/ai-crawler` · `/aeo-geo/methodology` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/llms-full-txt` | B. 技術權威 | 技術 | MOFU | llms-full.txt | `/aeo` | `/aeo/llms-txt` · `/aeo` · `/aeo-geo/methodology` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/schema` | B. 技術權威 | 技術 | MOFU | Schema.org | `/aeo` | `/aeo/faq-schema` · `/aeo/entity-clarity` · `/aeo-geo/methodology` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/faq-schema` | B. 技術權威 | 技術 | MOFU | FAQPage | `/aeo` | `/aeo/schema` · `/aeo/answer-readiness` · `/aeo-geo/methodology` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/entity-clarity` | B. 技術權威 | 技術 | MOFU | Entity Clarity | `/aeo` | `/aeo/trust-signals` · `/aeo/what-is-geo` · `/aeo/schema` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/answer-readiness` | B. 技術權威 | 技術 | MOFU | Answer Readiness | `/aeo` | `/aeo/faq-schema` · `/aeo/aeo-vs-seo` · `/aeo-geo/methodology` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/trust-signals` | B. 技術權威 | 技術 | MOFU | Trust Signals | `/aeo` | `/aeo/entity-clarity` · `/aeo/what-is-geo` · `/aeo-geo/methodology` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/managed-hosting` | D. 商業服務 | 商業 | BOFU | AEO Managed Hosting | `/aeo` | `/aeo-geo` · `/aeo/cost` · `/aeo/implementation` | `/tools/aeo-geo-checker` | Organization + Service + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/consulting` | D. 商業服務 | 商業 | BOFU | AEO Consulting | `/aeo` | `/aeo/managed-hosting` · `/aeo/cost` · `/aeo/how-to-choose-agency` | `/contact` | Organization + Service + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/cost` | E. 採購與比較 | 採購 | BOFU | AEO Pricing | `/aeo` | `/aeo/implementation` · `/aeo/managed-hosting` · `/aeo/how-to-choose-agency` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/implementation` | E. 採購與比較 | 採購 | MOFU | AEO Implementation | `/aeo` | `/aeo/cost` · `/aeo/managed-hosting` · `/aeo/ai-crawler` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/taiwan-companies` | E. 採購與比較 | 採購 | BOFU | 台灣 AEO 服務商 | `/aeo` | `/aeo/how-to-choose-agency` · `/aeo/aeo-agency-vs-seo-agency` · `/aeo-geo/taiwan-aeo-tools` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/how-to-choose-agency` | E. 採購與比較 | 採購 | BOFU | AEO Agency Selection | `/aeo` | `/aeo/taiwan-companies` · `/aeo/aeo-agency-vs-seo-agency` · `/aeo/cost` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |
| `/aeo/aeo-agency-vs-seo-agency` | A. 定義與比較 | 比較 | MOFU | AEO Agency / SEO Agency | `/aeo` | `/aeo/how-to-choose-agency` · `/aeo/taiwan-companies` · `/aeo/aeo-vs-seo` | `/tools/aeo-geo-checker` | Organization + TechArticle + BreadcrumbList + FAQPage | 已上線 |

## 既有頁面（本次補強內部連結，未改內容）

| URL | 角色 | 本次異動 |
|---|---|---|
| `/aeo-geo` | AEO/GEO 商業 hub（BOFU） | sf-inline-links 追加指向 `/aeo` |
| `/aeo-geo/methodology` | AI Readiness Score 方法論（canonical） | sf-inline-links 追加指向 `/aeo` |
| `/aeo-geo/taiwan-aeo-tools` | 台灣 AEO 工具比較 | sf-inline-links 追加指向 `/aeo` |
| `/tools/aeo-geo-checker` | 檢測工具（WebApplication） | sf-inline-links 追加指向 `/aeo` |
| `/what-is-shellfans` | 品牌實體 hub | 新增「延伸閱讀」區塊，3 條指向知識叢集 |

## 連結拓撲

```
/what-is-shellfans ─┐
                    ├──► /aeo (hub) ──► 22 個子頁
/aeo-geo ───────────┤         ▲
/aeo-geo/methodology┤         │ 每個子頁 related 皆回指 hub 或同群頁面
/aeo-geo/taiwan-... ┤         │
/tools/aeo-geo-...──┘         │
                              ▼
        子頁 CTA ──► /tools/aeo-geo-checker（檢測）
                 └──► /aeo-geo（服務）或 /contact（顧問）
```

錨文字刻意每頁不同 —— 全站同一句錨文字會讓這批連結看起來像機器批次產生。

## 尚未建立（第二批）

| URL | 群組 | 未做原因 |
|---|---|---|
| `/aeo/geo-vs-seo` | A | 非 P0/P1 |
| `/aeo/how-ai-search-works` | A | 非 P0/P1 |
| `/aeo/answer-engine-optimization-guide` | A | 非 P0/P1，且與 hub 有重疊風險 |
| `/aeo/organization-schema` 等 3 頁 | B | 與 `/aeo/schema` 重疊，需先確認切分方式 |
| `/aeo/agency`、`/aeo/consultant`、`/aeo/in-house-vs-agency`、`/aeo/tools-vs-service` | E | 非 P0/P1 |
| `/solutions/aeo/*`（7 頁） | F | 需真實產業案例，目前僅 1 家 AEO 客戶，強做會變虛構 |
| `/ai-readiness/*`（8 頁） | C | **刻意不做** —— 會與 `/aeo-geo/methodology` 重複，見稽核文件第 5 節 |
| `/aeo/service`、`/aeo/website-hosting`、`/aeo/audit`、`/aeo/pricing` | D | 與既有頁面同義，只會 cannibalize |

