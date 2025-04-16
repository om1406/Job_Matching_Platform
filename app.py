import streamlit as st
import pandas as pd
from resume_parser import parse_resume
from job_parser import load_jobs
from recommender import recommend_jobs_bert
from utils import clean_text, generate_skill_gap

st.set_page_config(page_title="AI Job Matcher", layout="wide")
st.title("🚀 AI Job Matching Platform")

# Sidebar filters
st.sidebar.header("🎛️ Filters")
stream = st.sidebar.selectbox("Select your stream", ['All', 'Data Science', 'Engineering', 'Finance', 'Marketing', 'Humanities', 'Others'])
top_n = st.sidebar.slider("Top N recommendations", 1, 20, 5)

uploaded_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    resume = parse_resume("temp_resume.pdf")
    name = resume.get("name", "Not Found")
    skills = resume.get("skills", [])
    raw_text = resume.get("raw_text", "")

    st.subheader("📄 Candidate Overview")
    st.markdown(f"**Name**: {name}")
    st.markdown(f"**Skills**: {', '.join(skills) if skills else 'Not Found'}")

    job_df = load_jobs("data/job_descriptions.csv")
    recommendations = recommend_jobs_bert(raw_text, job_df, top_n=top_n, stream=stream)

    st.subheader("📌 Recommended Jobs")
    if not recommendations.empty:
        st.dataframe(recommendations)

        csv = recommendations.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Recommendations as CSV", csv, "job_recommendations.csv", "text/csv")
    else:
        st.warning("No matching jobs found for the selected stream.")

    # Skill Gap Analysis
    if not job_df.empty and skills:
        st.subheader("📊 Skill Gap Analysis")
        matched_skills, missing_skills = generate_skill_gap(job_df, skills)

        st.markdown(f"**Matched Skills**: {', '.join(matched_skills)}")
        st.markdown(f"**Missing Skills**: {', '.join(missing_skills)}")
