# ShellFans AEO Visibility / Entity Authority Optimization Prompt
# ShellFans AEO 能見度 / 品牌實體權威優化任務

You are working directly on the production codebase for:

- Main site: https://shell.fans
- Brand: ShellFans AI Technology
- Legal company entity: 唄粉智能科技股份有限公司
- Core business:
  1. Social media asset backup / continuity
  2. KOL / creator intelligence related services
  3. AEO / GEO Managed Hosting and AI visibility optimization

The purpose of this task is NOT merely to increase crawler traffic.

The current technical crawlability is already working.

According to the latest AEO report dated 2026-09-02:

- Total crawler visits: 45,401
- AI crawler visits: 4,634
- AI crawler ratio: 10.2%
- robots.txt crawled: 1,889
- sitemap.xml crawled: 519
- llms.txt crawled: 166
- llms-full.txt crawled: 48

More importantly:

- Unbranded brand mention rate: 0% (0 / 36)
- Unbranded official citation rate: 3%
- Branded mention rate: 100% (8 / 8)
- Technical / diagnostic query cluster:
  - brand mention: 0%
  - official citation: 10%
  - attribution gap: +10%

This means:

AI systems can already crawl and sometimes cite ShellFans content,
but they do not consistently associate that content with the ShellFans brand,
and ShellFans is not yet included as a candidate answer for unbranded AEO / GEO commercial queries.

The optimization objective is therefore:

Crawl
→ Read
→ Understand
→ Cite
→ Attribute to ShellFans
→ Recommend ShellFans

Do NOT optimize primarily for increasing crawler count.

The priority is:

1. Entity attribution
2. Topical authority
3. Commercial query coverage
4. Third-party-verifiable claims readiness
5. Internal semantic architecture
6. AI-readable answer blocks
7. Structured data
8. Measurable visibility improvement

==================================================
PHASE 0 — INSPECT BEFORE MODIFYING
==================================================

Before changing any code:

1. Inspect the entire existing shell.fans codebase.

2. Identify:
   - framework
   - rendering method
   - routing method
   - reusable layout components
   - schema / JSON-LD implementation
   - metadata implementation
   - sitemap generator
   - robots.txt
   - llms.txt
   - llms-full.txt
   - canonical rules
   - hreflang if any
   - internal linking structure
   - current AEO/GEO pages
   - blog / article routes
   - footer / navigation
   - current /aeo-geo implementation

3. Search the codebase for existing pages or content related to:
   - AEO
   - Answer Engine Optimization
   - GEO
   - Generative Engine Optimization
   - AI SEO
   - AI crawler
   - GPTBot
   - OAI-SearchBot
   - ChatGPT-User
   - ClaudeBot
   - PerplexityBot
   - llms.txt
   - AI visibility
   - citation monitoring
   - AI crawler monitoring
   - AEO pricing
   - AEO implementation
   - AEO tools
   - AEO vs SEO

4. DO NOT create duplicate or competing pages if equivalent pages already exist.

5. If an equivalent page exists:
   - improve it
   - preserve its URL if already indexed
   - avoid keyword cannibalization
   - add redirects only when necessary

6. Compare production implementation with GitHub repository state.

7. Do not overwrite unrelated production work.

8. Create a short internal content map before editing.

==================================================
PHASE 1 — BUILD A QUERY-TO-PAGE CONTENT MAP
==================================================

The latest AI visibility probe shows ShellFans is missing from the following unbranded queries:

AEO / GEO recommendation queries:
- 台灣做 AEO（答案引擎優化）的公司推薦
- 台灣有哪些提供 Answer Engine Optimization（AEO，答案引擎優化）的服務公司？
- 想讓網站被 ChatGPT 引用，該找誰協助？
- 台灣有哪些 GEO 生成式引擎優化服務？
- AEO（答案引擎優化）顧問怎麼選？有推薦的嗎？

Foundational queries:
- AEO 和 SEO 有什麼不同？
- 什麼是 Answer Engine Optimization？
- GEO 生成式引擎優化是什麼意思？
- 公司網站需要做 AEO（答案引擎優化）嗎？

Technical queries:
- 要怎麼讓 AI 搜尋引擎正確理解我的網站？
- 如何檢查網站的 AI 爬蟲來訪狀況？
- 網站要怎麼設定才能讓 GPTBot 抓取？
- 有哪些工具可以檢測網站的 AEO 表現？
- llms.txt 是什麼？要怎麼寫？

