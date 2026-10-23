# Notion Creator OS — Complete Setup, Relation Architecture & Formula 2.0 Reference Guide

> **Technical Installation & Formula Manual (`NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md`)**
> * **Product ID:** `PRODUCT-03-AI-CREATOR-SOLOPRENEUR-OS`
> * **Compatibility:** Notion Free Plan, Notion Plus, Notion Business & Enterprise (Notion Formula 2.0 Syntax)
> * **Estimated Setup Time:** 15 Minutes

---

## 1. Quick-Start Installation: Importing Your 5 Notion Creator OS Databases

The **5-Database Minimalist Notion Creator OS Kit** (`06-NOTION-TEMPLATES/`) is engineered so you can deploy a complete, interconnected content production, prompt management, and monetization workspace inside Notion in under 15 minutes without bloated nested sub-pages.

### 1.1 Step-by-Step CSV & Markdown Import Procedure

1. **Create Your Master Workspace Page in Notion:**
   * Open Notion, click **+ New Page** in your sidebar, and title it **`Creator & Solopreneur OS — Command Center`**.
   * In the top-right `•••` menu of the page, enable **Full Width** so your multi-column waterfall boards and financial scorecards display without horizontal scrolling.

2. **Import the Master Monetization & Launch Hub (`05-Creator-Monetization-and-Launch-Hub.md`):**
   * Click `•••` -> **Import** -> **Text & Markdown** and select `06-NOTION-TEMPLATES/05-Creator-Monetization-and-Launch-Hub.md`.
   * This creates your executive command page containing the 4-Tier Value Ladder blueprint, the 14-Day Validate-Before-You-Build checklist, and the Friday Creator CEO SOP.

3. **Import the 4 Core Operational CSV Databases (`01` through `04`) + Baseline Audit (`sheet1`):**
   * On your Master Command Center page, type `/table view` -> **New database** for each of the five CSV files, then click `•••` -> **Merge with CSV** and upload:
     1. `01-Outlier-Idea-Bank-and-Hook-Vault.csv` (`25` pre-validated outlier concepts)
     2. `02-Master-Content-Calendar-and-1to15-Waterfall.csv` (`20`-week omnichannel production roadmap)
     3. `03-AI-Prompt-and-Script-Vault-62.csv` (`50` AI Workflow Prompts `P01`–`P50` + `12` Emergency Scripts `S01`–`S12`)
     4. `04-Sponsorship-CRM-and-Affiliate-Tracker.csv` (`20` B2B brand deal & affiliate records)
     5. `Spreadsheets/sheet1-creator-rpm-and-time-audit.csv` (`25`-activity time-leak & RPPH baseline audit)

---

## 2. Database Relation & Rollup Architecture

After importing the CSV files, convert the following text columns into **Select**, **Number**, and **Two-Way Relation** properties so changes in your Idea Bank or Sponsorship CRM automatically roll up into your Master Content Calendar:

| Source Database | Target Database | Relation Property Name | Rollup Property Configuration | Operational Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `01-Outlier-Idea-Bank` | `02-Master-Content-Calendar` | `Scheduled_Sprint_Week` | Rollup `Outlier_Multiplier_M` & `Thumbnail_3_Words` into Calendar | Ensures only ideas passing `M >= 2.5x` enter weekly production |
| `03-AI-Prompt-and-Script-Vault-62` | `02-Master-Content-Calendar` | `Attached_Workflow_Prompts` | Rollup `Full_Copy_Paste_Template` by Stage | Gives 1-click access to `P21`–`P35` inside each weekly sprint card |
| `04-Sponsorship-CRM` | `02-Master-Content-Calendar` | `Sponsored_Pillar_Slot` | Rollup `Total_Package_Value_USD` & `Invoice_Status` | Tracks total sponsor + product revenue per weekly Pillar upload |
| `sheet1-creator-rpm-and-time-audit` | `03-AI-Prompt-and-Script-Vault-62` | `Automation_Prompt_ID` | Rollup `Title` & `Engine_Stage` | Maps every manual time-leak directly to the AI prompt that automates it |

---

## 3. Exact Copy-Paste Notion Formula 2.0 Code Blocks

