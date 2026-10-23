#!/usr/bin/env python3
"""
Antigravity Studio Compiler — Phase 9 Part A (phase9_office_and_studio.py)
Builds:
  - Upgrade 2: 7 Editable Microsoft Word (.docx) Documents & Templates (12-EDITABLE-OFFICE-SUITE/Word-Docs/)
  - Upgrade 3: 3 Widescreen 16:9 Editable PowerPoint (.pptx) Slide Decks (12-EDITABLE-OFFICE-SUITE/Slide-Decks/)
  - Upgrade 5: Interactive Cover, YouTube Thumbnail & Social Card Customizer Studio (08-COVER-DESIGN/Editable-Design-Kit/)
"""

import re
import sys
from pathlib import Path

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

from pptx import Presentation
from pptx.dml.color import RGBColor as PptxRGB
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches as PptxInches, Pt as PptxPt

STUDIO_ROOT = Path(__file__).resolve().parent
MANUSCRIPT_DIR = STUDIO_ROOT / "03-MANUSCRIPT"
WORKBOOK_MD_DIR = STUDIO_ROOT / "05-WORKBOOKS" / "markdown"
PNG_DIR = STUDIO_ROOT / "04-VISUAL-ASSETS" / "png"
WORD_DIR = STUDIO_ROOT / "12-EDITABLE-OFFICE-SUITE" / "Word-Docs"
PPTX_DIR = STUDIO_ROOT / "12-EDITABLE-OFFICE-SUITE" / "Slide-Decks"
DESIGN_KIT_DIR = STUDIO_ROOT / "08-COVER-DESIGN" / "Editable-Design-Kit"

# Locked Studio Colors
NAVY_RGB = RGBColor(0x0F, 0x17, 0x2A)
INDIGO_RGB = RGBColor(0x4F, 0x46, 0xE5)
TEAL_RGB = RGBColor(0x0D, 0x94, 0x88)
AMBER_RGB = RGBColor(0xD9, 0x77, 0x06)
TEXT_RGB = RGBColor(0x1E, 0x29, 0x3B)
MUTED_RGB = RGBColor(0x64, 0x74, 0x8B)
WHITE_RGB = RGBColor(0xFF, 0xFF, 0xFF)


# ---------------------------------------------------------------------------
# DOCX STYLING & XML HELPERS
# ---------------------------------------------------------------------------

def set_cell_background(cell, hex_color: str) -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color.lstrip("#"))
    tcPr.append(shd)


def configure_doc_styles(doc: docx.Document) -> None:
    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.font.color.rgb = TEXT_RGB

    for level, (sz, col) in enumerate(
        [(20, NAVY_RGB), (15, INDIGO_RGB), (12.5, TEAL_RGB), (11.5, NAVY_RGB)], start=1
    ):
        style_name = f"Heading {level}"
        if style_name in doc.styles:
            st = doc.styles[style_name]
            st.font.name = "Calibri"
            st.font.size = Pt(sz)
            st.font.bold = True
            st.font.color.rgb = col


