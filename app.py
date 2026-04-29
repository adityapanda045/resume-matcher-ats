import streamlit as st

st.set_page_config(
    page_title="GrailAI — Career Intelligence Platform",
    layout="wide",
    page_icon="🏆"
)

from google import genai
from google.genai import types
import json
import re
from pypdf import PdfReader
import plotly.graph_objects as go
import pandas as pd

# ─────────────────────────────────────────
# SECURE API SETUP
# ─────────────────────────────────────────
def setup_client():
    try:
        key = st.secrets["GOOGLE_API_KEY"]
        if not key or len(key) < 20 or "PASTE" in key or "YOUR" in key:
            st.error("🔑 API Key is not set. Please add your real key to .streamlit/secrets.toml")
            return None
        client = genai.Client(api_key=key)
        return client
    except Exception as e:
        st.error(f"🔑 Could not load API Key: {e}")
        return None

client = setup_client()

# ─────────────────────────────────────────
# CORE FUNCTIONS
# ─────────────────────────────────────────
def extract_pdf_text(file):
    reader = PdfReader(file)
    return " ".join(p.extract_text() for p in reader.pages if p.extract_text())

def call_gemini(resume, jd, prompt):
    # These model names are confirmed available for this API key
    models = [
        "gemini-2.0-flash-lite",
        "gemini-2.0-flash",
        "gemini-2.5-flash",
        "gemini-flash-latest",
    ]
    full_prompt = f"{prompt}\n\nJOB DESCRIPTION:\n{jd}\n\nRESUME:\n{resume}"
    last_error = ""
    for model_name in models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=full_prompt
            )
            return response.text
        except Exception as e:
            last_error = str(e)
            continue
    st.error(f"Debug - Last error: {last_error[:200]}")
    return None

def parse_json(text):
    try:
        m = re.search(r'\{.*\}', text, re.DOTALL)
        return json.loads(m.group()) if m else None
    except Exception:
        return None

PROMPT = """
You are a Senior Technical Recruiter. Analyze the resume against the JD below.
Return ONLY a valid JSON object with no other text before or after it:
{
  "match": <integer 0-100>,
  "scores": {"Technical": <int>, "Domain Knowledge": <int>, "Experience": <int>, "Soft Skills": <int>},
  "skills": [<up to 5 strings of matching skills found>],
  "gaps": [<up to 5 strings of missing skills>],
  "questions": [<exactly 3 interview question strings that target the gaps>],
  "verdict": "<one clear sentence recommendation>"
}
"""

# ─────────────────────────────────────────
# UI — PREMIUM DARK GLASSMORPHISM THEME
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global Background ── */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.1);
}
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

/* ── Main Title ── */
.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #f72585, #7209b7, #4361ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.2rem;
}
.main-subtitle {
    text-align: center;
    color: rgba(255,255,255,0.5);
    font-size: 0.9rem;
    margin-bottom: 2rem;
    letter-spacing: 1px;
}

/* ── Glass Cards ── */
.glass-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(20px);
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.12);
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.07) !important;
    backdrop-filter: blur(20px);
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.12);
    padding: 20px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.6) !important; font-size: 0.85rem !important; }
