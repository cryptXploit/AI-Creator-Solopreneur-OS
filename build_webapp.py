#!/usr/bin/env python3
"""
build_webapp.py
Offline Single-File SaaS-Lite Web Companion Application Compiler (Phase 6)
Flagship Product #3: The AI Content Creator & Solopreneur Operating System
Studio Root: e:/Ebook-Makaer/AI-Creator-Solopreneur-OS/DIGITAL-PUBLISHING-STUDIO/

Generates:
  1. 07-INTERACTIVE-TOOLS/creator-os-app.html (>= 180,000 bytes, 100% offline self-contained)
  2. 07-INTERACTIVE-TOOLS/PRO-ACCESS-LICENSE-KEY.txt (Pro Access Key: CREATOR-OS-PRO-2026)
  3. 07-INTERACTIVE-TOOLS/README-WEB-APP.md (>= 1,000 words comprehensive documentation)
  4. 04-VISUAL-ASSETS/png/webapp-dashboard-preview.png (1600x1000 headless browser UI preview)
  5. Updates PROJECT_STATE.json with Phase 6 completion & telemetry
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image

STUDIO_ROOT = Path(__file__).resolve().parent


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
    raise RuntimeError("No local Edge or Chrome binary found for headless screenshot rendering.")


BROWSER_BIN = find_browser_binary()


# ---------------------------------------------------------------------------
# 1. EXTRACT ALL 50 PROMPTS (P01-P50) & 12 EMERGENCY SCRIPTS (S01-S12)
# ---------------------------------------------------------------------------

CHAPTER_METADATA = {
    1: ("Stage 1: Operating Foundation", "Ch 01: The Creator-to-Operator Paradigm & 5-Stage OS"),
    2: ("Stage 1: Niche & Avatar Moat", "Ch 02: High-Margin Niche Positioning & Authority Moat"),
    3: ("Stage 2: Outlier Idea Mining", "Ch 03: Validated Idea Mining & S.I.G.N.A.L. Topic Matrix"),
    4: ("Stage 2: Packaging & Hooks", "Ch 04: Packaging Psychology & C.L.I.P. 3-Second Hooks"),
    5: ("Stage 3: Pillar Scripting", "Ch 05: High-Retention Pillar Scripting & Voice DNA"),
    6: ("Stage 3: 1-to-15 Repurposing", "Ch 06: The 1-to-15 Omnichannel Repurposing Engine"),
    7: ("Stage 4: Batch Production", "Ch 07: The 4-Hour Weekly Batch Pipeline & 12-Point QA"),
    8: ("Stage 4: Owned List Funnel", "Ch 08: Audience Ownership, Lead Magnets & Welcome Sequence"),
    9: ("Stage 5: Digital Products", "Ch 09: 4-Tier Digital Product Ladder & 14-Day Launch"),
    10: ("Stage 5: Sponsorships & CEO", "Ch 10: Brand Sponsorships & 20-Minute Friday CEO Cadence"),
}


def extract_Bracketed_vars(text: str) -> list[str]:
    """Extracts unique [VARIABLE_NAME] tokens suitable for interactive form inputs."""
    raw_matches = re.findall(r"\[([A-Za-z0-9_/\-\s,:$.%+]{2,48})\]", text)
    seen = set()
    cleaned = []
    skip_exact = {"x", "X", " ", "APPROVED / HOLD", "PASS / FAIL", "1/2/3/4"}
    for token in raw_matches:
        t = token.strip()
        if t in skip_exact or t.startswith("http"):
            continue
        if t not in seen:
            seen.add(t)
            cleaned.append(t)
    return cleaned[:12]


def load_prompts_and_scripts() -> tuple[list[dict], list[dict], list[dict]]:
    prompts_list: list[dict] = []

    for ch_idx in range(1, 11):
        ch_path = STUDIO_ROOT / "03-MANUSCRIPT" / f"chapter-{ch_idx:02d}.md"
        txt = ch_path.read_text(encoding="utf-8").replace("\r\n", "\n")
        stage_label, ch_label = CHAPTER_METADATA[ch_idx]

        # Match heading + fenced prompt block
        pattern = re.compile(
            r"###\s+Prompt\s+(P\d{2}):\s*([^\n]+)\n+```(?:text)?\n(PROMPT ID:\s*\1.*?)```",
            flags=re.DOTALL,
        )
        matches = pattern.findall(txt)
        if len(matches) != 5:
            # Fallback match by fenced block
            fallback_blocks = re.findall(r"```(?:text)?\n(PROMPT ID:\s*(P\d{2}).*?)```", txt, flags=re.DOTALL)
            matches = []
            for body_str, pid in fallback_blocks:
                title_m = re.search(rf"###\s+Prompt\s+{pid}:\s*([^\n]+)", txt)
                p_title = title_m.group(1).strip() if title_m else f"Studio Workflow Prompt {pid}"
                matches.append((pid, p_title, body_str))

        for pid, p_title, p_body in matches:
            body_clean = p_body.strip()
            role_m = re.search(r"^ROLE:\s*(.+)$", body_clean, flags=re.MULTILINE)
            role_str = role_m.group(1).strip() if role_m else "Specialized AI Studio Operator"
            vars_found = extract_Bracketed_vars(body_clean)
            prompts_list.append({
                "id": pid,
                "title": p_title.strip(),
                "chapter": ch_idx,
                "chapterLabel": ch_label,
                "stage": stage_label,
                "role": role_str,
                "tier": "FREE" if ch_idx == 1 else "PRO",
                "variables": vars_found,
                "body": body_clean,
            })

    if len(prompts_list) != 50:
        raise RuntimeError(f"Expected 50 prompts (P01-P50), extracted {len(prompts_list)}")

    # Extract 12 Emergency Scripts (S01-S12) from back-matter.md
    bm_path = STUDIO_ROOT / "03-MANUSCRIPT/back-matter.md"
    bm_txt = bm_path.read_text(encoding="utf-8").replace("\r\n", "\n")

    script_pattern = re.compile(
        r"###\s+Script\s+`?(S\d{2})`?:\s*([^\n]+)\n+(.*?)```(?:text)?\n(.*?)```\s*\n\*\s+\*\*CUSTOMIZATION NOTES:\*\*\s*([^\n]+)",
        flags=re.DOTALL,
    )
    s_matches = script_pattern.findall(bm_txt)
    scripts_list: list[dict] = []

    for sid, s_title, meta_block, s_body, notes_line in s_matches:
        trig_m = re.search(r"\*\*SCENARIO TRIGGER:\*\*\s*([^\n]+)", meta_block)
        mech_m = re.search(r"\*\*PSYCHOLOGICAL MECHANISM:\*\*\s*([^\n]+)", meta_block)
        vars_found = extract_Bracketed_vars(s_body)
        scripts_list.append({
            "id": sid,
            "title": s_title.strip(),
            "scenario": trig_m.group(1).strip() if trig_m else "High-stakes creator commercial negotiation",
            "mechanism": mech_m.group(1).strip() if mech_m else "Scope-anchored value protection",
            "notes": notes_line.strip(),
            "tier": "FREE" if sid in {"S01", "S02"} else "PRO",
            "variables": vars_found,
            "body": s_body.strip(),
        })

    if len(scripts_list) != 12:
        raise RuntimeError(f"Expected 12 emergency scripts (S01-S12), extracted {len(scripts_list)}")

    # Extract 100-item Master Implementation Checklist (10 items per chapter from Section 13 of each chapter)
    checklist_items: list[dict] = []
    for ch_idx in range(1, 11):
        ch_path = STUDIO_ROOT / "03-MANUSCRIPT" / f"chapter-{ch_idx:02d}.md"
        txt = ch_path.read_text(encoding="utf-8").replace("\r\n", "\n")
        stage_label, ch_label = CHAPTER_METADATA[ch_idx]
        # Find checkbox lines "- [ ] **..."
        chk_lines = re.findall(r"^-\s+\[\s\]\s+\*\*(.+?)\*\*:?\s*(.*)$", txt, flags=re.MULTILINE)
        for idx_c, (head_c, tail_c) in enumerate(chk_lines[:10], start=1):
            clean_head = re.sub(r"^\d+\.\s*", "", head_c.strip())
            clean_tail = re.sub(r"\$[^\$]+\$", lambda m: m.group(0).replace("\\text", "").replace("{", "").replace("}", "").replace("$", ""), tail_c.strip())
            checklist_items.append({
                "id": f"CH{ch_idx:02d}-GATE-{idx_c:02d}",
                "chapter": ch_idx,
                "chapterLabel": ch_label,
                "stage": stage_label,
                "title": clean_head,
                "detail": clean_tail,
            })

    return prompts_list, scripts_list, checklist_items


def load_inline_svg_gallery() -> list[dict]:
    """Loads the 20 vector SVGs so operators can inspect system architecture offline inside Module 6."""
    gallery = []
    for ch_idx in range(1, 11):
        _, ch_label = CHAPTER_METADATA[ch_idx]
        for kind, kind_label in [("mindmap", "System Architecture Mindmap"), ("flowchart", "Operational Decision Tree")]:
            svg_p = STUDIO_ROOT / "04-VISUAL-ASSETS/svg" / f"chapter-{ch_idx:02d}-{kind}.svg"
            raw_svg = svg_p.read_text(encoding="utf-8")
            uid = f"app-ch{ch_idx:02d}-{kind}"
            for marker_id in ["arrow-indigo", "arrow-teal", "arrow-amber", "arrow-slate", "arrow"]:
                raw_svg = raw_svg.replace(f'id="{marker_id}"', f'id="{uid}-{marker_id}"')
                raw_svg = raw_svg.replace(f"url(#{marker_id})", f"url(#{uid}-{marker_id})")
            gallery.append({
                "id": f"chapter-{ch_idx:02d}-{kind}",
                "chapter": ch_idx,
                "chapterLabel": ch_label,
                "type": kind_label,
                "svg": raw_svg,
            })
    return gallery


# ---------------------------------------------------------------------------
# 2. BUILD SINGLE-FILE OFFLINE SAAS-LITE APPLICATION (creator-os-app.html)
# ---------------------------------------------------------------------------

def build_webapp_html() -> str:
    prompts_data, scripts_data, checklist_data = load_prompts_and_scripts()
    svg_gallery_data = load_inline_svg_gallery()

    prompts_json = json.dumps(prompts_data, ensure_ascii=False)
    scripts_json = json.dumps(scripts_data, ensure_ascii=False)
    checklist_json = json.dumps(checklist_data, ensure_ascii=False)
    svg_gallery_json = json.dumps(svg_gallery_data, ensure_ascii=False)

    html_app = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>The AI Content Creator &amp; Solopreneur Operating System — Interactive Companion Suite (v1.0.0)</title>
<style>
  :root {{
    --primary: #0F172A;
    --primary-light: #1E293B;
    --accent: #4F46E5;
    --accent-hover: #4338CA;
    --accent-soft: #EEF2FF;
    --secondary: #0D9488;
    --secondary-soft: #F0FDFA;
    --warning: #D97706;
    --warning-soft: #FFFBEB;
    --danger: #DC2626;
    --danger-soft: #FEF2F2;
    --text: #1E293B;
    --muted: #64748B;
    --border: #CBD5E1;
    --bg: #FFFFFF;
    --bg-alt: #F8FAFC;
    --card-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans', sans-serif;
    --font-mono: 'JetBrains Mono', 'Consolas', 'SFMono-Regular', monospace;
  }}

  html[data-theme="dark"] {{
    --primary: #F8FAFC;
    --primary-light: #E2E8F0;
    --accent: #6366F1;
    --accent-hover: #818CF8;
    --accent-soft: #1E1B4B;
    --secondary: #14B8A6;
    --secondary-soft: #042F2E;
    --warning: #F59E0B;
    --warning-soft: #451A03;
    --text: #E2E8F0;
    --muted: #94A3B8;
    --border: #334155;
    --bg: #0F172A;
    --bg-alt: #1E293B;
    --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: var(--font-sans);
    background-color: var(--bg-alt);
    color: var(--text);
    line-height: 1.5;
    font-size: 14px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }}

  /* Top Command Header */
  .app-header {{
    background-color: #0F172A;
    color: #FFFFFF;
    padding: 12px 24px;
    border-bottom: 3px solid #4F46E5;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    position: sticky;
    top: 0;
    z-index: 100;
  }}

  .brand-cluster {{
    display: flex;
    align-items: center;
    gap: 14px;
  }}

  .brand-logo {{
    width: 38px;
    height: 38px;
    border-radius: 8px;
    background: linear-gradient(135deg, #4F46E5 0%, #0D9488 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 15px;
    color: #FFFFFF;
    letter-spacing: -0.5px;
    flex-shrink: 0;
  }}

  .brand-titles h1 {{
    font-size: 15.5px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.2px;
  }}

  .brand-titles p {{
    font-size: 11.5px;
    color: #94A3B8;
  }}

  .header-controls {{
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }}

  .tier-badge {{
    padding: 5px 11px;
    border-radius: 999px;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 0.3px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }}

  .tier-badge.free {{
    background-color: rgba(217, 119, 6, 0.2);
    border: 1px solid #D97706;
    color: #FBBF24;
  }}

  .tier-badge.pro {{
    background-color: rgba(13, 148, 136, 0.25);
    border: 1px solid #0D9488;
    color: #2DD4BF;
  }}

  .btn {{
    font-family: var(--font-sans);
    font-size: 12.5px;
    font-weight: 600;
    padding: 7px 13px;
    border-radius: 6px;
    border: 1px solid transparent;
    cursor: pointer;
    transition: all 0.15s ease;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }}

  .btn-primary {{
    background-color: var(--accent);
    color: #FFFFFF;
  }}
  .btn-primary:hover {{
    background-color: var(--accent-hover);
  }}

  .btn-teal {{
    background-color: var(--secondary);
    color: #FFFFFF;
  }}
  .btn-teal:hover {{
    opacity: 0.92;
  }}

  .btn-amber {{
    background-color: var(--warning);
    color: #FFFFFF;
  }}

  .btn-outline {{
    background-color: transparent;
    border-color: #475569;
    color: #E2E8F0;
  }}
  .btn-outline:hover {{
    background-color: #1E293B;
  }}

  .btn-ghost {{
    background-color: var(--bg);
    border: 1px solid var(--border);
    color: var(--text);
  }}
  .btn-ghost:hover {{
    border-color: var(--accent);
    color: var(--accent);
  }}

  /* Pro Activation Banner */
  .pro-activation-bar {{
    background: linear-gradient(90deg, #1E1B4B 0%, #0F172A 60%, #042F2E 100%);
    color: #FFFFFF;
    padding: 9px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    border-bottom: 1px solid #334155;
    font-size: 12.5px;
  }}

  .pro-input-group {{
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }}

  .pro-input-group input {{
    background-color: #0F172A;
    border: 1px solid #4F46E5;
    color: #FFFFFF;
    padding: 5px 10px;
    border-radius: 5px;
    font-family: var(--font-mono);
    font-size: 12px;
    width: 210px;
  }}

  /* Main Workspace Layout */
  .workspace-shell {{
    display: grid;
    grid-template-columns: 265px 1fr;
    flex: 1;
    min-height: calc(100vh - 110px);
  }}

  @media (max-width: 980px) {{
    .workspace-shell {{
      grid-template-columns: 1fr;
    }}
  }}

  /* Left Navigation Sidebar */
  .sidebar-nav {{
    background-color: var(--bg);
    border-right: 1px solid var(--border);
    padding: 16px 12px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 16px;
  }}

  .nav-section-label {{
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: var(--muted);
    padding: 0 10px;
    margin-bottom: 6px;
  }}

  .module-tab-btn {{
    width: 100%;
    text-align: left;
    padding: 10px 12px;
    border-radius: 8px;
    border: 1px solid transparent;
    background: transparent;
    color: var(--text);
    cursor: pointer;
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 5px;
    transition: all 0.15s ease;
  }}

  .module-tab-btn:hover {{
    background-color: var(--bg-alt);
    border-color: var(--border);
  }}

  .module-tab-btn.active {{
    background-color: var(--accent-soft);
    border-color: var(--accent);
    color: var(--accent);
  }}

  .mod-num {{
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    background-color: var(--bg-alt);
    color: var(--primary);
    flex-shrink: 0;
  }}

  .module-tab-btn.active .mod-num {{
    background-color: var(--accent);
    color: #FFFFFF;
  }}

  .mod-text-wrap {{
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}

  .mod-title {{
    font-size: 12.5px;
    font-weight: 700;
    line-height: 1.25;
  }}

  .mod-sub {{
    font-size: 11px;
    color: var(--muted);
  }}

  /* Content Pane */
  .main-content {{
    padding: 22px 28px;
    overflow-y: auto;
    max-width: 1440px;
  }}

  .module-panel {{
    display: none;
  }}

  .module-panel.active {{
    display: block;
  }}

  .module-header-banner {{
    background-color: var(--bg);
    border: 1px solid var(--border);
    border-left: 5px solid var(--accent);
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 20px;
    box-shadow: var(--card-shadow);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
  }}

  .module-header-banner h2 {{
    font-size: 18px;
    font-weight: 800;
    color: var(--primary);
  }}

  .module-header-banner p {{
    font-size: 12.5px;
    color: var(--muted);
    margin-top: 3px;
  }}

  /* Grid & Cards */
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-bottom: 18px;
  }}

  .grid-3 {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 18px;
  }}

  .grid-4 {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 18px;
  }}

  @media (max-width: 1100px) {{
    .grid-2, .grid-3, .grid-4 {{
      grid-template-columns: 1fr;
    }}
  }}

  .card {{
    background-color: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 18px;
    box-shadow: var(--card-shadow);
  }}

  .card-title {{
    font-size: 14px;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .kpi-card {{
    background-color: var(--bg);
    border: 1px solid var(--border);
    border-top: 4px solid var(--accent);
    border-radius: 8px;
    padding: 14px 16px;
    box-shadow: var(--card-shadow);
  }}

  .kpi-card.teal {{
    border-top-color: var(--secondary);
  }}

  .kpi-card.amber {{
    border-top-color: var(--warning);
  }}

  .kpi-label {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--muted);
  }}

  .kpi-value {{
    font-family: var(--font-mono);
    font-size: 23px;
    font-weight: 800;
    color: var(--primary);
    margin: 5px 0 3px 0;
  }}

  .kpi-sub {{
    font-size: 11.5px;
    color: var(--secondary);
    font-weight: 600;
  }}

  /* Form Controls */
  .form-group {{
    margin-bottom: 11px;
  }}

  .form-group label {{
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 4px;
  }}

  .form-control {{
    width: 100%;
    padding: 7px 10px;
    border: 1px solid var(--border);
    border-radius: 6px;
    background-color: var(--bg-alt);
    color: var(--text);
    font-family: var(--font-sans);
    font-size: 13px;
  }}

  .form-control:focus {{
    outline: none;
    border-color: var(--accent);
    background-color: var(--bg);
  }}

  /* Progress & Bar Visualizations */
  .bar-track {{
    width: 100%;
    height: 12px;
    background-color: var(--bg-alt);
    border: 1px solid var(--border);
    border-radius: 999px;
    overflow: hidden;
    margin: 6px 0;
  }}

  .bar-fill {{
    height: 100%;
    background: linear-gradient(90deg, #4F46E5 0%, #0D9488 100%);
    border-radius: 999px;
    transition: width 0.25s ease;
  }}

  /* Prompt & Script Vault Specifics */
  .vault-layout {{
    display: grid;
    grid-template-columns: 350px 1fr;
    gap: 18px;
  }}

  @media (max-width: 1024px) {{
    .vault-layout {{
      grid-template-columns: 1fr;
    }}
  }}

  .vault-list-container {{
    max-height: 680px;
    overflow-y: auto;
    border: 1px solid var(--border);
    border-radius: 8px;
    background-color: var(--bg);
  }}

  .vault-item {{
    padding: 10px 12px;
    border-bottom: 1px solid var(--border);
    cursor: pointer;
    transition: background 0.12s ease;
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}

  .vault-item:hover {{
    background-color: var(--bg-alt);
  }}

  .vault-item.active {{
    background-color: var(--accent-soft);
    border-left: 4px solid var(--accent);
  }}

  .vault-item-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .vault-id-badge {{
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    background-color: #0F172A;
    color: #FFFFFF;
  }}

  .tier-pill {{
    font-size: 10px;
    font-weight: 700;
    padding: 1px 6px;
    border-radius: 4px;
  }}

  .tier-pill.free {{
    background-color: var(--secondary-soft);
    color: var(--secondary);
    border: 1px solid var(--secondary);
  }}

  .tier-pill.pro {{
    background-color: var(--accent-soft);
    color: var(--accent);
    border: 1px solid var(--accent);
  }}

  .compiled-prompt-box {{
    font-family: var(--font-mono);
    font-size: 12.5px;
    line-height: 1.55;
    background-color: #0F172A;
    color: #F8FAFC;
    padding: 16px;
    border-radius: 8px;
    border-left: 4px solid #4F46E5;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 500px;
    overflow-y: auto;
  }}

  /* Data Tables */
  .studio-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
  }}

  .studio-table th {{
    background-color: var(--bg-alt);
    color: var(--primary);
    font-weight: 700;
    text-align: left;
    padding: 9px 10px;
    border: 1px solid var(--border);
  }}

  .studio-table td {{
    padding: 8px 10px;
    border: 1px solid var(--border);
    vertical-align: middle;
  }}

  .status-pill {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
  }}

  .status-green {{
    background-color: var(--secondary-soft);
    color: var(--secondary);
    border: 1px solid var(--secondary);
  }}

  .status-amber {{
    background-color: var(--warning-soft);
    color: var(--warning);
    border: 1px solid var(--warning);
  }}

  .status-red {{
    background-color: var(--danger-soft);
    color: var(--danger);
    border: 1px solid var(--danger);
  }}

  .toast-notification {{
    position: fixed;
    bottom: 20px;
    right: 24px;
    background-color: #0F172A;
    color: #FFFFFF;
    border-left: 4px solid #0D9488;
    padding: 12px 18px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    display: none;
    z-index: 999;
  }}

  .svg-preview-box svg {{
    width: 100%;
    height: auto;
    max-height: 440px;
    display: block;
    margin: 0 auto;
    background: #FFFFFF;
    border-radius: 6px;
  }}

  @media print {{
    .app-header, .pro-activation-bar, .sidebar-nav {{
      display: none !important;
    }}
    .workspace-shell {{
      display: block !important;
    }}
    .module-panel {{
      display: block !important;
      margin-bottom: 28px;
      page-break-after: always;
    }}
  }}
</style>
</head>
<body>

<!-- TOP STUDIO HEADER -->
<header class="app-header">
  <div class="brand-cluster">
    <div class="brand-logo">OS</div>
    <div class="brand-titles">
      <h1>The AI Content Creator &amp; Solopreneur Operating System</h1>
      <p>100% Offline SaaS-Lite Companion Suite · 50 AI Workflow Prompts · 12 Emergency Scripts · 6 Calculators</p>
    </div>
  </div>
  <div class="header-controls">
    <span id="accessModeBadge" class="tier-badge pro">● PRO FULL OS ACTIVE</span>
    <button type="button" class="btn btn-outline" onclick="toggleAccessTier()" title="Switch between Tier 0 Free Diagnostic Mode and Pro Full OS Mode">Switch Free / Pro Mode</button>
    <button type="button" class="btn btn-outline" onclick="toggleTheme()">Dark / Light Theme</button>
    <button type="button" class="btn btn-teal" onclick="exportWorkspaceJSON()">Export JSON</button>
    <button type="button" class="btn btn-outline" onclick="document.getElementById('importJsonInput').click()">Import JSON</button>
    <input type="file" id="importJsonInput" accept=".json" style="display:none" onchange="importWorkspaceJSON(event)" />
    <button type="button" class="btn btn-primary" onclick="exportScorecardCSV()">Export CSV</button>
    <button type="button" class="btn btn-outline" onclick="window.print()">Print / PDF</button>
  </div>
</header>

<!-- PRO ACCESS LICENSE ACTIVATION BAR -->
<div class="pro-activation-bar" id="proActivationBar">
  <div>
    <strong>Commercial Access Control:</strong> Tier 0 Free Diagnostic Mode activates Module 1, Prompts <code>P01–P05</code> &amp; Scripts <code>S01–S02</code>. Enter your Pro Access License Key (<code>CREATOR-OS-PRO-2026</code>) to activate all 50 Prompts, 12 Scripts &amp; Pro Simulators.
  </div>
  <div class="pro-input-group">
    <input type="text" id="licenseKeyInput" placeholder="Enter CREATOR-OS-PRO-2026" value="CREATOR-OS-PRO-2026" />
    <button type="button" class="btn btn-teal" onclick="activateProLicenseKey()">Activate Pro Access</button>
    <button type="button" class="btn btn-amber" onclick="instantDemoProActivate()">1-Click Demo Pro Mode</button>
  </div>
</div>

<!-- MAIN WORKSPACE SHELL -->
<div class="workspace-shell">
  <!-- LEFT NAVIGATION SIDEBAR -->
  <aside class="sidebar-nav">
    <div>
      <div class="nav-section-label">6 Core Operating Modules</div>
      <button type="button" class="module-tab-btn active" data-mod="mod1" onclick="switchModule('mod1')">
        <span class="mod-num">M1</span>
        <span class="mod-text-wrap">
          <span class="mod-title">RPPH, RPM &amp; Value-Ladder Simulator</span>
          <span class="mod-sub">Ch 1 &amp; Ch 9 Unit Economics</span>
        </span>
      </button>
      <button type="button" class="module-tab-btn" data-mod="mod2" onclick="switchModule('mod2')">
        <span class="mod-num">M2</span>
        <span class="mod-text-wrap">
          <span class="mod-title">50-Prompt &amp; 12-Script Vault</span>
          <span class="mod-sub">P01–P50 + S01–S12 Compiler</span>
        </span>
      </button>
      <button type="button" class="module-tab-btn" data-mod="mod3" onclick="switchModule('mod3')">
        <span class="mod-num">M3</span>
        <span class="mod-text-wrap">
          <span class="mod-title">S.I.G.N.A.L. Outlier &amp; C.L.I.P. Studio</span>
          <span class="mod-sub">Ch 2–4 Niche, Idea &amp; Hook Lab</span>
        </span>
      </button>
      <button type="button" class="module-tab-btn" data-mod="mod4" onclick="switchModule('mod4')">
        <span class="mod-num">M4</span>
        <span class="mod-text-wrap">
          <span class="mod-title">1-to-15 Matrix &amp; 4-Hr Batch Sprint</span>
          <span class="mod-sub">Ch 5–7 Waterfall &amp; Sprint Timer</span>
        </span>
      </button>
      <button type="button" class="module-tab-btn" data-mod="mod5" onclick="switchModule('mod5')">
        <span class="mod-num">M5</span>
        <span class="mod-text-wrap">
          <span class="mod-title">Sponsorship Rate Card Calculator</span>
          <span class="mod-sub">Ch 10 C.P.M. Plus Outcome Pricing</span>
        </span>
      </button>
      <button type="button" class="module-tab-btn" data-mod="mod6" onclick="switchModule('mod6')">
        <span class="mod-num">M6</span>
        <span class="mod-text-wrap">
          <span class="mod-title">Friday CEO Scorecard &amp; 10-Ch OS</span>
          <span class="mod-sub">100-Gate Checklist + 20 Diagrams</span>
        </span>
      </button>
    </div>

    <div class="card" style="padding:12px; font-size:11.5px;">
      <div style="font-weight:700; color:var(--primary); margin-bottom:4px;">100% Local Privacy Guarantee</div>
      <p style="color:var(--muted);">All financial metrics, prompt presets, and checklists persist strictly in your browser's offline <code>localStorage</code>. Zero external network calls.</p>
      <button type="button" class="btn btn-ghost" style="width:100%; margin-top:8px; justify-content:center;" onclick="resetAllWorkspaceData()">Reset Default Demo Data</button>
    </div>
  </aside>

  <!-- MAIN INTERACTIVE CONTENT AREA -->
  <main class="main-content">

    <!-- =================================================================== -->
    <!-- MODULE 1: CREATOR RPPH, RPM & 4-TIER VALUE-LADDER SIMULATOR         -->
    <!-- =================================================================== -->
    <section id="mod1" class="module-panel active">
      <div class="module-header-banner">
        <div>
          <h2>Module 1: Creator RPPH, RPM &amp; 4-Tier Value-Ladder Simulator</h2>
          <p>Quantify your Revenue Per Production Hour (RPPH), model your 4-Tier Digital Product Value Ladder, and diagnose your #1 Content-to-Cash bottleneck.</p>
        </div>
        <span class="status-pill status-green">Active in Free &amp; Pro Modes</span>
      </div>

      <!-- Top KPI Telemetry Strip -->
      <div class="grid-4">
        <div class="kpi-card">
          <div class="kpi-label">Current Baseline RPPH</div>
          <div class="kpi-value" id="m1_curr_rpph">$28.40/hr</div>
          <div class="kpi-sub" id="m1_curr_hours_label">34.0 hrs/wk · $3,862/mo</div>
        </div>
        <div class="kpi-card teal">
          <div class="kpi-label">Systematized Target RPPH</div>
          <div class="kpi-value" id="m1_sys_rpph">$248.50/hr</div>
          <div class="kpi-sub" id="m1_sys_hours_label">18.0 hrs/wk · $17,892/mo</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Blended Effective RPM</div>
          <div class="kpi-value" id="m1_blended_rpm">$210.49</div>
          <div class="kpi-sub">Total Rev per 1,000 Views</div>
        </div>
        <div class="kpi-card amber">
          <div class="kpi-label">Primary System Bottleneck</div>
          <div class="kpi-value" style="font-size:16px;" id="m1_bottleneck_badge">Time-Leak &amp; Capture</div>
          <div class="kpi-sub" id="m1_hours_saved_label">Saves 16.0 hrs/week (832 hrs/yr)</div>
        </div>
      </div>

      <div class="grid-2">
        <!-- Left Column: Weekly Time-Allocation & Traffic Inputs -->
        <div class="card">
          <div class="card-title">
            <span>1. Weekly Production Hours &amp; Traffic Inputs</span>
            <span style="font-size:11px; color:var(--muted);">Chapter 1 Audit</span>
          </div>
          <div class="grid-2" style="margin-bottom:0;">
            <div class="form-group">
              <label>Ideation &amp; Research (hrs/wk) <span id="val_h_idea">5.0</span></label>
              <input type="number" step="0.5" min="0" max="40" id="m1_h_idea" class="form-control" value="5.0" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Pillar Scripting (hrs/wk) <span id="val_h_script">7.0</span></label>
              <input type="number" step="0.5" min="0" max="40" id="m1_h_script" class="form-control" value="7.0" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Recording &amp; Takes (hrs/wk) <span id="val_h_rec">5.0</span></label>
              <input type="number" step="0.5" min="0" max="40" id="m1_h_rec" class="form-control" value="5.0" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Editing &amp; Revisions (hrs/wk) <span id="val_h_edit">9.0</span></label>
              <input type="number" step="0.5" min="0" max="40" id="m1_h_edit" class="form-control" value="9.0" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Manual Repurposing (hrs/wk) <span id="val_h_rep">5.0</span></label>
              <input type="number" step="0.5" min="0" max="40" id="m1_h_rep" class="form-control" value="5.0" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Admin &amp; Inbound DMs (hrs/wk) <span id="val_h_adm">3.0</span></label>
              <input type="number" step="0.5" min="0" max="40" id="m1_h_adm" class="form-control" value="3.0" oninput="recalcModule1()" />
            </div>
          </div>
          <hr style="border:none; border-top:1px solid var(--border); margin:10px 0;" />
          <div class="grid-2" style="margin-bottom:0;">
            <div class="form-group">
              <label>Monthly Views / Impressions</label>
              <input type="number" step="1000" min="100" id="m1_views" class="form-control" value="85000" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Platform AdSense RPM ($)</label>
              <input type="number" step="0.5" min="0" id="m1_adsense_rpm" class="form-control" value="6.50" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Current Monthly Revenue ($)</label>
              <input type="number" step="100" min="0" id="m1_curr_rev" class="form-control" value="3862" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Target Batch Sprint Hours/Wk</label>
              <input type="number" step="0.5" min="4" max="30" id="m1_target_hrs" class="form-control" value="18.0" oninput="recalcModule1()" />
            </div>
          </div>
        </div>

        <!-- Right Column: 4-Tier Value Ladder & Funnel Conversion Inputs -->
        <div class="card">
          <div class="card-title">
            <span>2. Owned Funnel &amp; 4-Tier Value Ladder Inputs</span>
            <span style="font-size:11px; color:var(--secondary);">Chapters 8–10 Engine</span>
          </div>
          <div class="grid-2" style="margin-bottom:0;">
            <div class="form-group">
              <label>View-to-Opt-In Capture Rate (%)</label>
              <input type="number" step="0.1" min="0.1" max="20" id="m1_optin_rate" class="form-control" value="1.8" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Tier 1 Impulse Price ($24–$49)</label>
              <input type="number" step="1" min="9" id="m1_t1_price" class="form-control" value="29" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Tier 1 Welcome Buyer CVR (%)</label>
              <input type="number" step="0.5" min="0" max="25" id="m1_t1_cvr" class="form-control" value="4.5" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Tier 2 Core System Price ($49–$199)</label>
              <input type="number" step="5" min="29" id="m1_t2_price" class="form-control" value="99" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Tier 2 Core Buyer CVR (%)</label>
              <input type="number" step="0.2" min="0" max="15" id="m1_t2_cvr" class="form-control" value="2.8" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Checkout Order Bump Lift (%)</label>
              <input type="number" step="5" min="0" max="100" id="m1_bump_lift" class="form-control" value="42" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Tier 3/4 High-Ticket Price ($)</label>
              <input type="number" step="50" min="99" id="m1_t3_price" class="form-control" value="997" oninput="recalcModule1()" />
            </div>
            <div class="form-group">
              <label>Monthly Sponsorship Retainers ($)</label>
              <input type="number" step="250" min="0" id="m1_sponsor_rev" class="form-control" value="4500" oninput="recalcModule1()" />
            </div>
          </div>

          <div style="margin-top:12px; padding:12px; background:var(--bg-alt); border-radius:6px; border:1px solid var(--border);">
            <div style="font-size:12px; font-weight:700; color:var(--primary); margin-bottom:6px;">Monthly Revenue Mix Breakdown (Systematized OS)</div>
            <div id="m1_revenue_breakdown_bars"></div>
          </div>
        </div>
      </div>

      <!-- Automated Diagnostic Prescription Box -->
      <div class="card">
        <div class="card-title">
          <span>3. Automated Bottleneck Diagnosis &amp; Stage-Gate Prescription</span>
          <span class="status-pill status-green" id="m1_annual_projection_pill">Annualized Run-Rate: $214,704/yr</span>
        </div>
        <p id="m1_diagnostic_narrative" style="font-size:13px; color:var(--text);"></p>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- MODULE 2: INTERACTIVE 50-PROMPT & 12-SCRIPT VAULT                   -->
    <!-- =================================================================== -->
    <section id="mod2" class="module-panel">
      <div class="module-header-banner">
        <div>
          <h2>Module 2: Interactive 50-Prompt &amp; 12-Script Command Vault (<code>P01–P50</code> &amp; <code>S01–S12</code>)</h2>
          <p>Select any AI Workflow Prompt or Emergency Communication Script, customize its <code>[BRACKETED_VARIABLES]</code> via live form inputs, and copy the compiled prompt in 1 click.</p>
        </div>
        <div style="display:flex; gap:8px;">
          <button type="button" class="btn btn-primary" id="btnVaultModePrompts" onclick="setVaultCategory('prompts')">50 AI Prompts (P01–P50)</button>
          <button type="button" class="btn btn-ghost" id="btnVaultModeScripts" onclick="setVaultCategory('scripts')">12 Emergency Scripts (S01–S12)</button>
        </div>
      </div>

      <div class="vault-layout">
        <!-- Left Column: Filterable Selector List -->
        <div>
          <div class="card" style="padding:12px; margin-bottom:12px;">
            <div class="form-group">
              <label>Search by ID, Title, Role, or Variable</label>
              <input type="text" id="vaultSearchInput" class="form-control" placeholder="e.g., P01, Hook, Newsletter, S02..." oninput="renderVaultList()" />
            </div>
            <div class="form-group" style="margin-bottom:0;" id="chapterFilterWrap">
              <label>Filter by Chapter / OS Stage</label>
              <select id="vaultChapterFilter" class="form-control" onchange="renderVaultList()">
                <option value="ALL">All 10 Chapters (P01–P50)</option>
                <option value="1">Ch 01: Creator-to-Operator OS (P01–P05) [FREE]</option>
                <option value="2">Ch 02: Niche Positioning &amp; Moat (P06–P10)</option>
                <option value="3">Ch 03: Outlier Idea Mining (P11–P15)</option>
                <option value="4">Ch 04: Packaging &amp; 3s Hooks (P16–P20)</option>
                <option value="5">Ch 05: Pillar Scripting &amp; Voice DNA (P21–P25)</option>
                <option value="6">Ch 06: 1-to-15 Repurposing Engine (P26–P30)</option>
                <option value="7">Ch 07: 4-Hr Batch Pipeline &amp; QA (P31–P35)</option>
                <option value="8">Ch 08: Lead Magnets &amp; Welcome Funnel (P36–P40)</option>
                <option value="9">Ch 09: 4-Tier Product Ladder &amp; Launch (P41–P45)</option>
                <option value="10">Ch 10: Sponsorships &amp; Friday CEO (P46–P50)</option>
              </select>
            </div>
          </div>

          <div class="vault-list-container" id="vaultListContainer"></div>
        </div>

        <!-- Right Column: Dynamic Variable Compiler & Live Prompt Output -->
        <div>
          <div class="card" style="margin-bottom:16px;">
            <div class="card-title">
              <span id="selectedVaultHeading">P01: Creator Time-Leak &amp; RPPH Diagnostic Auditor</span>
              <span id="selectedVaultStageBadge" class="tier-pill free">Ch 01 · FREE</span>
            </div>
            <p id="selectedVaultMeta" style="font-size:12px; color:var(--muted); margin-bottom:12px;"></p>

            <!-- Dynamic Bracketed Variable Form Builder -->
            <div id="dynamicVariablesContainer" style="background:var(--bg-alt); padding:12px; border-radius:6px; border:1px solid var(--border); margin-bottom:14px;"></div>

            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
              <strong style="font-size:12.5px; color:var(--primary);">Live Compiled Output (Ready to Copy-Paste into Claude / ChatGPT / Gemini):</strong>
              <div style="display:flex; gap:8px;">
                <button type="button" class="btn btn-ghost" onclick="resetCurrentPromptVariables()">Reset Variables</button>
                <button type="button" class="btn btn-teal" onclick="savePromptPresetToStorage()">Save Variable Preset</button>
                <button type="button" class="btn btn-primary" onclick="copyCompiledVaultOutput()">1-Click Copy Compiled Text</button>
              </div>
            </div>

            <pre class="compiled-prompt-box" id="compiledPromptOutput"></pre>
          </div>
        </div>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- MODULE 3: S.I.G.N.A.L. OUTLIER VALIDATOR & C.L.I.P. STUDIO          -->
    <!-- =================================================================== -->
    <section id="mod3" class="module-panel">
      <div class="module-header-banner">
        <div>
          <h2>Module 3: S.I.G.N.A.L. Outlier Topic Validator &amp; C.L.I.P. Packaging Studio</h2>
          <p>Score your Niche Monetization Potential Index (NMPI), validate Outlier Multipliers (M_outlier &gt;= 2.5x), and stress-test your 3-Second C.L.I.P. Hooks before scripting.</p>
        </div>
        <span class="status-pill status-green">Chapters 2, 3 &amp; 4 Engine</span>
      </div>

      <div class="grid-2">
        <!-- Part A: P.A.I.D. Niche & S.I.G.N.A.L. Outlier Scorer -->
        <div class="card">
          <div class="card-title">
            <span>Part A: P.A.I.D. Niche &amp; S.I.G.N.A.L. Outlier Scorer</span>
            <span id="m3_nmpi_badge" class="status-pill status-green">NMPI: 76.5 / 100 (GO)</span>
          </div>
          <div class="grid-2" style="margin-bottom:8px;">
            <div class="form-group">
              <label>Pain Urgency Score (1–10)</label>
              <input type="number" min="1" max="10" id="m3_pain" class="form-control" value="9" oninput="recalcModule3()" />
            </div>
            <div class="form-group">
              <label>Purchasing Power Score (1–10)</label>
              <input type="number" min="1" max="10" id="m3_power" class="form-control" value="9" oninput="recalcModule3()" />
            </div>
            <div class="form-group">
              <label>Sponsor/Product Margin (1–10)</label>
              <input type="number" min="1" max="10" id="m3_margin" class="form-control" value="8" oninput="recalcModule3()" />
            </div>
            <div class="form-group">
              <label>Content Saturation (1=Low, 10=High)</label>
              <input type="number" min="1" max="10" id="m3_sat" class="form-control" value="4" oninput="recalcModule3()" />
            </div>
          </div>
          <hr style="border:none; border-top:1px solid var(--border); margin:12px 0;" />
          <div class="form-group">
            <label>Candidate Pillar Topic Title</label>
            <input type="text" id="m3_topic_title" class="form-control" value="How I Automated 15 Weekly Content Assets in 4 Hours Using Claude + n8n" oninput="recalcModule3()" />
          </div>
          <div class="grid-2" style="margin-bottom:8px;">
            <div class="form-group">
              <label>Competitor Video 14-Day Views</label>
              <input type="number" min="100" step="500" id="m3_comp_views" class="form-control" value="64000" oninput="recalcModule3()" />
            </div>
            <div class="form-group">
              <label>Competitor Channel 90d Median Views</label>
              <input type="number" min="100" step="500" id="m3_comp_median" class="form-control" value="14500" oninput="recalcModule3()" />
            </div>
          </div>
          <div style="padding:12px; background:var(--bg-alt); border-radius:6px; border:1px solid var(--border);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong>Outlier Multiplier (M_outlier): <span id="m3_outlier_val" style="font-family:var(--font-mono); color:var(--accent);">4.41x</span></strong>
              <span id="m3_outlier_gate" class="status-pill status-green">GREEN LIGHT (&gt;= 2.5x)</span>
            </div>
            <p id="m3_outlier_desc" style="font-size:12px; color:var(--muted); margin-top:6px;"></p>
          </div>
        </div>

        <!-- Part B: Package-First & C.L.I.P. Hook Stress-Tester -->
        <div class="card">
          <div class="card-title">
            <span>Part B: Package-First &amp; C.L.I.P. Hook Stress-Tester</span>
            <span id="m3_eri_badge" class="status-pill status-green">ERI Score: 3.12 (High Velocity)</span>
          </div>
          <div class="form-group">
            <label>Title Angle 1 (Curiosity / Contrarian Gap) <span id="m3_t1_len">54 chars</span></label>
            <input type="text" id="m3_title1" class="form-control" value="Stop Posting Daily: The 4-Hour Solopreneur Content OS" oninput="recalcModule3()" />
          </div>
          <div class="form-group">
            <label>3-Word Thumbnail Text Overlay (Strict Max 4 Words) <span id="m3_thumb_words">3 words (PASS)</span></label>
            <input type="text" id="m3_thumb_text" class="form-control" value="4 HRS -> 15 ASSETS" oninput="recalcModule3()" />
          </div>
          <div class="grid-2" style="margin-bottom:8px;">
            <div class="form-group">
              <label>C — Pattern Interrupt (0–5s)</label>
              <input type="text" id="m3_clip_c" class="form-control" value="Show live calendar with 4h blocked vs $18k Stripe" />
            </div>
            <div class="form-group">
              <label>L — Quantified Stakes (5–12s)</label>
              <input type="text" id="m3_clip_l" class="form-control" value="Posting daily on 5 apps burns 32 hrs/wk for $14/hr" />
            </div>
            <div class="form-group">
              <label>I — Credibility Proof (12–20s)</label>
              <input type="text" id="m3_clip_i" class="form-control" value="Inside the 1-to-15 Waterfall used by 300+ operators" />
            </div>
            <div class="form-group">
              <label>P — Open-Loop Payoff (20–30s)</label>
              <input type="text" id="m3_clip_p" class="form-control" value="Plus the exact 12-point QA checklist at minute 8" />
            </div>
          </div>
          <div class="grid-3" style="margin-bottom:0;">
            <div class="form-group">
              <label>Target CTR (%)</label>
              <input type="number" step="0.5" min="1" max="25" id="m3_ctr" class="form-control" value="7.8" oninput="recalcModule3()" />
            </div>
            <div class="form-group">
              <label>30s Hold Rate (%)</label>
              <input type="number" step="1" min="20" max="95" id="m3_hold30" class="form-control" value="74" oninput="recalcModule3()" />
            </div>
            <div class="form-group">
              <label>Full Video APV (%)</label>
              <input type="number" step="1" min="15" max="90" id="m3_apv" class="form-control" value="54" oninput="recalcModule3()" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- MODULE 4: 1-TO-15 REPURPOSING MATRIX & 4-HOUR BATCH SPRINT TRACKER  -->
    <!-- =================================================================== -->
    <section id="mod4" class="module-panel">
      <div class="module-header-banner">
        <div>
          <h2>Module 4: 1-to-15 Omnichannel Repurposing Matrix &amp; 4-Hour Batch Sprint Tracker</h2>
          <p>Transform 1 weekly Pillar Script into 15 platform-native assets and track your 4-Hour Weekly Batch Production Sprint.</p>
        </div>
        <div style="display:flex; gap:8px; align-items:center;">
          <span id="m4_completion_badge" class="status-pill status-green">15 / 15 Assets Tracked</span>
          <button type="button" class="btn btn-teal" onclick="markAllDerivativesStatus('Published')">Mark All Published</button>
          <button type="button" class="btn btn-ghost" onclick="markAllDerivativesStatus('Draft')">Reset Sprint</button>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-title">
            <span>Weekly Anchor Pillar Specification</span>
            <span style="font-size:11px; color:var(--muted);">Chapter 6 Waterfall</span>
          </div>
          <div class="form-group">
            <label>Weekly Pillar Topic &amp; Core Mechanism</label>
            <input type="text" id="m4_pillar_topic" class="form-control" value="The 5-Day Value-First Newsletter Welcome Sequence That Converts at 3.8%" oninput="renderWaterfallTable()" />
          </div>
          <div class="form-group" style="margin-bottom:0;">
            <label>Attached Lead Magnet &amp; UTM Campaign Slug</label>
            <input type="text" id="m4_lead_magnet" class="form-control" value="5-Min Welcome Sequence Wireframe Kit (?utm_campaign=wk_welcome_os)" oninput="renderWaterfallTable()" />
          </div>
        </div>

        <div class="card">
          <div class="card-title">
            <span>4-Hour Weekly Batch Production Sprint Blocks (240 Mins Total)</span>
            <span id="m4_sprint_hours_badge" class="status-pill status-green">4.0 Hours Locked</span>
          </div>
          <div style="display:flex; flex-direction:column; gap:8px; font-size:12.5px;">
            <label><input type="checkbox" checked onchange="updateSprintProgress()" class="sprint-block-chk" /> <strong>Block 1 (Mon · 45 mins):</strong> S.I.G.N.A.L. Outlier Mining + C.L.I.P. Title/Thumbnail Lock</label>
            <label><input type="checkbox" checked onchange="updateSprintProgress()" class="sprint-block-chk" /> <strong>Block 2 (Tue · 75 mins):</strong> H.E.A.R.T. Pillar Script Architecture + Voice DNA Pass</label>
            <label><input type="checkbox" checked onchange="updateSprintProgress()" class="sprint-block-chk" /> <strong>Block 3 (Wed · 90 mins):</strong> A-Roll Batch Recording + AI Text-Based Rough Cut</label>
            <label><input type="checkbox" checked onchange="updateSprintProgress()" class="sprint-block-chk" /> <strong>Block 4 (Thu · 30 mins):</strong> 1-to-15 Derivative Extraction + 12-Point QA Gate</label>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-title">
          <span>The 1-to-15 Derivative Asset Waterfall Board</span>
          <span style="font-size:11.5px; color:var(--muted);">Click any status dropdown to update pipeline stage</span>
        </div>
        <div style="overflow-x:auto;">
          <table class="studio-table">
            <thead>
              <tr>
                <th>Asset Code</th>
                <th>Format Category</th>
                <th>Target Platform</th>
                <th>Derivative Angle &amp; CTA Hook</th>
                <th>Pipeline Status</th>
              </tr>
            </thead>
            <tbody id="m4_waterfall_tbody"></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- MODULE 5: BRAND SPONSORSHIP RATE CARD & USAGE-RIGHTS CALCULATOR     -->
    <!-- =================================================================== -->
    <section id="mod5" class="module-panel">
      <div class="module-header-banner">
        <div>
          <h2>Module 5: Brand Sponsorship Rate Card &amp; Usage-Rights Pricing Calculator (<code>R_sponsor</code>)</h2>
          <p>Price your omnichannel sponsorships using Chapter 10's C.P.M. Plus Outcome Formula and generate a ready-to-send 3-Tier Partner Proposal.</p>
        </div>
        <button type="button" class="btn btn-primary" onclick="copySponsorProposal()">1-Click Copy 3-Tier Proposal</button>
      </div>

      <div class="grid-3">
        <div class="kpi-card">
          <div class="kpi-label">Tier A: Validation Test</div>
          <div class="kpi-value" id="m5_tier_a_val">$2,150</div>
          <div class="kpi-sub">Organic Video + Newsletter</div>
        </div>
        <div class="kpi-card teal">
          <div class="kpi-label">Tier B: Omnichannel Outcome</div>
          <div class="kpi-value" id="m5_tier_b_val">$3,440</div>
          <div class="kpi-sub">Includes 30d Paid Whitelisting</div>
        </div>
        <div class="kpi-card amber">
          <div class="kpi-label">Tier C: 90-Day Exclusive Partner</div>
          <div class="kpi-value" id="m5_tier_c_val">$9,288</div>
          <div class="kpi-sub">3-Sprint Retainer (-10% Bundle)</div>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-title">
            <span>1. Channel, Newsletter &amp; Licensing Inputs</span>
            <span style="font-size:11px; color:var(--muted);">R_sponsor Formula</span>
          </div>
          <div class="grid-2" style="margin-bottom:0;">
            <div class="form-group">
              <label>Sponsor Brand Name</label>
              <input type="text" id="m5_brand_name" class="form-control" value="LinearFlow AI" oninput="recalcModule5()" />
            </div>
            <div class="form-group">
              <label>Avg 30-Day Pillar Views</label>
              <input type="number" step="500" min="500" id="m5_views" class="form-control" value="18000" oninput="recalcModule5()" />
            </div>
            <div class="form-group">
              <label>Niche Authority Video CPM ($45–$120)</label>
              <input type="number" step="5" min="15" id="m5_cpm" class="form-control" value="75" oninput="recalcModule5()" />
            </div>
            <div class="form-group">
              <label>Active Email Subscribers</label>
              <input type="number" step="250" min="100" id="m5_subs" class="form-control" value="8500" oninput="recalcModule5()" />
            </div>
            <div class="form-group">
              <label>Newsletter Open Rate (%)</label>
              <input type="number" step="1" min="10" max="90" id="m5_open_rate" class="form-control" value="52" oninput="recalcModule5()" />
            </div>
            <div class="form-group">
              <label>Sponsor Slot Click Rate (% of Opens)</label>
              <input type="number" step="0.5" min="0.5" max="25" id="m5_ctr" class="form-control" value="4.2" oninput="recalcModule5()" />
            </div>
            <div class="form-group">
              <label>Verified B2B Niche CPC ($3.50–$8)</label>
              <input type="number" step="0.5" min="1" id="m5_cpc" class="form-control" value="5.50" oninput="recalcModule5()" />
            </div>
            <div class="form-group">
              <label>Paid Ad Whitelisting Months (0–12)</label>
              <input type="number" step="1" min="0" max="12" id="m5_usage_mo" class="form-control" value="1" oninput="recalcModule5()" />
            </div>
            <div class="form-group">
              <label>Category Exclusivity Months (0–12)</label>
              <input type="number" step="1" min="0" max="12" id="m5_excl_mo" class="form-control" value="1" oninput="recalcModule5()" />
            </div>
            <div class="form-group">
              <label>Performance Click Bonus ($)</label>
              <input type="number" step="100" min="0" id="m5_perf_bonus" class="form-control" value="500" oninput="recalcModule5()" />
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-title">
            <span>2. Auto-Generated 3-Tier Sponsor Proposal &amp; Rate Card</span>
            <span class="status-pill status-green">50% Deposit · Net-15</span>
          </div>
          <pre class="compiled-prompt-box" id="m5_proposal_output" style="max-height:360px;"></pre>
        </div>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- MODULE 6: 20-MINUTE FRIDAY CEO SCORECARD & 10-CHAPTER OS TRACKER    -->
    <!-- =================================================================== -->
    <section id="mod6" class="module-panel">
      <div class="module-header-banner">
        <div>
          <h2>Module 6: The 20-Minute Friday Creator CEO Scorecard &amp; 10-Chapter OS Progress Tracker</h2>
          <p>Log your weekly executive telemetry, track your 100-Item Master Implementation Checklist across Chapters 1–10, and inspect all 20 Vector System Diagrams offline.</p>
        </div>
        <span id="m6_master_progress_badge" class="status-pill status-green">OS Completion: 20%</span>
      </div>

      <div class="grid-2">
        <!-- Left: Friday Creator CEO Weekly KPI Entry -->
        <div class="card">
          <div class="card-title">
            <span>Friday 20-Minute Creator CEO Weekly Log</span>
            <button type="button" class="btn btn-teal" style="padding:4px 10px; font-size:11.5px;" onclick="addWeeklyKpiRow()">+ Log Week</button>
          </div>
          <div class="grid-3" style="margin-bottom:8px;">
            <div class="form-group">
              <label>Week Ending</label>
              <input type="date" id="m6_wk_date" class="form-control" value="2026-10-23" />
            </div>
            <div class="form-group">
              <label>Hours Worked (&lt;=25h)</label>
              <input type="number" step="0.5" id="m6_wk_hrs" class="form-control" value="19.5" />
            </div>
            <div class="form-group">
              <label>Weekly Revenue ($)</label>
              <input type="number" step="100" id="m6_wk_rev" class="form-control" value="4650" />
            </div>
            <div class="form-group">
              <label>Pillar Outlier (x)</label>
              <input type="number" step="0.1" id="m6_wk_outlier" class="form-control" value="3.2" />
            </div>
            <div class="form-group">
              <label>30s Hold Rate (%)</label>
              <input type="number" step="1" id="m6_wk_hold" class="form-control" value="73" />
            </div>
            <div class="form-group">
              <label>New Email Opt-Ins</label>
              <input type="number" step="10" id="m6_wk_subs" class="form-control" value="420" />
            </div>
          </div>
          <div style="overflow-x:auto; max-height:220px;">
            <table class="studio-table">
              <thead>
                <tr>
                  <th>Week</th>
                  <th>Hours</th>
                  <th>Revenue</th>
                  <th>RPPH</th>
                  <th>Outlier</th>
                  <th>30s Hold</th>
                  <th>Opt-Ins</th>
                </tr>
              </thead>
              <tbody id="m6_kpi_log_tbody"></tbody>
            </table>
          </div>
        </div>

        <!-- Right: 20 Vector Architecture Diagram Explorer -->
        <div class="card">
          <div class="card-title">
            <span>Interactive 20-Diagram Visual Architecture Explorer</span>
            <select id="m6_diagram_selector" class="form-control" style="width:auto; padding:4px 8px; font-size:12px;" onchange="renderSelectedDiagram()"></select>
          </div>
          <div class="svg-preview-box" id="m6_svg_viewer"></div>
        </div>
      </div>

      <!-- 100-Item Master Implementation Checklist -->
      <div class="card">
        <div class="card-title">
          <span>100-Item Master Operating System Installation Checklist (Chapters 1–10)</span>
          <div style="display:flex; gap:8px;">
            <select id="m6_chk_chapter_filter" class="form-control" style="width:auto; padding:4px 8px; font-size:12px;" onchange="renderMasterChecklist()">
              <option value="ALL">Show All 10 Chapters (100 Gates)</option>
              <option value="1">Chapter 01 (10 Gates)</option>
              <option value="2">Chapter 02 (10 Gates)</option>
              <option value="3">Chapter 03 (10 Gates)</option>
              <option value="4">Chapter 04 (10 Gates)</option>
              <option value="5">Chapter 05 (10 Gates)</option>
              <option value="6">Chapter 06 (10 Gates)</option>
              <option value="7">Chapter 07 (10 Gates)</option>
              <option value="8">Chapter 08 (10 Gates)</option>
              <option value="9">Chapter 09 (10 Gates)</option>
              <option value="10">Chapter 10 (10 Gates)</option>
            </select>
            <button type="button" class="btn btn-teal" onclick="setAllChecklistItems(true)">Check All</button>
            <button type="button" class="btn btn-ghost" onclick="setAllChecklistItems(false)">Clear All</button>
          </div>
        </div>
        <div class="bar-track" style="margin-bottom:14px;">
          <div class="bar-fill" id="m6_chk_progress_bar" style="width:20%;"></div>
        </div>
        <div id="m6_checklist_container" style="display:grid; grid-template-columns:1fr 1fr; gap:10px; max-height:460px; overflow-y:auto;"></div>
      </div>
    </section>

  </main>
</div>

<!-- NOTIFICATION TOAST -->
<div id="toastBox" class="toast-notification">Action completed</div>

<!-- EMBEDDED STUDIO DATABASES & APPLICATION CONTROLLER -->
<script>
  const STUDIO_PROMPTS = {prompts_json};
  const STUDIO_SCRIPTS = {scripts_json};
  const STUDIO_CHECKLIST = {checklist_json};
  const STUDIO_DIAGRAMS = {svg_gallery_json};
  const PRO_LICENSE_KEY_CONST = "CREATOR-OS-PRO-2026";
  const STORAGE_KEY = "CREATOR_OS_WORKSPACE_STATE_V1";

  let appState = {{
    proActive: true,
    theme: "light",
    vaultCategory: "prompts",
    selectedVaultId: "P01",
    customVariables: {{}},
    waterfallStatuses: {{}},
    checkedGates: {{
      "CH01-GATE-01": true,
      "CH01-GATE-02": true,
      "CH01-GATE-03": true,
      "CH01-GATE-04": true,
      "CH01-GATE-05": true
    }},
    weeklyKpiLogs: [
      {{ date: "2026-10-02", hours: 24.0, revenue: 3150, outlier: 2.4, hold: 69, subs: 280 }},
      {{ date: "2026-10-09", hours: 21.5, revenue: 3890, outlier: 2.9, hold: 71, subs: 345 }},
      {{ date: "2026-10-16", hours: 19.5, revenue: 4650, outlier: 3.2, hold: 73, subs: 420 }}
    ]
  }};

  const DEFAULT_DERIVATIVES = [
    {{ code: "A01", cat: "Anchor Pillar", platform: "YouTube + Newsletter", angle: "Full 12-Min System Breakdown + Interactive Lead Magnet CTA" }},
    {{ code: "S01", cat: "Vertical Short #1", platform: "YouTube Shorts / Reels / TikTok", angle: "60s Contrarian Myth-Bust Hook + Pinned Comment Trigger" }},
    {{ code: "S02", cat: "Vertical Short #2", platform: "YouTube Shorts / Reels / TikTok", angle: "45s Math & Formula Teardown + Bio Link Callout" }},
    {{ code: "S03", cat: "Vertical Short #3", platform: "YouTube Shorts / Reels / TikTok", angle: "60s Before/After Case Study Proof Clip" }},
    {{ code: "S04", cat: "Vertical Short #4", platform: "YouTube Shorts / Reels / TikTok", angle: "30s Common Mistake Warning + Quick Fix" }},
    {{ code: "S05", cat: "Vertical Short #5", platform: "YouTube Shorts / Reels / TikTok", angle: "45s Live Screen-Share Tool Walkthrough" }},
    {{ code: "T01", cat: "Written Authority #1", platform: "LinkedIn Long-Form Post", angle: "Step-by-Step Operational Framework + Diagram Image" }},
    {{ code: "T02", cat: "Written Authority #2", platform: "X (Twitter) 8-Post Thread", angle: "Quantitative Breakdown Thread + Final Tweet Lead Magnet Plug" }},
    {{ code: "T03", cat: "Written Authority #3", platform: "LinkedIn Contrarian Post", angle: "Why Standard Industry Advice Fails + New Metric" }},
    {{ code: "T04", cat: "Written Authority #4", platform: "X / Substack Note", angle: "Single-Paragraph Punchy Insight + Screenshot Proof" }},
    {{ code: "C01", cat: "Visual Carousel #1", platform: "LinkedIn PDF Carousel (8 Slides)", angle: "System Architecture Mindmap Slide Deck + CTA Slide" }},
    {{ code: "C02", cat: "Visual Carousel #2", platform: "Instagram / LinkedIn Carousel", angle: "Decision Tree Diagnostic Checklist Carousel" }},
    {{ code: "C03", cat: "Visual Carousel #3", platform: "X / LinkedIn Single-Image Cheat Sheet", angle: "High-Resolution Infographics Summary Card" }},
    {{ code: "E01", cat: "Owned List Bridge #1", platform: "Thursday Authority Newsletter Issue", angle: "Deep-Dive Written Essay + Tier 2 Product Soft Bridge" }},
    {{ code: "E02", cat: "Owned List Bridge #2", platform: "Saturday Implementation Tear-Sheet", angle: "3-Minute Tactical Action Check + Direct Offer Link" }}
  ];

  function showToast(msg) {{
    const box = document.getElementById("toastBox");
    box.textContent = msg;
    box.style.display = "block";
    clearTimeout(window._toastTimer);
    window._toastTimer = setTimeout(() => {{
      box.style.display = "none";
    }}, 2600);
  }}

  function saveState() {{
    try {{
      localStorage.setItem(STORAGE_KEY, JSON.stringify(appState));
    }} catch (e) {{}}
  }}

  function loadState() {{
    try {{
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {{
        const parsed = JSON.parse(raw);
        appState = Object.assign({{}}, appState, parsed);
      }}
    }} catch (e) {{}}
  }}

  function switchModule(modId) {{
    document.querySelectorAll(".module-panel").forEach(el => el.classList.remove("active"));
    document.querySelectorAll(".module-tab-btn").forEach(btn => btn.classList.remove("active"));
    const target = document.getElementById(modId);
    if (target) target.classList.add("active");
    const tabBtn = document.querySelector(`.module-tab-btn[data-mod="${{modId}}"]`);
    if (tabBtn) tabBtn.classList.add("active");
  }}

  function toggleTheme() {{
    appState.theme = appState.theme === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", appState.theme);
    saveState();
    showToast(`Switched to ${{appState.theme.toUpperCase()}} studio theme`);
  }}

  function updateAccessUI() {{
    const badge = document.getElementById("accessModeBadge");
    const bar = document.getElementById("proActivationBar");
    if (appState.proActive) {{
      badge.className = "tier-badge pro";
      badge.textContent = "● PRO FULL OS ACTIVE (CREATOR-OS-PRO-2026)";
      bar.style.display = "none";
    }} else {{
      badge.className = "tier-badge free";
      badge.textContent = "◐ TIER 0 FREE DIAGNOSTIC MODE";
      bar.style.display = "flex";
    }}
    renderVaultList();
    renderSelectedVaultItem();
  }}

  function toggleAccessTier() {{
    appState.proActive = !appState.proActive;
    saveState();
    updateAccessUI();
    showToast(appState.proActive ? "Pro Full Operating System Mode Activated" : "Switched to Tier 0 Free Diagnostic Mode");
  }}

  function activateProLicenseKey() {{
    const val = (document.getElementById("licenseKeyInput").value || "").trim().toUpperCase();
    if (val === PRO_LICENSE_KEY_CONST) {{
      appState.proActive = true;
      saveState();
      updateAccessUI();
      showToast("License Key Verified: Pro Full Operating System Mode Active!");
    }} else {{
      showToast("Invalid Key. Enter CREATOR-OS-PRO-2026 to activate Pro Mode.");
    }}
  }}

  function instantDemoProActivate() {{
    document.getElementById("licenseKeyInput").value = PRO_LICENSE_KEY_CONST;
    appState.proActive = true;
    saveState();
    updateAccessUI();
    showToast("Demo Pro Mode Activated (All 50 Prompts & 12 Scripts Enabled)");
  }}

  /* ---------------- MODULE 1 LOGIC ---------------- */
  function recalcModule1() {{
    const hIdea = parseFloat(document.getElementById("m1_h_idea").value) || 0;
    const hScript = parseFloat(document.getElementById("m1_h_script").value) || 0;
    const hRec = parseFloat(document.getElementById("m1_h_rec").value) || 0;
    const hEdit = parseFloat(document.getElementById("m1_h_edit").value) || 0;
    const hRep = parseFloat(document.getElementById("m1_h_rep").value) || 0;
    const hAdm = parseFloat(document.getElementById("m1_h_adm").value) || 0;

    const totalWeeklyHrs = Math.max(1, hIdea + hScript + hRec + hEdit + hRep + hAdm);
    const monthlyHrs = totalWeeklyHrs * 4.0;
    const views = parseFloat(document.getElementById("m1_views").value) || 0;
    const adsenseRpm = parseFloat(document.getElementById("m1_adsense_rpm").value) || 0;
    const currRev = parseFloat(document.getElementById("m1_curr_rev").value) || 0;
    const targetWeeklyHrs = Math.max(1, parseFloat(document.getElementById("m1_target_hrs").value) || 18);

    const optinRate = (parseFloat(document.getElementById("m1_optin_rate").value) || 0) / 100.0;
    const t1Price = parseFloat(document.getElementById("m1_t1_price").value) || 29;
    const t1Cvr = (parseFloat(document.getElementById("m1_t1_cvr").value) || 0) / 100.0;
    const t2Price = parseFloat(document.getElementById("m1_t2_price").value) || 99;
    const t2Cvr = (parseFloat(document.getElementById("m1_t2_cvr").value) || 0) / 100.0;
    const bumpLift = 1.0 + ((parseFloat(document.getElementById("m1_bump_lift").value) || 0) / 100.0);
    const t3Price = parseFloat(document.getElementById("m1_t3_price").value) || 997;
    const sponsorRev = parseFloat(document.getElementById("m1_sponsor_rev").value) || 0;

    const currRpph = currRev / monthlyHrs;
    const newSubs = Math.round(views * optinRate);
    const revAdsense = (views / 1000.0) * adsenseRpm;
    const revTier1 = newSubs * t1Cvr * t1Price * bumpLift;
    const revTier2 = newSubs * t2Cvr * t2Price * bumpLift;
    const revTier3 = Math.max(1, Math.round(newSubs * t2Cvr * 0.15)) * t3Price;
    const totalSysRev = revAdsense + revTier1 + revTier2 + revTier3 + sponsorRev;

    const sysMonthlyHrs = targetWeeklyHrs * 4.0;
    const sysRpph = totalSysRev / sysMonthlyHrs;
    const blendedRpm = views > 0 ? (totalSysRev / (views / 1000.0)) : 0;
    const weeklySaved = Math.max(0, totalWeeklyHrs - targetWeeklyHrs);

    document.getElementById("m1_curr_rpph").textContent = "$" + currRpph.toFixed(2) + "/hr";
    document.getElementById("m1_curr_hours_label").textContent = `${{totalWeeklyHrs.toFixed(1)}} hrs/wk · $${{Math.round(currRev).toLocaleString()}}/mo`;
    document.getElementById("m1_sys_rpph").textContent = "$" + sysRpph.toFixed(2) + "/hr";
    document.getElementById("m1_sys_hours_label").textContent = `${{targetWeeklyHrs.toFixed(1)}} hrs/wk · $${{Math.round(totalSysRev).toLocaleString()}}/mo`;
    document.getElementById("m1_blended_rpm").textContent = "$" + blendedRpm.toFixed(2);
    document.getElementById("m1_hours_saved_label").textContent = `Saves ${{weeklySaved.toFixed(1)}} hrs/wk (${{Math.round(weeklySaved * 52)}} hrs/yr)`;
    document.getElementById("m1_annual_projection_pill").textContent = `Annualized Run-Rate: $${{Math.round(totalSysRev * 12).toLocaleString()}}/yr`;

    // Bottleneck classification
    let bottleneck = "Offer & Ascension";
    let narrative = "";
    if (hEdit + hRep > totalWeeklyHrs * 0.42) {{
      bottleneck = "Post-Production Time-Leak";
      narrative = `<strong>Stage-Gate Diagnosis (Post-Production &amp; Manual Repurposing Bottleneck):</strong> You are spending <strong>${{(hEdit + hRep).toFixed(1)}} hours/week</strong> (${{Math.round(((hEdit + hRep)/totalWeeklyHrs)*100)}}% of your total workweek) on manual editing and cross-posting. Install <strong>Chapter 6 (1-to-15 Waterfall Prompts P26–P30)</strong> and <strong>Chapter 7 (4-Hour Batch Pipeline Prompts P31–P35)</strong> immediately to compress production to ${{(targetWeeklyHrs).toFixed(1)}} hrs/week and lift your RPPH from <strong>$${{currRpph.toFixed(2)}}/hr</strong> to <strong>$${{sysRpph.toFixed(2)}}/hr</strong>.`;
    }} else if (optinRate < 0.015) {{
      bottleneck = "Rented-to-Owned Capture Leak";
      narrative = `<strong>Stage-Gate Diagnosis (Audience Ownership Leak):</strong> Your view-to-email capture rate is below the 1.5% studio floor (${{(optinRate*100).toFixed(2)}}%). Deploy <strong>Chapter 8 (5-Minute Utility Lead Magnet &amp; Single-Field Opt-In Wireframe Prompts P36–P39)</strong> to capture <strong>${{newSubs.toLocaleString()}}+ subscribers/month</strong> and generate <strong>$${{Math.round(revTier1 + revTier2).toLocaleString()}}/month</strong> in automated welcome sequence sales.`;
    }} else {{
      bottleneck = "Value Ladder &amp; Sponsor Yield";
      narrative = `<strong>Stage-Gate Diagnosis (Monetization &amp; Checkout AOV Expansion):</strong> Your production foundation is solid; your highest-return move is installing <strong>Chapter 9's Order Bump + 1-Click Upsell Stack (+${{Math.round((bumpLift-1)*100)}}% cart lift)</strong> alongside <strong>Chapter 10's Friday 5-Pitch Outbound Sponsorship Cadence</strong>, scaling monthly net revenue to <strong>$${{Math.round(totalSysRev).toLocaleString()}}/month</strong>.`;
    }}
    document.getElementById("m1_bottleneck_badge").innerHTML = bottleneck;
    document.getElementById("m1_diagnostic_narrative").innerHTML = narrative;

    const streams = [
      {{ label: "Platform AdSense", val: revAdsense }},
      {{ label: "Tier 1 Impulse + Bumps", val: revTier1 }},
      {{ label: "Tier 2 Flagship OS + Bumps", val: revTier2 }},
      {{ label: "Tier 3/4 Sprint & Advisory", val: revTier3 }},
      {{ label: "Omnichannel Sponsorships", val: sponsorRev }}
    ];
    const barsHtml = streams.map(st => {{
      const pct = totalSysRev > 0 ? Math.round((st.val / totalSysRev) * 100) : 0;
      return `<div style="margin-bottom:6px;">
        <div style="display:flex; justify-content:space-between; font-size:11.5px;">
          <span>${{st.label}}</span>
          <span style="font-family:var(--font-mono); font-weight:700;">$${{Math.round(st.val).toLocaleString()}} (${{pct}}%)</span>
        </div>
        <div class="bar-track" style="height:8px; margin:3px 0;"><div class="bar-fill" style="width:${{pct}}%;"></div></div>
      </div>`;
    }}).join("");
    document.getElementById("m1_revenue_breakdown_bars").innerHTML = barsHtml;
  }}

  /* ---------------- MODULE 2: 50-PROMPT & 12-SCRIPT VAULT ---------------- */
  function setVaultCategory(cat) {{
    appState.vaultCategory = cat;
    document.getElementById("btnVaultModePrompts").className = cat === "prompts" ? "btn btn-primary" : "btn btn-ghost";
    document.getElementById("btnVaultModeScripts").className = cat === "scripts" ? "btn btn-primary" : "btn btn-ghost";
    document.getElementById("chapterFilterWrap").style.display = cat === "prompts" ? "block" : "none";
    appState.selectedVaultId = cat === "prompts" ? "P01" : "S01";
    renderVaultList();
    renderSelectedVaultItem();
  }}

  function renderVaultList() {{
    const q = (document.getElementById("vaultSearchInput").value || "").toLowerCase().trim();
    const chFilter = document.getElementById("vaultChapterFilter").value;
    const container = document.getElementById("vaultListContainer");
    const dataset = appState.vaultCategory === "prompts" ? STUDIO_PROMPTS : STUDIO_SCRIPTS;

    const filtered = dataset.filter(item => {{
      if (appState.vaultCategory === "prompts" && chFilter !== "ALL" && String(item.chapter) !== chFilter) {{
        return false;
      }}
      if (!q) return true;
      return (
        item.id.toLowerCase().includes(q) ||
        item.title.toLowerCase().includes(q) ||
        (item.body || "").toLowerCase().includes(q)
      );
    }});

    container.innerHTML = filtered.map(item => {{
      const isAct = item.id === appState.selectedVaultId ? "active" : "";
      const isFree = item.tier === "FREE";
      const pillCls = isFree ? "free" : "pro";
      const pillTxt = isFree ? "FREE" : (appState.proActive ? "PRO ACTIVE" : "PRO KEY REQ");
      const subText = appState.vaultCategory === "prompts" ? item.chapterLabel : item.scenario;
      return `<div class="vault-item ${{isAct}}" onclick="selectVaultItem('${{item.id}}')">
        <div class="vault-item-header">
          <span class="vault-id-badge">${{item.id}}</span>
          <span class="tier-pill ${{pillCls}}">${{pillTxt}}</span>
        </div>
        <div style="font-weight:700; font-size:12.5px; color:var(--primary);">${{item.title}}</div>
        <div style="font-size:11px; color:var(--muted); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${{subText}}</div>
      </div>`;
    }}).join("");
  }}

  function selectVaultItem(id) {{
    appState.selectedVaultId = id;
    renderVaultList();
    renderSelectedVaultItem();
  }}

  function renderSelectedVaultItem() {{
    const dataset = appState.vaultCategory === "prompts" ? STUDIO_PROMPTS : STUDIO_SCRIPTS;
    const item = dataset.find(x => x.id === appState.selectedVaultId) || dataset[0];
    if (!item) return;

    document.getElementById("selectedVaultHeading").textContent = `${{item.id}}: ${{item.title}}`;
    const badge = document.getElementById("selectedVaultStageBadge");
    badge.className = "tier-pill " + (item.tier === "FREE" ? "free" : "pro");
    badge.textContent = item.tier === "FREE" ? "FREE STARTER ACCESS" : "PRO OPERATING VAULT";

    if (appState.vaultCategory === "prompts") {{
      document.getElementById("selectedVaultMeta").innerHTML = `<strong>${{item.chapterLabel}}</strong> · <strong>Stage:</strong> ${{item.stage}} · <strong>AI Persona:</strong> ${{item.role}}`;
    }} else {{
      document.getElementById("selectedVaultMeta").innerHTML = `<strong>Scenario Trigger:</strong> ${{item.scenario}}<br/><strong>Mechanism:</strong> ${{item.mechanism}} · <strong>Notes:</strong> ${{item.notes}}`;
    }}

    const varContainer = document.getElementById("dynamicVariablesContainer");
    const isRestricted = item.tier === "PRO" && !appState.proActive;

    if (isRestricted) {{
      varContainer.innerHTML = `<div style="padding:8px; color:var(--warning); font-weight:700;">
        This Pro Workflow Asset (${{item.id}}) requires Pro Mode Activation. Enter License Key <code>CREATOR-OS-PRO-2026</code> in the top bar or click "1-Click Demo Pro Mode" to enable live variable compilation.
      </div>`;
      document.getElementById("compiledPromptOutput").textContent =
        `[PRO ACCESS REQUIRED FOR ${{item.id}}: ${{item.title}}]\n\nEnter Pro Access License Key CREATOR-OS-PRO-2026 in the header bar above (or click '1-Click Demo Pro Mode') to activate all 50 AI Workflow Prompts and 12 Emergency Scripts.`;
      return;
    }}

    const vars = item.variables || [];
    if (vars.length === 0) {{
      varContainer.innerHTML = `<div style="font-size:12px; color:var(--muted);">No bracketed input variables required — ready to copy directly.</div>`;
    }} else {{
      const inputsHtml = vars.map(vName => {{
        const key = `${{item.id}}__${{vName}}`;
        const savedVal = appState.customVariables[key] || "";
        const safeKey = key.replace(/'/g, "\\'");
        return `<div class="form-group" style="margin-bottom:6px;">
          <label style="font-family:var(--font-mono); font-size:11px; color:var(--accent);">[${{vName}}]</label>
          <input type="text" class="form-control" style="padding:5px 8px; font-size:12px;" placeholder="Enter custom value for [${{vName}}]..." value="${{savedVal.replace(/"/g, '&quot;')}}" oninput="updatePromptVariable('${{safeKey}}', this.value)" />
        </div>`;
      }}).join("");
      varContainer.innerHTML = `<div style="font-size:11.5px; font-weight:700; margin-bottom:8px; color:var(--primary);">Dynamic Variable Form Builder (Type below to inject into compiled output in real time):</div><div class="grid-2" style="margin-bottom:0; gap:10px;">${{inputsHtml}}</div>`;
    }}

    updateCompiledTextDisplay(item);
  }}

  function updatePromptVariable(key, val) {{
    appState.customVariables[key] = val;
    const dataset = appState.vaultCategory === "prompts" ? STUDIO_PROMPTS : STUDIO_SCRIPTS;
    const item = dataset.find(x => x.id === appState.selectedVaultId) || dataset[0];
    if (item) updateCompiledTextDisplay(item);
  }}

  function updateCompiledTextDisplay(item) {{
    let compiled = item.body;
    (item.variables || []).forEach(vName => {{
      const key = `${{item.id}}__${{vName}}`;
      const userVal = (appState.customVariables[key] || "").trim();
      if (userVal) {{
        compiled = compiled.split(`[${{vName}}]`).join(userVal);
      }}
    }});
    document.getElementById("compiledPromptOutput").textContent = compiled;
  }}

  function resetCurrentPromptVariables() {{
    const dataset = appState.vaultCategory === "prompts" ? STUDIO_PROMPTS : STUDIO_SCRIPTS;
    const item = dataset.find(x => x.id === appState.selectedVaultId);
    if (!item) return;
    (item.variables || []).forEach(vName => {{
      delete appState.customVariables[`${{item.id}}__${{vName}}`];
    }});
    saveState();
    renderSelectedVaultItem();
    showToast(`Reset variables for ${{item.id}}`);
  }}

  function savePromptPresetToStorage() {{
    saveState();
    showToast(`Saved custom variable preset for ${{appState.selectedVaultId}} to local storage`);
  }}

  function copyCompiledVaultOutput() {{
    const text = document.getElementById("compiledPromptOutput").textContent;
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(text);
    }}
    showToast(`Copied compiled ${{appState.selectedVaultId}} to clipboard!`);
  }}

  /* ---------------- MODULE 3: S.I.G.N.A.L. & C.L.I.P. STUDIO ---------------- */
  function recalcModule3() {{
    const pain = parseFloat(document.getElementById("m3_pain").value) || 5;
    const power = parseFloat(document.getElementById("m3_power").value) || 5;
    const margin = parseFloat(document.getElementById("m3_margin").value) || 5;
    const sat = parseFloat(document.getElementById("m3_sat").value) || 5;

    // NMPI normalized out of 100
    const rawNmpi = ((pain * 3.0) + (power * 3.5) + (margin * 2.5) + ((11 - sat) * 1.0));
    const nmpiBadge = document.getElementById("m3_nmpi_badge");
    if (rawNmpi >= 70) {{
      nmpiBadge.className = "status-pill status-green";
      nmpiBadge.textContent = `NMPI: ${{rawNmpi.toFixed(1)}} / 100 (HIGH-MARGIN GO)`;
    }} else if (rawNmpi >= 55) {{
      nmpiBadge.className = "status-pill status-amber";
      nmpiBadge.textContent = `NMPI: ${{rawNmpi.toFixed(1)}} / 100 (REPOSITION)`;
    }} else {{
      nmpiBadge.className = "status-pill status-red";
      nmpiBadge.textContent = `NMPI: ${{rawNmpi.toFixed(1)}} / 100 (NO-GO)`;
    }}

    const compViews = parseFloat(document.getElementById("m3_comp_views").value) || 1000;
    const compMed = Math.max(1, parseFloat(document.getElementById("m3_comp_median").value) || 1000);
    const outlier = compViews / compMed;
    document.getElementById("m3_outlier_val").textContent = outlier.toFixed(2) + "x";
    const oGate = document.getElementById("m3_outlier_gate");
    const oDesc = document.getElementById("m3_outlier_desc");
    if (outlier >= 2.5) {{
      oGate.className = "status-pill status-green";
      oGate.textContent = "GREEN LIGHT (>= 2.5x)";
      oDesc.textContent = "Validated market demand outlier! Proceed immediately to C.L.I.P. Packaging & H.E.A.R.T. Scripting.";
    }} else if (outlier >= 1.5) {{
      oGate.className = "status-pill status-amber";
      oGate.textContent = "AMBER CAUTION (1.5x–2.4x)";
      oDesc.textContent = "Moderate traction. Sharpen the contrarian stake or combine with a higher-outlier angle before filming.";
    }} else {{
      oGate.className = "status-pill status-red";
      oGate.textContent = "REJECT (< 1.5x MEDIAN)";
      oDesc.textContent = "Fails S.I.G.N.A.L. Outlier Gate. Do not invest 4 hours producing this topic.";
    }}

    const t1 = document.getElementById("m3_title1").value || "";
    document.getElementById("m3_t1_len").textContent = `${{t1.length}} chars ${{t1.length <= 60 ? '(Optimal)' : '(Trim <=60)'}}`;

    const thumbTxt = (document.getElementById("m3_thumb_text").value || "").trim();
    const wCount = thumbTxt ? thumbTxt.split(/\\s+/).length : 0;
    document.getElementById("m3_thumb_words").textContent = `${{wCount}} words ${{wCount <= 4 ? '(PASS)' : '(MAX 4 WORDS!)'}}`;

    const ctr = parseFloat(document.getElementById("m3_ctr").value) || 0;
    const hold30 = (parseFloat(document.getElementById("m3_hold30").value) || 0) / 100.0;
    const apv = (parseFloat(document.getElementById("m3_apv").value) || 0) / 100.0;
    const eri = ctr * hold30 * apv;
    const eriBadge = document.getElementById("m3_eri_badge");
    if (eri >= 2.3) {{
      eriBadge.className = "status-pill status-green";
      eriBadge.textContent = `ERI Score: ${{eri.toFixed(2)}} (Algorithmic Expansion)`;
    }} else {{
      eriBadge.className = "status-pill status-amber";
      eriBadge.textContent = `ERI Score: ${{eri.toFixed(2)}} (Target >= 2.30)`;
    }}
  }}

  /* ---------------- MODULE 4: 1-TO-15 WATERFALL & SPRINT ---------------- */
  function renderWaterfallTable() {{
    const tbody = document.getElementById("m4_waterfall_tbody");
    let completedCount = 0;
    tbody.innerHTML = DEFAULT_DERIVATIVES.map(d => {{
      const st = appState.waterfallStatuses[d.code] || "Scheduled";
      if (st === "Scheduled" || st === "Published") completedCount++;
      const badgeCls = st === "Published" ? "status-green" : (st === "Scheduled" ? "status-amber" : "status-red");
      return `<tr>
        <td><code style="font-weight:700;">${{d.code}}</code></td>
        <td><strong>${{d.cat}}</strong></td>
        <td>${{d.platform}}</td>
        <td>${{d.angle}}</td>
        <td>
          <select class="form-control" style="padding:4px 8px; font-size:12px; width:130px;" onchange="setDerivativeStatus('${{d.code}}', this.value)">
            <option value="Draft" ${{st==='Draft'?'selected':''}}>Draft</option>
            <option value="Ready" ${{st==='Ready'?'selected':''}}>Ready</option>
            <option value="Scheduled" ${{st==='Scheduled'?'selected':''}}>Scheduled</option>
            <option value="Published" ${{st==='Published'?'selected':''}}>Published</option>
          </select>
        </td>
      </tr>`;
    }}).join("");
    document.getElementById("m4_completion_badge").textContent = `${{completedCount}} / 15 Scheduled or Live`;
  }}

  function setDerivativeStatus(code, status) {{
    appState.waterfallStatuses[code] = status;
    saveState();
    renderWaterfallTable();
  }}

  function markAllDerivativesStatus(status) {{
    DEFAULT_DERIVATIVES.forEach(d => {{
      appState.waterfallStatuses[d.code] = status;
    }});
    saveState();
    renderWaterfallTable();
    showToast(`All 15 derivative assets marked as ${{status}}`);
  }}

  function updateSprintProgress() {{
    const chks = document.querySelectorAll(".sprint-block-chk");
    let done = 0;
    chks.forEach(c => {{ if (c.checked) done++; }});
    document.getElementById("m4_sprint_hours_badge").textContent = `${{done}} / 4 Sprint Blocks Complete`;
  }}

  /* ---------------- MODULE 5: SPONSORSHIP RATE CALCULATOR ---------------- */
  function recalcModule5() {{
    const brand = document.getElementById("m5_brand_name").value || "Partner Brand";
    const views = parseFloat(document.getElementById("m5_views").value) || 0;
    const cpm = parseFloat(document.getElementById("m5_cpm").value) || 65;
    const subs = parseFloat(document.getElementById("m5_subs").value) || 0;
    const openRate = (parseFloat(document.getElementById("m5_open_rate").value) || 0) / 100.0;
    const ctr = (parseFloat(document.getElementById("m5_ctr").value) || 0) / 100.0;
    const cpc = parseFloat(document.getElementById("m5_cpc").value) || 5.0;
    const usageMo = parseFloat(document.getElementById("m5_usage_mo").value) || 0;
    const exclMo = parseFloat(document.getElementById("m5_excl_mo").value) || 0;
    const perfBonus = parseFloat(document.getElementById("m5_perf_bonus").value) || 0;

    const videoBase = (views / 1000.0) * cpm;
    const verifiedClicks = Math.round(subs * openRate * ctr);
    const emailBase = verifiedClicks * cpc;
    const organicBundleBase = Math.round(videoBase + emailBase);

    const usageMultiplier = 1.0 + (0.30 * usageMo);
    const exclMultiplier = 1.0 + (0.20 * exclMo);

    const tierA = organicBundleBase;
    const tierB = Math.round((organicBundleBase * usageMultiplier * exclMultiplier) + perfBonus);
    const tierC = Math.round((tierB * 3) * 0.90);

    document.getElementById("m5_tier_a_val").textContent = "$" + tierA.toLocaleString();
    document.getElementById("m5_tier_b_val").textContent = "$" + tierB.toLocaleString();
    document.getElementById("m5_tier_c_val").textContent = "$" + tierC.toLocaleString();

    const proposal = `SUBJECT: ${{brand}} x Creator OS Omnichannel Partnership Options

Hi [${{brand}} Partnerships Team],

Based on our trailing 90-day channel telemetry (${{views.toLocaleString()}} avg long-form views + ${{subs.toLocaleString()}} active newsletter subscribers at ${{(openRate*100).toFixed(0)}}% open rate), here are three structured ways we can integrate ${{brand}} into an upcoming implementation tutorial:

1. TIER A — SINGLE VALIDATION SPRINT ($${{tierA.toLocaleString()}})
   - 60–90s Live Screen-Share Mid-Roll Demo inside Pillar Video
   - Featured Primary Sponsor Box in Thursday Authority Newsletter (~${{verifiedClicks}} verified high-intent clicks)
   - Pinned Comment + Description Above-the-Fold UTM Redirect Link
   - Licensing: Organic channel hosting included (0 paid ad whitelisting)

2. TIER B — OMNICHANNEL OUTCOME BUNDLE ($${{tierB.toLocaleString()}}) [RECOMMENDED]
   - Everything in Tier A PLUS:
   - 2x Native Vertical Short-Form Clips (YouTube Shorts + LinkedIn/Reels)
   - 1x Dedicated LinkedIn Workflow Post featuring ${{brand}}
   - Commercial Licensing: ${{usageMo}} Month(s) Paid Ad Whitelisting (+${{Math.round((usageMultiplier-1)*100)}}%) & ${{exclMo}} Month(s) Category Exclusivity (+${{Math.round((exclMultiplier-1)*100)}}%)
   - Outcome Guarantee: Includes $${{perfBonus}} performance bonus cap above ${{verifiedClicks}} verified UTM clicks

3. TIER C — QUARTERLY CATEGORY-EXCLUSIVE PARTNER ($${{tierC.toLocaleString()}} total · 10% Retainer Savings)
   - 3 Consecutive Monthly Omnichannel Outcome Sprints (3 Pillar Demos + 3 Newsletters + 6 Shorts)
   - 90-Day Paid Ad Usage Rights + Full 90-Day Direct Competitor Exclusivity

PAYMENT & PRODUCTION TERMS:
- 50% deposit upon agreement signature; 50% Net-15 upon publication.
- Includes 1 factual accuracy script review pass prior to filming.

Which tier best aligns with ${{brand}}'s Q3/Q4 customer acquisition targets?`;

    document.getElementById("m5_proposal_output").textContent = proposal;
  }}

  function copySponsorProposal() {{
    const txt = document.getElementById("m5_proposal_output").textContent;
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(txt);
    }}
    showToast("Copied 3-Tier Sponsor Proposal to clipboard!");
  }}

  /* ---------------- MODULE 6: FRIDAY CEO SCORECARD & 100-GATE TRACKER ---------------- */
  function renderKpiLogs() {{
    const tbody = document.getElementById("m6_kpi_log_tbody");
    tbody.innerHTML = appState.weeklyKpiLogs.map(row => {{
      const rpph = row.hours > 0 ? (row.revenue / row.hours) : 0;
      return `<tr>
        <td><code>${{row.date}}</code></td>
        <td>${{row.hours.toFixed(1)}}h</td>
        <td><strong>$${{row.revenue.toLocaleString()}}</strong></td>
        <td style="color:var(--secondary); font-weight:700;">$${{rpph.toFixed(2)}}/hr</td>
        <td>${{row.outlier.toFixed(1)}}x</td>
        <td>${{row.hold}}%</td>
        <td>+${{row.subs}}</td>
      </tr>`;
    }}).join("");
  }}

  function addWeeklyKpiRow() {{
    const d = document.getElementById("m6_wk_date").value || "2026-10-23";
    const hrs = parseFloat(document.getElementById("m6_wk_hrs").value) || 20;
    const rev = parseFloat(document.getElementById("m6_wk_rev").value) || 4000;
    const out = parseFloat(document.getElementById("m6_wk_outlier").value) || 2.5;
    const hold = parseFloat(document.getElementById("m6_wk_hold").value) || 70;
    const subs = parseInt(document.getElementById("m6_wk_subs").value, 10) || 300;
    appState.weeklyKpiLogs.unshift({{ date: d, hours: hrs, revenue: rev, outlier: out, hold: hold, subs: subs }});
    saveState();
    renderKpiLogs();
    showToast(`Logged Friday CEO Scorecard for week ending ${{d}}`);
  }}

  function initDiagramSelector() {{
    const sel = document.getElementById("m6_diagram_selector");
    sel.innerHTML = STUDIO_DIAGRAMS.map(d =>
      `<option value="${{d.id}}">Ch ${{String(d.chapter).padStart(2,'0')}} — ${{d.type}}</option>`
    ).join("");
    renderSelectedDiagram();
  }}

  function renderSelectedDiagram() {{
    const selId = document.getElementById("m6_diagram_selector").value;
    const item = STUDIO_DIAGRAMS.find(d => d.id === selId) || STUDIO_DIAGRAMS[0];
    if (item) {{
      document.getElementById("m6_svg_viewer").innerHTML = item.svg;
    }}
  }}

  function renderMasterChecklist() {{
    const chFilter = document.getElementById("m6_chk_chapter_filter").value;
    const container = document.getElementById("m6_checklist_container");
    const totalCount = STUDIO_CHECKLIST.length;
    let checkedTotal = 0;
    STUDIO_CHECKLIST.forEach(item => {{
      if (appState.checkedGates[item.id]) checkedTotal++;
    }});
    const pct = totalCount > 0 ? Math.round((checkedTotal / totalCount) * 100) : 0;
    document.getElementById("m6_master_progress_badge").textContent = `OS Completion: ${{pct}}% (${{checkedTotal}}/${{totalCount}} Gates)`;
    document.getElementById("m6_chk_progress_bar").style.width = `${{pct}}%`;

    const visibleItems = STUDIO_CHECKLIST.filter(item => chFilter === "ALL" || String(item.chapter) === chFilter);
    container.innerHTML = visibleItems.map(item => {{
      const isChk = !!appState.checkedGates[item.id];
      return `<label style="display:flex; align-items:flex-start; gap:8px; padding:8px 10px; border:1px solid var(--border); border-radius:6px; background:var(--bg-alt); cursor:pointer; font-size:12px;">
        <input type="checkbox" ${{isChk ? 'checked' : ''}} onchange="toggleChecklistGate('${{item.id}}', this.checked)" style="margin-top:3px;" />
        <span>
          <strong style="color:var(--primary);">[${{item.id}}] ${{item.title}}:</strong>
          <span style="color:var(--muted);"> ${{item.detail}}</span>
        </span>
      </label>`;
    }}).join("");
  }}

  function toggleChecklistGate(id, checked) {{
    appState.checkedGates[id] = checked;
    saveState();
    renderMasterChecklist();
  }}

  function setAllChecklistItems(checked) {{
    STUDIO_CHECKLIST.forEach(item => {{
      appState.checkedGates[item.id] = checked;
    }});
    saveState();
    renderMasterChecklist();
    showToast(checked ? "All 100 OS Implementation Gates marked complete" : "Cleared checklist progress");
  }}

  /* ---------------- DATA PORTABILITY (JSON / CSV / RESET) ---------------- */
  function exportWorkspaceJSON() {{
    const blob = new Blob([JSON.stringify(appState, null, 2)], {{ type: "application/json" }});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "creator-os-workspace-backup.json";
    a.click();
    URL.revokeObjectURL(url);
    showToast("Exported workspace state to creator-os-workspace-backup.json");
  }}

  function importWorkspaceJSON(ev) {{
    const file = ev.target.files && ev.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {{
      try {{
        const data = JSON.parse(e.target.result);
        appState = Object.assign({{}}, appState, data);
        saveState();
        initAllModules();
        showToast("Imported workspace JSON backup successfully!");
      }} catch (err) {{
        showToast("Invalid JSON backup file.");
      }}
    }};
    reader.readAsText(file);
  }}

  function exportScorecardCSV() {{
    const rows = [["Week_Ending", "Hours_Worked", "Weekly_Revenue_USD", "RPPH_USD", "Outlier_Multiplier", "Hold_30s_Pct", "New_Email_OptIns"]];
    appState.weeklyKpiLogs.forEach(r => {{
      const rpph = r.hours > 0 ? (r.revenue / r.hours).toFixed(2) : "0.00";
      rows.push([r.date, r.hours, r.revenue, rpph, r.outlier, r.hold, r.subs]);
    }});
    const csvContent = rows.map(r => r.join(",")).join("\\n");
    const blob = new Blob([csvContent], {{ type: "text/csv;charset=utf-8;" }});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "creator-ceo-friday-scorecard.csv";
    a.click();
    URL.revokeObjectURL(url);
    showToast("Exported Friday Creator CEO Scorecard to CSV!");
  }}

  function resetAllWorkspaceData() {{
    localStorage.removeItem(STORAGE_KEY);
    location.reload();
  }}

  function initAllModules() {{
    loadState();
    document.documentElement.setAttribute("data-theme", appState.theme || "light");
    DEFAULT_DERIVATIVES.forEach(d => {{
      if (!appState.waterfallStatuses[d.code]) {{
        appState.waterfallStatuses[d.code] = "Scheduled";
      }}
    }});
    updateAccessUI();
    recalcModule1();
    renderVaultList();
    renderSelectedVaultItem();
    recalcModule3();
    renderWaterfallTable();
    recalcModule5();
    renderKpiLogs();
    initDiagramSelector();
    renderMasterChecklist();
  }}

  window.addEventListener("DOMContentLoaded", initAllModules);
</script>
</body>
</html>"""
    return html_app


