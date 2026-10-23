#!/usr/bin/env python3
"""
build_phase7.py
Phase 7 Compiler: 5-Database Notion Creator OS Kit & Commercial Cover Suite
Flagship Product #3: The AI Content Creator & Solopreneur Operating System
Studio Root: e:/Ebook-Makaer/AI-Creator-Solopreneur-OS/DIGITAL-PUBLISHING-STUDIO/
"""

import csv
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image
from pypdf import PdfReader, PdfWriter

import build_webapp

STUDIO_ROOT = Path(__file__).resolve().parent
BROWSER_BIN = build_webapp.find_browser_binary()


# ---------------------------------------------------------------------------
# PART A: 5-DATABASE NOTION CREATOR OS KIT & SPREADSHEET BASELINE AUDIT
# ---------------------------------------------------------------------------

def write_csv_file(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for row in rows:
            writer.writerow([str(c) for c in row])


def build_db01_outlier_idea_bank() -> Path:
    out_path = STUDIO_ROOT / "06-NOTION-TEMPLATES/01-Outlier-Idea-Bank-and-Hook-Vault.csv"
    headers = [
        "Idea_ID",
        "Topic_Title",
        "Content_Pillar",
        "Pain_Urgency_1_10",
        "Purchasing_Power_1_10",
        "Info_Gap_1_10",
        "Product_Fit_1_10",
        "NMPI_Score",
        "Peer_Outlier_Views_14d",
        "Peer_Channel_Median_Views",
        "Outlier_Multiplier_M",
        "Validation_Status",
        "Thumbnail_3_Words",
        "CLIP_30s_Hook_Draft",
        "Target_Offer_Bridge",
    ]

    seed_topics = [
        ("IDEA-001", "How I Replaced a 35-Hour Content Week With a 4-Hour AI Batch Sprint", "Pillar 1: Batch Production", 9, 9, 9, 10, 68400, 14200, "4 HRS -> 15 ASSETS", "Show live calendar comparing 35h manual grind vs 4h sprint generating $18.4k/mo.", "Tier 2 Flagship Creator OS ($99)"),
        ("IDEA-002", "Why Daily Posting Destroys Solopreneur Profit Margins (The RPPH Equation)", "Pillar 1: Creator Economics", 9, 9, 8, 9, 52100, 13800, "STOP POSTING DAILY", "Reveal $11.40/hr burnout math vs $248/hr Operator RPPH model in first 15 seconds.", "Tier 0 7-Day RPPH Audit Kit ($0)"),
        ("IDEA-003", "The 5-Day Value-First Welcome Sequence Converting Cold Views Into $99 Buyers", "Pillar 3: Owned Funnels", 10, 9, 9, 10, 74500, 16000, "3.8% WELCOME CVR", "Walk through live ESP telemetry showing $6.42 90-day subscriber value from 5 plain-text emails.", "Tier 2 Welcome Funnel Blueprint ($99)"),
        ("IDEA-004", "How to Price B2B Brand Sponsorships Using Outcome + Usage-Rights Math", "Pillar 4: Monetization", 9, 10, 9, 9, 49800, 11500, "NEVER SELL CPM", "Contrast a $450 commodity CPM read with a $3,540 Omnichannel Outcome Bundle contract.", "Tier 3 Executive Sponsorship Kit ($199)"),
        ("IDEA-005", "The 1-to-15 Omnichannel Waterfall: Turning 1 Pillar Script Into 15 Native Posts", "Pillar 2: Repurposing", 9, 8, 9, 10, 81200, 18500, "1 SCRIPT -> 15 POSTS", "Display the complete 15-asset waterfall board running inside Notion and Claude.", "Tier 2 Creator Operator Pro Bundle ($79)"),
        ("IDEA-006", "How to Calibrate AI to Write in Your Exact Voice DNA (Zero Generic Slop)", "Pillar 2: AI Scripting", 8, 8, 9, 9, 61000, 17200, "CLONE YOUR VOICE", "Side-by-side teardown of raw LLM output vs 5-parameter Voice DNA calibrated script.", "Tier 1 50-Prompt Vault ($29)"),
        ("IDEA-007", "Validate Before You Build: How We Pre-Sold $14,200 Before Recording Module 1", "Pillar 4: Digital Products", 10, 9, 9, 10, 58900, 12900, "$14K BEFORE BUILD", "Show the 1-page Outcome Syllabus and 4-email Founding Member sprint that passed the 10-sale gate.", "Tier 2 Digital Product Playbook ($99)"),
        ("IDEA-008", "The 3-Second C.L.I.P. Hook Formula That Holds 74% of Viewers Past 0:30", "Pillar 2: Packaging & Hooks", 9, 8, 8, 9, 93400, 22000, "74% 30-SEC HOLD", "Overlay live YouTube retention curve flatlining at 74% after the 4-beat C.L.I.P. intro.", "Tier 1 Core Digital Edition ($29)"),
        ("IDEA-009", "Single-Field Opt-In Pages: How Stripping Navigation Lifted Email Capture to 54%", "Pillar 3: Owned Funnels", 8, 9, 8, 9, 43200, 12100, "54% OPT-IN PAGE", "Compare a bloated 12% website page against an above-the-fold single-field utility landing page.", "Tier 2 Funnel Wireframe Pack ($79)"),
        ("IDEA-010", "Checkout Order Bumps & 1-Click Upsells: Adding +45% Revenue Per Customer", "Pillar 4: Digital Products", 9, 10, 8, 10, 47600, 13400, "+45% CART VALUE", "Live Lemon Squeezy / ThriveCart math showing $99 base jumping to $143.47 effective AOV.", "Tier 2 Checkout Stack Calculator ($79)"),
        ("IDEA-011", "The S.I.G.N.A.L. Outlier Mining Protocol: Finding 3x Topics in 15 Minutes", "Pillar 1: Idea Validation", 8, 8, 9, 9, 66300, 15800, "3X OUTLIER RADAR", "Demonstrate live 90-day median calculation across 10 peer channels before writing a single word.", "Tier 0 Outlier Scorer Sheet ($0)"),
        ("IDEA-012", "Why 60-Page PDF eBooks Are Dead (Build 5-Minute Utility Lead Magnets Instead)", "Pillar 3: Owned Funnels", 9, 8, 9, 9, 54100, 14900, "KILL PDF EBOOKS", "Show why interactive calculators and Notion dashboards convert 4x higher than static PDFs.", "Tier 2 Lead Magnet Architect ($79)"),
        ("IDEA-013", "The 20-Minute Friday Creator CEO Review That Protects 85% Net Profit Margins", "Pillar 4: Studio Governance", 8, 9, 8, 9, 39800, 11200, "20-MIN CEO AUDIT", "Walk through the 4 five-minute Friday executive blocks and the 1-task burnout elimination rule.", "Tier 3 Executive Solopreneur Suite ($199)"),
        ("IDEA-014", "Paid Ad Whitelisting & Exclusivity Clauses: Stop Giving Brands Free IP Rights", "Pillar 4: Monetization", 9, 10, 9, 9, 44900, 10800, "CHARGE FOR ADS", "Highlight the exact contract clause that steals perpetual ad rights and the +30%/mo counter-script.", "Tier 1 12 Emergency Scripts Vault ($29)"),
        ("IDEA-015", "The H.E.A.R.T. Scripting Architecture: Eliminating Mid-Video Drop-Off", "Pillar 2: AI Scripting", 8, 8, 8, 9, 57200, 16400, "ZERO MID-ROLL DROP", "Show how 90-second tension-release pattern interrupts keep full-video AVD above 52%.", "Tier 1 Core Digital Edition ($29)"),
        ("IDEA-016", "How to Run a $20k/Month Solopreneur Media Business in 22 Hours a Week", "Pillar 1: Creator Economics", 10, 9, 9, 10, 88500, 19500, "$20K IN 22 HRS", "Full P&L and time-block breakdown across products, sponsorships, and automated email funnels.", "Tier 3 Executive Automation Suite ($199)"),
        ("IDEA-017", "60-Day Cold List Pruning: How Deleting 2,400 Dead Subscribers Saved Our Deliverability", "Pillar 3: Owned Funnels", 8, 9, 8, 8, 36900, 10500, "DELETE DEAD SUBS", "Prove how pruning 60-day unengaged contacts lifted broadcast open rates from 31% to 56%.", "Tier 2 Deliverability Shield SOP ($79)"),
        ("IDEA-018", "The 4-Tier Creator Value Ladder: From $29 Impulse Kit to $2,500 Async Advisory", "Pillar 4: Digital Products", 9, 10, 9, 10, 62400, 14600, "4-TIER VALUE STACK", "Map the exact buyer ascension path from free tool to capped 4-client async retainer.", "Tier 3 Executive Solopreneur Suite ($199)"),
        ("IDEA-019", "Text-Based Video Editing: Cutting 90 Minutes of Raw A-Roll in 25 Minutes", "Pillar 1: Batch Production", 8, 8, 8, 8, 51300, 15200, "EDIT VIA TEXT", "Live Descript/Cursor transcript cut removing filler words and dead air in one pass.", "Tier 2 Batch Production SOP ($79)"),
        ("IDEA-020", "How to Pitch 5 B2B Sponsors Every Friday in 15 Minutes (With 42% Reply Rate)", "Pillar 4: Monetization", 9, 10, 9, 9, 48200, 11900, "5 PITCHES / WK", "Tear down the exact 110-word outbound email and custom 60-second demo concept.", "Tier 3 Sponsorship CRM & Pitch Kit ($199)"),
        ("IDEA-021", "The 3-Link Click Segmentation Matrix: Auto-Tagging Beginners vs High-Ticket Buyers", "Pillar 3: Owned Funnels", 8, 9, 9, 9, 41700, 11400, "AUTO-TAG BUYERS", "Show how Email 2 routes subscribers into 3 tailored offer tracks automatically.", "Tier 2 Welcome Sequence Kit ($79)"),
        ("IDEA-022", "Package-First Creation: Why We Design the Thumbnail & Title Before Researching", "Pillar 2: Packaging & Hooks", 9, 8, 8, 8, 71800, 17800, "THUMBNAIL FIRST", "Explain the Package-First law and show 3 failed videos rescued by title/thumbnail swaps.", "Tier 1 Core Digital Edition ($29)"),
        ("IDEA-023", "The 12-Point Pre-Publish Quality Control Gate (Zero Broken Links or Weak Hooks)", "Pillar 1: Batch Production", 8, 8, 8, 9, 38400, 10900, "12-POINT QA GATE", "Walk through the Thursday 30-minute verification checklist that protects channel authority.", "Tier 2 Action Workbook Suite ($79)"),
        ("IDEA-024", "Day-14 Proof-of-Performance Reports: Turning 1-Off Brand Deals Into 90-Day Retainers", "Pillar 4: Monetization", 9, 10, 9, 9, 45600, 11300, "LOCK 90D RETAINERS", "Show the exact 1-page post-campaign ROI report that converts 50% of sponsors into quarterly deals.", "Tier 3 Sponsorship Retainer Kit ($199)"),
        ("IDEA-025", "How to Delegate Video Editing at $65/hr RPPH Using Modular Style Guides", "Pillar 1: Batch Production", 8, 9, 8, 9, 42900, 12000, "DELEGATE EDITING", "Demonstrate the quantitative RPPH delegation threshold and editor handoff folder architecture.", "Tier 4 Agency & White-Label Suite ($499)"),
    ]

    rows = []
    for item in seed_topics:
        (
            idea_id,
            title,
            pillar,
            pain,
            power,
            gap,
            fit,
            views_14d,
            med_views,
            thumb_3w,
            hook_draft,
            offer_bridge,
        ) = item
        nmpi = round((pain * 2.5) + (power * 3.0) + (gap * 2.0) + (fit * 2.5), 1)
        m_out = round(views_14d / med_views, 2)
        status = "GREEN LIGHT (PRODUCE)" if m_out >= 2.5 and nmpi >= 75 else "VALIDATED QUEUE"
        rows.append([
            idea_id,
            title,
            pillar,
            pain,
            power,
            gap,
            fit,
            f"{nmpi:.1f}",
            views_14d,
            med_views,
            f"{m_out:.2f}x",
            status,
            thumb_3w,
            hook_draft,
            offer_bridge,
        ])

    write_csv_file(out_path, headers, rows)
    return out_path


def build_db02_master_content_calendar() -> Path:
    out_path = STUDIO_ROOT / "06-NOTION-TEMPLATES/02-Master-Content-Calendar-and-1to15-Waterfall.csv"
    headers = [
        "Week_ID",
        "Publish_Date",
        "Pillar_Asset_Title",
        "Pillar_Format",
        "Stage_Gate_Status",
        "Batch_Mon_Research",
        "Batch_Tue_Script",
        "Batch_Wed_Capture",
        "Batch_Thu_QA",
        "Shorts_5_Status",
        "LinkedIn_X_4_Status",
        "Carousels_3_Status",
        "Emails_2_Status",
        "CTR_Pct",
        "Retention_30s_Pct",
        "AVD_Pct",
        "ERI_Score",
        "Email_OptIns_Generated",
        "Attributed_Revenue_USD",
    ]

    weeks_data = [
        ("WK-01", "2026-06-04", "How I Replaced a 35-Hour Content Week With a 4-Hour AI Batch Sprint", "YouTube 14m + Newsletter", "Published", "Complete (45m)", "Complete (75m)", "Complete (90m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 8.2, 74.5, 54.0, 385, 4280),
        ("WK-02", "2026-06-11", "Why Daily Posting Destroys Solopreneur Profit Margins (The RPPH Equation)", "YouTube 12m + Newsletter", "Published", "Complete (45m)", "Complete (70m)", "Complete (85m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 7.6, 72.0, 52.5, 310, 3690),
        ("WK-03", "2026-06-18", "The 5-Day Value-First Welcome Sequence Converting Cold Views Into $99 Buyers", "YouTube 16m + Newsletter", "Published", "Complete (40m)", "Complete (75m)", "Complete (90m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 8.8, 76.2, 55.8, 490, 6120),
        ("WK-04", "2026-06-25", "How to Price B2B Brand Sponsorships Using Outcome + Usage-Rights Math", "YouTube 15m + Newsletter", "Published", "Complete (45m)", "Complete (75m)", "Complete (85m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 7.4, 71.5, 53.0, 295, 5840),
        ("WK-05", "2026-07-02", "The 1-to-15 Omnichannel Waterfall: Turning 1 Pillar Script Into 15 Native Posts", "YouTube 13m + Newsletter", "Published", "Complete (40m)", "Complete (70m)", "Complete (90m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 8.5, 75.0, 54.5, 440, 4950),
        ("WK-06", "2026-07-09", "How to Calibrate AI to Write in Your Exact Voice DNA (Zero Generic Slop)", "YouTube 14m + Newsletter", "Published", "Complete (45m)", "Complete (75m)", "Complete (88m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 7.9, 73.2, 51.8, 360, 4120),
        ("WK-07", "2026-07-16", "Validate Before You Build: How We Pre-Sold $14,200 Before Recording Module 1", "YouTube 17m + Newsletter", "Published", "Complete (45m)", "Complete (75m)", "Complete (90m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 9.1, 77.4, 56.2, 530, 8450),
        ("WK-08", "2026-07-23", "The 3-Second C.L.I.P. Hook Formula That Holds 74% of Viewers Past 0:30", "YouTube 11m + Newsletter", "Published", "Complete (40m)", "Complete (68m)", "Complete (82m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 8.7, 75.8, 53.9, 415, 4690),
        ("WK-09", "2026-07-30", "Single-Field Opt-In Pages: How Stripping Navigation Lifted Email Capture to 54%", "YouTube 12m + Newsletter", "Published", "Complete (42m)", "Complete (72m)", "Complete (85m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 7.5, 71.8, 52.0, 375, 4380),
        ("WK-10", "2026-08-06", "Checkout Order Bumps & 1-Click Upsells: Adding +45% Revenue Per Customer", "YouTube 15m + Newsletter", "Published", "Complete (45m)", "Complete (75m)", "Complete (88m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 8.1, 73.6, 54.1, 390, 6290),
        ("WK-11", "2026-08-13", "The S.I.G.N.A.L. Outlier Mining Protocol: Finding 3x Topics in 15 Minutes", "YouTube 13m + Newsletter", "Published", "Complete (40m)", "Complete (70m)", "Complete (86m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 8.4, 74.1, 53.5, 405, 4510),
        ("WK-12", "2026-08-20", "Why 60-Page PDF eBooks Are Dead (Build 5-Minute Utility Lead Magnets Instead)", "YouTube 14m + Newsletter", "Published", "Complete (45m)", "Complete (74m)", "Complete (89m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 8.0, 72.9, 52.8, 368, 4190),
        ("WK-13", "2026-08-27", "The 20-Minute Friday Creator CEO Review That Protects 85% Net Profit Margins", "YouTube 12m + Newsletter", "Published", "Complete (42m)", "Complete (70m)", "Complete (84m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 7.7, 71.4, 51.9, 325, 4870),
        ("WK-14", "2026-09-03", "Paid Ad Whitelisting & Exclusivity Clauses: Stop Giving Brands Free IP Rights", "YouTube 15m + Newsletter", "Published", "Complete (45m)", "Complete (75m)", "Complete (90m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 7.8, 72.6, 53.4, 342, 5920),
        ("WK-15", "2026-09-10", "The H.E.A.R.T. Scripting Architecture: Eliminating Mid-Video Drop-Off", "YouTube 14m + Newsletter", "Published", "Complete (44m)", "Complete (73m)", "Complete (87m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 8.3, 74.8, 55.1, 398, 4640),
        ("WK-16", "2026-09-17", "How to Run a $20k/Month Solopreneur Media Business in 22 Hours a Week", "YouTube 16m + Newsletter", "Published", "Complete (45m)", "Complete (75m)", "Complete (90m)", "Passed (12/12)", "5/5 Published", "4/4 Published", "3/3 Published", "2/2 Sent", 9.3, 78.1, 56.8, 560, 9120),
        ("WK-17", "2026-09-24", "60-Day Cold List Pruning: How Deleting 2,400 Dead Subscribers Saved Deliverability", "YouTube 12m + Newsletter", "Scheduled (Buffer Wk 1)", "Complete (40m)", "Complete (70m)", "Complete (85m)", "Passed (12/12)", "5/5 Scheduled", "4/4 Scheduled", "3/3 Scheduled", "2/2 Queued", 7.9, 73.0, 52.4, 350, 4100),
        ("WK-18", "2026-10-01", "The 4-Tier Creator Value Ladder: From $29 Impulse Kit to $2,500 Async Advisory", "YouTube 15m + Newsletter", "Scheduled (Buffer Wk 2)", "Complete (45m)", "Complete (75m)", "Complete (88m)", "Passed (12/12)", "5/5 Scheduled", "4/4 Scheduled", "3/3 Scheduled", "2/2 Queued", 8.6, 75.2, 54.7, 430, 6850),
        ("WK-19", "2026-10-08", "Text-Based Video Editing: Cutting 90 Minutes of Raw A-Roll in 25 Minutes", "YouTube 13m + Newsletter", "Scheduled (Buffer Wk 3)", "Complete (42m)", "Complete (72m)", "Complete (86m)", "Passed (12/12)", "5/5 Scheduled", "4/4 Scheduled", "3/3 Scheduled", "2/2 Queued", 8.1, 73.5, 53.2, 380, 4420),
        ("WK-20", "2026-10-15", "How to Pitch 5 B2B Sponsors Every Friday in 15 Minutes (With 42% Reply Rate)", "YouTube 14m + Newsletter", "In Production (Next Sprint)", "Complete (45m)", "Complete (75m)", "In Progress", "Pending Thu QA", "3/5 Ready", "2/4 Ready", "2/3 Ready", "1/2 Drafted", 8.4, 74.0, 54.0, 410, 5600),
    ]

    rows = []
    for w in weeks_data:
        (
            wk_id,
            p_date,
            title,
            fmt,
            gate,
            b_mon,
            b_tue,
            b_wed,
            b_thu,
            s5,
            lx4,
            c3,
            e2,
            ctr,
            ret30,
            avd,
            optins,
            rev,
        ) = w
        eri = round(ctr * (ret30 / 100.0) * (avd / 100.0), 2)
        rows.append([
            wk_id,
            p_date,
            title,
            fmt,
            gate,
            b_mon,
            b_tue,
            b_wed,
            b_thu,
            s5,
            lx4,
            c3,
            e2,
            f"{ctr:.1f}%",
            f"{ret30:.1f}%",
            f"{avd:.1f}%",
            f"{eri:.2f}",
            optins,
            f"${rev:,}",
        ])

    write_csv_file(out_path, headers, rows)
    return out_path


def build_db03_prompt_and_script_vault_62() -> Path:
    out_path = STUDIO_ROOT / "06-NOTION-TEMPLATES/03-AI-Prompt-and-Script-Vault-62.csv"
    headers = [
        "Asset_ID",
        "Asset_Type",
        "Title",
        "Chapter_Source",
        "Engine_Stage",
        "Primary_Use_Case",
        "Input_Variables",
        "Full_Copy_Paste_Template",
    ]
    prompts_list, scripts_list, _ = build_webapp.load_prompts_and_scripts()
    rows = []

    for p in prompts_list:
        vars_str = ", ".join(f"[{v}]" for v in p["variables"]) if p["variables"] else "[NONE]"
        rows.append([
            p["id"],
            "AI Workflow Prompt",
            p["title"],
            f"Chapter {p['chapter']:02d}",
            p["stage"],
            p["role"],
            vars_str,
            p["body"],
        ])

    for s in scripts_list:
        vars_str = ", ".join(f"[{v}]" for v in s["variables"]) if s["variables"] else "[NONE]"
        rows.append([
            s["id"],
            "Emergency Communication Script",
            s["title"],
            "Back Matter Vault (Appendix B)",
            "Stage 5: Commercial & Crisis Protection",
            s["scenario"],
            vars_str,
            s["body"],
        ])

    if len(rows) != 62:
        raise RuntimeError(f"Expected exactly 62 rows in 03-AI-Prompt-and-Script-Vault-62.csv, got {len(rows)}")

    write_csv_file(out_path, headers, rows)
    return out_path


def build_db04_sponsorship_crm() -> Path:
    out_path = STUDIO_ROOT / "06-NOTION-TEMPLATES/04-Sponsorship-CRM-and-Affiliate-Tracker.csv"
    headers = [
        "Deal_ID",
        "Brand_Name",
        "Category",
        "Contact_Role",
        "Deal_Type",
        "Base_Placement_Rate_USD",
        "Niche_Authority_Multiplier",
        "Omnichannel_AddOns_USD",
        "Usage_Rights_Months",
        "Usage_Rights_Fee_USD",
        "Exclusivity_Fee_USD",
        "Total_Package_Value_USD",
        "Pipeline_Stage",
        "Deliverables_Summary",
        "Invoice_Status",
        "Renewal_Date",
    ]

    deals_seed = [
        ("SPON-001", "LinearFlow AI", "B2B Workflow SaaS", "Head of Creator Partnerships", "Tier B: Omnichannel Bundle", 1800, 1.25, 650, 1, 350, "Published & Completed", "1x 60s YouTube Mid-Roll + 1x Primary Newsletter + 2x Shorts + 30d Whitelisting", "100% Paid ($3,340)", "2026-11-15"),
        ("SPON-002", "MetricPulse Analytics", "Creator Telemetry SaaS", "VP of Growth Marketing", "Tier C: 90-Day Retainer", 5400, 1.30, 1800, 3, 900, "Active Quarterly Partner", "3x Pillar Integrations + 3x Newsletter Top Slots + 6x Shorts + 90d Exclusivity", "50% Deposit Paid ($12,726)", "2027-01-10"),
        ("SPON-003", "Descript Studio Pro", "AI Video & Audio Editor", "Partner Marketing Lead", "Hybrid Base + 25% RevShare", 1500, 1.20, 450, 1, 0, "Published & Completed", "1x Live Editing Workflow Demo + Newsletter Feature + Custom Affiliate Link", "100% Paid ($2,700)", "2026-11-20"),
        ("SPON-004", "Kit (ConvertKit)", "Email Service Provider", "Creator Ecosystem Director", "Tier B: Omnichannel Bundle", 2000, 1.25, 750, 2, 400, "Contract Signed", "1x Welcome Funnel Tutorial Demo + 2x Newsletter Slots + 60d Spark Ads", "50% Deposit Paid ($4,850)", "2026-12-05"),
        ("SPON-005", "Beehiiv Media", "Newsletter Platform", "Brand Partnerships Manager", "Tier A: Validation Sprint", 1600, 1.20, 400, 0, 0, "Published & Completed", "1x 60s Mid-Roll + Pinned Comment Link + 1x Newsletter Primary Box", "100% Paid ($2,320)", "2026-11-01"),
        ("SPON-006", "Make.com Enterprise", "Workflow Automation", "Demand Gen Lead", "Tier C: 90-Day Retainer", 6000, 1.30, 2100, 3, 1200, "Active Quarterly Partner", "3x Automation Blueprint Videos + 3x Newsletters + 90d Ad Usage Rights", "100% Paid ($16,500)", "2027-01-25"),
        ("SPON-007", "n8n Cloud", "AI Agent Automation", "Developer Relations Lead", "Tier B: Omnichannel Bundle", 1900, 1.30, 600, 1, 300, "Script Approved", "1x Local Agent Build Demo + 1x Newsletter + 1x LinkedIn Carousel + 30d Ads", "50% Deposit Paid ($3,940)", "2026-12-12"),
        ("SPON-008", "Lemon Squeezy", "Digital Commerce MoR", "Growth Partnerships Lead", "Tier B: Omnichannel Bundle", 1750, 1.25, 550, 1, 250, "Published & Completed", "1x Checkout AOV Stack Demo + 1x Newsletter Slot + 2x Vertical Clips", "100% Paid ($3,512)", "2026-11-18"),
        ("SPON-009", "Notion Labs", "Workspace OS", "Creator Program Manager", "Hybrid Base + Affiliate", 2200, 1.30, 800, 2, 0, "Published & Completed", "1x 5-Database Creator OS Walkthrough + Template Link + 60d Whitelisting", "100% Paid ($4,980)", "2026-12-01"),
        ("SPON-010", "Riverside.fm", "4K Studio Recording", "Influencer Marketing Lead", "Tier A: Validation Sprint", 1500, 1.15, 350, 0, 0, "Published & Completed", "1x Batch Recording Setup Demo + Pinned UTM Link + Newsletter Callout", "100% Paid ($2,075)", "2026-11-08"),
        ("SPON-011", "Framer Web", "Landing Page Builder", "Head of Brand Deals", "Tier B: Omnichannel Bundle", 1850, 1.20, 600, 1, 300, "Proposal Sent", "1x Opt-In Page Wireframe Build + Newsletter Feature + 30d Paid Ad Rights", "Awaiting Signature ($3,675)", "2026-12-15"),
        ("SPON-012", "Raycast Pro", "Productivity Launcher", "Community Growth Lead", "Tier A: Validation Sprint", 1400, 1.20, 300, 0, 0, "Published & Completed", "1x Solopreneur Speed Workflow Integration + Newsletter Box", "100% Paid ($1,980)", "2026-11-22"),
        ("SPON-013", "Superhuman Mail", "AI Executive Inbox", "B2B Partnerships Lead", "Tier B: Omnichannel Bundle", 2100, 1.25, 700, 1, 400, "Negotiating Usage Rights", "1x Friday Creator CEO Inbox Zero Demo + Newsletter + 30d Whitelisting", "Drafting Contract ($4,355)", "2026-12-20"),
        ("SPON-014", "ScreenStudio macOS", "High-Retention Screen Rec", "Founder & CEO", "Hybrid Base + 30% Affiliate", 1300, 1.20, 350, 1, 0, "Published & Completed", "1x Tutorial Pacing & Zoom-Keyframe Demo + Evergreen Affiliate Link", "100% Paid ($2,300)", "2026-11-30"),
        ("SPON-015", "Clay.com Outbound", "AI Prospecting Engine", "VP Marketing", "Tier C: 90-Day Retainer", 5800, 1.35, 1950, 3, 1000, "Contract Signed", "3x Outbound Sponsorship Automation Demos + 3x Newsletters + 90d Whitelisting", "50% Deposit Paid ($16,000)", "2027-02-01"),
        ("SPON-016", "ThriveCart Pro", "Checkout & Upsell Engine", "Affiliate & Partner Director", "Hybrid Base + RevShare", 1650, 1.25, 500, 1, 250, "Published & Completed", "1x 1-Click Upsell Funnel Walkthrough + Newsletter + 30d Ad Usage", "100% Paid ($3,308)", "2026-11-28"),
        ("SPON-017", "Perplexity Pro", "AI Research Engine", "Growth Marketing Lead", "Tier B: Omnichannel Bundle", 2000, 1.25, 650, 1, 350, "Script Approved", "1x S.I.G.N.A.L. Research Sprint Demo + Newsletter + 2x Shorts", "50% Deposit Paid ($4,100)", "2026-12-18"),
        ("SPON-018", "Loom Enterprise", "Async Video Communication", "Lifecycle Marketing Lead", "Tier A: Validation Sprint", 1600, 1.20, 400, 0, 0, "Proposal Sent", "1x Async Advisory & Editor Delegation Demo + Newsletter Slot", "Proposal Under Review ($2,320)", "2026-12-22"),
        ("SPON-019", "Senja.io", "Testimonial Capture", "Co-Founder", "Hybrid Base + 30% Recurring", 1250, 1.20, 300, 1, 0, "Published & Completed", "1x Day-21 Automated Testimonial Capture Demo + Newsletter Callout", "100% Paid ($2,175)", "2026-11-14"),
        ("SPON-020", "Mercury Bank", "B2B Creator Banking", "Head of Media Partnerships", "Tier C: 90-Day Retainer", 6500, 1.35, 2200, 3, 1500, "Active Quarterly Partner", "3x Solopreneur P&L & Cashflow Demos + 3x Newsletters + 90d FinTech Exclusivity", "100% Paid ($18,325)", "2027-02-15"),
    ]

    rows = []
    for d in deals_seed:
        (
            did,
            brand,
            cat,
            role,
            dtype,
            base_usd,
            m_auth,
            addons_usd,
            u_mo,
            excl_usd,
            stage,
            deliv,
            inv,
            renew,
        ) = d
        u_fee = round(base_usd * 0.30 * u_mo)
        total_val = round((base_usd * m_auth) + addons_usd + u_fee + excl_usd)
        rows.append([
            did,
            brand,
            cat,
            role,
            dtype,
            f"${base_usd:,}",
            f"{m_auth:.2f}x",
            f"${addons_usd:,}",
            u_mo,
            f"${u_fee:,}",
            f"${excl_usd:,}",
            f"${total_val:,}",
            stage,
            deliv,
            inv,
            renew,
        ])

    write_csv_file(out_path, headers, rows)
    return out_path


def build_sheet1_rpm_and_time_audit() -> Path:
    out_path = STUDIO_ROOT / "06-NOTION-TEMPLATES/Spreadsheets/sheet1-creator-rpm-and-time-audit.csv"
    headers = [
        "Audit_Entry_ID",
        "Week_Day",
        "Operational_Stage",
        "Specific_Task_Activity",
        "Baseline_Manual_Hours",
        "Systematized_OS_Hours",
        "Hours_Saved_Weekly",
        "Task_Value_Tier",
        "Automation_Prompt_ID",
        "Monthly_Views_Attributed",
        "Email_OptIns_Captured",
        "Direct_Revenue_Attributed_USD",
        "Baseline_RPPH_USD",
        "Systematized_RPPH_USD",
        "Action_Gate_Decision",
    ]

    audit_rows_seed = [
        ("AUD-01", "Monday", "Stage 1: Niche & Avatar", "Competitor Channel Audit & ICP Pain Matrix", 2.5, 0.4, "$100/hr Strategic", "P06, P07", 4500, 85, 650, "Automate via Prompt P06"),
        ("AUD-02", "Monday", "Stage 2: Outlier Research", "Scanning 10 Peer Channels for >=2.5x Outliers", 3.5, 0.5, "$100/hr Strategic", "P11, P12", 12000, 220, 1450, "Lock 45m Monday Sprint"),
        ("AUD-03", "Monday", "Stage 2: Packaging & Hooks", "Drafting 10 Title Angles & 3-Word Thumbnail Specs", 2.0, 0.4, "$1,000/hr High-Return", "P16, P17", 18500, 340, 2200, "Enforce Package-First Gate"),
        ("AUD-04", "Monday", "Stage 2: Hook Engineering", "Scripting First-30-Second C.L.I.P. Hook Beats", 1.5, 0.3, "$1,000/hr High-Return", "P18", 15000, 290, 1950, "Verify >=70% 30s Hold"),
        ("AUD-05", "Tuesday", "Stage 3: Pillar Scripting", "Outlining H.E.A.R.T. Narrative & Pattern Interrupts", 4.0, 0.8, "$1,000/hr High-Return", "P21, P22", 14000, 260, 1800, "Use 75m Tuesday Block"),
        ("AUD-06", "Tuesday", "Stage 3: Voice Calibration", "Editing AI Drafts With 5-Parameter Voice DNA Card", 2.5, 0.5, "$100/hr Strategic", "P23, P24", 8000, 150, 1100, "Apply Voice DNA Checklist"),
        ("AUD-07", "Tuesday", "Stage 4: Mid-Roll CTA", "Writing 15-Second Native Lead Magnet Bridge Callout", 1.0, 0.2, "$1,000/hr High-Return", "P25", 9500, 310, 2400, "Embed at 65% Video Mark"),
        ("AUD-08", "Wednesday", "Stage 4: Batch Recording", "Lighting, Audio Check & Filming 2 Pillar Videos", 4.5, 1.5, "$1,000/hr High-Return", "P31", 22000, 410, 3100, "Batch Film 2 Pillars/Wed"),
        ("AUD-09", "Wednesday", "Stage 4: Rough-Cut Edit", "Removing Silences, Retakes & Filler Words", 5.0, 0.6, "$10/hr Admin/Edit", "P32", 5000, 90, 400, "Automate via Text-Cut"),
        ("AUD-10", "Wednesday", "Stage 4: B-Roll & Captions", "Adding Dynamic Diagrams, Lower-Thirds & Captions", 4.5, 0.8, "$10/hr Admin/Edit", "P33", 6000, 110, 550, "Delegate at >=$65/hr RPPH"),
        ("AUD-11", "Thursday", "Stage 3: Short-Form Clips", "Extracting 5 Vertical Shorts (60s Myth/Math Clips)", 3.5, 0.4, "$100/hr Strategic", "P26, P27", 28000, 380, 1750, "Run 1-to-15 Prompt P26"),
        ("AUD-12", "Thursday", "Stage 3: Written Posts", "Rewriting Pillar Into 4 LinkedIn & X Authority Threads", 3.0, 0.4, "$100/hr Strategic", "P28", 16000, 270, 1600, "Run Waterfall Prompt P28"),
        ("AUD-13", "Thursday", "Stage 3: Visual Carousels", "Formatting 3 LinkedIn PDF Slide Decks & Cheat Sheets", 2.5, 0.4, "$100/hr Strategic", "P29", 11500, 195, 1250, "Use Modular SVG Template"),
        ("AUD-14", "Thursday", "Stage 4: Newsletter Issue", "Drafting Thursday Authority Newsletter + Offer Bridge", 2.5, 0.5, "$1,000/hr High-Return", "P30", 8500, 240, 2850, "Sync With Weekly Pillar"),
        ("AUD-15", "Thursday", "Stage 4: Pre-Publish QA", "Running 12-Point QA Gate, Timestamps & UTM Links", 1.5, 0.5, "$100/hr Strategic", "P34, P35", 7500, 180, 1300, "Enforce 12/12 QA Gate"),
        ("AUD-16", "Friday", "Stage 4: Lead Magnet Build", "Maintaining 5-Minute Utility Asset & Opt-In Page", 2.0, 0.3, "$1,000/hr High-Return", "P36, P37", 9000, 450, 3200, "Verify >=45% Opt-In CVR"),
        ("AUD-17", "Friday", "Stage 4: Welcome Sequence", "Auditing 5-Email Welcome Funnel Open & Buyer CVR", 1.5, 0.3, "$1,000/hr High-Return", "P38, P39", 6500, 320, 3900, "Maintain >=2.5% Buyer CVR"),
        ("AUD-18", "Friday", "Stage 4: List Hygiene", "Running 60-Day Cold Subscriber Pruning Rule", 1.0, 0.1, "$10/hr Admin/Edit", "P40", 3000, 60, 450, "Automate ESP Suppression"),
        ("AUD-19", "Friday", "Stage 5: Product Ladder", "Optimizing Tier 1 ($29) & Tier 2 ($99) Checkout Stack", 2.0, 0.4, "$1,000/hr High-Return", "P41, P44", 7000, 210, 4600, "Verify >=30% Bump Take"),
        ("AUD-20", "Friday", "Stage 5: Launch Validation", "Executing 14-Day Validate-Before-You-Build Campaign", 3.0, 0.6, "$1,000/hr High-Return", "P42, P43", 10500, 290, 5400, "Require >=10 Pre-Sales"),
        ("AUD-21", "Friday", "Stage 5: Buyer Ascension", "Day-21 Automated Check-In & Tier 3/4 Sprint Invite", 1.5, 0.2, "$1,000/hr High-Return", "P45", 4000, 110, 3800, "Automate Day-21 Trigger"),
        ("AUD-22", "Friday", "Stage 5: Sponsor Radar", "Identifying 5 Funded B2B SaaS Sponsor Prospects", 1.5, 0.2, "$1,000/hr High-Return", "P46", 3500, 75, 2900, "Min 10-15 Friday CEO"),
        ("AUD-23", "Friday", "Stage 5: Outbound Pitches", "Sending 5 Custom 110-Word Outbound Sponsor Pitches", 2.0, 0.3, "$1,000/hr High-Return", "P47, P48", 5500, 120, 4200, "Enforce R_sponsor Floor"),
        ("AUD-24", "Friday", "Stage 5: Sponsor Renewal", "Sending Day-14 ROI Reports & 90-Day Retainer Upsells", 1.0, 0.2, "$1,000/hr High-Return", "P49", 4200, 95, 5100, "Convert 50% to Retainers"),
        ("AUD-25", "Friday", "Stage 5: CEO Governance", "20-Minute Friday Creator CEO KPI Scorecard & Kill Rule", 1.0, 0.3, "$1,000/hr High-Return", "P50", 6000, 140, 2600, "Eliminate 1 Low-ROI Task"),
    ]

    rows = []
    for r in audit_rows_seed:
        (
            aid,
            day,
            stage,
            task,
            base_h,
            sys_h,
            tier,
            pids,
            views,
            optins,
            rev,
            decision,
        ) = r
        saved_h = round(base_h - sys_h, 1)
        base_rpph = round(rev / (base_h * 4.0), 2)
        sys_rpph = round(rev / (sys_h * 4.0), 2)
        rows.append([
            aid,
            day,
            stage,
            task,
            f"{base_h:.1f}",
            f"{sys_h:.1f}",
            f"{saved_h:.1f}",
            tier,
            pids,
            views,
            optins,
            f"${rev:,}",
            f"${base_rpph:.2f}/hr",
            f"${sys_rpph:.2f}/hr",
            decision,
        ])

    write_csv_file(out_path, headers, rows)
    return out_path


def build_db05_monetization_and_launch_hub_md() -> Path:
    out_path = STUDIO_ROOT / "06-NOTION-TEMPLATES/05-Creator-Monetization-and-Launch-Hub.md"
    content = r"""# 05 — The Creator Monetization, 4-Tier Value Ladder & 14-Day Launch Command Hub

> **Notion Master Command Center Page (`05-Creator-Monetization-and-Launch-Hub.md`)**
> * **Product ID:** `PRODUCT-03-AI-CREATOR-SOLOPRENEUR-OS`
> * **Connected Databases:** `01-Outlier-Idea-Bank`, `02-Master-Content-Calendar`, `03-AI-Prompt-and-Script-Vault-62`, `04-Sponsorship-CRM`
> * **Core Governance Cadence:** 4-Hour Weekly Batch Production Sprint (Mon–Thu) + 20-Minute Friday Creator CEO Review

---

## 1. Executive Mission & The Content-to-Cash Operating Law

Welcome to the central monetization and executive governance hub of **The AI Content Creator & Solopreneur Operating System**. Most independent creators fail to build durable wealth not because they lack work ethic, but because they operate without an owned conversion bridge or a multi-tier commercial value ladder. When you rely solely on platform AdSense or one-off flat-fee brand reads, you need millions of monthly views just to replace a mid-level corporate salary.

This Notion Command Center unifies **Stage 4 (Audience Ownership & Automated Welcome Funnels)** and **Stage 5 (4-Tier Digital Product Architecture, Outcome Sponsorships & Friday CEO Governance)** into four operational dashboards that you can duplicate directly into your Notion workspace:

1. **The 4-Tier Creator Value Ladder & Checkout AOV Architecture Matrix**
2. **The 14-Day Validate-Before-You-Build Pre-Sale Launch Protocol**
3. **The 5-Email Value-First Welcome Funnel & Intent Segmentation Tracker**
4. **The 20-Minute Friday Creator CEO Scorecard & Bottleneck Elimination SOP**

---

## 2. Dashboard 1: The 4-Tier Creator Value Ladder & Checkout AOV Stack

Never offer a single flat-priced product in isolation. A prospect who discovered your channel 48 hours ago has a different trust threshold than an established B2B operator who has read 20 of your newsletters. By structuring your intellectual property into four modular tiers—where **you build the flagship system once** and package it by implementation depth—you capture impulse buyers at the bottom of the ladder while ascending high-margin buyers into premium sprints and retainers.

### 2.1 Master 4-Tier Product Ecosystem Table

| Value Ladder Tier | Target Price Range | Flagship Deliverable Architecture | Target Buyer Conversion Floor | Primary Acquisition Bridge |
| :--- | :---: | :--- | :---: | :--- |
| **Tier 0: 5-Minute Utility Lead Magnet** | `$0` *(Free Entry)* | Interactive Calculator Sheet, 1-Page Visual Blueprint, or 5-Prompt Starter Kit (`<= 5 min` time-to-value) | `45% – 62%` of Opt-In Landing Page Visitors | Mid-roll video callout + pinned comment + social bio link |
| **Tier 1: Impulse Utility Kit & Tripwire** | `$27 – $49` | Core Digital Manual (`PDF` + `EPUB`) + 10 Fillable Action Worksheets + 50-Prompt Vault | `4.0% – 8.0%` of New Email Subscribers | Thank-you page instant offer + Welcome Sequence Emails 4 & 5 (`Beginner` tag) |
| **Tier 2: Flagship Operating System Bundle** | `$79 – $249` | Everything in Tier 1 **PLUS** Offline Web Companion App (`creator-os-app.html`), 5-Database Notion Kit & Financial Trackers | `1.5% – 3.5%` of Active Email List | Welcome Sequence Emails 4 & 5 (`Operator` tag) + Thursday Newsletter Bridge |
| **Tier 3: Implementation Sprint & Automation Suite** | `$497 – $997` | Everything in Tier 2 **PLUS** n8n/Make JSON Automation Blueprints, 14-Day Cohort Sprint or Async Teardown Audit | `10% – 20%` of Tier 2 Customers | Day-21 Automated Buyer Check-In (`P45`) + `High-Ticket` Intent Tag |
| **Tier 4: Capped Executive Advisory Retainer** | `$1,500 – $5,000/mo` | Monthly Async Loom Funnel/Channel Audits + Direct Slack Access (Strictly capped at `<= 4` active clients) | `2% – 5%` of Tier 2/3 Buyers | Direct application link inside Tier 3 onboarding & Back Matter |

### 2.2 The Checkout Stack & Effective AOV ($\text{AOV}_{\text{effective}}$) Blueprint

Before driving a single visitor to your checkout page on Lemon Squeezy, Gumroad, ThriveCart, or Stripe, configure both checkout expansion levers governed by Chapter 9's **Effective Average Order Value Equation**:

$$\text{AOV}_{\text{effective}} = P_{\text{core}} + \left(P_{\text{bump}} \times C_{\text{bump}}\right) + \left(P_{\text{upsell}} \times C_{\text{upsell}}\right)$$

* **Lever 1 — The 1-Click Checkout Order Bump (`$19 – $37`, Target Take Rate `25% – 42%`):**
  * **Rule:** Never offer "more theory" as an order bump. Offer an **Execution Accelerator** (e.g., *The 62 Copy-Paste Notion & Excel Prompt/Script Database + 10 Pre-Built Hook Templates*) priced at `25% to 40%` of your core offer.
  * **Copy Constraint:** Maximum `45 words` inside a dashed highlight box directly above the payment button.
* **Lever 2 — The Post-Purchase 1-Click Upsell (`$97 – $197`, Target Take Rate `12% – 22%`):**
  * **Rule:** Displayed immediately after the initial card charge succeeds, before the final download receipt screen, requiring zero card re-entry.
  * **Positioning:** Solves the *next logical bottleneck* created by the core purchase (e.g., *The Production-Ready n8n & Make.com JSON Automation Blueprints + 12-Month Living Vault Pass*).

---

## 3. Dashboard 2: The 14-Day Validate-Before-You-Build Launch Protocol

Amateur creators spend 6 months recording 40 course videos in a cave, launch to crickets, and burn out. Professional Creator Operators enforce the **Validate-Before-You-Build Rule**: you never produce Modules 1 through 5 until at least **10 paying customers** (or **`$1,000+` in pre-sale revenue**) have voted with their credit cards during a 7-day Founding Member pre-sale sprint.

### 3.1 Complete 14-Day Sprint Execution Checklist

#### Phase A: Days 1–3 — Outcome Syllabus & Pre-Sale Checkout Wiring (`0%` Module Production)
- [ ] **Day 1 (90 Mins):** Run **Prompt `P41`** in `03-AI-Prompt-and-Script-Vault-62` to lock the 5-Module Outcome Syllabus, naming the exact tangible template or calculator delivered in each module.
- [ ] **Day 2 (60 Mins):** Run **Prompt `P42`** to generate the 1-Page Founding Member Pre-Sale Page and configure a pre-order checkout link at a **`40%` Founding Member discount** (e.g., `$59` pre-sale vs. `$99` full retail, capped at 50 spots).
- [ ] **Day 3 (45 Mins):** Run **Prompt `P44`** to wire the 1-Click Order Bump (`$27`) and Post-Purchase 1-Click Upsell (`$97`) onto the pre-sale checkout flow and verify with a live `$1` test transaction.

#### Phase B: Days 4–7 — The 4-Email Founding Member Validation Sprint (**Gate 1 Audit on Day 7**)
- [ ] **Day 4 (Email 1 — The Quantified Cost of the Status Quo):** Send Founding Member Email 1 quantifying the weekly hours and dollars lost to manual workflows; open the 50 Founding Member passes.
- [ ] **Day 5 (Email 2 — Inside the 5-Module Architecture):** Walk through the module-by-module deliverables and answer the #1 implementation speed question.
- [ ] **Day 6 (Email 3 — Case Study & Unit Economics Proof):** Share a concrete Before/After breakdown demonstrating the exact RPPH and revenue lift.
- [ ] **Day 7 (Email 4 — Final 12-Hour Founding Price Close + GATE 1 VERIFICATION):** Close the Founding Member discount window at midnight and audit total pre-sales against **Validation Gate 1**:
  * **GO CONDITION (`>= 10` Paid Units OR `>= $1,000` Gross Pre-Sale Revenue):** Proceed immediately to Phase C (Days 8–13 Modular Build Sprint).
  * **KILL / PIVOT CONDITION (`< 10` Paid Units AND `< $1,000` Revenue):** Do **not** spend 40 hours building an unvalidated product. Issue an immediate `100%` refund to early buyers with a personal thank-you email, send a 1-question objection poll to non-buyers, and pivot the offer angle.

#### Phase C: Days 8–14 — Modular Asset Production, Live Delivery & Evergreen Bridge Installation
- [ ] **Days 8–10 (Core Build Part 1):** Produce Modules 1–3 action checklists, Notion/Excel templates, and concise `< 12-minute` Loom walkthroughs.
- [ ] **Days 11–13 (Core Build Part 2):** Produce Modules 4–5, finalize the Order Bump and Upsell delivery folders, and verify all download links in an incognito browser session.
- [ ] **Day 14 (Fulfillment & Evergreen Switch):** Deliver full access to Founding Member buyers, raise the checkout price to full retail (`$99–$249`), embed the offer into **Welcome Sequence Emails 4 & 5**, and activate the **Day-21 Automated Testimonial & Tier 3 Ascension Trigger (`P45`)**.

---

## 4. Dashboard 3: The 5-Email Value-First Welcome Funnel & Intent Matrix

Every new subscriber who opts in for your Tier 0 Lead Magnet enters your automated **5-Day E.N.G.A.G.E. Welcome Sequence** (`Prompts P38 & P39`). Use the tracking table below during your Friday review to ensure every email exceeds studio deliverability and conversion floors:

| Sequence Step & Timing | Strategic Mechanism | Target Open Rate Floor | Target Link CTR Floor | Dynamic Offer / Tag Routing | Current 30-Day Actual |
| :--- | :--- | :---: | :---: | :--- | :---: |
| **Email 1 (`T + 0 min`)** | Instant Lead Magnet delivery in Line 2 + reply trigger + 60s quick win | `>= 65.0%` | `>= 35.0%` | Delivers Tier 0 Asset + Whitelists sender | `[____]% Open / [____]% CTR` |
| **Email 2 (`T + 24 hrs`)** | Contrarian myth-bust + **3-Link Self-Segmentation Matrix** | `>= 55.0%` | `>= 12.0%` | Tags clickers: `Beginner`, `Operator`, or `High-Ticket` | `[____]% Open / [____]% CTR` |
| **Email 3 (`T + 48 hrs`)** | Quantitative case study + proprietary system walkthrough | `>= 50.0%` | `>= 6.0%` | Previews Flagship System syllabus | `[____]% Open / [____]% CTR` |
| **Email 4 (`T + 72 hrs`)** | Direct Problem-Agitate-System pitch dynamically matched to Intent Tag | `>= 48.0%` | `>= 5.0%` | Routes to Tier 1 (`$29`), Tier 2 (`$99`), or Tier 3 (`$697`) | `[____]% Open / [____]% CTR` |
| **Email 5 (`T + 96 hrs`)** | Top 3 buyer objection teardown + 48-hour Fast-Action Bonus expiry | `>= 45.0%` | `>= 4.5%` | Enforces `>= 2.5%` cumulative welcome buyer CVR | `[____]% Open / [____]% CVR` |

---

## 5. Dashboard 4: The 20-Minute Friday Creator CEO Operating Cadence

Every Friday at 2:00 PM, close your editing software and social feeds and run this strict **20-Minute Executive Review** (`Prompt P50`):

1. **Minutes 0–5 (Acquisition & Retention Telemetry Audit):** Log your weekly Pillar upload's Outlier Multiplier ($M_{\text{outlier}} \ge 2.0\times$), 30-second hook hold rate ($\ge 68\%$), and full-video Average View Duration ($\ge 50\%$) into `02-Master-Content-Calendar`.
2. **Minutes 5–10 (Owned List & Checkout Yield Audit):** Verify landing page opt-in rate ($\ge 45\%$), net new email subscribers, 5-day welcome sequence buyer conversion ($\ge 2.5\%$), and 90-day Subscriber Value ($V_{\text{sub}} \ge \$3.50$).
3. **Minutes 10–15 (Outbound Sponsorship & Renewal Sprint):** Filter `04-Sponsorship-CRM` for 5 qualified B2B brands, send five customized 110-word outbound pitches (`Prompt P47`), and send Day-14 Proof-of-Performance ROI reports (`Prompt P49`) to active partners.
4. **Minutes 15–20 (P&L Margin Check & The 1-Task Burnout Elimination Rule):** Calculate weekly RPPH (`Net Profit / Total Weekly Hours`). If total hours worked exceeded **`25.0 hours`**, identify the single lowest-return manual task and either **Delete**, **Automate** (via Chapter 6/7 prompts), or **Delegate** it before Monday morning's Block 1 sprint.
"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return out_path


def build_notion_setup_and_formulas_guide_md() -> Path:
    out_path = STUDIO_ROOT / "06-NOTION-TEMPLATES/NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md"
    content = r"""# Notion Creator OS — Complete Setup, Relation Architecture & Formula 2.0 Reference Guide

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
"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return out_path


# ---------------------------------------------------------------------------
# PART B: COMMERCIAL COVER SUITE (6 SVGs, 6 PNGs, 1 KDP WRAP PDF, 1 SPEC MD)
# ---------------------------------------------------------------------------

def _svg_grid_pattern(prefix: str, w: int, h: int, step: int = 80) -> str:
    """Generates subtle vector architectural grid lines and glowing data nodes for rich visual density."""
    lines = []
    for x in range(0, w + 1, step):
        lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="#1E293B" stroke-width="1" opacity="0.45" />')
    for y in range(0, h + 1, step):
        lines.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="#1E293B" stroke-width="1" opacity="0.45" />')
    # Add decorative circuit nodes at intersections
    for ix, x in enumerate(range(step, w, step * 2)):
        for iy, y in enumerate(range(step, h, step * 2)):
            col = "#4F46E5" if (ix + iy) % 2 == 0 else "#0D9488"
            lines.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{col}" opacity="0.32" />')
    return "\n  ".join(lines)


def build_ebook_kindle_cover_svg() -> Path:
    out_path = STUDIO_ROOT / "08-COVER-DESIGN/svg/ebook-cover-kdp-kindle.svg"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    grid_bg = _svg_grid_pattern("kdp", 1600, 2560, step=80)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 2560" width="1600" height="2560" font-family="'Inter', 'Segoe UI', 'Noto Sans', sans-serif">
  <defs>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="52%" stop-color="#111827" />
      <stop offset="100%" stop-color="#090D16" />
    </linearGradient>
    <linearGradient id="indigo-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4F46E5" />
      <stop offset="100%" stop-color="#6366F1" />
    </linearGradient>
    <linearGradient id="teal-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0D9488" />
      <stop offset="100%" stop-color="#14B8A6" />
    </linearGradient>
    <linearGradient id="amber-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D97706" />
      <stop offset="100%" stop-color="#F59E0B" />
    </linearGradient>
    <radialGradient id="glow-indigo" cx="50%" cy="38%" r="45%">
      <stop offset="0%" stop-color="#4F46E5" stop-opacity="0.32" />
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="glow-teal" cx="50%" cy="72%" r="40%">
      <stop offset="0%" stop-color="#0D9488" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- Deep Studio Navy Canvas & Architectural Grid -->
  <rect x="0" y="0" width="1600" height="2560" fill="url(#bg-grad)" />
  {grid_bg}
  <rect x="0" y="0" width="1600" height="2560" fill="url(#glow-indigo)" />
  <rect x="0" y="0" width="1600" height="2560" fill="url(#glow-teal)" />

  <!-- Outer Precision Frame -->
  <rect x="48" y="48" width="1504" height="2464" rx="18" fill="none" stroke="#334155" stroke-width="3" />
  <rect x="64" y="64" width="1472" height="2432" rx="12" fill="none" stroke="#4F46E5" stroke-width="1.5" opacity="0.6" />

  <!-- Top Imprint Header Strip -->
  <rect x="120" y="110" width="1360" height="74" rx="10" fill="#1E293B" stroke="#4F46E5" stroke-width="2" />
  <text x="800" y="157" fill="#E2E8F0" font-size="26" font-weight="800" letter-spacing="5" text-anchor="middle">APEX DIGITAL SYSTEMS STUDIO · FLAGSHIP EDITION</text>

  <!-- Primary Book Title Hierarchy -->
  <text x="800" y="310" fill="#818CF8" font-size="38" font-weight="800" letter-spacing="6" text-anchor="middle">THE QUANTITATIVE SOLOPRENEUR MANUAL</text>
  <text x="800" y="445" fill="#FFFFFF" font-size="112" font-weight="900" letter-spacing="-1" text-anchor="middle">THE AI CONTENT</text>
  <text x="800" y="575" fill="#FFFFFF" font-size="112" font-weight="900" letter-spacing="-1" text-anchor="middle">CREATOR &amp;</text>
  <text x="800" y="705" fill="#2DD4BF" font-size="108" font-weight="900" letter-spacing="-1" text-anchor="middle">SOLOPRENEUR</text>
  <text x="800" y="835" fill="#FFFFFF" font-size="104" font-weight="900" letter-spacing="-1" text-anchor="middle">OPERATING SYSTEM</text>

  <!-- Accent Divider Bar -->
  <rect x="280" y="885" width="1040" height="8" rx="4" fill="url(#indigo-grad)" />

  <!-- Subtitle Block -->
  <text x="800" y="955" fill="#CBD5E1" font-size="33" font-weight="500" text-anchor="middle">A Practical System to Research Validated Ideas, Script High-Retention</text>
  <text x="800" y="1005" fill="#CBD5E1" font-size="33" font-weight="500" text-anchor="middle">Content, Repurpose Across Platforms, Automate Production, and</text>
  <text x="800" y="1055" fill="#FFFFFF" font-size="35" font-weight="700" text-anchor="middle">Monetize Your Audience Without Burnout</text>

  <!-- Centerpiece Architectural Diagram: The 5-Stage Content-to-Cash Engine -->
  <rect x="120" y="1125" width="1360" height="940" rx="20" fill="#0F172A" stroke="#4F46E5" stroke-width="3" />
  <rect x="120" y="1125" width="1360" height="68" rx="18" fill="#1E1B4B" />
  <text x="800" y="1169" fill="#FFFFFF" font-size="27" font-weight="800" letter-spacing="3" text-anchor="middle">5-STAGE CONTENT-TO-CASH OPERATING ARCHITECTURE</text>

  <!-- Stage Cards Row 1 -->
  <rect x="165" y="1230" width="400" height="230" rx="12" fill="#1E293B" stroke="#4F46E5" stroke-width="2.5" />
  <rect x="165" y="1230" width="400" height="44" rx="10" fill="url(#indigo-grad)" />
  <text x="365" y="1259" fill="#FFFFFF" font-size="20" font-weight="800" text-anchor="middle">STAGE 1: NICHE &amp; AVATAR MOAT</text>
  <text x="365" y="1305" fill="#E2E8F0" font-size="19" font-weight="600" text-anchor="middle">P.A.I.D. Positioning Matrix</text>
  <text x="365" y="1340" fill="#94A3B8" font-size="17" text-anchor="middle">NMPI Score &gt;= 75 / 100 Gate</text>
  <text x="365" y="1375" fill="#2DD4BF" font-size="18" font-family="'JetBrains Mono', monospace" font-weight="700" text-anchor="middle">RPPH Floor: $150 - $250/hr</text>
  <text x="365" y="1415" fill="#CBD5E1" font-size="16" text-anchor="middle">3-Pillar Authority Architecture</text>

  <rect x="600" y="1230" width="400" height="230" rx="12" fill="#1E293B" stroke="#4F46E5" stroke-width="2.5" />
  <rect x="600" y="1230" width="400" height="44" rx="10" fill="url(#indigo-grad)" />
  <text x="800" y="1259" fill="#FFFFFF" font-size="20" font-weight="800" text-anchor="middle">STAGE 2: OUTLIER &amp; HOOKS</text>
  <text x="800" y="1305" fill="#E2E8F0" font-size="19" font-weight="600" text-anchor="middle">S.I.G.N.A.L. Idea Validation</text>
  <text x="800" y="1340" fill="#94A3B8" font-size="17" text-anchor="middle">Outlier Multiplier M &gt;= 2.5x</text>
  <text x="800" y="1375" fill="#FBBF24" font-size="18" font-family="'JetBrains Mono', monospace" font-weight="700" text-anchor="middle">30s C.L.I.P. Hold &gt;= 70%</text>
  <text x="800" y="1415" fill="#CBD5E1" font-size="16" text-anchor="middle">Package-First Title &amp; Thumbnail</text>

  <rect x="1035" y="1230" width="400" height="230" rx="12" fill="#1E293B" stroke="#0D9488" stroke-width="2.5" />
  <rect x="1035" y="1230" width="400" height="44" rx="10" fill="url(#teal-grad)" />
  <text x="1235" y="1259" fill="#FFFFFF" font-size="20" font-weight="800" text-anchor="middle">STAGE 3: 1-TO-15 WATERFALL</text>
  <text x="1235" y="1305" fill="#E2E8F0" font-size="19" font-weight="600" text-anchor="middle">H.E.A.R.T. Pillar Scripting</text>
  <text x="1235" y="1340" fill="#94A3B8" font-size="17" text-anchor="middle">5-Parameter Voice DNA Engine</text>
  <text x="1235" y="1375" fill="#2DD4BF" font-size="18" font-family="'JetBrains Mono', monospace" font-weight="700" text-anchor="middle">1 Pillar -&gt; 15 Native Assets</text>
  <text x="1235" y="1415" fill="#CBD5E1" font-size="16" text-anchor="middle">YouTube · LinkedIn · X · Shorts</text>

  <!-- Stage Cards Row 2 -->
  <rect x="165" y="1500" width="615" height="240" rx="12" fill="#1E293B" stroke="#D97706" stroke-width="2.5" />
  <rect x="165" y="1500" width="615" height="44" rx="10" fill="url(#amber-grad)" />
  <text x="472" y="1529" fill="#FFFFFF" font-size="20" font-weight="800" text-anchor="middle">STAGE 4: 4-HOUR BATCH SPRINT &amp; OWNED FUNNEL</text>
  <text x="472" y="1575" fill="#E2E8F0" font-size="19" font-weight="600" text-anchor="middle">Mon-Thu 240-Minute Production Pipeline + 12-Point QA Gate</text>
  <text x="472" y="1615" fill="#FBBF24" font-size="18" font-family="'JetBrains Mono', monospace" font-weight="700" text-anchor="middle">Opt-In Page CVR &gt;= 45% · 5-Day Welcome CVR &gt;= 2.5%</text>
  <text x="472" y="1655" fill="#CBD5E1" font-size="17" text-anchor="middle">5-Minute Utility Lead Magnets · 3-Tag Intent Segmentation</text>
  <text x="472" y="1695" fill="#94A3B8" font-size="16" text-anchor="middle">90-Day Subscriber Value V_sub &gt;= $3.50 · 60-Day List Hygiene</text>

  <rect x="820" y="1500" width="615" height="240" rx="12" fill="#1E293B" stroke="#0D9488" stroke-width="2.5" />
  <rect x="820" y="1500" width="615" height="44" rx="10" fill="url(#teal-grad)" />
  <text x="1127" y="1529" fill="#FFFFFF" font-size="20" font-weight="800" text-anchor="middle">STAGE 5: 4-TIER VALUE LADDER &amp; SPONSORSHIPS</text>
  <text x="1127" y="1575" fill="#E2E8F0" font-size="19" font-weight="600" text-anchor="middle">14-Day Validate-Before-You-Build Launch + Checkout Stack</text>
  <text x="1127" y="1615" fill="#2DD4BF" font-size="18" font-family="'JetBrains Mono', monospace" font-weight="700" text-anchor="middle">Effective AOV Lift +45% · R_sponsor Usage Multipliers</text>
  <text x="1127" y="1655" fill="#CBD5E1" font-size="17" text-anchor="middle">Impulse ($29) -&gt; Flagship ($99) -&gt; Sprint ($697) -&gt; Advisory ($2.5k)</text>
  <text x="1127" y="1695" fill="#94A3B8" font-size="16" text-anchor="middle">20-Minute Friday Creator CEO Scorecard · 85%+ Net Margin</text>

  <!-- Telemetry Metric Strip Inside Centerpiece -->
  <rect x="165" y="1780" width="1270" height="240" rx="12" fill="#111827" stroke="#334155" stroke-width="2" />
  <text x="800" y="1828" fill="#818CF8" font-size="22" font-weight="800" letter-spacing="2" text-anchor="middle">INCLUDED IN THIS COMPLETE OPERATING SYSTEM EDITION</text>

  <rect x="200" y="1855" width="280" height="130" rx="8" fill="#1E293B" stroke="#4F46E5" stroke-width="1.5" />
  <text x="340" y="1910" fill="#FFFFFF" font-size="42" font-weight="900" font-family="'JetBrains Mono', monospace" text-anchor="middle">50</text>
  <text x="340" y="1948" fill="#CBD5E1" font-size="17" font-weight="700" text-anchor="middle">TESTED AI PROMPTS</text>
  <text x="340" y="1972" fill="#94A3B8" font-size="14" text-anchor="middle">Prompts P01 through P50</text>

  <rect x="510" y="1855" width="280" height="130" rx="8" fill="#1E293B" stroke="#0D9488" stroke-width="1.5" />
  <text x="650" y="1910" fill="#2DD4BF" font-size="42" font-weight="900" font-family="'JetBrains Mono', monospace" text-anchor="middle">20</text>
  <text x="650" y="1948" fill="#CBD5E1" font-size="17" font-weight="700" text-anchor="middle">SYSTEM DIAGRAMS</text>
  <text x="650" y="1972" fill="#94A3B8" font-size="14" text-anchor="middle">Mindmaps &amp; Decision Trees</text>

  <rect x="820" y="1855" width="280" height="130" rx="8" fill="#1E293B" stroke="#D97706" stroke-width="1.5" />
  <text x="960" y="1910" fill="#FBBF24" font-size="42" font-weight="900" font-family="'JetBrains Mono', monospace" text-anchor="middle">12</text>
  <text x="960" y="1948" fill="#CBD5E1" font-size="17" font-weight="700" text-anchor="middle">EMERGENCY SCRIPTS</text>
  <text x="960" y="1972" fill="#94A3B8" font-size="14" text-anchor="middle">Sponsor &amp; Crisis Vault</text>

  <rect x="1130" y="1855" width="270" height="130" rx="8" fill="#1E293B" stroke="#4F46E5" stroke-width="1.5" />
  <text x="1265" y="1910" fill="#FFFFFF" font-size="42" font-weight="900" font-family="'JetBrains Mono', monospace" text-anchor="middle">10</text>
  <text x="1265" y="1948" fill="#CBD5E1" font-size="17" font-weight="700" text-anchor="middle">ACTION WORKBOOKS</text>
  <text x="1265" y="1972" fill="#94A3B8" font-size="14" text-anchor="middle">Fillable Audits &amp; Rubrics</text>

  <!-- Bottom Author & Imprint Footer -->
  <rect x="120" y="2135" width="1360" height="295" rx="16" fill="#1E293B" stroke="#0D9488" stroke-width="2.5" />
  <text x="800" y="2205" fill="#2DD4BF" font-size="25" font-weight="800" letter-spacing="3" text-anchor="middle">INCLUDES COMPANION WEB APP ACCESS · KEY: CREATOR-OS-PRO-2026</text>
  <text x="800" y="2265" fill="#FFFFFF" font-size="38" font-weight="900" letter-spacing="2" text-anchor="middle">APEX DIGITAL SYSTEMS STUDIO</text>
  <text x="800" y="2320" fill="#94A3B8" font-size="22" font-weight="600" text-anchor="middle">Quantitative Operating Systems for Independent Media &amp; Solopreneur Enterprises</text>
  <text x="800" y="2375" fill="#64748B" font-size="18" font-family="'JetBrains Mono', monospace" text-anchor="middle">EDITION v1.0.0 · 91,775 MANUSCRIPT WORDS · 28 CORE MATHEMATICAL FORMULAS</text>
</svg>"""
    ET.fromstring(svg.encode("utf-8"))
    out_path.write_text(svg, encoding="utf-8")
    return out_path


def build_kdp_full_wrap_cover_svg(kdp_pages: int = 314) -> tuple[Path, dict]:
    """
    Dynamically computes exact Amazon KDP 6"x9" white-paper full-wrap dimensions
    for `kdp_pages` (314 pages) at 300 DPI:
      - Spine width = kdp_pages * 0.002252 in = 0.707128 in
      - Total width = 0.125 + 6.00 + spine + 6.00 + 0.125 = 12.957128 in (3887 px at 300 DPI, 932.91 pt)
      - Total height = 0.125 + 9.00 + 0.125 = 9.250 in (2775 px at 300 DPI, 666.00 pt)
    """
    out_path = STUDIO_ROOT / "08-COVER-DESIGN/svg/kdp-paperback-full-wrap-cover.svg"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    dpi = 300
    bleed_in = 0.125
    trim_w_in = 6.00
    trim_h_in = 9.00
    spine_in = round(kdp_pages * 0.002252, 6)
    total_w_in = round((bleed_in * 2) + (trim_w_in * 2) + spine_in, 6)
    total_h_in = round((bleed_in * 2) + trim_h_in, 6)

    w_px = round(total_w_in * dpi)  # 3887 px
    h_px = round(total_h_in * dpi)  # 2775 px
    w_pt = round(total_w_in * 72.0, 2)  # 932.91 pt
    h_pt = round(total_h_in * 72.0, 2)  # 666.00 pt

    bleed_px = round(bleed_in * dpi)  # 38 px
    trim_w_px = round(trim_w_in * dpi)  # 1800 px
    spine_px = w_px - (2 * bleed_px) - (2 * trim_w_px)  # 211 px

    back_x = bleed_px  # 38
    spine_x = bleed_px + trim_w_px  # 1838
    spine_cx = spine_x + (spine_px // 2)  # 1943
    front_x = spine_x + spine_px  # 2049
    front_cx = front_x + (trim_w_px // 2)  # 2949
    back_cx = back_x + (trim_w_px // 2)  # 938

    grid_bg = _svg_grid_pattern("wrap", w_px, h_px, step=90)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_px} {h_px}" width="{w_px}" height="{h_px}" font-family="'Inter', 'Segoe UI', 'Noto Sans', sans-serif">
  <defs>
    <linearGradient id="wrap-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090D16" />
      <stop offset="50%" stop-color="#0F172A" />
      <stop offset="100%" stop-color="#111827" />
    </linearGradient>
    <linearGradient id="wrap-indigo" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4F46E5" />
      <stop offset="100%" stop-color="#6366F1" />
    </linearGradient>
    <linearGradient id="wrap-teal" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0D9488" />
      <stop offset="100%" stop-color="#14B8A6" />
    </linearGradient>
  </defs>

  <!-- Full-Bleed Canvas (3887 x 2775 px / 12.957in x 9.250in) -->
  <rect x="0" y="0" width="{w_px}" height="{h_px}" fill="url(#wrap-bg)" />
  {grid_bg}

  <!-- Subtle Safe-Zone & Spine Fold Guides -->
  <rect x="{bleed_px}" y="{bleed_px}" width="{w_px - 2*bleed_px}" height="{h_px - 2*bleed_px}" fill="none" stroke="#1E293B" stroke-width="2" />
  <rect x="{spine_x}" y="0" width="{spine_px}" height="{h_px}" fill="#090D16" stroke="#334155" stroke-width="2" />

  <!-- ===================================================================== -->
  <!-- 1. BACK COVER PANEL (Left 6"x9" Trim Area)                            -->
  <!-- ===================================================================== -->
  <rect x="{back_x + 90}" y="130" width="{trim_w_px - 180}" height="70" rx="10" fill="#1E293B" stroke="#0D9488" stroke-width="2" />
  <text x="{back_cx}" y="175" fill="#2DD4BF" font-size="25" font-weight="800" letter-spacing="3" text-anchor="middle">STOP RENTING ALGORITHMIC ATTENTION. INSTALL AN OPERATING SYSTEM.</text>

  <text x="{back_x + 110}" y="275" fill="#FFFFFF" font-size="38" font-weight="800">Why 94% of Content Creators Burn Out Below $25/Hour</text>
  <text x="{back_x + 110}" y="335" fill="#CBD5E1" font-size="25" font-weight="500">Most creators are trapped on a manual production treadmill—spending 35+ hours</text>
  <text x="{back_x + 110}" y="375" fill="#CBD5E1" font-size="25" font-weight="500">a week guessing topics, rewriting scripts, cross-posting manually, and praying</text>
  <text x="{back_x + 110}" y="415" fill="#CBD5E1" font-size="25" font-weight="500">for AdSense pennies. This manual replaces guesswork with quantitative engineering.</text>

  <!-- 5-Stage Back Cover Feature Stack -->
  <rect x="{back_x + 100}" y="470" width="{trim_w_px - 200}" height="1060" rx="16" fill="#111827" stroke="#4F46E5" stroke-width="2.5" />
  <text x="{back_cx}" y="535" fill="#818CF8" font-size="27" font-weight="800" letter-spacing="2" text-anchor="middle">INSIDE THIS 10-CHAPTER SOLOPRENEUR OPERATING MANUAL:</text>

  <rect x="{back_x + 140}" y="575" width="{trim_w_px - 280}" height="165" rx="10" fill="#1E293B" stroke="#4F46E5" stroke-width="1.5" />
  <text x="{back_x + 170}" y="625" fill="#FFFFFF" font-size="26" font-weight="800">1. The Creator-to-Operator Paradigm &amp; P.A.I.D. Niche Moat (Ch 1–2)</text>
  <text x="{back_x + 170}" y="668" fill="#CBD5E1" font-size="21">Audit your Revenue Per Production Hour (RPPH) and lock a high-margin niche</text>
  <text x="{back_x + 170}" y="705" fill="#2DD4BF" font-size="20" font-family="'JetBrains Mono', monospace">scoring NMPI &gt;= 75/100 before producing a single asset.</text>

  <rect x="{back_x + 140}" y="765" width="{trim_w_px - 280}" height="165" rx="10" fill="#1E293B" stroke="#4F46E5" stroke-width="1.5" />
  <text x="{back_x + 170}" y="815" fill="#FFFFFF" font-size="26" font-weight="800">2. S.I.G.N.A.L. Outlier Mining &amp; 3-Second C.L.I.P. Hooks (Ch 3–4)</text>
  <text x="{back_x + 170}" y="858" fill="#CBD5E1" font-size="21">Validate demand via competitor Outlier Multipliers (M &gt;= 2.5x) and script</text>
  <text x="{back_x + 170}" y="895" fill="#FBBF24" font-size="20" font-family="'JetBrains Mono', monospace">Package-First openings that hold 70%+ of viewers past 0:30.</text>

  <rect x="{back_x + 140}" y="955" width="{trim_w_px - 280}" height="165" rx="10" fill="#1E293B" stroke="#0D9488" stroke-width="1.5" />
  <text x="{back_x + 170}" y="1005" fill="#FFFFFF" font-size="26" font-weight="800">3. Voice DNA Calibration &amp; The 1-to-15 Waterfall Engine (Ch 5–6)</text>
  <text x="{back_x + 170}" y="1048" fill="#CBD5E1" font-size="21">Eliminate robotic AI prose with a 5-parameter Voice DNA card and turn</text>
  <text x="{back_x + 170}" y="1085" fill="#2DD4BF" font-size="20" font-family="'JetBrains Mono', monospace">1 weekly Pillar Script into 15 platform-native omnichannel posts.</text>

  <rect x="{back_x + 140}" y="1145" width="{trim_w_px - 280}" height="165" rx="10" fill="#1E293B" stroke="#D97706" stroke-width="1.5" />
  <text x="{back_x + 170}" y="1195" fill="#FFFFFF" font-size="26" font-weight="800">4. The 4-Hour Batch Sprint &amp; 5-Day Welcome Funnel (Ch 7–8)</text>
  <text x="{back_x + 170}" y="1238" fill="#CBD5E1" font-size="21">Compress weekly production into 4 time-boxed blocks and bridge rented</text>
  <text x="{back_x + 170}" y="1275" fill="#FBBF24" font-size="20" font-family="'JetBrains Mono', monospace">views into a 45%+ opt-in landing page and $3.50+ subscriber value.</text>

  <rect x="{back_x + 140}" y="1335" width="{trim_w_px - 280}" height="165" rx="10" fill="#1E293B" stroke="#0D9488" stroke-width="1.5" />
  <text x="{back_x + 170}" y="1385" fill="#FFFFFF" font-size="26" font-weight="800">5. 4-Tier Product Value Ladder &amp; Outcome Sponsorships (Ch 9–10)</text>
  <text x="{back_x + 170}" y="1428" fill="#CBD5E1" font-size="21">Pre-sell digital products via the 14-Day Validation Protocol, lift checkout</text>
  <text x="{back_x + 170}" y="1465" fill="#2DD4BF" font-size="20" font-family="'JetBrains Mono', monospace">AOV by +45%, and price B2B brand deals with usage-rights multipliers.</text>

  <!-- Back Cover Vault Summary & KDP Mandatory White Barcode Safe Box (2.0" x 1.2" = 600 x 360 px) -->
  <rect x="{back_x + 100}" y="1580" width="{trim_w_px - 200}" height="520" rx="16" fill="#1E293B" stroke="#334155" stroke-width="2" />
  <text x="{back_cx}" y="1645" fill="#FFFFFF" font-size="30" font-weight="800" text-anchor="middle">COMPLETE VAULT &amp; COMPANION TOOLKIT INCLUDED:</text>
  <text x="{back_x + 150}" y="1710" fill="#E2E8F0" font-size="24">✓ 50 Copy-Paste AI Workflow Prompts (P01–P50) with Bracketed Variables</text>
  <text x="{back_x + 150}" y="1765" fill="#E2E8F0" font-size="24">✓ 12 Emergency Creator &amp; Sponsorship Negotiation Scripts (S01–S12)</text>
  <text x="{back_x + 150}" y="1820" fill="#E2E8F0" font-size="24">✓ 20 Vector System Mindmaps &amp; Quantitative Stage-Gate Decision Trees</text>
  <text x="{back_x + 150}" y="1875" fill="#E2E8F0" font-size="24">✓ 28 Core Creator Economy Mathematical Formulas &amp; Benchmark Tables</text>
  <text x="{back_x + 150}" y="1930" fill="#2DD4BF" font-size="24" font-weight="700">✓ Offline Web Companion App Key Included: CREATOR-OS-PRO-2026</text>
  <text x="{back_x + 150}" y="1985" fill="#94A3B8" font-size="21">✓ 10 Companion Fillable Action Worksheets &amp; Friday CEO Scorecards</text>

  <!-- Left Footer Spec + Right KDP Barcode Safe Zone -->
  <text x="{back_x + 110}" y="2240" fill="#FFFFFF" font-size="32" font-weight="800">APEX DIGITAL SYSTEMS STUDIO</text>
  <text x="{back_x + 110}" y="2290" fill="#94A3B8" font-size="22">Category: Business &amp; Money / Digital Media &amp; Entrepreneurship</text>
  <text x="{back_x + 110}" y="2335" fill="#64748B" font-size="20" font-family="'JetBrains Mono', monospace">TRIM: 6.0&quot; x 9.0&quot; · {kdp_pages} PAGES · SPINE: {spine_in:.4f}&quot;</text>

  <!-- Reserved KDP White Barcode Box (600x360 px = 2.0in x 1.2in) -->
  <rect x="{back_x + trim_w_px - 720}" y="2180" width="600" height="360" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="3" />
  <text x="{back_x + trim_w_px - 420}" y="2350" fill="#475569" font-size="22" font-weight="700" font-family="'JetBrains Mono', monospace" text-anchor="middle">AMAZON KDP ISBN BARCODE ZONE</text>
  <text x="{back_x + trim_w_px - 420}" y="2390" fill="#64748B" font-size="18" font-family="'JetBrains Mono', monospace" text-anchor="middle">(2.00&quot; x 1.20&quot; Reserved Safe Area)</text>

  <!-- ===================================================================== -->
  <!-- 2. SPINE PANEL (Center 0.7071" = 211 px at 300 DPI)                   -->
  <!-- ===================================================================== -->
  <g transform="translate({spine_cx}, 1387) rotate(90)">
    <text x="0" y="10" fill="#FFFFFF" font-size="30" font-weight="800" letter-spacing="2" text-anchor="middle">THE AI CONTENT CREATOR &amp; SOLOPRENEUR OPERATING SYSTEM   ·   APEX DIGITAL SYSTEMS</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 3. FRONT COVER PANEL (Right 6"x9" Trim Area)                          -->
  <!-- ===================================================================== -->
  <rect x="{front_x + 100}" y="130" width="{trim_w_px - 200}" height="74" rx="10" fill="#1E293B" stroke="#4F46E5" stroke-width="2" />
  <text x="{front_cx}" y="177" fill="#E2E8F0" font-size="26" font-weight="800" letter-spacing="4" text-anchor="middle">APEX DIGITAL SYSTEMS STUDIO · FLAGSHIP EDITION</text>

  <text x="{front_cx}" y="330" fill="#818CF8" font-size="38" font-weight="800" letter-spacing="5" text-anchor="middle">THE QUANTITATIVE SOLOPRENEUR MANUAL</text>
  <text x="{front_cx}" y="470" fill="#FFFFFF" font-size="112" font-weight="900" text-anchor="middle">THE AI CONTENT</text>
  <text x="{front_cx}" y="600" fill="#FFFFFF" font-size="112" font-weight="900" text-anchor="middle">CREATOR &amp;</text>
  <text x="{front_cx}" y="730" fill="#2DD4BF" font-size="108" font-weight="900" text-anchor="middle">SOLOPRENEUR</text>
  <text x="{front_cx}" y="860" fill="#FFFFFF" font-size="104" font-weight="900" text-anchor="middle">OPERATING SYSTEM</text>

  <rect x="{front_x + 260}" y="910" width="{trim_w_px - 520}" height="8" rx="4" fill="url(#wrap-indigo)" />

  <text x="{front_cx}" y="980" fill="#CBD5E1" font-size="33" font-weight="500" text-anchor="middle">A Practical System to Research Validated Ideas, Script High-Retention</text>
  <text x="{front_cx}" y="1030" fill="#CBD5E1" font-size="33" font-weight="500" text-anchor="middle">Content, Repurpose Across Platforms, Automate Production, and</text>
  <text x="{front_cx}" y="1080" fill="#FFFFFF" font-size="35" font-weight="700" text-anchor="middle">Monetize Your Audience Without Burnout</text>

  <!-- Front Cover Architectural Centerpiece -->
  <rect x="{front_x + 100}" y="1150" width="{trim_w_px - 200}" height="960" rx="18" fill="#0F172A" stroke="#4F46E5" stroke-width="3" />
  <rect x="{front_x + 100}" y="1150" width="{trim_w_px - 200}" height="68" rx="16" fill="#1E1B4B" />
  <text x="{front_cx}" y="1194" fill="#FFFFFF" font-size="26" font-weight="800" letter-spacing="3" text-anchor="middle">5-STAGE CONTENT-TO-CASH OPERATING SYSTEM</text>

  <rect x="{front_x + 145}" y="1255" width="470" height="230" rx="12" fill="#1E293B" stroke="#4F46E5" stroke-width="2" />
  <text x="{front_x + 380}" y="1305" fill="#818CF8" font-size="22" font-weight="800" text-anchor="middle">1. NICHE &amp; AVATAR MOAT</text>
  <text x="{front_x + 380}" y="1350" fill="#FFFFFF" font-size="20" text-anchor="middle">P.A.I.D. Positioning Framework</text>
  <text x="{front_x + 380}" y="1390" fill="#2DD4BF" font-size="19" font-family="'JetBrains Mono', monospace" text-anchor="middle">NMPI Score &gt;= 75 / 100</text>
  <text x="{front_x + 380}" y="1430" fill="#94A3B8" font-size="18" text-anchor="middle">RPPH Target: $150-$250/hr</text>

  <rect x="{front_x + 665}" y="1255" width="470" height="230" rx="12" fill="#1E293B" stroke="#4F46E5" stroke-width="2" />
  <text x="{front_x + 900}" y="1305" fill="#818CF8" font-size="22" font-weight="800" text-anchor="middle">2. OUTLIER &amp; 3S HOOKS</text>
  <text x="{front_x + 900}" y="1350" fill="#FFFFFF" font-size="20" text-anchor="middle">S.I.G.N.A.L. Idea Validation</text>
  <text x="{front_x + 900}" y="1390" fill="#FBBF24" font-size="19" font-family="'JetBrains Mono', monospace" text-anchor="middle">Outlier M &gt;= 2.5x Median</text>
  <text x="{front_x + 900}" y="1430" fill="#94A3B8" font-size="18" text-anchor="middle">30s Hold Rate &gt;= 70%</text>

  <rect x="{front_x + 1185}" y="1255" width="470" height="230" rx="12" fill="#1E293B" stroke="#0D9488" stroke-width="2" />
  <text x="{front_x + 1420}" y="1305" fill="#2DD4BF" font-size="22" font-weight="800" text-anchor="middle">3. 1-TO-15 WATERFALL</text>
  <text x="{front_x + 1420}" y="1350" fill="#FFFFFF" font-size="20" text-anchor="middle">H.E.A.R.T. Pillar Scripting</text>
  <text x="{front_x + 1420}" y="1390" fill="#2DD4BF" font-size="19" font-family="'JetBrains Mono', monospace" text-anchor="middle">1 Script -&gt; 15 Native Posts</text>
  <text x="{front_x + 1420}" y="1430" fill="#94A3B8" font-size="18" text-anchor="middle">5-Parameter Voice DNA</text>

  <rect x="{front_x + 145}" y="1525" width="730" height="240" rx="12" fill="#1E293B" stroke="#D97706" stroke-width="2" />
  <text x="{front_x + 510}" y="1580" fill="#FBBF24" font-size="23" font-weight="800" text-anchor="middle">4. 4-HOUR BATCH SPRINT &amp; OWNED FUNNEL</text>
  <text x="{front_x + 510}" y="1625" fill="#FFFFFF" font-size="20" text-anchor="middle">Mon-Thu 240-Min Sprint + 12-Point QA Gate</text>
  <text x="{front_x + 510}" y="1668" fill="#2DD4BF" font-size="19" font-family="'JetBrains Mono', monospace" text-anchor="middle">Opt-In Page &gt;= 45% · Welcome CVR &gt;= 2.5%</text>
  <text x="{front_x + 510}" y="1710" fill="#94A3B8" font-size="18" text-anchor="middle">5-Minute Utility Lead Magnets · V_sub &gt;= $3.50</text>

  <rect x="{front_x + 925}" y="1525" width="730" height="240" rx="12" fill="#1E293B" stroke="#0D9488" stroke-width="2" />
  <text x="{front_x + 1290}" y="1580" fill="#2DD4BF" font-size="23" font-weight="800" text-anchor="middle">5. 4-TIER VALUE LADDER &amp; SPONSORSHIPS</text>
  <text x="{front_x + 1290}" y="1625" fill="#FFFFFF" font-size="20" text-anchor="middle">14-Day Validate-Before-You-Build Launch</text>
  <text x="{front_x + 1290}" y="1668" fill="#2DD4BF" font-size="19" font-family="'JetBrains Mono', monospace" text-anchor="middle">Checkout AOV +45% · R_sponsor Multipliers</text>
  <text x="{front_x + 1290}" y="1710" fill="#94A3B8" font-size="18" text-anchor="middle">20-Min Friday Creator CEO Cadence · 85% Margin</text>

  <rect x="{front_x + 145}" y="1810" width="1510" height="250" rx="12" fill="#111827" stroke="#334155" stroke-width="2" />
  <text x="{front_cx}" y="1875" fill="#FFFFFF" font-size="30" font-weight="800" text-anchor="middle">50 AI WORKFLOW PROMPTS · 20 SYSTEM DIAGRAMS · 12 EMERGENCY SCRIPTS</text>
  <text x="{front_cx}" y="1935" fill="#2DD4BF" font-size="24" font-family="'JetBrains Mono', monospace" font-weight="700" text-anchor="middle">10 FILLABLE WORKSHEETS · 28 CORE FORMULAS · OFFLINE WEB APP INCLUDED</text>
  <text x="{front_cx}" y="1995" fill="#94A3B8" font-size="21" text-anchor="middle">Complete End-to-End Implementation System for Modern Creator-Operators</text>

  <!-- Front Cover Bottom Author Banner -->
  <rect x="{front_x + 100}" y="2180" width="{trim_w_px - 200}" height="360" rx="16" fill="#1E293B" stroke="#0D9488" stroke-width="2.5" />
  <text x="{front_cx}" y="2265" fill="#2DD4BF" font-size="25" font-weight="800" letter-spacing="3" text-anchor="middle">INCLUDES PRO WEB SUITE LICENSE KEY: CREATOR-OS-PRO-2026</text>
  <text x="{front_cx}" y="2345" fill="#FFFFFF" font-size="44" font-weight="900" letter-spacing="2" text-anchor="middle">APEX DIGITAL SYSTEMS STUDIO</text>
  <text x="{front_cx}" y="2415" fill="#CBD5E1" font-size="24" font-weight="500" text-anchor="middle">Autonomous Digital Publishing &amp; Creator Economy Engineering</text>
  <text x="{front_cx}" y="2475" fill="#64748B" font-size="19" font-family="'JetBrains Mono', monospace" text-anchor="middle">PRODUCT-03-AI-CREATOR-SOLOPRENEUR-OS · PRINT EDITION v1.0.0</text>
</svg>"""
    ET.fromstring(svg.encode("utf-8"))
    out_path.write_text(svg, encoding="utf-8")

    geom = {
        "kdp_pages": kdp_pages,
        "spine_width_in": spine_in,
        "total_width_in": total_w_in,
        "total_height_in": total_h_in,
        "width_px_300dpi": w_px,
        "height_px_300dpi": h_px,
        "width_pt": w_pt,
        "height_pt": h_pt,
    }
    return out_path, geom


def build_gumroad_widescreen_cover_svg(
    filename: str,
    tier_badge: str,
    price_badge: str,
    headline_1: str,
    headline_2: str,
    subtitle: str,
    accent_hex: str,
    secondary_hex: str,
    cards: list[tuple[str, str, str]],
) -> Path:
    out_path = STUDIO_ROOT / "08-COVER-DESIGN/svg" / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    grid_bg = _svg_grid_pattern(filename[:8], 1600, 1000, step=64)

    card_elems = []
    for idx, (c_title, c_metric, c_desc) in enumerate(cards):
        cx = 70 + idx * 370
        card_elems.append(f"""
  <rect x="{cx}" y="555" width="345" height="275" rx="14" fill="#1E293B" stroke="{accent_hex}" stroke-width="2.5" />
  <rect x="{cx}" y="555" width="345" height="44" rx="12" fill="{accent_hex}" />
  <text x="{cx + 172}" y="584" fill="#FFFFFF" font-size="17" font-weight="800" text-anchor="middle">{html.escape(c_title)}</text>
  <text x="{cx + 172}" y="655" fill="{secondary_hex}" font-size="32" font-weight="900" font-family="'JetBrains Mono', monospace" text-anchor="middle">{html.escape(c_metric)}</text>
  <line x1="{cx + 30}" y1="685" x2="{cx + 315}" y2="685" stroke="#334155" stroke-width="1.5" />
  <text x="{cx + 172}" y="730" fill="#E2E8F0" font-size="16" font-weight="600" text-anchor="middle">{html.escape(c_desc.split('|')[0])}</text>
  <text x="{cx + 172}" y="762" fill="#94A3B8" font-size="14.5" text-anchor="middle">{html.escape(c_desc.split('|')[1] if '|' in c_desc else '')}</text>
  <rect x="{cx + 45}" y="782" width="255" height="30" rx="6" fill="#0F172A" stroke="#334155" stroke-width="1" />
  <text x="{cx + 172}" y="802" fill="#CBD5E1" font-size="12.5" font-family="'JetBrains Mono', monospace" text-anchor="middle">VERIFIED STUDIO ASSET</text>""")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000" width="1600" height="1000" font-family="'Inter', 'Segoe UI', 'Noto Sans', sans-serif">
  <defs>
    <linearGradient id="gr-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="55%" stop-color="#111827" />
      <stop offset="100%" stop-color="#090D16" />
    </linearGradient>
    <radialGradient id="gr-glow" cx="50%" cy="35%" r="55%">
      <stop offset="0%" stop-color="{accent_hex}" stop-opacity="0.28" />
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0" />
    </radialGradient>
  </defs>

  <rect x="0" y="0" width="1600" height="1000" fill="url(#gr-bg)" />
  {grid_bg}
  <rect x="0" y="0" width="1600" height="1000" fill="url(#gr-glow)" />

  <!-- Outer Frame -->
  <rect x="28" y="28" width="1544" height="944" rx="16" fill="none" stroke="#334155" stroke-width="2.5" />
  <rect x="40" y="40" width="1520" height="920" rx="12" fill="none" stroke="{accent_hex}" stroke-width="1.5" opacity="0.7" />

  <!-- Top Header Bar & Price Badge -->
  <rect x="70" y="70" width="1080" height="58" rx="10" fill="#1E293B" stroke="{accent_hex}" stroke-width="2" />
  <text x="95" y="107" fill="#FFFFFF" font-size="21" font-weight="800" letter-spacing="2">{html.escape(tier_badge)}</text>

  <rect x="1180" y="70" width="350" height="58" rx="10" fill="{secondary_hex}" />
  <text x="1355" y="108" fill="#FFFFFF" font-size="24" font-weight="900" font-family="'JetBrains Mono', monospace" text-anchor="middle">{html.escape(price_badge)}</text>

  <!-- Main Widescreen Title Block -->
  <text x="70" y="210" fill="#818CF8" font-size="26" font-weight="800" letter-spacing="4">THE AI CONTENT CREATOR &amp; SOLOPRENEUR OPERATING SYSTEM</text>
  <text x="70" y="305" fill="#FFFFFF" font-size="68" font-weight="900" letter-spacing="-1">{html.escape(headline_1)}</text>
  <text x="70" y="390" fill="{secondary_hex}" font-size="64" font-weight="900" letter-spacing="-1">{html.escape(headline_2)}</text>
  <text x="70" y="455" fill="#CBD5E1" font-size="25" font-weight="500">{html.escape(subtitle)}</text>

  <line x1="70" y1="495" x2="1530" y2="495" stroke="{accent_hex}" stroke-width="3" />

  <!-- 4 Deliverable Architecture Cards -->
  {''.join(card_elems)}

  <!-- Bottom Telemetry & Pro Key Strip -->
  <rect x="70" y="860" width="1460" height="72" rx="10" fill="#111827" stroke="#334155" stroke-width="2" />
  <text x="800" y="904" fill="#E2E8F0" font-size="20" font-weight="700" font-family="'JetBrains Mono', monospace" text-anchor="middle">APEX DIGITAL SYSTEMS STUDIO · INSTANT DOWNLOAD · OFFLINE &amp; CLOUD READY · ZERO FLUFF</text>
</svg>"""
    ET.fromstring(svg.encode("utf-8"))
    out_path.write_text(svg, encoding="utf-8")
    return out_path


def render_svg_cover_to_png(svg_path: Path, png_path: Path, width: int, height: int) -> None:
    png_path.parent.mkdir(parents=True, exist_ok=True)
    svg_raw = svg_path.read_text(encoding="utf-8")

    wrapper_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{
    width: {width}px;
    height: {height}px;
    overflow: hidden;
    background: #0F172A;
  }}
  svg {{
    display: block;
    width: {width}px;
    height: {height}px;
  }}
</style>
</head>
<body>
{svg_raw}
</body>
</html>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_html = Path(tmpdir) / "cover.html"
        tmp_png = Path(tmpdir) / "screen.png"
        tmp_html.write_text(wrapper_html, encoding="utf-8")
        user_data_dir = Path(tmpdir) / "profile"
        cmd = [
            BROWSER_BIN,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--user-data-dir={user_data_dir}",
            f"--window-size={width},{height + 160}",
            f"--screenshot={tmp_png}",
            tmp_html.as_uri(),
        ]
        subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if not tmp_png.is_file():
            raise RuntimeError(f"Failed to capture PNG screenshot for cover {svg_path.name}")
        with Image.open(tmp_png) as img:
            cropped = img.crop((0, 0, width, height))
            cropped.save(png_path, format="PNG", compress_level=1)


def render_kdp_full_wrap_pdf(svg_path: Path, pdf_path: Path, geom: dict) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    svg_raw = svg_path.read_text(encoding="utf-8")
    w_in = geom["total_width_in"]
    h_in = geom["total_height_in"]
    w_pt = geom["width_pt"]
    h_pt = geom["height_pt"]

    html_wrap = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: {w_in:.6f}in {h_in:.6f}in;
    margin: 0;
  }}
  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}
  html, body {{
    width: {w_in:.6f}in;
    height: {h_in:.6f}in;
    overflow: hidden;
    background: #0F172A;
  }}
  svg {{
    display: block;
    width: {w_in:.6f}in;
    height: {h_in:.6f}in;
  }}
</style>
</head>
<body>
{svg_raw}
</body>
</html>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_html = Path(tmpdir) / "kdp_wrap.html"
        tmp_pdf = Path(tmpdir) / "raw_wrap.pdf"
        tmp_html.write_text(html_wrap, encoding="utf-8")
        user_data_dir = Path(tmpdir) / "profile"
        cmd = [
            BROWSER_BIN,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            f"--user-data-dir={user_data_dir}",
            f"--print-to-pdf={tmp_pdf}",
            "--no-pdf-header-footer",
            tmp_html.as_uri(),
        ]
        subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if not tmp_pdf.is_file():
            raise RuntimeError("Failed to compile KDP full-wrap PDF via headless browser")

        reader = PdfReader(str(tmp_pdf))
        writer = PdfWriter()
        page = reader.pages[0]
        page.mediabox.lower_left = (0, 0)
        page.mediabox.upper_right = (w_pt, h_pt)
        writer.add_page(page)
        with open(pdf_path, "wb") as f_out:
            writer.write(f_out)


def build_cover_packaging_spec_md(geom: dict) -> Path:
    out_path = STUDIO_ROOT / "08-COVER-DESIGN/COVER-DESIGN-AND-PACKAGING-SPEC.md"
    kdp_pages = geom["kdp_pages"]
    spine_in = geom["spine_width_in"]
    w_in = geom["total_width_in"]
    h_in = geom["total_height_in"]
    w_pt = geom["width_pt"]
    h_pt = geom["height_pt"]
    w_px = geom["width_px_300dpi"]
    h_px = geom["height_px_300dpi"]

    content = f"""# Commercial Cover Suite & Amazon KDP Print Packaging Specification

> **Visual Packaging & Print Engineering Manual (`08-COVER-DESIGN/COVER-DESIGN-AND-PACKAGING-SPEC.md`)**
> * **Product ID:** `PRODUCT-03-AI-CREATOR-SOLOPRENEUR-OS`
> * **Title:** *The AI Content Creator & Solopreneur Operating System*
> * **Locked Interior Page Count (`6" × 9"` KDP Paperback):** `{kdp_pages} pages` (Verified from `PROJECT_STATE.json`)
> * **Calculated White-Paper Spine Width:** `{spine_in:.6f} in` (`{spine_in * 25.4:.2f} mm`)
> * **Full-Wrap Print Dimensions (With `0.125"` Bleed):** `{w_in:.6f} in × {h_in:.3f} in` (`{w_pt:.2f} pt × {h_pt:.2f} pt` / `{w_px} px × {h_px} px` at `300 DPI`)

---

## 1. Executive Packaging Philosophy & Locked Brand Palette

The visual packaging suite for **Flagship Product #3 (*The AI Content Creator & Solopreneur Operating System*)** is engineered to position the product as a quantitative, institutional-grade operating manual and software-accompanied toolkit rather than a generic lifestyle creator eBook. Every cover in `08-COVER-DESIGN/` adheres strictly to the locked **Creator Indigo, Deep Studio Navy, Conversion Teal & Retention Amber** design tokens established in Phase 1:

| Design Token Role | Hex Code | RGB Value | Packaging & Cover Application |
| :--- | :---: | :---: | :--- |
| **Deep Studio Navy (Canvas)** | `#0F172A` / `#090D16` | `rgb(15, 23, 42)` | Primary high-contrast cover background, spine fill, and architectural diagram container |
| **Creator Indigo (Primary Accent)** | `#4F46E5` / `#818CF8` | `rgb(79, 70, 229)` | Precision border frames, Stage 1–2 workflow badges, and divider rules |
| **Conversion Teal (Monetization)** | `#0D9488` / `#2DD4BF` | `rgb(13, 148, 136)` | Keyword highlight (`SOLOPRENEUR`), ROI telemetry callouts, and commercial price badges |
| **Retention Amber (Stage Gates)** | `#D97706` / `#FBBF24` | `rgb(217, 119, 6)` | Retention & batch sprint badges, Tier 4 Vault highlights, and warning threshold indicators |
| **Pure White (Typography & Barcode)** | `#FFFFFF` | `rgb(255, 255, 255)` | Primary display headlines (`Inter Black 900`) and mandatory KDP ISBN Barcode Safe Zone |
| **Slate Metadata Text** | `#CBD5E1` / `#94A3B8` | `rgb(203, 213, 225)` | Subtitles, back-cover copy blocks, and `JetBrains Mono` technical specifications |

---

## 2. Dynamic Amazon KDP `6" × 9"` Full-Wrap Paperback Geometry Math

Amazon Kindle Direct Publishing (KDP) enforces strict mathematical tolerances on print-ready paperback wraparound covers (`kdp-paperback-full-wrap-cover.pdf`). If a cover's width or spine deviates from the compiled interior page count by more than `0.03 inches`, KDP's automated pre-flight ingestion engine rejects the file.

### 2.1 Step-by-Step Spine & Full-Wrap Derivation (`{kdp_pages}` Pages)

Using the locked Phase 5 monochrome interior PDF (`09-EXPORTS/PRINT/the-ai-creator-solopreneur-os-kdp-paperback-6x9.pdf` at **`{kdp_pages} pages`**), `build_phase7.py` computes the exact KDP white-paper full-wrap geometry:

1. **Selected Trim Size ($W_{{\\text{{trim}}}} \\times H_{{\\text{{trim}}}}$):**
   * Front & Back Cover Width: `6.000 in` (`152.40 mm` / `432.00 pt` / `1800 px` at `300 DPI`)
   * Front & Back Cover Height: `9.000 in` (`228.60 mm` / `648.00 pt` / `2700 px` at `300 DPI`)
2. **Amazon KDP White-Paper Spine Thickness Multiplier ($k_{{\\text{{white}}}}$):**
   * Standard KDP B&W White Paper (`55 lb / 90 gsm`) thickness factor: `0.002252 in/page` (`0.0572 mm/page`)
3. **Calculated Spine Width ($W_{{\\text{{spine}}}}$):**
   $$W_{{\\text{{spine}}}} = {kdp_pages} \\times 0.002252\\text{{ in}} = {spine_in:.6f}\\text{{ in}} \\quad (17.96\\text{{ mm}} \\text{{ / }} 50.91\\text{{ pt}} \\text{{ / }} 211\\text{{ px at 300 DPI}})$$
4. **Outside Edge Bleed ($B$):**
   * Top, Bottom, Left (Back Cover outer edge), and Right (Front Cover outer edge): `0.125 in` (`3.175 mm` / `9.00 pt` / `38 px` at `300 DPI`)
5. **Total Full-Wrap Cover Width ($W_{{\\text{{total}}}}$):**
   $$W_{{\\text{{total}}}} = 0.125 + 6.000 + {spine_in:.6f} + 6.000 + 0.125 = {w_in:.6f}\\text{{ in}} \\quad ({w_pt:.2f}\\text{{ pt}} \\text{{ / }} {w_px}\\text{{ px at 300 DPI}})$$
6. **Total Full-Wrap Cover Height ($H_{{\\text{{total}}}}$):**
   $$H_{{\\text{{total}}}} = 0.125 + 9.000 + 0.125 = {h_in:.3f}\\text{{ in}} \\quad ({h_pt:.2f}\\text{{ pt}} \\text{{ / }} {h_px}\\text{{ px at 300 DPI}})$$

### 2.2 KDP Margin Safe Zones, Spine Hinge & Barcode Placement Rules

| Cover Zone | X-Coordinate Range (`300 DPI px`) | Physical Dimension | KDP Pre-Flight Safety Rule Enforced |
| :--- | :---: | :---: | :--- |
| **Left Outer Bleed** | `0 px – 38 px` | `0.125 in` | Background artwork extends to `0 px`; zero text within `0.25 in` (`75 px`) of trim |
| **Back Cover Panel** | `38 px – 1838 px` | `6.000 in × 9.000 in` | Contains 5-stage executive summary, vault checklist, and lower-right Barcode Safe Zone |
| **KDP ISBN Barcode Box** | `1118 px – 1718 px` (`Y: 2180–2540`) | `2.000 in × 1.200 in` | Pure `#FFFFFF` solid rectangle reserved `0.40 in` inside bottom/spine trim edges |
| **Center Spine Panel** | `1838 px – 2049 px` (`CX: 1943 px`) | `{spine_in:.4f} in × 9.000 in` | Rotated `90°` clockwise title text (`30px`, `0.10 in` height) with `> 0.0625 in` hinge clearance |
| **Front Cover Panel** | `2049 px – 3849 px` (`CX: 2949 px`) | `6.000 in × 9.000 in` | High-contrast title hierarchy + 5-Stage Content-to-Cash architectural centerpiece |
| **Right Outer Bleed** | `3849 px – 3887 px` | `0.125 in` | Background grid and navy gradient extend through full `3887 px` right edge |

---

## 3. Complete Inventory of Phase 7 Cover Deliverables

All vector source files (`08-COVER-DESIGN/svg/*.svg`), raster renders (`08-COVER-DESIGN/png/*.png`), and print-ready PDFs are compiled deterministically by `build_phase7.py`:

1. **Kindle / Apple Books / Draft2Digital eBook Portrait Cover (`1600 × 2560 px`, `1:1.6` Aspect Ratio):**
   * **Vector Source:** `08-COVER-DESIGN/svg/ebook-cover-kdp-kindle.svg`
   * **Primary PNG:** `08-COVER-DESIGN/ebook-cover-kdp-kindle.png` (and mirrored at `08-COVER-DESIGN/png/ebook-cover-kdp-kindle.png`)
   * **Platform Compliance:** Meets Amazon KDP Kindle (`1600 × 2560` ideal `1.6:1` portrait ratio, RGB color profile) and Apple Books / Kobo / Draft2Digital distribution specifications, maintaining full title legibility at `120 × 192 px` marketplace thumbnail scale.

2. **Amazon KDP `6" × 9"` Full-Wrap Paperback Print Cover (`3887 × 2775 px` / `12.957" × 9.250"`):**
   * **Vector Source:** `08-COVER-DESIGN/svg/kdp-paperback-full-wrap-cover.svg`
   * **300 DPI Raster PNG:** `08-COVER-DESIGN/png/kdp-paperback-full-wrap-cover.png`
   * **Print-Ready PDF/X-Ready Interior Match:** `08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf` (`932.91 pt × 666.00 pt`, single page, zero crop marks inside bleed).

3. **Gumroad / Lemon Squeezy Tier 0 Free Starter Kit Cover (`1600 × 1000 px` Widescreen `16:10`):**
   * **Vector Source:** `08-COVER-DESIGN/svg/gumroad-tier0-free-audit-cover.svg`
   * **Raster PNG:** `08-COVER-DESIGN/png/gumroad-tier0-free-audit-cover.png`
   * **Merchandising Focus:** Highlights the **7-Day Content Time-Leak & RPPH Diagnostic Audit**, Chapter 1 Vertical Slice (`9,704 words`), Prompts `P01`–`P05`, and Tier 0 Free Web App Diagnostic Mode.

4. **Gumroad / Lemon Squeezy Tier 2 Creator Operator Pro Workbook & Visual Atlas Cover (`1600 × 1000 px`):**
   * **Vector Source:** `08-COVER-DESIGN/svg/gumroad-tier2-workbook-edition-cover.svg`
   * **Raster PNG:** `08-COVER-DESIGN/png/gumroad-tier2-workbook-edition-cover.png`
   * **Merchandising Focus:** Highlights the **Complete 10-Chapter Book (`PDF` + `EPUB`)**, **Fillable Action Workbooks (`US Letter` + `ISO A4` + `Tablet Landscape`)**, **Offline SaaS-Lite Web App (`CREATOR-OS-PRO-2026`)**, and **5-Database Notion Creator OS Kit** (`$79` Retail Anchor).

5. **Gumroad / Lemon Squeezy Tier 3 Executive Solopreneur Automation Suite Cover (`1600 × 1000 px`):**
   * **Vector Source:** `08-COVER-DESIGN/svg/gumroad-tier3-flagship-bundle-cover.svg`
   * **Raster PNG:** `08-COVER-DESIGN/png/gumroad-tier3-flagship-bundle-cover.png`
   * **Merchandising Focus:** Highlights the **Full Flagship Operating System Bundle** including the **n8n & Make.com JSON Automation Blueprints**, **Excel Financial & Waterfall Trackers**, **Editable DOCX SOPs**, and **Sponsorship Rate Card & Pitch Kit** (`$199` Executive Bundle).

6. **Gumroad / Lemon Squeezy Tier 4 Agency & Living Creator Vault Membership Cover (`1600 × 1000 px`):**
   * **Vector Source:** `08-COVER-DESIGN/svg/gumroad-tier4-vault-membership-cover.svg`
   * **Raster PNG:** `08-COVER-DESIGN/png/gumroad-tier4-vault-membership-cover.png`
   * **Merchandising Focus:** Highlights the **Commercial White-Label Cohort & Agency Training License**, **Editable Source SVG Master Kit**, and **Living Creator Vault Updates** (`$499` Commercial License).

---

## 4. Marketplace Upload & Quality Verification Checklist

- [ ] **Kindle eBook Upload:** Upload `09-EXPORTS/EPUB/the-ai-creator-solopreneur-os.epub` as the manuscript and `08-COVER-DESIGN/ebook-cover-kdp-kindle.png` (`1600 × 2560 px`) as the front cover in KDP Kindle eBook setup.
- [ ] **KDP Paperback Upload:** Select `6 in × 9 in` trim, **Black & White interior with white paper**, **No bleed** (for interior PDF `09-EXPORTS/PRINT/the-ai-creator-solopreneur-os-kdp-paperback-6x9.pdf`), and **Upload a cover you already have (Print-Ready PDF)** using `08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf`.
- [ ] **Gumroad / Lemon Squeezy Product Cards:** Assign the four `1600 × 1000 px` PNG covers in `08-COVER-DESIGN/png/` to their corresponding Tier 0, Tier 2, Tier 3, and Tier 4 product listings.
"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return out_path


# ---------------------------------------------------------------------------
# MAIN COMPILER EXECUTION
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 90)
    print("ANTIGRAVITY PHASE 7 COMPILER: 5-DATABASE NOTION OS KIT & COMMERCIAL COVER SUITE")
    print(f"Studio Root: {STUDIO_ROOT}")
    print("=" * 90)

    state_path = STUDIO_ROOT / "PROJECT_STATE.json"
    state_data = json.loads(state_path.read_text(encoding="utf-8"))
    kdp_pages = state_data.get("phase5_exports", {}).get("kdp_paperback_6x9_pages", 314)
    print(f"[INFO] Loaded KDP 6\"x9\" Paperback Page Count from PROJECT_STATE.json: {kdp_pages} pages")

    # Part A: 5-Database Notion Creator OS Kit
    print("\n[PART A] Building 5-Database Minimalist Notion Creator OS Kit (06-NOTION-TEMPLATES/)...")
    p_csv1 = build_db01_outlier_idea_bank()
    print(f"  -> [1/7] {p_csv1.relative_to(STUDIO_ROOT).as_posix()} ({p_csv1.stat().st_size:,} bytes)")

    p_csv2 = build_db02_master_content_calendar()
    print(f"  -> [2/7] {p_csv2.relative_to(STUDIO_ROOT).as_posix()} ({p_csv2.stat().st_size:,} bytes)")

    p_csv3 = build_db03_prompt_and_script_vault_62()
    print(f"  -> [3/7] {p_csv3.relative_to(STUDIO_ROOT).as_posix()} ({p_csv3.stat().st_size:,} bytes)")

    p_csv4 = build_db04_sponsorship_crm()
    print(f"  -> [4/7] {p_csv4.relative_to(STUDIO_ROOT).as_posix()} ({p_csv4.stat().st_size:,} bytes)")

    p_md5 = build_db05_monetization_and_launch_hub_md()
    print(f"  -> [5/7] {p_md5.relative_to(STUDIO_ROOT).as_posix()} ({len(p_md5.read_text('utf-8').split()):,} words, {p_md5.stat().st_size:,} bytes)")

    p_md6 = build_notion_setup_and_formulas_guide_md()
    print(f"  -> [6/7] {p_md6.relative_to(STUDIO_ROOT).as_posix()} ({len(p_md6.read_text('utf-8').split()):,} words, {p_md6.stat().st_size:,} bytes)")

    p_csv_s1 = build_sheet1_rpm_and_time_audit()
    print(f"  -> [7/7] {p_csv_s1.relative_to(STUDIO_ROOT).as_posix()} ({p_csv_s1.stat().st_size:,} bytes)")

    # Part B: Commercial Cover Suite
    print("\n[PART B] Building Commercial Cover Suite & KDP Full-Wrap Package (08-COVER-DESIGN/)...")

    # 1. Kindle eBook Cover (1600x2560)
    svg_kindle = build_ebook_kindle_cover_svg()
    png_kindle_root = STUDIO_ROOT / "08-COVER-DESIGN/ebook-cover-kdp-kindle.png"
    png_kindle_sub = STUDIO_ROOT / "08-COVER-DESIGN/png/ebook-cover-kdp-kindle.png"
    render_svg_cover_to_png(svg_kindle, png_kindle_root, 1600, 2560)
    png_kindle_sub.parent.mkdir(parents=True, exist_ok=True)
    png_kindle_sub.write_bytes(png_kindle_root.read_bytes())
    print(f"  -> [1/7] Kindle eBook Cover (1600x2560): SVG={svg_kindle.stat().st_size:,}B, PNG={png_kindle_root.stat().st_size:,}B")

    # 2. KDP 6"x9" Paperback Full-Wrap Cover (3887x2775 px / 12.957"x9.250")
    svg_wrap, geom = build_kdp_full_wrap_cover_svg(kdp_pages=kdp_pages)
    png_wrap = STUDIO_ROOT / "08-COVER-DESIGN/png/kdp-paperback-full-wrap-cover.png"
    pdf_wrap = STUDIO_ROOT / "08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf"
    render_svg_cover_to_png(svg_wrap, png_wrap, geom["width_px_300dpi"], geom["height_px_300dpi"])
    render_kdp_full_wrap_pdf(svg_wrap, pdf_wrap, geom)
    print(
        f"  -> [2/7] KDP Full-Wrap ({geom['width_px_300dpi']}x{geom['height_px_300dpi']}px / {geom['width_pt']}x{geom['height_pt']}pt): "
        f"SVG={svg_wrap.stat().st_size:,}B, PNG={png_wrap.stat().st_size:,}B, PDF={pdf_wrap.stat().st_size:,}B"
    )

    # 3. Gumroad Tier 0 Free Starter Kit Cover (1600x1000)
    svg_t0 = build_gumroad_widescreen_cover_svg(
        filename="gumroad-tier0-free-audit-cover.svg",
        tier_badge="TIER 0 FREE STARTER KIT · DIAGNOSTIC AUDIT & CHAPTER 1 SLICE",
        price_badge="FREE DOWNLOAD ($0)",
        headline_1="7-DAY CONTENT TIME-LEAK",
        headline_2="& RPPH DIAGNOSTIC AUDIT KIT",
        subtitle="Quantify Your Revenue Per Production Hour, Eliminate Burnout & Install the 5-Stage Creator OS",
        accent_hex="#0D9488",
        secondary_hex="#2DD4BF",
        cards=[
            ("CH 01 VERTICAL SLICE", "9,704 Words", "Complete Chapter 1 Manual|5-Stage Content-to-Cash OS"),
            ("FILLABLE AUDIT PDF", "48 Fields", "Worksheet 01 Diagnostic|RPPH & Time-Leak Calculator"),
            ("STARTER AI PROMPTS", "P01 – P05", "5 Copy-Paste Prompts|Plus S01–S02 Sponsor Scripts"),
            ("OFFLINE WEB APP", "Module 1", "Interactive RPPH Simulator|& CSV Baseline Audit Sheet"),
        ],
    )
    png_t0 = STUDIO_ROOT / "08-COVER-DESIGN/png/gumroad-tier0-free-audit-cover.png"
    render_svg_cover_to_png(svg_t0, png_t0, 1600, 1000)
    print(f"  -> [3/7] Gumroad Tier 0 Cover (1600x1000): SVG={svg_t0.stat().st_size:,}B, PNG={png_t0.stat().st_size:,}B")

    # 4. Gumroad Tier 2 Workbook, Visual Atlas & Tablet Edition Cover (1600x1000)
    svg_t2 = build_gumroad_widescreen_cover_svg(
        filename="gumroad-tier2-workbook-edition-cover.svg",
        tier_badge="TIER 2 CREATOR OPERATOR PRO BUNDLE · INTERACTIVE WORKBOOK & WEB OS",
        price_badge="PRO BUNDLE · $79",
        headline_1="INTERACTIVE WORKBOOK, WEB APP",
        headline_2="& 5-DATABASE NOTION OS KIT",
        subtitle="Complete 10-Chapter Manual + Fillable Workbooks (US Letter, A4 & Tablet) + Offline SaaS-Lite App",
        accent_hex="#4F46E5",
        secondary_hex="#818CF8",
        cards=[
            ("COMPLETE 10-CH BOOK", "340 Pages", "US Letter PDF + KDP 6x9|& Reflowable EPUB 3.0"),
            ("3 FILLABLE WORKBOOKS", "1,372 Fields", "US Letter + ISO A4 +|11x8.5 Landscape Tablet"),
            ("OFFLINE SAAS WEB APP", "6 Modules", "Pro Key CREATOR-OS-PRO-2026|50 Prompts + 12 Scripts"),
            ("NOTION 5-DB OS KIT", "62 Templates", "Outlier Bank, 1-to-15 Board|& Sponsorship CRM CSVs"),
        ],
    )
    png_t2 = STUDIO_ROOT / "08-COVER-DESIGN/png/gumroad-tier2-workbook-edition-cover.png"
    render_svg_cover_to_png(svg_t2, png_t2, 1600, 1000)
    print(f"  -> [4/7] Gumroad Tier 2 Cover (1600x1000): SVG={svg_t2.stat().st_size:,}B, PNG={png_t2.stat().st_size:,}B")

    # 5. Gumroad Tier 3 Complete Flagship OS Bundle Cover (1600x1000)
    svg_t3 = build_gumroad_widescreen_cover_svg(
        filename="gumroad-tier3-flagship-bundle-cover.svg",
        tier_badge="TIER 3 EXECUTIVE SOLOPRENEUR SUITE · COMPLETE AUTOMATION & OFFICE KIT",
        price_badge="FLAGSHIP OS · $199",
        headline_1="THE COMPLETE EXECUTIVE",
        headline_2="SOLOPRENEUR AUTOMATION SUITE",
        subtitle="Everything in Tier 2 PLUS n8n/Make JSON Workflows, Excel Financial Trackers, DOCX SOPs & PPTX Decks",
        accent_hex="#0D9488",
        secondary_hex="#FBBF24",
        cards=[
            ("N8N & MAKE WORKFLOWS", "JSON Ready", "Automated Outlier Mining|& 1-to-15 Repurposing Flows"),
            ("EXCEL & SHEETS SUITE", "Multi-Tab", "RPPH, 4-Tier Value Ladder|& Sponsor Rate Calculators"),
            ("DOCX & PPTX OFFICE", "Editable", "Standard Operating Manuals|& Executive Pitch Decks"),
            ("FULL PRO VAULT ACCESS", "All 62 Assets", "50 AI Prompts + 12 Scripts|& 20 Vector Diagrams"),
        ],
    )
    png_t3 = STUDIO_ROOT / "08-COVER-DESIGN/png/gumroad-tier3-flagship-bundle-cover.png"
    render_svg_cover_to_png(svg_t3, png_t3, 1600, 1000)
    print(f"  -> [5/7] Gumroad Tier 3 Cover (1600x1000): SVG={svg_t3.stat().st_size:,}B, PNG={png_t3.stat().st_size:,}B")

    # 6. Gumroad Tier 4 Living Creator Vault Membership Cover (1600x1000)
    svg_t4 = build_gumroad_widescreen_cover_svg(
        filename="gumroad-tier4-vault-membership-cover.svg",
        tier_badge="TIER 4 AGENCY, INCUBATOR & LIVING CREATOR VAULT WHITE-LABEL LICENSE",
        price_badge="AGENCY VAULT · $499",
        headline_1="COMMERCIAL WHITE-LABEL",
        headline_2="& LIVING CREATOR VAULT EDITION",
        subtitle="Full Commercial Client & Cohort Training Rights + Editable Source SVG Master Kit + All Tier 3 Assets",
        accent_hex="#D97706",
        secondary_hex="#FBBF24",
        cards=[
            ("WHITE-LABEL RIGHTS", "Commercial", "Train Agency Clients &|Paid Creator Cohorts"),
            ("SOURCE SVG MASTER KIT", "26 Vectors", "20 System Diagrams +|6 Editable Cover Masters"),
            ("CLIENT ONBOARDING", "Turnkey SOPs", "Editor Delegation Kits &|Sponsorship Media Decks"),
            ("COMPLETE OS ARCHIVE", "115k+ Words", "All Books, Workbooks, Web|App, Notion & Automations"),
        ],
    )
    png_t4 = STUDIO_ROOT / "08-COVER-DESIGN/png/gumroad-tier4-vault-membership-cover.png"
    render_svg_cover_to_png(svg_t4, png_t4, 1600, 1000)
    print(f"  -> [6/7] Gumroad Tier 4 Cover (1600x1000): SVG={svg_t4.stat().st_size:,}B, PNG={png_t4.stat().st_size:,}B")

    # 7. Cover Design & Print Packaging Spec Markdown
    spec_md = build_cover_packaging_spec_md(geom)
    print(f"  -> [7/7] {spec_md.relative_to(STUDIO_ROOT).as_posix()} ({len(spec_md.read_text('utf-8').split()):,} words, {spec_md.stat().st_size:,} bytes)")

    # Update PROJECT_STATE.json
    state_data.setdefault("phase_status", {})["Phase 7"] = "COMPLETED"
    state_data["phase7_notion_and_covers"] = {
        "notion_csvs": {
            "06-NOTION-TEMPLATES/01-Outlier-Idea-Bank-and-Hook-Vault.csv": p_csv1.stat().st_size,
            "06-NOTION-TEMPLATES/02-Master-Content-Calendar-and-1to15-Waterfall.csv": p_csv2.stat().st_size,
            "06-NOTION-TEMPLATES/03-AI-Prompt-and-Script-Vault-62.csv": p_csv3.stat().st_size,
            "06-NOTION-TEMPLATES/04-Sponsorship-CRM-and-Affiliate-Tracker.csv": p_csv4.stat().st_size,
            "06-NOTION-TEMPLATES/Spreadsheets/sheet1-creator-rpm-and-time-audit.csv": p_csv_s1.stat().st_size,
        },
        "notion_guides": {
            "06-NOTION-TEMPLATES/05-Creator-Monetization-and-Launch-Hub.md": {
                "words": len(p_md5.read_text("utf-8").split()),
                "bytes": p_md5.stat().st_size,
            },
            "06-NOTION-TEMPLATES/NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md": {
                "words": len(p_md6.read_text("utf-8").split()),
                "bytes": p_md6.stat().st_size,
            },
        },
        "kdp_full_wrap_geometry": geom,
        "cover_suite": {
            "ebook_kindle_png_bytes": png_kindle_root.stat().st_size,
            "kdp_full_wrap_png_bytes": png_wrap.stat().st_size,
            "kdp_full_wrap_pdf_bytes": pdf_wrap.stat().st_size,
            "gumroad_tier0_png_bytes": png_t0.stat().st_size,
            "gumroad_tier2_png_bytes": png_t2.stat().st_size,
            "gumroad_tier3_png_bytes": png_t3.stat().st_size,
            "gumroad_tier4_png_bytes": png_t4.stat().st_size,
            "packaging_spec_words": len(spec_md.read_text("utf-8").split()),
        },
    }
    state_path.write_text(json.dumps(state_data, indent=2) + "\n", encoding="utf-8")
    print("\n[SUCCESS] PROJECT_STATE.json updated with Phase 7 Notion & Cover telemetry.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