Commercial / implementation queries:
- AEO（答案引擎優化）服務大概多少錢？
- AEO（答案引擎優化）導入需要多久才看得到成效？
- 企業導入 AEO 需要準備什麼？
- AEO 服務通常包含哪些工作項目？

Map them into topic clusters.

Recommended architecture:

A. Pillar:
   /aeo-guide

B. Technical:
   /aeo/ai-search-readability
   /aeo/ai-crawler-monitoring
   existing /aeo/gptbot-oai-searchbot
   existing or improved llms.txt-related content

C. Commercial:
   /aeo-tools
   /aeo/pricing-guide
   /aeo/implementation

D. Service:
   /aeo-geo

Do not blindly create all URLs if equivalent pages already exist.
Use existing pages whenever possible.

==================================================
PHASE 2 — CREATE / IMPROVE THE AEO PILLAR PAGE
==================================================

Create or substantially improve:

https://shell.fans/aeo-guide

This must be an INFORMATIONAL authority page, not merely a sales landing page.

Primary intent:
Become a comprehensive ShellFans-owned source for AEO / GEO concepts.

Recommended H1:

AEO 是什麼？Answer Engine Optimization 完整指南

The page should naturally cover:

- What is AEO?
- AEO vs SEO
- What is GEO?
- AEO vs GEO
- Why AI search changes website optimization
- How AI systems discover websites
- How AI systems understand websites
- How AI systems cite websites
- Brand mention vs citation
- Entity attribution
- AI crawler access
- robots.txt
- sitemap.xml
- llms.txt
- llms-full.txt
- structured data / Schema.org
- answer-first content
- internal linking
- authority signals
- third-party corroboration
- AI visibility monitoring
- citation monitoring
- crawler monitoring
- AEO KPIs
- implementation timeline
- service selection criteria

IMPORTANT CONTENT STYLE:

Every major H2 should use one of these structures where appropriate:

Question
→ 40–80 Chinese-character direct answer
→ supporting explanation
→ evidence / example
→ internal link

Example:

## AEO 和 SEO 有什麼不同？

AEO 的目標是讓網站內容成為 AI 回答中的來源、引用或品牌推薦；SEO 則主要提升網站在搜尋結果中的排名與點擊。兩者共用可爬取性、內容品質與網站權威等基礎，但 AEO 更重視答案結構、實體關係與引用可讀性。

Then expand.

Do not keyword-stuff.

==================================================
PHASE 3 — FIX ENTITY ATTRIBUTION
==================================================

The current report proves ShellFans content is already being cited for:

"網站要怎麼設定才能讓 GPTBot 抓取？"

Claude cited:

https://shell.fans/aeo/gptbot-oai-searchbot

but did NOT mention the ShellFans brand.

This is a high-priority attribution gap.

Inspect this page and all major AEO technical pages.

Each relevant page should clearly establish:

- Brand:
  ShellFans AI Technology

- Legal entity:
  唄粉智能科技股份有限公司

- Subject expertise:
  AEO / GEO Managed Hosting
  AI crawler monitoring
  AI visibility monitoring
  AI-readable website infrastructure

Add a concise visible attribution block where appropriate, for example:

「本頁由 ShellFans AI Technology 整理。ShellFans 提供 AEO/GEO Managed Hosting、AI crawler monitoring、AI visibility monitoring 與網站 AI-readable infrastructure 優化服務。」

Do not place this unnaturally in every paragraph.

Add it:
- near author / publisher metadata
- near article ending
- where editorial ownership is naturally established

==================================================
PHASE 4 — STRUCTURED DATA / ENTITY GRAPH
==================================================

Audit and improve JSON-LD.

At minimum, important AEO pages should use appropriate schema such as:

- Organization
- WebSite
- WebPage
- Article or TechArticle where appropriate
- BreadcrumbList
- FAQPage only where the visible page genuinely contains matching FAQ content
- Service for commercial service pages

Organization entity must consistently use:

name:
ShellFans AI Technology

legalName:
唄粉智能科技股份有限公司

url:
https://shell.fans/

Use the site's actual logo URL.

Connect relevant properties when valid:

- publisher
- author
- about
- mentions
- isPartOf
- mainEntity
- breadcrumb

Do not fabricate:
- reviews
- ratings
- awards
- client counts
- certifications
- rankings
- market leadership claims

Only use verifiable existing facts.

If sameAs already exists, validate existing destinations and keep only legitimate official profiles.

==================================================
PHASE 5 — BUILD / IMPROVE /aeo-tools
==================================================

Create or improve:

https://shell.fans/aeo-tools

Primary query intent:

「有哪些工具可以檢測網站的 AEO 表現？」

Do NOT write a page that simply claims "ShellFans is the best tool."

Instead explain the AEO tool taxonomy.

Suggested H1:

AEO 檢測工具有哪些？AI Visibility、Crawler 與 Citation 怎麼量測

The page should explain at least:

1. Technical readiness audit
2. AI crawler monitoring
3. Bot identity verification
4. AI citation monitoring
5. Brand mention monitoring
6. Prompt visibility monitoring
7. Entity consistency audit
8. Trend reporting
9. Competitive visibility analysis

Add a comparison table like:

檢測類型 | 主要回答的問題 | 典型指標

Examples:
AI crawler monitoring
→ 哪些 AI 系統真的來過網站？
→ crawler count / bot / path / timestamp

Citation monitoring
→ AI 有沒有把網站當來源？
→ citation rate / cited URL

Brand visibility
→ AI 回答有沒有提品牌？
→ mention rate

Attribution
→ AI 用了官方資料是否有說出品牌？
→ attribution gap

Then naturally explain which of these are currently covered by ShellFans.

If the site already has a free AEO scan, link to it prominently.

==================================================
PHASE 6 — BUILD / IMPROVE PRICING GUIDE
==================================================

Create or improve:

https://shell.fans/aeo/pricing-guide

Primary intent:

「AEO 服務大概多少錢？」

Do NOT invent market prices unless the site already contains verified pricing data.

The page should instead explain pricing structure and cost drivers clearly.

Suggested H1:

AEO / GEO 服務費用怎麼估？企業導入成本與計價方式

Cover:

- audit / diagnosis
- technical implementation
- schema
- content restructuring
- content production
- AI crawler monitoring
- citation monitoring
- prompt monitoring
- managed hosting
- monthly optimization
- third-party authority work

Explain the difference between:

- one-time audit
- project implementation
- monthly retainer
- managed service

If ShellFans has existing pricing / commercial model in the repository, reuse only verified data.

If pricing is not publicly defined, say:
「實際費用依網站規模、內容量、目標主題與監測範圍評估。」

Do not hallucinate pricing.

==================================================
PHASE 7 — BUILD / IMPROVE IMPLEMENTATION GUIDE
==================================================

Create or improve:

https://shell.fans/aeo/implementation

Primary intents:

- 企業導入 AEO 需要準備什麼？
- AEO 導入多久有成效？
- AEO 服務包含哪些工作？

Suggested H1:

企業導入 AEO 要準備什麼？流程、時程與成效指標

Explain stages:

Stage 1:
Technical accessibility

Stage 2:
Content / query mapping

Stage 3:
Entity establishment

Stage 4:
Citation readiness

Stage 5:
Visibility monitoring

Stage 6:
Iteration

If ShellFans' current business process in the repository/documentation defines an approximately 90-day engineering period, explain it carefully:

The reason is NOT that crawlers need 90 days to access a website.

Explain that different stages move at different speeds:

Crawl
→ index / retrieval
→ entity recognition
→ citation
→ recommendation

Do not guarantee a specific AI ranking result.

==================================================
PHASE 8 — IMPROVE AI CRAWLER MONITORING CONTENT
==================================================

Create or improve a dedicated page if an equivalent one does not already exist:

https://shell.fans/aeo/ai-crawler-monitoring

Suggested H1:

如何檢查網站的 AI 爬蟲？GPTBot、ClaudeBot 與 AI Crawler Monitoring 指南

This page should explain:

- server log vs analytics
- why GA4 cannot reliably show crawler traffic
- User-Agent spoofing risk
- edge/CDN logging
- reverse DNS verification where applicable
- official IP range verification where applicable
- crawler classification
- GPTBot
- OAI-SearchBot
- ChatGPT-User
- ClaudeBot
- Claude-SearchBot
- PerplexityBot
- Google-Extended
- Amazonbot
- Meta-ExternalAgent

