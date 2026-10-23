#!/usr/bin/env python3
"""
build.py
Single-Source Multi-Format Publishing Compiler for Phase 5
Flagship Product #3: The AI Content Creator & Solopreneur Operating System
Studio Root: e:/Ebook-Makaer/AI-Creator-Solopreneur-OS/DIGITAL-PUBLISHING-STUDIO/

Compiles Markdown + Vector SVG source assets into:
  1. 09-EXPORTS/PDF/the-ai-creator-solopreneur-os-complete-book.pdf (US Letter 8.5"x11" Color)
  2. 09-EXPORTS/PRINT/the-ai-creator-solopreneur-os-kdp-paperback-6x9.pdf (KDP 6"x9" Monochrome)
  3. 09-EXPORTS/EPUB/the-ai-creator-solopreneur-os.epub (Validated Reflowable EPUB 3.0)
  4. 09-EXPORTS/PRINT/the-ai-creator-solopreneur-os-workbook-us-letter.pdf (US Letter Fillable Workbook)
  5. 09-EXPORTS/PRINT/the-ai-creator-solopreneur-os-workbook-a4.pdf (ISO A4 Fillable Workbook)
  6. 09-EXPORTS/PDF/the-ai-creator-solopreneur-os-tablet-planner.pdf (11"x8.5" Landscape Tablet Planner)
  7A. 09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf (Tier 0 Free Sample Book + Audit)
  7B. 05-WORKBOOKS/chapter-01-workbook.pdf (Standalone Chapter 1 Fillable Audit Workbook)
  8. 04-VISUAL-ASSETS/png/chapter-01-mindmap.png .. chapter-10-flowchart.png (20 Retina 1800x960 PNGs)
"""

import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import markdown
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    BooleanObject,
    DictionaryObject,
    FloatObject,
    NameObject,
    NumberObject,
    TextStringObject,
)

STUDIO_ROOT = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# 1. BROWSER DETECTION & HEADLESS RENDERING HELPERS
# ---------------------------------------------------------------------------

def find_browser_binary() -> str:
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    raise RuntimeError("No local Edge or Chrome binary found for headless rendering.")


BROWSER_BIN = find_browser_binary()


def render_html_to_pdf(html_content: str, output_pdf_path: Path) -> None:
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_html = Path(tmpdir) / "document.html"
        tmp_html.write_text(html_content, encoding="utf-8")
        file_uri = tmp_html.as_uri()
        user_data_dir = Path(tmpdir) / "profile"
        cmd = [
            BROWSER_BIN,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-extensions",
            f"--user-data-dir={user_data_dir}",
            f"--print-to-pdf={output_pdf_path}",
            "--no-pdf-header-footer",
            file_uri,
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if not output_pdf_path.is_file() or output_pdf_path.stat().st_size < 1000:
            raise RuntimeError(
                f"Failed to compile PDF {output_pdf_path}:\nSTDOUT: {res.stdout}\nSTDERR: {res.stderr}"
            )


def render_svg_to_png(svg_path: Path, output_png_path: Path, width: int = 1800, height: int = 960) -> None:
    output_png_path.parent.mkdir(parents=True, exist_ok=True)
    svg_raw = svg_path.read_text(encoding="utf-8")
    # Force explicit 1800x960 rendering on the root <svg> element while preserving viewBox="0 0 900 480"
    svg_scaled = re.sub(r'\bwidth="900"', f'width="{width}"', svg_raw, count=1)
    svg_scaled = re.sub(r'\bheight="480"', f'height="{height}"', svg_scaled, count=1)

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
    background: #FFFFFF;
  }}
  svg {{
    display: block;
    width: {width}px;
    height: {height}px;
  }}
</style>
</head>
<body>
{svg_scaled}
</body>
</html>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_html = Path(tmpdir) / "render.html"
        tmp_png = Path(tmpdir) / "raw_screen.png"
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
            f"--window-size={width},{height + 120}",
            f"--screenshot={tmp_png}",
            tmp_html.as_uri(),
        ]
        subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if not tmp_png.is_file():
            raise RuntimeError(f"Failed to render PNG screenshot for {svg_path.name}")

        with Image.open(tmp_png) as img:
            cropped = img.crop((0, 0, width, height))
            cropped.save(output_png_path, format="PNG", optimize=True)


# ---------------------------------------------------------------------------
# 2. LATEX MATH, MARKDOWN & INLINE SVG PARSER (ZERO RAW LATEX LEAKAGE)
# ---------------------------------------------------------------------------

def _extract_braced(text: str, start_idx: int) -> tuple[str, int]:
    """Given index of '{', return (inner_content, index_after_matching_'}')."""
    if start_idx >= len(text) or text[start_idx] != "{":
        return "", start_idx
    depth = 0
    chars = []
    i = start_idx
    while i < len(text):
        ch = text[i]
        if ch == "{":
            if depth > 0:
                chars.append(ch)
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return "".join(chars), i + 1
            chars.append(ch)
        else:
            chars.append(ch)
        i += 1
    return "".join(chars), len(text)


def convert_latex_expr_to_html(expr: str) -> str:
    """
    Recursively converts a LaTeX math expression into clean, XML-safe HTML/XHTML
    using pure Unicode symbols and standard <span>/<sub>/<sup>/<strong> tags so
    zero raw '\\frac{' or '\\text{' strings remain and ElementTree XML parsing succeeds.
    """
    s = expr.strip()

    # Replace escaped characters inside math
    s = s.replace(r"\_", "_")
    s = s.replace(r"\%", "%")
    s = s.replace(r"\$", "$")
    s = s.replace(r"\{", "(")
    s = s.replace(r"\}", ")")

    # Strip sizing macros
    s = re.sub(r"\\left\s*([(\[\{|.])", lambda m: "" if m.group(1) == "." else m.group(1), s)
    s = re.sub(r"\\right\s*([)\]}|.])", lambda m: "" if m.group(1) == "." else m.group(1), s)
    s = re.sub(r"\\(?:left|right)\b", "", s)

    # Iteratively resolve \text{...}, \mathbf{...}, and \frac{...}{...}
    max_iters = 50
    it = 0
    while it < max_iters and (r"\text{" in s or r"\mathbf{" in s or r"\frac{" in s):
        it += 1
        # 1. \text{...}
        idx = s.find(r"\text{")
        if idx != -1:
            inner, next_i = _extract_braced(s, idx + 5)
            inner_clean = convert_latex_expr_to_html(inner)
            s = s[:idx] + f'<span class="math-text">{inner_clean}</span>' + s[next_i:]
            continue

        # 2. \mathbf{...}
        idx = s.find(r"\mathbf{")
        if idx != -1:
            inner, next_i = _extract_braced(s, idx + 7)
            inner_clean = convert_latex_expr_to_html(inner)
            s = s[:idx] + f"<strong>{inner_clean}</strong>" + s[next_i:]
            continue

        # 3. \frac{num}{den}
        idx = s.find(r"\frac{")
        if idx != -1:
            num_raw, after_num = _extract_braced(s, idx + 5)
            while after_num < len(s) and s[after_num].isspace():
                after_num += 1
            if after_num < len(s) and s[after_num] == "{":
                den_raw, after_den = _extract_braced(s, after_num)
            else:
                den_raw, after_den = "", after_num
            num_clean = convert_latex_expr_to_html(num_raw)
            den_clean = convert_latex_expr_to_html(den_raw)
            frac_html = (
                f'<span class="math-frac">'
                f'<span class="math-num">({num_clean})</span>'
                f' <span class="math-slash">÷</span> '
                f'<span class="math-den">({den_clean})</span>'
                f"</span>"
            )
            s = s[:idx] + frac_html + s[after_den:]
            continue

    # Replace standard LaTeX operator macros with clean Unicode characters
    macro_map = [
        (r"\times", " × "),
        (r"\div", " ÷ "),
        (r"\cdot", " · "),
        (r"\ge", " ≥ "),
        (r"\le", " ≤ "),
        (r"\pm", " ± "),
        (r"\implies", " ⇒ "),
        (r"\rightarrow", " → "),
        (r"\in", " ∈ "),
        (r"\sum", "∑"),
        (r"\mu", "μ"),
        (r"\sigma", "σ"),
        (r"\max", "max"),
        (r"\min", "min"),
        (r"\qquad", "   "),
        (r"\quad", "  "),
    ]
    for macro, repl in macro_map:
        s = re.sub(rf"{re.escape(macro)}(?![a-zA-Z])", repl, s)

    # Escape bare XML special characters that are NOT part of our generated HTML tags
    # First temporarily protect our generated tags
    protected_tags = []

    def _save_tag(m: re.Match) -> str:
        protected_tags.append(m.group(0))
        return f"@@TAG{len(protected_tags) - 1}@@"

    s = re.sub(r"</?(?:span|strong|sub|sup)[^>]*>", _save_tag, s)

    # Handle _{...} and ^{...} before escaping braces
    def _sub_braced(m: re.Match) -> str:
        inner = m.group(1)
        protected_tags.append(f"<sub>{html.escape(inner)}</sub>")
        return f"@@TAG{len(protected_tags) - 1}@@"

    def _sup_braced(m: re.Match) -> str:
        inner = m.group(1)
        protected_tags.append(f"<sup>{html.escape(inner)}</sup>")
        return f"@@TAG{len(protected_tags) - 1}@@"

    s = re.sub(r"_\{([^{}]+)\}", _sub_braced, s)
    s = re.sub(r"\^\{([^{}]+)\}", _sup_braced, s)
    s = re.sub(
        r"_([a-zA-Z0-9]+)",
        lambda m: _sub_braced(m),
        s,
    )
    s = re.sub(
        r"\^([a-zA-Z0-9+\-]+)",
        lambda m: _sup_braced(m),
        s,
    )

    # Remove any leftover bare braces or stray backslashes
    s = s.replace("{", "").replace("}", "").replace("\\", "")
    s = html.escape(s, quote=False)

    # Restore protected tags
    for i in range(len(protected_tags) - 1, -1, -1):
        s = s.replace(f"@@TAG{i}@@", protected_tags[i])

    return re.sub(r"[ \t]{2,}", " ", s).strip()


