#!/usr/bin/env python3
"""
PHASE 10: STATIC WEB DEPLOYMENT PORTAL, LIVE INTERACTIVE HUB & CLOUD BUNDLE COMPILER
Product #3: The AI Content Creator & Solopreneur Operating System
Target Root: e:/Ebook-Makaer/AI-Creator-Solopreneur-OS/DIGITAL-PUBLISHING-STUDIO/

Builds the complete 100% offline-ready, zero-CDN Static Web Deployment Portal inside
`15-WEB-DEPLOYMENT/` and mirrors the exact production tree into `docs/` for 1-click
GitHub Pages, Vercel, Netlify, and Cloudflare Pages hosting.
"""

import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

STUDIO_ROOT = Path(__file__).resolve().parent
DEPLOY_DIR = STUDIO_ROOT / "15-WEB-DEPLOYMENT"
DOCS_DIR = STUDIO_ROOT / "docs"

CHAPTER_TITLES = {
    "01": "The Creator-to-Operator Paradigm & The 5-Stage Content-to-Cash OS",
    "02": "Profitable Niche Positioning, Audience Avatar & Authority Moat (P.A.I.D.)",
    "03": "The AI Outlier Idea Engine & Predictive Topic Validation (S.I.G.N.A.L.)",
    "04": "Irresistible Packaging: Title, Thumbnail & 3-Second Hook Engineering (C.L.I.P.)",
    "05": "High-Retention Pillar Scripting & Voice Calibration (H.E.A.R.T.)",
    "06": "The 1-to-15 Omnichannel Waterfall & Derivative Content Matrix",
    "07": "The 4-Hour Weekly Batch Production Pipeline & AI Automation Stack",
    "08": "Rented-to-Owned Audience Architecture: Lead Magnets & Welcome Sequences",
    "09": "The Solopreneur Digital Product Value Ladder & 14-Day Launch Blueprint",
    "10": "Outcome-Based Sponsorships, Brand Deal Pricing & The Creator CEO Scorecard",
}


def build_ecosystem_portal_bar(prefix: str, active_route: str) -> str:
    """
    Returns the persistent, responsive top Ecosystem Live Portal Bar HTML + CSS.
    `prefix` is '.' for root pages (index.html, 404.html) or '..' for subfolder pages
    (app/, studio/, atlas/, downloads/).
    """
    def nav_cls(route_key: str) -> str:
        return "eco-portal-link active" if active_route == route_key else "eco-portal-link"

    return f"""
<!-- PHASE 10 GLOBAL ECOSYSTEM LIVE PORTAL BAR -->
<style>
  .eco-portal-bar {{
    background: linear-gradient(90deg, #060911 0%, #0F172A 45%, #1E1B4B 100%);
    border-bottom: 2px solid #4F46E5;
    padding: 8px 20px;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 12.5px;
    color: #F8FAFC;
    position: relative;
    z-index: 2000;
  }}
  .eco-portal-inner {{
    max-width: 1440px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 10px;
  }}
  .eco-portal-brand {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-weight: 800;
    color: #FFFFFF;
    text-decoration: none;
    letter-spacing: -0.2px;
  }}
  .eco-portal-dot {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #2DD4BF;
    box-shadow: 0 0 8px #2DD4BF;
    display: inline-block;
  }}
  .eco-portal-tag {{
    background: rgba(79, 70, 229, 0.3);
    border: 1px solid #818CF8;
    color: #E0E7FF;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 10.5px;
    font-weight: 800;
    padding: 2px 7px;
    border-radius: 999px;
    text-transform: uppercase;
  }}
  .eco-portal-nav {{
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px;
  }}
  .eco-portal-link {{
    color: #CBD5E1;
    text-decoration: none;
    font-weight: 700;
    padding: 5px 11px;
    border-radius: 6px;
    border: 1px solid transparent;
    transition: all 0.14s ease;
    white-space: nowrap;
  }}
  .eco-portal-link:hover {{
    color: #FFFFFF;
    background: rgba(79, 70, 229, 0.22);
    border-color: #6366F1;
  }}
  .eco-portal-link.active {{
    background: #4F46E5;
    color: #FFFFFF;
    border-color: #818CF8;
  }}
  .eco-portal-cta {{
    background: #0D9488;
    color: #FFFFFF !important;
    text-decoration: none;
    font-weight: 800;
    padding: 5px 12px;
    border-radius: 6px;
    border: 1px solid #2DD4BF;
    white-space: nowrap;
    transition: opacity 0.14s ease;
  }}
  .eco-portal-cta:hover {{
    opacity: 0.92;
  }}
</style>
<div class="eco-portal-bar" role="navigation" aria-label="Global Creator OS Ecosystem Portal Navigation">
  <div class="eco-portal-inner">
    <a href="{prefix}/index.html" class="eco-portal-brand">
      <span class="eco-portal-dot"></span>
      <span>CREATOR OS LIVE PORTAL</span>
      <span class="eco-portal-tag">v1.0.0 OFFLINE-READY</span>
    </a>
    <div class="eco-portal-nav">
      <a href="{prefix}/index.html" class="{nav_cls('home')}">Sales &amp; ROI Calculator</a>
      <a href="{prefix}/app/index.html" class="{nav_cls('app')}">Launch Creator OS Web App</a>
      <a href="{prefix}/studio/index.html" class="{nav_cls('studio')}">Thumbnail &amp; Cover Studio</a>
      <a href="{prefix}/atlas/index.html" class="{nav_cls('atlas')}">Visual Shortcut Atlas (31 SVGs)</a>
      <a href="{prefix}/downloads/index.html" class="{nav_cls('downloads')}">Tier 0 Download Hub</a>
      <a href="{prefix}/downloads/tier0-free-sample-starter-kit.zip" class="eco-portal-cta" download>Download Free Tier 0 Audit Kit (.ZIP)</a>
    </div>
  </div>
</div>
"""