To make your Notion databases dynamically compute your stage-gate metrics whenever you enter raw views, hours, or sponsor inputs, add a **Formula** property to the corresponding database and paste the exact **Notion Formula 2.0** expressions below.

### 3.1 Formula 1: Revenue Per Production Hour (`RPPH`) & Delegation Gate
* **Target Database:** `sheet1-creator-rpm-and-time-audit` (or Weekly CEO Scorecard)
* **Required Number Properties:** `Direct_Revenue_Attributed_USD`, `Systematized_OS_Hours`
* **Copy-Paste Notion Formula 2.0 Expression:**
```javascript
lets(
  monthlyHrs, prop("Systematized_OS_Hours") * 4,
  rpph, if(monthlyHrs > 0, round((prop("Direct_Revenue_Attributed_USD") / monthlyHrs) * 100) / 100, 0),
  status, ifs(
    rpph >= 200, "🟢 EXECUTIVE YIELD ($" + format(rpph) + "/hr)",
    rpph >= 65, "🟡 DELEGATION READY ($" + format(rpph) + "/hr)",
    "🔴 AUTOMATE / ELIMINATE ($" + format(rpph) + "/hr)"
  ),
  status
)
```

### 3.2 Formula 2: Niche Monetization Potential Index (`NMPI_Score` — 100-Point Scale)
* **Target Database:** `01-Outlier-Idea-Bank-and-Hook-Vault`
* **Required Number Properties:** `Pain_Urgency_1_10`, `Purchasing_Power_1_10`, `Info_Gap_1_10`, `Product_Fit_1_10`
* **Copy-Paste Notion Formula 2.0 Expression:**
```javascript
lets(
  score, round(
    (prop("Pain_Urgency_1_10") * 2.5 +
     prop("Purchasing_Power_1_10") * 3.0 +
     prop("Info_Gap_1_10") * 2.0 +
     prop("Product_Fit_1_10") * 2.5) * 10
  ) / 10,
  gate, ifs(
    score >= 75, "🟢 HIGH-MARGIN GO (" + format(score) + "/100)",
    score >= 60, "🟡 REFINEMENT REQ (" + format(score) + "/100)",
    "🔴 REJECT TOPIC (" + format(score) + "/100)"
  ),
  gate
)
```

### 3.3 Formula 3: S.I.G.N.A.L. Outlier Multiplier (`Outlier_Multiplier_M`)
* **Target Database:** `01-Outlier-Idea-Bank-and-Hook-Vault`
* **Required Number Properties:** `Peer_Outlier_Views_14d`, `Peer_Channel_Median_Views`
* **Copy-Paste Notion Formula 2.0 Expression:**
```javascript
lets(
  median, max(prop("Peer_Channel_Median_Views"), 1),
  mult, round((prop("Peer_Outlier_Views_14d") / median) * 100) / 100,
  verdict, ifs(
    mult >= 2.5, "🟢 VALIDATED OUTLIER (" + format(mult) + "x)",
    mult >= 1.5, "🟡 MODERATE TRACTION (" + format(mult) + "x)",
    "🔴 BELOW THRESHOLD (" + format(mult) + "x)"
  ),
  verdict
)
```

### 3.4 Formula 4: Effective Retention Index (`ERI_Score`)
* **Target Database:** `02-Master-Content-Calendar-and-1to15-Waterfall`
* **Required Number Properties:** `CTR_Pct` (e.g., `8.2`), `Retention_30s_Pct` (e.g., `74.5`), `AVD_Pct` (e.g., `54.0`)
* **Copy-Paste Notion Formula 2.0 Expression:**
```javascript
lets(
  eri, round((prop("CTR_Pct") * (prop("Retention_30s_Pct") / 100) * (prop("AVD_Pct") / 100)) * 100) / 100,
  ifs(
    eri >= 2.3, "🟢 ALGORITHMIC EXPANSION (ERI: " + format(eri) + ")",
    eri >= 1.6, "🟡 STABLE BASELINE (ERI: " + format(eri) + ")",
    "🔴 FIX HOOK / THUMBNAIL (ERI: " + format(eri) + ")"
  )
)
```

