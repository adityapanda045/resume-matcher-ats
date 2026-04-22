import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf

# 1. SECURE CONFIGURATION
# Using the Secret Manager for security
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def get_gemini_reponse(input_text, system_prompt):
    # Using 'gemini-1.5-flash' which is the 2026 standard for speed and reliability
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Combining instructions and data into a single clear 'Content' block
    response = model.generate_content([system_prompt, input_text])
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += str(reader.pages[page].extract_text())
    return text

# --- STREAMLIT UI ---
st.set_page_config(page_title="Babu's Smart AI-ATS", layout="wide")
st.title("🤖 Smart AI Resume Analyst (Enterprise Version)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Job Description")
    jd_text = st.text_area("Paste the Full Job Description here:", height=200, help="The AI needs this to find the requirements.")

with col2:
    st.subheader("📄 Candidate Resume")
    uploaded_file = st.file_uploader("Upload Resume (PDF format)", type="pdf", help="Please upload a clear PDF file.")

# --- PROFESSIONAL HR PROMPT ---
input_prompt = """
You are an expert Technical Recruiter with 15 years of experience at top firms like Infosys and Google. 
Your task is to analyze the Resume against the Job Description.

Please provide a detailed response in the following structure:
1. **Match Percentage**: A realistic score (0-100%).
2. **Top 5 Required Skills**: Extracted from the JD.
3. **Candidate Gaps**: What is missing or needs improvement?
4. **Final Verdict**: Should the HR move forward? (2 sentences).

Be professional, objective, and clear.
"""

if st.button("Run AI Analysis", type="primary"):
    # VALIDATION: This prevents the 'InvalidArgument' error
    if uploaded_file is not None and jd_text.strip() != "":
        with st.spinner('🔍 AI is scanning the resume against JD...'):
            try:
                resume_content = input_pdf_text(uploaded_file)
                # Orchestrating the API call
                analysis = get_gemini_reponse(resume_content, jd_text + "\n\n" + input_prompt)
                
                st.markdown("---")
                st.write("### 📊 AI Analysis Report")
                st.info(analysis)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.error("⚠️ Error: Please ensure you have pasted a Job Description AND uploaded a Resume PDF.")