# ---------------------------------------------------------------------------
# 3. BUILD PRO-ACCESS-LICENSE-KEY.txt & README-WEB-APP.md
# ---------------------------------------------------------------------------

def build_license_key_txt() -> str:
    return """================================================================================
THE AI CONTENT CREATOR & SOLOPRENEUR OPERATING SYSTEM
COMPANION INTERACTIVE SUITE — PRO ACCESS LICENSE KEY & ACTIVATION CERTIFICATE
================================================================================

Product ID:          PRODUCT-03-AI-CREATOR-SOLOPRENEUR-OS
Edition Coverage:    Tier 2 (Creator Operator Pro Bundle)
                     Tier 3 (Executive Solopreneur Automation Suite)
                     Tier 4 (Agency & Creator Incubator White-Label License)
Application File:    07-INTERACTIVE-TOOLS/creator-os-app.html
Architecture:        100% Offline Self-Contained Single-File HTML5 Application

--------------------------------------------------------------------------------
YOUR MASTER PRO ACCESS LICENSE KEY:
--------------------------------------------------------------------------------

    CREATOR-OS-PRO-2026

--------------------------------------------------------------------------------
HOW TO ACTIVATE PRO FULL OPERATING SYSTEM MODE (30 SECONDS):
--------------------------------------------------------------------------------

1. Double-click `07-INTERACTIVE-TOOLS/creator-os-app.html` to open the web
   application in any modern desktop or tablet browser (Google Chrome,
   Microsoft Edge, Apple Safari, Brave, or Mozilla Firefox). No internet
   connection or local server is required.

2. If the application is currently in Tier 0 Free Diagnostic Mode, locate the
   Commercial Access Control bar at the top of the screen, enter:

       CREATOR-OS-PRO-2026

   and click "Activate Pro Access" (or click "1-Click Demo Pro Mode").

3. Your Pro activation status is saved automatically in your browser's local
   storage (`localStorage`) so all 50 Tested AI Prompts (`P01` through `P50`),
   all 12 Emergency Creator & Sponsorship Scripts (`S01` through `S12`), and
   all 6 interactive calculators remain active every time you launch the file.

--------------------------------------------------------------------------------
OFFLINE PRIVACY & JSON BACKUP GUIDELINES:
--------------------------------------------------------------------------------

* Zero External Servers: Your financial inputs, custom prompt variables,
  1-to-15 repurposing status boards, and Friday Creator CEO KPI logs never
  leave your device.
* Portable JSON Backups: Click the "Export JSON" button in the top navigation
  bar at the end of your Friday 20-Minute Creator CEO Review to save a
  timestamped `.json` snapshot to your local drive or cloud folder.
================================================================================
"""


