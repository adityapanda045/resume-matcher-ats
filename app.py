import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf

# 1. SETUP THE BRAIN (API Key)
# In a real job, you'd hide this. For now, we are 'Orchestrating' the AI.
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def get_gemini_reponse(input_text, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, prompt])
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += str(reader.pages[page].extract_text())
    return text

# --- STREAMLIT UI ---
st.set_page_config(page_title="Babu's AI-ATS", layout="wide")
st.title("🤖 Smart AI Resume Analyst")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Job Description")
    jd_text = st.text_area("Paste the Full Job Description here:", height=200)

with col2:
    st.subheader("📄 Candidate Resume")
    uploaded_file = st.file_uploader("Upload Resume (PDF format)", type="pdf")

# --- THE SYSTEM PROMPT (Your 'Expert' Instruction) ---
# This is where your 'Prompt Engineering' skill shows!
input_prompt = """
As an experienced Technical Recruiter, analyze the provided Job Description and Resume. 
1. Extract the top 5 mandatory technical skills from the JD.
2. Check if the candidate possesses these or related skills (Semantic Matching).
3. Provide a 'Match Percentage'.
4. List 'Missing Skills' and a 2-sentence 'Recruiter's Feedback'.
Format the output clearly.
"""

if st.button("Run AI Analysis", type="primary"):
    if uploaded_file is not None and jd_text != "":
        resume_content = input_pdf_text(uploaded_file)
        
        # Combine the data for the AI
        combined_data = f"JOB DESCRIPTION: {jd_text} \n\n RESUME: {resume_content}"
        
        with st.spinner('AI is analyzing the ' + uploaded_file.name + '...'):
            analysis = get_gemini_reponse(combined_data, input_prompt)
            st.markdown("---")
            st.write("### 📊 AI Analysis Report")
            st.info(analysis)
    else:
        st.warning("Please provide both a JD and a Resume.")
