# ShellFans GA4 AI Referral Tracking Automation
# ShellFans GA4 AI 推薦流量與 UTM 自動追蹤設定

You are working on the production codebase for:

https://shell.fans

Goal:

Implement and verify GA4 tracking for AI referral traffic from:

- ChatGPT
- Claude
- Perplexity
- Gemini
- other AI answer engines when identifiable

The tracking model must support URLs such as:

https://shell.fans/aeo/gptbot-oai-searchbot?utm_source=claude&utm_medium=ai_answer&utm_campaign=aeo_visibility&utm_content=gptbot_setup

The purpose is to measure:

AI answer / citation
→ user click
→ landing page
→ engagement
→ AEO scan
→ contact / conversion

==================================================
PHASE 0 — INSPECT CURRENT ANALYTICS IMPLEMENTATION
==================================================

Before modifying anything:

1. Inspect the entire codebase for:
   - Google Analytics
   - GA4
   - gtag
   - Google Tag Manager
   - GTM
   - dataLayer
   - Measurement ID
   - analytics events
   - conversion events
   - cookie consent
   - consent mode
   - cross-domain settings

2. Identify whether shell.fans currently uses:
   - direct gtag.js
   - Google Tag Manager
   - another analytics wrapper

3. Find the existing GA4 Measurement ID.

4. Do NOT create a second GA4 implementation if one already exists.

5. Do NOT duplicate page_view tracking.

6. Check whether these subdomains are part of the same user journey:
   - shell.fans
   - console.shell.fans
   - app.shell.fans

7. Determine whether cross-domain or linker configuration is required.

==================================================
PHASE 1 — VERIFY UTM PARAMETER CAPTURE
==================================================

Ensure the website correctly accepts and preserves:

- utm_source
- utm_medium
- utm_campaign
- utm_content
- utm_term

Primary convention:

utm_source:
- chatgpt
- claude
- perplexity
- gemini

utm_medium:
- ai_answer

utm_campaign:
- aeo_visibility

utm_content:
- query or content identifier

Example:

?utm_source=claude&utm_medium=ai_answer&utm_campaign=aeo_visibility&utm_content=gptbot_setup

Requirements:

1. Query parameters must not break routing.
2. They must not trigger 404/redirect loops.
3. Canonical URLs must remain clean URLs without UTM parameters.
4. Do not add UTM URLs to sitemap.xml.
5. Do not use UTM URLs as canonical URLs.
6. Do not replace clean URLs in llms.txt with UTM URLs.

==================================================
PHASE 2 — CREATE AI REFERRAL SESSION CLASSIFICATION
==================================================

Implement a reusable front-end analytics helper.

The helper should classify a session as AI referral when:

utm_medium == "ai_answer"

OR

utm_source matches one of:

chatgpt
claude
perplexity
gemini
copilot
bing_chat
google_ai
openai

Normalize source names to lowercase.

Create a normalized property:

traffic_channel = "ai_referral"

and:

ai_platform = normalized platform name

Examples:

chatgpt
claude
perplexity
gemini

Do not overwrite native GA4 source/medium dimensions.

==================================================
PHASE 3 — SEND CUSTOM GA4 EVENTS
==================================================

Send a custom GA4 event on the first eligible landing page view:

event name:

ai_referral_landing

Suggested event parameters:

- ai_platform
- traffic_channel
- landing_path
- landing_url
- utm_source
- utm_medium
- utm_campaign
- utm_content
- referrer
- page_title

Do not include sensitive personal data.

Do not send:
- email
- phone number
- name
- account ID
- user-entered text

Ensure the event fires only once per session where practical.

==================================================
PHASE 4 — PRESERVE AI ATTRIBUTION THROUGH SESSION
==================================================

Persist first-touch AI attribution for the current session.

Preferred storage:
- sessionStorage

Store:

- ai_platform
- utm_source
- utm_medium
- utm_campaign
- utm_content
- first_landing_path