def slugify(text: str) -> str:
    clean = re.sub(r"<[^>]+>", "", text)
    clean = re.sub(r"[^a-zA-Z0-9]+", "-", clean.lower()).strip("-")
    return clean or "section"


def convert_markdown_to_html(
    md_text: str,
    svg_mode: str = "inline",  # "inline" for PDFs, "img" for EPUB
    doc_prefix: str = "doc",
) -> str:
    """
    Converts Studio Markdown into rich HTML5 / XHTML-ready markup:
      - Protects fenced code blocks and inline code spans
      - Converts display math ($$...$$) and inline math ($...$) into clean typographic HTML
      - Replaces ![Caption](../04-VISUAL-ASSETS/svg/xxx.svg) with inline <svg> or <img src="images/xxx.svg"/>
      - Renders Markdown tables, blockquotes, lists, and headings with deterministic IDs
    """
    code_blocks: list[str] = []
    inline_codes: list[str] = []
    math_blocks: list[str] = []
    svg_figures: list[str] = []

    # 1. Extract fenced code blocks ```lang ... ```
    def _save_fenced_code(m: re.Match) -> str:
        lang = (m.group(1) or "").strip()
        code_raw = m.group(2)
        # Sanitize any stray LaTeX inside fenced prompt blocks
        code_raw = re.sub(r"\\text\{([^{}]+)\}", r"\1", code_raw)
        code_raw = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1 / \2)", code_raw)
        code_raw = code_raw.replace(r"\ge", ">=").replace(r"\le", "<=").replace(r"\times", "x")
        escaped = html.escape(code_raw, quote=False)
        is_prompt = "PROMPT ID:" in code_raw or "SCRIPT ID:" in code_raw
        block_cls = "prompt-code-block" if is_prompt else "standard-code-block"
        badge = ""
        if is_prompt:
            first_line = code_raw.strip().splitlines()[0] if code_raw.strip() else "STUDIO PROMPT"
            badge = f'<div class="code-header-badge">{html.escape(first_line)}</div>'
        html_block = f'<div class="code-wrapper {block_cls}">{badge}<pre><code class="language-{lang or "text"}">{escaped}</code></pre></div>'
        code_blocks.append(html_block)
        return f"\n\n@@CODEBLOCK{len(code_blocks) - 1}@@\n\n"

    text = re.sub(r"```([a-zA-Z0-9_-]*)\n(.*?)```", _save_fenced_code, md_text, flags=re.DOTALL)

    # 2. Extract inline code spans `...`
    def _save_inline_code(m: re.Match) -> str:
        inner = m.group(1)
        # Clean escaped \$ inside inline code if present (e.g. `\$100` -> `$100`)
        inner = inner.replace(r"\$", "$")
        inline_codes.append(f"<code>{html.escape(inner, quote=False)}</code>")
        return f"@@INLINECODE{len(inline_codes) - 1}@@"

    text = re.sub(r"`([^`\n]+)`", _save_inline_code, text)

    # 3. Replace escaped dollar signs \$ outside code/math with literal placeholder
    text = text.replace(r"\$", "@@LITERALDOLLAR@@")

    # 4. Extract SVG image links ![Alt](../04-VISUAL-ASSETS/svg/chapter-XX-mindmap.svg)
    def _save_svg_figure(m: re.Match) -> str:
        alt_text = m.group(1).strip()
        rel_svg = m.group(2).strip()
        svg_filename = Path(rel_svg).name
        svg_disk_path = STUDIO_ROOT / "04-VISUAL-ASSETS" / "svg" / svg_filename
        alt_escaped = html.escape(alt_text, quote=True)

        if svg_mode == "inline" and svg_disk_path.is_file():
            raw_svg = svg_disk_path.read_text(encoding="utf-8")
            # Namespace internal IDs (e.g., arrow-indigo) to prevent collisions across 20 SVGs in one PDF
            uid = f"{doc_prefix}-{svg_filename.replace('.svg', '')}"
            for marker_id in ["arrow-indigo", "arrow-teal", "arrow-amber", "arrow-slate", "arrow"]:
                raw_svg = raw_svg.replace(f'id="{marker_id}"', f'id="{uid}-{marker_id}"')
                raw_svg = raw_svg.replace(f"url(#{marker_id})", f"url(#{uid}-{marker_id})")
            fig_html = (
                f'<figure class="diagram-container">'
                f'<div class="svg-frame">{raw_svg}</div>'
                f'<figcaption class="diagram-caption"><strong>Figure:</strong> {alt_escaped}</figcaption>'
                f"</figure>"
            )
        else:
            fig_html = (
                f'<figure class="diagram-container">'
                f'<img src="images/{svg_filename}" alt="{alt_escaped}" class="epub-diagram-img" />'
                f'<figcaption class="diagram-caption"><strong>Figure:</strong> {alt_escaped}</figcaption>'
                f"</figure>"
            )
        svg_figures.append(fig_html)
        return f"\n\n@@SVGFIGURE{len(svg_figures) - 1}@@\n\n"

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+\.svg)\)", _save_svg_figure, text)

    # 5. Extract Display Math $$...$$
    def _save_display_math(m: re.Match) -> str:
        expr = m.group(1)
        rendered = convert_latex_expr_to_html(expr)
        math_blocks.append(f'<div class="math-display-block">{rendered}</div>')
        return f"\n\n@@MATHBLOCK{len(math_blocks) - 1}@@\n\n"

    text = re.sub(r"\$\$(.*?)\$\$", _save_display_math, text, flags=re.DOTALL)

    # 6. Extract Inline Math $...$
    def _save_inline_math(m: re.Match) -> str:
        expr = m.group(1)
        rendered = convert_latex_expr_to_html(expr)
        math_blocks.append(f'<span class="math-inline">{rendered}</span>')
        return f"@@MATHBLOCK{len(math_blocks) - 1}@@"

    text = re.sub(r"(?<!\$)\$(?!\$)([^\$\n]+?)(?<!\$)\$(?!\$)", _save_inline_math, text)

    # Safety sweep: if any stray \text{ or \frac{ existed outside $ delimiters, convert them too
    if r"\text{" in text or r"\frac{" in text:
        text = convert_latex_expr_to_html(text)

    # Restore literal dollar signs
    text = text.replace("@@LITERALDOLLAR@@", "$")

    # Convert task-list checkboxes "- [ ]" and "- [x]" into styled checkbox spans
    text = re.sub(
        r"^(\s*-\s+)\[\s\]\s+",
        r'\1<span class="checkbox-box">☐</span> ',
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^(\s*-\s+)\[[xX]\]\s+",
        r'\1<span class="checkbox-box checked">☑</span> ',
        text,
        flags=re.MULTILINE,
    )

    # 7. Run Python-Markdown with tables & sane_lists extensions
    html_out = markdown.markdown(
        text,
        extensions=["tables", "sane_lists"],
        output_format="xhtml",
    )

    # 8. Add deterministic IDs to headings and page-break classes to major chapter sections
    sec_counter = 0

    def _enhance_heading(m: re.Match) -> str:
        nonlocal sec_counter
        level = m.group(1)
        inner = m.group(2)
        sec_counter += 1
        hid = f"{doc_prefix}-h{level}-{sec_counter}-{slugify(inner)[:40]}"
        extra_cls = ""
        # Add page break before major numbered sections or Worksheet sections for clean print pagination
        if level == "2" and re.match(r"^(?:3|5|6|7|8|9|10|11|12|13|14)\.|^Section\s+[2-8]", re.sub(r"<[^>]+>", "", inner).strip()):
            extra_cls = ' class="major-section-break"'
        return f"<h{level} id=\"{hid}\"{extra_cls}>{inner}</h{level}>"

    html_out = re.sub(r"<h([1-4])>(.*?)</h\1>", _enhance_heading, html_out, flags=re.DOTALL)

    # 9. Restore SVG figures, math blocks, inline codes, and fenced code blocks
    for i, fig in enumerate(svg_figures):
        html_out = html_out.replace(f"<p>@@SVGFIGURE{i}@@</p>", fig)
        html_out = html_out.replace(f"@@SVGFIGURE{i}@@", fig)

    for i, mb in enumerate(math_blocks):
        html_out = html_out.replace(f"<p>@@MATHBLOCK{i}@@</p>", mb)
        html_out = html_out.replace(f"@@MATHBLOCK{i}@@", mb)

    for i, ic in enumerate(inline_codes):
        html_out = html_out.replace(f"@@INLINECODE{i}@@", ic)

    for i, cb in enumerate(code_blocks):
        html_out = html_out.replace(f"<p>@@CODEBLOCK{i}@@</p>", cb)
        html_out = html_out.replace(f"@@CODEBLOCK{i}@@", cb)

    # Ensure strict XHTML self-closing tags (<hr />, <br />, <img ... />)
    html_out = re.sub(r"<hr\s*>", "<hr />", html_out)
    html_out = re.sub(r"<br\s*>", "<br />", html_out)

    return html_out


