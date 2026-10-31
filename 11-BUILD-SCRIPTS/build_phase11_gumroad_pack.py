#!/usr/bin/env python3
"""
PHASE 11: GUMROAD HYBRID STOREFRONT MASTER PACK, 600x600 SQUARE THUMBNAILS,
UNIFIED VERSION/UPSELL COPY & AI IMAGE PROMPTS (`build_phase11_gumroad_pack.py`)

Product #3: The AI Content Creator & Solopreneur Operating System
Author & System Architect: OMAR SUNNY
Studio Root: e:/Ebook-Makaer/AI-Creator-Solopreneur-OS/DIGITAL-PUBLISHING-STUDIO/
"""

import html
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

import build_webapp

STUDIO_ROOT = Path(__file__).resolve().parent
BROWSER_BIN = build_webapp.find_browser_binary()

COVER_DIR = STUDIO_ROOT / "08-COVER-DESIGN"
COVER_SVG_DIR = COVER_DIR / "svg"
COVER_PNG_DIR = COVER_DIR / "png"
GUMROAD_DIR = STUDIO_ROOT / "10-MARKETING" / "Gumroad-Hybrid-Master-Setup"
GUMROAD_THUMBS_DIR = GUMROAD_DIR / "Thumbnails-and-Covers"
BUILD_SCRIPTS_DIR = STUDIO_ROOT / "11-BUILD-SCRIPTS"


def render_svg_to_exact_png(svg_path: Path, png_path: Path, width: int = 600, height: int = 600) -> None:
    """Renders an SVG file to an exact width x height PNG using Headless Edge/Chrome and Pillow."""
    png_path.parent.mkdir(parents=True, exist_ok=True)
    svg_raw = svg_path.read_text(encoding="utf-8")
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
    background: #090D16;
  }}
  svg {{
    display: block;
    width: {width}px;
    height: {height}px;
  }}
</style>
</head>
<body>
{svg_raw}
</body>
</html>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_html = Path(tmpdir) / "thumb.html"
        tmp_png = Path(tmpdir) / "screen.png"
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
            f"--window-size={width},{height + 160}",
            f"--screenshot={tmp_png}",
            tmp_html.as_uri(),
        ]
        subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if not tmp_png.is_file():
            raise RuntimeError(f"Failed to render PNG from {svg_path.name}")
        with Image.open(tmp_png) as img:
            cropped = img.crop((0, 0, width, height))
            cropped.save(png_path, format="PNG", compress_level=1)


def build_square_thumbnail_svg(
    top_pill_text: str,
    price_tag: str,
    accent_primary: str,
    accent_secondary: str,
    badge_bg: str,
    title_line1: str,
    title_line2: str,
    title_line3: str,
    highlight_bar_text: str,
    metrics: list[tuple[str, str]],
    footer_label: str,
) -> str:
    """Generates a valid XML 600x600 1:1 Square Gumroad Discover Thumbnail SVG crediting OMAR SUNNY."""
    esc = html.escape
    m1_val, m1_lbl = metrics[0]
    m2_val, m2_lbl = metrics[1]
    m3_val, m3_lbl = metrics[2]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#060911" />
      <stop offset="55%" stop-color="#0F172A" />
      <stop offset="100%" stop-color="#1E1B4B" />
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent_primary}" />
      <stop offset="100%" stop-color="{accent_secondary}" />
    </linearGradient>
    <radialGradient id="glowCenter" cx="50%" cy="38%" r="55%">
      <stop offset="0%" stop-color="{accent_primary}" stop-opacity="0.32" />
      <stop offset="100%" stop-color="#090D16" stop-opacity="0" />
    </radialGradient>
    <pattern id="gridPat" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#334155" stroke-width="0.6" stroke-opacity="0.35" />
    </pattern>
  </defs>

  <!-- Canvas Background -->
  <rect width="600" height="600" fill="url(#bgGrad)" />
  <rect width="600" height="600" fill="url(#gridPat)" />
  <circle cx="300" cy="240" r="260" fill="url(#glowCenter)" />

  <!-- Outer Precision Frame -->
  <rect x="16" y="16" width="568" height="568" rx="18" fill="none" stroke="url(#accentGrad)" stroke-width="3" />
  <rect x="24" y="24" width="552" height="552" rx="14" fill="none" stroke="#334155" stroke-width="1" />

  <!-- Top Pill & Price Badge Row -->
  <rect x="38" y="38" width="336" height="36" rx="8" fill="{badge_bg}" stroke="{accent_secondary}" stroke-width="1.5" />
  <text x="54" y="61" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="13" font-weight="900" letter-spacing="1.2">{esc(top_pill_text)}</text>

  <rect x="390" y="38" width="172" height="36" rx="8" fill="url(#accentGrad)" />
  <text x="476" y="61" text-anchor="middle" fill="#FFFFFF" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="900">{esc(price_tag)}</text>

  <!-- 3D Ecosystem Stack Icon Graphic -->
  <g transform="translate(42, 92)">
    <rect x="0" y="0" width="516" height="82" rx="12" fill="#090D16" fill-opacity="0.82" stroke="#334155" stroke-width="1.5" />
    <rect x="18" y="14" width="54" height="54" rx="10" fill="url(#accentGrad)" />
    <text x="45" y="47" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="20" font-weight="900">OS</text>
    <text x="88" y="34" fill="{accent_secondary}" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="800" letter-spacing="1.4">APEX DIGITAL SYSTEMS STUDIO · EDITION 2026</text>
    <text x="88" y="58" fill="#F8FAFC" font-family="Inter, Segoe UI, sans-serif" font-size="15.5" font-weight="800">5-Stage Content-to-Cash Operating System</text>
  </g>

  <!-- Main Center Display Typography -->
  <text x="300" y="226" text-anchor="middle" fill="#FFFFFF" font-family="Inter, Segoe UI, sans-serif" font-size="36" font-weight="900" letter-spacing="-0.8">{esc(title_line1)}</text>
  <text x="300" y="270" text-anchor="middle" fill="{accent_secondary}" font-family="Inter, Segoe UI, sans-serif" font-size="35" font-weight="900" letter-spacing="-0.8">{esc(title_line2)}</text>
  <text x="300" y="314" text-anchor="middle" fill="#E0E7FF" font-family="Inter, Segoe UI, sans-serif" font-size="33" font-weight="900" letter-spacing="-0.6">{esc(title_line3)}</text>

  <!-- Highlight Feature Banner -->
  <rect x="38" y="338" width="524" height="44" rx="10" fill="#1E293B" stroke="{accent_primary}" stroke-width="2" />
  <text x="300" y="365" text-anchor="middle" fill="#FFFFFF" font-family="JetBrains Mono, Consolas, monospace" font-size="13.5" font-weight="800" letter-spacing="0.5">{esc(highlight_bar_text)}</text>

  <!-- 3-Column Quantitative Telemetry Cards -->
  <g transform="translate(38, 398)">
    <rect x="0" y="0" width="166" height="92" rx="10" fill="#090D16" stroke="#334155" stroke-width="1.5" />
    <line x1="0" y1="0" x2="166" y2="0" stroke="{accent_secondary}" stroke-width="3" />
    <text x="83" y="42" text-anchor="middle" fill="#FFFFFF" font-family="JetBrains Mono, Consolas, monospace" font-size="22" font-weight="900">{esc(m1_val)}</text>
    <text x="83" y="68" text-anchor="middle" fill="#94A3B8" font-family="Inter, Segoe UI, sans-serif" font-size="11.5" font-weight="800" letter-spacing="0.8">{esc(m1_lbl)}</text>

    <rect x="179" y="0" width="166" height="92" rx="10" fill="#090D16" stroke="#334155" stroke-width="1.5" />
    <line x1="179" y1="0" x2="345" y2="0" stroke="{accent_primary}" stroke-width="3" />
    <text x="262" y="42" text-anchor="middle" fill="{accent_secondary}" font-family="JetBrains Mono, Consolas, monospace" font-size="22" font-weight="900">{esc(m2_val)}</text>
    <text x="262" y="68" text-anchor="middle" fill="#94A3B8" font-family="Inter, Segoe UI, sans-serif" font-size="11.5" font-weight="800" letter-spacing="0.8">{esc(m2_lbl)}</text>

    <rect x="358" y="0" width="166" height="92" rx="10" fill="#090D16" stroke="#334155" stroke-width="1.5" />
    <line x1="358" y1="0" x2="524" y2="0" stroke="{accent_secondary}" stroke-width="3" />
    <text x="441" y="42" text-anchor="middle" fill="#FFFFFF" font-family="JetBrains Mono, Consolas, monospace" font-size="22" font-weight="900">{esc(m3_val)}</text>
    <text x="441" y="68" text-anchor="middle" fill="#94A3B8" font-family="Inter, Segoe UI, sans-serif" font-size="11.5" font-weight="800" letter-spacing="0.8">{esc(m3_lbl)}</text>
  </g>

  <!-- Bottom Author Credit & System Signature -->
  <rect x="38" y="508" width="524" height="52" rx="10" fill="#060911" stroke="#1E293B" stroke-width="1.5" />
  <text x="300" y="530" text-anchor="middle" fill="#CBD5E1" font-family="Inter, Segoe UI, sans-serif" font-size="11.5" font-weight="700" letter-spacing="1.2">{esc(footer_label)}</text>
  <text x="300" y="550" text-anchor="middle" fill="{accent_secondary}" font-family="Inter, Segoe UI, sans-serif" font-size="13" font-weight="900" letter-spacing="3">SYSTEM ARCHITECT: BY OMAR SUNNY</text>
</svg>
"""


def generate_all_square_thumbnails() -> list[tuple[Path, Path]]:
    """Generates the 3 600x600 Square Gumroad Discover Thumbnails (SVG + PNG) and copies covers."""
    COVER_DIR.mkdir(parents=True, exist_ok=True)
    COVER_SVG_DIR.mkdir(parents=True, exist_ok=True)
    COVER_PNG_DIR.mkdir(parents=True, exist_ok=True)
    GUMROAD_THUMBS_DIR.mkdir(parents=True, exist_ok=True)

    specs = [
        (
            "11-gumroad-square-thumb-listing1-free-audit-600x600",
            dict(
                top_pill_text="$0 FREE STARTER AUDIT KIT",
                price_tag="FREE · $0+",
                accent_primary="#0D9488",
                accent_secondary="#2DD4BF",
                badge_bg="#042F2E",
                title_line1="7-DAY CREATOR",
                title_line2="RPPH & TIME-LEAK",
                title_line3="DIAGNOSTIC KIT",
                highlight_bar_text="RPPH + CONTENT TIME-LEAK AUDIT • WEB APP • CSV",
                metrics=[
                    ("57 PAGES", "CH 1 SAMPLE BOOK"),
                    ("48 FIELDS", "FILLABLE WORKBOOK"),
                    ("P01–P05", "AI PROMPT SUITE"),
                ],
                footer_label="INSTANT DOWNLOAD • PDF + FILLABLE WORKBOOK + WEB APP",
            ),
        ),
        (
            "12-gumroad-square-thumb-listing2-flagship-os-600x600",
            dict(
                top_pill_text="COMPLETE AI CREATOR OS",
                price_tag="$0 / $19 / $39 / $59",
                accent_primary="#4F46E5",
                accent_secondary="#FBBF24",
                badge_bg="#1E1B4B",
                title_line1="THE AI CREATOR &",
                title_line2="SOLOPRENEUR",
                title_line3="OPERATING SYSTEM",
                highlight_bar_text="50 AI PROMPTS • WEB APP • 8-TAB EXCEL • NOTION OS",
                metrics=[
                    ("340 PAGES", "10-CH MANUAL"),
                    ("1,420", "FILLABLE FIELDS"),
                    ("112 FILES", "FULL PRO SUITE"),
                ],
                footer_label="BOOK • WORKBOOKS • SAAS APP • EXCEL • WORD • PPTX • N8N",
            ),
        ),
        (
            "13-gumroad-square-thumb-listing3-vip-membership-600x600",
            dict(
                top_pill_text="VIP MONTHLY VAULT PASS",
                price_tag="$9/MO · $49/YR",
                accent_primary="#6366F1",
                accent_secondary="#2DD4BF",
                badge_bg="#1E1B4B",
                title_line1="LIVING CREATOR",
                title_line2="VAULT & AGENCY",
                title_line3="MEMBERSHIP PASS",
                highlight_bar_text="MONTHLY OUTLIER HOOKS & SPONSOR FUNNEL DROPS",
                metrics=[
                    ("156 FILES", "ALL TIER 3 + 4"),
                    ("MONTHLY", "OUTLIER DROPS"),
                    ("AGENCY", "COHORT RIGHTS"),
                ],
                footer_label="FULL FLAGSHIP OS + MONTHLY RECURRING INTELLIGENCE VAULT",
            ),
        ),
    ]

    outputs = []
    for base_name, kwargs in specs:
        svg_code = build_square_thumbnail_svg(**kwargs)
        svg_root_path = COVER_DIR / f"{base_name}.svg"
        png_root_path = COVER_DIR / f"{base_name}.png"
        svg_sub_path = COVER_SVG_DIR / f"{base_name}.svg"
        png_sub_path = COVER_PNG_DIR / f"{base_name}.png"
        thumb_copy_svg = GUMROAD_THUMBS_DIR / f"{base_name}.svg"
        thumb_copy_png = GUMROAD_THUMBS_DIR / f"{base_name}.png"

        svg_root_path.write_text(svg_code, encoding="utf-8")
        svg_sub_path.write_text(svg_code, encoding="utf-8")
        thumb_copy_svg.write_text(svg_code, encoding="utf-8")

        render_svg_to_exact_png(svg_root_path, png_root_path, 600, 600)
        shutil.copy2(png_root_path, png_sub_path)
        shutil.copy2(png_root_path, thumb_copy_png)
        outputs.append((svg_root_path, png_root_path))

    cover_copies = [
        (COVER_PNG_DIR / "gumroad-tier0-free-audit-cover.png", "03-gumroad-tier0-free-audit-cover.png"),
        (COVER_PNG_DIR / "gumroad-tier2-workbook-edition-cover.png", "04-gumroad-tier2-workbook-edition-cover.png"),
        (COVER_PNG_DIR / "gumroad-tier3-flagship-bundle-cover.png", "05-gumroad-tier3-flagship-bundle-cover.png"),
        (COVER_PNG_DIR / "gumroad-tier4-vault-membership-cover.png", "06-gumroad-tier4-vault-membership-cover.png"),
        (COVER_PNG_DIR / "ebook-cover-kdp-kindle.png", "01-ebook-cover-kdp-kindle.png"),
        (STUDIO_ROOT / "13-VISUAL-CHEAT-SHEETS" / "png" / "00-ECOSYSTEM-MASTER-MAP-POSTER.png", "00-ECOSYSTEM-MASTER-MAP-POSTER.png"),
    ]
    for src, dst_name in cover_copies:
        if src.is_file():
            shutil.copy2(src, GUMROAD_THUMBS_DIR / dst_name)
            shutil.copy2(src, GUMROAD_THUMBS_DIR / src.name)

    return outputs


def build_file00_bangla_master_guide() -> str:
    return r"""# সম্পূর্ণ গামরোড (Gumroad) হাইব্রিড আর্কিটেকচার, রিসার্চ এবং স্টেপ-বাই-স্টেপ সেটআপ গাইড (বাংলায়)