Do not use long-lived persistent storage unless the existing consent model permits it.

When the user later performs a key action, attach the AI attribution to that event.

==================================================
PHASE 5 — TRACK HIGH-VALUE ACTIONS
==================================================

Inspect the site and identify actual existing user actions.

Where relevant, instrument:

aeo_scan_start
aeo_scan_complete
contact_submit
consultation_request
signup
login
pricing_view

Only add events for real interactions that exist.

Do not fabricate buttons, forms, or conversion flows.

For AI-attributed sessions, attach:

- ai_platform
- traffic_channel
- utm_campaign
- first_landing_path

==================================================
PHASE 6 — GA4 CUSTOM DIMENSIONS PREPARATION
==================================================

Prepare these event-scoped dimensions for GA4:

- ai_platform
- traffic_channel
- landing_path
- utm_campaign
- first_landing_path

IMPORTANT:

If Google Analytics Admin API credentials are available in the environment,
use the official GA4 Admin API to inspect whether custom dimensions already exist.

If sufficient authorized credentials are available:
- create missing custom dimensions
- do not duplicate existing ones

If credentials are NOT available:
- do NOT fail the entire task
- generate a precise setup report listing exactly which GA4 Admin settings must be created manually

Do not expose credentials in logs or commits.

==================================================
PHASE 7 — GA4 KEY EVENTS
==================================================

Inspect whether the following events already exist:

- aeo_scan_complete
- contact_submit
- consultation_request
- signup

If GA4 Admin API access is available and authorized:
- inspect current key events
- mark the appropriate actual business conversion events as key events
- do not mark page_view or ai_referral_landing as a key event

If Admin API access is not available:
output exact manual GA4 instructions.

==================================================
PHASE 8 — CUSTOM CHANNEL GROUP
==================================================

Desired GA4 channel:

AI Referral

Preferred rule:

Session medium exactly matches:
ai_answer

OR Session source matches regex:

^(chatgpt|claude|perplexity|gemini|copilot|bing_chat|google_ai|openai)$

If GA4 Admin API supports creating/updating the necessary channel group
and valid credentials are available:
- inspect existing custom channel groups
- create or update without duplication

Otherwise provide manual configuration instructions.

Do not modify unrelated channel-group rules.

==================================================
PHASE 9 — CROSS-SUBDOMAIN ATTRIBUTION
==================================================

Inspect navigation between:

shell.fans
console.shell.fans
app.shell.fans

Ensure AI referral attribution is not accidentally replaced by self-referral
when a user moves between ShellFans-owned subdomains.

Check:
- cookie domain
- linker behavior
- GA4 stream setup
- unwanted referral behavior
- GTM/gtag implementation

Make the smallest safe change required.

Do not break login/authentication flows.

==================================================
PHASE 10 — SHELLFANS BACKEND / AEO CONSOLE
==================================================

Inspect the existing ShellFans admin console.

If there is already an AEO/GEO analytics or reporting data model,
extend it safely to support AI referral metrics.

Desired metrics:

- AI referral sessions
- AI platform
- landing page
- campaign
- AEO scan completions
- contact conversions
- signup conversions

Suggested derived KPI:

AI Referral Conversion Rate
=
AI-attributed conversions / AI referral sessions

Future KPI:

Citation-to-Visit Rate
=
AI referral visits / measured AI citations

IMPORTANT:

Do not calculate Citation-to-Visit Rate unless actual citation-count data exists
for the same date range and platform.

Do not mix crawler visits with human referral visits.

Crawler:
server-side bot request

AI referral:
human session arriving from AI-related URL/referral

These must remain separate metrics.

==================================================
PHASE 11 — GA4 DATA API
==================================================

Inspect whether the project already uses:

Google Analytics Data API

If valid credentials and property access are available:

Create or reuse a backend integration that can query:

dimensions:
- sessionSource
- sessionMedium
- sessionCampaignName
- landingPagePlusQueryString
- eventName

metrics:
- sessions
- totalUsers
- engagedSessions
- keyEvents
- averageSessionDuration

Filter AI traffic using:

sessionMedium == ai_answer

or approved AI source list.

Do not hardcode secrets.

Use environment variables.

If credentials are not available:
prepare the integration code and clearly identify required environment variables.

==================================================
PHASE 12 — REQUIRED GA4 ADMIN API CREDENTIAL CHECK
==================================================

Check for existing authorized Google credentials.

Possible sources:

- Application Default Credentials
- Google Cloud service account
- OAuth tokens already configured
- environment variables
- existing application integrations

Do NOT create new credentials automatically.

Do NOT print private keys.

Do NOT commit credential files.

If credentials exist, verify permissions before making GA4 Admin changes.

Minimum principle:
least privilege.

If no credentials exist, stop only the GA4-admin-write portion,
not the website tracking implementation.

==================================================
PHASE 13 — TESTING
==================================================

Test this URL:

https://shell.fans/aeo/gptbot-oai-searchbot?utm_source=claude&utm_medium=ai_answer&utm_campaign=aeo_visibility&utm_content=gptbot_setup

Verify:

1. HTTP 200
2. canonical points to clean URL
3. UTM parameters do not affect page content indexing
4. GA4 loads once
5. page_view is not duplicated
6. ai_referral_landing fires
7. ai_platform = claude
8. traffic_channel = ai_referral
9. UTM values are correct
10. attribution persists through internal navigation

Also test:

utm_source=chatgpt
utm_source=perplexity
utm_source=gemini

==================================================
PHASE 14 — DEBUGVIEW / REALTIME VALIDATION
==================================================

If GA4 credentials / access allow programmatic validation,
verify received events where technically possible.

Otherwise prepare exact verification instructions using:

GA4 Realtime
GA4 DebugView

Expected event:

ai_referral_landing

Expected parameters:

ai_platform = claude
traffic_channel = ai_referral
utm_campaign = aeo_visibility

==================================================
PHASE 15 — SAFETY
==================================================

Do NOT:

- create duplicate GA4 tags
- expose Measurement secrets or credentials
- commit service account JSON
- modify unrelated analytics properties
- modify unrelated websites
- change consent behavior without checking existing implementation
- send PII to GA4
- use UTM URLs as canonical
- put UTM URLs into sitemap
- count AI crawlers as human AI referral traffic

==================================================
PHASE 16 — FINAL REPORT
==================================================

Report:

1. Current analytics architecture found
2. GA4 Measurement ID found
3. GTM or gtag implementation
4. Files modified
5. Events created
6. UTM normalization implemented
7. Session attribution implementation
8. Cross-subdomain changes
9. Conversion events instrumented
10. GA4 Admin API availability
11. Custom dimensions:
   - created
   - already existed
   - manual action required
12. Key events:
   - configured
   - manual action required
13. Custom channel group:
   - configured
   - manual action required
14. GA4 Data API integration status
15. Production validation results
16. Remaining manual GA4 steps

If any manual GA4 steps remain, output them in this exact form:

GA4 MANUAL ACTION REQUIRED

A.
Menu path:
Admin > ...

Setting:
...

Value:
...

B.
Menu path:
...

Do not simply say "configure this in GA4."

Give exact names and values.

==================================================
GIT REQUIREMENTS
==================================================

Before modifying:
- inspect current git status
- compare repository and deployed implementation where applicable

After modification:
- run relevant build/lint/tests
- inspect git diff
- commit changes
- push to the existing GitHub remote

Save this prompt at:

prompts/shellfans-ga4-ai-referral-tracking.md

Final response must include:
- commit hash
- push result
- production validation
- manual GA4 tasks, if any

Proceed autonomously.
Do not ask the user to manually verify anything that can be verified from code, APIs, logs, or production.