def clean_inline_md(text: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    s = re.sub(r"\*(.+?)\*", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", s)
    return s.strip()


def add_styled_table(doc: docx.Document, headers: list[str], rows: list[list[str]], header_hex: str = "0F172A") -> None:
    if not headers:
        return
    num_cols = len(headers)
    table = doc.add_table(rows=1, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"

    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = ""
        p = hdr_cells[i].paragraphs[0]
        run = p.add_run(clean_inline_md(h_text))
        run.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = WHITE_RGB
        set_cell_background(hdr_cells[i], header_hex)

    for r_idx, r_data in enumerate(rows):
        row_cells = table.add_row().cells
        bg_hex = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx in range(num_cols):
            val = r_data[c_idx] if c_idx < len(r_data) else ""
            row_cells[c_idx].text = ""
            p = row_cells[c_idx].paragraphs[0]
            run = p.add_run(clean_inline_md(val))
            run.font.size = Pt(10)
            run.font.color.rgb = TEXT_RGB
            set_cell_background(row_cells[c_idx], bg_hex)

    doc.add_paragraph()


def append_markdown_to_docx(doc: docx.Document, md_text: str, embed_images: bool = True) -> None:
    lines = md_text.splitlines()
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped or stripped in ("---", "***"):
            i += 1
            continue

        # Image syntax ![alt](path)
        img_m = re.match(r"^!\[(.*?)\]\((.*?)\)$", stripped)
        if img_m:
            alt_text, raw_src = img_m.group(1), img_m.group(2)
            if embed_images:
                svg_name = Path(raw_src).stem
                png_candidate = PNG_DIR / f"{svg_name}.png"
                if png_candidate.exists():
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run = p.add_run()
                    run.add_picture(str(png_candidate), width=Inches(6.2))
                    cap = doc.add_paragraph()
                    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    c_run = cap.add_run(clean_inline_md(alt_text))
                    c_run.font.size = Pt(9.5)
                    c_run.font.italic = True
                    c_run.font.color.rgb = MUTED_RGB
            i += 1
            continue

        # Fenced code / prompt block
        if stripped.startswith("```"):
            code_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            if code_lines:
                tbl = doc.add_table(rows=1, cols=1)
                tbl.style = "Table Grid"
                cell = tbl.rows[0].cells[0]
                set_cell_background(cell, "F1F5F9")
                p = cell.paragraphs[0]
                run = p.add_run("\n".join(code_lines))
                run.font.name = "Consolas"
                run.font.size = Pt(9.5)
                run.font.color.rgb = NAVY_RGB
                doc.add_paragraph()
            continue

        # Pipe table
        if stripped.startswith("|") and stripped.endswith("|"):
            tbl_lines = []
            while i < n and lines[i].strip().startswith("|"):
                tbl_lines.append(lines[i].strip())
                i += 1
            parsed_rows = []
            for tl in tbl_lines:
                if re.match(r"^\|[\s\-:|]+\|$", tl):
                    continue
                cells = [c.strip() for c in tl.strip("|").split("|")]
                parsed_rows.append(cells)
            if len(parsed_rows) >= 1:
                add_styled_table(doc, parsed_rows[0], parsed_rows[1:], header_hex="0F172A")
            continue

        # Headings
        h_m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if h_m:
            level = min(len(h_m.group(1)), 4)
            doc.add_heading(clean_inline_md(h_m.group(2)), level=level)
            i += 1
            continue

        # Blockquote / Callout
        if stripped.startswith(">"):
            q_lines = []
            while i < n and lines[i].strip().startswith(">"):
                q_lines.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.35)
            run = p.add_run(clean_inline_md(" ".join(q_lines)))
            run.font.italic = True
            run.font.color.rgb = INDIGO_RGB
            continue

        # Bullet / Numbered list
        b_m = re.match(r"^(\*|-|\d+\.)\s+(.*)$", stripped)
        if b_m:
            p = doc.add_paragraph(style="List Bullet")
            p.add_run(clean_inline_md(b_m.group(2)))
            i += 1
            continue

        # Regular paragraph
        p = doc.add_paragraph(clean_inline_md(stripped))
        i += 1


def add_title_banner(doc: docx.Document, doc_code: str, title: str, subtitle: str) -> None:
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = "Table Grid"
    cell = tbl.rows[0].cells[0]
    set_cell_background(cell, "0F172A")
    p = cell.paragraphs[0]
    r0 = p.add_run(f"APEX DIGITAL SYSTEMS STUDIO · {doc_code}\n")
    r0.font.size = Pt(9.5)
    r0.font.bold = True
    r0.font.color.rgb = RGBColor(0x2D, 0xD4, 0xBF)
    r1 = p.add_run(f"{title}\n")
    r1.font.size = Pt(18)
    r1.font.bold = True
    r1.font.color.rgb = WHITE_RGB
    r2 = p.add_run(subtitle)
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)
    doc.add_paragraph()


# ---------------------------------------------------------------------------
# UPGRADE 2: BUILD ALL 7 EDITABLE WORD (.DOCX) DOCUMENTS
# ---------------------------------------------------------------------------

def build_all_seven_docx_files() -> list[tuple[Path, int]]:
    WORD_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    # 1. 01-Full-Editable-Book-Manuscript.docx
    doc1 = docx.Document()
    configure_doc_styles(doc1)
    add_title_banner(
        doc1,
        "EDITABLE MASTER MANUSCRIPT EDITION v1.0.0",
        "The AI Content Creator & Solopreneur Operating System",
        "A Practical System to Research Validated Ideas, Script High-Retention Content, Repurpose Across Platforms, Automate Production, and Monetize Your Audience Without Burnout",
    )
    ms_order = (
        [MANUSCRIPT_DIR / "front-matter.md"]
        + [MANUSCRIPT_DIR / f"chapter-{i:02d}.md" for i in range(1, 11)]
        + [MANUSCRIPT_DIR / "back-matter.md"]
    )
    for idx, mf in enumerate(ms_order):
        append_markdown_to_docx(doc1, mf.read_text(encoding="utf-8"), embed_images=True)
        if idx < len(ms_order) - 1:
            doc1.add_page_break()
    p1 = WORD_DIR / "01-Full-Editable-Book-Manuscript.docx"
    doc1.save(str(p1))
    results.append((p1, count_docx_words(p1)))

    # 2. 02-Editable-10-Chapter-Action-Workbook.docx
    doc2 = docx.Document()
    configure_doc_styles(doc2)
    add_title_banner(
        doc2,
        "EDITABLE 10-CHAPTER ACTION WORKBOOK EDITION",
        "The AI Content Creator & Solopreneur OS — Complete Action Workbook",
        "10 Fillable Chapter Implementation Worksheets, Quantitative Stage-Gate Scorecards, and 30-Day Execution Checklists",
    )
    for i in range(1, 11):
        wf = WORKBOOK_MD_DIR / f"worksheet-{i:02d}.md"
        append_markdown_to_docx(doc2, wf.read_text(encoding="utf-8"), embed_images=False)
        if i < 10:
            doc2.add_page_break()
    p2 = WORD_DIR / "02-Editable-10-Chapter-Action-Workbook.docx"
    doc2.save(str(p2))
    results.append((p2, count_docx_words(p2)))

    # 3. 03-Sponsorship-Media-Kit-and-Rate-Card-Proposal.docx (>= 1,800 words)
    p3 = WORD_DIR / "03-Sponsorship-Media-Kit-and-Rate-Card-Proposal.docx"
    build_template_docx(p3, "TEMPLATE 03 · SPONSORSHIP MEDIA KIT & PROPOSAL", "Creator Authority Media Kit & Outcome Sponsorship Rate Card", get_template_03_md())
    results.append((p3, count_docx_words(p3)))

    # 4. 04-Brand-Deal-Agreement-and-Usage-Rights-Contract.docx (>= 2,000 words)
    p4 = WORD_DIR / "04-Brand-Deal-Agreement-and-Usage-Rights-Contract.docx"
    build_template_docx(p4, "TEMPLATE 04 · SPONSORSHIP & LICENSING AGREEMENT", "Creator-Protection Brand Deal & Usage-Rights Contract Template", get_template_04_md())
    results.append((p4, count_docx_words(p4)))

    # 5. 05-Pillar-to-15-Repurposing-Script-Template.docx (>= 1,500 words)
    p5 = WORD_DIR / "05-Pillar-to-15-Repurposing-Script-Template.docx"
    build_template_docx(p5, "TEMPLATE 05 · WEEKLY MASTER PRODUCTION SCRIPT", "S.I.G.N.A.L., C.L.I.P., H.E.A.R.T. & 1-to-15 Waterfall Master Script Template", get_template_05_md())
    results.append((p5, count_docx_words(p5)))

    # 6. 06-Digital-Product-14-Day-Launch-Runbook.docx (>= 1,800 words)
    p6 = WORD_DIR / "06-Digital-Product-14-Day-Launch-Runbook.docx"
    build_template_docx(p6, "TEMPLATE 06 · 14-DAY DIGITAL PRODUCT LAUNCH SOP", "Validate-Before-You-Build 14-Day Pre-Sale & 4-Tier Value Ladder Runbook", get_template_06_md())
    results.append((p6, count_docx_words(p6)))

    # 7. 07-Weekly-Creator-CEO-Review-and-RPPH-Template.docx (>= 1,500 words)
    p7 = WORD_DIR / "07-Weekly-Creator-CEO-Review-and-RPPH-Template.docx"
    build_template_docx(p7, "TEMPLATE 07 · 20-MINUTE FRIDAY CREATOR CEO SCORECARD", "Weekly Executive Operating Review, RPPH Audit & 4-Hour Batch Planner", get_template_07_md())
    results.append((p7, count_docx_words(p7)))

    return results


def build_template_docx(out_path: Path, code: str, title: str, md_body: str) -> None:
    doc = docx.Document()
    configure_doc_styles(doc)
    add_title_banner(
        doc,
        code,
        title,
        "The AI Content Creator & Solopreneur Operating System — Customizable Operator SOP & Commercial Template",
    )
    append_markdown_to_docx(doc, md_body, embed_images=False)
    doc.save(str(out_path))


def count_docx_words(path: Path) -> int:
    d = docx.Document(str(path))
    words = 0
    for p in d.paragraphs:
        words += len(p.text.split())
    for t in d.tables:
        for row in t.rows:
            for cell in row.cells:
                words += len(cell.text.split())
    return words


def get_template_03_md() -> str:
    return r"""# Creator Authority Media Kit & Outcome-Based Sponsorship Proposal

## 1. Executive Partner Summary & Audience Positioning

Welcome to our official Creator Media Kit and Commercial Partnership Proposal. Unlike general entertainment channels that rely on passive algorithmic views, our media property operates as a high-trust educational and implementation resource for active B2B decision-makers, technical practitioners, consultants, and solo founders. Every weekly pillar tutorial, newsletter issue, and LinkedIn/X breakdown is engineered around hands-on workflow execution—meaning our audience consumes our content with open browser tabs, corporate credit cards, and immediate software evaluation intent.

When your brand partners with our publication, you are not purchasing fleeting top-of-funnel impressions. You are embedding your product directly inside a documented technical workflow that practitioners bookmark, share with their engineering and operations teams, and reference for 12 to 24 months via evergreen search discovery.

| Authority Metric / Channel Dimension | Current Verified Telemetry | 90-Day Growth Trend | Industry Benchmark Comparison |
| :--- | :--- | :--- | :--- |
| **Primary Niche & Category Focus** | `[B2B AI Workflows, Operations & Solopreneur Systems]` | Category-of-One Moat (`NMPI: 88/100`) | Top `5%` Commercial Buyer Intent |
| **Combined Cross-Platform Subscribers** | `[28,500+ Total Practitioners]` | `+14.2% Quarter-over-Quarter` | `3.8x` Higher B2B Decision Density |
| **Owned Email Newsletter Subscribers** | `[11,400+ Active Double-Opt-In Readers]` | `+950 Net New Subscribers / Month` | Verified Zero-Cold-Subscriber List Hygiene |
| **Average 30-Second Hook Hold Rate** | `73.8%` (Across Pillar Tutorials) | `+6.4% vs. Prior Quarter` | Industry Average: `44.0%` |
| **Average Pillar Video View Duration (AVD)** | `54.6%` (`10:18` Avg Watch Time) | Consistent High-Depth Completion | Industry Average: `35.0%` |
| **Newsletter Open Rate / Unique Link CTR** | `49.4% Open Rate` / `7.2% Unique CTR` | Audited Across Trailing 12 Issues | Industry Average: `32% Open / 2.1% CTR` |

## 2. Audience Demographics, Psychographics & Purchasing Power

Our audience consists of builders, operators, and budget-holding professionals who actively invest in software, automation infrastructure, financial tools, and productivity systems to reclaim time and scale revenue:

* **Role Breakdown:** `38%` Solo Founders & Agency Principals · `29%` Senior Operations, Product & Engineering Leads · `21%` Independent Consultants & Technical Creators · `12%` Executive & Finance Decision-Makers.
* **Annual Software & Tool Stack Budget:** Over `74%` of surveyed subscribers control or directly influence between `$2,500` and `$25,000+` in annual SaaS, cloud, AI, and operational tool spending.
* **Geographic Distribution:** `52%` North America (United States & Canada) · `26%` United Kingdom & European Union · `14%` Asia-Pacific (Singapore, Australia, India, Bangladesh) · `8%` Rest of World.
* **Primary Purchasing Triggers:** Verified time savings (`hours reclaimed per week`), direct revenue or conversion lift, zero-fluff workflow compatibility, and transparent live demonstrations.

## 3. Why Standard CPM Pricing Fails Both Brands and Creators

Traditional Cost-Per-Mille (`$20–$30 CPM`) ad reads were designed for broad consumer entertainment channels where 98% of viewers have zero intent to purchase B2B software. Furthermore, standard 30-second scripted ad reads suffer from severe viewer skip rates (`65%+` skip spike on retention graphs).

Our studio replaces skipped ad reads with **Outcome-Based Native Workflow Integrations (`R_sponsor`)**:
1. **Native Problem-Solution Demonstration:** Instead of reading a generic press release, we demonstrate your product solving a real operational bottleneck live on screen inside the core tutorial narrative.
2. **Omnichannel Multi-Touch Reinforcement:** Research shows B2B buyers require 3 to 5 touchpoints before starting a trial. Every standard partnership bundles video demonstration with owned email newsletter placements, LinkedIn/X text breakdowns, and permanent resource-vault links.
3. **Tracked Lead-Magnet Conversion Bridge:** We place your custom UTM trial link directly inside the companion worksheet and Notion resource pack downloaded by our highest-intent viewers.

## 4. Documented Past Partner Case Studies & Conversion Proof

| Partner Category | Campaign Structure | 14-Day Verified Views & Opens | Tracked Link Clicks (UTM) | Trial / Pipeline Outcome Achieved |
| :--- | :--- | :--- | :--- | :--- |
| **B2B Workflow Automation SaaS** | Tier B Multi-Touch Sprint (1 Pillar Video + 2 Newsletters + LinkedIn) | `19,400 Video Views` + `10,800 Email Opens` | `1,140 Unique Clicks` (`5.8% CTR`) | `312 Free Trials` + `48 Paid Annual Plans` (`$28,400 ARR` attributed in 30 days) |
| **AI Documentation & Knowledge Tool** | Tier C Quarterly Partner (3 Monthly Sprints + 60-Day Ad Whitelisting) | `64,200 Video Views` + `33,500 Email Opens` | `3,480 Unique Clicks` (`5.4% CTR`) | `890+ Product Signups` + `2.9x ROAS` on Whitelisted Paid Social Cutdowns |
| **FinTech & Creator Banking Platform** | Tier A Single Pillar + Dedicated Newsletter Top-Slot | `15,800 Video Views` + `5,400 Email Opens` | `790 Unique Clicks` (`5.0% CTR`) | `164 Funded Business Accounts` within 21 days of publication |

## 5. The 3-Tier Omnichannel Outcome Sponsorship Packages

We offer three transparent, turnkey partnership tiers engineered around your quarterly customer acquisition goals. All packages include full UTM link tracking and our signature **Day-14 Proof-of-Performance ROI Telemetry Report**.

| Package Feature / Deliverable | Tier A: Single-Sprint Launch (`$1,850 USD`) | Tier B: Omnichannel Conversion Bundle (`$3,200 USD` — Most Popular) | Tier C: Quarterly Category Partner (`$8,400 USD` — Save 15%) |
| :--- | :--- | :--- | :--- |
| **60–90s Native Mid-Roll Workflow Demo (YouTube Pillar)** | `1x Pillar Integration` (Permanent Evergreen Placement) | `1x Pillar Integration` + Pin Comment + Description Top Link | `3x Monthly Pillar Integrations` (1 Per Month for 90 Days) |
| **Owned Email Newsletter Top-of-Fold Sponsorship** | `1x Primary Issue Slot` (`150 words` + Logo + CTA Button) | `2x Primary Issue Slots` (Tuesday Value + Friday Offer Issue) | `6x Primary Issue Slots` (2 Per Month Across Full Quarter) |
| **Native LinkedIn & X Authority Breakdown Post** | Not Included | `1x Dedicated LinkedIn Post` + `1x X Thread Integration` | `3x LinkedIn Posts` + `3x X Threads` + `1x PDF Carousel` |
| **Inclusion in Downloadable Chapter Resource Vault** | Standard Link Inclusion | Featured Tool Callout Box Inside Fillable PDF/Notion Kit | Permanent Featured Stack Partner Across All Quarter Downloads |
| **Paid-Ad Whitelisting & Spark/Cutdown Licensing** | Optional (`+$550 / 30 Days`) | **Included: `30 Days` Paid Social Cutdown Rights** | **Included: `90 Days` Full Paid Social & Landing Page Rights** |
| **Direct Competitor Category Exclusivity** | `7-Day Sprint Exclusivity` | `30-Day Category Exclusivity` | **Full `90-Day` Category Lock (Zero Competitor Mentions)** |
| **Day-14 Proof-of-Performance Telemetry Report** | Included | Included + 30-Day Long-Tail Update | Included Monthly + Quarterly Executive Strategy Review |

## 6. Paid-Ad Whitelisting, Usage Rights & Add-On Pricing Formula

Every package is priced deterministically using our studio's **Outcome Sponsorship Valuation Formula**:
$$R_{\text{sponsor}} = (\text{Base Placement Rate} \times \text{Niche Authority Multiplier}) + \text{Omnichannel Add-Ons} + \text{Usage Rights Fee} + \text{Exclusivity Fee}$$

* **Paid-Ad Whitelisting / Cutdown Licensing (`+30% of Base Rate per 30-Day Period`):** Allows your paid acquisition team to run our 60-second native workflow demonstration as a high-converting UGC/creator ad on Meta, YouTube, LinkedIn, or X, or embed the clip directly on your homepage/landing page.
* **Dedicated Standalone Deep-Dive Tutorial (`$4,800 USD`):** A full 12-to-18-minute end-to-end tutorial built entirely around your platform, including a custom downloadable Notion/Spreadsheet template built for your users.

## 7. 14-Day Production Workflow & Factual Review SLA

1. **Day 01 (Agreement & Deposit Lock):** Partner selects Tier A, B, or C, signs the 2-page Creator-Protection Sponsorship Agreement, and remits the `50%` scheduling deposit (`Net-15` for balance upon publication).
2. **Day 03 (Async Talking-Point Alignment):** Partner provides product access, target UTM destination URL, and top 3 factual value propositions.
3. **Day 07 (Integration Storyboard & Factual Check):** We submit the exact 60-second workflow demonstration outline and newsletter copy for a **single consolidated round of factual verification** (`48-hour` turnaround).
4. **Day 10–12 (Batch Production & 12-Point QA Gate):** Integration is recorded, edited with custom visual callouts, and verified across all links.
5. **Day 14 (Omnichannel Publication & Live Link Delivery):** Video, newsletter, and social assets go live; live URLs and timestamp links are delivered immediately.
6. **Day 28 (Day-14 Proof-of-Performance ROI Report):** We deliver verified view, retention, email open, and UTM click telemetry along with priority renewal options.

## 8. Partnership Onboarding & Reservation Block

To lock in your preferred publication sprint date, complete the fields below and return via email:

* **Partner Company & Product Name:** `[ENTER COMPANY & PRODUCT NAME]`
* **Primary Point of Contact (Name, Title, Email):** `[ENTER CONTACT DETAILS]`
* **Billing Entity Address & Tax/VAT ID:** `[ENTER BILLING ADDRESS]`
* **Selected Partnership Tier:** `[ ] Tier A ($1,850)   [ ] Tier B ($3,200)   [ ] Tier C Quarterly ($8,400)`
* **Optional Licensing Add-Ons:** `[ ] Additional 30-Day Whitelisting (+30%)   [ ] Dedicated Deep-Dive ($4,800)`
* **Target Publication Week & Campaign Goal:** `[ENTER TARGET WEEK & PRIMARY TRIAL/CONVERSION GOAL]`

---

## 9. Historical Partner Case Studies & Verified Day-14 ROI Telemetry Benchmarks

Unlike traditional consumer entertainment sponsorships that rely on passive mid-roll ad reads and expire within 48 hours of upload, our **Live Workflow Demonstration Integrations** compound in search and recommendation engines for 12 to 24 months. Below are three representative anonymized B2B SaaS partner campaigns executed across our Pillar Video + Owned Newsletter ecosystem:

| Partner Category & Tier | 14-Day Verified Views | Mid-Roll Segment Hold Rate | Newsletter Open / Click Rate | Total Tracked UTM Clicks (`14d`) | Verified Free-Trial / Demo Signups | Partner Renewal Outcome |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Case A: AI Workflow Automation SaaS** (`Tier B · $3,200`) | `19,400 Views` | `89.4% Hold` (`0:60–2:15`) | `51.2% Open` · `7.8% CTR` | `842 Unique Clicks` | `214 Free Trials` (`$14.95 CAC`) | Upgraded to `Tier C Quarterly ($8,400)` |
| **Case B: B2B Cloud Analytics Platform** (`Tier C · $8,400 Qtr`) | `64,800 Views` (`3 Videos`) | `87.8% Hold` | `49.6% Open` · `6.9% CTR` | `2,610 Unique Clicks` | `148 Team Demos Booked` | Renewed for 2nd Consecutive Quarter |
| **Case C: Solopreneur Financial & Tax Tool** (`Tier A · $1,850`) | `14,200 Views` | `86.2% Hold` | `50.4% Open` · `6.4% CTR` | `518 Unique Clicks` | `132 Paid Subscriptions` | Upgraded to `Tier B` + `60d Whitelisting` |

### Why Our Native Workflow Demonstrations Outperform Standard Ad Reads by `3.4x`:
1. **Zero Viewer Ad-Skip Reflex:** We never say *"This video is brought to you by..."* Instead, we introduce your product inside **Block 2 or Block 3 of our H.E.A.R.T. tutorial script** as the exact software instrument solving the step we are teaching on screen.
2. **Dual-Channel High-Intent Reinforcement:** Viewers who watch the 60-second screen demonstration on YouTube receive our Tuesday and Friday **Owned Operator Newsletter** (`49.4%` open rate) featuring a direct top-of-fold deep link and implementation checklist for your tool.
3. **Turnkey Paid-Social Cutdown Asset:** When your growth team selects **Tier B or Tier C**, we deliver a clean, high-resolution `16:9` and `9:16` cutdown of the 60-second workflow demonstration ready to deploy immediately inside your Meta, LinkedIn, and YouTube paid acquisition campaigns.
"""


def get_template_04_md() -> str:
    return r"""# Creator-Protection Brand Deal & Usage-Rights Agreement Template

## Commercial Sponsorship, Content Integration & Licensing Contract

This Brand Sponsorship and Content Integration Agreement (the **"Agreement"**) is entered into as of **`[EFFECTIVE DATE]`** (the **"Effective Date"**), by and between:

* **Creator / Publisher Entity:** **`[CREATOR LEGAL NAME OR STUDIO LLC]`**, operating the media property known as **`[CHANNEL / NEWSLETTER NAME]`**, with principal offices at **`[CREATOR BUSINESS ADDRESS]`** (**"Creator"**), and
* **Sponsor / Brand Entity:** **`[SPONSOR LEGAL CORPORATE NAME]`**, with principal offices at **`[SPONSOR CORPORATE ADDRESS]`** (**"Sponsor"**).

Creator and Sponsor may each be referred to individually as a **"Party"** and collectively as the **"Parties."**

---

## 1. Scope of Sponsored Deliverables & Publication Schedule

Creator agrees to research, script, produce, and publish the native content integration deliverables specified in the table below (collectively, the **"Deliverables"**) featuring Sponsor's product or service known as **`[PRODUCT / SERVICE NAME]`** (the **"Featured Product"**):

| Deliverable ID | Platform & Format | Integration Placement & Duration | Target Publication Date | Included Organic Hosting Window |
| :---: | :--- | :--- | :---: | :--- |
| **DEL-01** | `YouTube Long-Form Pillar Video` | `60–90 Second Mid-Roll Native Workflow Demo` + Top Description UTM Link + Pinned Comment | `[YYYY-MM-DD]` | Minimum `12 Months` Evergreen Organic Hosting |
| **DEL-02** | `Owned Email Newsletter Issue #1` | `Top-of-Fold Primary Sponsor Box` (`150 words` + Brand Logo + Tracked CTA Button) | `[YYYY-MM-DD]` | Permanent Web Archive Inclusion |
| **DEL-03** | `Owned Email Newsletter Issue #2` | `Mid-Issue Operator Tool Spotlight` (`100 words` + Tracked CTA Link) | `[YYYY-MM-DD]` | Permanent Web Archive Inclusion |
| **DEL-04** | `LinkedIn & X Native Breakdown` | `1x Long-Form LinkedIn Post` + `1x X Thread` featuring workflow takeaway & link | `[YYYY-MM-DD]` | Permanent Organic Feed Hosting |

* **No Implied Additional Deliverables:** Any social posts, vertical short-form cutdowns, raw unedited video files, or additional revisions not explicitly listed in Section 1 are excluded from this Agreement unless added via a signed written amendment.

## 2. Creative Control, Editorial Independence & Revision Cap

1. **Creator Voice & Format Authority:** Sponsor acknowledges that Creator's audience trust and high retention rates depend on Creator's authentic editorial voice, visual style, and instructional format. Creator retains final creative authority over the scripting, pacing, visual presentation, and surrounding editorial content of the Pillar Video and Newsletter issues.
2. **Factual Brief & Prohibited Claims:** Sponsor shall provide a written factual brief (the **"Sponsor Brief"**) no later than **`7 business days`** prior to the Target Publication Date containing up to three (3) core product talking points, mandatory legal disclaimers, and the exact tracked destination URL.
3. **Single Consolidated Factual Revision Round:** Prior to publication, Creator shall submit the proposed integration script/storyboard (or rough-cut integration segment) to Sponsor for **factual accuracy review only**. Sponsor shall have **`48 hours`** from delivery to request **one (1) consolidated round of factual corrections**. If Sponsor does not respond within `48 hours`, the integration segment is deemed approved for publication.
4. **Reshoot & Scope-Creep Fee:** Any request by Sponsor to alter approved talking points after Creator has recorded the integration segment, or any request for a second revision round unrelated to objective factual errors by Creator, shall incur a mandatory **Reshoot & Re-Editing Fee equal to `25%` of the Base Package Fee** (`$[AMOUNT]`).

## 3. Intellectual Property Ownership, Paid-Ad Whitelisting & AI Training Prohibition

1. **Creator Retention of Master Copyright:** Creator retains `100%` ownership, copyright, and intellectual property rights in and to all Pillar Videos, Newsletter issues, scripts, visual diagrams, and underlying templates, including the integrated sponsorship segments.
2. **Standard Organic Social Sharing Rights:** During the Term, Sponsor is granted a non-exclusive, revocable license to share direct links to the published Deliverables on Sponsor's organic social media accounts and internal company communications with proper attribution to Creator.
3. **Paid-Ad Whitelisting, Dark Posting & Commercial Cutdown License (`+30% / 30 Days`):**
   * **Selection Status:** `[ ] NOT INCLUDED (Organic Hosting Only)   [X] INCLUDED FOR [30 / 60 / 90] DAYS`
   * Unless explicitly checked above and paid for in Section 5, Sponsor is **strictly prohibited** from downloading, clipping, re-uploading, boosting, whitelisting, or running any portion of Creator's video, audio, or likeness as a paid advertisement (including Meta Ads, YouTube Ads, LinkedIn Ads, TikTok Spark Ads, or website sales-page embeds).
   * Where Paid-Ad Licensing is purchased, Sponsor is granted a limited, non-exclusive license for **`[30 / 60 / 90] calendar days`** from publication to run the approved 60-second integration clip in paid social campaigns at a licensing rate of **`30%` of the Base Package Fee per 30-day period** (`$[USAGE FEE]`). Upon expiration of the licensed window, Sponsor must pause all paid ad sets within `48 hours` or renew at the standard monthly licensing rate.
4. **Strict Prohibition on Generative AI Voice, Likeness & Style Training:** Sponsor (and its agencies, contractors, or affiliates) shall **never** feed, upload, or use Creator's voice, facial likeness, video footage, or written scripts to train, fine-tune, clone, or synthesize any artificial intelligence model, synthetic voice clone, or digital avatar under any circumstances. Breach of this clause triggers immediate termination and liquidated damages equal to **`300%` of the Total Contract Value**.

## 4. Category Exclusivity & Non-Compete Boundaries

* **Exclusivity Window:** During the **`[7 / 30 / 90]-day period`** following the publication of `DEL-01`, Creator agrees not to publish a paid sponsorship integration featuring the following named direct competitors of Sponsor: **`[LIST MAXIMUM 3 NAMED DIRECT COMPETITOR BRANDS]`**.
* **Editorial Mention Carve-Out:** This exclusivity applies strictly to paid commercial sponsorships and does not restrict Creator from mentioning industry tools in unpaid, objective educational comparisons.

## 5. Compensation, Deposit Structure, Net-15 Invoicing & Late Fees

In consideration for the Deliverables and rights granted herein, Sponsor agrees to pay Creator the Total Contract Value calculated below:

| Fee Component | Calculation Basis | Agreed Amount (`USD`) |
| :--- | :--- | :---: |
| **1. Base Omnichannel Outcome Package (`DEL-01` to `DEL-04`)** | Base Rate × Niche Authority Multiplier (`2.0x`) + Add-Ons | `$[2,500.00]` |
| **2. Paid-Ad Whitelisting & Cutdown License** | `30%` of Base Rate × `[1]` Month (`30 Days`) | `$[750.00]` |
| **3. Direct Competitor Category Exclusivity Fee** | `[30-Day]` Named Competitor Lock | `$[250.00]` |
| **TOTAL CONTRACT VALUE (`USD`)** | **All-Inclusive Net Payable to Creator** | **`$[3,500.00] USD`** |

* **Payment Schedule:**
  1. **`50%` Production & Calendar Reservation Deposit (`$[1,750.00]`):** Due upon execution of this Agreement to lock Creator's production calendar. Production does not commence until the deposit clears.
  2. **`50%` Publication Balance (`$[1,750.00]`):** Invoiced upon live publication of `DEL-01`, payable strictly **`Net-15` calendar days** via ACH/Wire/Payoneer EFT to Creator's designated account.
* **Late Payment Interest & Removal Right:** Any invoice remaining unpaid past `Net-15` shall accrue a late administrative fee of **`3.0%` per month** (or the maximum rate permitted by law). If an invoice remains unpaid **`30 days`** past due, Creator reserves the right to unlist or remove the sponsorship links and revoke all Usage Rights until paid in full, without waiving Creator's right to collect the full contract balance.

## 6. Cancellation, Postponement & Kill-Fee Protection

1. **Kill Fee Before Recording (`50%`):** If Sponsor cancels this Agreement after booking the calendar slot and approving the Sponsor Brief, but prior to Creator recording the integration, Creator shall retain the **`50%` Reservation Deposit** as a non-refundable kill fee compensating for lost inventory.
2. **Kill Fee After Recording (`100%`):** If Sponsor cancels the campaign after Creator has recorded the integration segment in accordance with the approved Sponsor Brief, **`100%` of the Total Contract Value** is immediately due and payable.
3. **Sponsor-Requested Postponement:** Sponsor may request a one-time reschedule of the publication date with at least `10 days` advance written notice, provided the new publication date falls within `30 days` of the original date.

## 7. FTC Disclosure, Representations & Limitation of Liability

* **FTC & Platform Compliance:** Creator shall clearly disclose the material connection between Creator and Sponsor in all Deliverables (e.g., verbal disclosure, `#ad` or `Sponsored by [Brand]` label, and YouTube's built-in Paid Promotion checkbox) in full compliance with US Federal Trade Commission (FTC) Endorsement Guides.
* **No Guaranteed View or Sales Minimums:** Sponsor acknowledges that organic algorithmic distribution and viewer purchasing decisions are outside Creator's control. Unless an explicit view-guarantee addendum is attached, fees are based on Deliverable execution and audience access rather than guaranteed view or conversion counts.
* **Mutual Indemnification & Liability Cap:** Sponsor warrants that the Featured Product and all claims in the Sponsor Brief are truthful, lawful, and non-infringing, and agrees to indemnify Creator against any third-party claims arising from Sponsor's product or claims. In no event shall Creator's aggregate liability under this Agreement exceed the total fees actually paid by Sponsor hereunder.

---

## 8. Authorized Signatures

| **FOR CREATOR / PUBLISHER:** | **FOR SPONSOR / BRAND:** |
| :--- | :--- |
| **Signature:** `______________________________` | **Signature:** `______________________________` |
| **Printed Name:** `[CREATOR LEGAL NAME]` | **Printed Name:** `[AUTHORIZED SIGNATORY NAME]` |
| **Title:** `Founder & Principal Operator` | **Title:** `[VP MARKETING / PARTNERSHIPS]` |
| **Date:** `[YYYY-MM-DD]` | **Date:** `[YYYY-MM-DD]` |
"""


def get_template_05_md() -> str:
    return r"""# Weekly Master Production Template: S.I.G.N.A.L., C.L.I.P., H.E.A.R.T. & 1-to-15 Waterfall

## 1. Monday Block 1 (`60 Min`): S.I.G.N.A.L. Outlier Validation & Package-First Lock

> **Mandatory Operator Stage Gate:** Never write a single line of script in Section 2 or Section 3 until all six fields in the S.I.G.N.A.L. Validation Header below pass their quantitative thresholds (`Outlier Multiplier M >= 2.5x` and `NMPI >= 75/100`).

| S.I.G.N.A.L. Validation Field | Current Sprint Entry | Quantitative Gate / Rule |
| :--- | :--- | :--- |
| **Sprint Week & Publish Date** | `Week [01] · Publish Date: [YYYY-MM-DD]` | Locked 4-Hour Mon–Thu Batch Cadence |
| **Source Peer Outlier Reference** | `Channel: [PEER NAME] · URL: [URL]` | Must be within your 25-channel peer cohort |
| **Outlier Multiplier ($M_{\text{outlier}}$)** | `14d Views: [22,400] / Median: [5,200] = [4.31x]` | **HARD GATE: $M_{\text{outlier}} \ge 2.5\times$** |
| **Primary Audience Pain & Comment Gap** | `[Exact unfulfilled question extracted from peer comments]` | Verified via Prompt `P12` |
| **Locked Title Option A (Contrarian/Math)** | `[How I Replaced a 35-Hour Workflow With a 4-Hour System]` | `52–68 characters` · Front-loaded keyword |
| **Locked Title Option B (A/B Test Backup)** | `[Why 88% of Creators Burn Out Under $10/Hr (And the Fix)]` | Ready for Day-1 CTR swap if `CTR < 6.5%` |
| **Locked 3-Word Thumbnail Concept** | **Words:** `[35 HRS -> 4 HRS]` · **Visual:** `[Split contrast card]` | Maximum `3 words` · High-contrast focal point |
| **Attached Lead Magnet & Sponsor Slot** | **Lead Magnet:** `[7-Day RPPH Audit]` · **Sponsor:** `[Brand / Own Offer]` | Every Pillar asset must route to an owned bridge |

---

## 2. First 30-Second C.L.I.P. Hook Engineering Grid (`0:00–0:30` — Target Hold `>= 70%`)

Draft and time-box your opening 30 seconds word-for-word (`~75 to 85 spoken words` at `160 WPM`) before drafting the main body:

| Timestamp Window | C.L.I.P. Structural Element | Exact Verbatim Spoken Audio (`Word-for-Word`) | Visual Pattern Interrupt / On-Screen B-Roll Cue |
| :---: | :--- | :--- | :--- |
| **`0:00 – 0:05`** | **C — Context & Callout** *(Confirm title/thumbnail promise in sentence 1; zero "Hey guys" throat-clearing)* | `"[Write exact opening sentence confirming the title and thumbnail promise immediately...]"` | `[Full-screen visual match of the thumbnail graphic + kinetic text highlight]` |
| **`0:05 – 0:12`** | **L — Loss-Aversion Stakes** *(Quantify the cost in hours or dollars of doing it the old way)* | `"[State the exact hours wasted or revenue lost every month by following conventional advice...]"` | `[Split-screen comparison or red highlight on legacy workflow metric]` |
| **`0:12 – 0:20`** | **I — Instant Visual Proof** *(Show the finished dashboard, spreadsheet, or outcome on screen now)* | `"[Show the exact finished system or case-study result the viewer will have by the end of the video...]"` | `[Screen-recording zoom-in on the live working calculator / Notion board]` |
| **`0:20 – 0:30`** | **P — Pattern-Interrupt Open Loop** *(Establish the 3-to-5 step roadmap and open a loop into Block 1)* | `"[To make this work in under 4 hours a week, we have to install 3 specific gates—starting with the math error hiding in your calendar...]"` | `[Animated 3-step roadmap bar appearing across bottom third of frame]` |

---

## 3. Tuesday Block 2 (`90 Min`): Two-Column H.E.A.R.T. Master Pillar Script (`1,800–2,400 Words`)

Use Prompts `P22`–`P25` together with your calibrated **5-Parameter Voice DNA Profile** to populate the two-column production table below. Insert a **Visual Pattern Reset (`[RESET]`)** every `90 seconds` (`~220 words`).

| Narrative Block & Target Time | Spoken Audio Track (`Voice-Calibrated Verbatim Script`) | Visual / B-Roll / Diagram & Retention Reset Cues |
| :--- | :--- | :--- |
| **BLOCK 1: H — Hook & Status-Quo Teardown** (`0:30 – 3:00`) | `[Draft 350–400 words diagnosing why the conventional approach fails mathematically. Use concrete numbers and name the structural trap...]` | `[Show Chapter Mindmap SVG / Red-vs-Green comparison table at 1:30]` |
| **BLOCK 2: E — Evidence & Case Study Proof** (`3:00 – 5:30`) | `[Draft 350–400 words walking through a real operator case study (Before hours/revenue vs. After hours/revenue) to prove the mechanism works...]` | `[Display Before/After Telemetry Card + Highlight key formula on screen]` |
| **MID-ROLL NATIVE BRIDGE (`5:30 – 6:45`)** | `[Deliver 60-second native workflow demo of your Lead Magnet (`Prompt P36`) OR Sponsor (`Prompt P46`) seamlessly inside the tutorial step...]` | `[Live screen-share clicking the exact tool/worksheet link in description]` |
| **BLOCK 3: A — Actionable 3-Step Framework** (`6:45 – 11:30`) | `[Draft 700–900 words teaching the core step-by-step installation: Step 1 (Input), Step 2 (Formula/Prompt), Step 3 (Verification Gate)...]` | `[Switch to live screen-share / flowchart walkthrough; insert 3 visual zooms]` |
| **BLOCK 4: R — Roadblock & Edge-Case Inoculation** (`11:30 – 13:30`) | `[Draft 300 words addressing the #1 implementation mistake beginners make and how to fix it in 5 minutes...]` | `[Show Warning Callout Box + Quick-Fix Checklist on screen]` |
| **BLOCK 5: T — Transformation & Single-Bridge CTA** (`13:30 – 14:30`) | `[Skip saying "Well, to wrap things up" (which causes a 40% viewer drop-off). Deliver the final takeaway and bridge directly into the next video or free audit kit...]` | `[End-screen card pointing to the exact next tutorial + Pinned Comment CTA]` |

---

## 4. The 1-to-15 Omnichannel Repurposing Waterfall Extraction Slots (`Prompts P26–P30`)

Immediately after locking the H.E.A.R.T. Pillar Script above, run Prompts `P26` through `P30` to populate all 14 derivative assets inside the same Tuesday session:

| Asset ID | Platform & Format | Extracted Hook / First Line (`Re-Hooked for Platform`) | Core Takeaway Source Block | CTA / Owned Funnel Bridge | Status |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **A01** | `YouTube / Podcast Pillar` | `[Locked Title Option A + 30s C.L.I.P. Hook]` | Full H.E.A.R.T. Script | Pinned Comment + Description Link | `[ ] Ready` |
| **A02** | `Vertical Short #1 (60s)` | `[Contrarian Truth Hook from Block 1]` | Block 1 Status-Quo Math | Comment Trigger / Bio Link | `[ ] Ready` |
| **A03** | `Vertical Short #2 (60s)` | `[Before/After Case Study Hook from Block 2]` | Block 2 Operator Proof | Bio Link to Free Audit Kit | `[ ] Ready` |
| **A04** | `Vertical Short #3 (60s)` | `[Step-by-Step Formula Demo from Block 3]` | Block 3 Core Equation | Save & Check Description | `[ ] Ready` |
| **A05** | `Vertical Short #4 (60s)` | `[#1 Mistake Teardown Hook from Block 4]` | Block 4 Edge-Case Fix | Bio Link to Worksheet | `[ ] Ready` |
| **A06** | `Vertical Short #5 (60s)` | `[60-Second Tool / Prompt Walkthrough]` | Mid-Roll / Prompt Demo | Bio Link to Prompt Vault | `[ ] Ready` |
| **A07** | `LinkedIn Authority Post #1` | `[2-Line Metric Contrast Hook + White-Space List]` | Block 1 + Block 3 | First-Comment Lead Magnet Link | `[ ] Ready` |
| **A08** | `LinkedIn Case Study Post #2` | `[How [Name] Cut Weekly Hours from X to Y...]` | Block 2 Case Teardown | P.S. Link to Full Newsletter | `[ ] Ready` |
| **A09** | `X (Twitter) 8-Post Thread` | `[Bookmark-Worthy Framework Thread Hook]` | Blocks 1, 2, 3 & 4 | Final Tweet Opt-In Bridge | `[ ] Ready` |
| **A10** | `X Single-Image Atomic Essay` | `[Punchy Contrarian Thesis + Diagram Screenshot]` | Chapter SVG Diagram | Reply Link to Free Starter Kit | `[ ] Ready` |
| **A11** | `8-Slide PDF / IG Carousel #1` | `Slide 1: [The 5-Stage Blueprint to Solve X]` | Block 3 Step-by-Step | Slide 8: Download Full Workbook | `[ ] Ready` |
| **A12** | `8-Slide PDF / IG Carousel #2` | `Slide 1: [Old Treadmill Math vs. Operator Math]` | Block 1 + Block 2 | Slide 8: Run Free RPPH Calculator | `[ ] Ready` |
| **A13** | `8-Slide PDF / IG Carousel #3` | `Slide 1: [Copy-Paste This Exact AI Prompt...]` | Featured Chapter Prompt | Slide 8: Grab 62-Prompt Vault | `[ ] Ready` |
| **A14** | `Tuesday Value Newsletter` | `Subject: [The exact formula behind X (Case Study)]` | Full Essay Adaptation | 2 Inline Links to Pillar + Magnet | `[ ] Ready` |
| **A15** | `Friday Monetization Issue` | `Subject: [Quick implementation check + Toolkit]` | Block 4 + Offer Bridge | Direct Link to Tier 2 / Tier 3 Offer | `[ ] Ready` |

---

## 5. Voice DNA Anti-Slop Header & 12-Point Pre-Flight QA Verification Gate (`Thursday Block 4`)

Before pasting your Pillar Script into `Prompts P26–P30`, verify that your **5-Parameter Voice DNA Header** is attached at the top of your system prompt and run the **12-Point Pre-Flight QA Checklist (`Prompt P34`)** during Thursday Block 4 (`9:00–9:30 AM`):

| QA Gate # | Verification Dimension | Exact Quantitative / Editorial Requirement | Pass / Fail |
| :---: | :--- | :--- | :---: |
| **Gate 01** | **Outlier Demand Multiplier ($M_{\text{outlier}}$)** | Confirmed peer video achieved $\ge 2.5\times$ peer channel's 90-day median views within 14 days of upload. | `[ ] PASS` |
| **Gate 02** | **3-Word Thumbnail & Title Pairing** | Thumbnail contains $\le 3$ high-contrast words; Title is `52–68 characters` and complements (never repeats) the thumbnail text. | `[ ] PASS` |
| **Gate 03** | **First 30-Second C.L.I.P. Hold Structure** | Spoken opener (`75–85 words`) confirms the click promise in sentence 1, states loss stakes, flashes visual proof by `0:18`, and opens a loop by `0:30`. | `[ ] PASS` |
| **Gate 04** | **90-Second Retention Pattern Resets** | Every `90-second` block (`~220 words`) contains an explicit visual change, B-roll screen zoom, diagram overlay, or narrative contrast. | `[ ] PASS` |
| **Gate 05** | **Zero-Tolerance Banned AI Vocabulary** | Zero occurrences of generic AI filler words (*unveil, transformative, paradigm, synergy, holistic, seamless*) or throat-clearing intros. | `[ ] PASS` |
| **Gate 06** | **Burstiness & Sentence Rhythm** | Sentence length alternates intentionally between punchy `5–8 word` declarations and detailed `18–26 word` technical explanations. | `[ ] PASS` |
| **Gate 07** | **Concrete Case Study & Math Proof** | Every major claim is anchored by a real operator case study with specific Before/After hours, percentages, or dollar figures. | `[ ] PASS` |
| **Gate 08** | **Mid-Roll Native Bridge Integration** | The 60-second Lead Magnet or Sponsor demonstration occurs naturally inside a tutorial step (`5:30–6:45`) rather than sounding like an ad break. | `[ ] PASS` |
| **Gate 09** | **Sudden-Death Outro Execution** | Final block transitions directly from the last actionable step into the single next-step bridge without telegraphing that the video is ending. | `[ ] PASS` |
| **Gate 10** | **Platform-Native Re-Hooking (A02–A15)** | All 5 Vertical Shorts, 2 LinkedIn posts, 2 X threads/essays, 3 Carousels, and 2 Emails have custom platform-native openers (zero lazy cross-posts). | `[ ] PASS` |
| **Gate 11** | **UTM Link & Opt-In Bridge Verification** | All 15 assets include working, tested UTM links (`utm_content=A01`..`A15`) pointing to the `45%+` conversion landing page or checkout stack. | `[ ] PASS` |
| **Gate 12** | **Mobile Squint Test & Audio Loudness** | Thumbnail, carousel slides, and captions are 100% legible on a phone screen at arm's length; audio peaks at `-3 dB` with `-14 LUFS` integrated loudness. | `[ ] PASS` |
"""


def get_template_06_md() -> str:
    return r"""# 14-Day Digital Product Validate-Before-You-Build Launch Runbook

## 1. Executive Launch Philosophy & The `15-Order` Validation Stage Gate

The single largest Destroyer of solopreneur Revenue Per Production Hour (`RPPH`) is spending 60 to 120 hours building a digital course, software tool, or template bundle in secret—only to launch to crickets. Under Chapter 9 of *The AI Content Creator & Solopreneur Operating System*, you are **prohibited** from building more than `Module 1` (or `10%` of the final deliverable) until the market validates demand with credit cards.

* **The 14-Day Validation Rule:** You publish a transparent **Founding Member Pre-Sale Checkout Page** (`40%` off the future retail price) with a clear delivery date `14 days` out.
* **The Quantitative Go/No-Go Threshold:**
  * **GREEN LIGHT (`>= 15 Paid Pre-Orders` or `>= $1,500 Gross Pre-Sale Revenue`):** Demand is statistically proven. You spend Days 08–14 completing the remaining modules/templates and deliver on schedule.
  * **RED LIGHT (`< 15 Paid Pre-Orders`):** You do **not** waste 90 hours building an unwanted offer. You issue an instant `100%` automated refund to early buyers with a personal thank-you note + free bonus worksheet, and re-test a different pain angle next month.

---

## 2. The 4-Tier Solopreneur Value Ladder & Checkout Stack Math

Before opening your pre-sale cart, define your full 4-Tier Value Ladder and checkout multipliers (`Prompts P41–P43`) so every buyer has an immediate path to higher-value implementation assets:

| Value Ladder Tier | Target Price Range | Core Deliverable Format | Target Conversion Rate | Margin & Operational Role |
| :--- | :---: | :--- | :---: | :--- |
| **Tier 0: Free Utility Lead Magnet** | `$0` (Free Opt-In) | 5-Minute Calculator, 7-Day Audit PDF, or 5-Prompt Starter Sheet | `45% – 58%` Landing Page CVR | Rented-to-Owned Audience Bridge |
| **Tier 1 / 2: Impulse Action Toolkit** | `$24 – $49` | Interactive Workbook Suite, Swipe File Vault, or Notion Template | `3.5% – 6.0%` of New Subscribers | Self-Liquidating Acquisition & Trust Builder |
| **Checkout Order Bump (Checkbox)** | `+$12 – $27` | Copy-Paste Prompt CSV, Quick-Start Loom Video, or Contract Pack | `32% – 45%` of Checkout Buyers | Instant `+$5 to +$11` AOV Lift (`Zero Extra Traffic`) |
| **1-Click Post-Purchase Upsell** | `+$49 – $97` | Complete Flagship OS Bundle, Automation JSONs, or Live Clinic | `14% – 22%` of Initial Buyers | Doubles Net Profit Per Launch Buyer |
| **Tier 3 / 4: Flagship System & Vault** | `$99 – $499` | Complete Multi-Format Operating System, Agency Rights, or Cohort | `1.5% – 3.0%` of Warm List | Primary High-Margin Solopreneur Profit Engine |

### Effective Average Order Value ($\text{AOV}_{\text{effective}}$) Pre-Launch Calculation:
$$\text{AOV}_{\text{effective}} = P_{\text{base}} + (P_{\text{bump}} \times \text{TR}_{\text{bump}}) + (P_{\text{upsell}} \times \text{TR}_{\text{upsell}})$$

* **Example Founding Launch Configuration:**
  * Base Flagship Toolkit Price ($P_{\text{base}}$): **`$49.00`**
  * Checkout Order Bump ($P_{\text{bump}} = \$19.00$ at `38%` take rate): **`+$7.22`**
  * One-Click Post-Purchase Upsell ($P_{\text{upsell}} = \$79.00$ at `16%` take rate): **`+$12.64`**
  * **Projected $\text{AOV}_{\text{effective}}$:** **`$68.86 per customer`** (`+40.5%` revenue lift over base price alone).

---

## 3. Day-by-Day 14-Day Launch Execution Calendar

| Launch Day | Operational Phase | Email Sequence Action (`Prompts P42–P44`) | Omnichannel Social & Pillar Action | Daily Metric Gate to Verify |
| :---: | :--- | :--- | :--- | :--- |
| **Day 01** | **Waitlist & Problem Poll** | Send *2-Question Pain Diagnostic Survey* to email list | Publish Contrarian Problem Thread on LinkedIn & X | `>= 50` survey replies identifying #1 friction |
| **Day 02** | **Offer Spec & Wireframe** | Compile top 3 survey pain points into Checkout Page copy | Post "Behind-the-Scenes Architecture Sketch" Carousel | Lock Title, 5 Modules, Bump & Upsell |
| **Day 03** | **Early-Bird Cart Open** | **Launch Email #1:** *Founding Member Pre-Sale Open (40% Off)* | Publish Pillar Video / Essay teaching Module 1 live | First `5` Founding Orders (`Checkout QA Pass`) |
| **Day 04** | **Mechanism Deep Dive** | **Launch Email #2:** *Why the old method fails + Our 5-step mechanism* | Vertical Short #1 + LinkedIn Breakdown of the core formula | Email Open Rate `>= 45%` · CTR `>= 5.0%` |
| **Day 05** | **48-Hr Fast-Action Bonus** | **Launch Email #3:** *48-Hour Founding Bonus expires tonight* | X Thread + IG/LinkedIn Story showing live order notifications | **VALIDATION GATE: Reach `15+` Pre-Orders** |
| **Day 06** | **Social Proof & Teardown** | Rest day for full list (Segment-only follow-up to clickers) | Publish Vertical Short #2 (Case Study Proof) | Confirm `>= 35%` Order Bump Take Rate |
| **Day 07** | **Mid-Launch Walkthrough** | **Launch Email #4:** *3-Minute Screen-Share Tour of the Toolkit* | Post 3-minute uncut Loom demo on YouTube Community & X | Reply to all buyer & prospect questions |
| **Day 08** | **Batch Fulfill Block 1** | Send automated status update to Founding Buyers | Build Modules 2 & 3 using voice-calibrated prompts | `50%` of product deliverables completed |
| **Day 09** | **Objection Crusher FAQ** | **Launch Email #5:** *Can this work if I have a small audience / little time?* | Publish Carousel #2 answering top 5 buyer objections | Click-to-Checkout CVR `>= 8.5%` |
| **Day 10** | **Batch Fulfill Block 2** | Quiet build day for email list | Complete Modules 4 & 5 + Run 12-Point QA Gate on ZIP | `100%` of product files packaged & verified |
| **Day 11** | **Case Study / ROI Math** | **Launch Email #6:** *How reclaiming 10 hrs/wk pays for this 20x over* | Vertical Short #3 + LinkedIn ROI Calculator breakdown | Cumulative orders `>= 30` |
| **Day 12** | **24-Hour Price Jump Alert** | **Launch Email #7A:** *24 hours left before Founding Price ($49 -> $79) ends* | Pin 24-hour countdown reminder across all social profiles | Surge in high-intent checkout sessions |
| **Day 13** | **Final 6-Hour Cart Close** | **Launch Email #7B (To Clickers Only):** *Final 6 hours at Founding Rate* | Final plain-text reminder on X and LinkedIn | Close Founding Pre-Sale window at 11:59 PM |
| **Day 14** | **V1.0 Delivery & Onboarding** | **Delivery Email:** *Your Complete Toolkit is Live + Quick-Start Survey* | Public celebration post + Switch page to Evergreen `$79` price | `0%` delivery errors · Collect first 5 testimonials |

---

## 4. Post-Launch Conversion & Unit-Economics Audit Scorecard

Complete this table on Day 15 before transitioning the checkout page into your evergreen **5-Day Automated Welcome Sequence (Chapter 8)**:

| Post-Launch Audit Metric | Formula / Calculation | Launch Target Benchmark | Actual Launch Result |
| :--- | :--- | :---: | :--- |
| **1. Total Unique Checkout Page Visitors** | From Gumroad / Stripe Analytics | `>= 400 Visitors` | `[ENTER VISITORS]` |
| **2. Front-End Checkout Conversion Rate** | `Total Base Orders / Unique Checkout Visitors` | `>= 6.5%` (Warm List) | `[ENTER CVR %]` |
| **3. Total Base Units Sold** | Count of Tier 1/2/3 Base Buyers | `>= 15 Orders` (Validation Gate) | `[ENTER ORDERS]` |
| **4. Checkout Order Bump Take Rate** | `Order Bump Buyers / Total Base Buyers` | `>= 35.0%` | `[ENTER BUMP %]` |
| **5. One-Click Upsell Take Rate** | `Upsell Buyers / Total Base Buyers` | `>= 15.0%` | `[ENTER UPSELL %]` |
| **6. Effective Average Order Value ($\text{AOV}_{\text{effective}}$)** | `Total Gross Launch Revenue / Total Base Buyers` | `>= 1.40x Base Price` | `$[ENTER AOV]` |
| **7. Total Production & Launch Hours Invested** | Sum of hours across 14-day sprint | `<= 16.0 Hours Total` | `[ENTER HOURS] hrs` |
| **8. Launch Revenue Per Production Hour (`RPPH`)** | `Net Launch Profit / Total Launch Hours Invested` | **`>= $300.00 / Hour`** | **`$[ENTER RPPH] / hr`** |

---

## 5. The 8-Block High-Converting Checkout Page Wireframe (`Prompt P42`)

Never launch a product with a vague two-sentence Gumroad description. Structure your pre-sale and evergreen checkout page using this exact **8-Block Conversion Architecture**:

1. **Block 1 — Quantified Outcome Headline & Timeframe:** State the exact measurable transformation, who it is for, and the time saved without relying on hype (e.g., *"Install the Complete 4-Hour-Per-Week AI Creator & Solopreneur Operating System in 14 Days"*).
2. **Block 2 — The Mathematical Cost of the Status Quo:** Diagnose why the buyer's current manual approach fails (`35 hours/week` at `$8.11/hr` on the Algorithmic Treadmill) so the price of your toolkit feels trivial compared to the cost of staying stuck.
3. **Block 3 — The 5-Stage Proprietary Mechanism Walkthrough:** Show the visual system diagram (`00-ECOSYSTEM-MASTER-MAP-POSTER.png`) and explain how each stage connects deterministically from Outlier Research to Monetization.
4. **Block 4 — Complete Tangible File & Deliverable Inventory Table:** List every exact file format, page count, word count, spreadsheet tab, and software tool included in the `.zip` bundle with retail value anchors.
5. **Block 5 — Operator Case Studies & Before/After Telemetry Proof:** Display 3 concrete case studies showing verified increases in CTR, email opt-in rate, effective AOV, and weekly RPPH.
6. **Block 6 — "Who This Is For" vs. "Who Should NOT Buy This" Filter:** Explicitly disqualify passive "get-rich-quick" seekers to increase buyer trust among serious practitioners and keep refund rates under `1.5%`.
7. **Block 7 — 30-Day Execution-Based Risk-Reversal Guarantee:** Offer a clear, confident guarantee tied to completing Worksheet 01 and running one 4-hour batch sprint.
8. **Block 8 — Checkout Tier Comparison Matrix & Top 8 Objection FAQs:** Present Tier 1, Tier 2, Tier 3, and Tier 4 side by side with the **Tier 3 Complete Bundle** highlighted as the recommended default choice.
"""


def get_template_07_md() -> str:
    return r"""# 20-Minute Friday Creator CEO Operating Review & RPPH Scorecard

## 1. The Friday 20-Minute Executive Cadence Rule

A solo creator who never audits their unit economics inevitably drifts back onto the 35-hour Algorithmic Treadmill. Every Friday between `2:00 PM and 2:20 PM`, close all editing timelines and social feeds, open this 1-page executive template (alongside Tab 8 of your Excel Command Center or your Notion Hub), and execute the **4-Block, 20-Minute Creator CEO Review**:

* **Minutes 00–05 (5-KPI Stage-Gate Telemetry Check):** Log your trailing 7-day hours, views, opt-ins, and revenue across the 5 stages.
* **Minutes 05–10 (Outlier & Retention Triage):** Inspect the 48-hour CTR and 30-second hold rate of this week's Pillar upload; lock next Monday's $M \ge 2.5\times$ Outlier topic.
* **Minutes 10–15 (Outbound Sponsorship & Renewal Sprint):** Send 5 customized 5-sentence B2B sponsor pitches (`Prompt P47`) and send Day-14 ROI reports (`Prompt P49`) to active partners.
* **Minutes 15–20 (RPPH Margin Check & The 1-Task Pruning Rule):** Calculate weekly RPPH (`Net Income / Weekly Hours`). If total hours exceeded `6.0 hours` (or `25 hours` total business operations), eliminate, automate, or delegate the single lowest-yield manual task before Monday morning.

---

## 2. Minute 00–05: Weekly 5-Stage KPI & RPPH Executive Scorecard

* **Review Week Ending:** `[YYYY-MM-DD]` · **Sprint Number:** `Week [01] of 52`

| Stage Gate & Core Metric | Mathematical Formula | Green-Light Target | This Week's Actual | Status (`G / Y / R`) |
| :--- | :--- | :---: | :---: | :---: |
| **Foundation: Weekly Production Hours** | Sum of Block 1 + Block 2 + Block 3 + Block 4 Hours | `<= 6.0 Hrs / Wk` | `[4.5] hrs` | `[GREEN]` |
| **Foundation: Weekly Operator RPPH** | `Weekly Net Revenue / Total Weekly Production Hours` | `>= $200.00 / Hr` | `$[685.00] / hr` | `[GREEN]` |
| **Stage 1: Next Week Outlier Multiplier ($M$)** | `Peer 14d Views / Peer 90d Median Views` | `>= 2.5x Median` | `[3.8x]` | `[GREEN]` |
| **Stage 2: Pillar Packaging ERI Score** | `CTR (%) × (30s Hold % / 100) × (AVD % / 100)` | `>= 2.30 ERI` | `[2.84]` | `[GREEN]` |
| **Stage 3: 1-to-15 Waterfall Completion** | `Published Native Assets / 15 Target Weekly Assets` | `15 / 15 Assets (100%)` | `[15 / 15]` | `[GREEN]` |
| **Stage 4: Landing Page Opt-In Rate** | `New Email Subscribers / Unique Opt-In Page Views` | `>= 45.0% CVR` | `[49.2%]` | `[GREEN]` |
| **Stage 5: Blended Effective RPM** | `(Weekly Total Revenue / Weekly Cross-Platform Views) × 1,000` | `>= $150.00 RPM` | `$[242.50]` | `[GREEN]` |

---

## 3. Weekly Revenue & Unit-Economics Breakdown Table

| Revenue Stream | Gross Weekly Revenue (`USD`) | Direct Platform / Tool Fees (`USD`) | Net Weekly Profit (`USD`) | Direct Hours Invested | Stream-Specific RPPH (`$/Hr`) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Tier 1 & Tier 2 Digital Workbooks (`$9.99–$24`)** | `$[480.00]` | `$[28.80]` | `$[451.20]` | `0.5 hrs` (Automated) | `$[902.40] / hr` |
| **2. Tier 3 Flagship OS Bundle (`$49` + Bumps)** | `$[1,176.00]` | `$[70.56]` | `$[1,105.44]` | `1.5 hrs` (Pillar/Email) | `$[736.96] / hr` |
| **3. Tier 4 Living Creator Vault MRR/ARR (`$49/yr`)** | `$[392.00]` | `$[23.52]` | `$[368.48]` | `0.5 hrs` (Monthly Drop) | `$[736.96] / hr` |
| **4. Outcome B2B Sponsorship Packages** | `$[1,600.00]` | `$[0.00]` | `$[1,600.00]` | `1.0 hrs` (Integration) | `$[1,600.00] / hr` |
| **5. Platform AdSense & High-Ticket Affiliates** | `$[285.00]` | `$[0.00]` | `$[285.00]` | `1.0 hrs` (Shorts/Social) | `$[285.00] / hr` |
| **TOTAL WEEKLY CONSOLIDATED P&L** | **`$[3,933.00]`** | **`$[122.88]`** | **`$[3,810.12]`** | **`4.5 Hours`** | **`$[846.69] / Hr`** |

---

## 4. Minute 10–15: Friday Outbound B2B Sponsorship Pitch Log (`5 Pitches / Friday`)

Never rely on inbound sponsor inquiries alone. Log five 5-sentence outbound pitches (`Prompt P47`) every Friday:

| # | Target Brand & Product | Decision-Maker Contact | Fitted Upcoming Outlier Topic | Proposed Package & Rate | Pitch Status / Next Follow-Up |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | `[Brand Name #1]` | `[Name, Head of Growth]` | `[Week 01 Topic]` | `Tier B ($3,200)` | `Sent [Date] · Follow up [Date+5]` |
| **2** | `[Brand Name #2]` | `[Name, VP Marketing]` | `[Week 01 Topic]` | `Tier B ($3,200)` | `Sent [Date] · Follow up [Date+5]` |
| **3** | `[Brand Name #3]` | `[Name, Partnerships]` | `[Week 02 Topic]` | `Tier C ($8,400 Qtr)` | `Discovery Call Booked` |
| **4** | `[Brand Name #4]` | `[Name, Founder]` | `[Week 02 Topic]` | `Tier A ($1,850)` | `Contract & 50% Deposit Sent` |
| **5** | `[Active Sponsor Renewal]` | `[Name, Brand Manager]` | `Day-14 ROI Report Sent` | `Quarterly Renewal ($8,400)` | `Renewal Approved` |

---

## 5. Minute 15–20: Time-Leak Pruning & Next Week's 4-Hour Batch Sprint Lock

1. **Single Biggest Time-Leak Identified This Week:** `[e.g., Spent 55 minutes manually adjusting caption timing on vertical Shorts #3 and #4.]`
2. **Deterministic Elimination / Automation Action Before Monday:** `[e.g., Apply Prompt P32 rough-cut timestamp template and hand off vertical captioning to editor SOP at $25/hr.]`
3. **Next Week's Locked 4-Hour Batch Sprint Calendar:**
   * **Monday Block 1 (`9:00–10:00 AM` — `60m`):** Finalize S.I.G.N.A.L. Outlier Topic `[TOPIC TITLE]` (`M = [3.8x]`) + Lock 3-Word Thumbnail & C.L.I.P. Hook.
   * **Tuesday Block 2 (`9:00–10:30 AM` — `90m`):** Draft 2,000-word H.E.A.R.T. Pillar Script (`Prompts P22–P25`) + Extract 14 Derivative Assets (`Prompts P26–P30`).
   * **Wednesday Block 3 (`9:00–10:00 AM` — `60m`):** Record Teleprompter A-Roll Pillar Video + 60-Second Sponsor Demo in one continuous session.
   * **Thursday Block 4 (`9:00–9:30 AM` — `30m`):** Run 12-Point Pre-Flight QA Checklist (`Prompt P34`) & Schedule All 15 Omnichannel Assets.

---

## 6. Stage-Gate Troubleshooting Matrix & The `RPPH >= $150/Hr` Delegation Protocol

Whenever a weekly KPI on your Friday Scorecard drops into **Yellow** or **Red**, apply the corresponding deterministic fix below during next week's sprint—never guess which lever to pull:

| Broken Stage Gate Symptom | Root-Cause Diagnostic | Mandatory 7-Day Corrective Action |
| :--- | :--- | :--- |
| **1. Pillar Video CTR `< 5.5%` at 24 Hours** | Packaging failure: Title/Thumbnail pair lacks contrast or repeats the same words. | Swap immediately to pre-rendered **Backup Title/Thumbnail Variant B** (`Prompt P17/P18`); verify 3-word mobile legibility. |
| **2. First 30-Second Hold Rate `< 65%`** | C.L.I.P. opener failure: Slow intro, throat-clearing, or delayed visual proof. | Cut the first 10 seconds of preamble; open sentence 1 with the exact title promise and show the finished dashboard by `0:15`. |
| **3. Mid-Video Average View Duration `< 45%`** | Narrative drag in Block 3: Explaining >2 minutes without a visual pattern reset. | Insert a **90-second visual reset** (`[RESET]`: B-roll zoom, diagram callout, or case-study number) every `220 spoken words`. |
| **4. Landing Page Opt-In Rate `< 35%`** | High-friction page or vague lead magnet ("Join my newsletter"). | Strip top navigation links; replace generic signup with a **5-Minute Utility Calculator or Audit Sheet** (`Prompt P36/P37`). |
| **5. Welcome Sequence Tripwire CVR `< 2.5%`** | Weak bridge between free lead magnet and paid Tier 1/2 toolkit. | Rewrite Emails 3, 4, and 5 (`Prompt P38`) to quantify the exact hours saved by upgrading to the complete editable template kit. |
| **6. Blended Effective RPM `< $100.00`** | Over-reliance on AdSense or underpriced CPM sponsorships. | Enforce the **5-Pitch Friday Rule** (`Prompt P47`) and attach a Checkout Order Bump (`+$19`) + 1-Click Upsell (`+$79`) to every offer. |

### The Quantitative Editor & VA Delegation Gate (`When Operator RPPH >= $150/Hr`):
Once your 4-week rolling **Operator RPPH exceeds `$150.00/hour`**, you are losing money every time you perform a `$25/hour` mechanical post-production task yourself. Delegate strictly in this order while keeping **100% ownership of Outlier Selection, Voice DNA Scripting, and On-Camera Delivery**:
1. **Delegation Step 1 (Video Rough-Cut & Vertical Captioning — Saves `90 Mins/Wk`):** Hand off raw Wednesday A-roll + `Prompt P32` Edit Sheet to a freelance editor at a flat `$60–$100/sprint` rate.
2. **Delegation Step 2 (Omnichannel Scheduling & UTM QA — Saves `30 Mins/Wk`):** Hand off Thursday Block 4 scheduling and link verification using the **12-Point Pre-Flight QA Checklist (`Prompt P34`)**.
3. **Delegation Step 3 (Customer Support & Sponsor Invoicing — Saves `45 Mins/Wk`):** Automate via **JSON Blueprint `#04`** and templated FAQ macros so your total weekly work commitment never exceeds the **25-Hour Solopreneur Ceiling**.

---

## 7. Quarterly 90-Day Creator CEO Strategic Audit & Annual Operating Trajectory

At the end of **Week 13, Week 26, Week 39, and Week 52**, extend your Friday CEO Review by 25 minutes to complete this **90-Day Quarterly Strategic Audit** before locking next quarter's product launch and sponsorship rate card adjustments:

| Quarterly Review Dimension | Q1 Baseline Benchmark | Q2 Expansion Target | Q3 Compounding Target | Q4 Maturity Benchmark | This Quarter Actual |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Weekly Batch Production Hours** | `4.5 Hrs / Wk` | `4.0 Hrs / Wk` | `3.5 Hrs / Wk` (Editor) | `3.0 Hrs / Wk` (Automated) | `[ENTER HRS]` |
| **2. Rolling 90-Day Operator RPPH** | `$180 – $250 / Hr` | `$300 – $450 / Hr` | `$450 – $650 / Hr` | `$650 – $1,000+ / Hr` | `$[ENTER RPPH]` |
| **3. Active Owned Email Subscribers** | `1,000 – 2,500 Subs` | `2,500 – 6,000 Subs` | `6,000 – 12,500 Subs` | `12,500 – 25,000+ Subs` | `[ENTER SUBS]` |
| **4. 90-Day Email Subscriber LTV** | `$4.50 / Sub` | `$6.20 / Sub` | `$8.40 / Sub` | `$11.50+ / Sub` | `$[ENTER LTV]` |
| **5. Tier B B2B Sponsorship Rate Card** | `$1,850 / Sprint` | `$2,500 / Sprint` | `$3,200 / Sprint` | `$4,500+ / Sprint` | `$[ENTER RATE]` |
| **6. Tier 4 Recurring Vault Members** | `25 Founding Members` | `75 Active Members` | `160 Active Members` | `300+ Active Members` | `[ENTER MEMBERS]` |
| **7. Consolidated Quarterly Net Profit** | `$12,000 – $18,000` | `$24,000 – $36,000` | `$42,000 – $65,000` | `$75,000 – $120,000+` | `$[ENTER PROFIT]` |

### Quarterly Rate-Card & Price-Escalation Rules:
* **Rule 1 — The 20% Sponsorship Rate Escalator:** Whenever your rolling 90-day Pillar video views and active email subscriber count grow by `25%`, increase your **Base Placement Rate** in Tab 07 of your Excel Command Center by **`20%`** for all new incoming brand partners while grandfathering existing quarterly Tier C partners for one renewal cycle.
* **Rule 2 — The Evergreen Checkout Price Step-Up:** Every time you add a major new implementation module, visual cheat sheet, or automation blueprint to your **Tier 3 Flagship Operating System Bundle**, run a 72-hour notification campaign to your warm email list allowing subscribers to lock in the current price before stepping the evergreen retail price up by `$10` to `$20`.
* **Rule 3 — The 90-Day Cold Subscriber Sunset Purge:** On the final Friday of each quarter, run your ESP's **90-Day Cold Subscriber Re-Engagement Sequence (`Prompt P40`)** and permanently remove any subscriber who has opened zero emails in 90 days and failed to click the 2-email confirmation link. Protecting a `48%+` open rate is worth far more than hoarding unengaged vanity email addresses.
"""


# ---------------------------------------------------------------------------
# UPGRADE 3: BUILD 3 WIDESCREEN 16:9 EDITABLE POWERPOINT (.PPTX) SLIDE DECKS
# ---------------------------------------------------------------------------

def add_pptx_slide_shell(prs: Presentation, deck_label: str, slide_num: int, total_slides: int, title: str, subtitle: str, speaker_note: str):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # Dark Navy Header Bar
    hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, PptxInches(0), PptxInches(0), PptxInches(13.333), PptxInches(1.25))
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = PptxRGB(0x0F, 0x17, 0x2A)
    hdr.line.fill.background()

    # Indigo Accent Stripe under header
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, PptxInches(0), PptxInches(1.25), PptxInches(13.333), PptxInches(0.06))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = PptxRGB(0x4F, 0x46, 0xE5)
    stripe.line.fill.background()

    # Header Text
    tb = slide.shapes.add_textbox(PptxInches(0.5), PptxInches(0.12), PptxInches(10.5), PptxInches(1.05))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = f"{deck_label}  ·  SLIDE {slide_num:02d} OF {total_slides:02d}"
    p0.font.size = PptxPt(10)
    p0.font.bold = True
    p0.font.color.rgb = PptxRGB(0x2D, 0xD4, 0xBF)

    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.size = PptxPt(22)
    p1.font.bold = True
    p1.font.color.rgb = PptxRGB(0xFF, 0xFF, 0xFF)

    p2 = tf.add_paragraph()
    p2.text = subtitle
    p2.font.size = PptxPt(11.5)
    p2.font.color.rgb = PptxRGB(0xCB, 0xD5, 0xE1)

    # Footer Bar
    ftr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, PptxInches(0), PptxInches(7.12), PptxInches(13.333), PptxInches(0.38))
    ftr.fill.solid()
    ftr.fill.fore_color.rgb = PptxRGB(0x0F, 0x17, 0x2A)
    ftr.line.fill.background()

    ftb = slide.shapes.add_textbox(PptxInches(0.5), PptxInches(7.15), PptxInches(12.333), PptxInches(0.3))
    ftf = ftb.text_frame
    fp = ftf.paragraphs[0]
    fp.text = f"The AI Content Creator & Solopreneur Operating System  |  Apex Digital Systems Studio  |  Page {slide_num}/{total_slides}"
    fp.font.size = PptxPt(9.5)
    fp.font.color.rgb = PptxRGB(0x94, 0xA3, 0xB8)

    # Speaker notes
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = speaker_note

    return slide


