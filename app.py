import streamlit as st

st.set_page_config(
    page_title="GrailAI — Career Intelligence Platform",
    layout="wide",
    page_icon="🏆"
)

from google import genai
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
        return genai.Client(api_key=key)
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

def call_gemini(prompt):
    models = ["gemini-2.0-flash-lite", "gemini-2.0-flash", "gemini-2.5-flash", "gemini-flash-latest"]
    last_error = ""
    for model_name in models:
        try:
            response = client.models.generate_content(model=model_name, contents=prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            continue
    return None

def parse_json(text):
    try:
        m = re.search(r'\{.*\}', text, re.DOTALL)
        return json.loads(m.group()) if m else None
    except Exception:
        return None

# ─────────────────────────────────────────
# PROMPTS
# ─────────────────────────────────────────
ANALYSIS_PROMPT = """
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

JOB DESCRIPTION:
{jd}

RESUME:
{resume}
"""

SCORE_ANSWER_PROMPT = """
You are an expert interview coach. A candidate answered an interview question.
Score their answer and give specific feedback.

Interview Question: {question}
Candidate's Answer: {answer}
Job they are applying for: {jd_summary}

Return ONLY a valid JSON object:
{{
  "score": <integer 1-10>,
  "strength": "<one sentence on what was good about the answer>",
  "improvement": "<one specific sentence on what to improve>",
  "ideal_answer_hint": "<one sentence hint about what a perfect answer looks like>"
}}
"""

FINAL_COACHING_PROMPT = """
You are an expert career coach. A candidate just completed a mock interview with 3 questions.
Based on their scores and answers, give a final coaching report.

Questions and scores:
{qa_summary}

Return ONLY a valid JSON object:
{{
  "readiness_score": <integer 0-100>,
  "overall_feedback": "<2-3 sentences of overall assessment>",
  "top_strength": "<their biggest strength shown in the interview>",
  "top_improvement": "<the single most important thing to work on>",
  "confidence_message": "<one encouraging sentence to boost their confidence>"
}}
"""

# ─────────────────────────────────────────
# UI — PREMIUM DARK GLASSMORPHISM THEME
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

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
.main-title {
    font-size: 2.8rem; font-weight: 800;
    background: linear-gradient(90deg, #f72585, #7209b7, #4361ee);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; margin-bottom: 0.2rem;
}
.main-subtitle {
    text-align: center; color: rgba(255,255,255,0.5);
    font-size: 0.9rem; margin-bottom: 2rem; letter-spacing: 1px;
}
.interview-card {
    background: rgba(247,37,133,0.08);
    border: 1px solid rgba(247,37,133,0.3);
    border-radius: 16px; padding: 24px; margin: 12px 0;
    box-shadow: 0 8px 32px rgba(247,37,133,0.1);
}
.question-box {
    background: rgba(255,255,255,0.07);
    border-left: 4px solid #f72585;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px; margin: 12px 0;
    font-size: 1.1rem; font-weight: 600; color: white;
}
.score-badge {
    display: inline-block;
    background: linear-gradient(90deg, #f72585, #7209b7);
    color: white; border-radius: 50px;
    padding: 6px 18px; font-weight: 700; font-size: 1rem;
}
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.07) !important;
    backdrop-filter: blur(20px); border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.12);
    padding: 20px !important; box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.6) !important; font-size: 0.85rem !important; }
