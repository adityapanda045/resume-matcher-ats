import streamlit as st
import sys

st.set_page_config(page_title="Babu's Diagnostic Tool")

st.title("🛠️ Babu's ATS Diagnostic Mode")
st.write("If you can see this, the app is **CONNECTED** and working!")

st.header("1. System Information")
st.write(f"Python Version: {sys.version}")

st.header("2. Library Check")
libraries = ["google.generativeai", "pypdf", "plotly", "pandas", "pydantic"]

for lib in libraries:
    try:
        __import__(lib)
        st.success(f"✅ {lib} is installed and working.")
    except ImportError as e:
        st.error(f"❌ {lib} is NOT installed. Error: {e}")
    except Exception as e:
        st.warning(f"⚠️ {lib} has a conflict: {e}")

st.header("3. Secrets Check")
if "GOOGLE_API_KEY" in st.secrets:
    st.success("✅ GOOGLE_API_KEY is found in Secrets.")
else:
    st.error("❌ GOOGLE_API_KEY is missing from Secrets.")

st.info("Babu, if all of these are GREEN, then the 'Oh no' was caused by a coding bug. If any are RED, we found the problem!")
