# APEX DIGITAL SYSTEMS STUDIO — MASTER EDITORIAL, TYPOGRAPHIC & DESIGN STYLE GUIDE

* **Product ID:** `PRODUCT-03-AI-CREATOR-SOLOPRENEUR-OS`
* **Title:** *The AI Content Creator & Solopreneur Operating System*
* **Subtitle:** *A Practical System to Research Validated Ideas, Script High-Retention Content, Repurpose Across Platforms, Automate Production, and Monetize Your Audience Without Burnout*
* **Imprint:** Apex Digital Systems Studio
* **Version:** `1.0.0` (Locked Baseline)

---

## 1. EDITORIAL PHILOSOPHY & VOICE ARCHITECTURE

This operating system manual is engineered for solo content creators, newsletter operators, educator-entrepreneurs, and lean digital media founders who treat content creation as a high-margin software and media business rather than a speculative hobby. Every paragraph, table, formula, and workflow diagram must operate as an executable Standard Operating Procedure (SOP).

### 1.1 Core Voice Mandates
1. **Direct, Quantitative, and Mechanistic:** Address the reader in the second person (`you`, `your studio`, `your production pipeline`). Replace vague motivational advice with explicit numbers, time-study benchmarks, conversion percentages, and dollar-per-hour calculations.
2. **Evidence-Backed Assertions:** Every claim regarding audience retention, click-through rate (CTR), email capture velocity, newsletter sponsorship pricing, or digital product conversion must trace directly to documented industry research in `01-MARKET-RESEARCH/sources.md`.
3. **Zero Motivational Filler:** Do not open chapters with generic commentary on how fast technology is changing. Open immediately with the operational friction point, the cost of inaction in hours and dollars, and the exact mechanism that resolves it.
4. **Operator Vocabulary:** Prefer precise operational nouns and verbs: *pipeline, throughput, retention curve, curiosity gap, conversion bridge, revenue per production hour (RPPH), batch sprint, outlier multiplier, offer architecture, attribution gate, and unit economics*.

---

## 2. LOCKED COLOR & TYPOGRAPHY PALETTE (CREATOR INDIGO, VIOLET & SLATE THEME)

All visual assets, stylesheets, HTML interactive tools, printable worksheets, and vector SVG diagrams across directories `01` through `14` must strictly adhere to the following color tokens and typographic hierarchy.

### 2.1 Hex Color Token Registry

| CSS / SVG Token | Hex Code | Role & Visual Application Rules | Print & Contrast Constraint |
| :--- | :--- | :--- | :--- |
| `--primary` | `#0F172A` | Deep Studio Navy/Slate. Used for H1/H2 headers, structural borders, table header text or outlines, and primary SVG diagram frames. | 17.4:1 contrast on `#FFFFFF`. Safe for CMYK and grayscale KDP printing. |
| `--accent` | `#4F46E5` | Creator Indigo. Used for H3 subheadings, primary workflow arrows, active stage badges, callout left-borders, and interactive CTAs. | 6.2:1 contrast on `#FFFFFF`. Distinguishable in grayscale via stroke weight. |
| `--secondary` | `#0D9488` | Conversion Teal. Reserved for monetization gates, verification highlights, positive ROI indicators, and revenue nodes. | 3.9:1 graphical contrast; pair with `#0F172A` text or bold white labels. |
| `--warning` | `#D97706` | Retention Amber. Reserved for hook retention gates, algorithm drop-off checkpoints, and time-leak alerts. | High visibility alert accent; pair with dark `#0F172A` text on light `#FFFBEB` tint. |
| `--text` | `#1E293B` | High-Contrast Slate. Standard body prose, table cells, list items, and worksheet instructions. | 14.6:1 contrast ratio on pure white canvas. |
| `--muted` | `#64748B` | Muted Slate. Figure captions, running headers, running footers, metadata labels, and form field hints. | 4.8:1 contrast ratio on `#FFFFFF` (WCAG AA compliant). |
| `--bg` | `#FFFFFF` | Pure White Canvas. Mandatory background for all print pages, worksheets, and SVG diagrams. | Zero dark ink-heavy full-bleed background boxes permitted in print layouts. |

