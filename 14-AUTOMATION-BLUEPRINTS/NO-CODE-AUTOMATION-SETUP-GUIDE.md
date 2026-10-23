# No-Code Automation Blueprints Setup & Architecture Guide (`Make.com` / `n8n` / `Zapier`)

* **Flagship Product #3:** *The AI Content Creator & Solopreneur Operating System*
* **Directory:** `14-AUTOMATION-BLUEPRINTS/`
* **Included Ready-to-Import Workflow Files:** `5 Production JSON Blueprints`
* **Operational Goal:** Automate 80% of repetitive research, repurposing, lead delivery, sponsor qualification, and Friday KPI aggregation while keeping weekly API costs under **`$10.00 to $15.00 per month`**.

---

## 1. Executive Architecture: Why Deterministic No-Code Workflows Multiply Operator RPPH

In **Chapter 1** and **Chapter 7** of *The AI Content Creator & Solopreneur Operating System*, we proved mathematically that the average creator loses **18.4 hours every week** to context-switching and manual administrative glue work—copying scripts into multiple prompt windows, manually generating UTM links, checking competitor channels one by one, replying to low-budget sponsor inquiries, and copying analytics numbers into spreadsheets on Friday afternoon.

When you connect your **5-Database Minimalist Notion Creator OS Kit (`06-NOTION-TEMPLATES/`)** to an automation orchestrator (**Make.com**, **n8n**, or **Zapier**) using the five JSON blueprints in this folder, your Notion workspace transforms from a passive note-taking app into an **active, event-driven production engine**:

| Blueprint File | Workflow Name & Core Function | Trigger Event | Weekly Time Saved | Direct Chapter Tie-In |
| :--- | :--- | :--- | :---: | :---: |
| **`01-youtube-and-blog-to-15-asset-repurposing-pipeline.json`** | **1-to-15 Omnichannel Repurposing Engine:** Chains Prompts `P26`–`P30` to turn 1 H.E.A.R.T. Pillar Script into 14 native derivatives with UTM links. | Notion DB2 Status changes to `Pillar Script Locked` | `2.5 Hours / Wk` | Chapters 05, 06 & 07 |
| **`02-outlier-idea-and-rss-trend-scraper-to-notion.json`** | **S.I.G.N.A.L. Outlier Radar & Comment Miner:** Scans 25 peer channels every Monday, filters for $M_{\text{outlier}} \ge 2.5\times$, and mines top 50 comments (`P12`–`P13`). | Weekly Cron (`Monday 07:30 AM`) | `1.5 Hours / Wk` | Chapter 03 |
| **`03-automated-lead-magnet-optin-and-welcome-delivery.json`** | **Lead Magnet Delivery & UTM Attribution Router:** Verifies new opt-ins, sends the Tier 0 Audit Kit immediately, tags UTM source, and triggers the 5-Day Sequence (`P38`). | Inbound Webhook on Opt-In Form Submit | `1.5 Hours / Wk` | Chapter 08 |
| **`04-sponsor-inquiry-qualification-and-mediakit-autosender.json`** | **B2B Sponsor Qualifier & Media Kit Auto-Sender:** Scores inbound brand leads, calculates Tier A/B/C quotes + `30%` whitelisting fees, logs to Notion DB5, and sends Media Kit. | Inbound Sponsor Form / Email Webhook | `1.2 Hours / Wk` | Chapter 10 |
| **`05-friday-creator-ceo-analytics-and-rpph-digest.json`** | **Friday 20-Min Creator CEO Executive Digest:** Aggregates 7-day views, ERI, opt-ins, and product/sponsor revenue, computes weekly `RPPH`, and emails your 2:00 PM briefing (`P50`). | Weekly Cron (`Friday 13:45 PM`) | `1.3 Hours / Wk` | Chapters 01 & 10 |
| **CONSOLIDATED AUTOMATION IMPACT** | **Full 5-Stage Creator OS Automation Stack** | **Event + Cron Driven** | **`8.0 Hours / Wk Saved`** | **Stages 1 through 5** |

---

## 2. Step-by-Step Platform Import Instructions (`n8n`, `Make.com`, and `Zapier`)

