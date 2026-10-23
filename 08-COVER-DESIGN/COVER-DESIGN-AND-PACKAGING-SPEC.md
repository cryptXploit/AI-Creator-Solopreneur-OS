# Commercial Cover Suite & Amazon KDP Print Packaging Specification

> **Visual Packaging & Print Engineering Manual (`08-COVER-DESIGN/COVER-DESIGN-AND-PACKAGING-SPEC.md`)**
> * **Product ID:** `PRODUCT-03-AI-CREATOR-SOLOPRENEUR-OS`
> * **Title:** *The AI Content Creator & Solopreneur Operating System*
> * **Locked Interior Page Count (`6" × 9"` KDP Paperback):** `314 pages` (Verified from `PROJECT_STATE.json`)
> * **Calculated White-Paper Spine Width:** `0.707128 in` (`17.96 mm`)
> * **Full-Wrap Print Dimensions (With `0.125"` Bleed):** `12.957128 in × 9.250 in` (`932.91 pt × 666.00 pt` / `3887 px × 2775 px` at `300 DPI`)

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

### 2.1 Step-by-Step Spine & Full-Wrap Derivation (`314` Pages)

Using the locked Phase 5 monochrome interior PDF (`09-EXPORTS/PRINT/the-ai-creator-solopreneur-os-kdp-paperback-6x9.pdf` at **`314 pages`**), `build_phase7.py` computes the exact KDP white-paper full-wrap geometry:

1. **Selected Trim Size ($W_{\text{trim}} \times H_{\text{trim}}$):**
   * Front & Back Cover Width: `6.000 in` (`152.40 mm` / `432.00 pt` / `1800 px` at `300 DPI`)
   * Front & Back Cover Height: `9.000 in` (`228.60 mm` / `648.00 pt` / `2700 px` at `300 DPI`)
2. **Amazon KDP White-Paper Spine Thickness Multiplier ($k_{\text{white}}$):**
   * Standard KDP B&W White Paper (`55 lb / 90 gsm`) thickness factor: `0.002252 in/page` (`0.0572 mm/page`)
3. **Calculated Spine Width ($W_{\text{spine}}$):**
   $$W_{\text{spine}} = 314 \times 0.002252\text{ in} = 0.707128\text{ in} \quad (17.96\text{ mm} \text{ / } 50.91\text{ pt} \text{ / } 211\text{ px at 300 DPI})$$
4. **Outside Edge Bleed ($B$):**
   * Top, Bottom, Left (Back Cover outer edge), and Right (Front Cover outer edge): `0.125 in` (`3.175 mm` / `9.00 pt` / `38 px` at `300 DPI`)
5. **Total Full-Wrap Cover Width ($W_{\text{total}}$):**
   $$W_{\text{total}} = 0.125 + 6.000 + 0.707128 + 6.000 + 0.125 = 12.957128\text{ in} \quad (932.91\text{ pt} \text{ / } 3887\text{ px at 300 DPI})$$
6. **Total Full-Wrap Cover Height ($H_{\text{total}}$):**
   $$H_{\text{total}} = 0.125 + 9.000 + 0.125 = 9.250\text{ in} \quad (666.00\text{ pt} \text{ / } 2775\text{ px at 300 DPI})$$

### 2.2 KDP Margin Safe Zones, Spine Hinge & Barcode Placement Rules

| Cover Zone | X-Coordinate Range (`300 DPI px`) | Physical Dimension | KDP Pre-Flight Safety Rule Enforced |
| :--- | :---: | :---: | :--- |
| **Left Outer Bleed** | `0 px – 38 px` | `0.125 in` | Background artwork extends to `0 px`; zero text within `0.25 in` (`75 px`) of trim |
| **Back Cover Panel** | `38 px – 1838 px` | `6.000 in × 9.000 in` | Contains 5-stage executive summary, vault checklist, and lower-right Barcode Safe Zone |
| **KDP ISBN Barcode Box** | `1118 px – 1718 px` (`Y: 2180–2540`) | `2.000 in × 1.200 in` | Pure `#FFFFFF` solid rectangle reserved `0.40 in` inside bottom/spine trim edges |
| **Center Spine Panel** | `1838 px – 2049 px` (`CX: 1943 px`) | `0.7071 in × 9.000 in` | Rotated `90°` clockwise title text (`30px`, `0.10 in` height) with `> 0.0625 in` hinge clearance |
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
