# ওনার ম্যানুয়াল ও স্টেপ-বাই-স্টেপ সেটআপ গাইড (Phase 10)
**ফ্ল্যাগশিপ প্রোডাক্ট #৩:** *The AI Content Creator & Solopreneur Operating System*  
**প্রিন্সিপাল আর্কিটেক্ট ও লেখক:** ওমর সানী (OMAR SUNNY)  
**ডিস্ট্রিবিউশন প্ল্যাটফর্ম:** Gumroad, Payhip, Amazon KDP, GitHub Pages, Netlify, Vercel  

---

## ১. ভূমিকা ও ইকোসিস্টেমের ওভারভিউ

অভিনন্দন ওমর সানী ভাই! আপনার **The AI Content Creator & Solopreneur Operating System** এখন একটি সম্পূর্ণ কমার্শিয়াল ডিজিটাল পাবলিশিং স্টুডিওতে রূপান্তরিত হয়েছে। এই প্রজেক্টে কেবল একটি সাধারণ ইবুক নয়, বরং একটি ফুল-স্ট্যাক কমার্শিয়াল সফটওয়্যার এবং প্রোডাক্ট ইকোসিস্টেম তৈরি করা হয়েছে।

এই গাইডে খুব সহজ বাংলা ভাষায় প্রতিটি ধাপ বুঝিয়ে দেওয়া হলো যাতে আপনি কোনো ভুল ছাড়াই এটি আন্তর্জাতিক বাজারে লঞ্চ করতে পারেন।

---

## ২. গামরোড (Gumroad) ও পেহিপ (Payhip) প্রোডাক্ট আপলোড ম্যাপিং

`09-EXPORTS/HYBRID-BUNDLE/` ফোল্ডারে আপনার ৫টি রেডিমেড রিলিজ `.zip` বান্ডেল তৈরি আছে:

| লিস্টিং নাম | গামরোড টিয়ার | ফাইল পাথ (Upload Path) | মূল্য (Price) | লাইসেন্স কি |
| :--- | :--- | :--- | :--- | :--- |
| **লিস্টিং ১: ফ্রি লিড ম্যাগনেট** | **Tier 0 Free Kit** | `09-EXPORTS/HYBRID-BUNDLE/tier0-free-sample-starter-kit.zip` | **$0** (Free Lead Magnet) | *Active by Default* |
| **লিস্টিং ২: বুক এডিশন** | **Tier 1 Reader** | `09-EXPORTS/HYBRID-BUNDLE/tier1-reader-edition.zip` | **$19** | *Standard Reader* |
| **লিস্টিং ৩: অ্যাকশন ওয়ার্কবুক** | **Tier 2 Workbook** | `09-EXPORTS/HYBRID-BUNDLE/tier2-implementation-pack.zip` | **$39** | `STUDIO-TIER2-2026` |
| **লিস্টিং ৪: ফ্ল্যাগশিপ ফুল ওএস** | **Tier 3 Flagship OS** | `09-EXPORTS/HYBRID-BUNDLE/tier3-creator-os-complete-bundle.zip` | **$59** | `CREATOR-OS-PRO-2026` |
| **লিস্টিং ৫: ভিআইপি লাইফটাইম ভল্ট** | **Tier 4 VIP Vault** | `09-EXPORTS/HYBRID-BUNDLE/tier4-pro-living-system-and-vault.zip` | **$99** বা **$9/mo** | `STUDIO-PRO-OS-2026` |

---

## ৩. ৩ মিনিটে ফ্রি ওয়েব অ্যাপ লাইভ হোস্টিং গাইড (GitHub Pages / Netlify Drop / Vercel)

আপনার অডিয়েন্স যাতে কোনো কিছু ডাউনলোড করার আগেই তাদের ব্রাউজারে সরাসরি অ্যাপটি টেস্ট করতে পারে, তার জন্য একটি রেডিমেড প্যাকেজ তৈরি আছে: `15-DEPLOY-AND-FUNNEL-BRIDGE/web-live-demo/`।

