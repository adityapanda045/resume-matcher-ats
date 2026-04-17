import streamlit as st

st.set_page_config(page_title="Dynamic ATS Matcher", layout="wide")
st.title("🚀 Dynamic ATS Resume Matcher")
st.markdown("---")

# --- INTERACTIVE DASHBOARD DESIGN ---
# Creating two columns to put Job details on the left, Resume on the right
col1, col2 = st.columns(2)

with col1:
    st.write("### 1. Job Requirements")
    job_title = st.text_input("Job Title:", value="Data Analyst")
    
    # This lets you type ANY skills you want on the live website!
    skills_input = st.text_input("Required Skills (comma separated):", value="python, sql, excel, communication")
    
with col2:
    st.write("### 2. Candidate Info")
    resume_text = st.text_area("Paste Candidate Resume Text:", height=150, value="Name: Babu. Skills: Python, SQL, Technical Process, Excel.")

# --- THE LOGIC ENGINE ---
# This line turns your comma-separated text into a clean Python list
required_skills = [skill.strip().lower() for skill in skills_input.split(",")]

# When the user clicks the button, the magic happens
if st.button("Calculate Match Score", type="primary"):
    st.markdown("---")
    st.write(f"### Match Results for: {job_title}")
    
    score = 0
    matched_skills = []
    missing_skills = []
    
    # The Loop checking the text
    for skill in required_skills:
        if skill in resume_text.lower():
            score += 1
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
            
    # The Math
    if len(required_skills) > 0:
        percentage = round((score / len(required_skills)) * 100, 2)
    else:
        percentage = 0
        
    # --- VISUAL RESULTS ---
    # st.metric creates a beautiful, large number card
    st.metric(label="Overall Match Score", value=f"{percentage}%")
    
    # Show exactly what matched and what didn't
    st.success(f"**✅ Skills Found:** {', '.join(matched_skills).title()}")
    st.error(f"**❌ Skills Missing:** {', '.join(missing_skills).title()}")