Each `.json` file in `14-AUTOMATION-BLUEPRINTS/` is structured as a clean, platform-agnostic node graph containing exact HTTP endpoints, Notion database property mappings, JavaScript formula nodes, and verbatim LLM system/user prompts.

### Option A: Importing Into `n8n` (Self-Hosted Docker or n8n Cloud — Recommended for Lowest Cost)

1. **Open Your n8n Workspace:** Log in to your n8n dashboard (or local Docker instance at `http://localhost:5678`) and click **Add Workflow**.
2. **Import From File:** Click the three-dot menu (`...`) in the top-right corner of the canvas and select **Import from File**, then select any of the five `.json` files in `14-AUTOMATION-BLUEPRINTS/`.
3. **Bind Credentials:**
   * Create a **Notion API Credential** using your Notion Internal Integration Secret (`ntn_...`) and share your 5 Notion Databases with that integration.
   * Create an **Anthropic / OpenAI Credential** using your API key (`sk-...`).
   * In the **Set / Environment** node at the start of the workflow, paste your five Notion Database IDs (`NOTION_DB1_SIGNAL_IDEA_BANK_ID` through `NOTION_DB5_SPONSOR_CRM_ID`).
4. **Test Single Execution:** Click **Test Workflow** on a sample Notion row before toggling the top-right switch to **Active**.

### Option B: Importing Into `Make.com` (Visual Scenario Builder)

1. **Create a New Scenario:** Log in to Make.com, navigate to **Scenarios**, and click **+ Create a new scenario**.
2. **Import Blueprint or Map Modules:** Click the bottom toolbar menu (`More -> Import Blueprint`) or add the modules corresponding to the `nodes` array in the JSON file:
   * **Module 1 (Trigger):** Select `Notion -> Watch Database Items` (for Blueprint `#01`), `Schedule` (for Blueprints `#02` and `#05`), or `Webhooks -> Custom mailhook / webhook` (for Blueprints `#03` and `#04`).
   * **Module 2–5 (LLM & Logic):** Add `Anthropic Claude -> Create a Message` or `OpenAI -> Create a Chat Completion` and copy the exact `system_prompt` and `user_prompt` strings directly from the JSON blueprint node.
   * **Module 6–7 (Output):** Add `Notion -> Create a Database Item` or `Update a Database Item` and map the JSON fields to your Notion columns.
3. **Set Scheduling Interval:** Set the scenario schedule to **Every 15 minutes** (for Blueprint `#01`), **Mondays at 07:30 AM** (for Blueprint `#02`), **Immediately as data arrives** (for Webhooks `#03` and `#04`), and **Fridays at 1:45 PM** (for Blueprint `#05`).

### Option C: Configuring in `Zapier` (Multi-Step Zaps)

1. **Create a New Zap:** Click **+ Create Zap** and select the trigger matching `trigger_type` in the JSON file (`Notion Updated Database Item`, `Schedule by Zapier`, or `Webhooks by Zapier — Catch Hook`).
2. **Add Code by Zapier (JavaScript):** Copy the exact formula snippet from the `code.javascript` node in the JSON blueprint (for example, the $M_{\text{outlier}} \ge 2.5\times$ filter in Blueprint `#02` or the `RPPH` and `ERI` calculator in Blueprint `#05`).
3. **Add AI Action Step:** Add the **Anthropic Claude** or **ChatGPT** app step, set temperature to `0.3`, and paste the `system_prompt` and `user_prompt` from the JSON node.

---

## 3. Environment Variables, API Keys & Notion Database ID Checklist

Before activating your workflows, store these eight environment variables in your automation platform's secure credential vault:

| Variable Name | Where to Obtain It | Used by Blueprints |
| :--- | :--- | :---: |
| **`NOTION_INTEGRATION_SECRET_TOKEN`** | Go to `https://www.notion.so/my-integrations` -> **New Integration** -> Copy Internal Secret (`ntn_...`) and connect it to all 5 Creator OS databases via the `... -> Connections` menu. | `#01, #02, #03, #04, #05` |
| **`NOTION_DB1_SIGNAL_IDEA_BANK_ID`** | Open Database 1 in Notion, copy the 32-character hex string in the URL between your workspace slash and `?v=`. | `#02, #05` |
| **`NOTION_DB2_CONTENT_PIPELINE_ID`** | Open Database 2 (`1-to-15 Content Pipeline`) in Notion and copy the 32-character database ID. | `#01, #03, #05` |
| **`NOTION_DB5_SPONSOR_CRM_ID`** | Open Database 5 (`Sponsorship & Brand Deal CRM`) in Notion and copy the 32-character database ID. | `#04, #05` |
| **`OPENAI_OR_ANTHROPIC_API_KEY`** | Generate from `console.anthropic.com` (`claude-3-7-sonnet`) or `platform.openai.com` (`gpt-4o`). Set a hard monthly spend limit of `$20.00`. | `#01, #02, #04, #05` |
| **`YOUTUBE_DATA_API_KEY`** | Enable **YouTube Data API v3** in Google Cloud Console (`Free Tier: 10,000 units/day`—more than enough for 25 peer channels). | `#02` |
| **`ESP_API_KEY_CONVERTKIT_OR_BEEHIIV`** | Copy from your Email Service Provider settings (`Kit / ConvertKit`, `Beehiiv`, or `MailerLite`) to enroll new subscribers into the 5-Day Welcome Sequence. | `#03, #05` |
| **`OPERATOR_CEO_EMAIL`** | Your primary executive email address where Friday 2:00 PM Creator CEO digests and error notifications are delivered. | `#04, #05` |

---

## 4. Deep-Dive Walkthrough of Each Automation Blueprint

### Blueprint `#01`: Master Pillar Script to 1-to-15 Omnichannel Repurposing Pipeline
* **Operational Problem Solved:** Manually running five separate prompts to extract 5 Vertical Shorts, 2 LinkedIn posts, 2 X threads/essays, 3 slide carousels, and 2 newsletter issues takes 45 to 60 minutes every Tuesday.
* **How the Blueprint Works:**
  1. On Tuesday morning during **Block 2 (`9:00–9:45 AM`)**, you draft and review your 2,000-word **H.E.A.R.T. Master Pillar Script** inside Notion DB2 and switch its status dropdown to `Stage 2: Pillar Script Locked`.
  2. Within 60 seconds, Blueprint `#01` pulls your script alongside your stored **5-Parameter Voice DNA Card** and executes three parallel LLM chains (`Prompts P26, P27, P28–P29`).
  3. Node 6 (`code.javascript`) automatically strips any banned AI cliches, appends deterministic UTM tracking parameters (`utm_content=A02` through `A15`) to your lead magnet and checkout links, and writes all 14 child asset pages back into Notion DB2 ready for your Thursday 30-minute scheduling sprint.

### Blueprint `#02`: S.I.G.N.A.L. 25-Channel Outlier Radar & Comment Gap Miner
* **Operational Problem Solved:** Eliminates manual Monday morning scrolling on YouTube and guarantees you never miss a breakout peer topic ($M_{\text{outlier}} \ge 2.5\times$).
* **How the Blueprint Works:**
  1. Every Monday at `7:30 AM` (90 minutes before your Monday Block 1 session starts), Blueprint `#02` queries your 25 peer channels via the free YouTube Data API.
  2. It divides each video's 14-day view count by that peer channel's rolling 90-day median view count:
     $$M_{\text{outlier}} = \frac{\text{Views}_{14\text{d}}}{\text{Median Views}_{90\text{d}}}$$
  3. Any video scoring below `2.50x` is discarded automatically. For videos scoring $M_{\text{outlier}} \ge 2.50\times$, Node 5 fetches the top 50 viewer comments and Node 6 runs `Prompts P12 & P13` to extract the top 3 unfulfilled viewer questions plus 3 contrarian titles and 3-word thumbnail concepts. When you sit down at `9:00 AM` on Monday, your pre-validated outlier ideas are waiting in Notion DB1.

