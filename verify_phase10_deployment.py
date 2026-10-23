#!/usr/bin/env python3
"""
PHASE 10 AUTOMATED QA & STATIC WEB DEPLOYMENT VERIFIER (`verify_phase10_deployment.py`)
Product #3: The AI Content Creator & Solopreneur Operating System
Target Root: e:/Ebook-Makaer/AI-Creator-Solopreneur-OS/DIGITAL-PUBLISHING-STUDIO/

Verifies:
1. Both `15-WEB-DEPLOYMENT/` and `docs/` exist and contain identical, complete production trees:
   - `index.html` (>= 170,000 bytes)
   - `app/index.html` (>= 500,000 bytes) and `app/creator-os-app.html`
   - `studio/index.html` (>= 45,000 bytes) and `studio/design-customizer-studio.html`
   - `atlas/index.html` (>= 45,000 bytes, containing all 31 embedded SVGs)
   - `downloads/index.html`
   - `404.html`, `manifest.json` (valid JSON), `vercel.json` (valid JSON), `netlify.toml`,
     `_headers`, `.nojekyll`, `robots.txt`, `sitemap.xml` (valid XML).
2. All 7 downloadable Tier 0 / Atlas files exist in `downloads/` and match source byte sizes,
   plus all 6 cover/preview PNGs exist in `assets/` and match source byte sizes.
3. Internal Link & Asset Integrity Check across `index.html`, `app/index.html`, `studio/index.html`,
   `atlas/index.html`, `downloads/index.html`, and `404.html`: 0 broken local relative links and
   0 external HTTP/HTTPS script/CSS dependencies.
4. `15-WEB-DEPLOYMENT/DEPLOYMENT-RUNBOOK.md` exists and contains >= 1,200 words.
5. Zero Banned Words / Phrases & Zero Placeholders across all Phase 10 text files.
6. Updates `PROJECT_STATE.json` with `"Phase 10": "COMPLETED"` and `"deployment_ready": true`.
7. Writes `11-QA-REPORTS/phase10-deployment-qa-report.md` and exits with code 0 ONLY if 0 errors.
"""

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

STUDIO_ROOT = Path(__file__).resolve().parent
DEPLOY_DIR = STUDIO_ROOT / "15-WEB-DEPLOYMENT"
DOCS_DIR = STUDIO_ROOT / "docs"
QA_REPORT_PATH = STUDIO_ROOT / "11-QA-REPORTS" / "phase10-deployment-qa-report.md"
PROJECT_STATE_PATH = STUDIO_ROOT / "PROJECT_STATE.json"

BANNED_WORDS = [
    "delve", "tapestry", "testament", "beacon", "symphony",
    "unlock", "unleash", "skyrocket", "supercharge", "game-changer",
    "pivotal", "realm", "foster", "underscore", "utilize", "leverage"
]

BANNED_PHRASES = [
    "in today's fast-paced digital world",
    "whether you are a beginner or an expert",
    "it is important to remember",
    "let's dive in",
    "without further ado",
    "the landscape of"
]

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bFIXME\b",
    r"lorem ipsum",
    r"\[PLACEHOLDER\b"
]


