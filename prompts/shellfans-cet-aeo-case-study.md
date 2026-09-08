# ShellFans CET AEO Case Study
# 師德文教 CET AEO 案例頁製作任務

You are working on the ShellFans production codebase and the existing CET AEO project.

Target public case-study page:

https://shell.fans/aeo/case-studies/cet-taiwan

Client / brand allowed to be publicly identified:

師德文教
CET Taiwan
https://cet-taiwan.com

IMPORTANT PRIVACY / DISCLOSURE RULE:

This case study must use a "brand disclosed, sensitive data partially anonymized" model.

You MAY publicly show:
- client brand name
- public website URL
- public page URLs
- general AEO implementation scope
- public technical improvements
- directional before/after trends
- percentages if supported by verified project data and approved for publication
- crawler categories/platform names
- non-sensitive screenshots/charts derived from public or approved metrics

You MUST NOT publicly expose:
- private client admin data
- internal credentials
- Google Search Console account identifiers
- GA4 property IDs unless already public
- user/customer PII
- internal revenue
- internal business KPIs
- private backend URLs
- confidential traffic numbers unless already explicitly approved
- internal ShellFans implementation secrets
- raw access logs containing IP addresses
- any metric you cannot verify

If exact values are sensitive or not clearly approved,
use:
- percentage change
- indexed baseline
- relative growth
- ranges
- "increased / decreased"
- anonymized counts

Do not invent any number.

==================================================
PHASE 0 — INSPECT BEFORE WRITING
==================================================

Before creating the case-study page:

1. Inspect the CET project implementation and current production state.

2. Review the actual AEO work already completed for CET, including:
   - existing CET AEO-related pages
   - JSON-LD / structured data
   - canonical
   - sitemap
   - robots.txt
   - Search Console-related implementation if visible in code
   - llms.txt if present
   - internal linking
   - headings
   - raw HTML / SSR visibility
   - AI-readable content structure

3. Specifically inspect these public CET pages if they exist:

https://cet-taiwan.com/about-cet-kite
https://cet-taiwan.com/about-cet-style-jet
https://cet-taiwan.com/kids-english-test-comparison
https://cet-taiwan.com/kids-english-exam

4. Inspect ShellFans AEO reporting data relevant to CET.

5. Identify:
   - project start date
   - baseline period
   - current measurement date
   - crawler activity
   - AI citation observations
   - brand mention observations
   - official citation observations
   - attribution gaps
   - winning URLs
   - query clusters
   - trend data

6. Do not assume the case is successful simply because crawler visits increased.

Separate:
- technical readiness
- crawler activity
- citation activity
- brand mention
- commercial visibility

==================================================
PHASE 1 — VERIFY CURRENT RESULTS
==================================================

Create an internal verification summary before building the page.

The summary must distinguish:

A. Verified facts
B. Derived calculations
C. Directional observations
D. Not enough evidence

Examples:

Verified fact:
"AI crawlers accessed the site during the project period."

Derived calculation:
"AI crawler visits increased X% compared with baseline."

Directional observation:
"Brand attribution improved after entity-related content changes."

Not enough evidence:
"No confirmed increase in lead conversions."

Do not publish category D as a positive claim.

==================================================
PHASE 2 — DEFINE PUBLIC DISCLOSURE LEVEL
==================================================

For every candidate metric, classify it as:

PUBLIC_EXACT
PUBLIC_PERCENTAGE
PUBLIC_DIRECTIONAL
PRIVATE
UNVERIFIED

Only render:

PUBLIC_EXACT
PUBLIC_PERCENTAGE
PUBLIC_DIRECTIONAL

Do not render:
PRIVATE
UNVERIFIED

If no approval metadata exists,
default sensitive business metrics to PRIVATE.

==================================================
PHASE 3 — PAGE INFORMATION ARCHITECTURE
==================================================

Create:

/aeo/case-studies/cet-taiwan

Suggested H1:

AEO 實際案例：師德文教 CET 如何提升 AI 可讀性與品牌能見度

Suggested sections:

1. Case Summary
2. Client Background
3. Initial Challenges
4. AEO Objectives
5. Implementation Scope
6. Technical Changes
7. Content / Query Mapping
8. AI Crawler Observation
9. AI Visibility / Citation Observation
10. Before / After
11. What Improved
12. What Still Needs Improvement
13. Lessons Learned
14. Next Optimization Stage
15. Methodology
16. Limitations
17. About ShellFans AEO/GEO

