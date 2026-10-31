#!/usr/bin/env python3
"""
PHASE 11 AUTOMATED QA & GUMROAD HYBRID MASTER SETUP VERIFIER (`verify_phase11_gumroad.py`)
Product #3: The AI Content Creator & Solopreneur Operating System
Author & System Architect: OMAR SUNNY
Studio Root: e:/Ebook-Makaer/AI-Creator-Solopreneur-OS/DIGITAL-PUBLISHING-STUDIO/
"""

import json
import re
import shutil
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

STUDIO_ROOT = Path(__file__).resolve().parent
COVER_DIR = STUDIO_ROOT / "08-COVER-DESIGN"
GUMROAD_DIR = STUDIO_ROOT / "10-MARKETING" / "Gumroad-Hybrid-Master-Setup"
GUMROAD_THUMBS_DIR = GUMROAD_DIR / "Thumbnails-and-Covers"
BUILD_SCRIPTS_DIR = STUDIO_ROOT / "11-BUILD-SCRIPTS"
QA_REPORT_PATH = STUDIO_ROOT / "11-QA-REPORTS" / "phase11-gumroad-qa-report.md"
PROJECT_STATE_PATH = STUDIO_ROOT / "PROJECT_STATE.json"

BANNED_WORD_STEMS = [
    r"\bdelv(?:e|es|ed|ing)\b",
    r"\btapestr(?:y|ies)\b",
    r"\btestaments?\b",
    r"\bbeacons?\b",
    r"\bsymphon(?:y|ies)\b",
    r"\bunlock(?:s|ed|ing)?\b",
    r"\bunleash(?:es|ed|ing)?\b",
    r"\bskyrocket(?:s|ed|ing)?\b",
    r"\bsupercharg(?:e|es|ed|ing)\b",
    r"\bgame-changers?\b",
    r"\bpivotal\b",
    r"\brealms?\b",
    r"\bfoster(?:s|ed|ing)?\b",
    r"\bunderscor(?:e|es|ed|ing)\b",
    r"\butiliz(?:e|es|ed|ing|ation)\b",
    r"\bleverag(?:e|es|ed|ing)\b",
]

BANNED_PHRASES = [
    "in today's fast-paced world",
    "in today's fast-paced digital world",
    "ever-evolving landscape",
    "it is important to remember",
    "in conclusion",
    "without further ado",
    "let's dive in",
    "look no further",
    "whether you are a beginner or an expert",
    "lorem ipsum",
]

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bFIXME\b",
]