Naturally explain ShellFans' edge collection approach if supported by the existing implementation.

Do not expose private infrastructure, secrets, IP allowlists, credentials, or internal security logic.

==================================================
PHASE 9 — INTERNAL LINKING / TOPIC GRAPH
==================================================

Create a strong internal semantic graph.

The target architecture should conceptually be:

/aeo-guide
   ↓
/aeo/ai-search-readability
/aeo/ai-crawler-monitoring
/aeo/gptbot-oai-searchbot
/aeo-tools
/aeo/pricing-guide
/aeo/implementation
   ↓
/aeo-geo

And relevant commercial pages should link back to the informational guide.

Anchor text should be descriptive.

Avoid:
- 點這裡
- more
- learn more

Prefer:
- AEO 完整指南
- AI 爬蟲監測
- GPTBot 與 OAI-SearchBot 設定
- AEO 導入流程
- AEO 費用與計價
- AEO 檢測工具

Also inspect:
/what-is-shellfans

Ensure it links naturally to:
/aeo-geo
/aeo-guide

and clearly describes AEO/GEO as one ShellFans service line without changing ShellFans' broader company positioning.

==================================================
PHASE 10 — ANSWER-FIRST CONTENT REQUIREMENTS
==================================================

For every new or updated AEO informational page:

1. One clear H1 only.
2. Correct H2/H3 hierarchy.
3. Important questions should appear as headings.
4. Place a concise direct answer immediately below the question.
5. Direct answers should be independently understandable.
6. Avoid vague pronouns where a brand/entity name is needed.
7. Keep paragraphs relatively short.
8. Use tables where comparison is useful.
9. Use bullet lists only where they improve extraction.
10. Clearly show:
   - updated date
   - publisher / author where supported by site design
11. Core content must exist in raw server-rendered HTML.
12. Do not depend on client-side JavaScript to reveal the primary content.

==================================================
PHASE 11 — BRAND / ENTITY CONSISTENCY
==================================================

Audit all major references to:

ShellFans
ShellFans AI
ShellFans AI Technology
唄粉智能科技
唄粉智能科技股份有限公司

Define and enforce a consistent hierarchy:

Brand:
ShellFans AI Technology

Short brand:
ShellFans

Legal entity:
唄粉智能科技股份有限公司

Do not blindly replace legal names where legally required.

Ensure:
- Organization schema
- About page
- AEO pages
- footer
- metadata
- JSON-LD
- llms.txt

do not contradict each other.

==================================================
PHASE 12 — llms.txt / llms-full.txt
==================================================

Inspect current:

https://shell.fans/llms.txt
https://shell.fans/llms-full.txt

Do not assume they are broken; crawler logs confirm both are already accessed.

Improve only where needed.

Ensure the important new / updated AEO authority pages are included and described accurately.

Prioritize:
- /what-is-shellfans
- /aeo-guide
- /aeo-geo
- /aeo-tools
- /aeo/implementation
- /aeo/pricing-guide
- /aeo/ai-crawler-monitoring
- /aeo/gptbot-oai-searchbot

Descriptions should explain each page's purpose, not just repeat titles.

==================================================
PHASE 13 — SITEMAP / ROBOTS / CANONICAL
==================================================

Verify:

- all intended indexable AEO pages return HTTP 200
- canonical URLs are self-consistent
- sitemap includes them
- robots.txt does not block them
- no accidental noindex
- no duplicate canonical conflicts
- no redirect chains
- http → https handled correctly
- www / non-www canonicalization remains correct

Do not modify working crawler rules unnecessarily.

==================================================
PHASE 14 — BUILD A QUERY COVERAGE MANIFEST
==================================================

Create a machine-readable internal manifest, if compatible with the project architecture.

For example:

data/aeo-query-map.json

or equivalent.

It should map:

query
→ intent
→ cluster
→ target URL
→ primary answer section

Example structure:

{
  "query": "有哪些工具可以檢測網站的 AEO 表現？",
  "cluster": "technical-tools",
  "target": "/aeo-tools"
}

Do not expose confidential internal strategy if this file would become publicly accessible.

Use a non-public application/data directory where appropriate.

Purpose:

future reporting should be able to compare AI visibility test prompts against target pages.