[data-testid="stMetricValue"] { color: #f72585 !important; font-weight: 800 !important; font-size: 2rem !important; }

/* ── Button ── */
.stButton > button {
    background: linear-gradient(90deg, #f72585, #7209b7, #4361ee) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 24px rgba(247,37,133,0.4) !important;
    transition: all 0.3s ease !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(247,37,133,0.6) !important;
}

/* ── Text Areas & Inputs ── */
.stTextArea textarea, .stFileUploader {
    background: rgba(255,255,255,0.05) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
}
.stTextArea label, .stFileUploader label { color: rgba(255,255,255,0.7) !important; font-weight: 600 !important; }

/* ── Subheaders ── */
h2, h3, .stSubheader { color: white !important; }

/* ── Success / Warning / Info boxes ── */
.stSuccess { background: rgba(0,255,136,0.1) !important; border: 1px solid rgba(0,255,136,0.3) !important; border-radius: 10px !important; }
.stWarning { background: rgba(255,171,0,0.1) !important; border: 1px solid rgba(255,171,0,0.3) !important; border-radius: 10px !important; }
.stInfo    { background: rgba(67,97,238,0.15) !important; border: 1px solid rgba(67,97,238,0.4) !important; border-radius: 10px !important; color: white !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: rgba(255,255,255,0.85) !important;
    border-radius: 0 0 10px 10px !important;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.1) !important; }

/* ── General text ── */
p, span, div { color: rgba(255,255,255,0.85); }
.stSpinner > div { border-top-color: #f72585 !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero Header ──
st.markdown('<div class="main-title">🏆 GrailAI</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">CAREER INTELLIGENCE PLATFORM &nbsp;|&nbsp; POWERED BY GEMINI AI &nbsp;|&nbsp; BUILT BY ADITYA</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🏆 GrailAI")
    st.markdown("*The Holy Grail of Career Tools*")
    st.markdown("---")
    st.markdown("### 👤 Developer")
    st.write("**Aditya**")
    st.write("Technical Process Executive")
    st.write("🎯 Target: Data Analytics Role")
    st.markdown("---")
    st.info("GrailAI uses NLP + Gemini AI to analyze resume-JD fit, score skill dimensions, and generate prescriptive interview insights.")
    if client:
        st.success("✅ API Connected")
    else:
        st.error("❌ API Not Connected")


col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Job Description")
    jd = st.text_area("Paste the Job Description here:", height=220,
                       placeholder="e.g. We are looking for a Data Analyst with Python, SQL, and Power BI...")
with col2:
    st.subheader("📄 Resume Upload")
    pdf_file = st.file_uploader("Upload your Resume (PDF only):", type=["pdf"])

st.markdown("---")

if st.button("🚀 Run Full Analysis", type="primary", use_container_width=True):
    if not client:
        st.error("❌ API key is not configured. Check the sidebar.")
        st.stop()
    if not jd.strip():
        st.warning("⚠️ Please paste the Job Description.")
        st.stop()
    if not pdf_file:
        st.warning("⚠️ Please upload your Resume PDF.")
        st.stop()

    with st.spinner("🧠 Analyzing your profile against the JD..."):
        resume_text = extract_pdf_text(pdf_file)
        if not resume_text.strip():
            st.error("Could not read the PDF. Please try a different file.")
            st.stop()

        raw = call_gemini(resume_text, jd, PROMPT)
        if not raw:
            st.error("❌ All Gemini models failed. Please check your API key and try again.")
            st.stop()

        data = parse_json(raw)
        if not data:
            st.error("❌ Could not parse the AI response. Please try again.")
            with st.expander("Raw AI Output (for debugging)"):
                st.code(raw)
            st.stop()

    st.success("✅ Analysis Complete!")
    st.markdown("---")

    # ── METRICS ──
    m1, m2, m3 = st.columns(3)
    m1.metric("🎯 Overall Match", f"{data.get('match', 0)}%")
    m2.metric("✔️ Skills Detected", len(data.get('skills', [])))
    m3.metric("⚠️ Critical Gaps", len(data.get('gaps', [])))

    st.markdown("---")

    # ── CHART + SKILLS ──
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📈 Skill Competency Breakdown")
        scores = data.get('scores', {})
        if scores:
            df = pd.DataFrame({"Skill": list(scores.keys()), "Score": list(scores.values())})
            fig = go.Figure(go.Bar(
                x=df["Score"], y=df["Skill"], orientation="h",
                marker=dict(color=["#4361ee", "#3a0ca3", "#7209b7", "#f72585"]),
                text=df["Score"], textposition="outside"
            ))
            fig.update_layout(
                xaxis=dict(range=[0, 100]),
                height=280,
                margin=dict(l=10, r=30, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("✔️ Top Skills Found")
        for s in data.get('skills', []):
            st.success(f"  {s}")
        st.subheader("⚠️ Skill Gaps")
        for g in data.get('gaps', []):
            st.warning(f"  {g}")

    # ── PRESCRIPTIVE INTERVIEW PREP ──
    st.markdown("---")
    st.subheader("🎯 Prescriptive Analytics: Strategic Interview Prep")
    st.caption("Based on your gaps, here are the questions you are likely to face — and how to prepare.")
    for i, q in enumerate(data.get('questions', []), 1):
        with st.expander(f"Question {i}: AI-Predicted Interview Question"):
            st.write(f"**{q}**")
            st.markdown("> 💡 **Pro Tip for Babu:** Connect this to your experience as a Technical Process Executive. Show the business impact, not just technical knowledge.")

    # ── FINAL VERDICT ──
    st.markdown("---")
    st.subheader("📝 Final Recommendation")
    st.info(f"**{data.get('verdict', '')}**")
    st.caption("Powered by Google Gemini | Developed by Babu as a Data Analytics Portfolio Project")
