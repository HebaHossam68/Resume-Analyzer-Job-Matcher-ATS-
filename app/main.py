import streamlit as st
import requests
import pandas as pd

# =========================
# Page Config (Tab Name)
# =========================
st.set_page_config(
    page_title="AI Resume Analyzer & Job Matcher",
    page_icon="📄",
    layout="wide"
)

# =========================
# CSS Styling
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f4c75, #3282b8, #bbe1fa);
    color: white;

}

h1, h2, h3 {
    color: #00e5ff;
}

.card {
    background-color: rgba(255, 255, 255, 0.08);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.35);
    margin-bottom: 20px;
}

.stButton > button {
    background: linear-gradient(90deg, #00e5ff, #00bcd4);
    color: black;
    border-radius: 14px;
    height: 3em;
    font-size: 18px;
    font-weight: bold;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #00bcd4, #00e5ff);
    transform: scale(1.03);
}

[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Header
# =========================
st.markdown("""
<div class="card">
    <h1>🤖 AI Resume Analyzer & Job Matcher</h1>
    <p>
    Intelligent system that analyzes CVs, extracts skills, matches them with job requirements,
    and provides automated hiring recommendations using NLP & AI.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# Backend URL
# =========================
NGROK_URL = "NGROK_URL_HERE/analyze"

# =========================
# Inputs Section
# =========================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_cv = st.file_uploader("📄 Upload CV (PDF)", type=["pdf"])
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    job_description = st.text_area("🧾 Paste Job Description", height=180)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Analyze Button
# =========================
if st.button("🚀 Analyze CV"):
    if not uploaded_cv or not job_description:
        st.warning("⚠️ Please upload a CV and enter the Job Description first.")
    else:
        with st.spinner("🔍 Analyzing CV using AI..."):
            try:
                files = {
                    "cv_file": (
                        uploaded_cv.name,
                        uploaded_cv.getvalue(),
                        "application/pdf"
                    )
                }
                data = {"job_description": job_description}

                response = requests.post(
                    NGROK_URL,
                    files=files,
                    data=data,
                    timeout=180
                )

                if response.status_code == 200:
                    report = response.json()

                    # =========================
                    # Match Result
                    # =========================
                    st.markdown(f"""
                    <div class="card">
                        <h2>📊 Match Result</h2>
                        <h3>Match Score: {report.get('final_score', 'N/A')}%</h3>
                        <h3>Decision: {report.get('decision', 'N/A')}</h3>
                    </div>
                    """, unsafe_allow_html=True)

                    # =========================
                    # Matching Table
                    # =========================
                    matching_table = report.get("matching_table", [])
                    st.markdown('<div class="card"><h2>📌 Skill Matching</h2>', unsafe_allow_html=True)
                    if matching_table:
                        st.dataframe(pd.DataFrame(matching_table), use_container_width=True)
                    else:
                        st.write("No matching data available.")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # =========================
                    # Summary Table
                    # =========================
                    summary_table = report.get("summary_table", [])
                    st.markdown('<div class="card"><h2>📋 Summary</h2>', unsafe_allow_html=True)
                    if summary_table:
                        st.dataframe(pd.DataFrame(summary_table), use_container_width=True)
                    else:
                        st.write("No summary data available.")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # =========================
                    # Recommendation
                    # =========================
                    st.markdown(f"""
                    <div class="card">
                        <h2>🧠 AI Recommendation</h2>
                        <p>{report.get('recommendation', 'No recommendation available.')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # =========================
                    # Debug (اختياري)
                    # =========================
                    with st.expander("🛠 Debug Info"):
                        st.write("CV Skills:", report.get("__debug_cv_skills"))
                        st.write("JD Skills:", report.get("__debug_jd_skills"))
                        st.write("Raw Response:", response.text)

                else:
                    st.error(f"❌ Backend Error: {response.status_code}")

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Request failed: {e}")

# =========================
# Footer
# =========================
st.markdown("""
<hr>
<p style="text-align:center; color:#FFFFFF;">
Developed by Heba Hossam | AI Engineer 💙
</p>
""", unsafe_allow_html=True)
