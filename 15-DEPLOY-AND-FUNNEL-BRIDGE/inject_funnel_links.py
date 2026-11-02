#!/usr/bin/env python3
"""
inject_funnel_links.py
Centralized Link Injection Engine for The AI Content Creator & Solopreneur OS
Author: OMAR SUNNY

Reads funnel-links-config.json and updates all checkout buttons, free download CTAs,
and store URLs across:
  - 10-MARKETING/index.html
  - 07-INTERACTIVE-TOOLS/creator-os-app.html
  - START-HERE-LAUNCHPAD.html
  - 15-DEPLOY-AND-FUNNEL-BRIDGE/web-live-demo/index.html
  - 15-DEPLOY-AND-FUNNEL-BRIDGE/web-live-demo/app.html
  - All marketing markdown documentation
"""

import json
import re
import sys
from pathlib import Path

STUDIO_ROOT = Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.name == "15-DEPLOY-AND-FUNNEL-BRIDGE" else Path(__file__).resolve().parent
CONFIG_PATH = STUDIO_ROOT / "15-DEPLOY-AND-FUNNEL-BRIDGE" / "funnel-links-config.json"


def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Configuration file missing: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def inject_links():
    cfg = load_config()
    links = cfg.get("funnel_links", {})
    t0_url = links.get("gumroad_tier0_free_url", "https://omarsunny.gumroad.com/l/creator-os-free-starter")
    t2_url = links.get("gumroad_tier2_workbook_url", "https://omarsunny.gumroad.com/l/creator-os-workbook")
    t3_url = links.get("gumroad_tier3_flagship_url", "https://omarsunny.gumroad.com/l/creator-os-flagship")
    t4_url = links.get("gumroad_tier4_vip_url", "https://omarsunny.gumroad.com/l/creator-os-vip-vault")
    demo_url = links.get("live_web_app_demo_url", "https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/app/")

    target_files = [
        STUDIO_ROOT / "10-MARKETING" / "index.html",
        STUDIO_ROOT / "07-INTERACTIVE-TOOLS" / "creator-os-app.html",
        STUDIO_ROOT / "START-HERE-LAUNCHPAD.html",
        STUDIO_ROOT / "15-DEPLOY-AND-FUNNEL-BRIDGE" / "web-live-demo" / "index.html",
        STUDIO_ROOT / "15-DEPLOY-AND-FUNNEL-BRIDGE" / "web-live-demo" / "app.html",
        STUDIO_ROOT / "15-WEB-DEPLOYMENT" / "index.html",
        STUDIO_ROOT / "docs" / "index.html"
    ]

    updated_count = 0
    for fpath in target_files:
        if not fpath.exists():
            continue
        content = fpath.read_text(encoding="utf-8")
        orig = content

        content = re.sub(r'https?://[^\s"\']*gumroad\.com/l/[a-zA-Z0-9\-_]+-tier0[^\s"\']*', t0_url, content)
        content = re.sub(r'https?://[^\s"\']*gumroad\.com/l/[a-zA-Z0-9\-_]+-tier2[^\s"\']*', t2_url, content)
        content = re.sub(r'https?://[^\s"\']*gumroad\.com/l/[a-zA-Z0-9\-_]+-(?:flagship|tier3)[^\s"\']*', t3_url, content)
        content = re.sub(r'https?://[^\s"\']*gumroad\.com/l/[a-zA-Z0-9\-_]+-(?:vip|tier4)[^\s"\']*', t4_url, content)

        if content != orig:
            fpath.write_text(content, encoding="utf-8")
            updated_count += 1
            print(f"  [UPDATED] Links injected into: {fpath.relative_to(STUDIO_ROOT)}")

    print(f"Successfully processed {len(target_files)} targets, updated {updated_count} files.")


if __name__ == "__main__":
    inject_links()