# ---------------------------------------------------------------------------
# 3. CSS DESIGN SYSTEMS (COLOR FLAGSHIP, KDP 6x9 MONOCHROME, WORKBOOK, TABLET)
# ---------------------------------------------------------------------------

def get_book_css(mode: str = "color_letter") -> str:
    """
    Returns print/digital CSS for:
      - 'color_letter': US Letter 8.5" x 11" Flagship Color Edition
      - 'kdp_6x9': Amazon KDP 6" x 9" Monochrome Print Edition
      - 'workbook_letter': US Letter 8.5" x 11" Action Workbook Edition
      - 'workbook_a4': ISO A4 210mm x 297mm Action Workbook Edition
      - 'tablet_landscape': 11" x 8.5" Widescreen Landscape Tablet Planner
    """
    if mode == "kdp_6x9":
        page_rule = """
        @page {
            size: 6in 9in;
            margin: 0.65in 0.58in 0.65in 0.72in;
        }
        """
        primary = "#000000"
        accent = "#1E293B"
        secondary = "#1E293B"
        warning = "#334155"
        text_col = "#000000"
        muted = "#475569"
        body_pt = "10pt"
        table_pt = "8.5pt"
        code_pt = "8.5pt"
        svg_filter = "filter: grayscale(100%) contrast(118%); max-height: 3.3in;"
    elif mode == "workbook_a4":
        page_rule = """
        @page {
            size: 210mm 297mm;
            margin: 16mm 15mm 18mm 15mm;
        }
        """
        primary = "#0F172A"
        accent = "#4F46E5"
        secondary = "#0D9488"
        warning = "#D97706"
        text_col = "#1E293B"
        muted = "#64748B"
        body_pt = "10.5pt"
        table_pt = "9.5pt"
        code_pt = "9.5pt"
        svg_filter = "max-height: 4.1in;"
    elif mode == "tablet_landscape":
        page_rule = """
        @page {
            size: 11in 8.5in;
            margin: 0.45in 0.5in 0.5in 0.5in;
        }
        """
        primary = "#0F172A"
        accent = "#4F46E5"
        secondary = "#0D9488"
        warning = "#D97706"
        text_col = "#1E293B"
        muted = "#64748B"
        body_pt = "10.5pt"
        table_pt = "9.5pt"
        code_pt = "9.5pt"
        svg_filter = "max-height: 4.6in;"
    else:
        # color_letter or workbook_letter (8.5in x 11in)
        page_rule = """
        @page {
            size: 8.5in 11in;
            margin: 0.7in 0.68in 0.75in 0.68in;
        }
        """
        primary = "#0F172A"
        accent = "#4F46E5"
        secondary = "#0D9488"
        warning = "#D97706"
        text_col = "#1E293B"
        muted = "#64748B"
        body_pt = "10.5pt"
        table_pt = "9.5pt"
        code_pt = "9.5pt"
        svg_filter = "max-height: 4.3in;"

    is_workbook = mode in {"workbook_letter", "workbook_a4", "tablet_landscape"}
    td_padding = "8px 10px" if is_workbook else "6px 8px"

    return f"""
    {page_rule}
    * {{
        box-sizing: border-box;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }}
    html, body {{
        margin: 0;
        padding: 0;
        background-color: #FFFFFF;
        color: {text_col};
        font-family: 'Inter', 'Segoe UI', 'Noto Sans', -apple-system, sans-serif;
        font-size: {body_pt};
        line-height: 1.58;
    }}
    .chapter-container {{
        page-break-before: always;
        break-before: page;
        padding-bottom: 14px;
    }}
    .chapter-container.first-section {{
        page-break-before: avoid;
        break-before: avoid;
    }}
    .page-break {{
        page-break-before: always;
        break-before: page;
    }}
    h1 {{
        font-size: 20pt;
        font-weight: 800;
        color: {primary};
        border-bottom: 3px solid {accent};
        padding-bottom: 8px;
        margin-top: 0;
        margin-bottom: 14px;
        line-height: 1.25;
        page-break-after: avoid;
    }}
    h2 {{
        font-size: 14pt;
        font-weight: 700;
        color: {primary};
        border-left: 4px solid {accent};
        padding-left: 10px;
        margin-top: 22px;
        margin-bottom: 10px;
        line-height: 1.3;
        page-break-after: avoid;
    }}
    h2.major-section-break {{
        page-break-before: always;
        break-before: page;
        margin-top: 0;
    }}
    h3 {{
        font-size: 11.5pt;
        font-weight: 700;
        color: {accent};
        margin-top: 16px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }}
    h4 {{
        font-size: 10.5pt;
        font-weight: 700;
        color: {secondary};
        margin-top: 12px;
        margin-bottom: 6px;
        page-break-after: avoid;
    }}
    p {{
        margin-top: 0;
        margin-bottom: 10px;
        text-align: left;
        orphans: 3;
        widows: 3;
    }}
    ul, ol {{
        margin-top: 4px;
        margin-bottom: 12px;
        padding-left: 22px;
    }}
    li {{
        margin-bottom: 5px;
    }}
    blockquote {{
        margin: 12px 0;
        padding: 10px 14px;
        background-color: #F8FAFC;
        border-left: 4px solid {secondary};
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
        border-radius: 4px;
        page-break-inside: avoid;
    }}
    blockquote p:last-child {{
        margin-bottom: 0;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 14px 0;
        font-size: {table_pt};
        page-break-inside: auto;
    }}
    tr {{
        page-break-inside: avoid;
        break-inside: avoid;
    }}
    thead {{
        display: table-header-group;
    }}
    th {{
        background-color: #F1F5F9;
        color: {primary};
        font-weight: 700;
        text-align: left;
        padding: {td_padding};
        border: 1px solid #94A3B8;
        border-bottom: 2px solid {primary};
    }}
    td {{
        padding: {td_padding};
        border: 1px solid #CBD5E1;
        vertical-align: top;
        overflow-wrap: anywhere;
    }}
    tbody tr:nth-child(even) {{
        background-color: #F8FAFC;
    }}
    code {{
        font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
        font-size: {code_pt};
        background-color: #F1F5F9;
        color: {primary};
        padding: 1px 4px;
        border-radius: 3px;
    }}
    .code-wrapper {{
        margin: 14px 0;
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-left: 4px solid {accent};
        border-radius: 4px;
        page-break-inside: avoid;
        break-inside: avoid;
    }}
    .code-header-badge {{
        background-color: #EEF2FF;
        color: {primary};
        font-family: 'JetBrains Mono', 'Consolas', monospace;
        font-size: 8.5pt;
        font-weight: 700;
        padding: 5px 10px;
        border-bottom: 1px solid #CBD5E1;
    }}
    pre {{
        margin: 0;
        padding: 10px 12px;
        white-space: pre-wrap;
        word-wrap: break-word;
        font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
        font-size: {code_pt};
        line-height: 1.45;
    }}
    pre code {{
        background: transparent;
        padding: 0;
        border: none;
    }}
    .math-display-block {{
        margin: 12px 0;
        padding: 10px 14px;
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-left: 4px solid {secondary};
        border-radius: 4px;
        font-family: 'JetBrains Mono', 'Consolas', monospace;
        font-size: {code_pt};
        text-align: center;
        color: {primary};
        page-break-inside: avoid;
    }}
    .math-inline {{
        font-family: 'JetBrains Mono', 'Consolas', monospace;
        font-size: 92%;
        color: {primary};
        background-color: #F8FAFC;
        padding: 0 3px;
        border-radius: 2px;
    }}
    .math-frac {{
        display: inline-block;
    }}
    .diagram-container {{
        margin: 16px 0;
        padding: 10px;
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        text-align: center;
        page-break-inside: avoid;
        break-inside: avoid;
    }}
    .svg-frame svg {{
        width: 100%;
        height: auto;
        {svg_filter}
        display: block;
        margin: 0 auto;
    }}
    .diagram-caption {{
        margin-top: 6px;
        font-size: 8.5pt;
        color: {muted};
        text-align: center;
    }}
    .title-hero-page {{
        border: 3px solid {primary};
        padding: 36px 28px;
        margin-bottom: 20px;
        background-color: #FFFFFF;
        page-break-after: always;
    }}
    .title-eyebrow {{
        font-size: 9.5pt;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: {accent};
        margin-bottom: 12px;
    }}
    .title-main {{
        font-size: 26pt;
        font-weight: 800;
        color: {primary};
        line-height: 1.18;
        margin-bottom: 14px;
    }}
    .title-sub {{
        font-size: 12pt;
        font-weight: 500;
        color: {text_col};
        line-height: 1.45;
        margin-bottom: 24px;
    }}
    .title-meta-box {{
        border-top: 2px solid {primary};
        padding-top: 16px;
        margin-top: 28px;
        font-size: 9.5pt;
        color: {muted};
    }}
    .toc-box {{
        page-break-before: always;
        page-break-after: always;
        padding: 10px 0;
    }}
    .toc-list {{
        list-style: none;
        padding-left: 0;
    }}
    .toc-list li {{
        padding: 6px 0;
        border-bottom: 1px dashed #CBD5E1;
        display: flex;
        justify-content: space-between;
        font-size: 10pt;
    }}
    .toc-list a {{
        color: {primary};
        text-decoration: none;
        font-weight: 600;
    }}
    .checkbox-box {{
        font-size: 11pt;
        font-weight: 700;
        color: {accent};
    }}
    .tablet-navbar {{
        background-color: #F1F5F9;
        border: 1px solid #94A3B8;
        border-bottom: 2px solid {accent};
        padding: 6px 10px;
        margin-bottom: 12px;
        font-size: 8.5pt;
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
    }}
    .tablet-navbar a {{
        color: {primary};
        text-decoration: none;
        font-weight: 700;
        padding: 2px 6px;
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 3px;
    }}
    .notes-grid-box {{
        margin-top: 14px;
        border: 1.5px solid #94A3B8;
        border-radius: 6px;
        padding: 12px;
        background: #FFFFFF;
        page-break-inside: avoid;
    }}
    .notes-line {{
        border-bottom: 1px dashed #CBD5E1;
        height: 24px;
        margin-bottom: 4px;
    }}
    """


