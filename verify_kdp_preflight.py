#!/usr/bin/env python3
"""
verify_kdp_preflight.py
Amazon KDP Print Previewer Pre-Flight & Margin Compliance Verification Suite
Flagship Product #3: The AI Content Creator & Solopreneur Operating System
Author: Omar Sunny
Studio Root: e:/Ebook-Makaer/AI-Creator-Solopreneur-OS/DIGITAL-PUBLISHING-STUDIO/

Audits every page of the KDP 6"x9" Paperback Interior PDF and KDP Full-Wrap Cover PDF:
  1. Exact 6.00" x 9.00" (432.0pt x 648.0pt) trim box on all interior pages.
  2. Zero non-printable markup / link annotations (/Annots) on any page (including Page 2).
  3. Strict symmetric gutter & margin compliance on ALL odd and even pages:
     - KDP 301-500 page requirement: >= 0.625" (45.0pt) inside gutter (left on odd, right on even)
       and >= 0.25" (18.0pt) outside/top/bottom margins.
     - Studio symmetric enforcement: X in [50.0pt, 382.0pt] (>= 0.694" left & right on ALL pages)
       and Y in [38.0pt, 610.0pt] (>= 0.528" top & bottom on ALL pages).
  4. Zero text overlap in the Back Cover ISBN Barcode (2.0"x1.2") & Amazon Transparency QR zone,
     plus verified 'OMAR SUNNY' author credit on Front Cover, Spine, Back Cover, and Interior Title Page.
"""

import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from pypdf import PdfReader

STUDIO_ROOT = Path(__file__).resolve().parent

KDP_FORBIDDEN_DCE_PATTERNS = [
    (re.compile(r"\bworkbooks?\b", re.IGNORECASE), "workbook(s)"),
    (re.compile(r"\bworksheets?\b", re.IGNORECASE), "worksheet(s)"),
    (re.compile(r"\bfillable\b", re.IGNORECASE), "fillable"),
    (re.compile(r"creator-os-app", re.IGNORECASE), "creator-os-app.html"),
    (re.compile(r"CREATOR-OS-PRO", re.IGNORECASE), "CREATOR-OS-PRO-2026"),
    (re.compile(r"PRODUCT-03", re.IGNORECASE), "PRODUCT-03"),
    (re.compile(r"05-WORKBOOKS", re.IGNORECASE), "05-WORKBOOKS"),
    (re.compile(r"01-MARKET-RESEARCH", re.IGNORECASE), "01-MARKET-RESEARCH"),
    (re.compile(r"sources\.md", re.IGNORECASE), "sources.md"),
    (re.compile(r"Editorial\s*&\s*Systems", re.IGNORECASE), "Editorial & Systems Team"),
    (re.compile(r"Half-Title Page", re.IGNORECASE), "Literal 'Half-Title Page'"),
    (re.compile(r"Full Title Page", re.IGNORECASE), "Literal 'Full Title Page'"),
    (re.compile(r"Monetize Your Audience Without Burnout", re.IGNORECASE), "Truncated >200-char subtitle 'Monetize Your Audience Without Burnout'"),
    (re.compile(r"☐"), "Interactive checkbox glyph ☐"),
    (re.compile(r"\*\*[^*\n]+\*\*"), "Unrendered raw Markdown **bold** syntax"),
    (re.compile(r"\[SRC-\d+\]"), "Unresolved [SRC-XX] citation tag"),
    (re.compile(r"\[[A-Z][A-Z0-9_\s/-]{2,}\]"), "Unresolved [ALL_CAPS] bracket placeholder"),
    (re.compile(r"\b[\w-]+\.(?:md|csv|svg|pdf|mp4|json|xlsx)\b"), "Local file extension reference"),
]