### 3.5 Formula 5: Omnichannel Sponsorship Package Valuation (`Total_Package_Value_USD`)
* **Target Database:** `04-Sponsorship-CRM-and-Affiliate-Tracker`
* **Required Number Properties:** `Base_Placement_Rate_USD`, `Niche_Authority_Multiplier`, `Omnichannel_AddOns_USD`, `Usage_Rights_Months`, `Exclusivity_Fee_USD`
* **Copy-Paste Notion Formula 2.0 Expression:**
```javascript
lets(
  baseAuth, prop("Base_Placement_Rate_USD") * prop("Niche_Authority_Multiplier"),
  usageFee, prop("Base_Placement_Rate_USD") * 0.30 * prop("Usage_Rights_Months"),
  totalDeal, round(baseAuth + prop("Omnichannel_AddOns_USD") + usageFee + prop("Exclusivity_Fee_USD")),
  "$" + format(totalDeal) + " (Includes $" + format(round(usageFee)) + " Usage Fee)"
)
```

### 3.6 Formula 6: 1-to-15 Waterfall Asset Completion Progress Bar (`Waterfall_Progress`)
* **Target Database:** `02-Master-Content-Calendar-and-1to15-Waterfall`
* **Required Select/Text Properties:** `Pillar_Script_Status`, `Derivative_Shorts_5`, `Derivative_LinkedIn_X_4`, `Derivative_Carousels_3`, `Derivative_Emails_2`
* **Copy-Paste Notion Formula 2.0 Expression:**
```javascript
lets(
  s1, if(contains(prop("Pillar_Script_Status"), "Complete") or contains(prop("Pillar_Script_Status"), "Published"), 1, 0),
  s2, if(contains(prop("Derivative_Shorts_5"), "5/5"), 5, 0),
  s3, if(contains(prop("Derivative_LinkedIn_X_4"), "4/4"), 4, 0),
  s4, if(contains(prop("Derivative_Carousels_3"), "3/3"), 3, 0),
  s5, if(contains(prop("Derivative_Emails_2"), "2/2"), 2, 0),
  doneCount, s1 + s2 + s3 + s4 + s5,
  pct, round((doneCount / 15) * 100),
  bars, repeat("█", round(pct / 10)) + repeat("░", 10 - round(pct / 10)),
  bars + " " + format(doneCount) + "/15 Assets (" + format(pct) + "%)"
)
```

### 3.7 Formula 7: 90-Day Subscriber Value (`V_sub_90d`) & Paid Growth Ceiling
* **Target Database:** `02-Master-Content-Calendar-and-1to15-Waterfall` (or Monthly Funnel Rollup)
* **Required Number Properties:** `Digital_Product_Revenue_90d`, `Affiliate_Revenue_90d`, `Sponsor_Newsletter_Rev_90d`, `Active_Email_Subscribers`
* **Copy-Paste Notion Formula 2.0 Expression:**
```javascript
lets(
  subs, max(prop("Active_Email_Subscribers"), 1),
  totalRev, prop("Digital_Product_Revenue_90d") + prop("Affiliate_Revenue_90d") + prop("Sponsor_Newsletter_Rev_90d"),
  vSub, round((totalRev / subs) * 100) / 100,
  maxCpa, round((vSub * 0.50) * 100) / 100,
  ifs(
    vSub >= 5.00, "🟢 SCALE PAID + ORGANIC ($" + format(vSub) + "/sub | Max CPA: $" + format(maxCpa) + ")",
    vSub >= 3.50, "🟢 HEALTHY MONETIZATION ($" + format(vSub) + "/sub)",
    "🔴 OPTIMIZE WELCOME SEQUENCE ($" + format(vSub) + "/sub < $3.50 Target)"
  )
)
```

### 3.8 Formula 8: Automated Sponsorship Renewal & Proof-of-Performance Alert (`Renewal_Action_Alert`)
* **Target Database:** `04-Sponsorship-CRM-and-Affiliate-Tracker`
* **Required Properties:** `Pipeline_Stage` (Select), `Next_Action_Date` (Date), `Total_Package_Value_USD` (Number)
* **Copy-Paste Notion Formula 2.0 Expression:**
```javascript
lets(
  daysLeft, dateBetween(prop("Next_Action_Date"), now(), "days"),
  ifs(
    empty(prop("Next_Action_Date")), "⚪ SET NEXT ACTION DATE",
    daysLeft < 0, "🚨 OVERDUE BY " + format(abs(daysLeft)) + " DAYS — SEND SCRIPT S08/P49 NOW",
    daysLeft <= 7, "🟠 ACTION DUE IN " + format(daysLeft) + " DAYS ($" + format(prop("Total_Package_Value_USD")) + ")",
    "🟢 SCHEDULED IN " + format(daysLeft) + " DAYS"
  )
)
```