### 2.2 Typography & Sizing Floors
* **Primary Sans-Serif (`Inter` / `Noto Sans`):**
  * Used for all headings (`H1` through `H4`), body prose, tables, callout boxes, and SVG node labels.
  * **Body Prose Floor:** Minimum `10.5pt` in print (`6x9in` KDP and `8.5x11in` US Letter) with `1.55` line-height.
  * **Table & Prompt Metadata Floor:** Minimum `9.5pt` with `6pt 8pt` internal cell padding so multi-column tables never clip or wrap single words across three lines.
  * **Caption, Header & Footer Floor:** Minimum `8.5pt` set in `--muted` (`#64748B`).
* **Monospace (`JetBrains Mono`):**
  * Used exclusively for copy-paste AI prompt templates, `[BRACKETED_INPUT_VARIABLES]`, automation JSON keys, file directory trees, and inline mathematical variables.
  * **Monospace Floor:** Minimum `9.5pt` with `1.45` line-height and light `#F8FAFC` background shading bordered by `1px solid #E2E8F0`.

---

## 3. MANDATORY 14-PART STUDIO CHAPTER SCHEMA

Every chapter in `03-MANUSCRIPT/` (`chapter-01.md` through `chapter-10.md`) must contain at least **6,500 words** and follow the exact 14-section architectural sequence below. No section may be omitted, reordered, or merged.

1. **Section 1: Title & Chapter Metadata Header**
   * Displays Chapter Number, Title, Part Assignment, Estimated Implementation Time (in hours), Core Operational Metric, Primary Framework Name, and Deliverable Outcome.
2. **Section 2: Learning Objectives**
   * Presents exactly 5 concrete, measurable operational outcomes starting with action verbs (*Calculate, Architect, Deploy, Audit, Automate*).
3. **Section 3: The Real-World Friction Point**
   * Diagnoses the specific operational bottleneck solo creators face at this stage of the pipeline. Includes a quantitative time-study or cost-of-friction breakdown table.
4. **Section 4: Why Standard Approaches Fail**
   * Critiques conventional creator advice (e.g., high-volume daily posting without validation, generic one-shot prompting, AdSense-only monetization) using empirical retention and RPM data.
5. **Section 5: Core Framework & Mathematical Model**
   * Introduces the chapter's named methodology and its governing mathematical equation (formatted in LaTeX block math `$$...$$`), accompanied by variable definitions and a benchmark comparison table contrasting an unsystematized creator against a systematized operator.
6. **Section 6: Visual Architecture — System Mindmap**
   * Embeds the chapter's first vector diagram (`../04-VISUAL-ASSETS/svg/chapter-XX-mindmap.svg`) and provides a node-by-node architectural walkthrough explaining how information, assets, and revenue flow across the framework.
7. **Section 7: Step-by-Step Implementation Protocol**
   * Delivers a chronological, multi-day or multi-stage installation SOP. Includes exact time allocations, directory structures, quality gates, and execution tables.
8. **Section 8: Operational Decision Tree**
   * Embeds the chapter's second vector diagram (`../04-VISUAL-ASSETS/svg/chapter-XX-flowchart.svg`) and defines the exact quantitative IF/THEN routing rules for troubleshooting underperforming metrics.
9. **Section 9: Tested AI Workflow Prompts (5 Prompts Per Chapter)**
   * Provides 5 production-tested, copy-paste AI prompts (`P01`–`P50` sequentially across the 10 chapters). Every prompt block must contain:
     * `PROMPT ID & TITLE`
     * `ROLE`
     * `CONTEXT`
     * `INPUT VARIABLES` (using `[UPPERCASE_BRACKETED_TOKENS]`)
     * `EXECUTION STEPS`
     * `QUALITY CONSTRAINTS`
     * `OUTPUT TEMPLATE`
10. **Section 10: Real-World Implementation Case Study**
    * Documents a named solo creator or lean operator archetype with realistic baseline metrics, exact intervention steps across a 30-to-90-day window, and a detailed Before vs. After financial and time-allocation table.