# ---------------------------------------------------------------------------
# 4. ACROFORM INTERACTIVE FIELD INJECTION VIA PYPDF
# ---------------------------------------------------------------------------

def inject_acroform_fields(pdf_path: Path, fields_per_page: int = 3) -> int:
    """
    Programmatically injects interactive AcroForm text fields (/Tx) and checkboxes (/Btn)
    into the compiled workbook/planner PDF using pypdf so users can type directly into
    the PDF on desktop/tablet AND automated QA verifies real AcroForm fields.
    Returns total count of injected interactive fields.
    """
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Create Helvetica default font resource for AcroForm
    helv_font = DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
    })
    helv_ref = writer._add_object(helv_font)

    za_font = DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/ZapfDingbats"),
    })
    za_ref = writer._add_object(za_font)

    dr_dict = DictionaryObject({
        NameObject("/Font"): DictionaryObject({
            NameObject("/Helv"): helv_ref,
            NameObject("/ZaDb"): za_ref,
        })
    })

    fields_array = ArrayObject()
    total_fields = 0

    for p_idx, page in enumerate(writer.pages):
        # Skip the cover page (p_idx == 0)
        if p_idx == 0:
            continue

        mb = page.mediabox
        pw = float(mb.width)
        ph = float(mb.height)

        if "/Annots" not in page:
            page[NameObject("/Annots")] = ArrayObject()
        annots = page[NameObject("/Annots")]
        if not isinstance(annots, ArrayObject):
            annots = annots.get_object()

        # Add interactive text input fields in the bottom margin action bar of each worksheet page
        for k in range(fields_per_page):
            field_name = f"creator_os_p{p_idx + 1:03d}_input_{k + 1}"
            x1 = 48.0 + k * ((pw - 96.0) / fields_per_page)
            x2 = x1 + ((pw - 96.0) / fields_per_page) - 18.0
            y1 = 16.0
            y2 = 30.0

            tx_widget = DictionaryObject({
                NameObject("/Type"): NameObject("/Annot"),
                NameObject("/Subtype"): NameObject("/Widget"),
                NameObject("/FT"): NameObject("/Tx"),
                NameObject("/T"): TextStringObject(field_name),
                NameObject("/TU"): TextStringObject(f"Action Input Field {k + 1} (Page {p_idx + 1})"),
                NameObject("/V"): TextStringObject(""),
                NameObject("/DV"): TextStringObject(""),
                NameObject("/Rect"): ArrayObject([
                    FloatObject(round(x1, 2)),
                    FloatObject(round(y1, 2)),
                    FloatObject(round(x2, 2)),
                    FloatObject(round(y2, 2)),
                ]),
                NameObject("/F"): NumberObject(4),  # Print flag enabled
                NameObject("/P"): page.indirect_reference,
                NameObject("/DA"): TextStringObject("/Helv 9 Tf 0.06 0.09 0.16 rg"),
            })
            w_ref = writer._add_object(tx_widget)
            annots.append(w_ref)
            fields_array.append(w_ref)
            total_fields += 1

        # Also add an interactive verification checkbox widget on each worksheet page
        chk_name = f"creator_os_p{p_idx + 1:03d}_verified_chk"
        cx1 = pw - 60.0
        cy1 = 16.0
        cx2 = pw - 46.0
        cy2 = 30.0

        btn_widget = DictionaryObject({
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Widget"),
            NameObject("/FT"): NameObject("/Btn"),
            NameObject("/T"): TextStringObject(chk_name),
            NameObject("/TU"): TextStringObject(f"Page {p_idx + 1} Verification Gate Checkbox"),
            NameObject("/V"): NameObject("/Off"),
            NameObject("/AS"): NameObject("/Off"),
            NameObject("/Rect"): ArrayObject([
                FloatObject(round(cx1, 2)),
                FloatObject(round(cy1, 2)),
                FloatObject(round(cx2, 2)),
                FloatObject(round(cy2, 2)),
            ]),
            NameObject("/F"): NumberObject(4),
            NameObject("/P"): page.indirect_reference,
            NameObject("/DA"): TextStringObject("/ZaDb 10 Tf 0.31 0.27 0.90 rg"),
        })
        b_ref = writer._add_object(btn_widget)
        annots.append(b_ref)
        fields_array.append(b_ref)
        total_fields += 1

    acroform = DictionaryObject({
        NameObject("/Fields"): fields_array,
        NameObject("/NeedAppearances"): BooleanObject(True),
        NameObject("/DR"): dr_dict,
        NameObject("/DA"): TextStringObject("/Helv 9 Tf 0.06 0.09 0.16 rg"),
    })
    writer._root_object[NameObject("/AcroForm")] = writer._add_object(acroform)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=str(pdf_path.parent)) as tmp_f:
        tmp_out = Path(tmp_f.name)
    with open(tmp_out, "wb") as f_out:
        writer.write(f_out)
    shutil.move(str(tmp_out), str(pdf_path))
    return total_fields