==================================================
PHASE 4 — CLIENT BACKGROUND
==================================================

Keep the client background concise.

Explain only publicly verifiable facts about CET Taiwan.

Do not fabricate:
- student counts
- revenue
- market share
- rankings
- awards
- internal customer data

Focus on:
- education
- children's English testing / learning-related content
- website content structure
- why AI readability matters for this type of site

==================================================
PHASE 5 — INITIAL CHALLENGES
==================================================

Describe the actual baseline problems only if supported by project evidence.

Potential areas to inspect:

- AI-readable content structure
- query-to-page alignment
- entity clarity
- brand attribution
- structured data
- internal linking
- direct-answer sections
- crawl accessibility
- indexability
- AI crawler visibility
- citation visibility

Do not claim all of these were problems unless verified.

==================================================
PHASE 6 — IMPLEMENTATION SCOPE
==================================================

Document actual work performed.

Potential examples, if verified:

- optimized four target CET pages
- improved H1/H2/H3 hierarchy
- added answer-first content
- improved JSON-LD
- improved canonical
- improved internal links
- improved comparison content
- improved AI-readable HTML
- query mapping
- Search Console submission
- sitemap updates
- structured data validation

Only include verified changes.

==================================================
PHASE 7 — BEFORE / AFTER DESIGN
==================================================

Build a clear Before / After section.

Preferred format:

Metric / Capability
Before
After
Evidence type

Examples:

AI-readable page structure
Before: weak / incomplete
After: improved
Evidence: HTML inspection

Structured data
Before: partial
After: implemented
Evidence: JSON-LD validation

AI crawler activity
Before: baseline
After: increased
Evidence: crawler logs

Brand mention
Before: X
After: Y
Evidence: AI visibility probe

Official citation
Before: X
After: Y
Evidence: AI visibility probe

If exact counts are private,
use:
- baseline = 100
- current = 145
or
- +45%
or
- directional labels

Do not mix metrics from different date ranges.

==================================================
PHASE 8 — CHARTS
==================================================

If trend data exists, create simple case-study charts.

Preferred:
- crawler trend
- AI visibility trend
- citation / mention trend
- query coverage trend

Use accessible labels.

Do not create fake historical data.

If there are too few points,
use milestone cards instead of line charts.

==================================================
PHASE 9 — EXPLAIN CRAWLER VS CITATION
==================================================

The case study must explicitly explain:

AI crawler visits are not the same as AI citation.

Recommended wording concept:

"AI crawler 到站代表內容已被取得，但不代表一定會被 AI 引用、提及或推薦。因此本案例將 crawler、citation、brand mention 與 attribution 分開觀察。"

This distinction is important and must appear visibly.

==================================================
PHASE 10 — QUERY / INTENT COVERAGE
==================================================

If ShellFans has prompt-panel data for CET,
show selected query categories rather than raw proprietary prompts.

Possible categories:

- brand queries
- children's English test comparison
- exam selection
- product/service explanation
- parent decision-support queries

Avoid exposing confidential prompt strategy if needed.

Show:
- covered
- partially covered
- not yet covered

==================================================
PHASE 11 — "WHAT STILL NEEDS IMPROVEMENT"
==================================================

Do not make this page read like a perfect success story.

Include a section that honestly shows remaining gaps.

Examples, only if verified:

- unbranded brand mention still low
- third-party authority signals still insufficient
- AI citation still inconsistent
- some query clusters not yet visible
- recrawl / reindex still pending
- entity attribution requires more time

This increases trust and makes the case study more credible.

==================================================
PHASE 12 — METHODOLOGY
==================================================

Explain ShellFans methodology in a neutral, technical way.

Suggested flow:

Baseline
→ Query mapping
→ Technical AEO
→ Content restructuring
→ Entity optimization
→ AI crawler monitoring
→ Citation monitoring
→ Visibility re-test
→ Iteration

Do not claim proprietary magic or guaranteed ranking.

==================================================
PHASE 13 — LIMITATIONS
==================================================

Add a visible limitations section.

Must include:

- AI platforms can change answers dynamically
- crawler visits do not guarantee citation
- citation does not guarantee brand mention
- AI visibility can vary by platform, time, prompt wording, location, and search behavior
- results should be compared using the same or equivalent prompt set over time

==================================================
PHASE 14 — SHELLFANS ATTRIBUTION
==================================================

At the bottom of the case study, add a concise ShellFans service block.

Example concept:

ShellFans AI Technology 提供 AEO/GEO Managed Hosting、AI crawler monitoring、AI visibility monitoring 與網站 AI-readable infrastructure 優化。

Link naturally to:

/aeo-geo
/aeo-guide
/aeo-tools
/aeo/implementation

Do not oversell.

==================================================
PHASE 15 — STRUCTURED DATA
==================================================

Add appropriate JSON-LD.

Use only valid schema types.

Recommended:

WebPage
Article or TechArticle
BreadcrumbList
Organization
about
publisher
author

If applicable:
- mentions CET Taiwan as an organization/entity
- isPartOf ShellFans website

Do not use Review schema.
Do not fabricate ratings.

==================================================
PHASE 16 — INTERNAL LINKING
==================================================

Add this case study into the ShellFans AEO topic graph.

Relevant pages should link to it where natural:

/aeo-guide
/aeo-geo
/aeo/implementation
/aeo-tools

Add or create:

/aeo/case-studies

if no case-study index exists.

If created, use it as a clean index page for future cases.

Do not create an empty archive with only placeholder content.

==================================================
PHASE 17 — SEO / AEO TECHNICAL CHECKS
==================================================

Verify:

- HTTP 200
- self canonical
- one H1
- correct title
- correct meta description
- raw HTML contains primary case-study content
- noindex absent
- sitemap included
- internal links valid
- JSON-LD valid
- mobile-friendly layout
- no accidental UTM canonical
- no duplicate page conflict

==================================================
PHASE 18 — IMAGE / SCREENSHOT PRIVACY
==================================================

If using screenshots:

Do not show:
- admin credentials
- private client dashboards
- personal names
- email addresses
- IP addresses
- unpublished financial data

Crop or redact as needed.

Prefer generated charts from approved aggregate data over raw admin screenshots.

==================================================
PHASE 19 — COPY STYLE
==================================================

Tone:

- professional
- technical
- factual
- evidence-led
- not promotional
- readable by enterprise clients

Avoid:
- "第一名"
- "保證"
- "必然"
- "大幅提升" unless supported
- "成功讓 ChatGPT 推薦"
- "一定被 AI 收錄"

Prefer:
- "觀察到"
- "測得"
- "在本次期間內"
- "顯示改善"
- "仍需持續觀察"

==================================================
PHASE 20 — VALIDATION OF PUBLIC CLAIMS
==================================================

Before finalizing:

Create a claim audit.

For every numeric or factual claim on the public page:

Claim
→ Source
→ Date range
→ Public disclosure class
→ Verified yes/no

If source is unclear:
remove the claim.

==================================================
PHASE 21 — GIT / DEPLOYMENT
==================================================

Before editing:

- inspect git status
- compare current branch with production where applicable
- do not overwrite unrelated changes

After editing:

- run build
- run lint
- run tests
- inspect git diff
- deploy using existing project workflow
- verify production URL

Commit and push to existing GitHub remote.

Save this prompt to:

prompts/shellfans-cet-aeo-case-study.md

==================================================
FINAL REPORT
==================================================

When complete, report:

1. CET current status discovered
2. Verified measurable results
3. Metrics excluded from public page and why
4. Public disclosure classification
5. Case-study page created
6. Case-study index created or reused
7. Files modified
8. Structured data added
9. Internal links added
10. Sitemap verification
11. Production validation
12. Build / lint / test results
13. Git commit hash
14. Push result
15. Remaining AEO gaps for CET
16. Recommended next measurement date

Also provide:

PUBLIC CASE STUDY CLAIM SUMMARY

with:

- claim
- evidence
- date range
- disclosure level

IMPORTANT:

Do not publish the page until the claim audit has passed.

If verified evidence is insufficient for a strong Before / After,
publish a "project progress case study" instead of a "success case study".

Proceed autonomously.
Do not ask the user to manually verify information that can be confirmed from the codebase, production site, AEO reporting system, logs, or existing approved project data.
