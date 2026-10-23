# STATIC WEB DEPLOYMENT & CLOUD HOSTING RUNBOOK (PHASE 10)

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