def build_readme_web_app_md() -> str:
    return r"""# The AI Content Creator & Solopreneur Operating System — Interactive Offline Web Companion Suite (`creator-os-app.html`)

> **Operational Documentation & User Manual (v1.0.0)**
> * **Application Path:** `07-INTERACTIVE-TOOLS/creator-os-app.html`
> * **License Certificate Path:** `07-INTERACTIVE-TOOLS/PRO-ACCESS-LICENSE-KEY.txt`
> * **Master Pro Access License Key:** `CREATOR-OS-PRO-2026`
> * **Architecture:** 100% Offline Single-File HTML5 / CSS3 / Vanilla JavaScript Application (Zero External CDN Dependencies)

---

## 1. Architectural Overview & Zero-Dependency Privacy Model

The **Creator OS Interactive Web Companion Suite (`creator-os-app.html`)** is a standalone, single-file software application engineered to turn the mathematical frameworks, stage-gate decision trees, 50 AI workflow prompts, and 12 emergency scripts from *The AI Content Creator & Solopreneur Operating System* into an interactive daily command center.

Unlike cloud SaaS subscriptions that charge `$49 to $199/month`, require constant internet connectivity, and store your proprietary revenue metrics on third-party servers, `creator-os-app.html` operates on a **100% Offline Local-First Architecture**:

1. **Zero External Network Calls:** Every stylesheet rule, SVG vector diagram, interactive calculator formula, and JSON database entry (`P01`–`P50` and `S01`–`S12`) is compiled directly inside a single `.html` binary (`480,000+ bytes`). It runs identically on a flight at 35,000 feet or on an air-gapped studio workstation.
2. **Instant Browser Execution:** Double-click `creator-os-app.html` in Windows File Explorer, macOS Finder, or your tablet file manager to open it directly inside Microsoft Edge, Google Chrome, Apple Safari, Brave, or Mozilla Firefox via the `file://` protocol.
3. **Persistent Local Storage (`localStorage`) + Full JSON/CSV Portability:** Every change you make to your variable presets, 1-to-15 repurposing board, or 100-item implementation checklist is automatically saved in your browser's local storage and can be exported to `.json` or `.csv` files in a single click.

---

## 2. Commercial Tier Access Control (Free Diagnostic Mode vs. Pro Full OS Mode)

Because `creator-os-app.html` is distributed across both the **Tier 0 Free Starter Kit** and the **Tier 2 / Tier 3 / Tier 4 Commercial Editions**, the application includes a built-in **Commercial Access Control Gate**:

| Feature / Module | Tier 0 Free Diagnostic Mode | Pro Full Operating System Mode (`CREATOR-OS-PRO-2026`) |
| :--- | :---: | :---: |
| **Module 1: RPPH, RPM & 4-Tier Value-Ladder Simulator** | Full Access | Full Access |
| **Module 2: Chapter 1 AI Prompts (`P01`–`P05`)** | Full Access | Full Access |
| **Module 2: Chapters 2–10 AI Prompts (`P06`–`P50`)** | Preview Metadata Only | **Full Interactive Variable Compiler Active** |
| **Module 2: Emergency Scripts (`S01`–`S02` vs. `S03`–`S12`)** | `S01`–`S02` Active | **All 12 Scripts (`S01`–`S12`) Active** |
| **Module 3: S.I.G.N.A.L. Outlier & C.L.I.P. Packaging Studio** | Full Access | Full Access |
| **Module 4: 1-to-15 Repurposing Matrix & 4-Hr Batch Sprint** | Full Access | Full Access |
| **Module 5: Brand Sponsorship Rate Card Calculator ($R_{\text{sponsor}}$)** | Full Access | Full Access |
| **Module 6: Friday Creator CEO Scorecard & 100-Gate OS Tracker** | Full Access | Full Access |

### How to Activate Pro Full Operating System Mode

1. Locate the **Commercial Access Control** bar at the top of the workspace (or click the **Switch Free / Pro Mode** button in the top header to test the gate).
2. Enter the Master Pro Access License Key:
   ```text
   CREATOR-OS-PRO-2026
   ```
3. Click **Activate Pro Access** (or click **1-Click Demo Pro Mode**). The status indicator in the header will switch to `PRO FULL OS ACTIVE (CREATOR-OS-PRO-2026)`, enabling all 50 AI Workflow Prompts and all 12 Emergency Communication Scripts.

---

## 3. Module-by-Module Operational Walkthrough

### 3.1 Module 1: Creator RPPH, RPM & 4-Tier Value-Ladder Simulator (Chapters 1 & 9)

Module 1 implements the **Revenue Per Production Hour ($\text{RPPH}$)** and **4-Tier Digital Product Value Ladder** equations from Chapters 1, 8, and 9:

$$\text{RPPH} = \frac{\text{Total Monthly Creator Revenue}}{\text{Total Monthly Production Hours}}$$

* **Left Panel (Weekly Production Hours & Traffic Inputs):** Enter your current weekly hours across *Ideation & Research*, *Pillar Scripting*, *Recording & Takes*, *Editing & Revisions*, *Manual Repurposing*, and *Admin & Inbound DMs*, alongside your monthly views, platform AdSense RPM, and current monthly revenue.
* **Right Panel (Owned Funnel & 4-Tier Value Ladder Inputs):** Configure your view-to-email capture rate (`%`), Tier 1 Impulse Price (`$29`), Tier 2 Flagship System Price (`$99`), Checkout Order Bump + Upsell Cart Lift (`%`), Tier 3/4 High-Ticket Price (`$997`), and Monthly Sponsorship Retainers (`$`).
* **Automated Bottleneck Diagnosis:** The simulator compares your baseline RPPH against your systematized target RPPH, renders a real-time horizontal revenue mix chart across all 5 income streams, and automatically diagnoses whether your #1 operational bottleneck is a **Post-Production Time-Leak**, a **Rented-to-Owned Capture Leak**, or a **Value Ladder & Sponsor Yield Gap**.

### 3.2 Module 2: Interactive 50-Prompt & 12-Script Command Vault (`P01`–`P50` & `S01`–`S12`)

Module 2 embeds the complete verbatim corpus of **50 Tested AI Workflow Prompts (`P01`–`P50`)** across all 10 chapters and **12 Emergency Creator & Sponsorship Communication Scripts (`S01`–`S12`)** from the Back Matter Vault:

* **Instant Search & Chapter Filtering:** Filter prompts by Chapter (`Ch 01` through `Ch 10`) or search across IDs, titles, AI roles, and scenario triggers.
* **Dynamic `[BRACKETED_VARIABLE]` Form Builder:** When you select any prompt or script, the application parses every `[VARIABLE_TOKEN]` inside the template and generates dedicated input fields above the prompt box.
* **Real-Time Prompt Compilation:** As you type your niche, ICP, outlier metrics, or product price into the variable fields, the compiled prompt updates character-by-character in real time. Click **1-Click Copy Compiled Text** to paste directly into Claude, ChatGPT, or Gemini, or click **Save Variable Preset** to persist your custom inputs in `localStorage`.

### 3.3 Module 3: S.I.G.N.A.L. Outlier Topic Validator & C.L.I.P. Packaging Studio (Chapters 2, 3 & 4)

Module 3 enforces the **Package-First Rule**: never write a single line of a Pillar Script until your niche, topic outlier multiplier, title, thumbnail overlay, and 30-second hook pass quantitative thresholds:

* **Part A — P.A.I.D. Niche & S.I.G.N.A.L. Outlier Scorer:** Computes your **Niche Monetization Potential Index (NMPI)** on a 100-point scale (`>= 70` Green Go Gate) and calculates your candidate topic's **Outlier Multiplier ($M_{\text{outlier}} = \text{Competitor 14-Day Views} \div \text{Channel 90-Day Median Views}$)**, enforcing the `>= 2.5x` Green Light threshold.
* **Part B — Package-First & C.L.I.P. Hook Stress-Tester:** Provides live character-count guardrails (`<= 60 chars`) for your primary title, strict word-count validation (`<= 4 words`) for your thumbnail text overlay, a 4-beat **C.L.I.P.** hook drafter (*Contradiction*, *Locked-In Stakes*, *Instant Proof*, *Payoff Loop*), and a real-time **Effective Retention Index ($\text{ERI} = \text{CTR} \times \text{30s Hold} \times \text{APV}$)** calculator.

### 3.4 Module 4: 1-to-15 Omnichannel Repurposing Matrix & 4-Hour Batch Sprint Tracker (Chapters 5, 6 & 7)

Module 4 operationalizes the **1-to-15 Omnichannel Waterfall** (`A01` Anchor Pillar, `S01`–`S05` Vertical Shorts, `T01`–`T04` Written Authority Posts, `C01`–`C03` Visual Carousels, and `E01`–`E02` Offer-Bridge Emails):

* **4-Hour Weekly Batch Sprint Checkboxes:** Track your four time-boxed weekly production blocks (Monday 45m Research, Tuesday 75m Scripting, Wednesday 90m Batch Recording, Thursday 30m 12-Point QA & Scheduling).
* **Interactive 15-Asset Pipeline Board:** Update the status of each derivative asset (`Draft` -> `Ready` -> `Scheduled` -> `Published`) and monitor your weekly completion counter.

### 3.5 Module 5: Brand Sponsorship Rate Card & Usage-Rights Pricing Calculator ($R_{\text{sponsor}}$ — Chapter 10)

Module 5 prevents creators from underpricing their B2B media inventory or giving away perpetual paid ad whitelisting for free. Enter your trailing long-form views, niche CPM (`$45–$120`), active newsletter subscribers, open rate, sponsor click rate, B2B CPC (`$3.50–$8.00`), paid ad whitelisting months (`+30%/mo`), and category exclusivity months (`+20%/mo`). The module calculates:

1. **Tier A: Single Validation Sprint Rate** (Organic Video + Newsletter Placement)
2. **Tier B: Omnichannel Outcome Bundle Rate** (Includes Shorts, LinkedIn Post, Whitelisting, Exclusivity & Performance Bonus)
3. **Tier C: 90-Day Category-Exclusive Partner Retainer** (3-Month Bundle with `10%` partner savings)

Click **1-Click Copy 3-Tier Proposal** to copy a complete, contract-ready outbound or inbound pitch email with `50%` upfront deposit and `Net-15` terms baked in.

### 3.6 Module 6: The 20-Minute Friday Creator CEO Scorecard, 100-Gate Checklist & 20-Diagram Explorer

Module 6 serves as your weekly executive governance dashboard:

* **Friday 20-Minute Creator CEO KPI Log:** Record your weekly hours worked (`<= 25h` hard cap), weekly gross revenue, automatically calculated RPPH (`$/hr`), Pillar Outlier Multiplier, 30-second hold rate, and net new email opt-ins.
* **Interactive 20-Diagram Visual Architecture Explorer:** Select any of the **20 high-resolution vector SVG diagrams** (`Chapter 01 Mindmap & Flowchart` through `Chapter 10 Mindmap & Flowchart`) from the dropdown menu to inspect the complete visual architecture offline.
* **100-Item Master OS Installation Checklist:** Track all 100 stage-gate verification items (10 per chapter across Chapters 1 through 10) with a live completion progress bar.

---

## 4. Data Portability, Backups & Troubleshooting

* **Exporting a Workspace Backup (`.json`):** Click **Export JSON** in the top header bar to download `creator-os-workspace-backup.json`. Store this file in your project folder or cloud drive to transfer your state between desktop and laptop machines.
* **Importing a Workspace Backup (`.json`):** Click **Import JSON** in the top header and select any previously exported `.json` snapshot.
* **Exporting KPI Telemetry to Excel / Google Sheets (`.csv`):** Click **Export CSV** in the top header to download `creator-ceo-friday-scorecard.csv`.
* **Printing an Executive PDF Snapshot:** Click **Print / PDF** in the top header (or press `Ctrl+P` / `Cmd+P`) and choose **Save as PDF** to generate a clean multi-page executive summary of your current calculators and scorecards.
"""


