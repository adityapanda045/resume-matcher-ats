# 🏆 GrailAI — AI Resume Checker & Mock Interview Simulator

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Try_Now_Free-f72585?style=for-the-badge)](https://resume-matcher-ats-mzuvprssvzq7twwbgbuhmb.streamlit.app/)
[![Built with Streamlit](https://img.shields.io/badge/Built_with-Streamlit-ff4b4b?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Powered by Gemini](https://img.shields.io/badge/Powered_by-Google_Gemini_AI-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

> **The #1 Free AI Resume Checker + Mock Interview Simulator.** Upload your resume, paste any job description, and get an instant ATS match score, skill gap analysis, and live AI interview coaching — in under 60 seconds. 100% free, no login required.

🌍 **Used by job seekers in** 🇺🇸 🇬🇧 🇦🇺 🇨🇦 🇩🇪 🇸🇬 🇮🇳 🇧🇷 🇫🇷 🇳🇱 and growing.

---

## 🔥 What Makes GrailAI Different

| Feature | GrailAI ✅ | Other Tools ❌ |
|---------|-----------|--------------|
| AI Resume-JD Match Score | ✅ Instant % score | ❌ Generic tips only |
| Live Mock Interview | ✅ Real AI conversation | ❌ Static Q&A lists |
| Answer Scoring (1–10) | ✅ Personalized feedback | ❌ Not available |
| Cover Letter Generator | ✅ Ready to send | ❌ Template-only |
| Resume Rewrite AI | ✅ ATS-optimized | ❌ Not available |
| Price | ✅ **100% FREE** | ❌ $20–$50/month |
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
| 🤖 **Mock Interview Simulator** | Answer questions live, get scored 1–10 per answer |
| 📋 **Interview Readiness Report** | Final coaching report with your readiness score (0–100%) |
| ✍️ **Resume Rewrite AI** | AI rewrites your resume with stronger bullets & ATS keywords |
| 📝 **Cover Letter Generator** | Personalized, ready-to-send cover letter in seconds |

---

## 🚀 Try It Live — No Login Required

**👉 [resume-matcher-ats-mzuvprssvzq7twwbgbuhmb.streamlit.app](https://resume-matcher-ats-mzuvprssvzq7twwbgbuhmb.streamlit.app/)**

No account. No credit card. Just upload your PDF and paste any job description. Get results in 30 seconds.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend / App** | Streamlit (Python) |
| **AI Engine** | Google Gemini 2.0 Flash (4-model fallback) |
| **PDF Parsing** | pypdf |
| **Data Visualization** | Plotly |
| **Styling** | Custom CSS — Dark Glassmorphism UI |
| **Hosting** | Streamlit Community Cloud (free) |

---

## 🔒 Security Architecture

- **Prompt Injection Guard** — System-level prefix prevents jailbreaking via malicious resume content
- **Input Sanitization** — All inputs truncated to 8,000 chars and null-byte stripped
- **Rate Limiting** — Session-level limits to prevent API abuse
- **PDF Size Validation** — Rejects files over 5 MB
- **No Data Storage** — Resume and JD are never stored or logged anywhere
- **API Key Safety** — Keys stored only in `.streamlit/secrets.toml` (never committed)

---

## 🖥️ Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/adityapanda045/resume-matcher-ats.git
cd resume-matcher-ats

# 2. Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Gemini API key
# Create .streamlit/secrets.toml and add:
# GOOGLE_API_KEY = "your-key-here"
# Get a free key at: https://aistudio.google.com/

# 5. Run
streamlit run app.py
```

---

## 📁 Project Structure

```
resume-matcher-ats/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── secrets.toml       # API keys (never commit — see .gitignore)
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📣 Share GrailAI

If GrailAI helped you, share it — you'll help thousands of job seekers worldwide:

- 🐦 [Share on Twitter/X](https://twitter.com/intent/tweet?text=Just%20tried%20GrailAI%20%F0%9F%8F%86%20-%20Free%20AI%20Resume%20Checker%20%2B%20Mock%20Interview%20Simulator.%20Scores%20your%20resume%20vs%20any%20JD%20instantly!%20Built%20by%20%40adityapanda045&url=https://resume-matcher-ats-mzuvprssvzq7twwbgbuhmb.streamlit.app/)
- 💼 [Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://resume-matcher-ats-mzuvprssvzq7twwbgbuhmb.streamlit.app/)

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

If you find GrailAI useful, **please give it a ⭐ star** — it helps more job seekers discover the tool and directly supports the project.

---

*🏆 GrailAI — The #1 Free AI Resume Checker & Mock Interview Simulator | Powered by Google Gemini AI | Built by Aditya Panda*