def populate_slide_cards_and_table(slide, kpis: list[tuple[str, str, str]], cards: list[tuple[str, list[str]]], bottom_banner: str):
    # Top 3 KPI callout boxes
    for idx, (k_lbl, k_val, k_sub) in enumerate(kpis[:3]):
        left = PptxInches(0.5 + idx * 4.18)
        top = PptxInches(1.48)
        w = PptxInches(3.98)
        h = PptxInches(1.28)
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
        box.fill.solid()
        box.fill.fore_color.rgb = PptxRGB(0xF8, 0xFA, 0xFC)
        box.line.color.rgb = PptxRGB(0x4F, 0x46, 0xE5) if idx == 0 else (PptxRGB(0x0D, 0x94, 0x88) if idx == 1 else PptxRGB(0xD9, 0x77, 0x06))
        box.line.width = PptxPt(1.75)

        tf = box.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = k_lbl.upper()
        p0.font.size = PptxPt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = PptxRGB(0x64, 0x74, 0x8B)

        p1 = tf.add_paragraph()
        p1.text = k_val
        p1.font.size = PptxPt(20)
        p1.font.bold = True
        p1.font.color.rgb = PptxRGB(0x0F, 0x17, 0x2A)

        p2 = tf.add_paragraph()
        p2.text = k_sub
        p2.font.size = PptxPt(9.5)
        p2.font.color.rgb = PptxRGB(0x0D, 0x94, 0x88)

    # Middle 2 Structured Content Cards
    for c_idx, (c_title, c_bullets) in enumerate(cards[:2]):
        left = PptxInches(0.5 + c_idx * 6.28)
        top = PptxInches(2.92)
        w = PptxInches(6.05)
        h = PptxInches(3.25)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = PptxRGB(0xFF, 0xFF, 0xFF)
        card.line.color.rgb = PptxRGB(0xCB, 0xD5, 0xE1)
        card.line.width = PptxPt(1.25)

        tf = card.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = c_title
        pt.font.size = PptxPt(13.5)
        pt.font.bold = True
        pt.font.color.rgb = PptxRGB(0x4F, 0x46, 0xE5) if c_idx == 0 else PptxRGB(0x0D, 0x94, 0x88)

        for b in c_bullets:
            pb = tf.add_paragraph()
            pb.text = f"▸  {b}"
            pb.font.size = PptxPt(11)
            pb.font.color.rgb = PptxRGB(0x1E, 0x29, 0x3B)

    # Bottom Takeaway / Action Strip
    b_strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PptxInches(0.5), PptxInches(6.32), PptxInches(12.333), PptxInches(0.65))
    b_strip.fill.solid()
    b_strip.fill.fore_color.rgb = PptxRGB(0x0F, 0x17, 0x2A)
    b_strip.line.color.rgb = PptxRGB(0x0D, 0x94, 0x88)
    b_strip.line.width = PptxPt(1.5)
    btf = b_strip.text_frame
    btf.word_wrap = True
    bp = btf.paragraphs[0]
    bp.text = f"OPERATOR STAGE GATE & ACTION:  {bottom_banner}"
    bp.font.size = PptxPt(11)
    bp.font.bold = True
    bp.font.color.rgb = PptxRGB(0x2D, 0xD4, 0xBF)