---

## 4. Recommended Filtered Database Views to Create in Notion

To prevent cognitive overload during your 4-Hour Weekly Batch Production Sprint, never work inside unfiltered raw tables. Configure the following six purpose-built database views on your Master Command Center dashboard:

1. **Monday Block 1 View (`Green-Light Outlier Queue` — Table View):**
   * **Source Database:** `01-Outlier-Idea-Bank-and-Hook-Vault`
   * **Filter Rule:** `Validation_Status` contains `GREEN LIGHT` AND `Outlier_Multiplier_M` `>= 2.5`.
   * **Sort Order:** `Outlier_Multiplier_M` descending, then `NMPI_Score` descending.
   * **Operational Usage:** Open this view at 9:00 AM every Monday during Block 1 (`60 minutes`). Pick the top-ranked unscheduled topic, lock your 3 thumbnail words and title before opening your script template, and assign it to the current sprint week.

2. **Tuesday Block 2 View (`Pillar Scripting & Voice DNA Studio` — Gallery View):**
   * **Source Database:** `03-AI-Prompt-and-Script-Vault-62`
   * **Filter Rule:** `Engine_Stage` is `Stage 2: Hook & Packaging` OR `Stage 3: Scripting & Waterfall`.
   * **Card Preview:** Display `ID`, `Title`, `Bracketed_Variables`, and `Primary_Metric_Gate`.
   * **Operational Usage:** Keep this view docked next to your active Pillar Script page on Tuesday morning (`90 minutes`) so you can copy Prompts `P14`–`P28` directly into your LLM workspace with zero context switching.

3. **Wednesday & Thursday Block 3/4 View (`Active 1-to-15 Waterfall Board` — Kanban Board View):**
   * **Source Database:** `02-Master-Content-Calendar-and-1to15-Waterfall`
   * **Group By:** `Stage_Gate_Status` (`Outlier Validated` -> `Script Locked` -> `Batch Recorded` -> `15 Assets Scheduled` -> `Published & Audited`).
   * **Visible Card Properties:** `Pillar_Topic_Title`, `Waterfall_Progress`, `Derivative_Shorts_5`, `Derivative_LinkedIn_X_4`, `Derivative_Carousels_3`, `Derivative_Emails_2`, and `Sponsor_Slot`.
   * **Operational Usage:** Drag your weekly sprint card across the board as your 5 vertical Shorts, 4 text posts, 3 carousels, and 2 email newsletters pass the 12-Point Pre-Flight QA Checklist (`Prompt P38`).

4. **Friday CEO View 1 (`Sponsorship & Affiliate Deal Pipeline` — Board View):**
   * **Source Database:** `04-Sponsorship-CRM-and-Affiliate-Tracker`
   * **Group By:** `Pipeline_Stage` (`Prospect Identified` -> `5-Sentence Pitch Sent` -> `Discovery / Value Call` -> `Contract & Deposit Locked` -> `Live Campaign` -> `Day-14 ROI Report & Renewal`).
   * **Calculate Column Footer:** Set the column footer calculation to **Sum of `Total_Package_Value_USD`** so you have real-time visibility into your contracted quarterly sponsorship pipeline.

5. **Friday CEO View 2 (`Time-Leak & Delegation Elimination Matrix` — Table View):**
   * **Source Database:** `Spreadsheets/sheet1-creator-rpm-and-time-audit`
   * **Filter Rule:** `Delegation_Priority` contains `Immediate` OR `High`.
   * **Sort Order:** `Weekly_Hours_Before_OS` descending.
   * **Operational Usage:** Review during Minute 15–20 of your Friday CEO Review to verify that no manual production task is creeping back above your 4-hour weekly batch ceiling.