[data-testid="stMetricValue"] { color: #f72585 !important; font-weight: 800 !important; font-size: 2rem !important; }
.stButton > button {
    background: linear-gradient(90deg, #f72585, #7209b7, #4361ee) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; padding: 14px 32px !important;
    font-size: 1.1rem !important; font-weight: 700 !important;
    box-shadow: 0 4px 24px rgba(247,37,133,0.4) !important;
    transition: all 0.3s ease !important; width: 100%;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 32px rgba(247,37,133,0.6) !important; }
.stTextArea textarea { background: rgba(255,255,255,0.05) !important; color: white !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 12px !important; }
.stTextArea label, .stFileUploader label { color: rgba(255,255,255,0.7) !important; font-weight: 600 !important; }
h2, h3 { color: white !important; }
.stSuccess { background: rgba(0,255,136,0.1) !important; border: 1px solid rgba(0,255,136,0.3) !important; border-radius: 10px !important; }
.stWarning { background: rgba(255,171,0,0.1) !important; border: 1px solid rgba(255,171,0,0.3) !important; border-radius: 10px !important; }
.stInfo { background: rgba(67,97,238,0.15) !important; border: 1px solid rgba(67,97,238,0.4) !important; border-radius: 10px !important; color: white !important; }
.streamlit-expanderHeader { background: rgba(255,255,255,0.07) !important; border-radius: 10px !important; color: white !important; border: 1px solid rgba(255,255,255,0.1) !important; }
.streamlit-expanderContent { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.08) !important; color: rgba(255,255,255,0.85) !important; }
hr { border-color: rgba(255,255,255,0.1) !important; }
p, span, div { color: rgba(255,255,255,0.85); }
.stSpinner > div { border-top-color: #f72585 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────
for key in ["analysis_data", "interview_started", "current_q", "answers",
            "scores_feedback", "interview_done", "resume_text", "jd_text"]:
    if key not in st.session_state:
        st.session_state[key] = None if key in ["analysis_data", "resume_text", "jd_text"] else \
                                  False if key in ["interview_started", "interview_done"] else \
                                  0 if key == "current_q" else []

# ─────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────
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
    st.markdown("### 🗺️ Features")
    st.write("✅ Resume-JD Match Score")
    st.write("✅ Skill Gap Analysis")
    st.write("✅ Competency Chart")
    st.write("🆕 **Mock Interview Simulator**")
    st.write("🆕 **Interview Readiness Score**")
    st.markdown("---")
    st.info("GrailAI uses NLP + Gemini AI to analyze resume-JD fit and simulate real interviews.")
    if client:
        st.success("✅ API Connected")
    else:
        st.error("❌ API Not Connected")

# ─────────────────────────────────────────
# SECTION 1: RESUME ANALYSIS
# ─────────────────────────────────────────
st.markdown("## 📊 Step 1: Resume Analysis")
col1, col2 = st.columns(2)
with col1:
    st.subheader("📋 Job Description")
    jd = st.text_area("Paste the Job Description here:", height=200,
                       placeholder="e.g. We are looking for a Data Analyst with Python, SQL, Power BI...")
with col2:
    st.subheader("📄 Resume Upload")
    pdf_file = st.file_uploader("Upload your Resume (PDF only):", type=["pdf"])

st.markdown("---")

if st.button("🚀 Run Full Analysis", type="primary", use_container_width=True):
    if not client:
        st.error("❌ API key not configured.")
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
            st.error("Could not read the PDF.")
            st.stop()

        full_prompt = ANALYSIS_PROMPT.format(jd=jd, resume=resume_text)
        raw = call_gemini(full_prompt)
        if not raw:
            st.error("❌ All Gemini models failed. Check your API key.")
            st.stop()

        data = parse_json(raw)
        if not data:
            st.error("❌ Could not parse AI response. Try again.")
            with st.expander("Raw AI Output"):
                st.code(raw)
            st.stop()

    # Save to session state for mock interview
    st.session_state.analysis_data = data
    st.session_state.resume_text = resume_text
    st.session_state.jd_text = jd
    st.session_state.interview_started = False
    st.session_state.current_q = 0
    st.session_state.answers = []
    st.session_state.scores_feedback = []
    st.session_state.interview_done = False

# ─────────────────────────────────────────
# SHOW ANALYSIS RESULTS
# ─────────────────────────────────────────
if st.session_state.analysis_data:
    data = st.session_state.analysis_data

    st.success("✅ Analysis Complete!")
    st.markdown("---")

    m1, m2, m3 = st.columns(3)
    m1.metric("🎯 Overall Match", f"{data.get('match', 0)}%")
    m2.metric("✔️ Skills Detected", len(data.get('skills', [])))
    m3.metric("⚠️ Critical Gaps", len(data.get('gaps', [])))

    st.markdown("---")
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
            fig.update_layout(xaxis=dict(range=[0, 100]), height=280,
                              margin=dict(l=10, r=30, t=10, b=10),
                              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font=dict(color="white"))
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("✔️ Top Skills Found")
        for s in data.get('skills', []):
            st.success(f"  {s}")
        st.subheader("⚠️ Skill Gaps")
        for g in data.get('gaps', []):
            st.warning(f"  {g}")

    st.markdown("---")
    st.subheader("🎯 Predicted Interview Questions")
    st.caption("These are the questions the recruiter is LIKELY to ask you based on your gaps.")
    for i, q in enumerate(data.get('questions', []), 1):
        with st.expander(f"Question {i}: {q[:60]}..."):
            st.write(f"**{q}**")
            st.markdown("> 💡 **Tip:** Connect your answer to your experience as a Technical Process Executive.")

    st.markdown("---")
    st.info(f"**📝 Recommendation:** {data.get('verdict', '')}")

    # ─────────────────────────────────────────
    # SECTION 2: MOCK INTERVIEW SIMULATOR
    # ─────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 🎤 Step 2: Mock Interview Simulator")
    st.markdown("""
    <div class='interview-card'>
        <h3 style='color:#f72585; margin:0'>🆕 India's First AI Mock Interview</h3>
        <p style='margin:8px 0 0 0; color:rgba(255,255,255,0.8)'>
        The AI will ask you the 3 predicted questions one by one. Type your answer.
        You will get a score (1-10) + specific feedback for each answer.
        At the end, you receive your <b>Interview Readiness Score</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    questions = data.get('questions', [])

    if not st.session_state.interview_started and not st.session_state.interview_done:
        if st.button("🎤 Start Mock Interview", use_container_width=True):
            st.session_state.interview_started = True
            st.session_state.current_q = 0
            st.session_state.answers = []
            st.session_state.scores_feedback = []
            st.rerun()

    # ── ACTIVE INTERVIEW ──
    if st.session_state.interview_started and not st.session_state.interview_done:
        q_index = st.session_state.current_q
        total = len(questions)

        st.markdown(f"### Question {q_index + 1} of {total}")
        progress = (q_index) / total
        st.progress(progress)

        # Show previous answered questions
        for i, (prev_q, prev_a, prev_fb) in enumerate(zip(
            questions[:q_index],
            st.session_state.answers,
            st.session_state.scores_feedback
        )):
            with st.expander(f"✅ Q{i+1} — Answered (Score: {prev_fb.get('score', '?')}/10)"):
                st.markdown(f"**Question:** {prev_q}")
                st.markdown(f"**Your Answer:** {prev_a}")
                score = prev_fb.get('score', 0)
                color = "#00ff88" if score >= 7 else "#ffab00" if score >= 4 else "#f72585"
                st.markdown(f"<span class='score-badge'>Score: {score}/10</span>", unsafe_allow_html=True)
                st.success(f"💪 Strength: {prev_fb.get('strength', '')}")
                st.warning(f"🎯 Improve: {prev_fb.get('improvement', '')}")
                st.info(f"💡 Ideal Answer Hint: {prev_fb.get('ideal_answer_hint', '')}")

        if q_index < total:
            current_question = questions[q_index]
            st.markdown(f"<div class='question-box'>🎤 {current_question}</div>", unsafe_allow_html=True)

            answer = st.text_area(
                "Your Answer:",
                height=150,
                placeholder="Type your answer here... Speak naturally as if in a real interview.",
                key=f"answer_{q_index}"
            )

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button(f"✅ Submit Answer", use_container_width=True):
                    if not answer.strip():
                        st.warning("Please type your answer first.")
                    else:
                        with st.spinner("🧠 Scoring your answer..."):
                            score_prompt = SCORE_ANSWER_PROMPT.format(
                                question=current_question,
                                answer=answer,
                                jd_summary=st.session_state.jd_text[:300]
                            )
                            score_raw = call_gemini(score_prompt)
                            feedback = parse_json(score_raw) if score_raw else {
                                "score": 5, "strength": "Answer submitted",
                                "improvement": "Be more specific",
                                "ideal_answer_hint": "Use STAR method"
                            }

                        st.session_state.answers.append(answer)
                        st.session_state.scores_feedback.append(feedback)
                        st.session_state.current_q += 1

                        if st.session_state.current_q >= total:
                            st.session_state.interview_done = True
                            st.session_state.interview_started = False
                        st.rerun()

            with col_b:
                if st.button("⏭️ Skip Question", use_container_width=True):
                    st.session_state.answers.append("(Skipped)")
                    st.session_state.scores_feedback.append({
                        "score": 0, "strength": "Question skipped",
                        "improvement": "Practice this question before your real interview",
                        "ideal_answer_hint": "Never skip this in a real interview"
                    })
                    st.session_state.current_q += 1
                    if st.session_state.current_q >= total:
                        st.session_state.interview_done = True
                        st.session_state.interview_started = False
                    st.rerun()

    # ── INTERVIEW COMPLETE — FINAL REPORT ──
    if st.session_state.interview_done:
        st.markdown("---")
        st.markdown("## 🏆 Interview Readiness Report")

        questions = data.get('questions', [])
        answers = st.session_state.answers
        scores_fb = st.session_state.scores_feedback

        # Show all Q&A
        total_score = sum(f.get('score', 0) for f in scores_fb)
        avg_score = round(total_score / len(scores_fb)) if scores_fb else 0

        for i, (q, a, fb) in enumerate(zip(questions, answers, scores_fb), 1):
            with st.expander(f"Q{i} — Score: {fb.get('score', 0)}/10"):
                st.markdown(f"**Question:** {q}")
                st.markdown(f"**Your Answer:** {a}")
                st.success(f"💪 {fb.get('strength', '')}")
                st.warning(f"🎯 {fb.get('improvement', '')}")
                st.info(f"💡 {fb.get('ideal_answer_hint', '')}")

        # Get final coaching report
        with st.spinner("Generating your final coaching report..."):
            qa_summary = "\n".join([
                f"Q{i+1}: {q}\nAnswer: {a}\nScore: {fb.get('score', 0)}/10"
                for i, (q, a, fb) in enumerate(zip(questions, answers, scores_fb))
            ])
            coaching_raw = call_gemini(FINAL_COACHING_PROMPT.format(qa_summary=qa_summary))
            coaching = parse_json(coaching_raw) if coaching_raw else None

        st.markdown("---")
        readiness = coaching.get('readiness_score', avg_score * 10) if coaching else avg_score * 10

        r1, r2 = st.columns(2)
        r1.metric("🎯 Interview Readiness Score", f"{readiness}%")
        r2.metric("📊 Avg Answer Score", f"{avg_score}/10")

        if coaching:
            st.markdown("---")
            st.subheader("📋 AI Coaching Report")
            st.info(f"**Overall Assessment:** {coaching.get('overall_feedback', '')}")
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"💪 **Your Biggest Strength:**\n{coaching.get('top_strength', '')}")
            with col2:
                st.warning(f"🎯 **#1 Thing to Improve:**\n{coaching.get('top_improvement', '')}")
            st.markdown(f"""
            <div class='interview-card' style='text-align:center'>
                <h3 style='color:#f72585'>💬 Coach's Message</h3>
                <p style='font-size:1.1rem'>{coaching.get('confidence_message', 'You are on the right track!')}</p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🔄 Restart Mock Interview", use_container_width=True):
            st.session_state.interview_started = False
            st.session_state.interview_done = False
            st.session_state.current_q = 0
            st.session_state.answers = []
            st.session_state.scores_feedback = []
            st.rerun()

    st.markdown("---")
    st.caption("🏆 GrailAI — Powered by Google Gemini | Built by Aditya | India's Career Intelligence Platform")