11. **Section 11: Common Operational Pitfalls & Fixes Table**
    * A structured 4-column Markdown table detailing at least 6 failure modes: *Pitfall Name*, *Root Operational Cause*, *Early Warning Metric*, and *Immediate Corrective Protocol*.
12. **Section 12: Chapter Action Worksheet Summary**
    * Summarizes the exercises, diagnostic tables, and scoring rubrics inside the companion workbook file (`../05-WORKBOOKS/markdown/worksheet-XX.md`) so the reader knows how to complete the hands-on audit.
13. **Section 13: Executive Summary & Implementation Checklist**
    * Provides a 10-point binary verification checklist (`[ ]`) with explicit numerical pass/fail criteria that must be satisfied before advancing to the next chapter.
14. **Section 14: Sources & Operational References**
    * Lists 6 or more formal citations with specific data takeaways mapped directly to entries in `01-MARKET-RESEARCH/sources.md`.

---

## 4. VECTOR SVG DIAGRAMMING STANDARDS (`04-VISUAL-ASSETS/svg/`)

Every chapter requires two bespoke vector diagrams: a **System Mindmap** (`chapter-XX-mindmap.svg`) and an **Operational Decision Tree / Flowchart** (`chapter-XX-flowchart.svg`).

### 4.1 Technical XML & Geometry Rules
* **Canvas Dimensions:** Every SVG root element must declare `xmlns="http://www.w3.org/2000/svg"`, `viewBox="0 0 900 480"`, `width="900"`, and `height="480"`.
* **Pure White Background:** The first visual child inside `<svg>` must be a full-canvas background rectangle (`<rect width="900" height="480" fill="#FFFFFF"/>`) or bordered studio frame so the graphic renders cleanly in dark-mode PDF readers and E-Ink devices.
* **Typography & Legibility:** All `<text>` nodes must specify `font-family="Inter, 'Noto Sans', sans-serif"` (or `'JetBrains Mono', monospace` for formula badges). Minimum font size is `10px` for secondary annotations and `12px`–`16px` for node titles.
* **Collision Prevention:** Every text string must fit comfortably inside its enclosing `<rect>` or `<g>` container with at least `10px` horizontal padding. Multi-line labels must use explicit `<tspan>` elements or separate `<text>` y-coordinates spaced at least `15px` apart.
* **Color Coding by Function:**
  * Central hubs and primary structural headers: `#0F172A` fill with `#FFFFFF` text, or `#F8FAFC` fill with `2px` `#0F172A` stroke.
  * Active process stages and directional connectors: `#4F46E5` stroke/fill accents.
  * Retention/algorithm evaluation gates (diamonds or amber badges): `#D97706` stroke with `#FFFBEB` fill and `#0F172A` text.
  * Monetization, conversion, and target RPPH output nodes: `#0D9488` stroke with `#F0FDFA` fill and `#0F172A` or `#0D9488` bold text.
* **File Size & Structural Richness:** Each SVG must be a genuine multi-node architectural diagram (`>= 3,000 bytes`) that parses with zero errors under Python's `xml.etree.ElementTree`.

---

## 5. ACTION WORKBOOK STANDARDS (`05-WORKBOOKS/markdown/`)

Each chapter is paired with a standalone, printable and fillable-ready Markdown workbook (`worksheet-01.md` through `worksheet-10.md`), containing at least **1,500 words**.

1. **Self-Contained Utility:** A reader printing only `worksheet-XX.md` must have all required formulas, scoring thresholds, step-by-step instructions, and structured input tables needed to execute the audit without flipping back to the main textbook.
2. **Fillable Grid Design:** Use Markdown tables with clear input columns (`[ ________ ]`), checkbox rows (`[ ]`), baseline vs. 30-day target columns, and explicit row-by-row calculation formulas.
3. **Stage-Gate Sign-Off:** Conclude every worksheet with a formal *Operator Sign-Off & Target Commitment Block* recording baseline metrics, 30-day targets, and the specific calendar date for the next review.

---

## 6. STRICT ANTI-CLICHÉ, BANNED-WORD & PLACEHOLDER FILTER

To preserve executive authority and pass automated studio quality assurance (`verify_phase1.py`), **zero files** across directories `01` through `14` may contain any prohibited AI-cliché terms or unresolved narrative placeholders.