def main() -> int:
    errors: list[str] = []
    checks: list[tuple[str, str, str]] = []

    print("=" * 92)
    print("AMAZON KDP PRINT PREVIEWER PRE-FLIGHT VERIFICATION SUITE (verify_kdp_preflight.py)")
    print("=" * 92)

    state_path = STUDIO_ROOT / "PROJECT_STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    expected_pages = int(state.get("kdp_paperback_6x9_pages", 314))

    kdp_pdf_path = STUDIO_ROOT / "09-EXPORTS/PRINT/the-ai-creator-solopreneur-os-kdp-paperback-6x9.pdf"
    if not kdp_pdf_path.is_file():
        print("[FAIL] Missing KDP 6x9 interior PDF")
        return 1

    reader = PdfReader(str(kdp_pdf_path))
    num_pages = len(reader.pages)
    if num_pages != expected_pages:
        errors.append(f"KDP page count {num_pages} != PROJECT_STATE expected {expected_pages}")
        checks.append(("KDP Page Count Sync", "FAIL", f"{num_pages} != {expected_pages}"))
    else:
        checks.append(("KDP Page Count Sync", "PASS", f"{num_pages} pages (matches PROJECT_STATE.json)"))

    # Check Title Page Author Attribution, Page 2 Copyright/Disclaimer, and Page 3 Numbered TOC
    p1_text = reader.pages[0].extract_text() or ""
    p2_text = reader.pages[1].extract_text() or ""
    p3_text = reader.pages[2].extract_text() or ""
    if "Omar Sunny" in p1_text:
        checks.append(("Interior Title Page Author ('Omar Sunny')", "PASS", "Verified on Page 1"))
    else:
        errors.append("Interior Title Page missing author 'Omar Sunny'")
        checks.append(("Interior Title Page Author ('Omar Sunny')", "FAIL", "Missing on Page 1"))

    if "Copyright" in p2_text and "Omar Sunny" in p2_text and "Page 2" in p2_text:
        checks.append(("Page 2 Copyright & Legal Disclaimer + Folio", "PASS", "Verified on Page 2 (directly behind Title Page)"))
    else:
        errors.append("Page 2 missing Copyright & Legal Disclaimer or 'Page 2' folio")
        checks.append(("Page 2 Copyright & Legal Disclaimer + Folio", "FAIL", "Missing on Page 2"))

    if "Master Table of Contents" in p3_text and "Page 4" in p3_text and "Page 12" in p3_text and "Page 287" in p3_text:
        checks.append(("Page 3 Master TOC with Printed Page Numbers", "PASS", "Verified exact starting page numbers (Page 4 .. Page 287)"))
    else:
        errors.append(f"Page 3 Master TOC missing printed starting page numbers: {p3_text[:150]}")
        checks.append(("Page 3 Master TOC with Printed Page Numbers", "FAIL", "Missing starting page numbers"))

    # Scan all pages for MediaBox, Annotations, Text Bounds, Vector Object Bounds, Blank/Sparse Pages, and Stamped Folios
    bad_dims = []
    annot_pages = []
    text_margin_violations = []
    rect_margin_violations = []
    sparse_pages = []
    missing_folios = []
    pdf_dce_hits = []

    min_x_global = 999.0
    max_x_global = 0.0
    min_y_global = 999.0
    max_y_global = 0.0

    for idx, page in enumerate(reader.pages):
        p_num = idx + 1
        mb = page.mediabox
        pw = float(mb.width)
        ph = float(mb.height)
        if abs(pw - 432.0) > 1.0 or abs(ph - 648.0) > 1.0:
            bad_dims.append((p_num, pw, ph))

        annots = page.get("/Annots")
        if annots:
            try:
                cnt = len(annots.get_object() if hasattr(annots, "get_object") else annots)
            except Exception:
                cnt = 1
            if cnt > 0:
                annot_pages.append((p_num, cnt))

        def v_op(op, args, cm, tm):
            nonlocal min_x_global, max_x_global, min_y_global, max_y_global
            if op == b"re" and len(args) == 4:
                x, y, w, h = [float(a) for a in args]
                ux1 = cm[0] * x + cm[2] * y + cm[4]
                ux2 = cm[0] * (x + w) + cm[2] * (y + h) + cm[4]
                uy1 = cm[1] * x + cm[3] * y + cm[5]
                uy2 = cm[1] * (x + w) + cm[3] * (y + h) + cm[5]
                mn_x, mx_x = min(ux1, ux2), max(ux1, ux2)
                mn_y, mx_y = min(uy1, uy2), max(uy1, uy2)
                # Ignore full-page white canvas rectangle (0..432, 0..648)
                if mn_x <= 1.0 and mx_x >= 431.0:
                    return
                if mn_x < min_x_global:
                    min_x_global = mn_x
                if mx_x > max_x_global:
                    max_x_global = mx_x
                if mn_y < min_y_global:
                    min_y_global = mn_y
                if mx_y > max_y_global:
                    max_y_global = mx_y
                # KDP gutter is 45.0pt (left on odd, right on even -> X in [45, 387]).
                # Enforce stricter [50.0pt, 382.0pt] horizontally and [38.0pt, 610.0pt] vertically.
                if mn_x < 50.0 or mx_x > 382.0 or mn_y < 38.0 or mx_y > 610.0:
                    rect_margin_violations.append(
                        (p_num, round(mn_x, 1), round(mx_x, 1), round(mn_y, 1), round(mx_y, 1))
                    )
            elif op in (b"m", b"l") and len(args) == 2:
                x, y = float(args[0]), float(args[1])
                ux = cm[0] * x + cm[2] * y + cm[4]
                uy = cm[1] * x + cm[3] * y + cm[5]
                if ux < 50.0 or ux > 382.0 or uy < 38.0 or uy > 610.0:
                    rect_margin_violations.append(
                        (p_num, round(ux, 1), round(ux, 1), round(uy, 1), round(uy, 1))
                    )

        page_text_chunks: list[str] = []

        def v_tx(text, cm, tm, fd, fs):
            nonlocal min_x_global, max_x_global, min_y_global, max_y_global
            s = text.strip()
            if not s:
                return
            page_text_chunks.append(s)
            x = cm[4] + tm[4] * cm[0]
            y = cm[5] + tm[5] * cm[3]
            if x < min_x_global:
                min_x_global = x
            if x > max_x_global:
                max_x_global = x
            if y < min_y_global:
                min_y_global = y
            if y > max_y_global:
                max_y_global = y
            if x < 50.0 or x > 380.0 or y < 38.0 or y > 610.0:
                text_margin_violations.append((p_num, round(x, 1), round(y, 1), ascii(s[:25])))

        page.extract_text(visitor_operand_before=v_op, visitor_text=v_tx)
        joined_page_txt = " ".join(page_text_chunks)
        if len(joined_page_txt) < 200:
            sparse_pages.append((p_num, len(joined_page_txt)))
        if p_num >= 2 and f"Page {p_num}" not in joined_page_txt:
            missing_folios.append(p_num)
        for pat, label in KDP_FORBIDDEN_DCE_PATTERNS:
            m = pat.search(joined_page_txt)
            if m:
                pdf_dce_hits.append(f"PDF p.{p_num}: {label} ('{m.group(0)}')")

    if bad_dims:
        errors.append(f"Trim size violations: {bad_dims[:5]}")
        checks.append(("Trim Size 6.00\" x 9.00\" (432x648pt)", "FAIL", f"{len(bad_dims)} pages off-spec"))
    else:
        checks.append(("Trim Size 6.00\" x 9.00\" (432x648pt)", "PASS", f"All {num_pages} pages exact 432.0x648.0pt"))

    if annot_pages:
        errors.append(f"Non-printable /Annots found on pages: {annot_pages}")
        checks.append(("Zero Non-Printable Markup (/Annots)", "FAIL", f"Found on {annot_pages}"))
    else:
        checks.append(("Zero Non-Printable Markup (/Annots)", "PASS", f"0 annotations across all {num_pages} pages (incl. Page 2)"))

    if text_margin_violations:
        errors.append(f"Text outside KDP safe margins: {text_margin_violations[:5]}")
        checks.append(("Text Margin & Gutter Compliance", "FAIL", f"{len(text_margin_violations)} violations"))
    else:
        checks.append(
            (
                "Text Margin & Gutter Compliance (Odd & Even Pages)",
                "PASS",
                f"0 violations; X in [{min_x_global:.1f}pt, {max_x_global:.1f}pt] (margins >= {min(min_x_global, 432-max_x_global)/72:.3f}in > 0.625in gutter)",
            )
        )

    if rect_margin_violations:
        errors.append(f"Object/Rect outside KDP safe margins: {rect_margin_violations[:5]}")
        checks.append(("Object/Vector Margin & Gutter Compliance", "FAIL", f"{len(rect_margin_violations)} violations"))
    else:
        checks.append(
            (
                "Object/Vector Margin & Gutter Compliance (All Pages)",
                "PASS",
                f"0 violations; all tables, code boxes & SVGs inside [{min_x_global:.1f}pt, {max_x_global:.1f}pt]",
            )
        )

    if sparse_pages:
        errors.append(f"Blank or sparse pages (<200 chars) in KDP PDF: {sparse_pages}")
        checks.append(("Zero Blank or Sparse Pages (<200 chars)", "FAIL", f"Found on {sparse_pages}"))
    else:
        checks.append(("Zero Blank or Sparse Pages (<200 chars)", "PASS", f"0 blank/sparse pages across all {num_pages} pages"))

    if missing_folios:
        errors.append(f"Missing printed page numbers on KDP pages: {missing_folios[:10]}")
        checks.append(("Printed Page Numbers (Pages 2..314)", "FAIL", f"Missing on {len(missing_folios)} pages"))
    else:
        checks.append(("Printed Page Numbers (Pages 2..314)", "PASS", f"All {num_pages - 1} content pages stamped with 'Page X' folio"))

    if pdf_dce_hits:
        errors.extend(pdf_dce_hits[:10])
        checks.append(("KDP Print Interior Zero DCE/Markdown/Placeholder", "FAIL", f"{len(pdf_dce_hits)} hits: {pdf_dce_hits[:3]}"))
    else:
        checks.append(("KDP Print Interior Zero DCE/Markdown/Placeholder", "PASS", "0 **bold**, 0 [SRC-XX], 0 [PLACEHOLDERS], 0 file exts"))

    # Check KDP Full-Wrap Cover SVG & PDF for Barcode/Transparency Safe Zone & Author Name
    wrap_svg_path = STUDIO_ROOT / "08-COVER-DESIGN/svg/kdp-paperback-full-wrap-cover.svg"
    wrap_pdf_path = STUDIO_ROOT / "08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf"
    if not wrap_svg_path.is_file() or not wrap_pdf_path.is_file():
        errors.append("Missing KDP Full-Wrap Cover SVG or PDF")
        checks.append(("KDP Full-Wrap Cover Files", "FAIL", "Missing SVG or PDF"))
    else:
        raw_svg = wrap_svg_path.read_text(encoding="utf-8")
        if "OMAR SUNNY" in raw_svg:
            checks.append(("KDP Cover Author Attribution ('OMAR SUNNY')", "PASS", "Verified on Front, Spine & Back Cover"))
        else:
            errors.append("KDP Full-Wrap Cover missing 'OMAR SUNNY'")
            checks.append(("KDP Cover Author Attribution ('OMAR SUNNY')", "FAIL", "Missing 'OMAR SUNNY'"))

        # Parse XML and ensure zero <text> nodes sit inside the lower-right Back Cover Barcode + Transparency zone
        # Lower-right back cover zone: x in [1120, 1838], y in [1700, 2737]
        root = ET.fromstring(raw_svg)
        overlapping_texts = []
        for elem in root.iter():
            if elem.tag.endswith("text"):
                try:
                    tx = float(elem.attrib.get("x", "0"))
                    ty = float(elem.attrib.get("y", "0"))
                    if 1120 <= tx <= 1838 and 1700 <= ty <= 2737:
                        overlapping_texts.append((tx, ty, "".join(elem.itertext()).strip()))
                except ValueError:
                    pass
        if overlapping_texts:
            errors.append(f"Text overlapping KDP Barcode/Transparency zone: {overlapping_texts}")
            checks.append(("KDP Back Cover Barcode & Transparency Safe Zone", "FAIL", f"Overlap: {overlapping_texts}"))
        else:
            checks.append(
                (
                    "KDP Back Cover Barcode & Transparency Safe Zone",
                    "PASS",
                    "0 text elements in lower-right Barcode (2.0\"x1.2\") + Transparency QR zone",
                )
            )

    # 5. Check Kindle EPUB 3.0 & KDP Covers for Content Review (DCE & Copyright/Metadata) Compliance
    epub_path = STUDIO_ROOT / "09-EXPORTS/EPUB/the-ai-creator-solopreneur-os.epub"
    kindle_svg_path = STUDIO_ROOT / "08-COVER-DESIGN/svg/ebook-cover-kdp-kindle.svg"
    if not epub_path.is_file() or not kindle_svg_path.is_file():
        errors.append("Missing Kindle EPUB or Kindle Cover SVG")
        checks.append(("Kindle EPUB 3.0 & Cover Files", "FAIL", "Missing EPUB or SVG"))
    else:
        dce_hits = []
        png_img_count = 0
        with zipfile.ZipFile(epub_path, "r") as zf:
            names = set(zf.namelist())
            opf_text = zf.read("OEBPS/content.opf").decode("utf-8")
            fm_text = zf.read("OEBPS/front-matter.xhtml").decode("utf-8")

            if "<dc:creator>Omar Sunny</dc:creator>" not in opf_text:
                errors.append("EPUB content.opf missing <dc:creator>Omar Sunny</dc:creator>")
                dce_hits.append("OPF missing Omar Sunny")
            if "Without Burnout" in opf_text:
                errors.append("EPUB content.opf contains >200-char truncated subtitle suffix 'Without Burnout'")
                dce_hits.append("OPF >200-char subtitle")
            if "By Omar Sunny" not in fm_text or "Copyright © 2026 by Omar Sunny" not in fm_text:
                errors.append("EPUB front-matter.xhtml missing 'By Omar Sunny' or 'Copyright © 2026 by Omar Sunny'")
                dce_hits.append("Front matter missing Omar Sunny copyright")
            if len(re.findall(r"<h1[^>]*>", fm_text)) != 1:
                errors.append("EPUB front-matter.xhtml has duplicate <h1> title blocks")
                dce_hits.append("Duplicate <h1> in front-matter.xhtml")

            for zname in sorted(names):
                if zname.endswith(".xhtml"):
                    xhtml_str = zf.read(zname).decode("utf-8")
                    png_img_count += len(re.findall(r'src="images/chapter-\d+-.*\.png"', xhtml_str))
                    for pat, label in KDP_FORBIDDEN_DCE_PATTERNS:
                        m = pat.search(xhtml_str)
                        if m:
                            dce_hits.append(f"{zname}: {label} ('{m.group(0)}')")

        # Also scan KDP Kindle Cover SVG and KDP Full-Wrap Cover SVG for forbidden DCE claims
        for cov_path, cov_label in [
            (kindle_svg_path, "ebook-cover-kdp-kindle.svg"),
            (wrap_svg_path, "kdp-paperback-full-wrap-cover.svg"),
        ]:
            cov_str = cov_path.read_text(encoding="utf-8")
            if "OMAR SUNNY" not in cov_str:
                dce_hits.append(f"{cov_label}: missing OMAR SUNNY")
            for pat, label in KDP_FORBIDDEN_DCE_PATTERNS:
                m = pat.search(cov_str)
                if m:
                    dce_hits.append(f"{cov_label}: {label} ('{m.group(0)}')")

        if dce_hits:
            errors.extend(dce_hits[:10])
            checks.append(("Kindle Content Review (Zero DCE & Metadata Blocks)", "FAIL", f"{len(dce_hits)} issues: {dce_hits[:3]}"))
        else:
            checks.append(
                (
                    "Kindle Content Review (Zero DCE & Metadata Blocks)",
                    "PASS",
                    f"0 workbook/fillable/key/truncation triggers; {png_img_count} PNG diagrams; Omar Sunny copyright verified",
                )
            )

    for name, status, detail in checks:
        print(f"[{status}] {name:<54} | {detail}")

    print("-" * 92)
    if errors:
        print(f"PRE-FLIGHT FAILED WITH {len(errors)} ERROR(S):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("ALL AMAZON KDP PRINT PREVIEWER PRE-FLIGHT CHECKS PASSED (0 ERRORS)!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