def build_landing_page() -> str:
    """
    Enhances `10-MARKETING/index.html` into the unified Phase 10 root `index.html`:
    - Injects PWA manifest link
    - Injects Global Ecosystem Live Portal Bar at top of <body>
    - Wires all Tier 0 & pricing CTAs to valid relative deployment routes
    - Adds Live Interactive Suite & Commercial Packaging Showcase section with local ./assets/ and ./downloads/ links
    """
    src_html = (STUDIO_ROOT / "10-MARKETING" / "index.html").read_text(encoding="utf-8")

    # 1. Inject PWA manifest link inside <head>
    src_html = src_html.replace(
        '<title>The AI Content Creator &amp; Solopreneur Operating System — Official Flagship Suite</title>',
        '<title>The AI Content Creator &amp; Solopreneur Operating System — Official Flagship Suite &amp; Live Portal</title>\n'
        '  <link rel="manifest" href="./manifest.json" />\n'
        '  <meta name="theme-color" content="#0F172A" />\n'
        '  <meta name="description" content="A Practical System to Research Validated Ideas, Script High-Retention Content, Repurpose Across Platforms, Automate Production, and Monetize Your Audience Without Burnout." />'
    )

    # 2. Inject Global Ecosystem Live Portal Bar right after <body>
    portal_bar = build_ecosystem_portal_bar(".", "home")
    src_html = src_html.replace("<body>", "<body>\n" + portal_bar, 1)

    # 3. Enhance Hero CTA row to wire directly to ./downloads/tier0-free-sample-starter-kit.zip and ./app/index.html
    old_hero_cta = """        <div class="hero-cta-row">
          <a href="#pricing" class="btn-primary">Get the Complete Flagship OS Bundle (Tier 3 — $49) &rarr;</a>
          <a href="#pricing" class="btn-secondary">Download Free 7-Day Audit Kit (Tier 0 — $0)</a>
        </div>"""
    new_hero_cta = """        <div class="hero-cta-row">
          <a href="#pricing" class="btn-primary">Get the Complete Flagship OS Bundle (Tier 3 — $49) &rarr;</a>
          <a href="./downloads/tier0-free-sample-starter-kit.zip" class="btn-secondary" download>Download Free 7-Day Audit Kit (Tier 0 — $0)</a>
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:26px;">
          <a href="./app/index.html" style="background:rgba(79,70,229,0.22);border:1px solid #818CF8;color:#E0E7FF;padding:8px 14px;border-radius:8px;font-size:0.84rem;font-weight:700;text-decoration:none;">&#9654; Launch Creator OS Web App (Free + Pro Mode)</a>
          <a href="./studio/index.html" style="background:rgba(13,148,136,0.20);border:1px solid #2DD4BF;color:#CCFBF1;padding:8px 14px;border-radius:8px;font-size:0.84rem;font-weight:700;text-decoration:none;">&#9998; Open Thumbnail &amp; Cover Studio</a>
          <a href="./atlas/index.html" style="background:rgba(217,119,6,0.20);border:1px solid #FBBF24;color:#FEF3C7;padding:8px 14px;border-radius:8px;font-size:0.84rem;font-weight:700;text-decoration:none;">&#9783; Explore 31-Diagram Visual Atlas</a>
          <a href="./downloads/index.html" style="background:rgba(148,163,184,0.16);border:1px solid #64748B;color:#F1F5F9;padding:8px 14px;border-radius:8px;font-size:0.84rem;font-weight:700;text-decoration:none;">&#8681; Open Tier 0 Download Hub</a>
        </div>"""
    src_html = src_html.replace(old_hero_cta, new_hero_cta, 1)

    # 4. Replace relative ../09-EXPORTS/HYBRID-BUNDLE/... links in the 5-Tier pricing cards
    src_html = src_html.replace(
        'href="../09-EXPORTS/HYBRID-BUNDLE/Tier0-Free-Creator-Audit-Starter-Kit.zip"',
        'href="./downloads/tier0-free-sample-starter-kit.zip" download'
    )
    src_html = src_html.replace(
        'href="../09-EXPORTS/HYBRID-BUNDLE/Tier1-KDP-and-D2D-Retail-Book-Pack.zip"',
        'href="#live-ecosystem-hub"'
    )
    src_html = src_html.replace(
        'href="../09-EXPORTS/HYBRID-BUNDLE/Tier2-Interactive-Workbook-and-Tablet-Edition.zip"',
        'href="#live-ecosystem-hub"'
    )
    src_html = src_html.replace(
        'href="../09-EXPORTS/HYBRID-BUNDLE/Tier3-Complete-Creator-Solopreneur-OS-Flagship-Bundle.zip"',
        'href="./app/index.html"'
    )
    src_html = src_html.replace(
        'href="../09-EXPORTS/HYBRID-BUNDLE/Tier4-Living-Creator-Vault-Membership-Pack.zip"',
        'href="#live-ecosystem-hub"'
    )

    # 5. Inject the Live Interactive Web Portal, Self-Hosted Tier 0 Download Hub & Commercial Cover Gallery right after the Pricing Section
    live_hub_section = """
  <!-- 6B. LIVE INTERACTIVE WEB ECOSYSTEM, TIER 0 DOWNLOAD HUB & COMMERCIAL EDITION SHOWCASE -->
  <section class="section section-dark" id="live-ecosystem-hub">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Live Static Web Portal &amp; Direct Starter Downloads</span>
        <h2>Launch the Interactive Web Suite &amp; Download Tier 0 Starter Files</h2>
        <p>Every interactive tool, vector diagram, and Tier 0 starter kit asset below is hosted directly inside this static web portal with zero external dependencies.</p>
      </div>

      <!-- 4 Live Interactive Portal Routes -->
      <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:18px;margin-bottom:44px;">
        <div style="background:#1E293B;border:2px solid #4F46E5;border-radius:14px;padding:22px;display:flex;flex-direction:column;justify-content:space-between;">
          <div>
            <span class="badge-pill badge-teal mono" style="margin-bottom:10px;">ROUTE 01 · /app/</span>
            <h3 style="font-size:1.15rem;font-weight:900;color:#FFFFFF;margin-bottom:8px;">Creator OS Web Companion App</h3>
            <p style="font-size:0.86rem;color:#CBD5E1;margin-bottom:16px;">6 interactive unit-economics simulators, 50 AI Workflow Prompts (P01–P50), 12 Emergency Scripts (S01–S12), and 20 embedded vector diagrams. Includes Free Diagnostic Mode + Pro Key (<code class="mono">CREATOR-OS-PRO-2026</code>).</p>
          </div>
          <a href="./app/index.html" class="price-cta" style="background:#4F46E5;">Launch Web Companion App &rarr;</a>
        </div>

        <div style="background:#1E293B;border:2px solid #0D9488;border-radius:14px;padding:22px;display:flex;flex-direction:column;justify-content:space-between;">
          <div>
            <span class="badge-pill badge-teal mono" style="margin-bottom:10px;">ROUTE 02 · /studio/</span>
            <h3 style="font-size:1.15rem;font-weight:900;color:#FFFFFF;margin-bottom:8px;">Thumbnail &amp; Cover Customizer Studio</h3>
            <p style="font-size:0.86rem;color:#CBD5E1;margin-bottom:16px;">Interactive vector &amp; high-resolution PNG design engine with 6 platform presets (YouTube 16:9 Thumbnail, 6&times;9 Book Cover, Gumroad Hero, LinkedIn/IG Carousel, Lead Magnet Cover) and 6 color palettes.</p>
          </div>
          <a href="./studio/index.html" class="price-cta" style="background:#0D9488;">Open Design Customizer Studio &rarr;</a>
        </div>

        <div style="background:#1E293B;border:2px solid #D97706;border-radius:14px;padding:22px;display:flex;flex-direction:column;justify-content:space-between;">
          <div>
            <span class="badge-pill badge-teal mono" style="margin-bottom:10px;">ROUTE 03 · /atlas/</span>
            <h3 style="font-size:1.15rem;font-weight:900;color:#FFFFFF;margin-bottom:8px;">31-SVG Visual Shortcut Atlas</h3>
            <p style="font-size:0.86rem;color:#CBD5E1;margin-bottom:16px;">Interactive browser embedding the Master Ecosystem Map Poster, all 10 One-Page Chapter Visual Cheat Sheets, and all 20 Chapter Mindmaps &amp; Flowcharts with full-screen zoom and 1-click SVG export.</p>
          </div>
          <a href="./atlas/index.html" class="price-cta" style="background:#D97706;">Explore 31-Diagram Visual Atlas &rarr;</a>
        </div>

        <div style="background:#1E293B;border:2px solid #818CF8;border-radius:14px;padding:22px;display:flex;flex-direction:column;justify-content:space-between;">
          <div>
            <span class="badge-pill badge-teal mono" style="margin-bottom:10px;">ROUTE 04 · /downloads/</span>
            <h3 style="font-size:1.15rem;font-weight:900;color:#FFFFFF;margin-bottom:8px;">Tier 0 Free Audit Starter Hub</h3>
            <p style="font-size:0.86rem;color:#CBD5E1;margin-bottom:16px;">Direct browser downloads for the 57-page Sample Book PDF, 13-page Fillable Ch 1 Workbook (48 AcroForm fields), 12-page Visual Shortcut Atlas PDF, Baseline Audit CSV, and complete Tier 0 Starter ZIP.</p>
          </div>
          <a href="./downloads/index.html" class="price-cta" style="background:#6366F1;">Open Direct Download Hub &rarr;</a>
        </div>
      </div>

      <!-- Direct 1-Click Self-Hosted Tier 0 & Visual Atlas File Table -->
      <div style="background:#0F172A;border:1px solid #334155;border-radius:14px;padding:24px;margin-bottom:44px;">
        <h3 style="font-size:1.2rem;font-weight:900;color:#FFFFFF;margin-bottom:6px;">Direct 1-Click Tier 0 Starter Kit &amp; Visual Atlas Downloads</h3>
        <p style="font-size:0.88rem;color:#94A3B8;margin-bottom:18px;">Click any asset below to download immediately from this static server (<code class="mono">./downloads/</code>):</p>
        <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:12px;">
          <a href="./downloads/tier0-free-sample-starter-kit.zip" download style="background:#1E1B4B;border:1px solid #6366F1;border-radius:10px;padding:12px 14px;color:#FFFFFF;text-decoration:none;font-weight:700;font-size:0.85rem;display:flex;justify-content:space-between;align-items:center;">
            <span>1. Complete Tier 0 Starter Kit (.ZIP)</span>
            <span class="mono" style="color:#2DD4BF;font-size:0.76rem;">2.26 MB</span>
          </a>
          <a href="./downloads/tier0-free-sample-chapter01-and-audit.pdf" download style="background:#1E293B;border:1px solid #334155;border-radius:10px;padding:12px 14px;color:#F8FAFC;text-decoration:none;font-weight:700;font-size:0.85rem;display:flex;justify-content:space-between;align-items:center;">
            <span>2. Chapter 1 + Audit Sample Book (.PDF)</span>
            <span class="mono" style="color:#94A3B8;font-size:0.76rem;">57 Pages</span>
          </a>
          <a href="./downloads/chapter-01-workbook.pdf" download style="background:#1E293B;border:1px solid #334155;border-radius:10px;padding:12px 14px;color:#F8FAFC;text-decoration:none;font-weight:700;font-size:0.85rem;display:flex;justify-content:space-between;align-items:center;">
            <span>3. Fillable Ch 01 Action Workbook (.PDF)</span>
            <span class="mono" style="color:#94A3B8;font-size:0.76rem;">48 Fields</span>
          </a>
          <a href="./downloads/the-ai-creator-solopreneur-os-visual-shortcut-atlas.pdf" download style="background:#1E293B;border:1px solid #334155;border-radius:10px;padding:12px 14px;color:#F8FAFC;text-decoration:none;font-weight:700;font-size:0.85rem;display:flex;justify-content:space-between;align-items:center;">
            <span>4. 12-Page Visual Shortcut Atlas (.PDF)</span>
            <span class="mono" style="color:#94A3B8;font-size:0.76rem;">12 Pages</span>
          </a>
          <a href="./downloads/sheet1-creator-rpm-and-time-audit.csv" download style="background:#1E293B;border:1px solid #334155;border-radius:10px;padding:12px 14px;color:#F8FAFC;text-decoration:none;font-weight:700;font-size:0.85rem;display:flex;justify-content:space-between;align-items:center;">
            <span>5. Creator RPM &amp; Time-Leak Audit (.CSV)</span>
            <span class="mono" style="color:#94A3B8;font-size:0.76rem;">25 Rows</span>
          </a>
          <a href="./downloads/00-ECOSYSTEM-MASTER-MAP-POSTER.png" download style="background:#1E293B;border:1px solid #334155;border-radius:10px;padding:12px 14px;color:#F8FAFC;text-decoration:none;font-weight:700;font-size:0.85rem;display:flex;justify-content:space-between;align-items:center;">
            <span>6. Master Ecosystem Map Poster (.PNG)</span>
            <span class="mono" style="color:#94A3B8;font-size:0.76rem;">300 DPI</span>
          </a>
          <a href="./downloads/cheat-sheet-ch01.png" download style="background:#1E293B;border:1px solid #334155;border-radius:10px;padding:12px 14px;color:#F8FAFC;text-decoration:none;font-weight:700;font-size:0.85rem;display:flex;justify-content:space-between;align-items:center;">
            <span>7. Chapter 01 Visual Cheat Sheet (.PNG)</span>
            <span class="mono" style="color:#94A3B8;font-size:0.76rem;">300 DPI</span>
          </a>
        </div>
      </div>

      <!-- Commercial Cover & Dashboard Preview Gallery (./assets/) -->
      <div style="display:grid;grid-template-columns:repeat(6, 1fr);gap:14px;align-items:stretch;">
        <div style="background:#0F172A;border:1px solid #334155;border-radius:10px;padding:10px;text-align:center;">
          <img src="./assets/ebook-cover-kdp-kindle.png" alt="KDP &amp; Kindle eBook Cover" style="width:100%;height:140px;object-fit:cover;border-radius:6px;margin-bottom:8px;" loading="lazy" />
          <div style="font-size:0.74rem;font-weight:800;color:#E2E8F0;">Tier 1 Retail eBook</div>
        </div>
        <div style="background:#0F172A;border:1px solid #334155;border-radius:10px;padding:10px;text-align:center;">
          <img src="./assets/gumroad-tier0-free-audit-cover.png" alt="Tier 0 Free Creator Audit Cover" style="width:100%;height:140px;object-fit:cover;border-radius:6px;margin-bottom:8px;" loading="lazy" />
          <div style="font-size:0.74rem;font-weight:800;color:#E2E8F0;">Tier 0 Free Audit Kit</div>
        </div>
        <div style="background:#0F172A;border:1px solid #334155;border-radius:10px;padding:10px;text-align:center;">
          <img src="./assets/gumroad-tier2-workbook-edition-cover.png" alt="Tier 2 Fillable Workbook Cover" style="width:100%;height:140px;object-fit:cover;border-radius:6px;margin-bottom:8px;" loading="lazy" />
          <div style="font-size:0.74rem;font-weight:800;color:#E2E8F0;">Tier 2 Workbook Suite</div>
        </div>
        <div style="background:#0F172A;border:1px solid #4F46E5;border-radius:10px;padding:10px;text-align:center;">
          <img src="./assets/gumroad-tier3-flagship-bundle-cover.png" alt="Tier 3 Flagship Creator OS Cover" style="width:100%;height:140px;object-fit:cover;border-radius:6px;margin-bottom:8px;" loading="lazy" />
          <div style="font-size:0.74rem;font-weight:800;color:#A5B4FC;">Tier 3 Flagship Bundle</div>
        </div>
        <div style="background:#0F172A;border:1px solid #334155;border-radius:10px;padding:10px;text-align:center;">
          <img src="./assets/gumroad-tier4-vault-membership-cover.png" alt="Tier 4 Living Vault Pass Cover" style="width:100%;height:140px;object-fit:cover;border-radius:6px;margin-bottom:8px;" loading="lazy" />
          <div style="font-size:0.74rem;font-weight:800;color:#E2E8F0;">Tier 4 Living Vault Pass</div>
        </div>
        <div style="background:#0F172A;border:1px solid #0D9488;border-radius:10px;padding:10px;text-align:center;">
          <img src="./assets/webapp-dashboard-preview.png" alt="Creator OS Offline Web App Dashboard Preview" style="width:100%;height:140px;object-fit:cover;border-radius:6px;margin-bottom:8px;" loading="lazy" />
          <div style="font-size:0.74rem;font-weight:800;color:#5EEAD4;">Offline SaaS-Lite App</div>
        </div>
      </div>
    </div>
  </section>
"""
    src_html = src_html.replace(
        "<!-- 7. 12-ITEM INTERACTIVE FAQ ACCORDION -->",
        live_hub_section + "\n  <!-- 7. 12-ITEM INTERACTIVE FAQ ACCORDION -->",
        1
    )

    return src_html