class LinkAndAssetParser(HTMLParser):
    """Extracts <a href>, <img src>, <script src>, and <link href> from HTML documents."""
    def __init__(self):
        super().__init__()
        self.a_hrefs = []
        self.img_srcs = []
        self.script_srcs = []
        self.link_hrefs = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        t = tag.lower()
        if t == "a" and "href" in attr_dict:
            self.a_hrefs.append(attr_dict["href"])
        elif t == "img" and "src" in attr_dict:
            self.img_srcs.append(attr_dict["src"])
        elif t == "script" and "src" in attr_dict:
            self.script_srcs.append(attr_dict["src"])
        elif t == "link" and "href" in attr_dict:
            self.link_hrefs.append(attr_dict["href"])


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    checks = []
    errors = []

    def record(name: str, passed: bool, detail: str):
        status = "PASS" if passed else "FAIL"
        checks.append((name, status, detail))
        if not passed:
            errors.append(f"{name}: {detail}")
        print(f"[{status}] {name} -> {detail}")

    print("=" * 88)
    print("PHASE 10 AUTOMATED QA & STATIC WEB DEPLOYMENT VERIFICATION")
    print("=" * 88)

    # 1. Check both root directories exist
    record(
        "15-WEB-DEPLOYMENT/ & docs/ Directories Exist",
        DEPLOY_DIR.is_dir() and DOCS_DIR.is_dir(),
        f"15-WEB-DEPLOYMENT={DEPLOY_DIR.is_dir()}, docs={DOCS_DIR.is_dir()}"
    )

    # 2. Verify core HTML routes & minimum byte thresholds in both directories
    route_thresholds = [
        ("index.html", 170000),
        ("app/index.html", 500000),
        ("app/creator-os-app.html", 500000),
        ("studio/index.html", 45000),
        ("studio/design-customizer-studio.html", 45000),
        ("atlas/index.html", 45000),
        ("downloads/index.html", 4000),
        ("404.html", 3000),
    ]

    for rel_path, min_bytes in route_thresholds:
        p_dep = DEPLOY_DIR / rel_path
        p_doc = DOCS_DIR / rel_path
        exists_both = p_dep.is_file() and p_doc.is_file()
        sz_dep = p_dep.stat().st_size if p_dep.is_file() else 0
        sz_doc = p_doc.stat().st_size if p_doc.is_file() else 0
        identical = exists_both and (sha256_file(p_dep) == sha256_file(p_doc))
        ok = exists_both and sz_dep >= min_bytes and identical
        record(
            f"HTML Route `{rel_path}` (>= {min_bytes:,} bytes & mirrored)",
            ok,
            f"size={sz_dep:,} bytes (min {min_bytes:,}), docs_mirror_identical={identical}"
        )

    # 3. Verify `atlas/index.html` embeds all 31 SVGs (1 Master Map + 10 Cheat Sheets + 20 Chapter Diagrams)
    atlas_html = (DEPLOY_DIR / "atlas" / "index.html").read_text(encoding="utf-8")
    svg_count = len(re.findall(r"<svg\b", atlas_html, re.IGNORECASE))
    master_count = len(re.findall(r'data-category="master"', atlas_html))
    cs_count = len(re.findall(r'data-category="cheatsheets"', atlas_html))
    diag_count = len(re.findall(r'data-category="diagrams"', atlas_html))
    record(
        "Atlas 31 Embedded Vector SVGs (1 Master + 10 Cheat Sheets + 20 Chapter Diagrams)",
        svg_count == 31 and master_count == 1 and cs_count == 10 and diag_count == 20,
        f"total_svgs={svg_count}, master={master_count}, cheat_sheets={cs_count}, chapter_diagrams={diag_count}"
    )

    # 4. Verify Static Hosting & PWA Config Files (`manifest.json`, `vercel.json`, `netlify.toml`, `_headers`, `.nojekyll`, `robots.txt`, `sitemap.xml`)
    config_files = [".nojekyll", "manifest.json", "vercel.json", "netlify.toml", "_headers", "robots.txt", "sitemap.xml"]
    for cfg in config_files:
        p_dep = DEPLOY_DIR / cfg
        p_doc = DOCS_DIR / cfg
        exists_both = p_dep.is_file() and p_doc.is_file()
        identical = exists_both and (sha256_file(p_dep) == sha256_file(p_doc))
        valid_schema = True
        schema_note = "text/config"
        if exists_both and cfg.endswith(".json"):
            try:
                parsed = json.loads(p_dep.read_text(encoding="utf-8"))
                schema_note = f"valid JSON ({len(parsed)} top-level keys)"
            except Exception as e:
                valid_schema = False
                schema_note = f"invalid JSON: {e}"
        elif exists_both and cfg.endswith(".xml"):
            try:
                root = ET.fromstring(p_dep.read_text(encoding="utf-8"))
                schema_note = f"valid XML (root={root.tag})"
            except Exception as e:
                valid_schema = False
                schema_note = f"invalid XML: {e}"
        record(
            f"Hosting Config `{cfg}`",
            exists_both and identical and valid_schema,
            f"exists={exists_both}, mirrored={identical}, {schema_note}"
        )

    # 5. Verify all 7 downloadable Tier 0 / Atlas files in `downloads/` match source byte sizes
    expected_downloads = {
        "tier0-free-sample-chapter01-and-audit.pdf": STUDIO_ROOT / "09-EXPORTS" / "PDF" / "tier0-free-sample-chapter01-and-audit.pdf",
        "chapter-01-workbook.pdf": STUDIO_ROOT / "05-WORKBOOKS" / "chapter-01-workbook.pdf",
        "the-ai-creator-solopreneur-os-visual-shortcut-atlas.pdf": STUDIO_ROOT / "09-EXPORTS" / "PDF" / "the-ai-creator-solopreneur-os-visual-shortcut-atlas.pdf",
        "sheet1-creator-rpm-and-time-audit.csv": STUDIO_ROOT / "06-NOTION-TEMPLATES" / "Spreadsheets" / "sheet1-creator-rpm-and-time-audit.csv",
        "00-ECOSYSTEM-MASTER-MAP-POSTER.png": STUDIO_ROOT / "13-VISUAL-CHEAT-SHEETS" / "png" / "00-ECOSYSTEM-MASTER-MAP-POSTER.png",
        "cheat-sheet-ch01.png": STUDIO_ROOT / "13-VISUAL-CHEAT-SHEETS" / "png" / "cheat-sheet-ch01.png",
        "tier0-free-sample-starter-kit.zip": STUDIO_ROOT / "09-EXPORTS" / "HYBRID-BUNDLE" / "tier0-free-sample-starter-kit.zip",
    }

    for fname, src_path in expected_downloads.items():
        p_dep = DEPLOY_DIR / "downloads" / fname
        p_doc = DOCS_DIR / "downloads" / fname
        src_sz = src_path.stat().st_size if src_path.is_file() else -1
        dep_sz = p_dep.stat().st_size if p_dep.is_file() else -2
        doc_sz = p_doc.stat().st_size if p_doc.is_file() else -3
        ok = (src_sz > 0) and (dep_sz == src_sz) and (doc_sz == src_sz)
        record(
            f"Self-Hosted Download `downloads/{fname}`",
            ok,
            f"source={src_sz:,} B, 15-WEB-DEPLOYMENT={dep_sz:,} B, docs={doc_sz:,} B"
        )

    # 6. Verify all 6 Cover & Preview PNGs in `assets/`
    expected_assets = {
        "ebook-cover-kdp-kindle.png": STUDIO_ROOT / "08-COVER-DESIGN" / "png" / "ebook-cover-kdp-kindle.png",
        "gumroad-tier0-free-audit-cover.png": STUDIO_ROOT / "08-COVER-DESIGN" / "png" / "gumroad-tier0-free-audit-cover.png",
        "gumroad-tier2-workbook-edition-cover.png": STUDIO_ROOT / "08-COVER-DESIGN" / "png" / "gumroad-tier2-workbook-edition-cover.png",
        "gumroad-tier3-flagship-bundle-cover.png": STUDIO_ROOT / "08-COVER-DESIGN" / "png" / "gumroad-tier3-flagship-bundle-cover.png",
        "gumroad-tier4-vault-membership-cover.png": STUDIO_ROOT / "08-COVER-DESIGN" / "png" / "gumroad-tier4-vault-membership-cover.png",
        "webapp-dashboard-preview.png": STUDIO_ROOT / "04-VISUAL-ASSETS" / "png" / "webapp-dashboard-preview.png",
    }

    for fname, src_path in expected_assets.items():
        p_dep = DEPLOY_DIR / "assets" / fname
        p_doc = DOCS_DIR / "assets" / fname
        src_sz = src_path.stat().st_size if src_path.is_file() else -1
        dep_sz = p_dep.stat().st_size if p_dep.is_file() else -2
        doc_sz = p_doc.stat().st_size if p_doc.is_file() else -3
        ok = (src_sz > 0) and (dep_sz == src_sz) and (doc_sz == src_sz)
        record(
            f"Commercial Cover/Preview Asset `assets/{fname}`",
            ok,
            f"source={src_sz:,} B, 15-WEB-DEPLOYMENT={dep_sz:,} B, docs={doc_sz:,} B"
        )

    # 7. Internal Link & Asset Integrity Check across all HTML pages
    html_pages_to_check = [
        "index.html",
        "app/index.html",
        "studio/index.html",
        "atlas/index.html",
        "downloads/index.html",
        "404.html",
    ]
    broken_links = []
    external_deps = []
    total_links_checked = 0

    for rel_html in html_pages_to_check:
        for base_root in [DEPLOY_DIR, DOCS_DIR]:
            page_path = base_root / rel_html
            parser = LinkAndAssetParser()
            parser.feed(page_path.read_text(encoding="utf-8"))

            # Check external scripts / stylesheets
            for s in parser.script_srcs + parser.link_hrefs:
                if s.lower().startswith(("http://", "https://", "//")):
                    external_deps.append(f"{base_root.name}/{rel_html} -> {s}")

            # Check all local relative href/src attributes resolve inside base_root
            for ref in parser.a_hrefs + parser.img_srcs + parser.script_srcs + parser.link_hrefs:
                total_links_checked += 1
                if not ref or ref.startswith("#") or ref.startswith(("mailto:", "tel:", "javascript:", "data:")):
                    continue
                if ref.lower().startswith(("http://", "https://", "//")):
                    continue
                clean_ref = ref.split("#")[0].split("?")[0]
                if not clean_ref:
                    continue
                resolved = (page_path.parent / clean_ref).resolve()
                # Ensure resolved path exists AND is inside base_root
                try:
                    resolved.relative_to(base_root.resolve())
                    inside_root = True
                except ValueError:
                    inside_root = False
                if not resolved.exists() or not inside_root:
                    broken_links.append(f"{base_root.name}/{rel_html}: `{ref}` -> {resolved} (exists={resolved.exists()}, inside_root={inside_root})")

    record(
        "Internal Link & Asset Integrity (0 Broken Relative Links)",
        len(broken_links) == 0,
        f"checked {total_links_checked} attributes across 15-WEB-DEPLOYMENT/ & docs/; broken={len(broken_links)}"
        + (f" ({broken_links[:3]})" if broken_links else "")
    )
    record(
        "Zero External HTTP/HTTPS Script/CSS Dependencies",
        len(external_deps) == 0,
        f"external_dependencies={len(external_deps)}"
    )

    # 8. Verify `15-WEB-DEPLOYMENT/DEPLOYMENT-RUNBOOK.md` exists and contains >= 1,200 words
    runbook_dep = DEPLOY_DIR / "DEPLOYMENT-RUNBOOK.md"
    runbook_doc = DOCS_DIR / "DEPLOYMENT-RUNBOOK.md"
    runbook_text = runbook_dep.read_text(encoding="utf-8") if runbook_dep.is_file() else ""
    runbook_words = len(re.findall(r"\b\w+\b", runbook_text))
    record(
        "DEPLOYMENT-RUNBOOK.md Word Count (>= 1,200 words & mirrored)",
        runbook_dep.is_file() and runbook_doc.is_file() and runbook_words >= 1200,
        f"words={runbook_words:,}, bytes={len(runbook_text.encode('utf-8')):,}"
    )

    # 9. Zero Banned Words / Phrases & Zero Placeholders across all Phase 10 text files
    text_extensions = {".html", ".md", ".json", ".toml", ".xml", ".txt"}
    banned_hits = []
    placeholder_hits = []
    scanned_files_count = 0

    for fpath in sorted(DEPLOY_DIR.rglob("*")):
        if fpath.is_file() and (fpath.suffix.lower() in text_extensions or fpath.name in {"_headers", ".nojekyll"}):
            scanned_files_count += 1
            content = fpath.read_text(encoding="utf-8")
            lower_content = content.lower()
            for bw in BANNED_WORDS:
                if re.search(rf"\b{re.escape(bw)}\b", lower_content):
                    banned_hits.append(f"{fpath.relative_to(STUDIO_ROOT)}: banned word '{bw}'")
            for bp in BANNED_PHRASES:
                if bp in lower_content:
                    banned_hits.append(f"{fpath.relative_to(STUDIO_ROOT)}: banned phrase '{bp}'")
            for pat in PLACEHOLDER_PATTERNS:
                if re.search(pat, content, re.IGNORECASE):
                    placeholder_hits.append(f"{fpath.relative_to(STUDIO_ROOT)}: pattern '{pat}'")

    record(
        "Zero Banned Words & Banned Phrases Across Phase 10 Files",
        len(banned_hits) == 0,
        f"scanned {scanned_files_count} text files; violations={len(banned_hits)}"
        + (f" ({banned_hits[:3]})" if banned_hits else "")
    )
    record(
        "Zero Placeholders (TODO/TBD/FIXME/Lorem Ipsum) Across Phase 10 Files",
        len(placeholder_hits) == 0,
        f"scanned {scanned_files_count} text files; violations={len(placeholder_hits)}"
        + (f" ({placeholder_hits[:3]})" if placeholder_hits else "")
    )

    # 10. Verify 100% file-tree parity between `15-WEB-DEPLOYMENT/` and `docs/`
    dep_files = sorted([p.relative_to(DEPLOY_DIR).as_posix() for p in DEPLOY_DIR.rglob("*") if p.is_file()])
    doc_files = sorted([p.relative_to(DOCS_DIR).as_posix() for p in DOCS_DIR.rglob("*") if p.is_file()])
    hash_mismatches = []
    if dep_files == doc_files:
        for rel in dep_files:
            if sha256_file(DEPLOY_DIR / rel) != sha256_file(DOCS_DIR / rel):
                hash_mismatches.append(rel)
    record(
        "100% Byte-for-Byte Mirror Parity (`15-WEB-DEPLOYMENT/` == `docs/`)",
        (dep_files == doc_files) and (len(hash_mismatches) == 0),
        f"files_in_each={len(dep_files)}, hash_mismatches={len(hash_mismatches)}"
    )

    # 11. Update PROJECT_STATE.json if 0 errors
    now_iso = datetime.now(timezone.utc).isoformat()
    if len(errors) == 0:
        state = json.loads(PROJECT_STATE_PATH.read_text(encoding="utf-8"))
        state.setdefault("phase_status", {})["Phase 10"] = "COMPLETED"
        state.setdefault("phases", {})["Phase 10"] = "COMPLETED"
        state["deployment_ready"] = True
        state["current_phase"] = "Phase 10: Completed — Static Web Deployment Portal & Live Interactive Hub Ready"
        state["studio_status"] = "100% PRODUCTION & CLOUD DEPLOYMENT READY (PHASES 1-10 VERIFIED, 0 ERRORS)"
        state["last_updated"] = now_iso
        state["phase10_deployment"] = {
            "deployment_dir": "15-WEB-DEPLOYMENT/",
            "github_pages_docs_dir": "docs/",
            "deployment_ready": True,
            "total_files_per_tree": len(dep_files),
            "routes": {
                "index.html": (DEPLOY_DIR / "index.html").stat().st_size,
                "app/index.html": (DEPLOY_DIR / "app" / "index.html").stat().st_size,
                "studio/index.html": (DEPLOY_DIR / "studio" / "index.html").stat().st_size,
                "atlas/index.html": (DEPLOY_DIR / "atlas" / "index.html").stat().st_size,
                "downloads/index.html": (DEPLOY_DIR / "downloads" / "index.html").stat().st_size,
                "404.html": (DEPLOY_DIR / "404.html").stat().st_size,
            },
            "embedded_atlas_svgs": svg_count,
            "runbook_words": runbook_words,
            "downloads_count": len(expected_downloads),
            "assets_count": len(expected_assets),
        }
        PROJECT_STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        record(
            "Update PROJECT_STATE.json (`Phase 10: COMPLETED`, `deployment_ready: true`)",
            True,
            "PROJECT_STATE.json updated cleanly"
        )

    # 12. Write formal QA report to `11-QA-REPORTS/phase10-deployment-qa-report.md`
    QA_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report_lines = [
        "# PHASE 10 QA REPORT — STATIC WEB DEPLOYMENT PORTAL & LIVE INTERACTIVE HUB",
        "",
        f"- **Product:** *The AI Content Creator & Solopreneur Operating System*",
        f"- **Verification Timestamp (UTC):** `{now_iso}`",
        f"- **Total Automated Checks Executed:** `{len(checks)}`",
        f"- **Passed:** `{sum(1 for _, s, _ in checks if s == 'PASS')}`",
        f"- **Errors:** `{len(errors)}`",
        f"- **Deployment Portal Trees:** `15-WEB-DEPLOYMENT/` & `docs/` (`{len(dep_files)}` identical files each)",
        "",
        "## Automated Verification Summary Table",
        "",
        "| # | Check Name | Status | Telemetry & Verification Detail |",
        "| :--- | :--- | :---: | :--- |",
    ]
    for idx, (name, status, detail) in enumerate(checks, start=1):
        report_lines.append(f"| {idx:02d} | {name} | **{status}** | {detail} |")

    report_lines.extend([
        "",
        "## Verified Production Routes (`15-WEB-DEPLOYMENT/` & `docs/`)",
        "",
        "| Route | File Path | Size (Bytes) | Description |",
        "| :--- | :--- | ---: | :--- |",
        f"| `/` | `index.html` | `{(DEPLOY_DIR / 'index.html').stat().st_size:,}` | Flagship Conversion Sales Landing Page, RPPH Calculator & Live Ecosystem Hub |",
        f"| `/app/` | `app/index.html` | `{(DEPLOY_DIR / 'app' / 'index.html').stat().st_size:,}` | Interactive SaaS-Lite Creator OS Web Companion Application (Free + Pro Key `CREATOR-OS-PRO-2026`) |",
        f"| `/studio/` | `studio/index.html` | `{(DEPLOY_DIR / 'studio' / 'index.html').stat().st_size:,}` | Interactive Cover, YouTube Thumbnail & Social Card Customizer Studio |",
        f"| `/atlas/` | `atlas/index.html` | `{(DEPLOY_DIR / 'atlas' / 'index.html').stat().st_size:,}` | Interactive Visual Shortcut Atlas & 31-Diagram Vector Architecture Explorer |",
        f"| `/downloads/` | `downloads/index.html` | `{(DEPLOY_DIR / 'downloads' / 'index.html').stat().st_size:,}` | Direct Tier 0 Free Audit Starter Kit Download Hub + 7 Self-Hosted Files |",
        f"| `/404.html` | `404.html` | `{(DEPLOY_DIR / '404.html').stat().st_size:,}` | Styled Creator Indigo 404 Fallback Route |",
        ""
    ])

    QA_REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")

    print("=" * 88)
    print(f"PHASE 10 QA SUMMARY: {len(checks) - len(errors)}/{len(checks)} PASSED | {len(errors)} ERRORS")
    print(f"QA Report written to: {QA_REPORT_PATH.relative_to(STUDIO_ROOT)}")
    print("=" * 88)

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