def read_png_ihdr_dimensions(png_path: Path) -> tuple[int, int]:
    """Reads width and height directly from the PNG binary IHDR header."""
    with png_path.open("rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"Invalid PNG header in {png_path}")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main() -> int:
    checks = []
    errors = []

    def record(name: str, passed: bool, detail: str) -> None:
        status = "PASS" if passed else "FAIL"
        checks.append((name, status, detail))
        if not passed:
            errors.append(f"{name}: {detail}")
        print(f"[{status}] {name} -> {detail}")

    print("=" * 92)
    print("PHASE 11 AUTOMATED QA: GUMROAD HYBRID 3-LISTING MASTER PACK & 600x600 THUMBNAILS")
    print("=" * 92)

    # 1. Verify the 3 Square SVGs in 08-COVER-DESIGN/
    square_bases = [
        "11-gumroad-square-thumb-listing1-free-audit-600x600",
        "12-gumroad-square-thumb-listing2-flagship-os-600x600",
        "13-gumroad-square-thumb-listing3-vip-membership-600x600",
    ]

    for base in square_bases:
        svg_path = COVER_DIR / f"{base}.svg"
        exists = svg_path.is_file()
        valid_xml = False
        viewbox_ok = False
        has_author = False
        if exists:
            raw = svg_path.read_text(encoding="utf-8")
            has_author = "OMAR SUNNY" in raw
            try:
                root = ET.fromstring(raw)
                valid_xml = True
                viewbox_ok = root.attrib.get("viewBox") == "0 0 600 600"
            except Exception:
                valid_xml = False
        record(
            f"Square SVG `{base}.svg` (Valid XML, viewBox='0 0 600 600', 'OMAR SUNNY')",
            exists and valid_xml and viewbox_ok and has_author,
            f"exists={exists}, xml={valid_xml}, viewBox_600x600={viewbox_ok}, author_OMAR_SUNNY={has_author}"
        )

    # 2. Verify all 3 rendered Square PNGs in 08-COVER-DESIGN/ and Thumbnails-and-Covers/
    for base in square_bases:
        for folder_label, folder_path in [("08-COVER-DESIGN", COVER_DIR), ("Thumbnails-and-Covers", GUMROAD_THUMBS_DIR)]:
            png_path = folder_path / f"{base}.png"
            exists = png_path.is_file()
            ihdr_w, ihdr_h = (0, 0)
            pil_w, pil_h = (0, 0)
            if exists:
                ihdr_w, ihdr_h = read_png_ihdr_dimensions(png_path)
                with Image.open(png_path) as im:
                    pil_w, pil_h = im.size
            ok = exists and (ihdr_w, ihdr_h) == (600, 600) and (pil_w, pil_h) == (600, 600)
            record(
                f"Square PNG `{folder_label}/{base}.png` Exact 600x600 px",
                ok,
                f"IHDR={ihdr_w}x{ihdr_h}, PIL={pil_w}x{pil_h}, bytes={png_path.stat().st_size if exists else 0:,}"
            )

    # 3. Verify all 5 required Markdown master guides + Bangla Master Guide
    md_thresholds = [
        ("00-BANGLA-COMPLETE-GUMROAD-STRATEGY-AND-STEP-BY-STEP-GUIDE.md", 1200),
        ("01-LISTING-1-FREE-STARTER-KIT-EXACT-FIELDS.md", 1500),
        ("02-LISTING-2-FLAGSHIP-3-VERSION-PRODUCT-EXACT-FIELDS.md", 2500),
        ("03-LISTING-3-VIP-RECURRING-MEMBERSHIP-EXACT-FIELDS.md", 1800),
        ("04-GUMROAD-CHECKOUT-UPSELLS-COUPONS-AND-WORKFLOWS.md", 1800),
        ("05-AI-COVER-AND-THUMBNAIL-IMAGE-GENERATION-PROMPTS.md", 1800),
    ]

    word_counts_map = {}
    for fname, min_words in md_thresholds:
        fpath = GUMROAD_DIR / fname
        exists = fpath.is_file()
        txt = fpath.read_text(encoding="utf-8") if exists else ""
        words = len(txt.split())
        word_counts_map[fname] = words
        has_author = "OMAR SUNNY" in txt
        ok = exists and words >= min_words and has_author
        record(
            f"Playbook `{fname}` (>= {min_words:,} words & 'OMAR SUNNY')",
            ok,
            f"words={words:,} (min {min_words:,}), author_OMAR_SUNNY={has_author}, bytes={fpath.stat().st_size if exists else 0:,}"
        )

    # 4. Strict Banned AI Cliché & Placeholder Scanner across all Phase 11 SVG & MD files
    files_to_scan = [COVER_DIR / f"{b}.svg" for b in square_bases] + [GUMROAD_DIR / m[0] for m in md_thresholds]
    banned_violations = []
    placeholder_violations = []

    for fpath in files_to_scan:
        if not fpath.is_file():
            continue
        txt = fpath.read_text(encoding="utf-8")
        low = txt.lower()
        for pat in BANNED_WORD_STEMS:
            m = re.search(pat, low)
            if m:
                banned_violations.append(f"{fpath.name}: banned word '{m.group(0)}'")
        for phrase in BANNED_PHRASES:
            if phrase in low:
                banned_violations.append(f"{fpath.name}: banned phrase '{phrase}'")
        for ppat in PLACEHOLDER_PATTERNS:
            m = re.search(ppat, txt)
            if m:
                placeholder_violations.append(f"{fpath.name}: placeholder '{m.group(0)}'")

    record(
        "Zero Banned Words & Phrases Across All Phase 11 SVG & Markdown Files",
        len(banned_violations) == 0,
        f"scanned={len(files_to_scan)} files, violations={len(banned_violations)}"
        + (f" ({banned_violations[:5]})" if banned_violations else "")
    )
    record(
        "Zero Placeholders (TODO/TBD/FIXME) Across All Phase 11 Files",
        len(placeholder_violations) == 0,
        f"scanned={len(files_to_scan)} files, violations={len(placeholder_violations)}"
        + (f" ({placeholder_violations[:5]})" if placeholder_violations else "")
    )

    # 5. Verify Tier 4 ZIP archive includes Gumroad-Hybrid-Master-Setup/ and passes testzip()
    t4_zip = STUDIO_ROOT / "09-EXPORTS" / "HYBRID-BUNDLE" / "tier4-pro-living-system-and-vault.zip"
    zip_ok = False
    zip_detail = "missing"
    if t4_zip.is_file():
        with zipfile.ZipFile(t4_zip, "r") as zf:
            bad_file = zf.testzip()
            names = set(zf.namelist())
            has_gumroad_setup = any("10-MARKETING/Gumroad-Hybrid-Master-Setup/" in n for n in names)
            has_sq_thumbs = any("12-gumroad-square-thumb-listing2-flagship-os-600x600.png" in n for n in names)
            zip_ok = (bad_file is None) and has_gumroad_setup and has_sq_thumbs
            zip_detail = f"entries={len(names)}, testzip={bad_file}, gumroad_pack={has_gumroad_setup}, square_thumbs={has_sq_thumbs}, size={t4_zip.stat().st_size:,} B"
    record(
        "Tier 4 ZIP Bundle Updated & Verified (`testzip() is None`)",
        zip_ok,
        zip_detail
    )

    # Mirror verifier into 11-BUILD-SCRIPTS/
    BUILD_SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    this_file = Path(__file__).resolve()
    mirror_file = BUILD_SCRIPTS_DIR / this_file.name
    if this_file != mirror_file:
        shutil.copy2(this_file, mirror_file)

    now_iso = datetime.now(timezone.utc).isoformat()
    if len(errors) == 0:
        state = json.loads(PROJECT_STATE_PATH.read_text(encoding="utf-8"))
        state["author"] = "OMAR SUNNY"
        state["current_phase"] = 11
        state["phases_completed"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        state.setdefault("phase_status", {})["Phase 11"] = "COMPLETED"
        state.setdefault("phases", {})["Phase 11"] = "COMPLETED"
        state["studio_status"] = "100% PRODUCTION, CLOUD & GUMROAD STOREFRONT READY (PHASES 1-11 VERIFIED, 0 ERRORS)"
        state["last_updated"] = now_iso
        state["phase11_gumroad_master_setup"] = {
            "author": "OMAR SUNNY",
            "directory": "10-MARKETING/Gumroad-Hybrid-Master-Setup/",
            "square_thumbnails_600x600": [f"{b}.png" for b in square_bases],
            "playbooks_word_counts": word_counts_map,
            "tier4_zip_bytes": t4_zip.stat().st_size if t4_zip.is_file() else 0,
        }
        PROJECT_STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        record(
            "Update PROJECT_STATE.json (`current_phase: 11`, `phases_completed: [1..11]`)",
            True,
            "PROJECT_STATE.json updated cleanly"
        )

    # Write QA report
    QA_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report_lines = [
        "# PHASE 11 QA REPORT — GUMROAD HYBRID MASTER SETUP & 600x600 SQUARE THUMBNAILS",
        "",
        "- **Product:** *The AI Content Creator & Solopreneur Operating System*",
        "- **Author & System Architect:** `OMAR SUNNY`",
        f"- **Verification Timestamp (UTC):** `{now_iso}`",
        f"- **Checks Passed:** `{len(checks) - len(errors)} / {len(checks)}` (`{len(errors)} errors`)",
        "",
        "| # | Check Name | Status | Verification Detail |",
        "| :--- | :--- | :---: | :--- |",
    ]
    for i, (name, st, det) in enumerate(checks, start=1):
        report_lines.append(f"| {i:02d} | {name} | **{st}** | {det} |")
    QA_REPORT_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("=" * 92)
    if errors:
        print(f"PHASE 11 VERIFICATION FAILED WITH {len(errors)} ERRORS:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PHASE 11 GUMROAD HYBRID MASTER SETUP VERIFICATION PASSED WITH 0 ERRORS")
    print("=" * 92)
    return 0


if __name__ == "__main__":
    sys.exit(main())