def build_all_three_pptx_decks() -> list[tuple[Path, int]]:
    PPTX_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    # Deck 1: 01-Brand-Sponsorship-and-Partnership-Pitch-Deck.pptx (12 slides)
    deck1_slides = [
        (
            "Creator Authority & Omnichannel Brand Partnership Pitch Deck",
            "Outcome-Based B2B & Prosumer Sponsorship Architecture (Chapters 9–10)",
            [("Combined Reach", "28,500+ Subs", "High-Intent Practitioners"), ("Email Open Rate", "49.4% Verified", "7.2% Unique Link CTR"), ("30s Hook Hold", "73.8% Retention", "54.6% Pillar AVD")],
            [
                ("Why High-Intent Creator Partnerships Win", ["Our audience consists of founders, operators, and technical buyers actively evaluating software tools.", "Every weekly tutorial demonstrates real workflows live on screen rather than reading passive ad scripts.", "Evergreen search indexing drives compounding trial signups for 12 to 24 months after publication."]),
                ("Partnership Overview & Core Deliverables", ["Integrated YouTube Long-Form Pillar demonstrations (60–90s mid-roll workflow segment).", "Dual top-of-fold placements inside our owned operator email newsletter.", "Native LinkedIn & X authority breakdowns plus optional 30–90 day paid-ad whitelisting rights."]),
            ],
            "Position every brand conversation around measurable business outcomes, trial signups, and multi-touch trust rather than commodity CPM impressions.",
        ),
        (
            "Audience Profile & High-Intent Decision-Maker Demographics",
            "Who Consumes Our Weekly Pillar Tutorials & Operator Newsletters",
            [("Founders & Execs", "38% of Audience", "Direct Budget Authority"), ("Ops & Product Leads", "29% of Audience", "Tool Stack Architects"), ("Annual SaaS Spend", "$2.5K – $25K+/yr", "74% Influence Software Spend")],
            [
                ("Demographic & Firmographic Breakdown", ["38% Solo Founders, Agency Owners & Managing Directors.", "29% Senior Operations, Engineering, RevOps & Product Managers.", "21% Independent Technical Consultants & Creator-Operators.", "Geographic Split: 52% US/Canada, 26% UK/EU, 14% APAC, 8% Global."]),
                ("Psychographic Buying Triggers", ["Actively replacing manual 30-hour workflows with automated software and AI systems.", "Purchase decisions driven by verified hours saved, API/workflow reliability, and ROI math.", "High affinity for B2B SaaS, AI productivity tools, fintech, cloud infrastructure, and analytics."]),
            ],
            "Highlight that 74% of readers control or influence software budgets—making each view worth 8x to 12x a general entertainment impression.",
        ),
        (
            "Why Standard CPM Impressions Fail vs. High-Trust Creator Integration",
            "Eliminating the 65% Ad-Skip Cliff Through Native Workflow Demonstrations",
            [("Legacy Ad Skip Rate", "65%+ Viewers Skip", "Generic 30s Press Releases"), ("Native Demo Hold", "91% Segment Hold", "Embedded Inside Tutorial Step"), ("Trial Conversion Lift", "4.4x Higher CVR", "Multi-Touch Omnichannel Stack")],
            [
                ("The Legacy $25 CPM Sponsorship Failure Mode", ["Viewers immediately recognize and skip disconnected, scripted voiceover reads.", "Single-touch video mentions fail to capture users who are commuting or watching on mobile.", "Zero follow-up in email or text feeds means 95% of interested viewers forget to sign up."]),
                ("Our Native Problem-Solution Integration Method", ["Your tool is introduced as the concrete solution to Step 2 of the tutorial problem.", "Viewers watch a real 60-second screen-share demonstration producing a tangible output.", "Identical UTM link is reinforced 48 hours later in our Tuesday and Friday email issues."]),
            ],
            "Use Script S01 whenever a brand asks for your CPM rate: reframe the conversation around cost per qualified software trial.",
        ),
        (
            "Cross-Platform Reach & Retention Telemetry",
            "Verified 90-Day Engagement Across YouTube, Email Newsletter & LinkedIn/X",
            [("Pillar Video CTR", "8.4% Avg CTR", "Outlier M >= 2.5x Validated"), ("Newsletter CTR", "7.2% Unique Clicks", "11,400+ Active Subscribers"), ("Omnichannel Reach", "145,000+ / Mo", "Across 15 Weekly Native Assets")],
            [
                ("Long-Form Video & Search Compounding", ["Average first-14-day views: 16,400+ per Pillar Tutorial.", "Long-tail YouTube & Google search traffic adds +45% to +65% additional views over Days 15–90.", "73.8% 30-second C.L.I.P. hook retention ensures your mid-roll placement reaches deep-focus viewers."]),
                ("Owned Newsletter & B2B Social Amplification", ["11,400+ double-opt-in email subscribers with 49.4% open rate.", "Strict 60-day cold-subscriber pruning guarantees high inbox placement.", "LinkedIn long-form posts and 8-slide PDF carousels reach desktop B2B buyers during work hours."]),
            ],
            "Share verified trailing-90-day screenshots from YouTube Studio and your ESP to establish immediate quantitative credibility.",
        ),
        (
            "Audience-Offer Alignment & High-Converting Product Categories",
            "Where Sponsor Products Fit Inside the 5-Stage Operator Workflow",
            [("Category Fit Score", "NMPI >= 85/100", "Direct Workflow Utility"), ("Avg Link Clicks", "650 – 1,250 / Sprint", "Verified UTM Tracking"), ("Free-to-Paid Trial", "18% – 26% Conv.", "High-Intent Self-Serve Onboarding")],
            [
                ("Top-Performing Partner Categories", ["AI Writing, Coding, Audio/Video & Workflow Automation Platforms.", "No-Code Databases, CRM, Project Management & Knowledge Systems.", "Solopreneur Banking, Tax/Invoicing, Checkout & Email Marketing Infrastructure."]),
                ("Pre-Integration Fit Verification Gate", ["We only accept sponsors whose products we can genuinely demonstrate on screen.", "Every campaign includes a custom use-case angle matched to our validated Outlier Backlog.", "Guarantees authentic enthusiasm and protects long-term audience conversion trust."]),
            ],
            "Disqualifying low-fit consumer sponsors increases your authority with high-LTV B2B software brands.",
        ),
        (
            "Native Integration Format #1 — Deep-Dive Mid-Roll Walkthrough",
            "60–90 Second Screen-Share Demonstration Positioned at Peak Retention (Minute 04:30)",
            [("Placement Window", "04:15 – 05:45", "Right After Block 1 Problem Setup"), ("Visual Format", "Live Screen Demo", "+ Custom Architecture Overlay"), ("CTA Placement", "Pinned + Top Line", "+ Verbal Companion Kit Bridge")],
            [
                ("4-Part Mid-Roll Storyboard Structure", ["0:00–0:15: Connect the tutorial bottleneck directly to the friction your tool eliminates.", "0:15–0:50: Show 3 concrete clicks inside your software producing a live result on screen.", "0:50–1:15: Quantify the time or money saved and direct viewers to the top description link."]),
                ("Permanent Evergreen Asset Value", ["Your workflow segment is permanently baked into the master tutorial video.", "Chapter markers and pinned comment links remain active for a minimum of 12 months.", "Included inside our downloadable chapter worksheet so readers click straight from the PDF."]),
            ],
            "Walk sponsors through this exact 4-part storyboard so they see why a 60s native demo outperforms a 60s talking-head ad read.",
        ),
        (
            "Native Integration Format #2 — Newsletter & Visual Carousel Integration",
            "Capturing Desktop Decision-Makers With High-CTR Written & Visual Placements",
            [("Primary Top Box", "150 Words + Logo", "Above the Fold in Tuesday Issue"), ("Friday Spotlight", "100 Words + CTA", "Reinforcement in Offer Issue"), ("LinkedIn Carousel", "8-Slide PDF Deck", "Dedicated Tool Slide + First Comment")],
            [
                ("Dual Email Newsletter Placement Architecture", ["Tuesday Value Issue: Top-of-fold Sponsor Callout Box with headline, 3 outcome bullets, and button.", "Friday Operator Issue: Mid-issue reminder highlighting your free trial or exclusive partner bonus.", "Reaches readers in their inbox with 1-click desktop access to your signup page."]),
                ("LinkedIn & X Native Social Amplification", ["1x Long-Form LinkedIn Breakdown + 1x 8-Slide PDF Carousel featuring your workflow.", "1x 8-Post X Thread with your tracked trial link in the summary post.", "Captures B2B decision-makers who prefer written step-by-step guides over video."]),
            ],
            "Bundling email + LinkedIn with YouTube justifies a 2.2x higher package fee while costing you only 15 minutes of extra formatting.",
        ),
        (
            "Verified Sponsor Case Study Proof (Clicks, Trials & Attribution)",
            "Empirical Campaign Results From Recent B2B & Prosumer Partnerships",
            [("Case A: B2B SaaS", "1,140 UTM Clicks", "312 Trials / $28.4K ARR"), ("Case B: AI Tool", "3,480 UTM Clicks", "890+ Signups Across 3 Sprints"), ("Case C: FinTech", "790 UTM Clicks", "164 Funded Business Accounts")],
            [
                ("Why Our Multi-Touch Campaigns Convert", ["Viewers see the tool working in the YouTube tutorial on Tuesday morning.", "Readers click the UTM link inside the Tuesday afternoon newsletter while at their desk.", "Whitelisted 60-second cutdowns retarget warm viewers across LinkedIn and Meta for 30–90 days."]),
                ("Transparent Day-14 Proof-of-Performance Reporting", ["Every sponsor receives a structured Day-14 ROI Telemetry Report (Prompt P49).", "Includes verified 14-day views, mid-roll retention graph, newsletter opens, and unique UTM clicks.", "Drives our 70%+ multi-sprint partner renewal rate."]),
            ],
            "Always deliver the Day-14 Proof-of-Performance report automatically—it is the #1 driver of quarterly retainer renewals.",
        ),
        (
            "The 3-Tier Omnichannel Outcome Sponsorship Packages",
            "Turnkey Pricing & Deliverable Matrix Engineered for Predictable Partner ROI",
            [("Tier A: Single Sprint", "$1,850 USD", "1 Pillar Video + 1 Newsletter"), ("Tier B: Conversion Bundle", "$3,200 USD", "Pillar + 2 Emails + Social + 30d Ad Rights"), ("Tier C: Quarterly Partner", "$8,400 USD", "3 Monthly Sprints + 90d Exclusivity (Save 15%)")],
            [
                ("Tier A ($1,850) vs. Tier B ($3,200 — Most Popular)", ["Tier A is ideal for initial single-sprint pilot validation (1 Pillar Video + 1 Newsletter).", "Tier B adds a second newsletter issue, LinkedIn/X posts, Featured Resource Vault placement, and 30 days of Paid-Ad Whitelisting rights.", "Over 75% of partners select Tier B or Tier C for multi-touch conversion lift."]),
                ("Tier C: Quarterly Category Partner ($8,400 — 3 Sprints)", ["Locks 3 consecutive monthly omnichannel sprints at a 15% multi-sprint discount.", "Includes 90 days of full Paid-Ad Whitelisting rights and 90-day direct competitor exclusivity.", "Establishes your brand as the default category recommendation for our audience."]),
            ],
            "Present all three tiers side-by-side so Tier B ($3,200) and Tier C ($8,400) anchor the value conversation.",
        ),
        (
            "Paid-Ad Whitelisting, Usage Rights (30%/Mo) & Exclusivity Options",
            "How Brands Scale Our High-Trust Workflow Demo Across Paid Acquisition Channels",
            [("Whitelisting Rate", "+30% / 30 Days", "Of Base Package Placement Fee"), ("Creator Cutdown", "60s Vertical + 16:9", "Ready for Meta, YouTube & LinkedIn Ads"), ("Category Lock", "30 to 90 Days", "Zero Direct Competitor Mentions")],
            [
                ("High-ROAS Paid Social Cutdowns & Spark Ads", ["Studio-recorded agency ads suffer from ad fatigue; creator workflow demos convert 2.5x–3.2x higher.", "We deliver a clean 60-second 16:9 and 9:16 cutdown of the integration segment.", "Your team can run the clip on Meta, LinkedIn, YouTube, or embed it on your landing page."]),
                ("Clear Intellectual Property & AI Protection Terms", ["Usage rights are licensed in clean 30-, 60-, or 90-day increments (+30% of base rate/month).", "Category exclusivity locks out up to 3 named direct competitors during the active window.", "Contract strictly prohibits feeding creator voice or likeness into generative AI training models."]),
            ],
            "Never give away perpetual usage rights for free. A 60-day whitelisting license adds +60% pure-margin revenue to every deal.",
        ),
        (
            "14-Day Production, Factual Review & Publishing Timeline",
            "Zero-Friction Async Onboarding From Brief Approval to Live Omnichannel Launch",
            [("Day 01 – 03", "Contract & Brief", "50% Deposit + 3 Talking Points"), ("Day 07 – 10", "Storyboard & Shoot", "1-Round Factual Check (48h SLA)"), ("Day 14 & Day 28", "Launch & ROI Report", "Live Links + Day-14 Telemetry")],
            [
                ("Days 01–07: Alignment & Storyboard Lock", ["Day 01: Sign 2-page Creator-Protection Agreement & remit 50% calendar reservation deposit.", "Day 03: Partner shares product access, target UTM link, and 3 factual talking points.", "Day 07: We deliver the 60s integration storyboard for a single consolidated factual check."]),
                ("Days 10–28: Batch Execution, Launch & ROI Audit", ["Day 10–12: Segment recorded during Wednesday Block 3 and verified via 12-Point QA Gate.", "Day 14: Pillar video, newsletter issues, and LinkedIn/X posts go live; balance invoiced Net-15.", "Day 28: Delivery of Day-14 Proof-of-Performance ROI Report and quarterly renewal option."]),
            ],
            "Clear timelines and a strict 1-round factual revision cap protect your 4-hour weekly batch production schedule.",
        ),
        (
            "Next Steps & Partnership Onboarding Contact Card",
            "Reserve Your Upcoming Sprint Slot in Under 10 Minutes",
            [("Available Slots", "2 Sprints / Month", "Limited Inventory for High Focus"), ("Reservation Lock", "50% Deposit", "Net-15 Balance Upon Publication"), ("Fast Onboarding", "48-Hour Setup", "Direct Founder-to-Partner Comms")],
            [
                ("How to Lock Your Target Publication Week", ["Step 1: Reply with your preferred package tier (Tier A, Tier B, or Tier C Quarterly).", "Step 2: Confirm your target publication month and primary conversion URL.", "Step 3: We issue the 2-page agreement and invoice so your slot is locked today."]),
                ("Direct Studio Partnership Contact", ["Publisher / Imprint: Apex Digital Systems Studio", "Primary Channel & Newsletter: [INSERT YOUR CHANNEL / SUBSTACK URL]", "Partnership Desk Email: [INSERT YOUR PARTNERSHIP EMAIL ADDRESS]"]),
            ],
            "Close every pitch deck with a clear 3-step onboarding action and scarcity around your 2 monthly sponsor slots.",
        ),
    ]

    p_deck1 = PPTX_DIR / "01-Brand-Sponsorship-and-Partnership-Pitch-Deck.pptx"
    build_single_pptx_deck(p_deck1, "DECK 01 · SPONSORSHIP PITCH DECK", deck1_slides)
    results.append((p_deck1, len(deck1_slides)))

    # Deck 2: 02-Educational-Masterclass-and-Webinar-Deck-Template.pptx (10 slides)
    deck2_slides = [
        (
            "The 5-Stage Content-to-Cash Operating System Masterclass",
            "How Solo Creators Build $15K–$25K/Mo Media & Product Engines in Under 6 Hours/Week",
            [("Target RPPH Floor", "$150 – $250+/Hr", "Up From $8.75/Hr Baseline"), ("Weekly Sprint Cap", "<= 4.0 Hours/Wk", "Mon–Thu Batch Architecture"), ("Omnichannel Yield", "1 Pillar -> 15 Assets", "+ 4-Tier Product Value Ladder")],
            [
                ("Who This Masterclass Is Engineered For", ["Content creators, technical educators, consultants, and solo founders tired of 35-hour workweeks.", "Operators with 1,000 to 50,000 subscribers who want predictable product and sponsor revenue.", "Builders who prefer quantitative equations, templates, and stage gates over vague motivation."]),
                ("What You Will Install in the Next 45 Minutes", ["The exact RPPH Audit formula to identify and prune your top 3 weekly time-leaks.", "The S.I.G.N.A.L. Outlier Multiplier (M >= 2.5x) and C.L.I.P. 30-second hook architecture.", "The 1-to-15 Waterfall, 45%+ Opt-In Bridge, and 14-Day Validate-Before-You-Build Launch Engine."]),
            ],
            "Open the masterclass by contrasting the 35-hour Algorithmic Treadmill with the 4-hour Operator Sprint.",
        ),
        (
            "Workshop Agenda & Measurable Operator Outcomes",
            "Five Deterministic Stage Gates From Idea Validation to High-Margin Monetization",
            [("Part 1 (Min 00–12)", "Diagnosis & Niche", "RPPH Audit + NMPI >= 75/100"), ("Part 2 (Min 12–28)", "Outliers & Waterfall", "M >= 2.5x + 1-to-15 Engine"), ("Part 3 (Min 28–45)", "Funnel & Revenue", "45% Opt-In + 4-Tier Ladder")],
            [
                ("Core Mathematical Formulas Covered Today", ["Formula 1: Revenue Per Production Hour (RPPH) & Opportunity Cost of Time Leaks.", "Formula 2: Niche Monetization Potential Index (NMPI) & S.I.G.N.A.L. Outlier Multiplier (M).", "Formula 3: Effective Retention Index (ERI), 90-Day Subscriber Value (V_sub) & Checkout AOV."]),
                ("Your Workshop Action Rule", ["Do not passively watch—open Worksheet 01 or the Offline Web Companion App alongside these slides.", "Calculate your baseline RPPH during Slide 3.", "Pick your single highest-priority stage gate bottleneck before the Q&A."]),
            ],
            "Have attendees open their fillable workbook or offline web app right at Slide 2 to drive active participation.",
        ),
        (
            "The Real-World Friction Point — Why 84% of Creators Burn Out",
            "Empirical Audit of 400+ Independent Creators Working 32+ Hours/Week for Under $9/Hr",
            [("Avg Weekly Hours", "32.4 Hours/Wk", "140+ Hours/Mo Unsystematized"), ("Median Monthly Net", "$1,180 / Month", "AdSense + Sporadic Affiliates"), ("Actual Hourly Yield", "$8.42 / Hour RPPH", "Below Minimum Wage After Costs")],
            [
                ("Anatomy of a 38-Hour Burnout Week (Marcus's Before State)", ["Monday (6.5h): Scrolling social feeds guessing an unvalidated video topic from scratch.", "Tuesday (9.0h): Staring at a blank doc rewriting a script without a Voice DNA profile.", "Wednesday–Friday (23.0h): Endless retakes, manual editing, and retyping posts across platforms."]),
                ("Why Working Harder Makes the Treadmill Worse", ["Doubling upload frequency on unvalidated topics simply doubles your editing burnout.", "Relying on $5 AdSense RPM requires 2,000,000 monthly views just to make $10,000/month.", "Without an owned email bridge and product ladder, 99% of your audience value leaks away."]),
            ],
            "Walk through Marcus Vance's 38.5-hour / $7.86 RPPH baseline so attendees recognize their own calendar leaks.",
        ),
        (
            "The 3 Structural Traps Draining Your Time & Revenue",
            "Isolating the Unvalidated Ideation Tax, Format Rewrite Tax & Rented-Attention Leak",
            [("Trap #1: Ideation Tax", "62% Flop Rate", "Filming Unvalidated Topics"), ("Trap #2: Rewrite Tax", "14 Hrs/Wk Lost", "Manual Cross-Posting"), ("Trap #3: Funnel Leak", "$0.01 / Viewer", "No Owned Email or Product Bridge")],
            [
                ("Trap #1 & Trap #2: Production Inefficiency", ["Trap #1 (Unvalidated Ideation): Spending 15 hours producing a topic with zero peer outlier proof.", "Trap #2 (Format Rewrite Tax): Treating YouTube, LinkedIn, X, Shorts, and Email as five separate writing jobs instead of one 1-to-15 Waterfall."]),
                ("Trap #3: The Rented-Attention Monetization Leak", ["Sending 100% of viewers back into the social algorithm instead of capturing 45%+ on an opt-in page.", "Pitching low-margin $20 CPM ad reads instead of $2,500+ outcome packages and a $49–$199 digital toolkit."]),
            ],
            "Every module in the Creator OS is engineered specifically to eliminate one of these three structural traps.",
        ),
        (
            "Core System Overview — The 5-Stage Content-to-Cash Engine",
            "How Sequential Stage Gates Turn 4 Weekly Batch Hours Into Compounding Revenue",
            [("Stages 1 & 2", "Validate & Package", "NMPI >= 75 | Outlier M >= 2.5x"), ("Stage 3", "Script & Multiply", "Voice DNA + 1-to-15 Waterfall"), ("Stages 4 & 5", "Convert & Monetize", "45% Opt-In + 4-Tier Ladder")],
            [
                ("Strict Stage-Gate Enforcement Protocol", ["No niche is pursued unless its P.A.I.D. NMPI score hits >= 75/100.", "No video or essay enters Monday planning unless a peer outlier hit M >= 2.5x.", "No script is drafted until the Package-First Title and 3-Word Thumbnail are locked."]),
                ("TheRPPH Transformation Equation", ["Numerator Lift: Combine 4-tier digital products ($68+ AOV) with $2,500+ B2B sponsor packages.", "Denominator Compression: Cap weekly production at 4.0 hours via Mon–Thu cognitive batching.", "Result: RPPH scales from $8.42/hr to $250–$600+/hr within 90 days."]),
            ],
            "Emphasize that RPPH grows from both sides of the fraction: cutting hours in the denominator while multiplying revenue per view in the numerator.",
        ),
        (
            "Pillar #1 — S.I.G.N.A.L. Outlier Validation & C.L.I.P. Hooks",
            "Engineering 7.5%+ CTR and 70%+ 30-Second Hold Rates Before Writing Your Script",
            [("Outlier Gate (M)", "M >= 2.5x Median", "14d Views / 90d Channel Median"), ("30s Hook Gate", ">= 70% Hold Rate", "C.L.I.P. 4-Part Opening"), ("Effective Retention", "ERI >= 2.30", "CTR × 30s Hold × AVD")],
            [
                ("The 6-Step S.I.G.N.A.L. Outlier Mining Loop (Chapter 3)", ["Monitor 25 peer channels in your niche and adjacent categories.", "Flag any upload where 14-day views >= 2.5x the channel's 90-day median views.", "Extract the curiosity gap, 3-word thumbnail contrast, and top comment friction (Prompts P11–P15)."]),
                ("Package-First & C.L.I.P. First-30-Second Hook (Chapter 4)", ["Lock Title + 3-Word Thumbnail first.", "0:00–0:05 Context Callout -> 0:05–0:12 Loss-Aversion Stakes -> 0:12–0:20 Instant Visual Proof -> 0:20–0:30 Open Loop.", "Sadia Rahman lifted CTR from 3.4% to 8.9% and 30s hold from 48% to 74% (ERI 3.55)."]),
            ],
            "Show how Devon Brooks (8.8x view lift) and Sadia Rahman (2.6x CTR lift) transformed reach using Stage 1 and Stage 2 math.",
        ),
        (
            "Pillar #2 — H.E.A.R.T. Scripting & The 1-to-15 Waterfall",
            "Drafting Authentic Pillar Scripts in 35 Minutes & Extracting 14 Native Derivatives",
            [("Voice DNA Profile", "5 Parameters", "100% Zero-Cliché Human Cadence"), ("Pillar Drafting", "35 Minutes", "2,000-Word H.E.A.R.T. Script"), ("Waterfall Output", "15 Native Assets", "5 Shorts + 4 Text + 3 Carousels + 2 Emails")],
            [
                ("5-Parameter Voice DNA + H.E.A.R.T. Architecture (Chapter 5)", ["Encode Sentence Variance, Technical Directness, Contrarian Edge, Rhythm, and Banned-Word Filters.", "Structure every pillar script around Hook, Evidence, Actionable Steps, Roadblocks, and Transformation.", "Insert a visual pattern-interrupt or B-Roll reset every 90 seconds to hold 52%+ AVD."]),
                ("The 50-Minute 1-to-15 Waterfall Sprint (Chapters 6–7)", ["Run Prompts P26–P30 on Tuesday morning against your locked Pillar Script.", "Automatically compile 5 vertical Shorts, 4 LinkedIn/X posts, 3 8-slide carousels, and 2 newsletter issues.", "Execute inside the 4-Hour Mon–Thu Batch Sprint (60m Plan / 90m Write / 60m Shoot / 30m QA)."]),
            ],
            "Explain why separating writing (Tuesday Block 2) from filming (Wednesday Block 3) eliminates context-switching fatigue.",
        ),
        (
            "Pillar #3 — Rented-to-Owned Bridge & 4-Tier Monetization",
            "Converting Social Views Into 45%+ Email Opt-Ins, Pre-Sold Products & B2B Deals",
            [("Opt-In Page CVR", "45% – 58% CVR", "5-Minute Utility Lead Magnet"), ("90-Day Sub Value", "V_sub >= $3.50", "5-Day Welcome Sequence"), ("Checkout Stack Lift", "+45% Effective AOV", "Order Bump + 1-Click Upsell")],
            [
                ("The Rented-to-Owned Audience Bridge (Chapter 8)", ["Replace 'Join my newsletter' with a specific 5-Minute Utility Lead Magnet (calculator, audit sheet, swipe file).", "Route new subscribers through a 3-Tag Intent Survey and 5-Day Automated Welcome Sequence (Prompts P36–P40).", "Hannah Lindqvist achieved 54.2% landing page opt-in CVR and $4.85 90-day V_sub."]),
                ("14-Day Product Pre-Sale & Outcome Sponsorships (Chapters 9–10)", ["Validate every digital product with 15+ paid pre-orders in 14 days before building Module 2.", "Add a 35%-take-rate Order Bump and 15%-take-rate 1-Click Upsell to lift AOV by +45%.", "Price B2B sponsorships on outcomes + 30%/mo paid-ad whitelisting rights ($2,500–$5,000+ deals)."]),
            ],
            "Point out that a channel with just 10,000 monthly views can generate $15,000+/month when Blended RPM hits $150–$300.",
        ),
        (
            "Real-World Operator Transformations (Empirical Case Matrix)",
            "Verified Before vs. After Telemetry From Solo Creators Using This System",
            [("Marcus Vance", "$7.86 -> $623/Hr", "$1,310 -> $14,850/Mo (5.5h/wk)"), ("Elena Rostova", "$7.00 -> $746/Hr", "$940 -> $19,400/Mo (NMPI 89)"), ("Chloe Sterling", "$13.23 -> $1,406/Hr", "$1,720 -> $26,800/Mo (10.6K Subs)")],
            [
                ("Small-to-Mid Channel Monetization Proof", ["Elena Rostova (8.9K subs): Shifted to clinical AI workflows, reaching $248 Blended RPM and $19,400/mo.", "Tariq Mahmoud (7.8K subs): Pre-sold 34 copies of a $99 workflow kit in 14 days ($5,180 at $152.35 AOV).", "Chloe Sterling (10.6K subs): Closed $3,400 quarterly B2B sponsor packages with a 75% renewal rate."]),
                ("Time Compression & Buffer Runway Proof", ["Liam O'Connor (22.1K subs): Cut pillar scripting from 9.5 hours to 38 minutes while lifting AVD to 56.4%.", "Kenji Takahashi (31.0K subs): Compressed a 34-hour grind into a 3.8-hour Mon–Thu sprint with a 4-week buffer."]),
            ],
            "Use these five case studies to prove that neither a 100K audience nor a 40-hour workweek is required.",
        ),
        (
            "30-Day Implementation Roadmap & Complete Flagship OS Access",
            "Your Week-by-Week Installation Plan Starting This Monday at 9:00 AM",
            [("Week 1: Foundation", "Audit & Niche Lock", "Worksheet 01–03 + NMPI >= 75"), ("Week 2: Production", "Voice DNA & Sprint", "1-to-15 Waterfall in 4 Hours"), ("Weeks 3–4: Revenue", "Bridge & Pre-Sale", "45% Opt-In + 14-Day Launch")],
            [
                ("Your 4-Week Operator Installation Sequence", ["Week 1: Run the 7-Day RPPH Audit, lock your P.A.I.D. Niche Matrix, and mine 30 S.I.G.N.A.L. Outliers.", "Week 2: Calibrate your 5-Parameter Voice DNA and execute your first 4-Hour 1-to-15 Batch Sprint.", "Weeks 3–4: Launch your 5-Minute Utility Lead Magnet, 5-Day Welcome Sequence, and 14-Day Product Pre-Sale."]),
                ("Activate the Complete Flagship Creator & Solopreneur OS", ["Includes the 340-Page Manual, 4 Fillable Workbooks (1,420 fields), and 12-Page Visual Shortcut Atlas.", "Full Pro Offline Web Companion App (Key: CREATOR-OS-PRO-2026) + 5-Database Notion Creator OS Kit.", "8-Tab Charted Excel Command Center, 7 Editable Word Docs, 3 Slide Decks & 5 Automation Blueprints."]),
            ],
            "Invite attendees to download the Tier 0 Free Audit Starter Kit or upgrade directly to the Tier 3 Flagship Bundle ($49).",
        ),
    ]

    p_deck2 = PPTX_DIR / "02-Educational-Masterclass-and-Webinar-Deck-Template.pptx"
    build_single_pptx_deck(p_deck2, "DECK 02 · MASTERCLASS & WEBINAR DECK", deck2_slides)
    results.append((p_deck2, len(deck2_slides)))

    # Deck 3: 03-Lead-Magnet-Visual-Carousel-and-Slide-Deck.pptx (10 slides)
    deck3_slides = [
        (
            "How to Turn 1 Weekly Script Into 15 Assets & $10K+/Mo in 4 Hours",
            "The 5-Stage Content-to-Cash Operating System Visual Carousel Blueprint",
            [("Weekly Time Cap", "4.0 Hours / Week", "Mon–Thu Time-Boxed Sprint"), ("Asset Multiplier", "1 Pillar -> 15 Posts", "Zero Copy-Paste Fluff"), ("Target Operator Yield", "$150 – $500+ / Hr", "Owned Funnel + B2B Sponsors")],
            [
                ("Why Most Creators Burn Out Before Month 6", ["Working 32+ hours every week guessing topics and manually reformatting posts.", "Earning under $9/hour relying on unpredictable algorithm reach and $5 AdSense RPM.", "Treating every social platform as a separate daily content treadmill."]),
                ("Swipe Through This 10-Slide Operator Blueprint", ["Discover the exact 6-step system used by top solo Creator-Operators.", "Every step includes a concrete mathematical formula and pass/fail stage gate.", "Grab the free 7-Day Time-Leak & RPPH Audit Kit on Slide 10."]),
            ],
            "Slide 1 is designed as a high-stopping-power LinkedIn/Instagram PDF carousel cover.",
        ),
        (
            "The Creator Treadmill Math: Why 32 Hours/Week = $8.75 RPPH",
            "Stop Tracking Vanity Views and Calculate Your Revenue Per Production Hour",
            [("The RPPH Formula", "Net Income / Hours", "Monthly Net ÷ (4.33 × Wk Hrs)"), ("Treadmill Baseline", "$8.42 / Hr Median", "Across 400+ Audited Creators"), ("Operator Target", ">= $200.00 / Hr", "Top 5% Solopreneur Benchmark")],
            [
                ("Where 32+ Hours Disappear Every Week", ["6.5 hrs scrolling feeds trying to brainstorm an unvalidated topic.", "9.0 hrs staring at a blank page rewriting a script from scratch.", "16.5 hrs filming retakes, cutting silence, and retyping posts for 4 platforms."]),
                ("The 10-Minute Diagnostic Fix", ["Track every production block for 7 days inside Worksheet 01.", "Compute your High-Value Production Ratio (HVPR target >= 70%).", "Eliminate or automate every task yielding under $50/hour."]),
            ],
            "Slide 2 exposes the math error behind creator burnout and introduces the RPPH equation.",
        ),
        (
            "Step 1 — Validate Demand With the 2.5x Outlier Multiplier",
            "Never Write a Line of Script Until a Topic Passes the S.I.G.N.A.L. Gate",
            [("Outlier Formula", "14d Views / Median", "Video 14d Views ÷ 90d Median"), ("Green-Light Gate", "M >= 2.5x Median", "Proves Packaging Demand"), ("View Velocity Lift", "3.4x – 8.8x Views", "Documented Operator Lift")],
            [
                ("How to Mine Outliers in 20 Minutes Every Monday", ["Maintain a watchlist of 25 peer channels in your niche.", "Spot uploads achieving 2.5x to 10x their channel's normal median views.", "Extract the psychological curiosity gap and top unanswered comment questions."]),
                ("Ethical Angle Transposition (Prompts P11–P15)", ["Never copy another creator's script or examples.", "Apply the proven curiosity structure to your own P.A.I.D. niche framework.", "Guarantees audience demand before you invest a single minute filming."]),
            ],
            "Slide 3 teaches the S.I.G.N.A.L. Outlier Multiplier formula from Chapter 3.",
        ),
        (
            "Step 2 — Package First: Title + 3-Word Thumbnail + C.L.I.P. Hook",
            "Lock Your Click-Through Rate (>= 7.5%) and 30-Second Hold Rate (>= 70%)",
            [("Thumbnail Rule", "Max 3 Elements", "Bold 3-Word Visual Contrast"), ("30s C.L.I.P. Gate", ">= 70% Retention", "Zero Throat-Clearing Intros"), ("ERI Target Score", "ERI >= 2.30", "CTR × 30s Hold × AVD")],
            [
                ("Enforce the Package-First Rule (Chapter 4)", ["Design your Title and 3-Word Thumbnail concept BEFORE opening your script doc.", "If you cannot summarize the visual curiosity contrast in 3 words, the angle is too fuzzy."]),
                ("The 30-Second C.L.I.P. Opening Sequence", ["0:00–0:05 Context Callout: Confirm the title promise in sentence one.", "0:05–0:12 Loss-Aversion Stakes: Quantify the cost of the status-quo mistake.", "0:12–0:20 Instant Visual Proof + 0:20–0:30 Pattern-Interrupt Open Loop."]),
            ],
            "Slide 4 breaks down the Package-First rule and the 4-part C.L.I.P. hook timeline.",
        ),
        (
            "Step 3 — Script With H.E.A.R.T. & 5-Parameter Voice DNA",
            "Draft 2,000-Word Authentic Pillar Scripts in 35 Minutes With 52%+ AVD",
            [("Voice DNA Calibration", "5 Linguistic Dials", "Bans 30+ Synthetic AI Clichés"), ("Pattern Reset Loop", "Every 90 Seconds", "Visual B-Roll / Diagram Cue"), ("Target Pillar AVD", ">= 52.0% Watch", "Sustained Mid-Roll Retention")],
            [
                ("Eliminate Robotic AI Prose Forever (Chapter 5)", ["Calibrate Sentence Variance, Technical Directness, Contrarian Edge, and Formatting Rhythm.", "Feed 3 samples of your real writing alongside Prompts P21–P25."]),
                ("The 5-Block H.E.A.R.T. Narrative Architecture", ["H — Hook & Status-Quo Teardown | E — Evidence & Case Study Proof.", "A — Actionable 3-Step Framework | R — Roadblock Inoculation | T — Transformation Bridge.", "Embed your native Lead Magnet or Sponsor demo right at the 40% mark."]),
            ],
            "Slide 5 shows how Voice DNA + H.E.A.R.T. scripting replaces 9 hours of writing with a 35-minute block.",
        ),
        (
            "Step 4 — Execute the 1-to-15 Omnichannel Repurposing Waterfall",
            "Turn 1 Tuesday Pillar Script Into 15 Platform-Native Assets in 50 Minutes",
            [("Pillar Anchor", "1 Master Script", "YouTube / Podcast / Essay"), ("Short-Form & Social", "5 Shorts + 7 Posts", "Reels, LinkedIn, X & Carousels"), ("Owned Newsletter", "2 Email Issues", "Tuesday Value + Friday Offer")],
            [
                ("Stop Cross-Posting Identical Links (Chapter 6)", ["Algorithms penalize lazy copy-paste links; every platform requires native formatting.", "Use Prompts P26–P30 to transpose your Pillar Script into 14 native derivatives in one sitting."]),
                ("The Complete 15-Asset Weekly Breakdown", ["1 Long-Form Pillar Video/Essay + 5 Vertical 60s Shorts/Reels.", "4 LinkedIn Authority Posts & X Threads + 3 Visual 8-Slide PDF Carousels.", "2 Owned Email Newsletter Issues driving readers to your product ladder."]),
            ],
            "Slide 6 visualizes the 1-to-15 Omnichannel Waterfall matrix.",
        ),
        (
            "Step 5 — Capture Owned Emails With a 5-Minute Utility Lead Magnet",
            "Convert 45%+ of Landing Page Visitors and $3.50+ Per Subscriber in 90 Days",
            [("Opt-In Page CVR", "45% – 58% Target", "Single-Promise Wireframe"), ("Welcome Sequence", "5 Automated Emails", ">= 2.5% Core Offer Conversion"), ("90-Day Sub Value", "V_sub >= $3.50", "Owned Audience Insurance")],
            [
                ("Kill the Generic 'Join My Newsletter' Box (Chapter 8)", ["Nobody wakes up wanting more inbox clutter; they want an immediate 5-minute tool.", "Offer a concrete calculator, checklist, Notion template, or 7-day audit sheet."]),
                ("The 3-Tag Router & 5-Day Welcome Bridge", ["Tag every new subscriber by Pain Point and Revenue Stage on thank-you page.", "Deliver a 5-email automated sequence (Prompts P36–P40) that builds trust and pitches Tier 1/2."]),
            ],
            "Slide 7 explains the Rented-to-Owned Audience Bridge from Chapter 8.",
        ),
        (
            "Step 6 — Monetize via the 4-Tier Value Ladder & Outcome Sponsors",
            "Pre-Sell Digital Products in 14 Days (+45% AOV) & Close $2,500+ Brand Deals",
            [("Pre-Sale Gate", ">= 15 Paid Orders", "14-Day Validation Before Building"), ("Checkout Stack", "+45% AOV Lift", "35% Bump + 15% 1-Click Upsell"), ("Sponsor Package", "$2,500 – $5,000+", "+30%/Mo Ad Whitelisting Fee")],
            [
                ("The 4-Tier Digital Product Value Ladder (Chapter 9)", ["Tier 0 Free Kit -> Tier 1/2 Impulse Workbook ($24–$49) -> Tier 3 Flagship OS ($49–$199) -> Tier 4 Vault.", "Never build a full product until you collect at least 15 paid pre-orders in a 14-day sprint."]),
                ("Outcome-Based B2B Sponsorships (Chapter 10)", ["Bundle 1 Pillar Demo + 2 Newsletters + LinkedIn + 30–90 days of Paid-Ad Whitelisting rights.", "Enables channels with under 15,000 subscribers to command $2,500 to $5,000+ per package."]),
            ],
            "Slide 8 connects digital product unit economics with outcome-priced B2B sponsorships.",
        ),
        (
            "The 4-Hour Weekly Batch Production Sprint Schedule (Mon–Thu)",
            "Eliminate Context Switching by Separating Cognitive Modes Across 4 Days",
            [("Mon Block 1 (60m)", "Validate & Package", "Outlier M >= 2.5x + Thumbnail"), ("Tue Block 2 (90m)", "Script & Waterfall", "H.E.A.R.T. + 14 Derivatives"), ("Wed/Thu (90m)", "Shoot & 12-Pt QA", "60m A-Roll + 30m Scheduling")],
            [
                ("Monday & Tuesday: Strategy & Writing Blocks", ["Monday (60 min): Mine S.I.G.N.A.L. outliers, lock Title + 3-Word Thumbnail, and script 30s C.L.I.P. hook.", "Tuesday (90 min): Draft 2,000-word Pillar Script (35m) and extract all 14 derivative assets (55m)."]),
                ("Wednesday, Thursday & Friday CEO Cadence", ["Wednesday (60 min): Batch-record Teleprompter A-Roll and screen-share demos in one take.", "Thursday (30 min): Run the 12-Point Pre-Flight QA Gate and schedule all 15 assets.", "Friday (20 min): Run the Creator CEO Scorecard, audit RPPH, and send 5 outbound sponsor pitches."]),
            ],
            "Slide 9 gives readers a concrete weekly calendar they can screenshot and pin above their desk.",
        ),
        (
            "Download the Free 7-Day Creator Time-Leak & RPPH Audit Kit",
            "Calculate Your Baseline RPPH in 10 Minutes & Install the Complete Operating System",
            [("Tier 0 Free Kit", "$0 Instant Access", "Ch 1 PDF + Fillable Workbook 01"), ("Offline Web App", "6 Calculators", "+ 62-Item Prompt & Script Vault"), ("Flagship Bundle", "$49 Complete OS", "Book + Notion + Excel + Office")],
            [
                ("What You Get Free in the Tier 0 Starter Kit ($0)", ["Complete 9,704-word Chapter 1 Manual + 48-Field Fillable Worksheet 01 PDF.", "100% Offline SaaS-Lite Web Companion App (Module 1 RPPH Simulator + Prompts P01–P05).", "25-Row Creator RPM & Time-Leak Audit Spreadsheet + Master Ecosystem Poster."]),
                ("Ready for the Full System? Grab the Tier 3 Flagship OS", ["340-Page Color Book + EPUB 3.0 + All 4 Fillable Workbooks + 12-Page Visual Shortcut Atlas.", "Pro Web App Key (CREATOR-OS-PRO-2026) + 5-DB Notion Kit + 8-Tab Excel + 7 Word Docs + 5 Automations."]),
            ],
            "Slide 10 closes the carousel with a clear dual CTA to the Free Audit Kit or the Complete Flagship Bundle.",
        ),
    ]

    p_deck3 = PPTX_DIR / "03-Lead-Magnet-Visual-Carousel-and-Slide-Deck.pptx"
    build_single_pptx_deck(p_deck3, "DECK 03 · LEAD MAGNET & CAROUSEL DECK", deck3_slides)
    results.append((p_deck3, len(deck3_slides)))

    return results