def build_web_app_page() -> str:
    """
    Deploys `07-INTERACTIVE-TOOLS/creator-os-app.html` with the unified Ecosystem Live Portal Bar
    for `app/index.html` and `app/creator-os-app.html`.
    """
    src_html = (STUDIO_ROOT / "07-INTERACTIVE-TOOLS" / "creator-os-app.html").read_text(encoding="utf-8")
    src_html = src_html.replace(
        "<title>The AI Content Creator &amp; Solopreneur Operating System — Interactive Companion Suite (v1.0.0)</title>",
        "<title>The AI Content Creator &amp; Solopreneur Operating System — Interactive Companion Suite (v1.0.0)</title>\n"
        '<link rel="manifest" href="../manifest.json" />'
    )
    portal_bar = build_ecosystem_portal_bar("..", "app")
    src_html = src_html.replace("<body>", "<body>\n" + portal_bar, 1)
    return src_html


def build_studio_page() -> str:
    """
    Deploys `08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html` with the unified
    Ecosystem Live Portal Bar for `studio/index.html` and `studio/design-customizer-studio.html`.
    """
    src_html = (STUDIO_ROOT / "08-COVER-DESIGN" / "Editable-Design-Kit" / "design-customizer-studio.html").read_text(encoding="utf-8")
    src_html = src_html.replace(
        "<title>Creator OS — Interactive Cover, YouTube Thumbnail &amp; Social Card Customizer Studio</title>",
        "<title>Creator OS — Interactive Cover, YouTube Thumbnail &amp; Social Card Customizer Studio</title>\n"
        '  <link rel="manifest" href="../manifest.json" />'
    )
    portal_bar = build_ecosystem_portal_bar("..", "studio")
    src_html = src_html.replace("<body>", "<body>\n" + portal_bar, 1)
    return src_html


