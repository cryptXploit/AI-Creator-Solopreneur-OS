#!/usr/bin/env python3
"""
Phase 7 Verification Suite (verify_phase7.py)
Product #3: The AI Content Creator & Solopreneur Operating System
Validates the 5-Database Notion Creator OS Kit, 3 Markdown Guides,
6 Vector SVG Covers, 6 High-Res PNG Renders, and Dynamic KDP Full-Wrap PDF.
Writes 11-QA-REPORTS/phase7-qa-report.md and exits with 0 on success.
"""

import csv
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from pypdf import PdfReader

STUDIO_ROOT = Path(__file__).resolve().parent
NOTION_DIR = STUDIO_ROOT / "06-NOTION-TEMPLATES"
SPREADSHEETS_DIR = NOTION_DIR / "Spreadsheets"
COVER_DIR = STUDIO_ROOT / "08-COVER-DESIGN"
COVER_SVG_DIR = COVER_DIR / "svg"
COVER_PNG_DIR = COVER_DIR / "png"
QA_DIR = STUDIO_ROOT / "11-QA-REPORTS"
STATE_PATH = STUDIO_ROOT / "PROJECT_STATE.json"

BANNED_WORDS_PATTERN = re.compile(
    r"\b("
    r"delve[sd]?|delving|"
    r"tapestr(?:y|ies)|"
    r"testaments?|"
    r"beacons?|"
    r"symphon(?:y|ies)|"
    r"unlock(?:s|ed|ing)?|"
    r"unleash(?:es|ed|ing)?|"
    r"skyrocket(?:s|ed|ing)?|"
    r"supercharg(?:e|es|ed|ing)|"
    r"game-changer[s]?|"
    r"pivotal|"
    r"realms?|"
    r"foster(?:s|ed|ing)?|"
    r"underscor(?:e|es|ed|ing)|"
    r"utiliz(?:e|es|ed|ing|ation)|"
    r"leverag(?:e|es|ed|ing)"
    r")\b",
    re.IGNORECASE,
)

BANNED_PHRASES = [
    "in today's fast-paced world",
    "ever-evolving landscape",
    "it is important to remember",
    "in conclusion",
    "without further ado",
    "let's dive in",
    "look no further",
]

PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b"),
    re.compile(r"\bTBD\b"),
    re.compile(r"lorem ipsum", re.IGNORECASE),
    re.compile(r"\[XX\]"),
]


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def check_text_prohibitions(text: str, label: str, errors: list):
    for m in BANNED_WORDS_PATTERN.finditer(text):
        errors.append(f"[{label}] Banned word detected: '{m.group(0)}'")
    lower_t = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lower_t:
            errors.append(f"[{label}] Banned phrase detected: '{phrase}'")
    for pat in PLACEHOLDER_PATTERNS:
        m = pat.search(text)
        if m:
            errors.append(f"[{label}] Placeholder token detected: '{m.group(0)}'")