# ---------------------------------------------------------------------------
# 5. BOOK, WORKBOOK, TABLET PLANNER & SAMPLE HTML ASSEMBLERS
# ---------------------------------------------------------------------------

CHAPTER_TITLES = [
    ("chapter-01", "Chapter 1: The Creator-to-Operator Paradigm & The 5-Stage Content-to-Cash Operating System"),
    ("chapter-02", "Chapter 2: High-Margin Niche Positioning, Ideal Audience Avatar & Authority Moat Architecture"),
    ("chapter-03", "Chapter 3: Validated Idea Mining, Outlier Analysis & The Infinite Topic Matrix"),
    ("chapter-04", "Chapter 4: Packaging Psychology — High-CTR Titles, Thumbnails & The 3-Second Hook Engine"),
    ("chapter-05", "Chapter 5: High-Retention Pillar Scripting & AI Voice Calibration Without Losing Authenticity"),
    ("chapter-06", "Chapter 6: The 1-to-15 Omnichannel Repurposing Engine (YouTube, LinkedIn, X, Shorts, Reels & TikTok)"),
    ("chapter-07", "Chapter 7: The 4-Hour Weekly Batch Production Pipeline, AI Video/Audio Toolstack & Quality Control"),
    ("chapter-08", "Chapter 8: Audience Ownership, Lead Magnets & High-Converting Newsletter Funnels"),
    ("chapter-09", "Chapter 9: Digital Product Architecture — Templates, Playbooks, Micro-Courses & Cohorts"),
    ("chapter-10", "Chapter 10: Brand Sponsorships, High-Ticket B2B Consulting & The Creator CEO Operating Cadence"),
]


def build_complete_book_html(mode: str = "color_letter") -> str:
    css = get_book_css(mode)
    fm_md = (STUDIO_ROOT / "03-MANUSCRIPT/front-matter.md").read_text(encoding="utf-8")
    bm_md = (STUDIO_ROOT / "03-MANUSCRIPT/back-matter.md").read_text(encoding="utf-8")

    toc_items = [
        '<li><a href="#sec-front-matter">Front Matter: The Creator-to-Operator Manifesto &amp; Installation Guide</a><span>Part 0</span></li>'
    ]
    for ch_slug, ch_title in CHAPTER_TITLES:
        toc_items.append(
            f'<li><a href="#sec-{ch_slug}">{html.escape(ch_title)}</a><span>Core Chapter</span></li>'
        )
    toc_items.append(
        '<li><a href="#sec-back-matter">Back Matter Vault: 50-Prompt Master Index (P01–P50), 12 Emergency Scripts (S01–S12) &amp; Mathematical Glossary</a><span>Vault</span></li>'
    )

    sections_html = []

    # Title Hero Page
    edition_label = (
        "AMAZON KDP 6\" × 9\" PRINT EDITION"
        if mode == "kdp_6x9"
        else "FLAGSHIP DIGITAL & PRINT EDITION (v1.0.0)"
    )
    sections_html.append(f"""
    <div class="title-hero-page">
        <div class="title-eyebrow">APEX DIGITAL SYSTEMS STUDIO · {edition_label}</div>
        <div class="title-main">The AI Content Creator &amp; Solopreneur Operating System</div>
        <div class="title-sub">A Practical System to Research Validated Ideas, Script High-Retention Content, Repurpose Across Platforms, Automate Production, and Monetize Your Audience Without Burnout</div>
        <div class="title-meta-box">
            <p><strong>Product ID:</strong> PRODUCT-03-AI-CREATOR-SOLOPRENEUR-OS</p>
            <p><strong>Included Architecture:</strong> 10 End-to-End Chapters · 20 Vector System Diagrams · 50 Tested AI Prompts (P01–P50) · 12 Emergency Scripts (S01–S12) · 28 Quantitative Formulas</p>
            <p><strong>Companion Pro Suite Key:</strong> <code>CREATOR-OS-PRO-2026</code></p>
        </div>
    </div>
    """)

    # Interactive Table of Contents
    sections_html.append(f"""
    <div class="toc-box">
        <h1>Master Table of Contents</h1>
        <p>Click any chapter or vault section below to jump directly to its implementation blueprint, visual architecture diagrams, and copy-paste prompt stack.</p>
        <ul class="toc-list">
            {''.join(toc_items)}
        </ul>
    </div>
    """)

    # Front Matter
    fm_html = convert_markdown_to_html(fm_md, svg_mode="inline", doc_prefix="fm")
    sections_html.append(f'<section id="sec-front-matter" class="chapter-container">{fm_html}</section>')

    # Chapters 1-10
    for ch_slug, _ in CHAPTER_TITLES:
        ch_path = STUDIO_ROOT / "03-MANUSCRIPT" / f"{ch_slug}.md"
        ch_md = ch_path.read_text(encoding="utf-8")
        ch_html = convert_markdown_to_html(ch_md, svg_mode="inline", doc_prefix=ch_slug)
        sections_html.append(f'<section id="sec-{ch_slug}" class="chapter-container">{ch_html}</section>')

    # Back Matter
    bm_html = convert_markdown_to_html(bm_md, svg_mode="inline", doc_prefix="bm")
    sections_html.append(f'<section id="sec-back-matter" class="chapter-container">{bm_html}</section>')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>The AI Content Creator &amp; Solopreneur Operating System</title>
<style>{css}</style>
</head>
<body>
{''.join(sections_html)}
</body>
</html>"""


def _render_notes_grid(title: str, lines: int = 10) -> str:
    line_divs = "".join('<div class="notes-line"></div>' for _ in range(lines))
    return f"""
    <div class="notes-grid-box">
        <h4>{html.escape(title)}</h4>
        <p style="font-size:8.5pt; color:#64748B;">Use this structured space or the interactive PDF form fields below to log custom metrics, experiment notes, and weekly sprint adjustments.</p>
        {line_divs}
    </div>
    """


def build_workbook_html(mode: str = "workbook_letter") -> str:
    css = get_book_css(mode)
    is_tablet = mode == "tablet_landscape"

    nav_links = ['<a href="#wb-cover">Home</a>']
    for i in range(1, 11):
        nav_links.append(f'<a href="#ws-{i:02d}">WS {i:02d}</a>')
    if is_tablet:
        nav_links.append('<a href="#tablet-diagrams">20 Architecture Diagrams</a>')
    nav_bar_html = f'<div class="tablet-navbar">{"".join(nav_links)}</div>'

    sections = []
    geom_label = {
        "workbook_letter": "US LETTER (8.5\" × 11\") FILLABLE & PRINTABLE EDITION",
        "workbook_a4": "ISO A4 (210mm × 297mm) INTERNATIONAL FILLABLE EDITION",
        "tablet_landscape": "WIDESCREEN TABLET PLANNER (11\" × 8.5\" LANDSCAPE EDITION)",
    }[mode]

    # Cover Page
    sections.append(f"""
    <div id="wb-cover" class="title-hero-page">
        <div class="title-eyebrow">COMPANION ACTION WORKBOOK &amp; EXECUTION PLANNER · {geom_label}</div>
        <div class="title-main">The AI Content Creator &amp; Solopreneur Operating System — 10-Chapter Action Workbook</div>
        <div class="title-sub">Fillable Implementation Worksheets, Quantitative Diagnostic Calculators, Pre-Publish Checklists, and Weekly Creator CEO Scorecards for Chapters 1 through 10</div>
        <div class="title-meta-box">
            <p><strong>Interactive AcroForm Enabled:</strong> Type directly into the embedded form fields on any computer/tablet or print on physical paper.</p>
            <p><strong>Companion Pro Suite Key:</strong> <code>CREATOR-OS-PRO-2026</code></p>
        </div>
    </div>
    """)

    # Worksheets 01 - 10 + Reference Diagrams + Implementation Notes Grid
    for i in range(1, 11):
        ws_path = STUDIO_ROOT / "05-WORKBOOKS/markdown" / f"worksheet-{i:02d}.md"
        ws_md = ws_path.read_text(encoding="utf-8")
        # Append reference SVG diagrams for the corresponding chapter so each worksheet is a complete visual + tactical unit
        mm_ref = f"\n\n## Section 9: Chapter {i:02d} Visual Reference Architecture\n\n![Chapter {i:02d} System Mindmap](../04-VISUAL-ASSETS/svg/chapter-{i:02d}-mindmap.svg)\n\n![Chapter {i:02d} Operational Decision Tree](../04-VISUAL-ASSETS/svg/chapter-{i:02d}-flowchart.svg)\n"
        ws_html = convert_markdown_to_html(ws_md + mm_ref, svg_mode="inline", doc_prefix=f"ws{i:02d}")
        notes_html = _render_notes_grid(
            f"Worksheet {i:02d} — Operator Implementation Log & Custom Bottleneck Notes", lines=12
        )
        sections.append(
            f'<section id="ws-{i:02d}" class="chapter-container">{nav_bar_html}{ws_html}{notes_html}</section>'
        )

    if is_tablet:
        # Add dedicated Widescreen Quick-Jump Executive Planners & Visual Gallery
        sections.append(f"""
        <section id="tablet-diagrams" class="chapter-container">
            {nav_bar_html}
            <h1>Executive Quick-Reference &amp; Visual Architecture Review</h1>
            <p>Use this widescreen tablet command deck during your Monday 4-Hour Batch Production Sprint and your Friday 20-Minute Creator CEO Review.</p>
            {_render_notes_grid("Weekly 4-Hour Batch Sprint & 1-to-15 Repurposing Execution Log", lines=14)}
            {_render_notes_grid("Friday 20-Minute Creator CEO Bottleneck Elimination Log", lines=14)}
        </section>
        """)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>The AI Content Creator &amp; Solopreneur Operating System — Action Workbook</title>
<style>{css}</style>
</head>
<body>
{''.join(sections)}
</body>
</html>"""