6. **Emergency Crisis & Negotiation Quick-Access Bar (`Scripts S01–S12` — List View):**
   * **Source Database:** `03-AI-Prompt-and-Script-Vault-62`
   * **Filter Rule:** `Asset_Type` is `Emergency Script`.
   * **Sort Order:** `ID` ascending (`S01` through `S12`).
   * **Operational Usage:** Pin this compact list view at the top-right of your Command Center so whenever a sponsor requests a "quick CPM rate," tries to sneak perpetual paid-ad whitelisting into a contract, or you face a low-energy production week, the exact verbatim response script is one click away.

---

## 5. Configuring 1-Click Notion Database Automation Buttons

Notion's native **Button** block (`/button`) allows you to automate repetitive weekly page creation without external webhooks. Add these three buttons to the top header of your `Creator & Solopreneur OS — Command Center`:

### 5.1 Button 1: `+ Launch New Weekly 1-to-15 Production Sprint`
* **Trigger Action:** Click Button
* **Step 1 (`Add page to`):** Select `02-Master-Content-Calendar-and-1to15-Waterfall`
* **Step 2 (`Set Default Properties`):**
  * `Pillar_Script_Status` = `Drafting H.E.A.R.T. Outline`
  * `Derivative_Shorts_5` = `0/5 Queued`
  * `Derivative_LinkedIn_X_4` = `0/4 Queued`
  * `Derivative_Carousels_3` = `0/3 Queued`
  * `Derivative_Emails_2` = `0/2 Queued`
  * `Batch_Hours_Logged` = `4.0`
  * `Stage_Gate_Status` = `In Production`
* **Step 3 (`Open page`):** Open the newly created sprint page in **Side Peek** mode pre-populated with your 12-Point Pre-Flight QA Checklist.

### 5.2 Button 2: `+ Log Validated S.I.G.N.A.L. Outlier Idea`
* **Trigger Action:** Click Button
* **Step 1 (`Add page to`):** Select `01-Outlier-Idea-Bank-and-Hook-Vault`
* **Step 2 (`Set Default Properties`):**
  * `Validation_Status` = `PENDING M >= 2.5x CHECK`
  * `Hook_Archetype` = `Contrarian Truth`
* **Step 3 (`Open page`):** Open in **Center Peek** so you can immediately paste the peer channel outlier URL, 14-day view count, and channel median views.

### 5.3 Button 3: `+ Add B2B Sponsor Prospect (5-Sentence Pitch Queue)`
* **Trigger Action:** Click Button
* **Step 1 (`Add page to`):** Select `04-Sponsorship-CRM-and-Affiliate-Tracker`
* **Step 2 (`Set Default Properties`):**
  * `Pipeline_Stage` = `Prospect Identified`
  * `Niche_Authority_Multiplier` = `2.0`
  * `Usage_Rights_Months` = `1`
  * `Attached_Script_ID` = `P47 / S01`

---

## 6. CSV Import, Character Encoding & Formula Troubleshooting Protocol

If you encounter any formatting discrepancies when importing the 5 CSV files into Notion, Google Sheets, or Airtable, apply the following deterministic fixes:

1. **UTF-8 Character Encoding Preservation:** All CSV files in `06-NOTION-TEMPLATES/` are compiled in strict **UTF-8 encoding** with standard RFC 4180 double-quote escaping. If opening a CSV in legacy Microsoft Excel on Windows displays special symbols incorrectly, use **Data -> From Text/CSV -> File Origin: 65001 : Unicode (UTF-8)** instead of double-clicking the raw file.
2. **Converting Imported Text Columns to Number Properties Before Pasting Formulas:** When Notion imports a CSV file, it defaults numeric columns (such as `Outlier_Multiplier_M`, `CTR_Pct`, or `Base_Placement_Rate_USD`) to `Text` properties. Before pasting the **Notion Formula 2.0** snippets from Section 3, click the column header in Notion, select **Edit property -> Type -> Number**, and choose **Number with commas** or **US Dollar** as appropriate.
3. **Preserving Multiline Prompt Templates in `03-AI-Prompt-and-Script-Vault-62.csv`:** Because each of the 62 rows in `03-AI-Prompt-and-Script-Vault-62.csv` contains the complete copy-paste prompt or emergency script inside `Full_Copy_Paste_Template`, enable **Wrap all columns** in your Notion table view (`••• -> Layout -> Wrap all columns`) so the entire prompt specification and bracketed variable list are visible at a glance.