* **প্রজেক্ট:** *The AI Content Creator & Solopreneur Operating System (Flagship Product #3)*
* **লেখক ও সিস্টেম আর্কিটেক্ট:** `OMAR SUNNY`
* **স্টুডিও ডিরেক্টরি:** `10-MARKETING/Gumroad-Hybrid-Master-Setup/`

---

## ১. গভীর রিসার্চ ও চূড়ান্ত সিদ্ধান্ত: ১টি লিংকে সব টিয়ার (`$0 / $19 / $39 / $59`) + আলাদা মেম্বারশিপ প্রোডাক্ট কেন সবচেয়ে সেরা?

আপনার প্রশ্ন ছিল:
> *"একটা লিংকের মধ্যে (Same Link Product) 'Versions' ব্যবহার করে সব টিয়ার (`$0, $19, $39, $59`) রাখলে বেশি ভালো হবে, নাকি আলাদা টিয়ারগুলো সব আলাদা লিংক/প্রোডাক্ট হিসেবে আপলোড দেবো? আমি যদি `$0, $19, $39, $59` এই সব টিয়ার ১টা লিংকে রাখি এবং বাকি Membership প্রোডাক্ট আলাদা রেখে একসাথে লিংক করে পাবলিশ করি যাতে Gumroad বুঝতে পারে এগুলো একই প্রোডাক্ট এবং সেভাবে ইউজারকে সাজেস্ট করে—এটা কেমন হয়? যদি এটা বেস্ট হয় তাহলে লক করো।"*

### রিসার্চ ফলাফল: হ্যাঁ, আপনার এই **"২-লিংক ইউনিফায়েড হাইব্রিড আর্কিটেকচার" (১টি মেইন প্রোডাক্টে ৪টি ভার্সন `$0 / $19 / $39 / $59` + ১টি আলাদা রিকারিং মেম্বারশিপ প্রোডাক্ট `$9/mo` বা `$49/yr`)** ১০০% সেরা এবং সবচেয়ে বেশি কনভার্ট করা কৌশল! আমরা এটি **LOCK** করেছি।

কেন ৫টি আলাদা প্রোডাক্ট লিংকের চেয়ে **১টি মেইন লিংকে ৪টি ভার্সন (`$0, $19, $39, $59`) + ১টি মেম্বারশিপ লিংক** বেশি কার্যকর, তার ৫টি টেকনিক্যাল কারণ নিচে দেওয়া হলো:

1. **গামরোড ডিসকভার (Gumroad Discover) অ্যালগরিদম ও রিভিউ একত্রীকরণ:**
   * আপনি যদি `$0`, `$19`, `$39`, এবং `$59`-এর জন্য ৪টি আলাদা প্রোডাক্ট লিংক খোলেন, তবে আপনার ট্রাফিক, ডাউনলোড সংখ্যা এবং ৫-স্টার রিভিউ ৪ ভাগে ভাগ হয়ে যাবে।
   * কিন্তু যখন `$0 (Free Starter Kit)`, `$19 (Tier 1)`, `$39 (Tier 2)`, এবং `$59 (Tier 3 Flagship)` **একই প্রোডাক্ট লিংকে (`gumroad.com/l/ai-creator-solopreneur-os`) ৪টি Version হিসেবে** থাকে, তখন ফ্রি ডাউনলোডকারী ইউজাররা যে ৫-স্টার রিভিউ দেবে এবং ডাউনলোড কাউন্টার বাড়াবে (`1,500+ Downloads • 4.9★ Rating`), সেটি সরাসরি আপনার `$39` ও `$59` পেইড ভার্সনের সোশ্যাল প্রুফ হিসেবে কাজ করবে!
2. **ডিকয় প্রাইসিং সাইকোলজি (Decoy & Anchoring Psychology):**
   * ইউজার যখন ফ্রি অডিট কিট ডাউনলোড করতে আপনার লিংকে ঢুকবে, ডানপাশের বক্সেই সে এক নজরে ৪টি অপশন দেখবে:
     * **Version 0:** `Tier 0: Free 7-Day Creator Audit Starter Kit ($0)`
     * **Version 1:** `Tier 1: Core Digital Book & Print-Ready Edition ($19)`
     * **Version 2:** `Tier 2: Interactive Workbook, Visual Atlas & Planner Edition ($39)`
     * **Version 3:** `⭐ Tier 3: Complete Flagship AI Creator OS Bundle — MOST POPULAR ($59)`
   * এতে করে ফ্রি ট্রাফিকের ১০%–১৫% ইউজার ফ্রি ফাইল না নিয়ে সাথে সাথেই `$19` বা `$59` ভার্সন সিলেক্ট করে কিনে ফেলে।
3. **গামরোডের টেকনিক্যাল নিয়ম (কেন Membership আলাদা রাখতে হয়):**
   * গামরোডে একটি `Digital Product`-এর ভেতর ওয়ান-টাইম পেমেন্ট (`$0 / $19 / $39 / $59`) এবং মাসিক/বার্ষিক সাবস্ক্রিপশন (`$9/mo` বা `$49/yr`) একই প্রোডাক্টে রাখা যায় না। সাবস্ক্রিপশনের জন্য গামরোডে আলাদা `Membership` প্রোডাক্ট টাইপ সিলেক্ট করতে হয়।
   * তাই **Product #1 (`gumroad.com/l/ai-creator-solopreneur-os`)** হবে আপনার ৪-ভার্সনের মেইন প্রোডাক্ট (`$0 / $19 / $39 / $59`), এবং **Product #2 (`gumroad.com/l/ai-creator-vip-vault`)** হবে আপনার রিকারিং ভিআইপি মেম্বারশিপ (`$9/mo` বা `$49/yr`)।
4. **গামরোড কীভাবে বুঝবে এই দুটি একই ইকোসিস্টেমের প্রোডাক্ট? (৪টি সংযোগ সূত্র):**
   * **সূত্র ১ (Cross-Link Button in Description):** মেইন প্রোডাক্টের ডেসক্রিপশনের ভেতরে মেম্বারশিপ প্রোডাক্টের সরাসরি বাটন/লিংক (`https://[আপনার-ইউজারনেম].gumroad.com/l/ai-creator-vip-vault`) থাকবে, এবং মেম্বারশিপ প্রোডাক্টের ভেতরে মেইন প্রোডাক্টের লিংক থাকবে।
   * **সূত্র ২ (Same Category & Identical 5 Discover Tags):** দুটি প্রোডাক্টেই একই ক্যাটাগরি এবং একই ৫টি ট্যাগ দেওয়া থাকবে, ফলে গামরোডের `"More like this"` এবং ক্রিয়েটর প্রোফাইলে দুটি প্রোডাক্ট সবসময় পাশাপাশি সাজেস্ট করবে।
   * **সূত্র ৩ (Checkout Upsell Bridge):** গামরোডের `Checkout -> Upsells` অপশনে গিয়ে আপনি মেইন প্রোডাক্টের সাথে মেম্বারশিপ প্রোডাক্টকে যুক্ত করে দেবেন। ফলে কেউ মেইন প্রোডাক্ট চেকআউট করার সময় গামরোড নিজেই পপ-আপ দিয়ে আপনার মেম্বারশিপ প্রোডাক্ট সাজেস্ট করবে!
   * **সূত্র ৪ (Automated Workflow Emails):** কেউ `$0` ফ্রি ভার্সন ডাউনলোড করলেই গামরোডের `Workflows` অটোমেটিক ৭টি ইমেইল পাঠাবে, যেখানে `$59` ফ্ল্যাগশিপ বান্ডেল এবং `$49/yr` মেম্বারশিপ—দুটিরই ডিসকাউন্ট লিংক দেওয়া থাকবে।

---

## ২. মেইন প্রোডাক্ট লিস্টিং (`$0 / $19 / $39 / $59` একই লিংকে) — স্টেপ-বাই-স্টেপ ফিল্ড সেটআপ

গামরোডে **Products -> New product** ক্লিক করে নিচের তথ্যগুলো হুবহু কপি-পেস্ট করুন:

### ধাপ ২.১: বেসিক প্রোডাক্ট সেটিংস ও ইউআরএল স্লাগ (URL Slug)
* **Product Type:** `Digital product`
* **Name:** `The AI Content Creator & Solopreneur Operating System (By OMAR SUNNY)`
* **URL Slug (`gumroad.com/l/...`):** `ai-creator-solopreneur-os`
* **Base Price:** `$0`
  * *(নোট: যেহেতু প্রথম ভার্সনটি `$0` ফ্রি স্টার্টার কিট, তাই Base Price `$0` দিন এবং `"Allow customers to pay what they want"` অন করে Minimum: `$0`, Suggested: `$5` দিন। এরপর নিচে ৪টি ভার্সনে `+$0`, `+$19`, `+$39`, `+$59` বসাবেন।)*
* **Call to Action Button:** `I want this!`

### ধাপ ২.২: কভার ও ৬০০×৬০০ স্কয়ার থাম্বনেইল আপলোড
সবগুলো ছবি `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/` ফোল্ডারে রেডি আছে:
* **Thumbnail (`600 × 600 px` Square):** `12-gumroad-square-thumb-listing2-flagship-os-600x600.png`
* **Cover Carousel (`1280 × 720` / Widescreen — ৪টি স্লাইড ক্রমানুসারে আপলোড করুন):**
  1. `05-gumroad-tier3-flagship-bundle-cover.png` (মেইন ফ্ল্যাগশিপ কভার)
  2. `04-gumroad-tier2-workbook-edition-cover.png` (ওয়ার্কবুক ও ওয়েব অ্যাপ কভার)
  3. `03-gumroad-tier0-free-audit-cover.png` (ফ্রি স্টার্টার কিট কভার)
  4. `00-ECOSYSTEM-MASTER-MAP-POSTER.png` (৫-স্টেজ সিস্টেম আর্কিটেকচার পোস্টার)

### ধাপ ২.৩: প্রোডাক্ট সামারি (Product Summary), Additional Details এবং Refund Policy
* **Summary (ডানপাশের বক্সের জন্য কপি-পেস্ট করুন):**
  `Complete 5-Stage AI Content Creator & Solopreneur Operating System by OMAR SUNNY. Turn 1 weekly pillar script into 15+ platform-native assets in 4 hours/week. Includes 340-Page Manual, Fillable Workbooks, Offline SaaS Web App, 8-Tab Excel, 5-DB Notion OS, Word/PPTX Kits & n8n/Make Automations.`
* **Additional Details (Callout Attributes — `Add detail` ক্লিক করে ৮টি যোগ করুন):**
  1. `Author & Architect` : `OMAR SUNNY`
  2. `Edition` : `2026 Complete Multi-Format Release (v1.0)`
  3. `Book & Workbooks` : `340-Page Manual + 4 Fillable Workbooks (1,420 Fields)`
  4. `Interactive Software` : `100% Offline SaaS Web App + Design Customizer Studio`
  5. `Templates & Prompts` : `50 AI Workflow Prompts + 12 Sponsor Scripts + 31 SVGs`
  6. `Office & Databases` : `8-Tab Charted Excel + 5 Notion CSVs + 7 DOCX + 3 PPTX`
  7. `Automation Flows` : `5 Ready-to-Import n8n & Make.com JSON Blueprints`
  8. `Commercial License` : `DRM-Free Personal & Creator Business Operating License`
* **Refund Policy:**
  * **Refund Period:** `30-day money back guarantee`
  * **Fine Print (কপি-পেস্ট করুন):**
    `30-Day 100% Risk-Free Operator Guarantee by OMAR SUNNY: Test the 5-Stage Content-to-Cash Operating System, run the 7-Day RPPH Diagnostic Audit, and deploy the AI Prompts and Offline Web App. If the system does not save you at least 10+ production hours in your first 30 days, reply to your Gumroad receipt email for a full 100% refund—no hurdles.`

### ধাপ ২.৪: ৪টি ভার্সন (Versions) ও ফাইল ম্যাপ (`$0 / $19 / $39 / $59`)
`Product` ট্যাবের নিচে **Versions -> Add version** ক্লিক করে এই ৪টি ভার্সন তৈরি করুন এবং প্রতিটির `Content` ট্যাবে নির্দিষ্ট `.zip` ফাইলটি আপলোড করুন (`09-EXPORTS/HYBRID-BUNDLE/` ফোল্ডার থেকে):

| ভার্সন ক্রম | Version Name (কপি-পেস্ট) | Additional Amount (`$0` Base হলে) | কোন `.zip` ফাইল আপলোড দেবেন (`09-EXPORTS/HYBRID-BUNDLE/`) |
| :--- | :--- | :---: | :--- |
| **Version 1 (Free)** | `Tier 0: Free 7-Day Creator RPPH & Time-Leak Audit Starter Kit ($0)` | `+$0` | `tier0-free-sample-starter-kit.zip` |
| **Version 2 ($19)** | `Tier 1: Core 10-Chapter Book, KDP Print & EPUB 3.0 Edition ($19)` | `+$19` | `tier1-reader-edition.zip` |
| **Version 3 ($39)** | `Tier 2: Interactive Fillable Workbooks, 12-Page Visual Atlas & Web OS ($39)` | `+$39` | `tier2-implementation-pack.zip` |
| **Version 4 ($59)** | `⭐ Tier 3: Complete Flagship AI Creator OS Bundle — MOST POPULAR ($59)` | `+$59` | `tier3-creator-os-complete-bundle.zip` |

---

## ৩. মেম্বারশিপ প্রোডাক্ট লিস্টিং (`$9/mo` বা `$49/yr`) ও ক্রস-লিংকিং বাটন

দ্বিতীয় প্রোডাক্ট হিসেবে গামরোডে **New product -> Membership** সিলেক্ট করুন:
* **Name:** `VIP Living Creator & Solopreneur Vault Membership (Monthly Outlier Hooks, AI Prompts & Full Flagship OS — By OMAR SUNNY)`
* **URL Slug:** `ai-creator-vip-vault`
* **Thumbnail (`600 × 600 px`):** `13-gumroad-square-thumb-listing3-vip-membership-600x600.png`
* **Cover (`1280 × 720 px`):** `06-gumroad-tier4-vault-membership-cover.png`
* **Billing Options:**
  * **Monthly:** `$9 / month`
  * **Yearly (Default):** `$49 / year` *(Save 55% — 2 Months Value Price!)*
* **Uploaded Content:** `09-EXPORTS/HYBRID-BUNDLE/tier4-pro-living-system-and-vault.zip` (১৫৬টি ফাইল + Month 01 Living Vault Drop)।

---

## ৪. ক্যাটাগরি এবং ট্যাগস (Category & 5 Discover Tags)

দুটি প্রোডাক্টেই **Share -> Gumroad Discover** সেকশনে হুবহু একই ক্যাটাগরি এবং ট্যাগ ব্যবহার করবেন যাতে গামরোড দুটিকে একই সিরিজ হিসেবে চিনে রাখে:

* **Primary Category:** `Business & Money > Marketing & Sales` *(অথবা `Education > How-To`)*
* **5 Exact Discover Tags (দুটি লিস্টিংয়েই একই দিন):**
  1. `content creation`
  2. `solopreneur`
  3. `notion template`
  4. `ai prompts`
  5. `youtube automation`

---

## ৫. কানেকশন, চেকআউট আপসেল, অটো ইমেইল ও দ্রুত ইউজার আনার কমপ্লিট মার্কেটিং রোডম্যাপ

1. **গামরোড প্রোফাইল ও কাস্টম সেকশন সাজানো (Profile Connection):** গামরোডের `Profile` ট্যাবে গিয়ে `The AI Content Creator & Solopreneur Operating System (By OMAR SUNNY)` নামে একটি সেকশন খুলে সেখানে আপনার মেইন ৪-ভার্সন প্রোডাক্ট এবং ভিআইপি মেম্বারশিপ পাশাপাশি পিন করুন।
2. **চেকআউট আপসেল (Checkout -> Upsells):**
   * **Upsell #1:** কেউ `$0`, `$19`, বা `$39` সিলেক্ট করলে তাকে পপ-আপে `⭐ Tier 3: Complete Flagship AI Creator OS Bundle ($59)`-এ আপগ্রেড করার অফার দিন।
   * **Upsell #2:** কেউ মেইন প্রোডাক্ট কিনলে তাকে ১-ক্লিকে `$10 OFF`-এ (`$39/yr`) `VIP Living Creator Vault Yearly Pass` কার্টে যোগ করার অফার দিন।
3. **অটোমেটেড ইমেইল সিকোয়েন্স (Workflows):** গামরোডের `Workflows` ট্যাবে গিয়ে ফ্রি ডাউনলোডারদের জন্য ৭টি অটোমেটেড ইমেইল সেট করুন (`0 hr`, `24 hr`, `72 hr`, `120 hr`, `168 hr`, `216 hr`, `264 hr`)।
4. **সোশ্যাল মিডিয়া ও দ্রুত ট্রাফিক হ্যাক:** ইউটিউব, লিংকডইন, ফেসবুক ও এক্স-এ ফ্রি ৭-দিনের অডিট কিট এবং লাইভ ক্যালকুলেটরের লিংক শেয়ার করুন, `LAUNCH20` কুপন কোড (`?code=LAUNCH20`) ব্যবহার করুন এবং `30%` গামরোড অ্যাফিলিয়েট প্রোগ্রাম চালু করুন।
"""


def build_file01_listing1_free() -> str:
    return r"""# GUMROAD LISTING 1 — FREE 7-DAY CREATOR AUDIT STARTER KIT (EXACT INPUT FIELDS)

* **Product Title:** *The AI Content Creator & Solopreneur Operating System*
* **System Architect & Author Credit:** `OMAR SUNNY`
* **Usage Mode:** Use this guide if you publish **Tier 0 (`$0+`) as a Standalone Free Lead Magnet Listing** (`gumroad.com/l/ai-creator-audit-kit`) OR copy the **Version 0** block directly into your unified 4-version listing (`02-LISTING-2-FLAGSHIP-3-VERSION-PRODUCT-EXACT-FIELDS.md`).

---

## 1. EXACT PRODUCT CREATION & PRICING SETTINGS

| Gumroad Input Field | Exact Copy-Paste Value |
| :--- | :--- |
| **Product Type** | `Digital product` |
| **Product Name** | `Free 7-Day Creator RPPH, Content Time-Leak & Monetization Audit (AI Creator OS Starter Kit — By OMAR SUNNY)` |
| **URL Slug (`gumroad.com/l/...`)** | `ai-creator-audit-kit` |
| **Base Price** | `$0` |
| **Pay What You Want Toggle** | `ON` (Checked: *Allow customers to pay what they want*) |
| **Minimum Amount** | `$0` |
| **Suggested Amount** | `$5` |
| **Call to Action Button** | `Download` (or `I want this!`) |
| **Square Thumbnail (`600 × 600 px`)** | `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/11-gumroad-square-thumb-listing1-free-audit-600x600.png` |
| **Product Cover Banner (`1280 × 720` / `1600 × 1000`)** | `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/03-gumroad-tier0-free-audit-cover.png` |
| **Secondary Cover Slide 2** | `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/00-ECOSYSTEM-MASTER-MAP-POSTER.png` |

---

## 2. SUMMARY, ADDITIONAL DETAILS & REFUND POLICY

### 2.1 Summary Field (Right Sidebar Callout Box)
```text
Free 7-Day Creator RPPH & Time-Leak Diagnostic Kit by OMAR SUNNY. Includes the 57-Page Chapter 1 Sample & Audit Manual (PDF), 13-Page Fillable Chapter 1 Action Workbook (48 Fields), 25-Row RPM & Time-Leak Audit CSV, 5 Core AI Workflow Prompts (P01-P05), and the Master 5-Stage Ecosystem Map Poster.
```

### 2.2 Additional Details (`Attribute : Value` Pairs)
Click **Add detail** 5 times and paste these exact pairs:

| Attribute (Left Box) | Value (Right Box) |
| :--- | :--- |
| `Author` | `OMAR SUNNY` |
| `Edition` | `2026 Starter Kit (v1.0)` |
| `Format` | `PDF + Fillable Workbook + Interactive Web App + CSV` |
| `License` | `Personal & Solopreneur Creator Use` |
| `Instant Access` | `5 Self-Contained Files + Live Web App Access` |

### 2.3 Refund Policy Setting
* **Selection:** `30-day money back guarantee`
* **Fine Print:**
  `100% Free Starter Kit by OMAR SUNNY. If you leave an optional supporter tip at checkout, it is backed by a full 30-day no-questions-asked refund policy.`

---

## 3. FULL RICH-TEXT PRODUCT DESCRIPTION (COPY-PASTE READY)

Paste the following complete copy into the Gumroad **Description** editor:

```markdown
### Stop Running on the 35-Hour Content Burnout Treadmill. Audit Your Revenue Per Production Hour (RPPH) in 45 Minutes.

**Architected by OMAR SUNNY · Apex Digital Systems Studio**

Most solo creators, YouTubers, newsletter operators, and LinkedIn/X educators do not have a work-ethic problem—they have a **unit-economics and production-architecture problem**. They spend 30 to 40 hours every week researching random topics, writing from scratch, editing manually, and posting daily for $6 to $14 per production hour.

This **100% Free Starter & Diagnostic Audit Kit (Tier 0)** gives you the exact quantitative instruments from **Chapter 1** of *The AI Content Creator & Solopreneur Operating System* by **OMAR SUNNY** so you can audit your baseline RPPH, eliminate non-monetized time leaks, and map your 4-hour weekly batch production sprint today.

---

### What You Get Immediately Inside This Free Starter Kit (.ZIP)

1. **57-Page Sample Manual & Chapter 1 Vertical Slice (`tier0-free-sample-chapter01-and-audit.pdf`):**
   * Complete Front Matter + Full 9,704-word Chapter 1 (*The Creator-to-Operator Paradigm & The 5-Stage Content-to-Cash Operating System*).
   * The mathematical derivation of **Revenue Per Production Hour ($RPPH$)**, **High-Value Production Ratio ($HVPR \ge 70\%$)**, and **Monthly Time-Leak Opportunity Cost**.
   * Full quantitative case study teardown: how B2B creator Marcus Vance compressed his weekly production from 38.5 hours to 5.5 hours while scaling from $1,310/mo ($7.86/hr RPPH) to $14,850/mo ($623/hr RPPH).
2. **13-Page Fillable Chapter 1 Action Workbook (`chapter-01-workbook.pdf`):**
   * Programmatically injected with **48 interactive AcroForm text inputs and checkboxes**—type directly inside Adobe Reader, Chrome, Edge, macOS Preview, or iPad GoodNotes without printing.
   * Complete your 7-Day Content Time-Leak Log, Task Elimination Matrix, and 90-Day Operator RPPH Target Sheet.
3. **Creator RPM & Time-Leak Baseline Audit Tracker (`sheet1-creator-rpm-and-time-audit.csv`):**
   * 25-row pre-structured spreadsheet ready for instant import into Notion, Microsoft Excel, or Google Sheets.
4. **Master 5-Stage Content-to-Cash Ecosystem Map Poster (`00-ECOSYSTEM-MASTER-MAP-POSTER.png` & `cheat-sheet-ch01.png`):**
   * High-resolution 300-DPI visual architecture poster mapping all 5 stages (`S.I.G.N.A.L. Validation -> C.L.I.P. Packaging -> H.E.A.R.T. Scripting -> 1-to-15 Waterfall -> 4-Tier Monetization & B2B Sponsorships`).
5. **5 Copy-Paste AI Workflow Prompts (`P01–P05`) + 2 Emergency Sponsor Negotiation Scripts (`S01–S02`):**
   * `P01`: 7-Day Creator Time-Leak & RPPH Diagnostic Auditor
   * `P02`: Pillar Format & Primary Platform Selection Architect
   * `P03`: Content-to-Cash Monetization Bridge Mapper
   * `P04`: Weekly 6-Hour Production Sprint Block Scheduler
   * `P05`: 90-Day Creator-CEO Bottleneck & Margin Turnaround Planner

---

### Who This Free Starter Kit Is Engineered For

* **YouTube & Video Creators (On-Camera or Faceless):** Tired of spending 20+ hours scripting and editing a single video that stalls at 400 views or earns $18 in AdSense revenue.
* **LinkedIn, X & Newsletter Writers:** Posting daily on social platforms without a deterministic Rented-to-Owned email bridge or a 4-tier digital product value ladder.
* **Solopreneurs, Coaches & Technical Educators:** Who want to turn 1 weekly deep-dive Pillar Script into 15 platform-native assets in a single 4-hour batch sprint.

---

### Ready for the Complete 10-Chapter Flagship OS or VIP Monthly Vault?

If you want all 10 Chapters (91,775 words), all 50 AI Workflow Prompts (`P01–P50`), all 12 Emergency Scripts (`S01–S12`), the full Pro Offline SaaS Web Companion App (`CREATOR-OS-PRO-2026`), the 8-Tab Charted Excel Command Center, the 5-Database Notion Creator OS, 7 Editable Word SOPs, 3 PowerPoint Pitch Decks, and 5 n8n/Make JSON Automations:

* **[👉 Click Here to Get the Complete Flagship AI Creator & Solopreneur OS ($19 / $39 / $59 Editions)](https://gumroad.com/l/ai-creator-solopreneur-os)**
* **[👉 Click Here to Join the VIP Living Creator Vault Membership ($9/mo or $49/yr — Includes Full Flagship OS + Monthly Outlier Drops)](https://gumroad.com/l/ai-creator-vip-vault)**

---

### Technical Specifications
* **System Architect & Author:** OMAR SUNNY (`BY OMAR SUNNY`)
* **Delivery Format:** Instant DRM-Free `.ZIP` Download (`2.26 MB`) + Direct Individual Files
* **Compatibility:** Windows, macOS, Linux, iPadOS, iOS, Android (100% Offline-Ready)
```

---

## 4. CONTENT TAB SETUP, FILE DELIVERY & WELCOME NOTE

1. Click the **Content** tab at the top of the Gumroad editor.
2. Upload **`09-EXPORTS/HYBRID-BUNDLE/tier0-free-sample-starter-kit.zip`** AND the individual files from `15-WEB-DEPLOYMENT/downloads/` (`tier0-free-sample-chapter01-and-audit.pdf`, `chapter-01-workbook.pdf`, `sheet1-creator-rpm-and-time-audit.csv`, `00-ECOSYSTEM-MASTER-MAP-POSTER.png`, `cheat-sheet-ch01.png`) so mobile and desktop buyers can view each asset directly in Gumroad's built-in reader or download the single ZIP archive.
3. Above the file list in the Gumroad Content Editor, paste this **Welcome & Upgrade Callout Note**:

```markdown
### Welcome to The AI Content Creator & Solopreneur OS (Starter Kit) — By OMAR SUNNY

Thank you for downloading the **7-Day Creator RPPH & Time-Leak Diagnostic Audit Kit**!

**Your 3-Step Quick-Start Protocol (Next 30 Minutes):**
1. **Open `chapter-01-workbook.pdf`** on your computer or tablet and fill in Table 1.1 (your 7-day production hours across ideation, scripting, recording, editing, and admin) and Table 1.2 (your current monthly creator revenue streams).
2. **Run Prompt `P01` (`7-Day Creator Time-Leak & RPPH Diagnostic Auditor`)** inside Claude, ChatGPT, or Gemini using the copy-paste block inside `tier0-free-sample-chapter01-and-audit.pdf`.
3. **Review `00-ECOSYSTEM-MASTER-MAP-POSTER.png`** to identify which of the 5 Stage Gates (`Validate`, `Script`, `Multiply`, `Convert`, `Monetize`) is currently capping your growth.

---

#### Exclusive Reader Upgrade Offer: Save 15% on the Complete Flagship Creator OS
When you are ready to install the entire 10-Chapter Operating Manual, the Full Pro Offline Web App (`CREATOR-OS-PRO-2026`), the 8-Tab Charted Excel Command Center, the 5-Database Notion OS, and all 50 AI Prompts:
* **Upgrade to the Flagship Bundle here:** `https://gumroad.com/l/ai-creator-solopreneur-os?code=SUBSCRIBER15` (Use code **`SUBSCRIBER15`** at checkout for **15% OFF**).
* **Or join the VIP Living Creator Vault ($9/mo or $49/yr):** `https://gumroad.com/l/ai-creator-vip-vault`

— **OMAR SUNNY**, System Architect
```

---

## 5. SHARE, GUMROAD DISCOVER & SOCIAL PROMOTION COPY

* **Category:** `Business & Money > Marketing & Sales` (or `Education > How-To`)
* **5 Exact Discover Tags:** `content creation`, `solopreneur`, `notion template`, `ai prompts`, `youtube automation`
* **Display Product Rating:** `ON`
* **Show on Gumroad Profile:** `ON`

### Copy-Paste Social Bio & YouTube Description Callout for Listing 1
```text
📊 Free 7-Day Creator RPPH & Content Time-Leak Audit Kit (By OMAR SUNNY) — Download the 57-page Chapter 1 Manual, Fillable 48-Field Workbook, RPM Audit CSV & 5 AI Prompts for $0:
👉 https://gumroad.com/l/ai-creator-audit-kit?wanted=true
```

---

## 6. COMPLETE RECEIPT EMAIL CUSTOMIZATION & POST-DOWNLOAD UPGRADE PATH

Inside Gumroad **Settings -> Customizing Checkout & Receipt**, paste the following custom receipt message for **Listing 1 (`ai-creator-audit-kit`)** so every free subscriber sees a clear 3-step onboarding checklist and a direct 15% upgrade voucher inside their email receipt:

```markdown
Thank you for downloading the Free 7-Day Creator RPPH & Content Time-Leak Audit Kit by OMAR SUNNY!

1. Click the "View content" button in this email to download `tier0-free-sample-starter-kit.zip` (or open the individual PDFs and CSV directly on your device).
2. Complete `chapter-01-workbook.pdf` (48 interactive fillable fields) to benchmark your current Revenue Per Production Hour (RPPH) and High-Value Production Ratio (HVPR).
3. Run AI Prompt P01 inside Claude, ChatGPT, or Gemini to generate your 7-day time-leak elimination schedule.
4. When you are ready to install the complete 10-Chapter Manual, all 50 AI Workflow Prompts (P01-P50), 12 Emergency Sponsor Scripts (S01-S12), the Full Pro Offline SaaS Web App (Key: CREATOR-OS-PRO-2026), the 8-Tab Charted Excel Command Center, and the 5-Database Notion Creator OS, claim your 15% reader discount using code SUBSCRIBER15 at:
https://gumroad.com/l/ai-creator-solopreneur-os?code=SUBSCRIBER15

Please leave a 5-star (★★★★★) rating on Gumroad after you run your audit—it helps fellow solo creators discover this free diagnostic kit!
— OMAR SUNNY, System Architect
```
"""


def build_file02_listing2_flagship() -> str:
    return r"""# GUMROAD LISTING 2 — THE FLAGSHIP MULTI-VERSION PRODUCT SETUP (`$0 / $19 / $39 / $59` UNIFIED LINK + `$19 / $39 / $59` PAID MATRIX)

* **Product Title:** *The AI Content Creator & Solopreneur Operating System (By OMAR SUNNY)*
* **System Architect & Author Credit:** `OMAR SUNNY`
* **Canonical URL Slug:** `gumroad.com/l/ai-creator-solopreneur-os`

---

## 1. LOCKED PRIMARY ARCHITECTURE: 4 VERSIONS ON 1 UNIFIED LINK (`$0 / $19 / $39 / $59`) VS. 3 PAID VERSIONS (`$19 / $39 / $59`)

You have two ways to configure the price tiers on `gumroad.com/l/ai-creator-solopreneur-os`:

* **Configuration A (LOCKED RECOMMENDED — All 4 Tiers `$0 / $19 / $39 / $59` on 1 Single Link):**
  * **Base Price:** `$0` (with `"Allow customers to pay what they want"` ON: Minimum `$0`, Suggested `$5`).
  * **Version 0 (Free Starter Kit):** Additional amount `+$0` (Total = `$0`).
  * **Version 1 (Tier 1 Core Book & Print Edition):** Additional amount `+$19` (Total = `$19`).
  * **Version 2 (Tier 2 Interactive Workbook, Visual Atlas & Web OS):** Additional amount `+$39` (Total = `$39`).
  * **Version 3 (⭐ Tier 3 Complete Flagship AI Creator OS Bundle):** Additional amount `+$59` (Total = `$59`).
  * *Why Configuration A Wins:* Every single free download (`$0`) and 5-star review accumulates on this exact URL, boosting Gumroad Discover rankings and social proof for the `$19`, `$39`, and `$59` versions!
* **Configuration B (Alternative — Paid-Only 3 Versions `$19 / $39 / $59` when Listing 1 is kept separate):**
  * **Base Price:** `$19`
  * **Version 1 (Tier 1 Core Book):** Additional amount `+$0` (Total = `$19`, or `$19` in the `$19/$29/$49` matrix).
  * **Version 2 (Tier 2 Workbook & Atlas):** Additional amount `+$20` (Total = `$39`, or `+$10` for `$29`).
  * **Version 3 (⭐ Tier 3 Flagship Bundle):** Additional amount `+$40` (Total = `$59`, or `+$30` for `$49`).

---

## 2. EXACT PRODUCT HEADER, COVERS, SUMMARY & ATTRIBUTES

| Gumroad Input Field | Exact Copy-Paste Value |
| :--- | :--- |
| **Product Type** | `Digital product` |
| **Name Field** | `The AI Content Creator & Solopreneur Operating System (By OMAR SUNNY)` |
| **URL Slug (`gumroad.com/l/...`)** | `ai-creator-solopreneur-os` |
| **Base Price Field** | `$0` (for 4-Version `$0/$19/$39/$59` setup) OR `$19` (for 3-Version `$19/$39/$59` setup) |
| **Purchasing Power Parity (PPP)** | `ON` -> Maximum Discount: `40%` |
| **Call to Action Button** | `I want this!` |
| **Square Thumbnail (`600 × 600 px`)** | `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/12-gumroad-square-thumb-listing2-flagship-os-600x600.png` |
| **Cover Slide 1 (Hero `1600 × 1000`)** | `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/05-gumroad-tier3-flagship-bundle-cover.png` |
| **Cover Slide 2 (Workbook & Web App)** | `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/04-gumroad-tier2-workbook-edition-cover.png` |
| **Cover Slide 3 (System Map Poster)** | `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/00-ECOSYSTEM-MASTER-MAP-POSTER.png` |
| **Cover Slide 4 (Free Starter Kit)** | `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/03-gumroad-tier0-free-audit-cover.png` |

### 2.1 Summary Field (Right Sidebar Callout)
```text
The Complete 5-Stage AI Content Creator & Solopreneur Operating System by OMAR SUNNY. Turn 1 weekly pillar script into 15+ platform-native assets in 4 hours/week. Includes 340-Page Manual, 4 Fillable Workbooks, Offline SaaS Web App, 8-Tab Charted Excel, 5-DB Notion OS, Word/PPTX Kits & n8n/Make Automations.
```

### 2.2 8 Additional Details (`Attribute : Value` Pairs)

| Attribute | Value |
| :--- | :--- |
| `System Architect` | `OMAR SUNNY` |
| `Release Version` | `2026 Flagship Edition v1.0 (112 Production Files)` |
| `Manual & eBook` | `340-Page Color PDF + 314-Page 6x9 Print PDF + EPUB 3.0 (91,775 Words)` |
| `Fillable Workbooks` | `US Letter + ISO A4 + 11x8.5 iPad Landscape (1,420 AcroForm Fields)` |
| `Web Applications` | `Offline SaaS Companion App (Key: CREATOR-OS-PRO-2026) + Cover Studio` |
| `Prompts & Diagrams` | `50 AI Prompts (P01-P50) + 12 Scripts (S01-S12) + 31 Vector SVGs` |
| `Office & Spreadsheets` | `8-Tab Charted Excel + 5 Notion CSVs + 7 Word DOCX + 3 PowerPoint Decks` |
| `Automation Workflows` | `5 Importable n8n & Make.com JSON Blueprints + Setup Guide` |

### 2.3 Refund Policy Setting
* **Refund Period:** `30-day money back guarantee`
* **Fine Print:**
  `30-Day 100% Risk-Free Operator Guarantee by OMAR SUNNY: Deploy the 5-Stage Operating System, run the Offline Web App, and test the 50 AI Workflow Prompts for 30 days. If the system does not save you at least 10+ hours of weekly production work or clarify your monetization roadmap, reply to your receipt email within 30 days for a complete 100% refund.`

---

## 3. FULL RICH-TEXT PRODUCT DESCRIPTION WITH MEMBERSHIP LINK (COPY-PASTE READY)

```markdown
### Replace the 35-Hour Content Treadmill With a Deterministic 4-Hour Weekly Operating System.

**System Architect & Author: OMAR SUNNY · Apex Digital Systems Studio**

Most creators fail to build a sustainable one-person media business because they treat content creation as daily guesswork. They brainstorm unvalidated ideas, write scripts from scratch without a retention architecture, manually reformat posts across five platforms, and rely on low-margin AdSense pennies instead of owned email funnels, digital product value ladders, and outcome-based B2B sponsorships.

***The AI Content Creator & Solopreneur Operating System*** (authored and engineered by **OMAR SUNNY**) is a complete, quantitative media operating manual, interactive software suite, fillable workbook system, Notion & Excel command center, editable Office kit, and automation pack.

> **The Quantified Operator Promise:** Turn **1 Weekly Validated Pillar Script** into **15+ Platform-Native Assets** and build predictable **Digital Product + Outcome Sponsorship Revenue** in **Under 6 Hours Per Week**.

---

### The 5-Stage Content-to-Cash Operating Engine Inside

1. **STAGE 1 — VALIDATE (`S.I.G.N.A.L.` · Chapters 1–3):** Audit your baseline Revenue Per Production Hour ($RPPH$), lock a high-margin `P.A.I.D.` niche moat ($NMPI \ge 75/100$), and mine peer-channel outlier concepts with proven view velocity ($M_{\text{outlier}} \ge 2.5\times$) before writing a single word.
2. **STAGE 2 — SCRIPT (`C.L.I.P.` + `H.E.A.R.T.` · Chapters 4–5):** Engineer Package-First Titles and 3-Word Thumbnails ($CTR \ge 7.5\%$), write 3-second `C.L.I.P.` hooks ($30\text{s Hold} \ge 70\%$), and calibrate your 5-Parameter Voice DNA so AI drafts sound 100% human.
3. **STAGE 3 — MULTIPLY (`1-to-15 Waterfall` · Chapters 6–7):** Execute the 4-Hour Mon–Thu Batch Production Sprint to turn 1 Pillar Script into 5 vertical Shorts/Reels, 4 LinkedIn/X posts, 3 visual carousels, and 2 newsletter issues.
4. **STAGE 4 — CONVERT (`Owned Audience Bridge` · Chapter 8):** Route rented social views to a $45\%+$ conversion landing page using a 5-Minute Utility Lead Magnet, 3-tag intent survey, and 5-day automated welcome sequence ($V_{\text{sub}} \ge \$3.50$).
5. **STAGE 5 — MONETIZE (`4-Tier Value Ladder & B2B Sponsors` · Chapters 9–10):** Pre-sell your digital product via the 14-Day Validation Sprint ($+45\%$ checkout AOV with order bumps) and close outcome-priced B2B sponsorship retainers ($R_{\text{sponsor}}$ formula + $+30\%/\text{mo}$ whitelisting fee).

---

### Complete 10-Chapter Curriculum Breakdown (91,775 Words)

* **Chapter 01 (`9,704 words`):** The Creator-to-Operator Paradigm & The 5-Stage Content-to-Cash OS — $RPPH$, $HVPR$, and 7-Day Time-Leak Audit.
* **Chapter 02 (`8,120 words`):** Profitable Niche Positioning, Audience Avatar & Authority Moat (`P.A.I.D.`) — Niche Monetization Potential Index ($NMPI$) and Category-of-One positioning.
* **Chapter 03 (`8,045 words`):** The AI Outlier Idea Engine & Predictive Topic Validation (`S.I.G.N.A.L.`) — Peer-channel median mining, Outlier Multiplier ($M_{\text{outlier}} \ge 2.5\times$), and 100-Idea Vault.
* **Chapter 04 (`8,310 words`):** Irresistible Packaging: Title, Thumbnail & 3-Second Hook Engineering (`C.L.I.P.`) — Curiosity-delta titles, 3-word visual anchors, and Early Retention Index ($ERI$).
* **Chapter 05 (`7,980 words`):** High-Retention Pillar Scripting & Voice Calibration (`H.E.A.R.T.`) — 5-Parameter Voice DNA Engine and 90-second tension-release resets.
* **Chapter 06 (`7,860 words`):** The 1-to-15 Omnichannel Waterfall & Derivative Content Matrix — Transposing 1 pillar script into 15 platform-native assets with zero quality dilution.
* **Chapter 07 (`7,785 words`):** The 4-Hour Weekly Batch Production Pipeline & AI Automation Stack — Mon–Thu cognitive batch blocks, teleprompter velocity, and 12-Point QA Gate.
* **Chapter 08 (`8,240 words`):** Rented-to-Owned Audience Architecture: Lead Magnets & Welcome Sequences — 5-Minute Utility Lead Magnets, 45%+ opt-in wireframes, and 5-Day Value-First Bridge.
* **Chapter 09 (`8,190 words`):** The Solopreneur Digital Product Value Ladder & 14-Day Launch Blueprint — Validate-Before-You-Build pre-sales, 4-tier pricing, and checkout order bumps.
* **Chapter 10 (`8,415 words`):** Outcome-Based Sponsorships, Brand Deal Pricing & The Creator CEO Scorecard — $R_{\text{sponsor}}$ pricing equation, usage-rights redlines, and 20-minute Friday review.
* **Front & Back Matter Vault (`9,126 words`):** Quick-Start Execution Guide + **50 Copy-Paste AI Workflow Prompts (`P01–P50`)** + **12 Emergency Creator & Sponsor Negotiation Scripts (`S01–S12`)**.

---

### Deep Dive Into the Flagship Software, Spreadsheets, Office Templates & Automations (Tier 3)

1. **100% Offline SaaS-Lite Web Companion App (`creator-os-app.html` + Key `CREATOR-OS-PRO-2026`):**
   * Runs natively in any desktop or mobile browser with zero internet connection, zero subscriptions, and automatic `localStorage` + JSON backup persistence.
   * **Module 1:** RPPH, Blended RPM & 4-Tier Value Ladder Simulator.
   * **Module 2:** Interactive 50-Prompt (`P01–P50`) & 12-Script (`S01–S12`) Variable Compiler with 1-click copy.
   * **Module 3:** `P.A.I.D.` Niche Scorer, `S.I.G.N.A.L.` Outlier Multiplier Lab & `C.L.I.P.` Hook Studio.
   * **Module 4:** 1-to-15 Omnichannel Waterfall Tracker & Live 4-Hour Batch Sprint Timer.
   * **Module 5:** Owned Audience Subscriber Value ($V_{\text{sub}}$) & 14-Day Pre-Sale Launch Validator.
   * **Module 6:** B2B Outcome Sponsorship Calculator ($R_{\text{sponsor}}$), Friday CEO Scorecard & 20-SVG Diagram Viewer.
2. **8-Tab Charted Excel & Google Sheets Command Center (`the-ai-creator-solopreneur-os-financial-and-rpm-matrix.xlsx`):**
   * Contains **650 live formulas** and **4 native visual charts** across 8 tabs (`Executive Summary`, `7-Day Time-Leak & RPPH Audit`, `P.A.I.D. & S.I.G.N.A.L. Scorer`, `1-to-15 Waterfall Tracker`, `Rented-to-Owned Funnel Economics`, `4-Tier Product Launch Simulator`, `B2B Sponsorship Rate Card & CRM`, `12-Month P&L Projection`).
3. **5-Database Minimalist Notion Creator OS Kit:**
   * Ready-to-import CSV databases (`Outlier Idea Bank`, `Master Content Calendar & 1-to-15 Waterfall`, `62-Item AI Prompt & Script Vault`, `Sponsorship CRM`, and `RPM & Time Audit`) + 2,137-word Formula 2.0 Setup Guide.
4. **Editable Microsoft Word (`.docx`) & PowerPoint (`.pptx`) Executive Office Suite:**
   * **7 Word Documents:** Full Editable Book Manuscript (`86,118 words`), Editable 10-Chapter Action Workbook, Sponsorship Media Kit & Rate Card Proposal, Brand Deal Agreement & Usage-Rights Contract, 1-to-15 Repurposing Script Template, 14-Day Digital Product Launch Runbook, and Weekly Creator CEO Review Template.
   * **3 PowerPoint Slide Decks (`32 Slides`):** Brand Sponsorship & Partnership Pitch Deck (12 slides), Educational Masterclass & Webinar Deck Template (10 slides), and Lead Magnet Visual Carousel Deck (10 slides).
5. **Interactive Thumbnail, Cover & Carousel Customizer Studio (`design-customizer-studio.html`):**
   * Customize and export 300-DPI PNGs and editable vector SVGs across 6 platform presets (`YouTube 16:9 Thumbnail`, `6x9 Book Cover`, `Gumroad 16:9 Hero`, `LinkedIn/IG 4:5 Carousel`, `Lead Magnet Cover`, `Social Quote Card`).
6. **5 Ready-to-Import n8n & Make.com JSON Automation Blueprints (`14-AUTOMATION-BLUEPRINTS/`):**
   * Includes `01-n8n-outlier-youtube-rss-idea-miner.json`, `02-make-1to15-omnichannel-repurposing-pipeline.json`, `03-n8n-lead-magnet-optin-to-5day-welcome-bridge.json`, `04-make-sponsor-crm-invoice-and-roi-report-automator.json`, and `05-n8n-friday-creator-ceo-kpi-scorecard-digest.json` + 2,085-word API & Webhook Setup Guide.

---

### Compare Editions: Choose Your Tier on the Right Sidebar

| Deliverable / System Component | Tier 0: Free Starter ($0) | Tier 1: Core Book ($19) | Tier 2: Workbook & Atlas ($39) | ⭐ Tier 3: Complete Flagship OS ($59) |
| :--- | :---: | :---: | :---: | :---: |
| **Ch 1 Sample Book + Fillable Ch 1 Workbook + Audit CSV** | ✅ | ✅ | ✅ | ✅ |
| **340-Page Full-Color Master Manual PDF (All 10 Chapters)** | — | ✅ | ✅ | ✅ |
| **314-Page 6"x9" Print Interior PDF + Validated EPUB 3.0** | — | ✅ | ✅ | ✅ |
| **50 AI Workflow Prompts (`P01–P50`) & 12 Scripts (`S01–S12`)** | `P01–P05` | ✅ All 62 | ✅ All 62 | ✅ All 62 |
| **US Letter, ISO A4 & iPad Landscape Fillable Workbooks (1,420 Fields)** | Ch 1 Only | — | ✅ All 4 | ✅ All 4 |
| **12-Page Visual Shortcut Atlas PDF + 31 Vector SVGs/PNGs** | 2 PNGs | 20 in Book | ✅ All 31 | ✅ All 31 |
| **100% Offline SaaS-Lite Web Companion App (`creator-os-app.html`)** | Free Mode | — | ✅ Pro Mode | ✅ Full Pro Mode (`CREATOR-OS-PRO-2026`) |
| **5-Database Minimalist Notion Creator OS Kit + Formula 2.0 Guide** | — | — | — | ✅ Included |
| **8-Tab Charted Excel Command Center (650 Formulas + 4 Charts)** | — | — | — | ✅ Included |
| **7 Editable Microsoft Word (`.docx`) Manuals, SOPs & Contracts** | — | — | — | ✅ Included |
| **3 Editable PowerPoint (`.pptx`) Pitch & Masterclass Decks (32 Slides)** | — | — | — | ✅ Included |
| **Interactive Cover, Thumbnail & Carousel Customizer Studio** | — | — | — | ✅ Included |
| **5 Importable n8n & Make.com JSON Automation Blueprints** | — | — | — | ✅ Included |

---

### Looking for Ongoing Monthly Outlier Hooks, Faceless Scripts & Agency White-Label Rights?

If you want **everything in the Tier 3 Flagship Bundle** PLUS **Monthly Recurring Outlier Title/Thumbnail Frameworks, 60-Second Faceless & On-Camera Scripts, B2B Sponsor Pitch Packs, and Commercial Agency/Cohort Training Rights**, join our companion membership listing:

**[👉 Click Here to Join the VIP Living Creator Vault Membership ($9/month or $49/year — Save 55%!)](https://gumroad.com/l/ai-creator-vip-vault)**

---

### Frequently Asked Questions

* **Do I need a large audience (50K+ subscribers) for this system to work?**
  No. Eight of the ten documented creator case studies in the manual generate between $11,900 and $26,800/month with fewer than 20,000 subscribers by replacing $5 AdSense CPMs with $150–$300+ Blended Effective RPMs.
* **Does this work for faceless channels and written newsletters?**
  Yes. Every framework, prompt, and 1-to-15 waterfall workflow supports both on-camera video creators and faceless/written operators.
* **Does the Web App require an ongoing subscription or OpenAI API key?**
  Zero subscriptions and zero API keys required. The Web Companion App (`creator-os-app.html`) runs 100% offline in your browser, and all 50 prompts work inside free or paid accounts on Claude, ChatGPT, or Gemini.

---

### 30-Day 100% Risk-Free Operator Guarantee (By OMAR SUNNY)
Download your chosen edition today, run the calculators, and deploy the prompts. If you are not 100% satisfied within 30 days, reply to your Gumroad receipt email for an immediate full refund.
```

---

## 4. EXACT "VERSIONS" CONFIGURATION (`Product Tab -> Versions`)

Scroll down to the **Versions** section on the Gumroad Product tab and configure each version exactly as follows:

### Version 0 (Include if running the Unified 4-Version `$0 / $19 / $39 / $59` Setup on 1 Link)
* **Version Name:** `Tier 0: Free 7-Day Creator RPPH & Time-Leak Audit Starter Kit ($0)`
* **Version Description:** `57-Page Sample Manual (Chapter 1 + Audit) + 13-Page Fillable Ch 1 Workbook (48 Fields) + 25-Row RPM/Time-Leak Audit CSV + Prompts P01-P05 + Master 5-Stage Ecosystem Map Poster.`
* **Additional Amount:** `+$0` (Total = `$0`)
* **Content Tab File to Upload:** `09-EXPORTS/HYBRID-BUNDLE/tier0-free-sample-starter-kit.zip`

### Version 1 (Base Paid Tier — `$19`)
* **Version Name:** `Tier 1: Core Digital Book, KDP Print & EPUB 3.0 Edition ($19)`
* **Version Description:** `Complete 340-Page Full-Color Master Manual PDF (91,775 Words across all 10 Chapters) + Validated Reflowable EPUB 3.0 + 314-Page 6"x9" Print Edition + All 50 AI Workflow Prompts (P01-P50) & 12 Emergency Scripts (S01-S12).`
* **Additional Amount:** `+$19` (if Base Price is `$0`) OR `+$0` (if Base Price is `$19`)
* **Content Tab File to Upload:** `09-EXPORTS/HYBRID-BUNDLE/tier1-reader-edition.zip`

### Version 2 (Mid Decoy Tier — `$39` [or `$29`])
* **Version Name:** `Tier 2: Interactive Fillable Workbooks, 12-Page Visual Atlas & Planner Edition ($39)`
* **Version Description:** `Everything in Tier 1 PLUS: US Letter & ISO A4 Fillable 10-Chapter Workbooks (848 AcroForm Fields), 132-Page Landscape iPad/Tablet Planner (524 Fields), 12-Page Visual Shortcut Atlas PDF, 31 Vector Diagrams/Cheat-Sheets, Offline Web App & 62-Item Prompt Vault CSV.`
* **Additional Amount:** `+$39` (if Base Price is `$0`) OR `+$20` (if Base Price is `$19`; use `+$10` for `$29` matrix)
* **Content Tab File to Upload:** `09-EXPORTS/HYBRID-BUNDLE/tier2-implementation-pack.zip`

### Version 3 (Hero Flagship Tier — `$59` [or `$49`])
* **Version Name:** `⭐ Tier 3: Complete Flagship AI Creator OS Bundle — MOST POPULAR ($59)`
* **Version Description:** `Complete 112-File Solopreneur Ecosystem: Everything in Tier 2 + Full Pro Offline Web App (Key: CREATOR-OS-PRO-2026) + 8-Tab Charted Excel Command Center + 5-DB Notion Creator OS + 7 Editable Word Docs (Manual, Workbook, Sponsor Media Kit, Brand Contract, Launch Runbook) + 3 PowerPoint Decks (32 Slides) + Design Customizer Studio + 5 n8n/Make JSON Automations.`
* **Additional Amount:** `+$59` (if Base Price is `$0`) OR `+$40` (if Base Price is `$19`; use `+$30` for `$49` matrix)
* **Content Tab File to Upload:** `09-EXPORTS/HYBRID-BUNDLE/tier3-creator-os-complete-bundle.zip`

---

## 5. SHARE & GUMROAD DISCOVER SETTINGS

* **Category:** `Business & Money > Marketing & Sales`
* **5 Exact Discover Tags:** `content creation`, `solopreneur`, `notion template`, `ai prompts`, `youtube automation`
* **Display Product Rating:** `ON`
* **Gumroad Affiliates:** Enable `30%` Affiliate Commission across this listing so creator partners can promote your flagship bundle.
"""


def build_file03_listing3_membership() -> str:
    return r"""# GUMROAD LISTING 3 — VIP LIVING CREATOR VAULT RECURRING MEMBERSHIP (EXACT INPUT FIELDS)

* **Product Title:** *VIP Living Creator & Solopreneur Vault Membership (By OMAR SUNNY)*
* **System Architect & Author Credit:** `OMAR SUNNY`
* **Canonical URL Slug:** `gumroad.com/l/ai-creator-vip-vault`

---

## 1. EXACT MEMBERSHIP PRODUCT SETTINGS & BILLING SETUP

In Gumroad, click **Products -> New product**, select **`Membership`**, and enter the exact fields below:

| Gumroad Input Field | Exact Copy-Paste Value |
| :--- | :--- |
| **Product Type** | `Membership` |
| **Product Name** | `VIP Living Creator & Solopreneur Vault Membership (Monthly Outlier Hooks, AI Prompts & Full Flagship OS — By OMAR SUNNY)` |
| **URL Slug (`gumroad.com/l/...`)** | `ai-creator-vip-vault` |
| **Monthly Billing Price** | `$9` / month |
| **Annual Billing Price (Default Recommended)** | `$49` / year *(Saves 55% over monthly billing)* |
| **Call to Action Button** | `Subscribe` (or `Join the VIP Vault`) |
| **Square Thumbnail (`600 × 600 px`)** | `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/13-gumroad-square-thumb-listing3-vip-membership-600x600.png` |
| **Product Cover Banner (`1600 × 1000` / `1280 × 720`)** | `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/06-gumroad-tier4-vault-membership-cover.png` |
| **Secondary Cover Slide 2** | `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/05-gumroad-tier3-flagship-bundle-cover.png` |
| **Secondary Cover Slide 3** | `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/00-ECOSYSTEM-MASTER-MAP-POSTER.png` |

---

## 2. MEMBERSHIP TIER CONFIGURATION, SUMMARY & ATTRIBUTES

### 2.1 Membership Tier Setup (Under `Tiers` Section)
* **Tier Name:** `Executive Creator Vault & Agency White-Label Member (Full OS + Monthly Drops)`
* **Tier Description:**
  `Instant download of the complete 156-File Flagship AI Creator & Solopreneur OS (all Books, Fillable Workbooks, Pro Web App CREATOR-OS-PRO-2026, 8-Tab Excel, 5-DB Notion OS, 7 Word SOPs, 3 PPTX Decks, Cover Studio & 5 Automations) + Commercial Agency/Cohort Rights + Monthly Validated Outlier Hook, Faceless Script & Sponsor Funnel Drops.`
* **Prices Enabled:**
  * Monthly: `$9`
  * Yearly: `$49`
* **Membership Access Toggles:**
  * `[x]` *New members will have access to all previous posts* (`ON`)
  * `[x]` *Show number of members on product page* (`ON` once you pass 25+ members)
  * `[x]` *Allow members to pay what they want* (`OFF` — keep fixed `$9/mo` and `$49/yr` pricing for clean recurring predictability)

### 2.2 Summary Field (Right Sidebar Callout)
```text
All-Access VIP Living Creator Vault & White-Label Membership by OMAR SUNNY. Get immediate access to the entire 156-File Flagship Creator OS Bundle PLUS monthly outlier title/thumbnail frameworks, 60s faceless & on-camera scripts, B2B sponsor pitch drops, and agency cohort training rights.
```

### 2.3 Additional Details (`Attribute : Value` Pairs)

| Attribute | Value |
| :--- | :--- |
| `System Architect` | `OMAR SUNNY` |
| `Baseline Archive` | `156 Production Files (Entire Tier 3 Flagship OS Included Day 1)` |
| `Monthly Vault Drop` | `20 Outlier Hooks + 5 Full 60s Scripts + 3 Sponsor Pitches Monthly` |
| `Pro Software Key` | `CREATOR-OS-PRO-2026 (Included Immediately)` |
| `Commercial Rights` | `Agency Client & Creator Cohort White-Label Training License` |
| `Cancellation Policy` | `Cancel Anytime in 1 Click — Keep All Downloaded Baseline Files` |

### 2.4 Refund Policy Setting
* **Selection:** `30-day money back guarantee`
* **Fine Print:**
  `30-Day 100% Risk-Free Membership Guarantee by OMAR SUNNY: Join the VIP Living Creator Vault today and download the full 156-file archive + Month 01 Drop. If you are not satisfied within your first 30 days, request a full refund in one click and cancel recurring billing with zero penalty.`

---

## 3. FULL RICH-TEXT MEMBERSHIP DESCRIPTION WITH CROSS-LINK BUTTON (COPY-PASTE READY)

```markdown
### Get the Complete 156-File AI Creator OS Today—Plus Monthly Validated Outlier Hooks, Faceless Scripts & Sponsor Funnel Drops.

**Architected by OMAR SUNNY · Apex Digital Systems Studio**

Social algorithms, packaging patterns, and AI automation workflows evolve every quarter. While our core 10-chapter manual gives you the permanent mathematical operating system, the **VIP Living Creator & Solopreneur Vault Membership** ensures you never have to research trending hook structures, faceless script formats, or active B2B sponsor angles from scratch again.

When you join today (for **$9/month** or **$49/year — saving 55%**), you receive **instant Day-1 access to the entire Flagship AI Creator OS Bundle (`$59` value included free)** PLUS our recurring monthly intelligence drops and commercial agency cohort license.

---

### Part 1: Instant Day-1 Baseline Archive (All 156 Production Files Included)

1. **Complete 10-Chapter Master Manual & Retail Suite (`91,775 Words`):**
   * 340-Page US Letter Color Book PDF + 314-Page 6"x9" Print Interior PDF + Validated Reflowable EPUB 3.0.
2. **All 4 Interactive Fillable Action Workbooks (`1,420 AcroForm Fields`):**
   * US Letter Fillable Workbook (448 fields), ISO A4 Fillable Workbook (400 fields), 132-Page iPad/Tablet Landscape Planner (524 fields), and Standalone Chapter 1 Audit Workbook (48 fields).
3. **Full Pro Offline SaaS-Lite Web Companion App + Design Customizer Studio:**
   * Includes `creator-os-app.html` (`528 KB` 6-Module Simulator & 62-Item Searchable Vault) activated with Pro License Key **`CREATOR-OS-PRO-2026`**, plus `design-customizer-studio.html` for 1-click vector/PNG covers and thumbnails.
4. **8-Tab Charted Excel Command Center & 5-Database Minimalist Notion Creator OS Kit:**
   * Live Excel workbook (`650` dynamic formulas + `4` native charts) + 5 Notion CSV databases & Formula 2.0 Setup Guide.
5. **Editable Microsoft Office Suite (`7 Word DOCX` + `3 PowerPoint PPTX Decks`):**
   * Full Editable Manuscript DOCX, Editable Workbook DOCX, Sponsorship Media Kit & Rate Card DOCX, Brand Deal Agreement & Usage-Rights Contract DOCX, 1-to-15 Repurposing Template DOCX, 14-Day Launch Runbook DOCX, Weekly CEO Review DOCX, plus 32-Slide PPTX Pitch & Masterclass Decks.
6. **12-Page Visual Shortcut Atlas, 31 Vector Diagrams & 5 n8n/Make JSON Automations:**
   * All editable source `.svg` files, 300-DPI `.png` renders, and 5 ready-to-import automation blueprints.
7. **Commercial Agency, Cohort & White-Label Training Rights:**
   * Deploy the worksheets, SOPs, and slide decks inside your paid client accounts, creator cohorts, or agency onboarding programs.

---

### Part 2: Included Immediately — Month 01 Living Creator Vault Drop (`4,108 Words`)

* **20 Plug-and-Play Outlier Title & 3-Word Thumbnail Frameworks:** Proven across Tech/AI, Solopreneur Business, Personal Finance, Productivity, and Creative/Design niches with documented $M_{\text{outlier}} \ge 3.0\times$ performance.
* **5 Complete Word-for-Word 60-Second Vertical Scripts (Faceless & On-Camera):** Includes visual B-roll cues, 3-second `C.L.I.P.` hooks, mid-script retention resets, and owned-bridge CTAs.
* **3 Outbound B2B Sponsor Pitch Email Templates + Renewal Sequences:** Ready to send to SaaS, AI tool, and B2B marketing directors.
* **The 48-Hour Weekend "$5K Micro-Toolkit" Cash-Injection Playbook:** Hour-by-hour Friday-to-Sunday execution schedule.

---

### Part 3: Full 12-Month Recurring Vault Release Roadmap

On the 1st of every month, a new **Living Creator Vault Drop** is published directly to your Gumroad Library & Email Inbox:

| Month | Scheduled Monthly Intelligence & Template Drop | Included Assets |
| :--- | :--- | :--- |
| **Month 01 (Instant)** | Outlier Packaging Pack + 5 Vertical Scripts + 48-Hr $5K Launch Playbook | 20 Hooks + 5 Scripts + 3 Sponsor Emails |
| **Month 02** | High-Retention YouTube & Faceless Documentary Storytelling Pack | 20 Outlier Titles + 3 Pillar Script Templates |
| **Month 03** | LinkedIn & X Authority Carousel + Newsletter Growth Bridge Pack | 15 Carousel Frameworks + 5 Welcome Emails |
| **Month 04** | B2B SaaS & AI Tool Sponsor Directory + Outbound Pitch Pack | 50 Verified Sponsor Categories + 4 Pitch Scripts |
| **Month 05** | High-Converting Checkout Order Bump & 1-Click Upsell Copy Pack | 10 Sales Page Wireframes + 5 Checkout Stacks |
| **Month 06** | Advanced n8n & Make.com Multi-Agent Content Repurposing Pack | 3 New JSON Workflows + Prompt Upgrades |
| **Months 07–12** | Quarterly Algorithm Telemetry, Packaging Benchmarks & Prompt Drops | 20 Monthly Outlier Hooks + 5 Scripts Every Month |

---

### Prefer a One-Time Purchase Without Recurring Billing?

If you only want the one-time digital editions without monthly vault updates or agency licensing, switch to our main multi-version product page:

**[👉 Click Here to View the One-Time Editions ($0 Free Starter Kit / $19 / $39 / $59 Flagship Bundle)](https://gumroad.com/l/ai-creator-solopreneur-os)**

---

### Cancel Anytime + 30-Day 100% Money-Back Guarantee (By OMAR SUNNY)
Join for **$9/month** or lock in the **$49/year Annual Pass (Save 55%)**. You can cancel recurring billing in a single click from your Gumroad receipt at any time and keep all downloaded baseline files.
```

---

## 4. CONTENT TAB SETUP & MONTHLY POST PUBLISHING WORKFLOW FOR LISTING 3

1. Open the **Content** tab inside the Gumroad Membership editor.
2. Upload **`09-EXPORTS/HYBRID-BUNDLE/tier4-pro-living-system-and-vault.zip`** (`72.2 MB`, containing all 185 production files including the Phase 11 Master Pack) AND **`10-MARKETING/tier4-monthly-vault-drop-01.md`**.
3. Paste the following **VIP Member Onboarding Note** at the top of the Content page:

```markdown
### Welcome to the VIP Living Creator & Solopreneur Vault — By OMAR SUNNY

Your all-access membership is active! Below you can download the complete **Tier 4 Master Archive (`tier4-pro-living-system-and-vault.zip`)** and **Month 01 Living Creator Vault Drop (`tier4-monthly-vault-drop-01.md`)**.

* **Your Pro Web App License Key:** `CREATOR-OS-PRO-2026`
* **How to Activate:** Open `07-INTERACTIVE-TOOLS/creator-os-app.html` in any browser, paste `CREATOR-OS-PRO-2026` into the top bar, and click **Activate Pro Access**.
* **How to Customize Covers & Thumbnails:** Open `08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html` in your browser to customize and export 300-DPI PNG and SVG graphics.
* **Monthly Vault Drops:** Every new monthly drop will be delivered automatically to your email inbox and added to this page on the 1st of each month.

— **OMAR SUNNY**, System Architect
```

### How to Publish Monthly Drops to Active Members on Gumroad (`Posts` Tab)
1. On the 1st of each month, open Gumroad -> **Posts -> New post**.
2. Under **Audience**, select **`Members of VIP Living Creator & Solopreneur Vault Membership`**.
3. Check **`Send as email`** and **`Post to profile / product page`**.
4. Attach the new monthly Markdown/PDF/CSV drop file and click **Publish**. Both existing members and future members (since *"New members will have access to all previous posts"* is enabled) will have instant access.

---

## 5. SHARE & GUMROAD DISCOVER SETTINGS

* **Category:** `Business & Money > Marketing & Sales`
* **5 Exact Discover Tags:** `content creation`, `solopreneur`, `notion template`, `ai prompts`, `youtube automation`
* **Display Product Rating:** `ON`
* **Gumroad Affiliates:** Enable `30%` recurring affiliate commission so creator partners can promote your VIP Vault.

---

## 6. VIP MEMBER RETENTION, ANNUAL UPGRADE & COHORT LICENSING PROTOCOL

To maximize Lifetime Value (LTV) and keep monthly churn below `4%` on **Listing 3 (`gumroad.com/l/ai-creator-vip-vault`)**, implement the following three operational rules engineered by **OMAR SUNNY**:

1. **Default to the `$49/year` Annual Pass (55% Savings Anchor):**
   * Because monthly billing is `$9/month` (`$108/year`), pricing the annual tier at `$49/year` gives members more than 6 months free while locking in upfront cash flow and zero monthly churn for 365 days.
2. **Pin the Next Month's Drop Preview Inside Every Monthly Post:**
   * At the bottom of each monthly Gumroad Post, include a 3-bullet preview of next month's scheduled Outlier Title/Thumbnail pack, 60-second vertical script templates, and B2B sponsor outreach sequence so monthly subscribers stay active.
3. **Agency & Creator Incubator White-Label Verification:**
   * Agency owners, fractional CMOs, and cohort instructors who maintain an active VIP Living Creator Vault pass receive ongoing commercial rights to use the 7 Editable Word SOPs, 3 PowerPoint Decks, 8-Tab Charted Excel Command Center, and 10 Fillable Chapter Worksheets across their managed client accounts.
"""


def build_file04_upsells_coupons_workflows() -> str:
    return r"""# GUMROAD CHECKOUT UPSELLS, DISCOUNT COUPONS, AUTOMATED WORKFLOWS & GROWTH PLAYBOOK

* **Product Title:** *The AI Content Creator & Solopreneur Operating System*
* **System Architect & Author Credit:** `OMAR SUNNY`
* **Target Storefront:** Gumroad (`Checkout -> Upsells`, `Checkout -> Discounts`, `Workflows`)

---

## 1. EXACT GUMROAD CHECKOUT UPSELL CONFIGURATIONS (`Checkout -> Upsells`)

Gumroad's native **Checkout Upsells** increase Average Order Value (AOV) by **+35% to +48%** with zero extra ad spend. Navigate to **Checkout -> Upsells -> New upsell** and create these 3 upsells:

---

### Upsell #1: Same-Product Version Upgrade Popup (`Tier 0 / Tier 1 / Tier 2` -> `⭐ Tier 3 Flagship Bundle`)

Use this upsell so anyone selecting the Free `$0` Starter Kit, `$19` Core Book, or `$39` Workbook Edition is immediately offered a 1-click upgrade to the **Complete 112-File Flagship Bundle** at checkout:

* **Upsell Name (Internal):** `Upgrade to Tier 3 Complete Flagship Creator OS Bundle`
* **Upsell Type:** `Replace the version selected with another version of the same product`
* **Product:** `The AI Content Creator & Solopreneur Operating System (By OMAR SUNNY)`
* **Versions to Replace (Triggers):**
  * `Tier 0: Free 7-Day Creator RPPH & Time-Leak Audit Starter Kit ($0)`
  * `Tier 1: Core Digital Book, KDP Print & EPUB 3.0 Edition ($19)`
  * `Tier 2: Interactive Fillable Workbooks, 12-Page Visual Atlas & Planner Edition ($39)`
* **Version to Offer (Replacement):**
  * `⭐ Tier 3: Complete Flagship AI Creator OS Bundle — MOST POPULAR ($59)`
* **Upsell Headline (Copy-Paste — Zero Banned Words):**
  `Wait—Upgrade to the Complete 112-File Flagship AI Creator OS Bundle (Includes Pro Web App + 8-Tab Excel + Notion OS + Word/PPTX Kits)`
* **Upsell Description (Copy-Paste):**
  `Add the complete executive implementation stack by OMAR SUNNY right now: get the Full Pro Offline SaaS Web App (Key: CREATOR-OS-PRO-2026), the 8-Tab Charted Excel Command Center (650 formulas), the 5-Database Notion Creator OS, 7 Editable Word SOPs & Sponsor Contracts, 3 PowerPoint Pitch Decks (32 slides), the Thumbnail/Cover Customizer Studio, and 5 n8n/Make JSON Automations. One single B2B sponsor deal or digital product pre-sale pays for this upgrade 50x over.`

---

### Upsell #2: Cross-Sell the VIP Living Creator Vault Yearly Membership (`$10 OFF` Add-On)

Use this upsell to offer your recurring **Listing 3 (`ai-creator-vip-vault`)** whenever someone checks out on your main product:

* **Upsell Name (Internal):** `VIP Living Creator Vault Yearly Pass Add-On ($10 OFF)`
* **Upsell Type:** `Add another product to the cart`
* **Trigger Product:** `The AI Content Creator & Solopreneur Operating System (By OMAR SUNNY)` (All Versions)
* **Offered Product:** `VIP Living Creator & Solopreneur Vault Membership` -> `Yearly ($49/year)`
* **Discount Attached to Upsell:** `Fixed amount` -> `$10 OFF` (Customer pays `$39/year` instead of `$49/year`)
* **Upsell Headline (Copy-Paste):**
  `Add the VIP Living Creator Vault Annual Pass for $10 OFF (Monthly Outlier Hooks, 60s Scripts & Agency White-Label Rights)`
* **Upsell Description (Copy-Paste):**
  `Get 12 months of recurring Living Creator Vault Drops by OMAR SUNNY (20 validated outlier title/thumbnail frameworks, 5 faceless & on-camera scripts, and 3 B2B sponsor pitches every month) PLUS immediate access to Month 01 Drop and Commercial Agency/Cohort Training Rights.`

---

### Upsell #3: Standalone Free Starter Kit (`Listing 1`) -> Flagship Bundle (`$10 OFF` Cross-Sell)

If you also publish `Listing 1 (Free 7-Day Creator Audit Starter Kit)` as a separate product URL (`gumroad.com/l/ai-creator-audit-kit`), enable this upsell:

* **Trigger Product:** `Free 7-Day Creator RPPH, Content Time-Leak & Monetization Audit`
* **Offered Product:** `The AI Content Creator & Solopreneur Operating System (By OMAR SUNNY)` -> `⭐ Tier 3: Complete Flagship AI Creator OS Bundle ($59)`
* **Discount Attached to Upsell:** `Fixed amount` -> `$10 OFF` (or `20% OFF`)
* **Upsell Headline (Copy-Paste):**
  `Fast-Track Your 4-Hour Production Week: Get $10 OFF the Complete 112-File Flagship AI Creator OS Bundle Right Now`
* **Upsell Description (Copy-Paste):**
  `Skip manual setup and install the complete 10-Chapter Operating System by OMAR SUNNY today—including all 4 Fillable Workbooks, the Pro Offline SaaS Web App (Key: CREATOR-OS-PRO-2026), 50 AI Workflow Prompts, 12 Emergency Scripts, 8-Tab Excel Command Center, 5 Notion Databases, 7 Word SOPs, 3 PowerPoint Decks, and 5 JSON Automations.`

---

## 2. EXACT DISCOUNT COUPON CODES (`Checkout -> Discounts`)

Navigate to **Checkout -> Discounts -> New discount** and create these 4 strategic promo codes across both `ai-creator-solopreneur-os` and `ai-creator-vip-vault`:

| Coupon Code | Discount Type & Value | Target Products | Strategic Use Case & URL Parameter |
| :--- | :---: | :--- | :--- |
| **`LAUNCH20`** | `20% OFF` | Listing 2 (All Paid Versions) & Listing 3 | Public 72-Hour Launch Promo (`?code=LAUNCH20`) for social bios and launch posts. |
| **`SUBSCRIBER15`** | `15% OFF` | Listing 2 & Listing 3 | Evergreen discount inside the Tier 0 Free Welcome Note & Automated Email Sequence (`?code=SUBSCRIBER15`). |
| **`VIPUPGRADE`** | `$15 OFF` (Fixed) | Listing 2 (`Tier 3 Flagship`) & Listing 3 (`Yearly`) | High-intent 48-hour flash upgrade code sent in Workflow Email #6 (`?code=VIPUPGRADE`). |
| **`CREATORBD50`** | `50% OFF` | Listing 2 & Listing 3 | Regional South Asia / Student / Emerging Creator community code (`?code=CREATORBD50`). |

---

## 3. AUTOMATED 7-EMAIL GUMROAD WORKFLOW SETUP (`Workflows` Tab)

Gumroad's built-in **Workflows** engine sends automated emails to everyone who downloads your `$0` Free Starter Kit and automatically stops sending sales emails the moment they upgrade to a paid tier.

### Step-by-Step Workflow Creation Rules:
1. Click **Workflows -> New workflow** in your Gumroad left sidebar.
2. **Workflow Name:** `Tier 0 Free Audit Kit -> Flagship Creator OS & VIP Vault 14-Day Ascension Sequence`
3. **Trigger:** `Purchases` -> Select **`Free 7-Day Creator Audit Starter Kit ($0)`** (both the standalone Listing 1 and `Version 0 ($0)` of Listing 2).
4. **Filter / Stop Condition (`Does not have bought`):** Select `Tier 1 ($19)`, `Tier 2 ($39)`, `Tier 3 ($59)`, and `VIP Living Creator Vault Membership`. *(This guarantees paying customers never get spammed with upgrade pitches!)*
5. Click **Save and continue**, then add the **7 Emails** below (full 3,850-word body copy is also archived in `10-MARKETING/email-funnel-and-upsell-sequence.md`):

| Email # | Send Delay | Exact Subject Line (Copy-Paste) | Primary Hook, Deliverable & CTA Link |
| :---: | :---: | :--- | :--- |
| **Email 1** | `0 hours` (Immediate) | `[Download Inside] Your 7-Day Creator RPPH Audit Kit + Quick-Start Protocol` | Delivers `tier0-free-sample-starter-kit.zip`, instructs them to fill out Worksheet 01 + run Prompt `P01`, and introduces **OMAR SUNNY**'s 5-Stage Content-to-Cash Engine. |
| **Email 2** | `1 day` (`24 hrs`) | `Why 94% of hard-working creators are trapped at $8.50/hour (The RPPH Math)` | Breaks down the $RPPH$ equation and Marcus Vance's turnaround (`38.5 hrs -> 5.5 hrs/wk`, `$1,310 -> $14,850/mo`). Links to `Tier 2 ($39)` & `Tier 3 ($59)`. |
| **Email 3** | `3 days` (`72 hrs`) | `The 3-Second C.L.I.P. Hook Formula & 3-Word Thumbnail Rule (7.5%+ CTR)` | Teaches the Package-First rule and `C.L.I.P.` hook structure (`Prompts P16–P20`) + links to the Thumbnail Studio & `Tier 3 Flagship Bundle`. |
| **Email 4** | `5 days` (`120 hrs`) | `How to turn 1 weekly script into 15 native posts in a 4-hour batch sprint` | Walks through the Mon–Thu 4-Hour Batch Pipeline (`Chapters 6–7`) and the 5-Database Notion Creator OS + n8n/Make automations. |
| **Email 5** | `7 days` (`168 hrs`) | `Pre-selling $4,900 in 14 days BEFORE building your digital product (Ch 9)` | Reveals the 14-Day Validate-Before-You-Build protocol and $+45\%$ checkout stack (`8-Tab Excel Command Center`). |
| **Email 6** | `9 days` (`216 hrs`) | `How small channels charge $2,500+ per sponsor using Outcome + Whitelisting Math` | Shares the $R_{\text{sponsor}}$ pricing equation, Scripts `S01–S04`, and the Word Brand Deal Contract. Includes code **`SUBSCRIBER15`** (`15% OFF`). |
| **Email 7** | `11 days` (`264 hrs`) | `[Final 24h Notice] Claim your $15 VIP Upgrade Credit on the Complete Creator OS` | Complete 112-file value stack recap + 30-day risk-free guarantee + code **`VIPUPGRADE`** (`$15 OFF` `Tier 3 Flagship` or `VIP Yearly Membership`). |

---

## 4. COMPLETE COPY-PASTE EMAIL BODIES FOR GUMROAD WORKFLOWS (BY OMAR SUNNY)

### Workflow Email 1 (Send Immediately: `0 Hours After Free Download`)
* **Subject:** `[Download Inside] Your 7-Day Creator RPPH Audit Kit + Quick-Start Protocol`
* **Body:**
```markdown
Hi there,

Welcome! Your **7-Day Creator RPPH & Time-Leak Diagnostic Audit Kit** is ready inside your Gumroad Library.

I architected *The AI Content Creator & Solopreneur Operating System* to solve one specific crisis: talented creators working 30 to 40 hours a week on the content treadmill while earning less than $12 per production hour.

### Your 30-Minute Quick-Start Action Plan Today:
1. **Open `chapter-01-workbook.pdf`** (it has 48 interactive fillable fields—you can type directly inside the PDF on your laptop or tablet).
2. **Complete Table 1.1 & Table 1.2** to calculate your current **Revenue Per Production Hour ($RPPH$)** and **High-Value Production Ratio ($HVPR$)**.
3. **Copy Prompt `P01`** from `tier0-free-sample-chapter01-and-audit.pdf` and paste it into Claude or ChatGPT to generate your personalized 7-Day Time-Leak Elimination Plan.

If you want to skip straight to the complete 10-Chapter Operating System—including all 50 AI Workflow Prompts (`P01–P50`), 12 Emergency Scripts (`S01–S12`), the Full Pro Offline Web App (`CREATOR-OS-PRO-2026`), the 8-Tab Charted Excel Command Center, and the 5-Database Notion OS—you can claim your 15% reader discount anytime here:

👉 **Get the Complete Flagship AI Creator OS (15% OFF with code SUBSCRIBER15):**
https://gumroad.com/l/ai-creator-solopreneur-os?code=SUBSCRIBER15

👉 **Or join the VIP Living Creator Vault Membership ($9/mo or $49/yr):**
https://gumroad.com/l/ai-creator-vip-vault

To your 4-hour production week,
**OMAR SUNNY**
System Architect, *The AI Content Creator & Solopreneur Operating System*
```

### Workflow Email 2 (`24 Hours After Free Download`)
* **Subject:** `Why 94% of hard-working creators are trapped at $8.50/hour (The RPPH Math)`
* **Body:**
```markdown
Hi there,

Did you run your baseline RPPH calculation inside `chapter-01-workbook.pdf` yesterday?

When B2B creator Marcus Vance (14,200 subscribers) ran that exact audit, he discovered a painful truth:
- **Weekly Production Time:** 38.5 hours/week
- **Monthly Net Creator Income:** $1,310/month
- **Baseline RPPH:** **$7.86 per production hour**

He was spending 29 hours a week on unvalidated scripting, manual video cuts, and formatting social posts—and less than 2 hours a week on high-margin monetization assets.

After installing the **5-Stage Content-to-Cash Operating Engine**:
1. He filtered every topic through the **S.I.G.N.A.L. Outlier Score ($M \ge 2.5\times$)** before scripting.
2. He compressed production into a **4-Hour Mon–Thu Batch Sprint** using the **1-to-15 Waterfall**.
3. He installed a **5-Minute Utility Lead Magnet** ($51\%$ opt-in rate) + **4-Tier Digital Product Value Ladder** + **Outcome B2B Sponsorships**.

Within 90 days, his weekly hours dropped from **38.5 hours to 5.5 hours**, and his monthly net revenue climbed to **$14,850/month ($623/hr RPPH)**.

Want the exact 10-chapter blueprint, 50 prompts, 8-Tab Excel simulator, and Notion workspace Marcus used?

👉 **Activate the Complete Flagship AI Creator OS Bundle (15% OFF):**
https://gumroad.com/l/ai-creator-solopreneur-os?code=SUBSCRIBER15

Best regards,
**OMAR SUNNY**
```

### Workflow Email 3 (`72 Hours After Free Download`)
* **Subject:** `The 3-Second C.L.I.P. Hook Formula & 3-Word Thumbnail Rule (7.5%+ CTR)`
* **Body:**
```markdown
Hi there,

The single most expensive mistake in content creation is spending 8 hours researching and filming a video BEFORE designing the title and thumbnail.

In Chapter 4 of *The AI Content Creator & Solopreneur Operating System*, we enforce the **Package-First Law**:
1. Generate 10 curiosity-delta titles using **Prompt `P16`** (`Curiosity-Gap & Quantified Outcome Title Matrix`).
2. Design a **3-Word Visual Anchor Thumbnail** with at least a `4.5:1` contrast ratio using our interactive **Thumbnail & Cover Customizer Studio**.
3. Script the first 30 seconds using the 4-beat **C.L.I.P. Hook Architecture** (`Context Interrupt -> Lens Validation -> Information Gap -> Proof Roadmap`) so $70\%+$ of viewers hold past the `0:30` mark.

When fintech UX creator Sadia Rahman (19.5K subs) applied this exact protocol, her click-through rate jumped from **3.4% to 8.9%** and her monthly revenue grew from **$2,100 to $16,250/month**.

Get all 50 AI Prompts (`P01–P50`), the Thumbnail Customizer Studio, and the complete 10-Chapter Operating System here:

👉 **Get Instant Access to the Flagship Bundle (15% OFF with code SUBSCRIBER15):**
https://gumroad.com/l/ai-creator-solopreneur-os?code=SUBSCRIBER15

— **OMAR SUNNY**
```

---

## 5. FAST USER ACQUISITION & TRAFFIC FLYWHEEL PLAYBOOK

1. **Pin Your Unified Gumroad Link With `?wanted=true` or `?code=LAUNCH20`:**
   * Share `https://[username].gumroad.com/l/ai-creator-solopreneur-os` in your YouTube description, LinkedIn featured section, X bio, and Facebook profile.
2. **Pair Your Live GitHub Pages Calculator With Your Gumroad Link:**
   * Let visitors test their live RPPH on `https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/` and click straight through to download the `$0` Starter Kit or `$59` Flagship Bundle.
3. **Activate Gumroad Discover + 30% Affiliates:**
   * Once your first 10 downloaders leave 5-star ratings on `ai-creator-solopreneur-os`, toggle on Gumroad Discover and invite newsletter/creator peers to earn a `30%` affiliate commission on every `$39`, `$59`, and `$49/yr` sale.
"""


def build_file05_ai_image_prompts() -> str:
    return r"""# 12 HIGH-PRECISION AI COVER & THUMBNAIL IMAGE GENERATION PROMPTS (MIDJOURNEY V6, IDEOGRAM 2.0, DALL-E 3 & LEONARDO AI)

* **Product Title:** *The AI Content Creator & Solopreneur Operating System*
* **System Architect & Official Author Credit:** `OMAR SUNNY` (`BY OMAR SUNNY`)
* **Locked Color Palette:** Deep Studio Navy (`#0F172A`), Creator Indigo (`#4F46E5`), Conversion Teal (`#0D9488`), Retention Amber (`#D97706`), Pure White (`#FFFFFF`)

> **How to Use These Prompts:** Your studio already includes deterministic, pixel-verified vector SVGs and PNGs in `08-COVER-DESIGN/` and `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/`. If you also want photorealistic 3D hardware/box mockups for social ads, Gumroad carousel slides, or A/B testing, paste any of the 12 prompts below directly into **Ideogram 2.0** (best for exact typography rendering), **DALL-E 3**, **Midjourney v6**, or **Leonardo AI**.

---

## PART A: SQUARE `1:1` (`600 × 600 px`) GUMROAD DISCOVER THUMBNAIL PROMPTS

### Prompt 01: Listing 1 Square Thumbnail (`$0` Free 7-Day Creator Audit Starter Kit)
* **Target Dimension:** `600 × 600 px` (`1:1` Square Aspect Ratio)
* **Best Models:** Ideogram 2.0 (Design/Realistic mode), DALL-E 3, Midjourney v6 (`--ar 1:1`)
```text
A high-contrast 1:1 square digital product thumbnail (600x600) on a deep obsidian navy background (#090D16) with a subtle glowing architectural grid. In the center, a sleek 3D isometric stack showing an open technical workbook with glowing teal data charts (#2DD4BF), a laptop displaying an RPPH unit-economics dashboard, and a glowing teal badge at the top reading "FREE $0 AUDIT KIT". Bold ultra-crisp sans-serif headline text reading "7-DAY CREATOR RPPH AUDIT" in pure white (#FFFFFF) and vibrant conversion teal (#2DD4BF). At the bottom edge, sleek micro-typography with wide letter-spacing reading "BY OMAR SUNNY". Studio rim lighting, executive SaaS aesthetic, 8k resolution, razor-sharp vector-style typography --ar 1:1 --v 6.0
```

### Prompt 02: Listing 2 Square Thumbnail (`$0 / $19 / $39 / $59` Complete Flagship AI Creator OS Bundle)
* **Target Dimension:** `600 × 600 px` (`1:1` Square Aspect Ratio)
* **Best Models:** Ideogram 2.0, DALL-E 3, Midjourney v6 (`--ar 1:1`)
```text
A premium 1:1 square Gumroad Discover product thumbnail (600x600) featuring a flagship multi-device software and publishing box set on a dark slate and indigo studio surface (#0F172A). Centerpiece shows a matte navy hardcover manual titled "AI CREATOR & SOLOPRENEUR OS", flanked by a glowing MacBook Pro running a dark-mode SaaS dashboard, an iPad Pro with an interactive landscape planner and Apple Pencil, and an 8-tab financial chart tablet. Top gold and electric indigo badge (#4F46E5, #FBBF24) reading "COMPLETE FLAGSHIP OS". Bottom sleek wide-spaced micro-typography reading "BY OMAR SUNNY". Dramatic volumetric indigo and teal lighting, ultra-clean commercial product photography --ar 1:1 --v 6.0
```

### Prompt 03: Listing 3 Square Thumbnail (`$9/mo` or `$49/yr` VIP Living Creator Vault Membership)
* **Target Dimension:** `600 × 600 px` (`1:1` Square Aspect Ratio)
* **Best Models:** Ideogram 2.0, DALL-E 3, Midjourney v6 (`--ar 1:1`)
```text
An executive 1:1 square membership product thumbnail (600x600) on a deep midnight navy and royal indigo background (#090D16, #1E1B4B). In the center, a glowing futuristic matte-black and brushed-gold digital vault emblem opening to reveal glowing holographic cards labeled "OUTLIER HOOKS", "50 AI PROMPTS", "SPONSOR CRM", and "WHITE-LABEL RIGHTS". Top glowing teal and amber pill badge reading "VIP MONTHLY VAULT • $9/MO". Main bold headline reading "LIVING CREATOR VAULT PASS". Sleek bottom micro-typography reading "SYSTEM ARCHITECT: OMAR SUNNY". High-contrast luxury SaaS aesthetic, 8k render --ar 1:1 --v 6.0
```

---

## PART B: WIDESCREEN `16:9` (`1280 × 720` / `1600 × 1000`) GUMROAD HEADER COVER PROMPTS

### Prompt 04: Gumroad Hero Slide 1 — Complete Flagship 112-File Ecosystem Showcase (`Tier 3`)
* **Target Dimension:** `1280 × 720 px` (`16:9` Widescreen Gumroad Cover)
```text
A widescreen 16:9 commercial hero banner (1280x720) for a flagship digital operating system on a dark carbon-slate executive desk (#090D16) with subtle indigo and teal ambient backlighting (#4F46E5, #0D9488). Arranged in a clean architectural flat-lay and 3D perspective: (1) A thick hardcover technical manual titled "THE AI CONTENT CREATOR & SOLOPRENEUR OPERATING SYSTEM", (2) A widescreen laptop displaying a 6-module Creator RPPH & Prompt Vault web application, (3) An iPad Pro showing fillable AcroForm worksheets, (4) Floating UI cards showing "8-TAB EXCEL COMMAND CENTER", "5-DB NOTION OS", "7 WORD DOCS + 3 PPTX DECKS", and "5 N8N/MAKE AUTOMATIONS". Top left badge: "FLAGSHIP EDITION v1.0". Bottom right signature in crisp wide-spaced caps: "BY OMAR SUNNY". Photorealistic studio product render, zero clutter --ar 16:9 --v 6.0
```

### Prompt 05: Gumroad Slide 2 — Interactive Fillable Workbooks, 12-Page Visual Atlas & iPad Planner (`Tier 2`)
* **Target Dimension:** `1280 × 720 px` (`16:9` Widescreen Gumroad Cover)
```text
A widescreen 16:9 product showcase banner (1280x720) highlighting an interactive workbook and visual diagram suite on a dark navy studio surface (#0F172A). Center shows a dual-screen setup: an iPad Pro in landscape orientation displaying a dark-indigo and teal 5-Stage Content-to-Cash flowchart diagram alongside three printed spiral-bound engineering workbooks (US Letter, ISO A4, and 12-Page Visual Shortcut Atlas) with visible fillable form tables and mathematical formulas. Top badge: "1,420 FILLABLE FIELDS + 31 VECTOR DIAGRAMS". Bottom credit in clean micro-typography: "SYSTEM ARCHITECT: OMAR SUNNY". Sharp studio lighting, high-contrast technical clarity --ar 16:9 --v 6.0
```

### Prompt 06: Gumroad Slide 3 — 8-Tab Charted Excel, 5-DB Notion OS & Automation Blueprints Showcase
* **Target Dimension:** `1280 × 720 px` (`16:9` Widescreen Gumroad Cover)
```text
A widescreen 16:9 dark-mode SaaS and financial command center showcase (1280x720). A sleek ultrawide monitor on a minimal obsidian desk displaying an 8-tab financial spreadsheet with glowing indigo and emerald bar charts ("RPPH Calculator", "S.I.G.N.A.L. Outlier Scorer", "1-to-15 Waterfall", "4-Tier Value Ladder", "Sponsor Rate Card") next to a connected node-based automation workflow (n8n / Make JSON pipeline) and a 5-database Notion dashboard. Clean bold typography overlay at top: "AUTOMATE PRODUCTION IN 4 HOURS/WEEK". Bottom micro-typography: "BY OMAR SUNNY" --ar 16:9 --v 6.0
```

### Prompt 07: Gumroad Slide 4 — VIP Living Creator Vault & White-Label Agency License Cover (`Tier 4`)
* **Target Dimension:** `1280 × 720 px` (`16:9` Widescreen Gumroad Cover)
```text
A widescreen 16:9 luxury executive membership banner (1280x720) in deep navy (#090D16), electric indigo (#4F46E5), and warm gold (#FBBF24). Features a 3D metallic VIP access card embossed with "CREATOR-OS-PRO-2026" resting beside a stack of executive pitch decks, brand sponsorship contracts, and monthly outlier intelligence dossiers. Headline text: "VIP LIVING CREATOR VAULT & WHITE-LABEL EDITION". Bottom credit in wide-spaced uppercase: "BY OMAR SUNNY" --ar 16:9 --v 6.0
```

---

## PART C: AMAZON KDP `1:1.6`, PAYHIP `4:3` & YOUTUBE `16:9` THUMBNAIL PROMPTS

### Prompt 08: Amazon KDP & Apple Books 2D/3D Hardcover Book Cover (`1600 × 2560 px`, `1:1.6` Ratio)
* **Target Dimension:** `1600 × 2560 px` (`1:1.6` Portrait Book Cover)
```text
A vertical 1:1.6 non-fiction business and systems engineering book cover design (1600x2560) in the visual style of Stripe Press and MIT Press. Deep matte navy background (#0F172A) with a precision geometric double-border in electric indigo (#4F46E5). Top monospace label: "OPERATING SYSTEM MANUAL · 91,775 WORDS". Bold white and teal sans-serif title: "THE AI CONTENT CREATOR & SOLOPRENEUR OPERATING SYSTEM". Centerpiece is a clean vector schematic diagram of a 5-stage pipeline (Validate -> Script -> Multiply -> Convert -> Monetize) with mathematical nodes. Bottom author credit in crisp wide-tracked uppercase: "BY OMAR SUNNY" --ar 10:16 --v 6.0
```

### Prompt 09: Payhip / Lemon Squeezy `4:3` Product Card Mockup (`1200 × 900 px`)
* **Target Dimension:** `1200 × 900 px` (`4:3` Marketplace Card)
```text
A 4:3 aspect ratio product showcase card (1200x900) on a deep slate background (#0F172A) showing an isometric arrangement of the complete AI Creator OS: 340-page manual, 4 fillable workbooks, SaaS web app screen, Excel charts, and 50 AI prompt cards. High-contrast teal and indigo rim lighting, bold badge "$59 COMPLETE BUNDLE", and bottom credit "BY OMAR SUNNY" --ar 4:3 --v 6.0
```

### Prompt 10: High-CTR YouTube `16:9` Video Thumbnail (`1920 × 1080 px` — 3-Word Hook Rule)
* **Target Dimension:** `1920 × 1080 px` (`16:9` YouTube Thumbnail)
```text
A high-CTR 16:9 YouTube thumbnail (1920x1080) using a split-contrast layout. Left side (dark red/slate warning zone): a cluttered 40-hour calendar with "$7.86/HR BURNOUT" in bold white and amber text. Right side (glowing teal and indigo operator zone): a clean 4-hour batch sprint calendar connected to 15 social media asset icons and "$623/HR RPPH" in massive neon-teal impact typography. Top 3-word hook banner: "4 HRS -> 15 POSTS". Bottom corner badge: "OMAR SUNNY OS" --ar 16:9 --v 6.0
```

---

## PART D: LINKEDIN AUTHORITY BANNER & NOTION WORKSPACE HEADER PROMPTS

### Prompt 11: LinkedIn Personal Brand Authority Header Banner (`1584 × 396 px` / `4:1` Ratio)
* **Target Dimension:** `1584 × 396 px` (`4:1` LinkedIn Cover)
```text
An ultra-wide 4:1 LinkedIn profile cover banner (1584x396) in deep studio navy (#090D16) and indigo (#1E1B4B) with the left 25% kept clean for the circular profile photo safe zone. On the right 75%, a sleek horizontal schematic of the "5-STAGE CONTENT-TO-CASH OPERATING SYSTEM" with glowing teal nodes (S.I.G.N.A.L. -> C.L.I.P. -> H.E.A.R.T. -> 1-TO-15 WATERFALL -> 4-TIER MONETIZATION) and crisp typography reading "THE AI CONTENT CREATOR & SOLOPRENEUR OS · ARCHITECTED BY OMAR SUNNY" --ar 4:1 --v 6.0
```

### Prompt 12: Notion Creator OS Workspace Cover Header (`1500 × 600 px` / `5:2` Ratio)
* **Target Dimension:** `1500 × 600 px` (`5:2` Notion Page Banner)
```text
A minimalist 5:2 widescreen Notion dashboard header banner (1500x600) in obsidian navy (#0F172A) with a fine blueprint grid, glowing indigo and conversion teal telemetry waveforms, and a centered metallic badge reading "AI CREATOR & SOLOPRENEUR OS — COMMAND CENTER · BY OMAR SUNNY" --ar 5:2 --v 6.0
```

---

## PART E: POST-GENERATION TYPOGRAPHY & PIXEL POLISH PROTOCOL (`design-customizer-studio.html`)

Whenever you generate an AI background or 3D mockup using Prompts 01–12 above, you can combine it with your offline **Design Customizer Studio** (`08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html` or live at `/studio/`):

1. **Exact Pixel Verification:** Gumroad Discover requires exact **`600 × 600 px` (`1:1` Square)** for product thumbnails and **`1280 × 720 px` (`16:9` Widescreen)** (or `1600 × 1000 px`) for top product page covers.
2. **Contrast & Mobile Legibility Rule:** At least **65% of the thumbnail area** should remain high-contrast dark navy (`#090D16` / `#0F172A`) so your 3-word primary hook and price badge (`FREE $0+`, `$19 / $39 / $59`, or `VIP $9/MO`) are readable even at `120 × 120 px` on mobile feeds.
3. **Author Signature Consistency:** Always preserve the bottom micro-typography credit **`BY OMAR SUNNY`** (`letter-spacing: 3px;`) across every cover, square thumbnail, and social card so buyers immediately recognize all listings as part of the same flagship ecosystem.
4. **Recommended Ideogram 2.0 & Midjourney v6 Parameter Reference Table:**
   * **Gumroad Square Discover Thumbnail (`1:1`):** Generate at `1024 × 1024 px` (`--ar 1:1`) and downscale/crop to exact `600 × 600 px` PNG using `design-customizer-studio.html` or `build_phase11_gumroad_pack.py`.
   * **Gumroad Product Header Carousel (`16:9`):** Generate at `1280 × 720 px` or `1920 × 1080 px` (`--ar 16:9`) so all 4 slides fill the top of the Gumroad storefront page edge-to-edge without vertical cropping.
   * **Amazon KDP & Apple Books Portrait (`1:1.6`):** Generate at `1600 × 2560 px` (`--ar 10:16`) at `300 DPI` sRGB color profile.
   * **Color Hex Enforcement:** When prompting Ideogram 2.0, set the custom color palette to `#090D16` (Obsidian Navy), `#0F172A` (Deep Slate), `#4F46E5` (Creator Indigo), `#0D9488` (Conversion Teal), and `#FBBF24` (Retention Amber).
"""


def update_tier4_zip_bundles() -> None:
    """Appends the new Phase 11 Gumroad Master Setup files & 600x600 square thumbnails into the Tier 4 ZIP bundles."""
    zip_targets = [
        STUDIO_ROOT / "09-EXPORTS" / "HYBRID-BUNDLE" / "tier4-pro-living-system-and-vault.zip",
        STUDIO_ROOT / "09-EXPORTS" / "HYBRID-BUNDLE" / "Tier4-Living-Creator-Vault-Membership-Pack.zip",
    ]
    new_files_to_add = list(GUMROAD_DIR.rglob("*")) + [
        COVER_DIR / "11-gumroad-square-thumb-listing1-free-audit-600x600.svg",
        COVER_DIR / "11-gumroad-square-thumb-listing1-free-audit-600x600.png",
        COVER_DIR / "12-gumroad-square-thumb-listing2-flagship-os-600x600.svg",
        COVER_DIR / "12-gumroad-square-thumb-listing2-flagship-os-600x600.png",
        COVER_DIR / "13-gumroad-square-thumb-listing3-vip-membership-600x600.svg",
        COVER_DIR / "13-gumroad-square-thumb-listing3-vip-membership-600x600.png",
    ]

    for zpath in zip_targets:
        if not zpath.is_file():
            continue
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_zip = Path(tmpdir) / zpath.name
            with zipfile.ZipFile(zpath, "r") as zin, zipfile.ZipFile(tmp_zip, "w", compression=zipfile.ZIP_DEFLATED) as zout:
                existing_names = set()
                new_rel_names = {
                    f.relative_to(STUDIO_ROOT).as_posix()
                    for f in new_files_to_add
                    if f.is_file()
                }
                for item in zin.infolist():
                    if item.filename not in new_rel_names:
                        zout.writestr(item, zin.read(item.filename))
                        existing_names.add(item.filename)
                for f in sorted(new_files_to_add):
                    if f.is_file():
                        arcname = f.relative_to(STUDIO_ROOT).as_posix()
                        if arcname not in existing_names:
                            zout.write(f, arcname)
                            existing_names.add(arcname)
            shutil.copy2(tmp_zip, zpath)


def main() -> int:
    print("=" * 88)
    print("PHASE 11 COMPILER: GUMROAD HYBRID MASTER SETUP, 600x600 THUMBNAILS & AI PROMPTS")
    print("=" * 88)

    GUMROAD_DIR.mkdir(parents=True, exist_ok=True)
    GUMROAD_THUMBS_DIR.mkdir(parents=True, exist_ok=True)
    BUILD_SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Generate the 3 600x600 Square Thumbnails (SVG + PNG) and copy covers
    print("[1/4] Rendering 3 Square 600x600 Gumroad Discover Thumbnails (SVG -> PNG)...")
    thumb_outputs = generate_all_square_thumbnails()
    for svg_p, png_p in thumb_outputs:
        with Image.open(png_p) as im:
            w, h = im.size
        print(f"  -> {png_p.name}: {w}x{h} px ({png_p.stat().st_size:,} bytes)")

    # 2. Generate the Master Gumroad Configuration & Prompt Playbooks
    print("[2/4] Authoring Gumroad Hybrid Master Setup Markdown Playbooks...")
    md_files = {
        "00-BANGLA-COMPLETE-GUMROAD-STRATEGY-AND-STEP-BY-STEP-GUIDE.md": build_file00_bangla_master_guide(),
        "01-LISTING-1-FREE-STARTER-KIT-EXACT-FIELDS.md": build_file01_listing1_free(),
        "02-LISTING-2-FLAGSHIP-3-VERSION-PRODUCT-EXACT-FIELDS.md": build_file02_listing2_flagship(),
        "03-LISTING-3-VIP-RECURRING-MEMBERSHIP-EXACT-FIELDS.md": build_file03_listing3_membership(),
        "04-GUMROAD-CHECKOUT-UPSELLS-COUPONS-AND-WORKFLOWS.md": build_file04_upsells_coupons_workflows(),
        "05-AI-COVER-AND-THUMBNAIL-IMAGE-GENERATION-PROMPTS.md": build_file05_ai_image_prompts(),
    }

    for fname, content in md_files.items():
        fpath = GUMROAD_DIR / fname
        fpath.write_text(content, encoding="utf-8")
        words = len(content.split())
        print(f"  -> {fname:62s} : {words:>6,d} words ({fpath.stat().st_size:>8,d} bytes)")

    # 3. Update Tier 4 ZIP Bundles with the new Gumroad Master Setup Pack
    print("[3/4] Updating Tier 4 VIP Vault ZIP Bundles with Phase 11 Gumroad Master Pack...")
    update_tier4_zip_bundles()

    # 4. Mirror script into 11-BUILD-SCRIPTS/
    this_file = Path(__file__).resolve()
    mirror_script = BUILD_SCRIPTS_DIR / this_file.name
    if this_file != mirror_script:
        shutil.copy2(this_file, mirror_script)

    print("=" * 88)
    print("PHASE 11 BUILD COMPLETE: 10-MARKETING/Gumroad-Hybrid-Master-Setup/ Ready.")
    print("=" * 88)
    return 0


if __name__ == "__main__":
    sys.exit(main())
