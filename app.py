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
# UI
# ─────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stMetric"] {
    background: #ffffff;
    border-radius: 10px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.stButton button { width: 100%; }
</style>
""", unsafe_allow_html=True)

st.title("🏆 GrailAI — Career Intelligence Platform")
st.caption("AI-Powered Resume Analytics & Prescriptive Interview Prep | The Holy Grail of Career Tools")

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