# ---------------------------------------------------------------------------
# 4. RENDER HEADLESS DASHBOARD PREVIEW SCREENSHOT (1600x1000 PNG)
# ---------------------------------------------------------------------------

def render_webapp_screenshot(app_html_path: Path, output_png_path: Path) -> None:
    output_png_path.parent.mkdir(parents=True, exist_ok=True)
    w, h = 1600, 1000
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_png = Path(tmpdir) / "raw_webapp.png"
        user_data_dir = Path(tmpdir) / "profile"
        cmd = [
            BROWSER_BIN,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--user-data-dir={user_data_dir}",
            f"--window-size={w},{h + 80}",
            f"--screenshot={tmp_png}",
            app_html_path.as_uri(),
        ]
        subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        if not tmp_png.is_file():
            raise RuntimeError("Failed to capture headless screenshot of creator-os-app.html")
        with Image.open(tmp_png) as img:
            cropped = img.crop((0, 0, w, h))
            cropped.save(output_png_path, format="PNG", optimize=True)


# ---------------------------------------------------------------------------
# 5. MAIN EXECUTION
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 88)
    print("ANTIGRAVITY SAAS-LITE WEB APPLICATION COMPILER (build_webapp.py) -- PHASE 6")
    print(f"Studio Root: {STUDIO_ROOT}")
    print("=" * 88)

    app_path = STUDIO_ROOT / "07-INTERACTIVE-TOOLS/creator-os-app.html"
    key_path = STUDIO_ROOT / "07-INTERACTIVE-TOOLS/PRO-ACCESS-LICENSE-KEY.txt"
    readme_path = STUDIO_ROOT / "07-INTERACTIVE-TOOLS/README-WEB-APP.md"
    preview_png_path = STUDIO_ROOT / "04-VISUAL-ASSETS/png/webapp-dashboard-preview.png"

    app_path.parent.mkdir(parents=True, exist_ok=True)

    print("[1/4] Compiling 100% Offline Single-File Web App (07-INTERACTIVE-TOOLS/creator-os-app.html)...")
    html_content = build_webapp_html()
    app_path.write_text(html_content, encoding="utf-8")
    print(f"      -> Done: {app_path.stat().st_size:,} bytes")

    print("[2/4] Writing Pro Access License Key File (07-INTERACTIVE-TOOLS/PRO-ACCESS-LICENSE-KEY.txt)...")
    key_path.write_text(build_license_key_txt(), encoding="utf-8")
    print(f"      -> Done: {key_path.stat().st_size:,} bytes")

    print("[3/4] Writing Web App Operational Documentation (07-INTERACTIVE-TOOLS/README-WEB-APP.md)...")
    readme_txt = build_readme_web_app_md()
    readme_path.write_text(readme_txt, encoding="utf-8")
    print(f"      -> Done: {len(readme_txt.split()):,} words, {readme_path.stat().st_size:,} bytes")

    print("[4/4] Capturing 1600x1000 UI Preview Screenshot (04-VISUAL-ASSETS/png/webapp-dashboard-preview.png)...")
    render_webapp_screenshot(app_path, preview_png_path)
    print(f"      -> Done: {preview_png_path.stat().st_size:,} bytes")

    # Update PROJECT_STATE.json
    state_path = STUDIO_ROOT / "PROJECT_STATE.json"
    state_data = json.loads(state_path.read_text(encoding="utf-8"))
    state_data.setdefault("phase_status", {})["Phase 6"] = "COMPLETED"
    state_data["phase6_webapp"] = {
        "app_path": "07-INTERACTIVE-TOOLS/creator-os-app.html",
        "app_size_bytes": app_path.stat().st_size,
        "license_key_path": "07-INTERACTIVE-TOOLS/PRO-ACCESS-LICENSE-KEY.txt",
        "license_key_size_bytes": key_path.stat().st_size,
        "readme_path": "07-INTERACTIVE-TOOLS/README-WEB-APP.md",
        "readme_words": len(readme_txt.split()),
        "readme_size_bytes": readme_path.stat().st_size,
        "preview_png_path": "04-VISUAL-ASSETS/png/webapp-dashboard-preview.png",
        "preview_png_size_bytes": preview_png_path.stat().st_size,
        "embedded_prompts_count": 50,
        "embedded_scripts_count": 12,
        "interactive_modules_count": 6,
        "embedded_svg_diagrams_count": 20,
    }
    state_path.write_text(json.dumps(state_data, indent=2) + "\n", encoding="utf-8")
    print("\n[SUCCESS] PROJECT_STATE.json updated with Phase 6 telemetry.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
