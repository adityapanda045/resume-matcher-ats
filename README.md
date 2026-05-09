# 🏆 GrailAI — AI Career Intelligence Platform

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Click_Here-f72585?style=for-the-badge)](https://resume-matcher-ats-mzuvprssvzq7twwbgbuhmb.streamlit.app/)
[![Built with Streamlit](https://img.shields.io/badge/Built_with-Streamlit-ff4b4b?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Powered by Gemini](https://img.shields.io/badge/Powered_by-Google_Gemini_AI-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Ko-fi](https://img.shields.io/badge/Support-Ko--fi-FF5E5B?style=for-the-badge&logo=ko-fi)](https://ko-fi.com/adityapanda045)

> **The Holy Grail of Career Tools** — AI-powered resume analysis + real-time mock interview simulator. Built to help job seekers worldwide land their dream role.

🌍 **Used by job seekers in** 🇺🇸 🇬🇧 🇦🇺 🇨🇦 🇩🇪 🇸🇬 🇮🇳 and growing.

---

## ✨ What GrailAI Does

GrailAI takes your resume and a job description, then uses **Google Gemini AI** to give you:

| Feature | Description |
|---------|-------------|
| 🎯 **Resume Match Score** | Instant % match between your resume and any JD |
| 📊 **Skill Competency Chart** | Visual breakdown across Technical, Domain, Experience & Soft Skills |
| ✅ **Matched Skills** | What you already have that the job wants |
| ⚠️ **Skill Gap Analysis** | Exactly what's missing — fix it before the interview |
| 🎤 **Predicted Interview Questions** | AI generates the 3 questions recruiters WILL ask based on your gaps |
| 🤖 **Mock Interview Simulator** | Answer questions live, get scored 1-10 per answer |
| 📋 **Interview Readiness Report** | Final coaching report with your readiness score (0-100%) |

---

## 🚀 Live Demo

**👉 Try it FREE:** [resume-matcher-ats-mzuvprssvzq7twwbgbuhmb.streamlit.app](https://resume-matcher-ats-mzuvprssvzq7twwbgbuhmb.streamlit.app/)

No login. No account. Just upload your PDF and paste any job description.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend / App** | Streamlit (Python) |
| **AI Engine** | Google Gemini 2.0 Flash (with 4-model fallback) |
| **PDF Parsing** | pypdf |
| **Data Viz** | Plotly |
| **Styling** | Custom CSS — Dark Glassmorphism UI |
| **Hosting** | Streamlit Community Cloud |

---

## 🔒 Security Architecture

GrailAI is built with security-first principles:

- **Prompt Injection Guard** — System-level prefix on every AI call prevents jailbreaking via malicious resume content
- **Input Sanitization** — All user inputs are truncated to 8,000 chars and null-byte stripped before reaching the AI
- **Rate Limiting** — Max 5 analyses per session to prevent API abuse
- **PDF Size Validation** — Rejects files over 5 MB
- **No Data Storage** — Your resume and JD are never stored or logged anywhere
- **API Key Safety** — Keys stored only in `.streamlit/secrets.toml`, never in source code

---

## 🖥️ Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/adityapanda045/resume-matcher-ats.git
cd resume-matcher-ats

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Gemini API key
# Create .streamlit/secrets.toml and add:
# GOOGLE_API_KEY = "your-key-here"
# Get a free key at: https://aistudio.google.com/

# 4. Run the app
streamlit run app.py
```

---

## 📁 Project Structure

```
resume-matcher-ats/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .streamlit/
│   └── secrets.toml   # API keys (never commit this!)
├── .gitignore          # Protects secrets from being pushed
└── README.md
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a PR.

---

## 👋 About the Creator

**Aditya Panda** — AI Product Builder & Data Analytics Professional

- 💼 Open to remote roles and freelance projects worldwide
- 🔗 [LinkedIn](https://www.linkedin.com/in/aditya-panda)
- 📩 [Email](mailto:adityapanda045@gmail.com)
- 💻 [GitHub](https://github.com/adityapanda045)
- ☕ [Support on Ko-fi](https://ko-fi.com/adityapanda045)

> *If GrailAI helped you land an interview or a job, I'd love to hear about it! Drop me a message on LinkedIn.*

---

## ⭐ Star This Repo

If you find GrailAI useful, **please give it a ⭐ star on GitHub** — it helps more job seekers find the tool.

---

*🏆 GrailAI — The Holy Grail of Career Tools | Powered by Google Gemini AI*