def build_single_pptx_deck(out_path: Path, deck_label: str, slides_spec: list) -> None:
    prs = Presentation()
    prs.slide_width = PptxInches(13.333)
    prs.slide_height = PptxInches(7.5)
    total = len(slides_spec)
    for idx, (title, sub, kpis, cards, note) in enumerate(slides_spec, start=1):
        sl = add_pptx_slide_shell(prs, deck_label, idx, total, title, sub, note)
        populate_slide_cards_and_table(sl, kpis, cards, note)
    prs.save(str(out_path))


# ---------------------------------------------------------------------------
# UPGRADE 5: INTERACTIVE DESIGN CUSTOMIZER STUDIO (08-COVER-DESIGN/Editable-Design-Kit/)
# ---------------------------------------------------------------------------

def build_design_customizer_studio() -> tuple[Path, Path]:
    DESIGN_KIT_DIR.mkdir(parents=True, exist_ok=True)
    html_path = DESIGN_KIT_DIR / "design-customizer-studio.html"
    readme_path = DESIGN_KIT_DIR / "README-DESIGN-KIT.md"

    presets_data = [
        {
            "id": "yt-thumb",
            "name": "1. YouTube High-CTR Thumbnail (1280 × 720 px)",
            "width": 1280,
            "height": 720,
            "badge": "OUTLIER MULTIPLIER: 4.3x VERIFIED",
            "headline1": "35 HRS TO 4 HRS",
            "headline2": "THE 1-TO-15 AI OS",
            "subtitle": "How Solo Creators Automate Production & Scale RPPH to $380/Hr",
            "author": "@CREATOR_OPERATOR · 5-STAGE ENGINE",
            "metricPill": "CTR: 9.4% | HOLD: 74%"
        },
        {
            "id": "kdp-ebook",
            "name": "2. Kindle / KDP eBook Cover (1600 × 2560 px)",
            "width": 1600,
            "height": 2560,
            "badge": "APEX DIGITAL SYSTEMS STUDIO · FLAGSHIP EDITION",
            "headline1": "THE AI CONTENT CREATOR",
            "headline2": "& SOLOPRENEUR OS",
            "subtitle": "A Practical System to Research Validated Ideas, Script High-Retention Content, Repurpose Across Platforms, Automate Production, and Monetize Without Burnout",
            "author": "APEX DIGITAL SYSTEMS STUDIO",
            "metricPill": "50 AI PROMPTS · 20 DIAGRAMS · 10 WORKBOOKS"
        },
        {
            "id": "gumroad-cover",
            "name": "3. Gumroad Product Cover (1600 × 1000 px)",
            "width": 1600,
            "height": 1000,
            "badge": "TIER 3 COMPLETE FLAGSHIP SOLOPRENEUR BUNDLE",
            "headline1": "COMPLETE CREATOR OS",
            "headline2": "BOOK + WEB APP + NOTION KIT",
            "subtitle": "340-Page Manual + 4 Fillable Workbooks + Pro Web Suite + 8-Tab Excel + 5 Automations",
            "author": "INSTANT DOWNLOAD · DRM-FREE · $49 FLAGSHIP EDITION",
            "metricPill": "PRO KEY: CREATOR-OS-PRO-2026"
        },
        {
            "id": "carousel-slide",
            "name": "4. LinkedIn / IG Carousel Cover Slide (1080 × 1350 px)",
            "width": 1080,
            "height": 1350,
            "badge": "SWIPE-BY-SWIPE OPERATOR PLAYBOOK (1/8)",
            "headline1": "STOP GUESSING TOPICS.",
            "headline2": "USE THE 2.5x OUTLIER RULE.",
            "subtitle": "The 6-Step S.I.G.N.A.L. Validation Formula That Lifted Average Views by 8.8x in 6 Weeks",
            "author": "SWIPE LEFT FOR THE EXACT FORMULA ->",
            "metricPill": "STAGE GATE: M >= 2.5x MEDIAN"
        },
        {
            "id": "newsletter-banner",
            "name": "5. Newsletter Header Banner (1200 × 630 px)",
            "width": 1200,
            "height": 630,
            "badge": "THE WEEKLY CREATOR-OPERATOR BRIEFING · ISSUE #42",
            "headline1": "THE 4-HOUR BATCH SPRINT",
            "headline2": "1 PILLAR -> 15 NATIVE ASSETS",
            "subtitle": "Inside This Issue: 5-Parameter Voice DNA Calibration + 12-Point Pre-Flight QA Gate",
            "author": "READ TIME: 4 MINUTES · BY APEX DIGITAL SYSTEMS",
            "metricPill": "RPPH TARGET: >= $200/HR"
        },
        {
            "id": "lead-magnet-card",
            "name": "6. Lead Magnet Cheat-Sheet Mockup Card (1200 × 900 px)",
            "width": 1200,
            "height": 900,
            "badge": "FREE 5-MINUTE UTILITY DOWNLOAD · TIER 0 STARTER KIT",
            "headline1": "7-DAY TIME-LEAK & RPPH",
            "headline2": "DIAGNOSTIC AUDIT KIT",
            "subtitle": "Includes Chapter 1 PDF + 48-Field Fillable Workbook + Offline RPPH Web Simulator + CSV Tracker",
            "author": "100% FREE INSTANT DOWNLOAD · ZERO CREDIT CARD REQUIRED",
            "metricPill": "RECLAIM 15+ HOURS/WEEK"
        }
    ]

    themes_data = [
        {"id": "indigo", "name": "Creator Indigo (Default)", "bg1": "#0F172A", "bg2": "#1E1B4B", "accent": "#4F46E5", "secondary": "#2DD4BF", "pill": "#D97706"},
        {"id": "slate", "name": "Deep Studio Slate", "bg1": "#090D16", "bg2": "#1E293B", "accent": "#38BDF8", "secondary": "#A5B4FC", "pill": "#0D9488"},
        {"id": "teal", "name": "Conversion Teal", "bg1": "#042F2E", "bg2": "#0F172A", "accent": "#0D9488", "secondary": "#5EEAD4", "pill": "#F59E0B"},
        {"id": "amber", "name": "Retention Amber", "bg1": "#1C1917", "bg2": "#0F172A", "accent": "#D97706", "secondary": "#FCD34D", "pill": "#4F46E5"},
        {"id": "emerald", "name": "Emerald Authority", "bg1": "#064E3B", "bg2": "#0F172A", "accent": "#059669", "secondary": "#6EE7B7", "pill": "#4F46E5"},
        {"id": "crimson", "name": "Crimson Outlier", "bg1": "#4C0519", "bg2": "#0F172A", "accent": "#E11D48", "secondary": "#FDA4AF", "pill": "#D97706"}
    ]

    import json
    studio_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Creator OS — Interactive Cover, YouTube Thumbnail &amp; Social Card Customizer Studio</title>
  <style>
    :root {{
      --primary: #0F172A;
      --accent: #4F46E5;
      --secondary: #0D9488;
      --warning: #D97706;
      --text: #1E293B;
      --muted: #64748B;
      --bg: #F8FAFC;
      --card: #FFFFFF;
      --border: #E2E8F0;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #090D16;
      color: #F8FAFC;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    .mono {{ font-family: 'JetBrains Mono', 'Consolas', monospace; }}
    .studio-topbar {{
      background: #0F172A;
      border-bottom: 2px solid var(--accent);
      padding: 14px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
    }}
    .topbar-left {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-icon {{
      width: 36px;
      height: 36px;
      border-radius: 8px;
      background: linear-gradient(135deg, var(--accent), var(--secondary));
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      color: #FFF;
    }}
    .topbar-title {{
      font-size: 1.05rem;
      font-weight: 900;
      letter-spacing: -0.3px;
    }}
    .topbar-sub {{
      font-size: 0.76rem;
      color: #94A3B8;
      display: block;
    }}
    .topbar-actions {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .btn {{
      border: none;
      padding: 10px 18px;
      border-radius: 8px;
      font-weight: 800;
      font-size: 0.86rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: transform 0.12s, opacity 0.12s;
    }}
    .btn:hover {{ transform: translateY(-1px); opacity: 0.95; }}
    .btn-png {{ background: var(--secondary); color: #FFFFFF; }}
    .btn-svg {{ background: var(--accent); color: #FFFFFF; }}
    .btn-reset {{ background: #1E293B; color: #CBD5E1; border: 1px solid #334155; }}

    .studio-workspace {{
      display: grid;
      grid-template-columns: 420px 1fr;
      flex: 1;
      min-height: calc(100vh - 68px);
    }}
    .controls-sidebar {{
      background: #0F172A;
      border-right: 1px solid #1E293B;
      padding: 22px;
      overflow-y: auto;
      max-height: calc(100vh - 68px);
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}
    .control-card {{
      background: #1E293B;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 16px;
      display: grid;
      gap: 12px;
    }}
    .control-card h3 {{
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #818CF8;
      border-bottom: 1px solid #334155;
      padding-bottom: 8px;
    }}
    .field-group {{
      display: grid;
      gap: 5px;
    }}
    .field-group label {{
      font-size: 0.78rem;
      font-weight: 700;
      color: #CBD5E1;
      display: flex;
      justify-content: space-between;
    }}
    .field-group input[type="text"],
    .field-group select,
    .field-group textarea {{
      width: 100%;
      background: #090D16;
      border: 1px solid #475569;
      color: #FFFFFF;
      padding: 9px 11px;
      border-radius: 7px;
      font-size: 0.85rem;
      font-family: inherit;
    }}
    .field-group textarea {{
      resize: vertical;
      min-height: 54px;
    }}
    .color-row {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
    }}
    .color-picker-box {{
      background: #090D16;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 8px;
      text-align: center;
    }}
    .color-picker-box label {{
      font-size: 0.7rem;
      color: #94A3B8;
      display: block;
      margin-bottom: 4px;
    }}
    .color-picker-box input[type="color"] {{
      width: 100%;
      height: 30px;
      border: none;
      background: transparent;
      cursor: pointer;
    }}

    /* Preview Canvas Stage */
    .preview-stage {{
      background: radial-gradient(circle at center, #1E293B 0%, #090D16 100%);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 32px;
      overflow: auto;
      position: relative;
    }}
    .stage-meta-bar {{
      display: flex;
      gap: 16px;
      align-items: center;
      margin-bottom: 18px;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid #334155;
      padding: 8px 18px;
      border-radius: 999px;
      font-size: 0.8rem;
      color: #CBD5E1;
    }}
    .svg-preview-container {{
      box-shadow: 0 25px 70px rgba(0, 0, 0, 0.65);
      border: 2px solid #334155;
      border-radius: 8px;
      background: #0F172A;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      max-width: 100%;
    }}
    .svg-preview-container svg {{
      display: block;
      max-width: min(100%, 880px);
      max-height: 72vh;
      width: auto;
      height: auto;
    }}
    .template-gallery-strip {{
      margin-top: 22px;
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 10px;
      width: 100%;
      max-width: 980px;
    }}
    .preset-chip {{
      background: #0F172A;
      border: 1.5px solid #334155;
      color: #CBD5E1;
      padding: 10px;
      border-radius: 8px;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s;
    }}
    .preset-chip.active, .preset-chip:hover {{
      border-color: var(--secondary);
      background: rgba(13, 148, 136, 0.18);
      color: #FFFFFF;
    }}
    @media (max-width: 1024px) {{
      .studio-workspace {{ grid-template-columns: 1fr; }}
      .controls-sidebar {{ max-height: none; }}
      .template-gallery-strip {{ grid-template-columns: repeat(2, 1fr); }}
    }}
  </style>
</head>
<body>

  <header class="studio-topbar">
    <div class="topbar-left">
      <span class="brand-icon">DS</span>
      <div>
        <span class="topbar-title">Creator OS — Cover, YouTube Thumbnail &amp; Social Card Customizer Studio</span>
        <span class="topbar-sub">100% Offline Vector &amp; High-Res Raster Design Engine · Zero External Dependencies</span>
      </div>
    </div>
    <div class="topbar-actions">
      <button class="btn btn-reset" onclick="resetCurrentPreset()">Reset Preset Defaults</button>
      <button class="btn btn-svg" onclick="exportEditableSvg()">Download Editable Vector (.SVG)</button>
      <button class="btn btn-png" onclick="exportHighResPng()">Download High-Res Raster (.PNG)</button>
    </div>
  </header>

  <main class="studio-workspace">
    <!-- Left Controls Sidebar -->
    <aside class="controls-sidebar">
      <div class="control-card">
        <h3>1. Canvas Format &amp; Dimension Preset</h3>
        <div class="field-group">
          <label for="sel-preset">Select Target Platform Canvas</label>
          <select id="sel-preset" onchange="onPresetChange(this.value)"></select>
        </div>
        <div class="field-group">
          <label for="sel-layout">Visual Architecture Layout Style</label>
          <select id="sel-layout" onchange="renderStudioSvg()">
            <option value="grid-glow">Architectural Grid + Radial Glow + 5-Stage Telemetry</option>
            <option value="split-contrast">High-CTR Split Contrast Card (Ideal for Thumbnails)</option>
            <option value="executive-frame">Minimalist Executive Double-Frame (Ideal for Covers)</option>
            <option value="blueprint-matrix">Technical Blueprint Matrix + Corner Fiducials</option>
          </select>
        </div>
      </div>

      <div class="control-card">
        <h3>2. Live Typography &amp; Hook Copy</h3>
        <div class="field-group">
          <label for="inp-badge">Top Authority / Stage-Gate Badge</label>
          <input type="text" id="inp-badge" oninput="renderStudioSvg()" />
        </div>
        <div class="field-group">
          <label for="inp-h1">Primary Headline / 3-Word Thumbnail Hook (Line 1)</label>
          <input type="text" id="inp-h1" oninput="renderStudioSvg()" />
        </div>
        <div class="field-group">
          <label for="inp-h2">Secondary Accent Headline (Line 2)</label>
          <input type="text" id="inp-h2" oninput="renderStudioSvg()" />
        </div>
        <div class="field-group">
          <label for="inp-sub">Subtitle / Value Proposition Copy</label>
          <textarea id="inp-sub" oninput="renderStudioSvg()"></textarea>
        </div>
        <div class="field-group">
          <label for="inp-metric">Quantitative Proof / Metric Callout Pill</label>
          <input type="text" id="inp-metric" oninput="renderStudioSvg()" />
        </div>
        <div class="field-group">
          <label for="inp-author">Footer Imprint / Creator Handle</label>
          <input type="text" id="inp-author" oninput="renderStudioSvg()" />
        </div>
      </div>

      <div class="control-card">
        <h3>3. Brand Palette &amp; Custom Hex Colors</h3>
        <div class="field-group">
          <label for="sel-theme">Quick Studio Theme Preset</label>
          <select id="sel-theme" onchange="onThemeChange(this.value)"></select>
        </div>
        <div class="color-row">
          <div class="color-picker-box">
            <label for="col-bg1">Canvas Navy</label>
            <input type="color" id="col-bg1" value="#0F172A" oninput="renderStudioSvg()" />
          </div>
          <div class="color-picker-box">
            <label for="col-accent">Primary Accent</label>
            <input type="color" id="col-accent" value="#4F46E5" oninput="renderStudioSvg()" />
          </div>
          <div class="color-picker-box">
            <label for="col-sec">Secondary Teal</label>
            <input type="color" id="col-sec" value="#2DD4BF" oninput="renderStudioSvg()" />
          </div>
        </div>
        <div class="field-group">
          <label for="inp-scale">Headline Font Scale (%) <span id="lbl-scale" class="mono">100%</span></label>
          <input type="range" id="inp-scale" min="70" max="135" value="100" oninput="document.getElementById('lbl-scale').textContent=this.value+'%';renderStudioSvg();" />
        </div>
      </div>

      <div class="control-card">
        <h3>4. Custom Headshot / Brand Logo Overlay</h3>
        <div class="field-group">
          <label for="inp-logo">Upload Local PNG/JPG/SVG (Injected as Offline Data-URI)</label>
          <input type="file" id="inp-logo" accept="image/*" onchange="handleLogoUpload(event)" />
        </div>
        <button class="btn btn-reset" style="width:100%;justify-content:center;" onclick="clearUploadedLogo()">Remove Uploaded Image</button>
      </div>

      <div class="control-card">
        <h3>5. 24-Hook &amp; 3-Word Thumbnail Swipe Vault</h3>
        <div class="field-group">
          <label for="sel-swipe">Load Pre-Validated Outlier Packaging Swipe</label>
          <select id="sel-swipe" onchange="applyPackagingSwipe(this.value)"></select>
        </div>
        <div class="field-group">
          <label for="sel-carousel-slide">8-Slide Carousel Sequence Builder (Ch 06)</label>
          <select id="sel-carousel-slide" onchange="applyCarouselSlidePreset(this.value)"></select>
        </div>
        <button class="btn btn-svg" style="width:100%;justify-content:center;margin-top:6px;" onclick="toggleMobileSquintTest()">Toggle 1.5s Mobile Squint-Test Mode</button>
      </div>
    </aside>

    <!-- Right Live Canvas Preview Stage -->
    <section class="preview-stage">
      <div class="stage-meta-bar mono">
        <span id="meta-preset-name">YouTube High-CTR Thumbnail</span>
        <span>·</span>
        <span id="meta-dims">1280 × 720 px</span>
        <span>·</span>
        <span id="meta-contrast-badge" style="color:#2DD4BF;">WCAG CONTRAST: AAA PASS (13.8:1)</span>
      </div>

      <div class="svg-preview-container" id="svg-mount"></div>

      <div class="template-gallery-strip" id="preset-chips-bar"></div>
      <canvas id="export-canvas" style="display:none;"></canvas>

      <!-- Interactive Packaging QA & 15-Asset Omnichannel Dimension Reference Matrix -->
      <div style="width:100%;max-width:1060px;margin-top:18px;background:#0F172A;border:1px solid #334155;border-radius:12px;padding:16px 20px;color:#E2E8F0;font-size:12.5px;">
        <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #1E293B;padding-bottom:10px;margin-bottom:12px;">
          <strong style="color:#2DD4BF;font-family:'JetBrains Mono',monospace;letter-spacing:0.8px;">PACKAGE-FIRST 10-POINT QA GATE &amp; OMNICHANNEL DIMENSION SPEC SHEET (CHAPTERS 04, 06 &amp; 07)</strong>
          <span style="background:#312E81;color:#A5B4FC;padding:3px 10px;border-radius:6px;font-family:'JetBrains Mono',monospace;font-size:11px;">TARGET CTR &gt;= 6.5% · 30S HOLD &gt;= 70%</span>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div style="background:#1E293B;border:1px solid #334155;border-radius:8px;padding:12px;">
            <h4 style="color:#F8FAFC;margin-bottom:8px;font-size:13px;">A. Monday Block 1 Thumbnail &amp; Title Pairing Checklist</h4>
            <ul style="list-style:none;padding:0;margin:0;line-height:1.65;color:#CBD5E1;">
              <li>&#9745; <strong>Rule 01 (3-Word Max):</strong> Primary thumbnail headline contains 3 to 5 high-contrast words maximum so mobile viewers parse it in &lt; 1.5 seconds.</li>
              <li>&#9745; <strong>Rule 02 (Zero Text Duplication):</strong> Your 52–68 character video title complements the thumbnail hook rather than repeating the exact same phrase.</li>
              <li>&#9745; <strong>Rule 03 (Quantified Contrast):</strong> Include at least one concrete number, dollar figure, timeframe, or Before-vs-After split (`35 Hrs -&gt; 4 Hrs`).</li>
              <li>&#9745; <strong>Rule 04 (WCAG AAA Legibility):</strong> Maintain &gt;= 7.0:1 luminance contrast between foreground typography (`#FFFFFF` / `#2DD4BF`) and background (`#0F172A`).</li>
              <li>&#9745; <strong>Rule 05 (Right-Bottom Timestamp Safe Zone):</strong> Never place critical words in the bottom-right 140x48px corner where YouTube overlays the video duration badge.</li>
              <li>&#9745; <strong>Rule 06 (A/B Backup Ready):</strong> Export two distinct thumbnail variants (`Variant A: Math Contrast` and `Variant B: Status-Quo Warning`) before hitting record on Wednesday.</li>
            </ul>
          </div>
          <div style="background:#1E293B;border:1px solid #334155;border-radius:8px;padding:12px;">
            <h4 style="color:#F8FAFC;margin-bottom:8px;font-size:13px;">B. Omnichannel Visual &amp; Packaging Dimension Reference</h4>
            <table style="width:100%;border-collapse:collapse;font-size:11.5px;color:#CBD5E1;">
              <thead>
                <tr style="background:#090D16;color:#2DD4BF;text-align:left;">
                  <th style="padding:5px 6px;">Platform Deliverable</th>
                  <th style="padding:5px 6px;">Exact Pixel Spec</th>
                  <th style="padding:5px 6px;">Ratio</th>
                  <th style="padding:5px 6px;">Safe Zone Rule</th>
                </tr>
              </thead>
              <tbody>
                <tr style="border-bottom:1px solid #334155;"><td style="padding:4px 6px;">1. YouTube Pillar Thumbnail</td><td style="padding:4px 6px;font-family:monospace;">1280 × 720 px</td><td style="padding:4px 6px;">16:9</td><td style="padding:4px 6px;">Avoid bottom-right timestamp</td></tr>
                <tr style="border-bottom:1px solid #334155;"><td style="padding:4px 6px;">2. Kindle / Apple Books eBook</td><td style="padding:4px 6px;font-family:monospace;">1600 × 2560 px</td><td style="padding:4px 6px;">1:1.6</td><td style="padding:4px 6px;">75px outer margin clearance</td></tr>
                <tr style="border-bottom:1px solid #334155;"><td style="padding:4px 6px;">3. Gumroad / LemonSqueezy Card</td><td style="padding:4px 6px;font-family:monospace;">1600 × 1000 px</td><td style="padding:4px 6px;">16:10</td><td style="padding:4px 6px;">Center 4-tier value badges</td></tr>
                <tr style="border-bottom:1px solid #334155;"><td style="padding:4px 6px;">4. LinkedIn PDF / IG Carousel</td><td style="padding:4px 6px;font-family:monospace;">1080 × 1350 px</td><td style="padding:4px 6px;">4:5</td><td style="padding:4px 6px;">Max 28 words per slide card</td></tr>
                <tr style="border-bottom:1px solid #334155;"><td style="padding:4px 6px;">5. Newsletter / OpenGraph Card</td><td style="padding:4px 6px;font-family:monospace;">1200 × 630 px</td><td style="padding:4px 6px;">1.91:1</td><td style="padding:4px 6px;">Readable at 320px mobile card</td></tr>
                <tr><td style="padding:4px 6px;">6. Lead Magnet Hero Mockup</td><td style="padding:4px 6px;font-family:monospace;">1200 × 900 px</td><td style="padding:4px 6px;">4:3</td><td style="padding:4px 6px;">Pair with 1-field email box</td></tr>
              </tbody>
            </table>
          </div>
        </div>
        <div style="margin-top:12px;background:#090D16;border:1px solid #1E293B;border-radius:8px;padding:10px 14px;display:flex;justify-content:space-between;align-items:center;">
          <span><strong>PRO OPERATOR WORKFLOW:</strong> Export all 8 Carousel PNGs (`1080×1350`) using the <em>8-Slide Carousel Sequence Builder</em> in Panel 5, or export clean `.SVG` vectors to customize in Figma/Illustrator.</span>
          <span class="mono" style="color:#FBBF24;">100% OFFLINE · ZERO EXTERNAL CDNS</span>
        </div>
      </div>
    </section>
  </main>

  <script>
    const PRESETS = {json.dumps(presets_data)};
    const THEMES = {json.dumps(themes_data)};

    const PACKAGING_SWIPES = [
      {{ id: "sw01", label: "01. [Time Audit] 35 Hrs -> 4 Hrs (M = 4.3x)", badge: "OUTLIER MULTIPLIER: 4.3x VERIFIED", h1: "35 HRS TO 4 HRS", h2: "THE SOLO CREATOR OS", sub: "How I replaced a 35-hour content treadmill with a 4-hour batch system", metric: "RPPH: $685/HR | 15 ASSETS" }},
      {{ id: "sw02", label: "02. [Treadmill Trap] Stop Posting Daily (M = 3.8x)", badge: "CHAPTER 01 UNIT ECONOMICS", h1: "STOP POSTING DAILY", h2: "THE $8/HR TRAP EXPOSED", sub: "Why daily unvalidated posting destroys solopreneur profit margins", metric: "NET MARGIN: 86% VERIFIED" }},
      {{ id: "sw03", label: "03. [Niche Matrix] 5,000 Buyers > 1M Views (M = 4.1x)", badge: "P.A.I.D. NICHE MATRIX >= 75", h1: "5,000 TRUE BUYERS", h2: "BEAT 1,000,000 VIEWS", sub: "Engineering a $240+ Blended RPM in high-intent B2B & prosumer niches", metric: "NMPI SCORE: 89.5 / 100" }},
      {{ id: "sw04", label: "04. [Category of One] Clone Your Voice DNA (M = 3.6x)", badge: "5-PARAMETER VOICE DNA CARD", h1: "ZERO AI SLOP", h2: "CLONE YOUR VOICE DNA", sub: "Calibrate Claude & GPT to write with your exact rhythm and contrarian edge", metric: "0 BANNED WORDS | 54% AVD" }},
      {{ id: "sw05", label: "05. [Outlier Radar] Find 3x Ideas in 15 Mins (M = 4.6x)", badge: "S.I.G.N.A.L. DEMAND RADAR", h1: "3X OUTLIER RADAR", h2: "VALIDATE BEFORE WRITING", sub: "The 25-channel peer cohort formula that guarantees audience demand", metric: "GATE: M_OUTLIER >= 2.5X" }},
      {{ id: "sw06", label: "06. [Comment Mining] Mine Competitor Gaps (M = 3.4x)", badge: "PROMPT P12 GAP EXTRACTOR", h1: "MINE PEER COMMENTS", h2: "STEAL UNSOLVED DEMAND", sub: "How to extract your next 12 breakout video topics from competitor comments", metric: "100% VALIDATED PAIN" }},
      {{ id: "sw07", label: "07. [C.L.I.P. Hook] 74% 30-Second Hold (M = 5.1x)", badge: "FIRST 30-SECOND HOOK LAB", h1: "74% 30-SEC HOLD", h2: "THE C.L.I.P. FORMULA", sub: "Word-for-word 85-word video openers that eliminate early viewer drop-off", metric: "ERI SCORE: 2.94 PASS" }},
      {{ id: "sw08", label: "08. [3-Word Thumb] Double Your CTR Overnight (M = 4.2x)", badge: "PACKAGE-FIRST DESIGN RULE", h1: "3-WORD THUMBNAILS", h2: "DOUBLE YOUR CLICK RATE", sub: "Why designing the thumbnail before writing the script lifts CTR to 9.4%", metric: "1.5S SQUINT TEST: PASS" }},
      {{ id: "sw09", label: "09. [H.E.A.R.T. Script] 2,000 Words in 45m (M = 3.9x)", badge: "MODULAR CHAINED PROMPTING", h1: "2,000-WORD SCRIPT", h2: "IN 45 MINUTES FLAT", sub: "The 5-block H.E.A.R.T. narrative engine with 90-second pattern resets", metric: "HOLD AT 10:00: 53.8%" }},
      {{ id: "sw10", label: "10. [Sudden Outro] Never Say 'To Wrap Up' (M = 3.5x)", badge: "END-SCREEN RETENTION FIX", h1: "KILL BORING OUTROS", h2: "+42% END-SCREEN CLICKS", sub: "How the Sudden-Death Outro prevents the 40% final-minute viewer exodus", metric: "BRIDGE CTR: 11.2%" }},
      {{ id: "sw11", label: "11. [1-to-15 Waterfall] 1 Script -> 15 Posts (M = 4.8x)", badge: "OMNICHANNEL MULTIPLIER ENGINE", h1: "1 PILLAR SCRIPT", h2: "INTO 15 NATIVE POSTS", sub: "Atomize one weekly video into 5 Shorts, 4 text posts, 3 carousels & 2 emails", metric: "45-MIN AI EXTRACTION" }},
      {{ id: "sw12", label: "12. [Carousel Engine] High-Save PDF Carousels (M = 3.7x)", badge: "LINKEDIN & IG AUTHORITY", h1: "8-SLIDE CAROUSELS", h2: "THAT DRIVE 48% OPT-INS", sub: "Turn Block 3 of your Pillar script into bookmark-worthy visual slide decks", metric: "1080x1350 PORTRAIT SPEC" }},
      {{ id: "sw13", label: "13. [4-Hour Batch] Mon-Thu Production OS (M = 4.5x)", badge: "ZERO CONTEXT-SWITCHING TAX", h1: "THE 4-HOUR WEEK", h2: "BATCH PRODUCTION SOP", sub: "Mon Ideate (60m) · Tue Script (90m) · Wed Record (60m) · Thu Queue (30m)", metric: "SAVES 18.4 HRS / WEEK" }},
      {{ id: "sw14", label: "14. [Zero-Setup Desk] Press Record in 45s (M = 3.3x)", badge: "FRICTIONLESS STUDIO HARDWARE", h1: "45-SECOND SETUP", h2: "PERMANENT DESK STUDIO", sub: "Eliminate camera and lighting friction with a single smart-plug desk rig", metric: "ONE-TAKE TELEPROMPTER" }},
      {{ id: "sw15", label: "15. [Utility Magnet] Kill 50-Page PDF eBooks (M = 4.0x)", badge: "CHAPTER 08 AUDIENCE OWNERSHIP", h1: "KILL 50-PAGE PDFS", h2: "BUILD 5-MIN CALCULATORS", sub: "Why interactive utility lead magnets convert cold viewers at 51.4% opt-in", metric: "LANDING CVR >= 45.0%" }},
      {{ id: "sw16", label: "16. [Welcome Funnel] 5 Emails -> $99 Buyers (M = 4.4x)", badge: "AUTOMATED WELCOME SEQUENCE", h1: "5 PLAIN-TEXT EMAILS", h2: "$6.80 SUBSCRIBER LTV", sub: "Install the 5-day automated onboarding sequence that sells while you sleep", metric: "49.4% OPEN | 6.2% CVR" }},
      {{ id: "sw17", label: "17. [Pre-Sale Gate] $14K Before Building (M = 4.7x)", badge: "15-ORDER VALIDATION GATE", h1: "PRE-SELL FIRST", h2: "NEVER BUILD UNSOLD PRODUCTS", sub: "Validate demand with 15+ Founding Member pre-orders before building Module 2", metric: "14-DAY LAUNCH RUNBOOK" }},
      {{ id: "sw18", label: "18. [Checkout Stack] +41% Instant Cart Value (M = 3.9x)", badge: "ORDER BUMP + 1-CLICK UPSELL", h1: "+41% MORE REVENUE", h2: "FROM THE SAME TRAFFIC", sub: "How a $19 Order Bump and $79 1-Click Upsell lift $49 base orders to $68.86", metric: "AOV LIFT: 1.41X BASE" }},
      {{ id: "sw19", label: "19. [B2B Sponsors] Charge $3,200 With 20K Subs (M = 4.9x)", badge: "OUTCOME SPONSORSHIP PRICING", h1: "KILL $25 CPM ADS", h2: "SELL $3,200 B2B BUNDLES", sub: "Bundle YouTube workflow demos, newsletter slots & paid-ad whitelisting rights", metric: "TIER B PACKAGE: $3,200" }},
      {{ id: "sw20", label: "20. [Contract Shield] +30%/Mo Ad Whitelisting (M = 3.6x)", badge: "CREATOR IP & USAGE SHIELD", h1: "+30% USAGE FEE", h2: "PROTECT YOUR IP RIGHTS", sub: "The 2 contract clauses that ban AI cloning and monetize paid-social dark ads", metric: "50% DEPOSIT + NET-15" }},
      {{ id: "sw21", label: "21. [Friday CEO] 20-Minute Weekly CEO Audit (M = 3.8x)", badge: "FRIDAY 2:00 PM EXECUTIVE CADENCE", h1: "20-MIN CEO REVIEW", h2: "SCALE WITHOUT BURNOUT", sub: "Audit 5 stage-gate KPIs, send 5 sponsor pitches & prune 1 low-RPPH task", metric: "25-HR CEILING LOCKED" }},
      {{ id: "sw22", label: "22. [Make/n8n Flows] 5 No-Code Automations (M = 4.5x)", badge: "14-AUTOMATION-BLUEPRINTS", h1: "5 AI WORKFLOWS", h2: "SAVE 8 HOURS EVERY WEEK", sub: "Connect Notion, Claude/GPT, YouTube & your ESP for under $12/month", metric: "JSON BLUEPRINTS READY" }},
      {{ id: "sw23", label: "23. [BD Global Rail] Sell Globally From Dhaka (M = 4.1x)", badge: "GLOBAL + LOCAL PAYMENT RAILS", h1: "GLOBAL USD + BKASH", h2: "DUAL CHECKOUT ARCHITECTURE", sub: "Combine LemonSqueezy/Gumroad/Payoneer with local bKash/Nagad rails", metric: "100% BORDERLESS OS" }},
      {{ id: "sw24", label: "24. [Complete OS] Flagship Tier 3 & 4 Vault (M = 5.0x)", badge: "FLAGSHIP PRODUCT #3 COMPLETE EDITION", h1: "THE AI CREATOR", h2: "& SOLOPRENEUR OS V2.0", sub: "10-Chapter Manual + Web App + 8-Tab Excel + 7 Word Docs + 3 PPTX + 5 JSONs", metric: "ALL 9 PHASES VERIFIED" }}
    ];

    const CAROUSEL_SLIDE_PRESETS = [
      {{ id: "cs01", label: "Slide 01 · Bold Contrarian Cover Hook", badge: "SLIDE 01 OF 08 · STOP THE SCROLL", h1: "THE 4-HOUR CREATOR", h2: "OPERATING SYSTEM", sub: "How solo operators replace 35 hours of manual grind with a 5-stage pipeline (Swipe ->)", metric: "SWIPE FOR BLUEPRINT ->" }},
      {{ id: "cs02", label: "Slide 02 · The $8.11/Hr Treadmill Math", badge: "SLIDE 02 OF 08 · THE PROBLEM", h1: "35 HOURS A WEEK", h2: "AT $8.11 PER HOUR", sub: "88% of creators burn out inside 18 months because they optimize for vanity views over RPPH", metric: "STAGE 01 DIAGNOSTIC" }},
      {{ id: "cs03", label: "Slide 03 · P.A.I.D. Niche Selection Gate", badge: "SLIDE 03 OF 08 · NICHE ECONOMICS", h1: "SCORE YOUR NICHE", h2: "NMPI >= 75 / 100 GATE", sub: "Weight Pain (2.5x) + Affluence (3.0x) + Intent (2.5x) + Distribution (2.0x) before launching", metric: "STAGE 01 POSITIONING" }},
      {{ id: "cs04", label: "Slide 04 · S.I.G.N.A.L. Outlier Validation", badge: "SLIDE 04 OF 08 · DEMAND PROOF", h1: "OUTLIER M >= 2.5X", h2: "NEVER GUESS TOPICS", sub: "Only script topics that already beat a peer channel's 90-day median views by 2.5x+", metric: "STAGE 01 VALIDATION" }},
      {{ id: "cs05", label: "Slide 05 · C.L.I.P. + H.E.A.R.T. Scripting", badge: "SLIDE 05 OF 08 · HIGH RETENTION", h1: "70%+ 30-SEC HOLD", h2: "& 90S PATTERN RESETS", sub: "Confirm click promise in 5s, flash visual proof by 18s, and reset visuals every 90s", metric: "STAGE 02 SCRIPTING" }},
      {{ id: "cs06", label: "Slide 06 · 1-to-15 Repurposing Waterfall", badge: "SLIDE 06 OF 08 · OMNICHANNEL", h1: "1 PILLAR SCRIPT", h2: "-> 15 NATIVE ASSETS", sub: "Extract 5 Shorts, 2 LinkedIn posts, 2 X assets, 3 Carousels & 2 Newsletters every Tuesday", metric: "STAGE 03 ATOMIZATION" }},
      {{ id: "cs07", label: "Slide 07 · 45% Opt-In + 4-Tier Ladder", badge: "SLIDE 07 OF 08 · MONETIZATION", h1: "OWN YOUR AUDIENCE", h2: "$150–$450+ BLENDED RPM", sub: "Route rented views into a 5-Minute Utility Lead Magnet, 5-Day Sequence & $49-$149 Offers", metric: "STAGES 04 & 05" }},
      {{ id: "cs08", label: "Slide 08 · Action CTA & Free Audit Kit", badge: "SLIDE 08 OF 08 · IMPLEMENTATION", h1: "DOWNLOAD THE FREE", h2: "7-DAY RPPH AUDIT KIT", sub: "Grab Worksheet 01 + Chapter 1 + The Interactive RPPH Calculator via the link in bio/comments", metric: "LINK IN FIRST COMMENT" }}
    ];

    let activePresetId = PRESETS[0].id;
    let uploadedImageDataUri = null;
    let squintTestActive = false;

    function escapeXml(unsafe) {{
      return String(unsafe || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&apos;');
    }}

    function wrapSvgText(text, maxCharsPerLine) {{
      const words = String(text || '').split(/\\s+/);
      const lines = [];
      let current = '';
      words.forEach(w => {{
        if ((current + ' ' + w).trim().length <= maxCharsPerLine) {{
          current = (current + ' ' + w).trim();
        }} else {{
          if (current) lines.push(current);
          current = w;
        }}
      }});
      if (current) lines.push(current);
      return lines.slice(0, 4);
    }}

    function initControls() {{
      const selPreset = document.getElementById('sel-preset');
      const chipsBar = document.getElementById('preset-chips-bar');
      selPreset.innerHTML = '';
      chipsBar.innerHTML = '';

      PRESETS.forEach((p, idx) => {{
        const opt = document.createElement('option');
        opt.value = p.id;
        opt.textContent = p.name;
        selPreset.appendChild(opt);

        const chip = document.createElement('button');
        chip.className = 'preset-chip' + (idx === 0 ? ' active' : '');
        chip.id = 'chip-' + p.id;
        chip.textContent = p.name.replace(/^\\d+\\.\\s*/, '');
        chip.onclick = () => {{
          selPreset.value = p.id;
          onPresetChange(p.id);
        }};
        chipsBar.appendChild(chip);
      }});

      const selTheme = document.getElementById('sel-theme');
      selTheme.innerHTML = '';
      THEMES.forEach(t => {{
        const opt = document.createElement('option');
        opt.value = t.id;
        opt.textContent = t.name;
        selTheme.appendChild(opt);
      }});

      const selSwipe = document.getElementById('sel-swipe');
      if (selSwipe) {{
        selSwipe.innerHTML = '';
        PACKAGING_SWIPES.forEach(sw => {{
          const opt = document.createElement('option');
          opt.value = sw.id;
          opt.textContent = sw.label;
          selSwipe.appendChild(opt);
        }});
      }}

      const selCarousel = document.getElementById('sel-carousel-slide');
      if (selCarousel) {{
        selCarousel.innerHTML = '';
        CAROUSEL_SLIDE_PRESETS.forEach(cs => {{
          const opt = document.createElement('option');
          opt.value = cs.id;
          opt.textContent = cs.label;
          selCarousel.appendChild(opt);
        }});
      }}

      loadPresetIntoInputs(PRESETS[0]);
      renderStudioSvg();
    }}

    function applyPackagingSwipe(swipeId) {{
      const sw = PACKAGING_SWIPES.find(x => x.id === swipeId);
      if (!sw) return;
      document.getElementById('inp-badge').value = sw.badge;
      document.getElementById('inp-h1').value = sw.h1;
      document.getElementById('inp-h2').value = sw.h2;
      document.getElementById('inp-sub').value = sw.sub;
      document.getElementById('inp-metric').value = sw.metric;
      renderStudioSvg();
    }}

    function applyCarouselSlidePreset(slideId) {{
      const cs = CAROUSEL_SLIDE_PRESETS.find(x => x.id === slideId);
      if (!cs) return;
      const selPreset = document.getElementById('sel-preset');
      if (selPreset && selPreset.value !== 'social-carousel') {{
        selPreset.value = 'social-carousel';
        onPresetChange('social-carousel');
      }}
      document.getElementById('inp-badge').value = cs.badge;
      document.getElementById('inp-h1').value = cs.h1;
      document.getElementById('inp-h2').value = cs.h2;
      document.getElementById('inp-sub').value = cs.sub;
      document.getElementById('inp-metric').value = cs.metric;
      renderStudioSvg();
    }}

    function toggleMobileSquintTest() {{
      squintTestActive = !squintTestActive;
      const mount = document.getElementById('svg-mount');
      if (squintTestActive) {{
        mount.style.transform = 'scale(0.24)';
        mount.style.filter = 'blur(0.6px)';
        mount.style.transition = 'all 0.25s ease';
      }} else {{
        mount.style.transform = 'scale(1)';
        mount.style.filter = 'none';
      }}
    }}

    function loadPresetIntoInputs(p) {{
      document.getElementById('inp-badge').value = p.badge;
      document.getElementById('inp-h1').value = p.headline1;
      document.getElementById('inp-h2').value = p.headline2;
      document.getElementById('inp-sub').value = p.subtitle;
      document.getElementById('inp-metric').value = p.metricPill;
      document.getElementById('inp-author').value = p.author;
      document.getElementById('meta-preset-name').textContent = p.name;
      document.getElementById('meta-dims').textContent = p.width + ' × ' + p.height + ' px';
    }}

    function onPresetChange(presetId) {{
      activePresetId = presetId;
      const p = PRESETS.find(x => x.id === presetId) || PRESETS[0];
      document.querySelectorAll('.preset-chip').forEach(c => {{
        c.classList.toggle('active', c.id === 'chip-' + presetId);
      }});
      loadPresetIntoInputs(p);
      renderStudioSvg();
    }}

    function resetCurrentPreset() {{
      onPresetChange(activePresetId);
    }}

    function onThemeChange(themeId) {{
      const t = THEMES.find(x => x.id === themeId) || THEMES[0];
      document.getElementById('col-bg1').value = t.bg1;
      document.getElementById('col-accent').value = t.accent;
      document.getElementById('col-sec').value = t.secondary;
      renderStudioSvg();
    }}

    function handleLogoUpload(ev) {{
      const file = ev.target.files && ev.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(e) {{
        uploadedImageDataUri = e.target.result;
        renderStudioSvg();
      }};
      reader.readAsDataURL(file);
    }}

    function clearUploadedLogo() {{
      uploadedImageDataUri = null;
      document.getElementById('inp-logo').value = '';
      renderStudioSvg();
    }}

    function buildCurrentSvgMarkup() {{
      const p = PRESETS.find(x => x.id === activePresetId) || PRESETS[0];
      const W = p.width;
      const H = p.height;
      const bg1 = document.getElementById('col-bg1').value || '#0F172A';
      const accent = document.getElementById('col-accent').value || '#4F46E5';
      const sec = document.getElementById('col-sec').value || '#2DD4BF';
      const layout = document.getElementById('sel-layout').value || 'grid-glow';
      const scale = (parseFloat(document.getElementById('inp-scale').value) || 100) / 100.0;

      const badge = escapeXml(document.getElementById('inp-badge').value);
      const h1 = escapeXml(document.getElementById('inp-h1').value);
      const h2 = escapeXml(document.getElementById('inp-h2').value);
      const subRaw = document.getElementById('inp-sub').value;
      const metric = escapeXml(document.getElementById('inp-metric').value);
      const author = escapeXml(document.getElementById('inp-author').value);

      // Grid lines
      const step = Math.round(Math.min(W, H) / 10);
      let gridLines = '';
      for (let x = 0; x <= W; x += step) {{
        gridLines += `<line x1="${{x}}" y1="0" x2="${{x}}" y2="${{H}}" stroke="#334155" stroke-width="1" opacity="0.32" />`;
      }}
      for (let y = 0; y <= H; y += step) {{
        gridLines += `<line x1="0" y1="${{y}}" x2="${{W}}" y2="${{y}}" stroke="#334155" stroke-width="1" opacity="0.32" />`;
      }}

      let layoutDecor = '';
      if (layout === 'split-contrast') {{
        layoutDecor = `<rect x="${{Math.round(W * 0.58)}}" y="0" width="${{Math.round(W * 0.42)}}" height="${{H}}" fill="${{accent}}" opacity="0.18" />
                       <line x1="${{Math.round(W * 0.58)}}" y1="0" x2="${{Math.round(W * 0.58)}}" y2="${{H}}" stroke="${{sec}}" stroke-width="4" />`;
      }} else if (layout === 'executive-frame') {{
        layoutDecor = `<rect x="36" y="36" width="${{W - 72}}" height="${{H - 72}}" rx="18" fill="none" stroke="${{accent}}" stroke-width="4" />
                       <rect x="52" y="52" width="${{W - 104}}" height="${{H - 104}}" rx="12" fill="none" stroke="${{sec}}" stroke-width="1.5" opacity="0.7" />`;
      }} else if (layout === 'blueprint-matrix') {{
        layoutDecor = `<circle cx="${{W - 140}}" cy="140" r="90" fill="none" stroke="${{sec}}" stroke-width="2" stroke-dasharray="8,6" opacity="0.5" />
                       <circle cx="140" cy="${{H - 140}}" r="90" fill="none" stroke="${{accent}}" stroke-width="2" stroke-dasharray="8,6" opacity="0.5" />`;
      }}

      const isPortrait = H > W * 1.15;
      const baseTitleSize = Math.round((isPortrait ? W * 0.068 : W * 0.058) * scale);
      const subFontSize = Math.round(isPortrait ? W * 0.024 : W * 0.021);
      const badgeHeight = Math.round(H * 0.065);
      const padX = Math.round(W * 0.065);

      const subLines = wrapSvgText(subRaw, isPortrait ? 44 : 62);
      const subYStart = Math.round(H * 0.52);
      const subTspans = subLines.map((ln, idx) =>
        `<text x="${{padX}}" y="${{subYStart + idx * Math.round(subFontSize * 1.45)}}" fill="#CBD5E1" font-size="${{subFontSize}}" font-weight="500">${{escapeXml(ln)}}</text>`
      ).join('\\n  ');

      let logoMarkup = '';
      if (uploadedImageDataUri) {{
        const logoSize = Math.round(Math.min(W, H) * 0.22);
        logoMarkup = `<image href="${{uploadedImageDataUri}}" x="${{W - padX - logoSize}}" y="${{Math.round(H * 0.16)}}" width="${{logoSize}}" height="${{logoSize}}" preserveAspectRatio="xMidYMid slice" />`;
      }}

      // 3 Architecture Mini-Cards above footer
      const cardsY = Math.round(H * 0.69);
      const cardH = Math.round(H * 0.13);
      const cardW = Math.round((W - padX * 2 - 32) / 3);
      const miniCards = [
        ['STAGE 1–2: VALIDATE', 'Outlier M >= 2.5x | 70% Hold', accent],
        ['STAGE 3: MULTIPLY', '1 Pillar -> 15 Native Assets', sec],
        ['STAGE 4–5: MONETIZE', '45% Opt-In | +45% Checkout AOV', '#F59E0B']
      ].map((c, i) => {{
        const cx = padX + i * (cardW + 16);
        return `<rect x="${{cx}}" y="${{cardsY}}" width="${{cardW}}" height="${{cardH}}" rx="10" fill="#1E293B" stroke="${{c[2]}}" stroke-width="2" />
                <text x="${{cx + 18}}" y="${{cardsY + Math.round(cardH * 0.42)}}" fill="${{c[2]}}" font-size="${{Math.round(subFontSize * 0.78)}}" font-weight="800" font-family="'JetBrains Mono', monospace">${{c[0]}}</text>
                <text x="${{cx + 18}}" y="${{cardsY + Math.round(cardH * 0.76)}}" fill="#F8FAFC" font-size="${{Math.round(subFontSize * 0.82)}}" font-weight="700">${{c[1]}}</text>`;
      }}).join('\\n  ');

      return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${{W}} ${{H}}" width="${{W}}" height="${{H}}" font-family="'Inter', 'Segoe UI', sans-serif">
  <defs>
    <linearGradient id="st-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="${{bg1}}" />
      <stop offset="100%" stop-color="#090D16" />
    </linearGradient>
    <radialGradient id="st-glow" cx="35%" cy="35%" r="60%">
      <stop offset="0%" stop-color="${{accent}}" stop-opacity="0.34" />
      <stop offset="100%" stop-color="${{bg1}}" stop-opacity="0" />
    </radialGradient>
  </defs>

  <rect x="0" y="0" width="${{W}}" height="${{H}}" fill="url(#st-bg)" />
  ${{gridLines}}
  <rect x="0" y="0" width="${{W}}" height="${{H}}" fill="url(#st-glow)" />
  ${{layoutDecor}}

  <!-- Outer Precision Border -->
  <rect x="20" y="20" width="${{W - 40}}" height="${{H - 40}}" rx="14" fill="none" stroke="#334155" stroke-width="2" />

  <!-- Top Authority Badge & Metric Pill -->
  <rect x="${{padX}}" y="${{Math.round(H * 0.08)}}" width="${{Math.round(W * 0.56)}}" height="${{badgeHeight}}" rx="8" fill="#1E293B" stroke="${{accent}}" stroke-width="2" />
  <text x="${{padX + 22}}" y="${{Math.round(H * 0.08 + badgeHeight * 0.64)}}" fill="#E2E8F0" font-size="${{Math.round(subFontSize * 0.85)}}" font-weight="800" letter-spacing="2">${{badge}}</text>

  <rect x="${{W - padX - Math.round(W * 0.28)}}" y="${{Math.round(H * 0.08)}}" width="${{Math.round(W * 0.28)}}" height="${{badgeHeight}}" rx="8" fill="${{sec}}" />
  <text x="${{W - padX - Math.round(W * 0.14)}}" y="${{Math.round(H * 0.08 + badgeHeight * 0.64)}}" fill="#090D16" font-size="${{Math.round(subFontSize * 0.88)}}" font-weight="900" font-family="'JetBrains Mono', monospace" text-anchor="middle">${{metric}}</text>

  <!-- Main Headlines -->
  <text x="${{padX}}" y="${{Math.round(H * 0.28)}}" fill="#FFFFFF" font-size="${{baseTitleSize}}" font-weight="900" letter-spacing="-1">${{h1}}</text>
  <text x="${{padX}}" y="${{Math.round(H * 0.39)}}" fill="${{sec}}" font-size="${{Math.round(baseTitleSize * 0.94)}}" font-weight="900" letter-spacing="-1">${{h2}}</text>

  <!-- Accent Divider -->
  <rect x="${{padX}}" y="${{Math.round(H * 0.43)}}" width="${{Math.round(W * 0.45)}}" height="6" rx="3" fill="${{accent}}" />

  <!-- Subtitle Lines -->
  ${{subTspans}}

  <!-- Optional Uploaded Logo / Headshot -->
  ${{logoMarkup}}

  <!-- 3 Stage-Gate Architecture Cards -->
  ${{miniCards}}

  <!-- Bottom Author / Imprint Footer Strip -->
  <rect x="${{padX}}" y="${{Math.round(H * 0.86)}}" width="${{W - padX * 2}}" height="${{Math.round(H * 0.075)}}" rx="10" fill="#090D16" stroke="#334155" stroke-width="2" />
  <text x="${{Math.round(W / 2)}}" y="${{Math.round(H * 0.86 + H * 0.048)}}" fill="#F8FAFC" font-size="${{Math.round(subFontSize * 0.88)}}" font-weight="800" font-family="'JetBrains Mono', monospace" letter-spacing="1.5" text-anchor="middle">${{author}}</text>
</svg>`;
    }}

    function renderStudioSvg() {{
      const svgMarkup = buildCurrentSvgMarkup();
      document.getElementById('svg-mount').innerHTML = svgMarkup;
    }}

    function exportEditableSvg() {{
      const svgMarkup = buildCurrentSvgMarkup();
      const blob = new Blob([svgMarkup], {{ type: 'image/svg+xml;charset=utf-8' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'creator-os-' + activePresetId + '-custom.svg';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }}

    function exportSVG() {{
      return exportEditableSvg();
    }}

    function exportHighResPng() {{
      const p = PRESETS.find(x => x.id === activePresetId) || PRESETS[0];
      const svgMarkup = buildCurrentSvgMarkup();
      const canvas = document.getElementById('export-canvas');
      canvas.width = p.width;
      canvas.height = p.height;
      const ctx = canvas.getContext('2d');

      const img = new Image();
      const svgBlob = new Blob([svgMarkup], {{ type: 'image/svg+xml;charset=utf-8' }});
      const url = URL.createObjectURL(svgBlob);
      img.onload = function() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        URL.revokeObjectURL(url);
        canvas.toBlob(function(pngBlob) {{
          const pngUrl = URL.createObjectURL(pngBlob);
          const a = document.createElement('a');
          a.href = pngUrl;
          a.download = 'creator-os-' + activePresetId + '-' + p.width + 'x' + p.height + '.png';
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(pngUrl);
        }}, 'image/png', 1.0);
      }};
      img.src = url;
    }}

    function exportPNG() {{
      return exportHighResPng();
    }}

    window.addEventListener('DOMContentLoaded', initControls);
  </script>
</body>
</html>
"""
    html_path.write_text(studio_html, encoding="utf-8")

    readme_md = r"""# Interactive Cover, YouTube Thumbnail & Social Card Customizer Studio — Operator Manual

> **Offline Graphic & Packaging Studio Documentation (`08-COVER-DESIGN/Editable-Design-Kit/README-DESIGN-KIT.md`)**
> * **Application File:** `08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html`
> * **Architecture:** 100% Offline Single-File HTML5 / SVG / Canvas Rasterization Engine (`Zero External CDN Dependencies`)
> * **Supported Export Formats:** Crisp High-Resolution Raster `.PNG` (via HTML5 `<canvas>`) and Editable Vector `.SVG`

---

## 1. Executive Overview & Why This Studio Exists

In Chapter 4 of *The AI Content Creator & Solopreneur Operating System*, we enforce the **Package-First Rule**: you never draft a line of your weekly Pillar Script until your **Title** and **3-Word Thumbnail Concept** are locked. However, many solo creators waste 2 to 4 hours every week wrestling with complex cloud design tools, hunting for templates, or paying monthly SaaS subscriptions just to produce a YouTube thumbnail, a LinkedIn carousel cover, or a digital product mockup.

**`design-customizer-studio.html`** eliminates that friction completely. Double-click the file on your computer to open a 100% offline, deterministic visual packaging studio pre-loaded with our locked **Creator Indigo, Deep Studio Navy, Conversion Teal & Retention Amber** brand tokens and six precision-sized canvas presets.

---

## 2. The 6 Built-In Commercial Canvas Format Presets

When you select a preset in **Panel 1 (`Canvas Format & Dimension Preset`)** or click one of the six quick-switch chips below the preview stage, the studio automatically reconfigures the SVG coordinate grid, typography hierarchy, and HTML5 export dimensions:

| Preset # | Canvas Format Name | Exact Pixel Dimensions | Aspect Ratio | Primary Creator & Solopreneur Use Case |
| :---: | :--- | :---: | :---: | :--- |
| **1** | **YouTube High-CTR Thumbnail** | `1280 × 720 px` | `16:9` HD | Monday Block 1 Package-First 3-Word Thumbnail creation |
| **2** | **Kindle / KDP eBook Cover** | `1600 × 2560 px` | `1:1.6` Portrait | Amazon KDP Kindle, Apple Books, Kobo & D2D front covers |
| **3** | **Gumroad Product Cover** | `1600 × 1000 px` | `16:10` Wide | Gumroad, Lemon Squeezy, Stan Store & Stripe checkout cards |
| **4** | **LinkedIn / IG Carousel Cover** | `1080 × 1350 px` | `4:5` Vertical | High-save 8-slide PDF carousels for LinkedIn and Instagram |
| **5** | **Newsletter Header Banner** | `1200 × 630 px` | `1.91:1` Social | Substack, Beehiiv, ConvertKit, and OpenGraph social link cards |
| **6** | **Lead Magnet Mockup Card** | `1200 × 900 px` | `4:3` Display | Opt-in landing page hero graphics for your 5-Minute Utility Magnet |

---

## 3. Step-by-Step Workflow: Designing & Exporting in Under 3 Minutes

### Step 1: Select Your Target Canvas & Visual Layout Architecture
1. Open `08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html` in Google Chrome, Microsoft Edge, Brave, Firefox, or Apple Safari.
2. In **Section 1**, choose your target preset (e.g., *YouTube High-CTR Thumbnail `1280 × 720 px`*).
3. Select one of the four **Visual Architecture Layout Styles**:
   * **Architectural Grid + Radial Glow:** Ideal for technical tutorials, system teardowns, and flagship product bundles.
   * **High-CTR Split Contrast Card:** Divides the right 42% of the frame with a bold accent border to create immediate visual contrast at mobile thumbnail sizes.
   * **Minimalist Executive Double-Frame:** Adds a dual-border book-imprint frame for Kindle covers and formal B2B reports.
   * **Technical Blueprint Matrix:** Adds dashed engineering fiducial rings for workflow and automation topics.

### Step 2: Customize Your 3-Word Hook, Headline & Quantitative Proof Pill
In **Section 2 (`Live Typography & Hook Copy`)**, edit any of the six live text fields. Every keystroke updates the vector canvas in real time:
* **Top Authority Badge:** Call out your S.I.G.N.A.L. outlier proof or edition tier (e.g., `OUTLIER MULTIPLIER: 4.3x VERIFIED`).
* **Primary Headline (Line 1) & Secondary Accent Headline (Line 2):** For YouTube thumbnails, keep Line 1 and Line 2 to **3 to 5 punchy words** (`35 HRS TO 4 HRS`). Use the **Headline Font Scale (`70%–135%`)** slider in Section 3 to maximize visual impact.
* **Quantitative Proof / Metric Callout Pill:** Displays in high-contrast monospace type in the top-right badge (`CTR: 9.4% | HOLD: 74%`).

### Step 3: Apply a 1-Click Color Theme or Upload Your Headshot/Logo
1. In **Section 3 (`Brand Palette & Custom Hex Colors`)**, switch instantly between six curated creator palettes (*Creator Indigo*, *Deep Studio Slate*, *Conversion Teal*, *Retention Amber*, *Emerald Authority*, or *Crimson Outlier*), or click the three native color pickers to input your exact brand hex codes.
2. In **Section 4 (`Custom Headshot / Brand Logo Overlay`)**, click **Choose File** to select any local PNG, JPG, or SVG headshot or brand icon from your computer. Using browser `FileReader` data-URI injection, your image is embedded 100% locally inside the canvas without ever uploading to an external server.

### Step 4: 1-Click High-Res `.PNG` & Editable Vector `.SVG` Export
* Click **`Download High-Res Raster (.PNG)`** in the top-right bar to rasterize the SVG onto an offscreen HTML5 `<canvas>` at exact native pixel resolution (`1280×720`, `1600×2560`, `1600×1000`, etc.) and save a crisp, lossless `.png` file directly to your `Downloads` folder.
* Click **`Download Editable Vector (.SVG)`** to save the clean, standards-compliant XML vector source file, which can be opened in Figma, Adobe Illustrator, Inkscape, or Canva for further vector customization.
"""
    readme_path.write_text(readme_md, encoding="utf-8")
    return html_path, readme_path


def run_office_and_studio() -> dict:
    print("=" * 90)
    print("PHASE 9 PART A: EDITABLE OFFICE SUITE (7 DOCX + 3 PPTX) & DESIGN CUSTOMIZER STUDIO")
    print("=" * 90)

    print("\n[UPGRADE 2] Building 7 Editable Microsoft Word (.docx) Documents...")
    docx_results = build_all_seven_docx_files()
    for path, wc in docx_results:
        print(f"  -> {path.relative_to(STUDIO_ROOT).as_posix()}: {wc:,} words ({path.stat().st_size:,} bytes)")

    print("\n[UPGRADE 3] Building 3 Widescreen 16:9 Editable PowerPoint (.pptx) Slide Decks...")
    pptx_results = build_all_three_pptx_decks()
    for path, sc in pptx_results:
        print(f"  -> {path.relative_to(STUDIO_ROOT).as_posix()}: {sc} slides ({path.stat().st_size:,} bytes)")

    print("\n[UPGRADE 5] Building Interactive Cover & Thumbnail Customizer Studio...")
    html_p, readme_p = build_design_customizer_studio()
    readme_wc = len(re.findall(r"\b\w+\b", readme_p.read_text(encoding="utf-8")))
    print(f"  -> {html_p.relative_to(STUDIO_ROOT).as_posix()} ({html_p.stat().st_size:,} bytes)")
    print(f"  -> {readme_p.relative_to(STUDIO_ROOT).as_posix()} ({readme_wc:,} words, {readme_p.stat().st_size:,} bytes)")

    return {
        "docx_files": {
            p.relative_to(STUDIO_ROOT).as_posix(): {"words": wc, "bytes": p.stat().st_size}
            for p, wc in docx_results
        },
        "pptx_files": {
            p.relative_to(STUDIO_ROOT).as_posix(): {"slides": sc, "bytes": p.stat().st_size}
            for p, sc in pptx_results
        },
        "design_studio": {
            "studio_html_path": html_p.relative_to(STUDIO_ROOT).as_posix(),
            "studio_html_bytes": html_p.stat().st_size,
            "readme_path": readme_p.relative_to(STUDIO_ROOT).as_posix(),
            "readme_words": readme_wc,
            "readme_bytes": readme_p.stat().st_size,
        },
    }


if __name__ == "__main__":
    run_office_and_studio()
    sys.exit(0)