def build_atlas_page() -> str:
    """
    Builds `atlas/index.html` (>= 45,000 bytes) — Interactive Visual Shortcut Atlas & 31-SVG
    Architecture Explorer embedding:
    - Tab 1: Master Ecosystem Map Poster (`00-ECOSYSTEM-MASTER-MAP-POSTER.svg`)
    - Tab 2: 10 One-Page Chapter Visual Cheat Sheets (`cheat-sheet-ch01.svg` .. `cheat-sheet-ch10.svg`)
    - Tab 3: 20 Chapter System Mindmaps & Decision Flowcharts (`chapter-01-mindmap.svg` .. `chapter-10-flowchart.svg`)
    With chapter filters, search, full-screen zoom modal, 1-click SVG download, and direct link
    to `../downloads/the-ai-creator-solopreneur-os-visual-shortcut-atlas.pdf`.
    """
    portal_bar = build_ecosystem_portal_bar("..", "atlas")

    # Collect all 31 SVGs
    cards_html = []

    # 1. Master Ecosystem Map Poster
    master_svg_path = STUDIO_ROOT / "13-VISUAL-CHEAT-SHEETS" / "svg" / "00-ECOSYSTEM-MASTER-MAP-POSTER.svg"
    master_svg = master_svg_path.read_text(encoding="utf-8")
    cards_html.append(f"""
      <article class="atlas-card" data-category="master" data-chapter="00" data-search="master ecosystem map poster 5-stage content-to-cash engine signal clip heart waterfall">
        <div class="atlas-card-head">
          <div>
            <span class="atlas-badge badge-master mono">MASTER ARCHITECTURE POSTER · DIAGRAM 01 / 31</span>
            <h3>The AI Content Creator &amp; Solopreneur OS — Master 5-Stage Ecosystem Map</h3>
            <p>Complete end-to-end visual blueprint linking S.I.G.N.A.L. Validation, C.L.I.P. Packaging, H.E.A.R.T. Scripting, 1-to-15 Repurposing, Owned Audience Bridge, and 4-Tier Monetization.</p>
          </div>
          <div class="atlas-card-actions">
            <button type="button" class="btn-atlas btn-zoom" onclick="openSvgModal(this)">Full-Screen Zoom</button>
            <button type="button" class="btn-atlas btn-dl" onclick="downloadInlineSvg(this, '00-ECOSYSTEM-MASTER-MAP-POSTER.svg')">Download .SVG</button>
          </div>
        </div>
        <div class="atlas-svg-stage">
          {master_svg}
        </div>
      </article>
    """)

    # 2. 10 One-Page Chapter Visual Cheat Sheets
    for i in range(1, 11):
        ch_num = f"{i:02d}"
        cs_name = f"cheat-sheet-ch{ch_num}.svg"
        cs_path = STUDIO_ROOT / "13-VISUAL-CHEAT-SHEETS" / "svg" / cs_name
        cs_svg = cs_path.read_text(encoding="utf-8")
        ch_title = CHAPTER_TITLES[ch_num]
        diag_idx = i + 1
        cards_html.append(f"""
      <article class="atlas-card" data-category="cheatsheets" data-chapter="{ch_num}" data-search="chapter {ch_num} cheat sheet {ch_title.lower()}">
        <div class="atlas-card-head">
          <div>
            <span class="atlas-badge badge-cs mono">CHAPTER {ch_num} ONE-PAGE CHEAT SHEET · DIAGRAM {diag_idx:02d} / 31</span>
            <h3>Chapter {ch_num} Visual Cheat Sheet: {ch_title}</h3>
            <p>High-density 1-page reference card summarizing Chapter {ch_num} stage gates, core mathematical formulas, AI workflow prompts, and execution checklist.</p>
          </div>
          <div class="atlas-card-actions">
            <button type="button" class="btn-atlas btn-zoom" onclick="openSvgModal(this)">Full-Screen Zoom</button>
            <button type="button" class="btn-atlas btn-dl" onclick="downloadInlineSvg(this, '{cs_name}')">Download .SVG</button>
          </div>
        </div>
        <div class="atlas-svg-stage">
          {cs_svg}
        </div>
      </article>
        """)

    # 3. 20 Chapter System Mindmaps & Decision Flowcharts
    diag_counter = 12
    for i in range(1, 11):
        ch_num = f"{i:02d}"
        ch_title = CHAPTER_TITLES[ch_num]
        for kind, kind_label in [("mindmap", "System Architecture Mindmap"), ("flowchart", "Stage-Gate Decision Flowchart")]:
            svg_name = f"chapter-{ch_num}-{kind}.svg"
            svg_path = STUDIO_ROOT / "04-VISUAL-ASSETS" / "svg" / svg_name
            svg_raw = svg_path.read_text(encoding="utf-8")
            cards_html.append(f"""
      <article class="atlas-card" data-category="diagrams" data-chapter="{ch_num}" data-search="chapter {ch_num} {kind} {kind_label.lower()} {ch_title.lower()}">
        <div class="atlas-card-head">
          <div>
            <span class="atlas-badge badge-diag mono">CHAPTER {ch_num} {kind.upper()} · DIAGRAM {diag_counter:02d} / 31</span>
            <h3>Chapter {ch_num} {kind_label}: {ch_title}</h3>
            <p>Production vector {kind} (`900x480` viewBox) illustrating the deterministic workflow and quantitative pass/fail gates for Chapter {ch_num}.</p>
          </div>
          <div class="atlas-card-actions">
            <button type="button" class="btn-atlas btn-zoom" onclick="openSvgModal(this)">Full-Screen Zoom</button>
            <button type="button" class="btn-atlas btn-dl" onclick="downloadInlineSvg(this, '{svg_name}')">Download .SVG</button>
          </div>
        </div>
        <div class="atlas-svg-stage">
          {svg_raw}
        </div>
      </article>
            """)
            diag_counter += 1

    chapter_options = ['<option value="ALL">All Chapters (Master Map + Ch 01–Ch 10)</option>', '<option value="00">00 — Master Ecosystem Map Poster</option>']
    for i in range(1, 11):
        ch_num = f"{i:02d}"
        chapter_options.append(f'<option value="{ch_num}">Chapter {ch_num}: {CHAPTER_TITLES[ch_num]}</option>')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Visual Shortcut Atlas &amp; 31-Diagram Architecture Explorer — AI Creator &amp; Solopreneur OS</title>
  <link rel="manifest" href="../manifest.json" />
  <style>
    :root {{
      --primary: #0F172A;
      --accent: #4F46E5;
      --accent-light: #818CF8;
      --secondary: #0D9488;
      --secondary-light: #2DD4BF;
      --warning: #D97706;
      --text: #F8FAFC;
      --muted: #94A3B8;
      --card: #1E293B;
      --border: #334155;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #090D16;
      color: var(--text);
      line-height: 1.55;
      min-height: 100vh;
    }}
    .mono {{ font-family: 'JetBrains Mono', 'Consolas', monospace; }}
    .atlas-hero {{
      background: radial-gradient(circle at 20% 20%, rgba(79, 70, 229, 0.25) 0%, transparent 50%),
                  linear-gradient(180deg, #0F172A 0%, #090D16 100%);
      border-bottom: 2px solid var(--accent);
      padding: 36px 24px;
    }}
    .container {{
      max-width: 1380px;
      margin: 0 auto;
    }}
    .hero-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-wrap: wrap;
      gap: 20px;
    }}
    .hero-top h1 {{
      font-size: 2.1rem;
      font-weight: 900;
      letter-spacing: -0.6px;
      margin-top: 6px;
      margin-bottom: 8px;
    }}
    .hero-top p {{
      color: var(--muted);
      max-width: 780px;
      font-size: 0.96rem;
    }}
    .pdf-cta-btn {{
      background: linear-gradient(135deg, var(--accent) 0%, var(--secondary) 100%);
      color: #FFFFFF;
      text-decoration: none;
      font-weight: 800;
      font-size: 0.9rem;
      padding: 13px 22px;
      border-radius: 10px;
      border: 1px solid var(--secondary-light);
      display: inline-flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 10px 24px rgba(79, 70, 229, 0.35);
      white-space: nowrap;
    }}
    .filter-toolbar {{
      background: #0F172A;
      border-bottom: 1px solid var(--border);
      padding: 16px 24px;
      position: sticky;
      top: 0;
      z-index: 900;
    }}
    .toolbar-grid {{
      max-width: 1380px;
      margin: 0 auto;
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
    }}
    .tab-group {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .tab-btn {{
      background: #1E293B;
      color: #CBD5E1;
      border: 1px solid #334155;
      padding: 9px 15px;
      border-radius: 8px;
      font-weight: 800;
      font-size: 0.82rem;
      cursor: pointer;
      transition: all 0.14s;
    }}
    .tab-btn:hover {{
      border-color: var(--accent-light);
      color: #FFFFFF;
    }}
    .tab-btn.active {{
      background: var(--accent);
      color: #FFFFFF;
      border-color: var(--accent-light);
    }}
    .filter-inputs {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }}
    .filter-inputs select, .filter-inputs input {{
      background: #1E293B;
      color: #FFFFFF;
      border: 1px solid #475569;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 0.84rem;
      font-family: inherit;
    }}
    .atlas-main {{
      padding: 32px 24px 64px;
    }}
    .atlas-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 28px;
    }}
    .atlas-card {{
      background: var(--card);
      border: 1.5px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35);
    }}
    .atlas-card-head {{
      padding: 18px 22px;
      background: #0F172A;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
    }}
    .atlas-badge {{
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 999px;
      margin-bottom: 6px;
    }}
    .badge-master {{ background: rgba(13, 148, 136, 0.25); color: #2DD4BF; border: 1px solid #0D9488; }}
    .badge-cs {{ background: rgba(79, 70, 229, 0.25); color: #A5B4FC; border: 1px solid #6366F1; }}
    .badge-diag {{ background: rgba(217, 119, 6, 0.22); color: #FBBF24; border: 1px solid #D97706; }}
    .atlas-card-head h3 {{
      font-size: 1.15rem;
      font-weight: 800;
      color: #FFFFFF;
      margin-bottom: 4px;
    }}
    .atlas-card-head p {{
      font-size: 0.84rem;
      color: var(--muted);
    }}
    .atlas-card-actions {{
      display: flex;
      gap: 8px;
      flex-shrink: 0;
    }}
    .btn-atlas {{
      border: none;
      padding: 8px 14px;
      border-radius: 7px;
      font-weight: 800;
      font-size: 0.8rem;
      cursor: pointer;
    }}
    .btn-zoom {{ background: var(--accent); color: #FFFFFF; }}
    .btn-dl {{ background: var(--secondary); color: #FFFFFF; }}
    .atlas-svg-stage {{
      padding: 20px;
      background: #FFFFFF;
      display: flex;
      justify-content: center;
      align-items: center;
      overflow-x: auto;
    }}
    .atlas-svg-stage svg {{
      width: 100%;
      max-width: 1080px;
      height: auto;
      display: block;
      border-radius: 6px;
    }}
    /* Full-Screen Zoom Modal */
    .zoom-modal {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(6, 9, 17, 0.94);
      z-index: 3000;
      flex-direction: column;
    }}
    .zoom-modal.open {{
      display: flex;
    }}
    .zoom-modal-bar {{
      background: #0F172A;
      border-bottom: 2px solid var(--accent);
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .zoom-modal-canvas {{
      flex: 1;
      overflow: auto;
      padding: 28px;
      display: flex;
      justify-content: center;
      align-items: flex-start;
    }}
    .zoom-modal-inner {{
      background: #FFFFFF;
      padding: 16px;
      border-radius: 8px;
      width: 100%;
      max-width: 1300px;
      transform-origin: top center;
      transition: width 0.15s ease;
    }}
    .zoom-modal-inner svg {{
      width: 100%;
      height: auto;
      display: block;
    }}
  </style>
</head>
<body>
{portal_bar}

  <header class="atlas-hero">
    <div class="container hero-top">
      <div>
        <span class="atlas-badge badge-master mono">INTERACTIVE 31-DIAGRAM ARCHITECTURE EXPLORER</span>
        <h1>Visual Shortcut Atlas &amp; System Diagram Explorer</h1>
        <p>Inspect, filter, zoom, and export all 31 vector architecture assets: the Master 5-Stage Ecosystem Map Poster, all 10 One-Page Chapter Visual Cheat Sheets, and all 20 Chapter Mindmaps &amp; Stage-Gate Decision Flowcharts.</p>
      </div>
      <a href="../downloads/the-ai-creator-solopreneur-os-visual-shortcut-atlas.pdf" class="pdf-cta-btn" download>
        <span>&#8681; Download 12-Page Visual Shortcut Atlas (.PDF)</span>
      </a>
    </div>
  </header>

  <section class="filter-toolbar" aria-label="Diagram Filters">
    <div class="toolbar-grid">
      <div class="tab-group" role="tablist">
        <button type="button" class="tab-btn active" data-tab="all" onclick="setAtlasTab('all')">All 31 Vector Diagrams</button>
        <button type="button" class="tab-btn" data-tab="master" onclick="setAtlasTab('master')">Tab 1: Master Ecosystem Map (1)</button>
        <button type="button" class="tab-btn" data-tab="cheatsheets" onclick="setAtlasTab('cheatsheets')">Tab 2: 10 Chapter Cheat Sheets (10)</button>
        <button type="button" class="tab-btn" data-tab="diagrams" onclick="setAtlasTab('diagrams')">Tab 3: 20 Mindmaps &amp; Flowcharts (20)</button>
      </div>
      <div class="filter-inputs">
        <select id="sel-chapter" aria-label="Filter by Chapter" onchange="applyAtlasFilters()">
          {''.join(chapter_options)}
        </select>
        <input type="search" id="inp-search" placeholder="Search formula, framework, stage..." oninput="applyAtlasFilters()" />
        <span class="mono" id="lbl-count" style="font-size:0.8rem;color:#2DD4BF;font-weight:800;">Showing 31 / 31</span>
      </div>
    </div>
  </section>

  <main class="atlas-main">
    <div class="container">
      <div class="atlas-grid" id="atlas-grid">
        {''.join(cards_html)}
      </div>
    </div>
  </main>

  <!-- Full-Screen Zoom Modal -->
  <div class="zoom-modal" id="zoomModal" role="dialog" aria-modal="true" aria-label="Diagram Full-Screen Zoom">
    <div class="zoom-modal-bar">
      <strong id="zoomTitle" style="color:#FFFFFF;font-size:0.95rem;">Diagram Inspector</strong>
      <div style="display:flex;gap:8px;align-items:center;">
        <button type="button" class="tab-btn" onclick="setZoomScale('1300px')">100% Fit</button>
        <button type="button" class="tab-btn" onclick="setZoomScale('1850px')">150% Zoom</button>
        <button type="button" class="tab-btn" onclick="setZoomScale('2400px')">200% Zoom</button>
        <button type="button" class="btn-atlas btn-dl" onclick="closeSvgModal()">Close [ESC]</button>
      </div>
    </div>
    <div class="zoom-modal-canvas">
      <div class="zoom-modal-inner" id="zoomCanvasInner"></div>
    </div>
  </div>

  <script>
    let currentTab = 'all';

    function setAtlasTab(tab) {{
      currentTab = tab;
      document.querySelectorAll('.tab-btn[data-tab]').forEach(btn => {{
        btn.classList.toggle('active', btn.getAttribute('data-tab') === tab);
      }});
      applyAtlasFilters();
    }}

    function applyAtlasFilters() {{
      const ch = document.getElementById('sel-chapter').value;
      const q = (document.getElementById('inp-search').value || '').toLowerCase().trim();
      const cards = document.querySelectorAll('.atlas-card');
      let visible = 0;
      cards.forEach(card => {{
        const cat = card.getAttribute('data-category');
        const cardCh = card.getAttribute('data-chapter');
        const hay = card.getAttribute('data-search') + ' ' + card.innerText.toLowerCase();
        const matchTab = (currentTab === 'all') || (cat === currentTab);
        const matchCh = (ch === 'ALL') || (cardCh === ch);
        const matchQ = (!q) || hay.includes(q);
        const show = matchTab && matchCh && matchQ;
        card.style.display = show ? 'block' : 'none';
        if (show) visible++;
      }});
      document.getElementById('lbl-count').textContent = 'Showing ' + visible + ' / 31';
    }}

    function openSvgModal(btn) {{
      const card = btn.closest('.atlas-card');
      const title = card.querySelector('h3').textContent;
      const svgEl = card.querySelector('svg');
      document.getElementById('zoomTitle').textContent = title;
      const inner = document.getElementById('zoomCanvasInner');
      inner.innerHTML = svgEl.outerHTML;
      document.getElementById('zoomModal').classList.add('open');
    }}

    function closeSvgModal() {{
      document.getElementById('zoomModal').classList.remove('open');
    }}

    function setZoomScale(maxW) {{
      document.getElementById('zoomCanvasInner').style.maxWidth = maxW;
    }}

    function downloadInlineSvg(btn, filename) {{
      const card = btn.closest('.atlas-card');
      const svgEl = card.querySelector('svg');
      const serializer = new XMLSerializer();
      const svgBlob = new Blob([serializer.serializeToString(svgEl)], {{ type: 'image/svg+xml;charset=utf-8' }});
      const url = URL.createObjectURL(svgBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') closeSvgModal();
    }});
  </script>
</body>
</html>
"""


def build_downloads_hub_page() -> str:
    """
    Builds `downloads/index.html` — Direct Tier 0 Free Audit Starter Kit Download Hub.
    """
    portal_bar = build_ecosystem_portal_bar("..", "downloads")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Tier 0 Free Creator Audit Starter Kit Download Hub — AI Creator &amp; Solopreneur OS</title>
  <link rel="manifest" href="../manifest.json" />
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #090D16;
      color: #F8FAFC;
      line-height: 1.6;
      min-height: 100vh;
    }}
    .mono {{ font-family: 'JetBrains Mono', 'Consolas', monospace; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 48px 24px; }}
    .hub-header {{
      background: linear-gradient(160deg, #1E1B4B 0%, #0F172A 100%);
      border: 2px solid #4F46E5;
      border-radius: 16px;
      padding: 32px;
      margin-bottom: 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
    }}
    .hub-header h1 {{ font-size: 1.9rem; font-weight: 900; margin-bottom: 8px; }}
    .hub-header p {{ color: #CBD5E1; max-width: 720px; font-size: 0.95rem; }}
    .btn-zip {{
      background: #0D9488;
      color: #FFFFFF;
      text-decoration: none;
      font-weight: 800;
      padding: 14px 24px;
      border-radius: 10px;
      border: 1px solid #2DD4BF;
      font-size: 0.95rem;
    }}
    .dl-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 18px;
    }}
    .dl-card {{
      background: #1E293B;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 14px;
    }}
    .dl-card h3 {{ font-size: 1.08rem; font-weight: 800; color: #FFFFFF; margin-bottom: 6px; }}
    .dl-card p {{ font-size: 0.86rem; color: #94A3B8; }}
    .dl-btn {{
      display: inline-flex;
      justify-content: space-between;
      align-items: center;
      background: #4F46E5;
      color: #FFFFFF;
      text-decoration: none;
      padding: 10px 16px;
      border-radius: 8px;
      font-weight: 800;
      font-size: 0.85rem;
    }}
    @media (max-width: 800px) {{ .dl-grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
{portal_bar}
  <main class="container">
    <div class="hub-header">
      <div>
        <span class="mono" style="color:#2DD4BF;font-size:0.78rem;font-weight:800;">DIRECT SELF-HOSTED DOWNLOAD HUB · ZERO OPT-IN FRICTION</span>
        <h1>Tier 0 Free Creator Audit Starter Kit &amp; Visual Atlas Files</h1>
        <p>Download the complete ZIP bundle or individual PDF, Fillable Workbook, CSV, and 300-DPI Poster files directly below.</p>
      </div>
      <a href="./tier0-free-sample-starter-kit.zip" class="btn-zip" download>&#8681; Download Complete Tier 0 ZIP (2.26 MB)</a>
    </div>

    <div class="dl-grid">
      <div class="dl-card">
        <div>
          <h3>1. Tier 0 Free Sample Book: Chapter 1 &amp; 7-Day Audit (.PDF)</h3>
          <p>57-page US Letter color edition containing the Front Matter, complete Chapter 01 (9,704 words), Prompts P01–P05, and the 5-Stage Content-to-Cash Operating Engine.</p>
        </div>
        <a href="./tier0-free-sample-chapter01-and-audit.pdf" class="dl-btn" download><span>Download PDF</span><span class="mono">1.62 MB · 57 Pages</span></a>
      </div>

      <div class="dl-card">
        <div>
          <h3>2. Standalone Fillable Chapter 01 Action Workbook (.PDF)</h3>
          <p>13-page interactive AcroForm PDF workbook with 48 fillable input fields and checkboxes for your 7-Day Time-Leak &amp; Baseline RPPH Diagnostic Audit.</p>
        </div>
        <a href="./chapter-01-workbook.pdf" class="dl-btn" download><span>Download Fillable PDF</span><span class="mono">533 KB · 48 Fields</span></a>
      </div>

      <div class="dl-card">
        <div>
          <h3>3. 12-Page Visual Shortcut Atlas &amp; Cheat Sheet Book (.PDF)</h3>
          <p>Landscape executive reference atlas containing the Master Ecosystem Map Poster and all 10 One-Page Chapter Visual Cheat Sheets.</p>
        </div>
        <a href="./the-ai-creator-solopreneur-os-visual-shortcut-atlas.pdf" class="dl-btn" download><span>Download Visual Atlas PDF</span><span class="mono">1.15 MB · 12 Pages</span></a>
      </div>

      <div class="dl-card">
        <div>
          <h3>4. Creator RPM &amp; Time-Leak Baseline Audit Tracker (.CSV)</h3>
          <p>25-row pre-populated spreadsheet template ready for Notion, Excel, or Google Sheets import to calculate your baseline RPPH and HVPR.</p>
        </div>
        <a href="./sheet1-creator-rpm-and-time-audit.csv" class="dl-btn" download><span>Download CSV Tracker</span><span class="mono">5.2 KB · 25 Rows</span></a>
      </div>

      <div class="dl-card">
        <div>
          <h3>5. Master 5-Stage Ecosystem Map Poster (.PNG)</h3>
          <p>High-resolution 300-DPI PNG render of the complete AI Content Creator &amp; Solopreneur Operating System architecture map.</p>
        </div>
        <a href="./00-ECOSYSTEM-MASTER-MAP-POSTER.png" class="dl-btn" download><span>Download Poster PNG</span><span class="mono">300 DPI Raster</span></a>
      </div>

      <div class="dl-card">
        <div>
          <h3>6. Chapter 01 One-Page Visual Cheat Sheet (.PNG)</h3>
          <p>High-resolution 300-DPI PNG reference card for Chapter 01 (The Creator-to-Operator Paradigm &amp; RPPH Audit).</p>
        </div>
        <a href="./cheat-sheet-ch01.png" class="dl-btn" download><span>Download Cheat Sheet PNG</span><span class="mono">300 DPI Raster</span></a>
      </div>
    </div>
  </main>
</body>
</html>
"""


def build_404_page() -> str:
    """
    Builds `404.html` — Styled Creator Indigo fallback page with quick links back to
    `./index.html`, `./app/index.html`, `./studio/index.html`, `./atlas/index.html`, and `./downloads/index.html`.
    """
    portal_bar = build_ecosystem_portal_bar(".", "404")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Route Not Found (404) — The AI Content Creator &amp; Solopreneur Operating System</title>
  <link rel="manifest" href="./manifest.json" />
  <style>
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
    .wrap-404 {{
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 48px 24px;
    }}
    .card-404 {{
      max-width: 720px;
      width: 100%;
      background: #0F172A;
      border: 2px solid #4F46E5;
      border-radius: 18px;
      padding: 40px 32px;
      text-align: center;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.55);
    }}
    .code-badge {{
      display: inline-block;
      background: rgba(79, 70, 229, 0.25);
      border: 1px solid #818CF8;
      color: #A5B4FC;
      padding: 4px 12px;
      border-radius: 999px;
      font-size: 0.78rem;
      font-weight: 800;
      margin-bottom: 14px;
    }}
    .card-404 h1 {{
      font-size: 2.2rem;
      font-weight: 900;
      margin-bottom: 12px;
    }}
    .card-404 p {{
      color: #94A3B8;
      margin-bottom: 28px;
      font-size: 0.98rem;
    }}
    .route-links {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
    }}
    .route-btn {{
      background: #1E293B;
      border: 1px solid #334155;
      color: #FFFFFF;
      text-decoration: none;
      padding: 14px 16px;
      border-radius: 10px;
      font-weight: 800;
      font-size: 0.88rem;
      transition: border-color 0.15s, background 0.15s;
    }}
    .route-btn:hover {{
      border-color: #2DD4BF;
      background: rgba(13, 148, 136, 0.18);
    }}
    .route-btn.primary {{
      background: #4F46E5;
      border-color: #818CF8;
      grid-column: span 2;
    }}
    @media (max-width: 600px) {{
      .route-links {{ grid-template-columns: 1fr; }}
      .route-btn.primary {{ grid-column: span 1; }}
    }}
  </style>
</head>
<body>
{portal_bar}
  <main class="wrap-404">
    <div class="card-404">
      <span class="code-badge mono">HTTP 404 · STAGE-GATE NAVIGATION FALLBACK</span>
      <h1>Requested Studio Route Not Found</h1>
      <p>The URL you requested is outside the active static deployment routes. Select any verified destination in the AI Content Creator &amp; Solopreneur OS portal below:</p>
      <div class="route-links">
        <a href="./index.html" class="route-btn primary">&larr; Return to Main Conversion Portal &amp; RPPH Calculator (/)</a>
        <a href="./app/index.html" class="route-btn">Launch Creator OS Web App (/app/)</a>
        <a href="./studio/index.html" class="route-btn">Thumbnail &amp; Cover Studio (/studio/)</a>
        <a href="./atlas/index.html" class="route-btn">31-SVG Visual Shortcut Atlas (/atlas/)</a>
        <a href="./downloads/index.html" class="route-btn">Tier 0 Free Starter Kit Hub (/downloads/)</a>
      </div>
    </div>
  </main>
</body>
</html>
"""


def build_static_configs() -> dict:
    """
    Returns the static hosting, PWA, and SEO configuration files required in both
    `15-WEB-DEPLOYMENT/` and `docs/`.
    """
    manifest = {
        "name": "The AI Content Creator & Solopreneur Operating System",
        "short_name": "Creator OS v1.0",
        "description": "A Practical System to Research Validated Ideas, Script High-Retention Content, Repurpose Across Platforms, Automate Production, and Monetize Your Audience Without Burnout.",
        "start_url": "./index.html",
        "scope": "./",
        "display": "standalone",
        "background_color": "#0F172A",
        "theme_color": "#4F46E5",
        "orientation": "any",
        "icons": [
            {
                "src": "./assets/gumroad-tier3-flagship-bundle-cover.png",
                "sizes": "1280x720",
                "type": "image/png"
            },
            {
                "src": "./assets/ebook-cover-kdp-kindle.png",
                "sizes": "1600x2560",
                "type": "image/png"
            }
        ]
    }

    vercel_cfg = {
        "version": 2,
        "cleanUrls": True,
        "trailingSlash": False,
        "headers": [
            {
                "source": "/(.*)",
                "headers": [
                    {"key": "X-Content-Type-Options", "value": "nosniff"},
                    {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
                    {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"}
                ]
            },
            {
                "source": "/downloads/(.*)",
                "headers": [
                    {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}
                ]
            },
            {
                "source": "/assets/(.*)",
                "headers": [
                    {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}
                ]
            }
        ]
    }

    netlify_toml = """# Netlify Static Deployment Configuration — AI Creator & Solopreneur OS
[build]
  publish = "."
  command = "echo 'Static bundle pre-compiled — zero build step required'"

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    X-Frame-Options = "SAMEORIGIN"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/downloads/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[redirects]]
  from = "/webapp"
  to = "/app/index.html"
  status = 301

[[redirects]]
  from = "/customizer"
  to = "/studio/index.html"
  status = 301
"""

    headers_txt = """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin

/downloads/*
  Cache-Control: public, max-age=31536000, immutable

/assets/*
  Cache-Control: public, max-age=31536000, immutable
"""

    robots_txt = """User-agent: *
Allow: /

Sitemap: https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/sitemap.xml
"""

    sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/</loc>
    <lastmod>2026-10-23</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/app/index.html</loc>
    <lastmod>2026-10-23</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/studio/index.html</loc>
    <lastmod>2026-10-23</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/atlas/index.html</loc>
    <lastmod>2026-10-23</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/downloads/index.html</loc>
    <lastmod>2026-10-23</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
"""

    return {
        ".nojekyll": "",
        "manifest.json": json.dumps(manifest, indent=2),
        "vercel.json": json.dumps(vercel_cfg, indent=2),
        "netlify.toml": netlify_toml,
        "_headers": headers_txt,
        "robots.txt": robots_txt,
        "sitemap.xml": sitemap_xml,
    }


def build_deployment_runbook() -> str:
    """
    Returns `DEPLOYMENT-RUNBOOK.md` (>= 1,200 words) covering GitHub Pages, Vercel,
    Netlify, Cloudflare Pages, custom domains, and Gumroad/Lemon Squeezy checkout wiring.
    """
    return """# STATIC WEB DEPLOYMENT & CLOUD HOSTING RUNBOOK (PHASE 10)

**Product Title:** *The AI Content Creator & Solopreneur Operating System*  
**Subtitle:** *A Practical System to Research Validated Ideas, Script High-Retention Content, Repurpose Across Platforms, Automate Production, and Monetize Your Audience Without Burnout*  
**GitHub Repository:** `https://github.com/cryptXploit/AI-Creator-Solopreneur-OS`  
**Deployment Trees:** `15-WEB-DEPLOYMENT/` and `docs/` (100% Identical Production Mirrors)  
**Version:** `1.0.0` (Zero External CDN Dependencies · 100% Offline & Static Hosting Compatible)

---

## 1. ARCHITECTURE OVERVIEW & MULTI-ROUTE TOPOLOGY

Phase 10 packages the entire interactive web ecosystem of **Flagship Product #3** into a unified, self-contained static web portal. Every HTML route, SVG diagram, PNG commercial cover, and Tier 0 lead-magnet file uses clean relative paths (`./` and `../`) with **zero external HTTP/HTTPS scripts, stylesheets, or font CDNs**.

Because the complete production tree is generated inside `15-WEB-DEPLOYMENT/` and mirrored byte-for-byte into `docs/` at the repository root, the site runs identically in four environments:

1. **Local Offline File System (`file://` or `python -m http.server`):** Double-click `docs/index.html` or `15-WEB-DEPLOYMENT/index.html` on Windows, macOS, or Linux with zero internet connection.
2. **GitHub Pages Subpath Hosting (`https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/`):** Serves directly from the `/docs` folder on your `main` or `master` branch in 60 seconds.
3. **Vercel / Netlify / Cloudflare Pages Edge Hosting:** Instant 1-click Git integration with pre-configured `vercel.json`, `netlify.toml`, and `_headers` security and immutable cache policies.
4. **Custom Root Domain (`https://creator-os.yourdomain.com/`):** Works at any apex domain or subdomain without modifying a single asset path.

### Complete Production Route Map

| Route Path | File Location (`docs/` & `15-WEB-DEPLOYMENT/`) | Primary Function & Interactive Capabilities |
| :--- | :--- | :--- |
| `/` | `index.html` | **Flagship Conversion Sales Landing Page:** Live 5-Slider RPPH & Revenue Lift Calculator, 10-Chapter Curriculum Explorer, 62-Item Prompt & Script Index Preview, 10 Documented Case Studies, 5-Tier USD/BDT Pricing Matrix, and 12-Point Operator FAQ. |
| `/app/` | `app/index.html` (`app/creator-os-app.html`) | **Interactive SaaS-Lite Creator OS Web Companion Application:** 6 calculators (RPPH Simulator, 62-Item Prompt/Script Compiler, S.I.G.N.A.L. Outlier Scorer, 1-to-15 Waterfall & 4-Hr Batch Timer, Owned Audience + Pre-Sale Validator, B2B Sponsor Pricing & CEO Scorecard). Includes Tier 0 Free Diagnostic Mode + Pro Activation (`CREATOR-OS-PRO-2026`). |
| `/studio/` | `studio/index.html` (`studio/design-customizer-studio.html`) | **Interactive Cover, YouTube Thumbnail & Social Card Customizer Studio:** Live SVG + 300-DPI PNG design engine with 6 platform presets and 6 executive color palettes. |
| `/atlas/` | `atlas/index.html` | **Interactive Visual Shortcut Atlas & 31-SVG Explorer:** Browser for the Master 5-Stage Ecosystem Map Poster, all 10 One-Page Chapter Visual Cheat Sheets, and all 20 Chapter Mindmaps & Decision Flowcharts with chapter filters, search, full-screen zoom modal, and 1-click `.svg` + `.pdf` export. |
| `/downloads/` | `downloads/index.html` + 7 files | **Direct Tier 0 Free Audit Starter Kit Download Hub:** Self-hosted instant downloads for `tier0-free-sample-starter-kit.zip`, `tier0-free-sample-chapter01-and-audit.pdf`, `chapter-01-workbook.pdf`, `the-ai-creator-solopreneur-os-visual-shortcut-atlas.pdf`, `sheet1-creator-rpm-and-time-audit.csv`, `00-ECOSYSTEM-MASTER-MAP-POSTER.png`, and `cheat-sheet-ch01.png`. |
| `/404.html` | `404.html` | **Creator Indigo 404 Fallback Page:** Automatic fallback route guiding visitors back to `/`, `/app/`, `/studio/`, `/atlas/`, and `/downloads/`. |

---

## 2. 1-CLICK GITHUB PAGES ACTIVATION (`https://github.com/cryptXploit/AI-Creator-Solopreneur-OS`)

GitHub Pages natively supports deploying static portals directly from a `/docs` directory on the repository's default branch. Because `build_phase10_deployment.py` mirrors the entire portal into `docs/` and includes `.nojekyll` (which prevents Jekyll from ignoring prefix config files or altering asset paths), activation takes less than 60 seconds:

### Step-by-Step GitHub Pages Activation Checklist

1. Open your browser and navigate to **`https://github.com/cryptXploit/AI-Creator-Solopreneur-OS`**.
2. Click the **Settings** tab in the top repository navigation bar.
3. In the left sidebar under the **Code and automation** section, click **Pages**.
4. Under **Build and deployment** -> **Source**, select **Deploy from a branch**.
5. Under **Branch**:
   - Select **`main`** (or **`master`**, whichever you prefer—both branches are automatically synced via the repository's `post-commit` hook).
   - Change the folder dropdown next to the branch name from `/ (root)` to **`/docs`**.
   - Click **Save**.
6. Wait 45 to 90 seconds for the `pages-build-deployment` GitHub Action to complete, then refresh the **Settings -> Pages** screen.

### Expected Live GitHub Pages URLs

Once active, your live interactive ecosystem will be publicly accessible at:

- **Main Conversion Landing Page & RPPH Calculator:**  
  `https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/`
- **Interactive SaaS-Lite Creator OS Web App:**  
  `https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/app/`
- **Interactive Thumbnail, Book Cover & Carousel Customizer Studio:**  
  `https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/studio/`
- **31-SVG Visual Shortcut Atlas & Diagram Explorer:**  
  `https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/atlas/`
- **Tier 0 Free Audit Starter Kit Download Hub:**  
  `https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/downloads/`
- **Direct 1-Click Tier 0 Starter ZIP Download Link (for YouTube descriptions & social bios):**  
  `https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/downloads/tier0-free-sample-starter-kit.zip`

---

## 3. VERCEL 1-CLICK DEPLOYMENT PROTOCOL

Vercel provides global edge caching and instant SSL provisioning. A pre-validated `vercel.json` configuration file is included in both `15-WEB-DEPLOYMENT/vercel.json` and `docs/vercel.json`.

### Option A: Deploy via Vercel Dashboard (GitHub Integration)

1. Log in to **`https://vercel.com/new`** and click **Import Git Repository**.
2. Select **`cryptXploit/AI-Creator-Solopreneur-OS`**.
3. Under **Configure Project**:
   - **Framework Preset:** Select `Other` (Static HTML/JS).
   - **Root Directory:** Click **Edit** and set the path to `docs` (or `15-WEB-DEPLOYMENT`).
   - **Build Command:** Leave blank / override as off (all assets are pre-built).
   - **Output Directory:** Leave default (`.`).
4. Click **Deploy**. Every future `git commit` pushed to GitHub will automatically update your production Vercel deployment in under 15 seconds.

### Option B: Deploy via Vercel CLI

Run the following command locally from `DIGITAL-PUBLISHING-STUDIO/`:

```powershell
npx vercel --prod ./docs
```

---

## 4. NETLIFY & CLOUDFLARE PAGES DEPLOYMENT PROTOCOL

Both `15-WEB-DEPLOYMENT/` and `docs/` include `netlify.toml` and `_headers` to configure security headers (`X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy: strict-origin-when-cross-origin`) and 1-year immutable caching (`Cache-Control: public, max-age=31536000, immutable`) on `/downloads/*` and `/assets/*`.

### Deploying on Netlify

1. Log in to **`https://app.netlify.com/`** -> **Add new site** -> **Import an existing project** -> **GitHub**.
2. Choose **`cryptXploit/AI-Creator-Solopreneur-OS`**.
3. Set **Base directory** to `docs` (or `15-WEB-DEPLOYMENT`) and leave **Build command** empty.
4. Alternatively, for instant manual hosting without Git CI, open **`https://app.netlify.com/drop`** and drag-and-drop the `15-WEB-DEPLOYMENT` folder directly into your browser window.

### Deploying on Cloudflare Pages (Unlimited Free Bandwidth for PDF & ZIP Downloads)

Cloudflare Pages is especially advantageous for high-traffic creator funnels because it offers unlimited free bandwidth on static assets, meaning 100,000+ downloads of `tier0-free-sample-starter-kit.zip` (`2.26 MB`) incur `$0` in egress fees:

1. Log in to the **Cloudflare Dashboard** -> **Workers & Pages** -> **Create application** -> **Pages** -> **Connect to Git**.
2. Select **`cryptXploit/AI-Creator-Solopreneur-OS`**.
3. Set **Build command** to empty and **Build output directory** to `/docs` (or `/15-WEB-DEPLOYMENT`).
4. Click **Save and Deploy**. Cloudflare automatically parses `_headers` and `404.html`.

---

## 5. CONNECTING LIVE GUMROAD / LEMON SQUEEZY CHECKOUT URLS & CUSTOM DOMAINS

### Wiring Commercial Checkout Links on `index.html`

By default, the static web portal is wired for zero-broken-link self-hosted operation:
- **Tier 0 (`$0`):** Triggers an immediate browser download of `./downloads/tier0-free-sample-starter-kit.zip`.
- **Tier 3 (`$49 Flagship`):** Launches `./app/index.html` directly or routes to the Live Ecosystem Hub (`#live-ecosystem-hub`).
- **Tiers 1, 2, and 4:** Scroll smoothly to `#live-ecosystem-hub` where operators can test the live tools and download the starter files.

Once you publish your paid product listings on **Gumroad**, **Lemon Squeezy**, **Payhip**, or **Paddle** (following the step-by-step instructions in `10-MARKETING/GUMROAD-AND-MARKETPLACE-LAUNCH-RUNBOOK-BD.md`), you can replace the paid Tier CTA `href` attributes in `index.html` with your live checkout URLs:

- **Tier 1 (`$9.99` Digital / `$16.99` KDP Print):** Replace with your Amazon KDP / Draft2Digital / Gumroad Tier 1 link (upload `09-EXPORTS/HYBRID-BUNDLE/tier1-reader-edition.zip`).
- **Tier 2 (`$24` Interactive Workbook Edition):** Replace with your Gumroad Tier 2 product link (upload `09-EXPORTS/HYBRID-BUNDLE/tier2-implementation-pack.zip`).
- **Tier 3 (`$49` Complete Creator OS Flagship Bundle):** Replace with your Gumroad Tier 3 checkout link (upload `09-EXPORTS/HYBRID-BUNDLE/tier3-creator-os-complete-bundle.zip`).
- **Tier 4 (`$49/yr` or `$9/mo` Living Creator Vault Membership):** Replace with your Gumroad Membership link (upload `09-EXPORTS/HYBRID-BUNDLE/tier4-pro-living-system-and-vault.zip`).

### Custom Domain DNS Configuration (`CNAME` & Apex `A` Records)

To serve the portal on a custom domain (for example, `os.yourdomain.com`):

1. Add a `CNAME` record in your DNS provider (Cloudflare, Namecheap, Route53) pointing `os` to `cryptxploit.github.io` (for GitHub Pages) or `cname.vercel-dns.com` (for Vercel).
2. Add your custom domain inside **GitHub Settings -> Pages -> Custom domain** (or **Vercel -> Settings -> Domains**) and enable **Enforce HTTPS**.

---

## 6. LOCAL OFFLINE TESTING & QA VERIFICATION COMMANDS

To test the entire multi-route portal locally over HTTP on your Windows workstation before or after pushing to GitHub:

```powershell
# 1. Rebuild both 15-WEB-DEPLOYMENT/ and docs/
python build_phase10_deployment.py

# 2. Run the automated Phase 10 QA verifier (checks all routes, sizes, JSON/XML schemas, links, and banned words)
python verify_phase10_deployment.py

# 3. Serve the portal locally on http://localhost:8080
python -m http.server 8080 --directory docs
```

Open `http://localhost:8080` in Chrome, Edge, Brave, or Firefox to test PWA installation, offline `localStorage` persistence in `/app/`, SVG/PNG export in `/studio/`, and full-screen diagram inspection in `/atlas/`.
"""


def copy_assets_and_downloads(target_root: Path):
    """
    Copies the 7 required Tier 0 / Atlas files into `target_root/downloads/`
    and the 6 required cover/preview PNGs into `target_root/assets/`.
    """
    dl_dir = target_root / "downloads"
    assets_dir = target_root / "assets"
    dl_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    downloads_map = {
        "tier0-free-sample-chapter01-and-audit.pdf": STUDIO_ROOT / "09-EXPORTS" / "PDF" / "tier0-free-sample-chapter01-and-audit.pdf",
        "chapter-01-workbook.pdf": STUDIO_ROOT / "05-WORKBOOKS" / "chapter-01-workbook.pdf",
        "the-ai-creator-solopreneur-os-visual-shortcut-atlas.pdf": STUDIO_ROOT / "09-EXPORTS" / "PDF" / "the-ai-creator-solopreneur-os-visual-shortcut-atlas.pdf",
        "sheet1-creator-rpm-and-time-audit.csv": STUDIO_ROOT / "06-NOTION-TEMPLATES" / "Spreadsheets" / "sheet1-creator-rpm-and-time-audit.csv",
        "00-ECOSYSTEM-MASTER-MAP-POSTER.png": STUDIO_ROOT / "13-VISUAL-CHEAT-SHEETS" / "png" / "00-ECOSYSTEM-MASTER-MAP-POSTER.png",
        "cheat-sheet-ch01.png": STUDIO_ROOT / "13-VISUAL-CHEAT-SHEETS" / "png" / "cheat-sheet-ch01.png",
        "tier0-free-sample-starter-kit.zip": STUDIO_ROOT / "09-EXPORTS" / "HYBRID-BUNDLE" / "tier0-free-sample-starter-kit.zip",
    }

    for dest_name, src_path in downloads_map.items():
        if not src_path.exists():
            raise FileNotFoundError(f"Missing required download source file: {src_path}")
        shutil.copy2(src_path, dl_dir / dest_name)

    assets_map = {
        "ebook-cover-kdp-kindle.png": STUDIO_ROOT / "08-COVER-DESIGN" / "png" / "ebook-cover-kdp-kindle.png",
        "gumroad-tier0-free-audit-cover.png": STUDIO_ROOT / "08-COVER-DESIGN" / "png" / "gumroad-tier0-free-audit-cover.png",
        "gumroad-tier2-workbook-edition-cover.png": STUDIO_ROOT / "08-COVER-DESIGN" / "png" / "gumroad-tier2-workbook-edition-cover.png",
        "gumroad-tier3-flagship-bundle-cover.png": STUDIO_ROOT / "08-COVER-DESIGN" / "png" / "gumroad-tier3-flagship-bundle-cover.png",
        "gumroad-tier4-vault-membership-cover.png": STUDIO_ROOT / "08-COVER-DESIGN" / "png" / "gumroad-tier4-vault-membership-cover.png",
        "webapp-dashboard-preview.png": STUDIO_ROOT / "04-VISUAL-ASSETS" / "png" / "webapp-dashboard-preview.png",
    }

    for dest_name, src_path in assets_map.items():
        if not src_path.exists():
            raise FileNotFoundError(f"Missing required cover/preview asset: {src_path}")
        shutil.copy2(src_path, assets_dir / dest_name)


def populate_portal_tree(target_root: Path, pages: dict, configs: dict, runbook_md: str):
    """
    Writes all HTML routes, config files, runbook, and binary assets into `target_root`.
    """
    if target_root.exists():
        shutil.rmtree(target_root)

    (target_root / "app").mkdir(parents=True, exist_ok=True)
    (target_root / "studio").mkdir(parents=True, exist_ok=True)
    (target_root / "atlas").mkdir(parents=True, exist_ok=True)
    (target_root / "downloads").mkdir(parents=True, exist_ok=True)
    (target_root / "assets").mkdir(parents=True, exist_ok=True)

    # Write HTML pages
    (target_root / "index.html").write_text(pages["index.html"], encoding="utf-8")
    (target_root / "app" / "index.html").write_text(pages["app/index.html"], encoding="utf-8")
    (target_root / "app" / "creator-os-app.html").write_text(pages["app/index.html"], encoding="utf-8")
    (target_root / "studio" / "index.html").write_text(pages["studio/index.html"], encoding="utf-8")
    (target_root / "studio" / "design-customizer-studio.html").write_text(pages["studio/index.html"], encoding="utf-8")
    (target_root / "atlas" / "index.html").write_text(pages["atlas/index.html"], encoding="utf-8")
    (target_root / "downloads" / "index.html").write_text(pages["downloads/index.html"], encoding="utf-8")
    (target_root / "404.html").write_text(pages["404.html"], encoding="utf-8")

    # Write static hosting & PWA configs
    for cfg_name, cfg_content in configs.items():
        (target_root / cfg_name).write_text(cfg_content, encoding="utf-8")

    # Write Deployment Runbook
    (target_root / "DEPLOYMENT-RUNBOOK.md").write_text(runbook_md, encoding="utf-8")

    # Copy binary downloads and image assets
    copy_assets_and_downloads(target_root)


def main():
    print("=" * 80)
    print("PHASE 10 COMPILER: STATIC WEB DEPLOYMENT PORTAL (15-WEB-DEPLOYMENT/ & docs/)")
    print("=" * 80)

    pages = {
        "index.html": build_landing_page(),
        "app/index.html": build_web_app_page(),
        "studio/index.html": build_studio_page(),
        "atlas/index.html": build_atlas_page(),
        "downloads/index.html": build_downloads_hub_page(),
        "404.html": build_404_page(),
    }
    configs = build_static_configs()
    runbook_md = build_deployment_runbook()

    print("[1/2] Building 15-WEB-DEPLOYMENT/ production portal...")
    populate_portal_tree(DEPLOY_DIR, pages, configs, runbook_md)

    print("[2/2] Mirroring identical production portal to docs/ for GitHub Pages...")
    populate_portal_tree(DOCS_DIR, pages, configs, runbook_md)

    for rel in ["index.html", "app/index.html", "studio/index.html", "atlas/index.html", "downloads/index.html", "404.html", "DEPLOYMENT-RUNBOOK.md"]:
        sz = (DEPLOY_DIR / rel).stat().st_size
        print(f"  -> {rel:30s} : {sz:>10,d} bytes")

    print("=" * 80)
    print("PHASE 10 BUILD COMPLETE: 15-WEB-DEPLOYMENT/ and docs/ synchronized.")
    print("=" * 80)


if __name__ == "__main__":
    main()