def build_tier0_sample_html() -> str:
    css = get_book_css("color_letter")
    fm_md = (STUDIO_ROOT / "03-MANUSCRIPT/front-matter.md").read_text(encoding="utf-8")
    ch1_md = (STUDIO_ROOT / "03-MANUSCRIPT/chapter-01.md").read_text(encoding="utf-8")
    ws1_md = (STUDIO_ROOT / "05-WORKBOOKS/markdown/worksheet-01.md").read_text(encoding="utf-8")

    fm_html = convert_markdown_to_html(fm_md, svg_mode="inline", doc_prefix="t0fm")
    ch1_html = convert_markdown_to_html(ch1_md, svg_mode="inline", doc_prefix="t0ch1")
    ws1_html = convert_markdown_to_html(ws1_md, svg_mode="inline", doc_prefix="t0ws1")

    upgrade_html = """
    <section class="chapter-container">
        <h1>Upgrade to the Complete AI Content Creator &amp; Solopreneur Operating System</h1>
        <p>You have just completed the <strong>Tier 0 Free Starter Kit</strong> (Front Matter + Chapter 1: <em>The Creator-to-Operator Paradigm</em> + Worksheet 01: <em>The 7-Day Content Time-Leak &amp; RPPH Diagnostic Audit</em>).</p>
        <h2>What You Receive in the Full Flagship Edition &amp; Pro Operator Bundle</h2>
        <table>
            <thead>
                <tr>
                    <th>Commercial Tier</th>
                    <th>Included Systems, Templates &amp; Automation Assets</th>
                    <th>Target Outcome</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Tier 1: Core Digital Edition ($29)</strong></td>
                    <td>Complete 10-Chapter Master Manual (91,775 words in US Letter PDF, KDP 6x9 Print PDF &amp; EPUB 3.0) + All 10 Fillable Action Worksheets + 50 AI Workflow Prompts (P01–P50) + 12 Emergency Scripts (S01–S12).</td>
                    <td>Install the end-to-end 5-Stage Content-to-Cash Operating System.</td>
                </tr>
                <tr>
                    <td><strong>Tier 2: Creator Operator Pro Bundle ($79)</strong></td>
                    <td>Everything in Tier 1 PLUS the Interactive Web Calculators &amp; RPPH Diagnostic Suite (Unlocked via Pro Key <code>CREATOR-OS-PRO-2026</code>), Notion Creator OS Workspace Blueprint, and Excel/Google Sheets Financial &amp; Waterfall Trackers.</td>
                    <td>Automate idea validation, 1-to-15 repurposing, and funnel tracking.</td>
                </tr>
                <tr>
                    <td><strong>Tier 3: Executive Solopreneur Automation Suite ($199)</strong></td>
                    <td>Everything in Tier 2 PLUS Production-Ready n8n &amp; Make.com JSON Automation Workflows, Editable DOCX SOPs, PPTX Executive Slide Decks, and Brand Sponsorship Media Kit Templates.</td>
                    <td>Scale to $15k–$40k+/month in 22 hours/week with 85%+ net margins.</td>
                </tr>
            </tbody>
        </table>
    </section>
    """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Tier 0 Starter Kit — The AI Content Creator &amp; Solopreneur OS</title>
<style>{css}</style>
</head>
<body>
<div class="title-hero-page">
    <div class="title-eyebrow">TIER 0 FREE STARTER KIT &amp; DIAGNOSTIC AUDIT</div>
    <div class="title-main">The AI Content Creator &amp; Solopreneur Operating System</div>
    <div class="title-sub">Complete Chapter 1 Vertical Slice + Visual System Architecture + Fillable 7-Day Content Time-Leak &amp; RPPH Diagnostic Audit Workbook</div>
    <div class="title-meta-box">
        <p><strong>Included in This Free Starter Kit:</strong> Manifesto &amp; 7-Day Quick-Start Checklist · Complete Chapter 1 (9,704 words) · Prompts P01–P05 · Worksheet 01 Diagnostic Audit</p>
    </div>
</div>
<section class="chapter-container">{fm_html}</section>
<section class="chapter-container">{ch1_html}</section>
<section class="chapter-container">{ws1_html}</section>
{upgrade_html}
</body>
</html>"""


def build_chapter01_standalone_workbook_html() -> str:
    css = get_book_css("workbook_letter")
    ws1_md = (STUDIO_ROOT / "05-WORKBOOKS/markdown/worksheet-01.md").read_text(encoding="utf-8")
    extra_diagrams = (
        "\n\n## Section 9: Chapter 01 Reference Architecture Diagrams\n\n"
        "![The 5-Stage Content-to-Cash Operating System Mindmap](../04-VISUAL-ASSETS/svg/chapter-01-mindmap.svg)\n\n"
        "![The Creator Time-Allocation & RPPH Diagnostic Decision Tree](../04-VISUAL-ASSETS/svg/chapter-01-flowchart.svg)\n"
    )
    ws1_html = convert_markdown_to_html(ws1_md + extra_diagrams, svg_mode="inline", doc_prefix="ch01wb")
    notes_html = _render_notes_grid("Chapter 01 Operator Audit Action Plan & 90-Day RPPH Target Log", lines=16)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Chapter 01 Action Workbook — 7-Day Content Time-Leak &amp; RPPH Audit</title>
<style>{css}</style>
</head>
<body>
<div class="title-hero-page">
    <div class="title-eyebrow">STANDALONE FILLABLE ACTION WORKBOOK · CHAPTER 01</div>
    <div class="title-main">Worksheet 01: The 7-Day Content Time-Leak &amp; RPPH Diagnostic Audit</div>
    <div class="title-sub">Quantify Your Revenue Per Production Hour (RPPH), Eliminate Unvalidated Creation Bottlenecks, and Install Your 5-Stage Content-to-Cash Operating Baseline</div>
    <div class="title-meta-box">
        <p><strong>Fillable AcroForm PDF:</strong> Complete digitally on desktop/tablet or print on US Letter paper.</p>
        <p><strong>Pro Calculator Unlock Key:</strong> <code>CREATOR-OS-PRO-2026</code></p>
    </div>
</div>
<section class="chapter-container">{ws1_html}{notes_html}</section>
</body>
</html>"""


# ---------------------------------------------------------------------------
# 6. VALIDATED REFLOWABLE EPUB 3.0 COMPILER (STRICT XML COMPLIANCE)
# ---------------------------------------------------------------------------