==================================================
PHASE 15 — REPORTING IMPROVEMENT PREPARATION
==================================================

Inspect the current AEO report generation code.

Do NOT redesign the entire reporting system unless necessary.

Prepare the underlying data model so the report can eventually distinguish:

- Crawlability
- AI crawler visits
- Brand mention rate
- Official citation rate
- Attribution rate
- Attribution gap
- Commercial query visibility
- Informational query visibility
- Query cluster performance
- Winning URL
- Cited URL
- competitor cited domains

The business KPI priority should become:

1. Unbranded brand mention rate
2. Official citation rate
3. Attribution rate
4. Commercial query visibility
5. Query-cluster coverage

Crawler count remains a supporting metric, not the primary success metric.

==================================================
PHASE 16 — VALIDATION
==================================================

After implementation, perform automated and manual validation.

Check each important URL with curl.

Validate:

- HTTP status
- redirect behavior
- canonical
- title
- meta description
- H1
- rendered/raw HTML content
- internal links
- JSON-LD
- sitemap inclusion
- robots access
- noindex
- content visibility without JavaScript

At minimum test:

https://shell.fans/aeo-guide
https://shell.fans/aeo-geo
https://shell.fans/aeo-tools
https://shell.fans/aeo/implementation
https://shell.fans/aeo/pricing-guide
https://shell.fans/aeo/ai-crawler-monitoring
https://shell.fans/aeo/gptbot-oai-searchbot
https://shell.fans/what-is-shellfans
https://shell.fans/llms.txt
https://shell.fans/llms-full.txt
https://shell.fans/robots.txt
https://shell.fans/sitemap.xml

If some proposed page was intentionally merged into an existing page, validate the actual selected URL instead.

==================================================
PHASE 17 — CONTENT QUALITY / CLAIM SAFETY
==================================================

Do not fabricate:

- AEO rankings
- "Taiwan No.1"
- best provider claims
- market share
- citation success guarantees
- ChatGPT ranking guarantees
- guaranteed timeline
- fake testimonials
- fake client results
- fake statistics

Use only facts available in the codebase or existing approved ShellFans materials.

Use wording such as:

- 提升被 AI 正確理解與引用的機會
- 建立 AI-readable 官方資料源
- 監測 AI crawler、citation 與 brand visibility
- 不保證任何 AI 平台一定引用或推薦

==================================================
PHASE 18 — GIT / DELIVERY REQUIREMENTS
==================================================

After all work:

1. Run all relevant build / lint / test commands.
2. Fix regressions caused by this task.
3. Verify production behavior.
4. Review git diff.
5. Commit with a clear message.
6. Push to the project's existing GitHub remote.

Also save this task prompt itself to:

prompts/shellfans-aeo-visibility-entity-authority-2026-09-02.md

Do not create a second duplicate prompt file.

==================================================
FINAL REPORT
==================================================

When complete, report:

1. Existing architecture discovered
2. Existing pages reused
3. New pages created
4. Existing pages modified
5. Query-to-page mapping
6. Entity attribution changes
7. Structured-data changes
8. Internal-link changes
9. llms.txt / llms-full.txt changes
10. sitemap / robots / canonical verification
11. Build/test results
12. Production URL validation results
13. Git commit hash
14. GitHub push result
15. Remaining issues, if any

Also provide a compact BEFORE / AFTER table:

Metric / capability
Before
After implementation

Include:

- AEO topical coverage
- unbranded query landing-page coverage
- entity attribution
- AEO tools query coverage
- pricing query coverage
- implementation query coverage
- crawler-monitoring query coverage
- schema/entity graph
- internal topic graph

IMPORTANT:

Do not claim AI visibility has already increased immediately after deployment.

Implementation completion is NOT the same as AI visibility improvement.

Clearly distinguish:

Technical/content deployment:
DONE / NOT DONE

External AI re-crawl / re-index:
PENDING / OBSERVED

Brand mention improvement:
TO BE MEASURED

Citation improvement:
TO BE MEASURED

The next visibility probe should use the same unbranded prompt set so results can be compared against the 2026-09-02 baseline:

- Unbranded mention rate: 0%
- Official citation rate: 3%
- Technical-query attribution gap: +10%

Proceed autonomously.
Do not stop to ask for confirmation unless an action would risk data loss, credential exposure, or destructive production changes.