### 6.1 Prohibited Single Words (Case-Insensitive)
Never use any of the following words (shown here with dot separators so this style guide itself remains 100% clean during automated full-repo scanning):
* `d.e.l.v.e` (use *examine, analyze, inspect, break down*)
* `t.a.p.e.s.t.r.y` (use *system, architecture, matrix, network*)
* `t.e.s.t.a.m.e.n.t` (use *evidence, proof, indicator, validation*)
* `b.e.a.c.o.n` (use *signal, benchmark, reference point, standard*)
* `s.y.m.p.h.o.n.y` (use *sequence, coordination, pipeline, synchronization*)
* `u.n.l.o.c.k` (use *activate, access, enable, open, release* — applies to prose, headers, and UI button labels alike)
* `u.n.l.e.a.s.h` (use *deploy, launch, execute, activate*)
* `s.k.y.r.o.c.k.e.t` (use *multiply, compound, increase, accelerate*)
* `s.u.p.e.r.c.h.a.r.g.e` (use *optimize, accelerate, amplify, upgrade*)
* `g.a.m.e-c.h.a.n.g.e.r` (use *high-impact shift, structural advantage, operational multiplier*)
* `p.i.v.o.t.a.l` (use *critical, decisive, central, foundational*)
* `r.e.a.l.m` (use *domain, sector, category, environment*)
* `f.o.s.t.e.r` (use *build, cultivate, establish, generate*)
* `u.n.d.e.r.s.c.o.r.e` (use *demonstrate, confirm, highlight, emphasize*)
* `u.t.i.l.i.z.e` (use *use, apply, deploy, run*)
* `l.e.v.e.r.a.g.e` (use *use, apply, deploy, capitalize on, build upon*)

### 6.2 Prohibited Phrases (Case-Insensitive)
Never use any of the following stock phrases (shown with dot separators):
* `i.n t.o.d.a.y.'s f.a.s.t-p.a.c.e.d w.o.r.l.d`
* `e.v.e.r-e.v.o.l.v.i.n.g l.a.n.d.s.c.a.p.e`
* `i.t i.s i.m.p.o.r.t.a.n.t t.o r.e.m.e.m.b.e.r`
* `i.n c.o.n.c.l.u.s.i.o.n`
* `w.i.t.h.o.u.t f.u.r.t.h.e.r a.d.o`
* `l.e.t.'s d.i.v.e i.n`
* `l.o.o.k n.o f.u.r.t.h.e.r`

### 6.3 Zero Narrative Placeholders Policy
* No file may contain shorthand drafting markers such as `T.O.D.O`, `T.B.D`, `L.o.r.e.m i.p.s.u.m`, or uncalculated `[X.X]` tokens in narrative prose, financial tables, or case studies.
* Every table cell must contain either a concrete benchmark number, an explicit formula, or a formatted worksheet entry line (`[ ________ ]`).
* Bracketed tokens in the form `[VARIABLE_NAME]` are restricted exclusively to the `INPUT VARIABLES` and template body sections of the 50 AI Workflow Prompts and 12 Emergency Scripts, where they represent user-supplied parameters.

---

## 7. TABLE, FORMULA & CODE BLOCK FORMATTING RULES

1. **Mathematical Formulas:**
   * All core chapter metrics (such as Revenue Per Production Hour $\text{RPPH}$, Outlier Multiplier Score $\text{OMS}$, Retention Velocity Index $\text{RVI}$, and Newsletter Subscriber Value $\text{NSV}$) must be presented in clean LaTeX display blocks (`$$...$$`) followed immediately by a bulleted variable glossary and a worked numerical example.
2. **Markdown Tables:**
   * Every table must have a clear header row, explicit column alignment (`:---`, `:---:`, `---:`), and between 3 and 7 columns so that horizontal width remains readable on both `6x9in` trade paperback and `8.5x11in` digital layouts.
3. **Directory & File References:**
   * Always use forward slashes (`/`) in relative and absolute paths inside Markdown files (`../04-VISUAL-ASSETS/svg/chapter-01-mindmap.svg`) to guarantee cross-platform compatibility across Windows, macOS, and Linux build pipelines.