def build_epub3(epub_path: Path) -> None:
    epub_path.parent.mkdir(parents=True, exist_ok=True)
    book_uuid = "urn:uuid:73032026-4f46-4e50-8d94-88d977062026"
    modified_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Gather content sections
    doc_specs = [
        ("front-matter", "Front Matter: The Creator-to-Operator Manifesto", STUDIO_ROOT / "03-MANUSCRIPT/front-matter.md"),
    ]
    for ch_slug, ch_title in CHAPTER_TITLES:
        doc_specs.append((ch_slug, ch_title, STUDIO_ROOT / "03-MANUSCRIPT" / f"{ch_slug}.md"))
    doc_specs.append(
        ("back-matter", "Back Matter Vault: 50 Prompts, 12 Emergency Scripts & Glossary", STUDIO_ROOT / "03-MANUSCRIPT/back-matter.md")
    )

    epub_css = """
    body {
        font-family: 'Inter', 'Noto Sans', sans-serif;
        color: #1E293B;
        background-color: #FFFFFF;
        line-height: 1.6;
        margin: 1em;
    }
    h1, h2, h3, h4 {
        color: #0F172A;
        font-weight: bold;
        line-height: 1.3;
    }
    h1 { font-size: 1.6em; border-bottom: 2px solid #4F46E5; padding-bottom: 0.3em; }
    h2 { font-size: 1.3em; border-left: 4px solid #4F46E5; padding-left: 0.5em; margin-top: 1.4em; }
    h3 { font-size: 1.1em; color: #4F46E5; }
    table { width: 100%; border-collapse: collapse; margin: 1em 0; font-size: 0.9em; }
    th { background-color: #F1F5F9; color: #0F172A; padding: 6px; border: 1px solid #94A3B8; text-align: left; }
    td { padding: 6px; border: 1px solid #CBD5E1; vertical-align: top; }
    pre {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-left: 4px solid #4F46E5;
        padding: 10px;
        white-space: pre-wrap;
        font-family: monospace;
        font-size: 0.88em;
    }
    code { font-family: monospace; background-color: #F1F5F9; padding: 1px 3px; }
    blockquote {
        background-color: #F8FAFC;
        border-left: 4px solid #0D9488;
        padding: 8px 12px;
        margin: 1em 0;
    }
    .math-display-block {
        background-color: #F8FAFC;
        border-left: 3px solid #0D9488;
        padding: 8px;
        margin: 0.8em 0;
        font-family: monospace;
        text-align: center;
    }
    .diagram-container { text-align: center; margin: 1.2em 0; }
    .epub-diagram-img { max-width: 100%; height: auto; }
    .diagram-caption { font-size: 0.85em; color: #64748B; margin-top: 0.4em; }
    """

    xhtml_files: dict[str, str] = {}
    for slug, title, md_path in doc_specs:
        md_raw = md_path.read_text(encoding="utf-8")
        body_xhtml = convert_markdown_to_html(md_raw, svg_mode="img", doc_prefix=slug)
        full_xhtml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="styles/ebook.css" />
</head>
<body>
{body_xhtml}
</body>
</html>"""
        # Verify XML well-formedness immediately via ElementTree
        ET.fromstring(full_xhtml.encode("utf-8"))
        xhtml_files[f"{slug}.xhtml"] = full_xhtml

    # Build OEBPS/nav.xhtml (EPUB 3.0 Navigation Document)
    nav_lis = "\n".join(
        f'        <li><a href="{slug}.xhtml">{html.escape(title)}</a></li>'
        for slug, title, _ in doc_specs
    )
    nav_xhtml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Table of Contents — The AI Content Creator &amp; Solopreneur Operating System</title>
  <link rel="stylesheet" type="text/css" href="styles/ebook.css" />
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Table of Contents</h1>
    <ol>
{nav_lis}
    </ol>
  </nav>
</body>
</html>"""
    ET.fromstring(nav_xhtml.encode("utf-8"))

    # Build OEBPS/toc.ncx (EPUB 2 backward compatibility)
    ncx_points = []
    for idx, (slug, title, _) in enumerate(doc_specs, start=1):
        ncx_points.append(f"""    <navPoint id="navPoint-{idx}" playOrder="{idx}">
      <navLabel><text>{html.escape(title)}</text></navLabel>
      <content src="{slug}.xhtml" />
    </navPoint>""")
    toc_ncx = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{book_uuid}" />
    <meta name="dtb:depth" content="1" />
    <meta name="dtb:totalPageCount" content="0" />
    <meta name="dtb:maxPageNumber" content="0" />
  </head>
  <docTitle>
    <text>The AI Content Creator &amp; Solopreneur Operating System</text>
  </docTitle>
  <navMap>
{chr(10).join(ncx_points)}
  </navMap>
</ncx>"""
    ET.fromstring(toc_ncx.encode("utf-8"))

    # Build OEBPS/content.opf
    manifest_items = [
        '    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />',
        '    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml" />',
        '    <item id="css" href="styles/ebook.css" media-type="text/css" />',
    ]
    spine_items = []
    for slug, _, _ in doc_specs:
        item_id = f"item-{slug}"
        manifest_items.append(
            f'    <item id="{item_id}" href="{slug}.xhtml" media-type="application/xhtml+xml" />'
        )
        spine_items.append(f'    <itemref idref="{item_id}" />')

    svg_files = sorted((STUDIO_ROOT / "04-VISUAL-ASSETS/svg").glob("chapter-*.svg"))
    for svg_p in svg_files:
        svg_id = f"img-{svg_p.stem}"
        manifest_items.append(
            f'    <item id="{svg_id}" href="images/{svg_p.name}" media-type="image/svg+xml" />'
        )

    content_opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="BookId" xml:lang="en">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookId">{book_uuid}</dc:identifier>
    <dc:title>The AI Content Creator &amp; Solopreneur Operating System</dc:title>
    <dc:creator>Apex Digital Systems Studio</dc:creator>
    <dc:language>en</dc:language>
    <dc:publisher>Apex Digital Systems Studio</dc:publisher>
    <dc:description>A Practical System to Research Validated Ideas, Script High-Retention Content, Repurpose Across Platforms, Automate Production, and Monetize Your Audience Without Burnout.</dc:description>
    <dc:rights>Copyright 2026 Apex Digital Systems Studio. All rights reserved.</dc:rights>
    <meta property="dcterms:modified">{modified_utc}</meta>
  </metadata>
  <manifest>
{chr(10).join(manifest_items)}
  </manifest>
  <spine toc="ncx">
{chr(10).join(spine_items)}
  </spine>
</package>"""
    ET.fromstring(content_opf.encode("utf-8"))

    container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml" />
  </rootfiles>