### পদ্ধতি ক: Netlify Drop (সবচেয়ে সহজ — মাত্র ৩০ সেকেন্ড)
1. আপনার ব্রাউজারে যান: [app.netlify.com/drop](https://app.netlify.com/drop)
2. `15-DEPLOY-AND-FUNNEL-BRIDGE/web-live-demo` ফোল্ডারটি মাউস দিয়ে ড্র্যাগ করে ব্রাউজারে ছেড়ে দিন।
3. নিমিষেই আপনার ওয়েব অ্যাপ লাইভ হয়ে যাবে এবং আপনি একটি লাইভ URL (যেমন `https://creator-os-demo.netlify.app`) পাবেন!

### পদ্ধতি খ: GitHub Pages (১০০% ফ্রি ও পার্মানেন্ট)
1. এই গিট রিপোজিটরি GitHub-এ পুশ করা আছে (`https://github.com/cryptXploit/AI-Creator-Solopreneur-OS.git`)।
2. রিপোজিটরির **Settings** -> **Pages** অপশনে যান।
3. **Build and deployment** সেকশনে Branch নির্বাচন করুন `master` (অথবা `main`) এবং ফোল্ডার দিন `/docs`।
4. **Save** ক্লিক করুন। ২ মিনিটের মধ্যে আপনার পুরো পোর্টাল ও ইন্টারেক্টিভ অ্যাপ লাইভ হবে:  
   `https://cryptxploit.github.io/AI-Creator-Solopreneur-OS/app/`

---

## ৪. সেন্ট্রালাইজড লিংক ইনজেকশন কিভাবে করবেন (`inject_funnel_links.py`)

যখন আপনার গামরোড বা পেহিপ লিংক রেডি হবে:
1. `15-DEPLOY-AND-FUNNEL-BRIDGE/funnel-links-config.json` ফাইলটি ওপেন করুন।
2. আপনার আসল Gumroad, Payhip, এবং Amazon লিংকগুলো বসিয়ে দিন:
```json
{
  "funnel_links": {
    "gumroad_tier0_free_url": "https://omarsunny.gumroad.com/l/creator-os-free-starter",
    "gumroad_tier2_workbook_url": "https://omarsunny.gumroad.com/l/creator-os-workbook",
    "gumroad_tier3_flagship_url": "https://omarsunny.gumroad.com/l/creator-os-flagship",
    "gumroad_tier4_vip_url": "https://omarsunny.gumroad.com/l/creator-os-vip-vault"
  }
}
```
3. টার্মিনালে নিচের কমান্ডটি রান করুন:
```bash
python 15-DEPLOY-AND-FUNNEL-BRIDGE/inject_funnel_links.py
```
এটি নিজে থেকে আপনার ল্যান্ডিং পেজ (`index.html`), ওয়েব অ্যাপ (`creator-os-app.html`), ব্রাউজার লঞ্চপ্যাড (`START-HERE-LAUNCHPAD.html`) এবং সমস্ত ফোল্ডারে নতুন লিংক ইনজেক্ট করে দেবে!

---

## ৫. প্যাসিভ অ্যাফিলিয়েট ইনকাম সেটআপ (Make.com, Notion, Payoneer)

ফ্রি টিয়ার (Tier 0) ব্যবহারকারীরা যখন সফটওয়্যারগুলো ব্যবহার শুরু করবে, তখন আপনি প্রতিটি সাইন-আপ থেকে প্যাসিভ রেভিনিউ আর্ন করতে পারবেন:

1. **Make.com Affiliate Program:**
   - Make.com-এ গিয়ে এফিলিয়েট একাউন্ট খুলুন এবং আপনার রেফারেল লিংক নিন।
   - ফ্রি অটোমেশন গাইডে (`FREE-AUTOMATION-1CLICK-TEST-GUIDE.md`) আপনার লিংকটি যুক্ত করুন। একজন ব্যবহারকারী পেড প্ল্যান নিলেই আপনি প্রতি মাসে কমিশন পাবেন।
2. **Notion Affiliate Program:**
   - নোশন এফিলিয়েট পার্টনারশিপে আবেদন করুন। ফ্রি নোশন গাইডে আপনার লিংক বসান।
3. **Payoneer / Wise:**
   - গামরোড থেকে বাংলাদেশে সরাসরি ডলার উইথড্র করার জন্য Payoneer ব্যবহার করুন।

---

## ৬. আমাজন কেডিপি (Amazon KDP) ফাইল নির্দেশিকা

আমাজনে পেপারব্যাক ও ইবুক আপলোডের জন্য নিচের ফাইলগুলো সম্পূর্ণ প্রস্তুত ও ভেরিফায়েড:
- **Paperback Interior PDF (Exact 314 Pages):** `09-EXPORTS/PDF/the-ai-creator-solopreneur-os-kdp-paperback-6x9.pdf`
- **Kindle eBook File:** `09-EXPORTS/EPUB/the-ai-creator-solopreneur-os.epub`
- **Book Cover Image:** `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/01-ebook-cover-kdp-kindle.png`

এই ফাইলগুলোতে মার্জিন, পেজ নাম্বার, ব্ল্যাঙ্ক পেজ এবং কোড ব্লক সংক্রান্ত সমস্ত জটিলতা শতভাগ সমাধান করে ভেরিফাই করা হয়েছে।

---
*গাইডটি ওমর সানীর জন্য সযত্নে প্রস্তুতকৃত। যেকোনো প্রয়োজনে `verify_phase10_funnel.py` চালিয়ে সমস্ত ফাইলের স্বাস্থ্য পরীক্ষা করতে পারেন।*
