# 🏆 GrailAI — AI Resume Checker & Mock Interview Simulator

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Try_Free_Now-f72585?style=for-the-badge)](https://resume-matcher-ats-mzuvprssvzq7twwbgbuhmb.streamlit.app/)
[![Product Hunt](https://img.shields.io/badge/Product_Hunt-Upvote_Us-DA552F?style=for-the-badge&logo=producthunt)](https://www.producthunt.com/)
[![Built with Streamlit](https://img.shields.io/badge/Built_with-Streamlit-ff4b4b?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Powered by Gemini](https://img.shields.io/badge/Powered_by-Google_Gemini_AI-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Ko-fi](https://img.shields.io/badge/Support-Ko--fi-FF5E5B?style=for-the-badge&logo=ko-fi)](https://ko-fi.com/adityapanda045)

> **The #1 Free AI Resume Checker + Mock Interview Simulator.** Upload your resume, paste any job description, and get instant ATS match score, skill gap analysis, and live AI interview coaching — in under 60 seconds.

🌍 **Used by job seekers in** 🇺🇸 🇬🇧 🇦🇺 🇨🇦 🇩🇪 🇸🇬 🇮🇳 🇧🇷 🇫🇷 🇳🇱 and growing.

---

## 🔥 Why GrailAI Beats Every Other Resume Tool

| Feature | GrailAI ✅ | Other Tools ❌ |
|---------|-----------|--------------|
| AI Resume-JD Match Score | ✅ Instant % score | ❌ Generic tips only |
| Live Mock Interview | ✅ Real AI conversation | ❌ Static Q&A lists |
| Answer Scoring (1-10) | ✅ Personalized feedback | ❌ Not available |
| Cover Letter Generator (Pro) | ✅ Ready to send | ❌ Template-only |
| Resume Rewrite AI (Pro) | ✅ ATS-optimized | ❌ Not available |
| Price | ✅ Free / $4.99 Pro | ❌ $20–$50/month |
| Data Privacy | ✅ Never stored | ❌ Often sold |

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **ATS Resume Score** | Instant % match between your resume and any job description |
| 📊 **Skill Competency Chart** | Visual breakdown across Technical, Domain, Experience & Soft Skills |
| ✅ **Matched Skills** | What you already have that the recruiter wants |
| ⚠️ **Skill Gap Analysis** | Exactly what's missing — fix it before the interview |
| 🎤 **Predicted Interview Questions** | AI generates the exact questions recruiters WILL ask |
| 🤖 **Mock Interview Simulator** | Answer questions live, get scored 1-10 per answer |
| 📋 **Interview Readiness Report** | Final coaching report with your readiness score (0-100%) |
| ✍️ **Resume Rewrite AI** ⚡ Pro | AI rewrites your resume with stronger bullets & ATS keywords |
| 📝 **Cover Letter Generator** ⚡ Pro | Personalized, ready-to-send cover letter in seconds |

---

## 🚀 Try It Free — No Login Required

**👉 [resume-matcher-ats-mzuvprssvzq7twwbgbuhmb.streamlit.app](https://resume-matcher-ats-mzuvprssvzq7twwbgbuhmb.streamlit.app/)**

No account. No credit card. Just upload your PDF and paste any job description. Get results in 30 seconds.

---

## ⚡ Pro Plan — $4.99/month

Upgrade for the complete career toolkit:

- 🔓 **Unlimited analyses** (free tier: 3/session)
- ✍️ **Resume Rewrite AI** — Beat ATS with stronger bullets + keywords
- 📝 **Cover Letter Generator** — Personalized, ready-to-send in seconds
- 🚀 **Priority AI** — Faster responses

**[→ Get Pro for $4.99/month](https://buy.stripe.com/grailai_pro)**

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend / App** | Streamlit (Python) |
| **AI Engine** | Google Gemini 2.0 Flash (4-model fallback) |
| **PDF Parsing** | pypdf |
| **Data Viz** | Plotly |
| **Styling** | Custom CSS — Dark Glassmorphism UI |
| **Payments** | Stripe |
| **Hosting** | Streamlit Community Cloud |

---

## 🔒 Security Architecture

- **Prompt Injection Guard** — System-level prefix prevents jailbreaking via malicious resume content
- **Input Sanitization** — All inputs truncated to 8,000 chars and null-byte stripped
- **Rate Limiting** — Session-level limits to prevent API abuse
- **PDF Size Validation** — Rejects files over 5 MB
- **No Data Storage** — Resume and JD are never stored or logged
- **API Key Safety** — Keys stored only in `.streamlit/secrets.toml`

---

## 🖥️ Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/adityapanda045/resume-matcher-ats.git
cd resume-matcher-ats

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Gemini API key
# Create .streamlit/secrets.toml:
# GOOGLE_API_KEY = "your-key-here"
# Get a free key at: https://aistudio.google.com/

# 4. Run
streamlit run app.py
```

---

## 📣 Share GrailAI

If GrailAI helped you, share it — you'll help thousands of job seekers worldwide:

- 🐦 [Share on Twitter/X](https://twitter.com/intent/tweet?text=Just%20tried%20GrailAI%20%F0%9F%8F%86%20-%20Free%20AI%20Resume%20Checker%20%2B%20Mock%20Interview%20Simulator.%20Scores%20your%20resume%20vs%20any%20JD%20instantly!%20Built%20by%20%40adityapanda045&url=https://resume-matcher-ats-mzuvprssvzq7twwbgbuhmb.streamlit.app/)
- 💼 [Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://resume-matcher-ats-mzuvprssvzq7twwbgbuhmb.streamlit.app/)
- 💬 [Share on WhatsApp](https://api.whatsapp.com/send?text=Try%20GrailAI%20FREE%20%F0%9F%8F%86%20-%20AI%20Resume%20Checker%20%2B%20Mock%20Interview%20Simulator.%20Scores%20your%20resume%20against%20any%20job%20description%20in%2030%20seconds!%20https://resume-matcher-ats-mzuvprssvzq7twwbgbuhmb.streamlit.app/)

---

## 📁 Project Structure

```
resume-matcher-ats/
├── app.py              # Main Streamlit application (Pro tier + all features)
├── requirements.txt    # Python dependencies
├── .streamlit/
│   └── secrets.toml   # API keys + Pro license keys (never commit!)
├── .gitignore
└── README.md
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Open an issue or submit a PR.

---

## 👋 About the Creator

**Aditya Panda** — AI Product Builder & Data Analytics Professional

- 💼 Open to remote roles and freelance projects worldwide
- 🔗 [LinkedIn](https://www.linkedin.com/in/aditya-panda-b37437247)
- 📩 [Email](mailto:adityapanda045@gmail.com)
- 💻 [GitHub](https://github.com/adityapanda045)
- ☕ [Support on Ko-fi](https://ko-fi.com/adityapanda045)

> *If GrailAI helped you land an interview or a job, I'd love to hear about it! Drop me a message on LinkedIn.*

---

## ⭐ Star This Repo

If you find GrailAI useful, **please give it a ⭐ star** — it helps more job seekers find the tool and directly supports the project.

---

*🏆 GrailAI — The #1 Free AI Resume Checker & Mock Interview Simulator | Powered by Google Gemini AI | Built by Aditya Panda*
