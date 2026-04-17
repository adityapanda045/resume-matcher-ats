import streamlit as st

# --- YOUR DATA ---
my_project_files = {
    "JD_Data_Analyst.txt": "Skills: Python, SQL, Power BI, Excel. Location: Pune.",
    "JD_Web_Developer.txt": "Skills: HTML, CSS, JavaScript, Flask. Role: Backend.",
    "JD_Process_Executive.txt": "Skills: Operations, Management, Reporting, Excel.",
    "JD_Python_Dev.txt": "Skills: Python, Django, APIs, PostgreSQL.",
    "JD_Machine_Learning.txt": "Skills: Python, Scikit-learn, Statistics, Math."
}

required_skills = ["python", "sql", "excel", "communication", "management"]

# --- THE DESIGN ---
st.set_page_config(page_title="Resume Matcher", layout="wide")
st.title("🚀 ATS Resume Ranking System")
st.markdown("---")

# --- THE INPUT ---
st.write("### Test Candidate Output")
st.write("Paste the candidate's resume text below to run the matching logic.")

# Instead of reading local files, we let the user paste the text!
resume_text = st.text_area("Candidate Resume Text:", value="Name: Babu. Skills: Python, SQL, Technical Process, Excel.")

if st.button("Calculate Match Score"):
    
    st.markdown("### Match Results against Job Descriptions")
    
    results = []
    
    # --- YOUR LOGIC ---
    for jd_name, jd_text in my_project_files.items():
        score = 0
        for skill in required_skills:
            if skill.lower() in resume_text.lower():
                score = score + 1
                
        percentage = round((score / len(required_skills)) * 100, 2)
        results.append({"Job": jd_name.replace(".txt", ""), "Score": f"{percentage}%"})
        
    # --- VISUAL OUTPUT ---
    sorted_results = sorted(results, key=lambda x: float(x['Score'].strip('%')), reverse=True)
    st.table(sorted_results)