def main() -> int:
    errors = []
    checks = []

    print("=" * 84)
    print("PHASE 7 QA VERIFICATION: NOTION CREATOR OS KIT & COMMERCIAL COVER SUITE")
    print("=" * 84)

    # Load PROJECT_STATE.json to check locked KDP page count
    kdp_pages = 314
    if not STATE_PATH.exists():
        errors.append("PROJECT_STATE.json missing")
    else:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        kdp_pages = int(state.get("kdp_paperback_6x9_pages", 314))
        checks.append(("PROJECT_STATE.json kdp_paperback_6x9_pages", "PASS", f"{kdp_pages} pages"))

    expected_spine_in = round(kdp_pages * 0.002252, 6)
    expected_total_w_in = round(6.0 + 6.0 + expected_spine_in + 0.25, 6)
    expected_total_h_in = 9.250
    expected_pt_w = round(expected_total_w_in * 72.0, 2)
    expected_pt_h = round(expected_total_h_in * 72.0, 2)
    expected_px_w = int(round(expected_total_w_in * 300))
    expected_px_h = int(round(expected_total_h_in * 300))

    # 1. Verify 5 Notion CSVs
    csv_specs = [
        (NOTION_DIR / "01-Outlier-Idea-Bank-and-Hook-Vault.csv", 25, False),
        (NOTION_DIR / "02-Master-Content-Calendar-and-1to15-Waterfall.csv", 20, False),
        (NOTION_DIR / "03-AI-Prompt-and-Script-Vault-62.csv", 62, True),
        (NOTION_DIR / "04-Sponsorship-CRM-and-Affiliate-Tracker.csv", 20, False),
        (SPREADSHEETS_DIR / "sheet1-creator-rpm-and-time-audit.csv", 25, False),
    ]

    csv_telemetry = []
    for path, min_rows, exact_62 in csv_specs:
        rel = path.relative_to(STUDIO_ROOT).as_posix()
        if not path.exists():
            errors.append(f"Missing CSV file: {rel}")
            checks.append((f"CSV {rel}", "FAIL", "File missing"))
            continue

        raw_text = path.read_text(encoding="utf-8")
        check_text_prohibitions(raw_text, rel, errors)

        with path.open("r", encoding="utf-8", newline="") as f:
            reader = list(csv.reader(f))

        if len(reader) < 2:
            errors.append(f"CSV {rel} has no data rows")
            continue

        header = reader[0]
        data_rows = reader[1:]
        col_count = len(header)
        uniform_cols = all(len(r) == col_count for r in data_rows)
        if not uniform_cols:
            errors.append(f"CSV {rel} has inconsistent column counts across rows")

        row_count = len(data_rows)
        if exact_62:
            if row_count != 62:
                errors.append(f"CSV {rel} must have exactly 62 data rows (found {row_count})")
            # Check P01..P50 and S01..S12 IDs
            found_ids = {r[0].strip() for r in data_rows if r}
            expected_ids = {f"P{i:02d}" for i in range(1, 51)} | {f"S{i:02d}" for i in range(1, 13)}
            missing_ids = sorted(expected_ids - found_ids)
            if missing_ids:
                errors.append(f"CSV {rel} missing IDs: {missing_ids}")
            else:
                checks.append((f"CSV {rel} 62 IDs (P01..P50 + S01..S12)", "PASS", "All 62 IDs verified"))
        else:
            if row_count < min_rows:
                errors.append(f"CSV {rel} has {row_count} data rows (minimum {min_rows})")

        size_bytes = path.stat().st_size
        csv_telemetry.append((rel, row_count, col_count, size_bytes))
        checks.append((f"CSV {rel}", "PASS", f"{row_count} data rows, {col_count} cols ({size_bytes:,} bytes)"))

    # 2. Verify 3 Markdown Guides
    md_specs = [
        (NOTION_DIR / "05-Creator-Monetization-and-Launch-Hub.md", 1500),
        (NOTION_DIR / "NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md", 1500),
        (COVER_DIR / "COVER-DESIGN-AND-PACKAGING-SPEC.md", 1200),
    ]

    md_telemetry = []
    for path, min_words in md_specs:
        rel = path.relative_to(STUDIO_ROOT).as_posix()
        if not path.exists():
            errors.append(f"Missing Markdown file: {rel}")
            checks.append((f"Markdown {rel}", "FAIL", "File missing"))
            continue

        raw_text = path.read_text(encoding="utf-8")
        check_text_prohibitions(raw_text, rel, errors)
        wc = count_words(raw_text)
        size_bytes = path.stat().st_size
        if wc < min_words:
            errors.append(f"Markdown {rel} has {wc} words (minimum {min_words})")
            checks.append((f"Markdown {rel}", "FAIL", f"{wc} words < {min_words}"))
        else:
            checks.append((f"Markdown {rel}", "PASS", f"{wc:,} words ({size_bytes:,} bytes)"))
        md_telemetry.append((rel, wc, size_bytes))

    # 3. Verify 6 SVG Covers
    svg_specs = [
        (COVER_SVG_DIR / "ebook-cover-kdp-kindle.svg", f"0 0 1600 2560"),
        (COVER_SVG_DIR / "kdp-paperback-full-wrap-cover.svg", f"0 0 {expected_px_w} {expected_px_h}"),
        (COVER_SVG_DIR / "gumroad-tier0-free-audit-cover.svg", "0 0 1600 1000"),
        (COVER_SVG_DIR / "gumroad-tier2-workbook-edition-cover.svg", "0 0 1600 1000"),
        (COVER_SVG_DIR / "gumroad-tier3-flagship-bundle-cover.svg", "0 0 1600 1000"),
        (COVER_SVG_DIR / "gumroad-tier4-vault-membership-cover.svg", "0 0 1600 1000"),
    ]

    svg_telemetry = []
    for path, expected_vb in svg_specs:
        rel = path.relative_to(STUDIO_ROOT).as_posix()
        if not path.exists():
            errors.append(f"Missing SVG cover: {rel}")
            checks.append((f"SVG {rel}", "FAIL", "File missing"))
            continue

        size_bytes = path.stat().st_size
        if size_bytes < 5000:
            errors.append(f"SVG {rel} is too small ({size_bytes} bytes < 5,000)")

        raw_svg = path.read_text(encoding="utf-8")
        try:
            root = ET.fromstring(raw_svg)
            vb = root.attrib.get("viewBox", "")
            if vb != expected_vb:
                errors.append(f"SVG {rel} viewBox '{vb}' != expected '{expected_vb}'")
                checks.append((f"SVG {rel}", "FAIL", f"viewBox '{vb}' != '{expected_vb}'"))
            else:
                checks.append((f"SVG {rel}", "PASS", f"Valid XML, viewBox='{vb}' ({size_bytes:,} bytes)"))
        except ET.ParseError as e:
            errors.append(f"SVG {rel} XML parse error: {e}")
            checks.append((f"SVG {rel}", "FAIL", f"XML parse error: {e}"))
            vb = "ERROR"
        svg_telemetry.append((rel, vb, size_bytes))

    # 4. Verify PNG Covers (including root ebook-cover-kdp-kindle.png + png/ directory)
    png_specs = [
        (COVER_DIR / "ebook-cover-kdp-kindle.png", 1600, 2560),
        (COVER_PNG_DIR / "ebook-cover-kdp-kindle.png", 1600, 2560),
        (COVER_PNG_DIR / "kdp-paperback-full-wrap-cover.png", expected_px_w, expected_px_h),
        (COVER_PNG_DIR / "gumroad-tier0-free-audit-cover.png", 1600, 1000),
        (COVER_PNG_DIR / "gumroad-tier2-workbook-edition-cover.png", 1600, 1000),
        (COVER_PNG_DIR / "gumroad-tier3-flagship-bundle-cover.png", 1600, 1000),
        (COVER_PNG_DIR / "gumroad-tier4-vault-membership-cover.png", 1600, 1000),
    ]

    png_telemetry = []
    for path, exp_w, exp_h in png_specs:
        rel = path.relative_to(STUDIO_ROOT).as_posix()
        if not path.exists():
            errors.append(f"Missing PNG cover: {rel}")
            checks.append((f"PNG {rel}", "FAIL", "File missing"))
            continue

        size_bytes = path.stat().st_size
        if size_bytes < 40000:
            errors.append(f"PNG {rel} too small ({size_bytes} bytes < 40,000)")

        png_bytes = path.read_bytes()
        if png_bytes[:8] != b"\x89PNG\r\n\x1a\n":
            errors.append(f"PNG {rel} invalid magic bytes")
            checks.append((f"PNG {rel}", "FAIL", "Invalid magic bytes"))
            continue

        w, h = struct.unpack(">II", png_bytes[16:24])
        if (w, h) != (exp_w, exp_h):
            errors.append(f"PNG {rel} IHDR dimensions {w}x{h} != expected {exp_w}x{exp_h}")
            checks.append((f"PNG {rel}", "FAIL", f"{w}x{h} != {exp_w}x{exp_h}"))
        else:
            checks.append((f"PNG {rel}", "PASS", f"{w}×{h} px verified via IHDR ({size_bytes:,} bytes)"))
        png_telemetry.append((rel, w, h, size_bytes))

    # 5. Verify KDP Full-Wrap PDF
    pdf_path = COVER_DIR / "kdp-paperback-full-wrap-cover.pdf"
    pdf_rel = pdf_path.relative_to(STUDIO_ROOT).as_posix()
    pdf_info = ("MISSING", 0, 0.0, 0.0, 0)
    if not pdf_path.exists():
        errors.append(f"Missing KDP Full-Wrap PDF: {pdf_rel}")
        checks.append((f"PDF {pdf_rel}", "FAIL", "File missing"))
    else:
        pdf_size = pdf_path.stat().st_size
        if pdf_size < 50000:
            errors.append(f"PDF {pdf_rel} too small ({pdf_size} bytes < 50,000)")
        reader = PdfReader(str(pdf_path))
        num_pages = len(reader.pages)
        if num_pages != 1:
            errors.append(f"PDF {pdf_rel} must have exactly 1 page (found {num_pages})")
        mb = reader.pages[0].mediabox
        pt_w = float(mb.width)
        pt_h = float(mb.height)
        if abs(pt_w - expected_pt_w) > 3.0 or abs(pt_h - expected_pt_h) > 3.0:
            errors.append(
                f"PDF {pdf_rel} MediaBox {pt_w:.2f}x{pt_h:.2f}pt outside ±3pt tolerance of {expected_pt_w:.2f}x{expected_pt_h:.2f}pt"
            )
            checks.append((f"PDF {pdf_rel}", "FAIL", f"{pt_w:.2f}x{pt_h:.2f}pt != {expected_pt_w:.2f}x{expected_pt_h:.2f}pt"))
        else:
            checks.append(
                (f"PDF {pdf_rel}", "PASS", f"1 page, {pt_w:.2f}pt × {pt_h:.2f}pt ({pdf_size:,} bytes)")
            )
        pdf_info = (pdf_rel, num_pages, pt_w, pt_h, pdf_size)

    # Print summary table to console
    for name, status, detail in checks:
        print(f"[{status}] {name:<62} | {detail}")

    print("-" * 84)
    print(f"KDP 6x9 Paperback Locked Pages: {kdp_pages} pages")
    print(f"Calculated Spine Width:         {expected_spine_in:.6f} in ({expected_spine_in * 25.4:.2f} mm)")
    print(f"Full-Wrap Bleed Dimensions:     {expected_total_w_in:.6f} in × {expected_total_h_in:.3f} in ({expected_pt_w:.2f}pt × {expected_pt_h:.2f}pt / {expected_px_w}×{expected_px_h}px)")
    print(f"Total Errors:                   {len(errors)}")
    print("=" * 84)

    if errors:
        for err in errors:
            print(f"  ERROR: {err}")

    # Write QA report
    QA_DIR.mkdir(parents=True, exist_ok=True)
    report_path = QA_DIR / "phase7-qa-report.md"
    now_iso = datetime.now(timezone.utc).isoformat()
    status_str = "PASSED (0 ERRORS)" if not errors else f"FAILED ({len(errors)} ERRORS)"

    lines = [
        "# Phase 7 QA Report — 5-Database Notion Creator OS Kit & Commercial Cover Suite",
        "",
        f"- **Timestamp:** `{now_iso}`",
        f"- **Status:** **{status_str}**",
        f"- **Locked KDP 6\"×9\" Page Count:** `{kdp_pages} pages`",
        f"- **Calculated Spine Width:** `{expected_spine_in:.6f} in` (`{expected_spine_in * 25.4:.2f} mm`)",
        f"- **Full-Wrap Dimensions (with 0.125\" Bleed):** `{expected_total_w_in:.6f}\" × {expected_total_h_in:.3f}\"` (`{expected_pt_w:.2f}pt × {expected_pt_h:.2f}pt` / `{expected_px_w}×{expected_px_h}px` at 300 DPI)",
        "",
        "## 1. Notion Creator OS CSV Databases",
        "",
        "| File Path | Data Rows | Columns | File Size (Bytes) |",
        "| :--- | :---: | :---: | :---: |",
    ]
    for rel, rows, cols, sz in csv_telemetry:
        lines.append(f"| `{rel}` | {rows} | {cols} | {sz:,} |")

    lines.extend([
        "",
        "## 2. Notion & Cover Packaging Markdown Manuals",
        "",
        "| File Path | Word Count | File Size (Bytes) |",
        "| :--- | :---: | :---: |",
    ])
    for rel, wc, sz in md_telemetry:
        lines.append(f"| `{rel}` | {wc:,} | {sz:,} |")

    lines.extend([
        "",
        "## 3. Master Vector SVG Covers",
        "",
        "| File Path | viewBox | File Size (Bytes) |",
        "| :--- | :---: | :---: |",
    ])
    for rel, vb, sz in svg_telemetry:
        lines.append(f"| `{rel}` | `{vb}` | {sz:,} |")

    lines.extend([
        "",
        "## 4. High-Resolution PNG Renders (Verified via PNG IHDR Header)",
        "",
        "| File Path | Pixel Dimensions | File Size (Bytes) |",
        "| :--- | :---: | :---: |",
    ])
    for rel, w, h, sz in png_telemetry:
        lines.append(f"| `{rel}` | `{w} × {h} px` | {sz:,} |")

    lines.extend([
        "",
        "## 5. KDP 6\"×9\" Full-Wrap Print PDF",
        "",
        "| File Path | Pages | MediaBox Dimensions (pt) | File Size (Bytes) |",
        "| :--- | :---: | :---: | :---: |",
        f"| `{pdf_info[0]}` | {pdf_info[1]} | `{pdf_info[2]:.2f}pt × {pdf_info[3]:.2f}pt` | {pdf_info[4]:,} |",
        "",
        "## 6. Verification Check Log",
        "",
        "| Check | Status | Details |",
        "| :--- | :---: | :--- |",
    ])
    for name, st, detail in checks:
        lines.append(f"| {name} | **{st}** | {detail} |")

    if errors:
        lines.extend(["", "## 7. Errors", ""])
        for err in errors:
            lines.append(f"- {err}")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"QA Report written to: {report_path.relative_to(STUDIO_ROOT).as_posix()}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