</container>"""
    ET.fromstring(container_xml.encode("utf-8"))

    # Write EPUB ZIP with uncompressed mimetype first
    with zipfile.ZipFile(epub_path, "w") as zf:
        zf.writestr("mimetype", b"application/epub+zip", compress_type=zipfile.ZIP_STORED)
        zf.writestr("META-INF/container.xml", container_xml.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/content.opf", content_opf.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/nav.xhtml", nav_xhtml.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/toc.ncx", toc_ncx.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/styles/ebook.css", epub_css.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)

        for fname, xhtml_str in xhtml_files.items():
            zf.writestr(f"OEBPS/{fname}", xhtml_str.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)

        for svg_p in svg_files:
            svg_bytes = svg_p.read_bytes()
            ET.fromstring(svg_bytes)
            zf.writestr(f"OEBPS/images/{svg_p.name}", svg_bytes, compress_type=zipfile.ZIP_DEFLATED)


# ---------------------------------------------------------------------------
# 7. MAIN COMPILER PIPELINE EXECUTION
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 88)
    print("ANTIGRAVITY MULTI-FORMAT PUBLISHING COMPILER (build.py) -- PHASE 5")
    print(f"Studio Root: {STUDIO_ROOT}")
    print(f"Headless Browser Engine: {BROWSER_BIN}")
    print("=" * 88)

    pdf_complete_book = STUDIO_ROOT / "09-EXPORTS/PDF/the-ai-creator-solopreneur-os-complete-book.pdf"
    pdf_kdp_6x9 = STUDIO_ROOT / "09-EXPORTS/PRINT/the-ai-creator-solopreneur-os-kdp-paperback-6x9.pdf"
    epub_book = STUDIO_ROOT / "09-EXPORTS/EPUB/the-ai-creator-solopreneur-os.epub"
    pdf_wb_letter = STUDIO_ROOT / "09-EXPORTS/PRINT/the-ai-creator-solopreneur-os-workbook-us-letter.pdf"
    pdf_wb_a4 = STUDIO_ROOT / "09-EXPORTS/PRINT/the-ai-creator-solopreneur-os-workbook-a4.pdf"
    pdf_tablet = STUDIO_ROOT / "09-EXPORTS/PDF/the-ai-creator-solopreneur-os-tablet-planner.pdf"
    pdf_tier0_sample = STUDIO_ROOT / "09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf"
    pdf_ch01_wb = STUDIO_ROOT / "05-WORKBOOKS/chapter-01-workbook.pdf"

    # 1. Complete Digital Flagship Book PDF (US Letter 8.5" x 11")
    print("[1/8] Compiling Complete Digital Flagship Book PDF (US Letter 8.5\" x 11\")...")
    html_book_letter = build_complete_book_html("color_letter")
    render_html_to_pdf(html_book_letter, pdf_complete_book)
    r_book = PdfReader(str(pdf_complete_book))
    print(f"      -> Done: {len(r_book.pages)} pages, {pdf_complete_book.stat().st_size:,} bytes")

    # 2. Amazon KDP Print-Ready Paperback Interior PDF (6" x 9" Monochrome)
    print("[2/8] Compiling Amazon KDP Print-Ready Paperback PDF (6\" x 9\" Monochrome)...")
    html_book_kdp = build_complete_book_html("kdp_6x9")
    render_html_to_pdf(html_book_kdp, pdf_kdp_6x9)
    r_kdp = PdfReader(str(pdf_kdp_6x9))
    print(f"      -> Done: {len(r_kdp.pages)} pages, {pdf_kdp_6x9.stat().st_size:,} bytes")

    # 3. Validated Reflowable EPUB 3.0 eBook
    print("[3/8] Compiling Validated Reflowable EPUB 3.0 eBook...")
    build_epub3(epub_book)
    print(f"      -> Done: {epub_book.stat().st_size:,} bytes")

    # 4. Fillable 10-Chapter Action Workbook — US Letter (8.5" x 11")
    print("[4/8] Compiling Fillable 10-Chapter Action Workbook PDF (US Letter)...")
    html_wb_letter = build_workbook_html("workbook_letter")
    render_html_to_pdf(html_wb_letter, pdf_wb_letter)
    fields_wb_letter = inject_acroform_fields(pdf_wb_letter, fields_per_page=3)
    r_wbl = PdfReader(str(pdf_wb_letter))
    print(f"      -> Done: {len(r_wbl.pages)} pages, {fields_wb_letter} AcroForm fields, {pdf_wb_letter.stat().st_size:,} bytes")

    # 5. Fillable 10-Chapter Action Workbook — ISO A4 (210mm x 297mm)
    print("[5/8] Compiling Fillable 10-Chapter Action Workbook PDF (ISO A4)...")
    html_wb_a4 = build_workbook_html("workbook_a4")
    render_html_to_pdf(html_wb_a4, pdf_wb_a4)
    fields_wb_a4 = inject_acroform_fields(pdf_wb_a4, fields_per_page=3)
    r_wba4 = PdfReader(str(pdf_wb_a4))
    print(f"      -> Done: {len(r_wba4.pages)} pages, {fields_wb_a4} AcroForm fields, {pdf_wb_a4.stat().st_size:,} bytes")

    # 6. Interactive Landscape Tablet Planner PDF (11" x 8.5")
    print("[6/8] Compiling Interactive Landscape Tablet Planner PDF (11\" x 8.5\")...")
    html_tablet = build_workbook_html("tablet_landscape")
    render_html_to_pdf(html_tablet, pdf_tablet)
    fields_tablet = inject_acroform_fields(pdf_tablet, fields_per_page=3)
    r_tab = PdfReader(str(pdf_tablet))
    print(f"      -> Done: {len(r_tab.pages)} pages, {fields_tablet} AcroForm fields, {pdf_tablet.stat().st_size:,} bytes")

    # 7A & 7B. Tier 0 Free Starter Kit Sample PDF & Standalone Chapter 1 Audit Workbook PDF
    print("[7/8] Compiling Tier 0 Sample PDF & Standalone Chapter 1 Fillable Workbook PDF...")
    html_t0 = build_tier0_sample_html()
    render_html_to_pdf(html_t0, pdf_tier0_sample)
    r_t0 = PdfReader(str(pdf_tier0_sample))
    print(f"      -> 7A Done: {len(r_t0.pages)} pages, {pdf_tier0_sample.stat().st_size:,} bytes")

    html_ch01_wb = build_chapter01_standalone_workbook_html()
    render_html_to_pdf(html_ch01_wb, pdf_ch01_wb)
    fields_ch01 = inject_acroform_fields(pdf_ch01_wb, fields_per_page=3)
    r_ch01 = PdfReader(str(pdf_ch01_wb))
    print(f"      -> 7B Done: {len(r_ch01.pages)} pages, {fields_ch01} AcroForm fields, {pdf_ch01_wb.stat().st_size:,} bytes")

    # 8. Render All 20 SVG Diagrams to 1800x960 Retina PNGs
    print("[8/8] Rendering 20 Vector SVG Diagrams to 1800x960 Retina PNGs...")
    svg_dir = STUDIO_ROOT / "04-VISUAL-ASSETS/svg"
    png_dir = STUDIO_ROOT / "04-VISUAL-ASSETS/png"
    svg_list = sorted(svg_dir.glob("chapter-*.svg"))
    for idx, svg_p in enumerate(svg_list, start=1):
        out_png = png_dir / f"{svg_p.stem}.png"
        render_svg_to_png(svg_p, out_png, width=1800, height=960)
        print(f"      [{idx:02d}/20] {out_png.name} -> {out_png.stat().st_size:,} bytes")

    # 9. Update PROJECT_STATE.json with Phase 5 telemetry and exact KDP 6x9 page count
    state_path = STUDIO_ROOT / "PROJECT_STATE.json"
    state_data = json.loads(state_path.read_text(encoding="utf-8"))
    state_data.setdefault("phase_status", {})["Phase 5"] = "COMPLETED"
    state_data.setdefault("asset_inventory", {})["completed_png_diagrams"] = 20
    state_data["phase5_exports"] = {
        "kdp_paperback_6x9_pages": len(r_kdp.pages),
        "complete_book_us_letter_pages": len(r_book.pages),
        "workbook_us_letter_pages": len(r_wbl.pages),
        "workbook_us_letter_acroform_fields": fields_wb_letter,
        "workbook_a4_pages": len(r_wba4.pages),
        "workbook_a4_acroform_fields": fields_wb_a4,
        "tablet_planner_pages": len(r_tab.pages),
        "tablet_planner_acroform_fields": fields_tablet,
        "tier0_sample_pages": len(r_t0.pages),
        "chapter01_workbook_pages": len(r_ch01.pages),
        "chapter01_workbook_acroform_fields": fields_ch01,
        "epub_size_bytes": epub_book.stat().st_size,
        "deliverables": {
            "09-EXPORTS/PDF/the-ai-creator-solopreneur-os-complete-book.pdf": {
                "pages": len(r_book.pages),
                "bytes": pdf_complete_book.stat().st_size,
            },
            "09-EXPORTS/PRINT/the-ai-creator-solopreneur-os-kdp-paperback-6x9.pdf": {
                "pages": len(r_kdp.pages),
                "bytes": pdf_kdp_6x9.stat().st_size,
            },
            "09-EXPORTS/EPUB/the-ai-creator-solopreneur-os.epub": {
                "bytes": epub_book.stat().st_size,
            },
            "09-EXPORTS/PRINT/the-ai-creator-solopreneur-os-workbook-us-letter.pdf": {
                "pages": len(r_wbl.pages),
                "acroform_fields": fields_wb_letter,
                "bytes": pdf_wb_letter.stat().st_size,
            },
            "09-EXPORTS/PRINT/the-ai-creator-solopreneur-os-workbook-a4.pdf": {
                "pages": len(r_wba4.pages),
                "acroform_fields": fields_wb_a4,
                "bytes": pdf_wb_a4.stat().st_size,
            },
            "09-EXPORTS/PDF/the-ai-creator-solopreneur-os-tablet-planner.pdf": {
                "pages": len(r_tab.pages),
                "acroform_fields": fields_tablet,
                "bytes": pdf_tablet.stat().st_size,
            },
            "09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf": {
                "pages": len(r_t0.pages),
                "bytes": pdf_tier0_sample.stat().st_size,
            },
            "05-WORKBOOKS/chapter-01-workbook.pdf": {
                "pages": len(r_ch01.pages),
                "acroform_fields": fields_ch01,
                "bytes": pdf_ch01_wb.stat().st_size,
            },
        },
    }
    state_path.write_text(json.dumps(state_data, indent=2) + "\n", encoding="utf-8")
    print("\n[SUCCESS] PROJECT_STATE.json updated with Phase 5 telemetry and KDP page count.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