### Blueprint `#03`: Automated Lead Magnet Opt-In, UTM Attribution & 5-Day Welcome Delivery
* **Operational Problem Solved:** Ensures `100%` instant delivery of your Tier 0 Lead Magnet while tracking exactly which video, short, carousel, or post generated every new email subscriber.
* **How the Blueprint Works:**
  1. When a viewer submits their email on your `45%+` conversion landing page, Node 2 filters out disposable or malformed email addresses to protect your sender reputation.
  2. Node 3 tags the subscriber with their exact `utm_source` and `utm_content` (`A01`–`A15`) and enrolls them in your **5-Day Automated Welcome & Tripwire Sequence (Chapter 8)**.
  3. Node 4 dispatches the Day-0 email containing the download link and the **3-Option One-Click Segmentation Poll**, while Node 5 increments the `Attributed_Email_Opt_Ins` counter on the exact content asset in Notion DB2.

### Blueprint `#04`: Sponsor Inquiry Qualification, Rate Calculation & Media Kit Auto-Sender
* **Operational Problem Solved:** Protects your time from zero-budget "commission-only affiliate" spam while responding to qualified B2B software sponsors within 5 minutes with a professional rate card.
* **How the Blueprint Works:**
  1. When a brand fills out your partnership inquiry form, Node 2 computes your **Outcome Sponsorship Package Rates** (`Tier A $1,850`, `Tier B $3,200`, `Tier C $8,400`) and adds `+30% per 30 days` if the brand checked Paid-Ad Whitelisting.
  2. Node 3 classifies the lead and drafts a custom response using `Prompt P48`.
  3. Node 4 logs the deal in **Notion DB5 (`Sponsorship CRM`)**, and Node 5 automatically emails your **1-Page Media Kit & Rate Card Proposal (`03-Sponsorship-Media-Kit-and-Rate-Card-Proposal.docx`)** to the brand decision-maker.

### Blueprint `#05`: Friday 20-Minute Creator CEO Telemetry & RPPH Executive Digest
* **Operational Problem Solved:** Automates the data-gathering step of your **Friday 2:00 PM Creator CEO Review (Chapter 10)** so you spend your 20 minutes making high-impact decisions rather than copying numbers.
* **How the Blueprint Works:**
  1. Every Friday at `1:45 PM`, Node 2 and Node 3 pull your trailing 7-day views, CTR, 30-second hold rate, email opt-ins, digital product orders, and sponsor invoices.
  2. Node 4 calculates your weekly **RPPH (`Net Profit / Batch Hours`)**, **Engaged Retention Index (`ERI`)**, and **Blended Effective RPM**, flagging any metric that dipped below its green-light gate.
  3. Node 5 (`Prompt P50`) synthesizes a concise 1-page executive briefing identifying the single biggest bottleneck and recommending the one manual task to prune before Monday morning.

---

## 5. Monthly API Cost Budgeting, Rate Limits & Error-Handling Best Practices

Running all five automation blueprints requires **under `$12.00/month`** in total infrastructure and API fees:

1. **LLM Token Cost (`~$3.50 to $6.00 / Month`):**
   * Blueprint `#01` runs once per week (`~12,000` input/output tokens across 3 calls = `~$0.12/week` or `$0.50/month` on Claude 3.7 Sonnet or GPT-4o).
   * Blueprints `#02`, `#04`, and `#05` consume fewer than `30,000` tokens combined per week (`~$1.50/month`).
2. **Orchestrator Plan (`$0 to $9.00 / Month`):**
   * **Self-Hosted `n8n`:** `$0/month` (runs locally in Docker on your PC or on a `$4/mo` VPS).
   * **`Make.com` Core Plan (`$9/month` for 10,000 operations) or Free Tier (`1,000 operations/month`):** Our 5 blueprints consume only `~320 operations per month` combined, fitting comfortably inside Make.com's **Free Tier**!
3. **3-Retry Exponential Backoff & Dead-Letter Queue:**
   * Every JSON blueprint includes an `error_handling_policy` configured for `3 retries` with `60-second` exponential backoff. If an external API (such as Notion or OpenAI) experiences temporary downtime, the payload is saved to a fallback Notion row and an alert is sent to `OPERATOR_CEO_EMAIL` so zero content or customer data is ever lost.
