import io

import pandas as pd
import plotly.express as px
import streamlit as st

from job_matcher import analyze_all_roles, get_role_analysis
from resume_parser import extract_resume_text
from roadmap_generator import generate_roadmap
from skill_extractor import (
    extract_skills,
    group_skills_by_category,
    load_skill_dictionary,
)
from text_cleaner import clean_resume_text


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
)

st.title("AI Resume Analyzer and Job Recommendation System")
st.caption(
    "Educational guidance only. Match scores are estimates, not hiring decisions."
)

st.info(
    "This tool analyzes job-related skills mentioned in the resume. "
    "It does not use gender, age, religion, nationality, photo, marital status, "
    "disability, or other protected personal information."
)

try:
    skill_df = load_skill_dictionary("data/skill_dictionary.csv")
    job_roles_df = pd.read_csv("data/job_roles.csv")
except FileNotFoundError as error:
    st.error(f"Required data file not found: {error}")
    st.stop()

with st.sidebar:
    st.header("Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload a PDF or DOCX resume",
        type=["pdf", "docx"],
        help="Only PDF and DOCX files are supported.",
    )

    st.markdown("---")
    st.subheader("About the score")
    st.write(
        "Final Score = 70% Skill Match + 30% TF-IDF Text Similarity"
    )

    st.write(
        "A missing keyword does not always mean that you do not have that skill. "
        "You may need to add truthful skill details to your resume."
    )

if uploaded_file is None:
    st.subheader("How to use this application")
    st.write(
        "1. Upload a PDF or DOCX resume from the sidebar."
        "2. Select a target job role."
        "3. View detected skills, match scores, missing skills, and a roadmap."
    )

    st.subheader("Supported Job Roles")
    st.dataframe(
        job_roles_df[["role", "description"]],
        use_container_width=True,
        hide_index=True,
    )

    st.stop()

file_size_mb = uploaded_file.size / (1024 * 1024)

if file_size_mb > 10:
    st.error("File size must be smaller than 10 MB.")
    st.stop()

try:
    raw_resume_text = extract_resume_text(uploaded_file)
except Exception as error:
    st.error(f"Could not extract text from this file: {error}")
    st.stop()

cleaned_resume_text = clean_resume_text(raw_resume_text)

if not cleaned_resume_text.strip():
    st.error(
        "No readable text was found in this resume. "
        "The file may be scanned or image-based. Use a text-based PDF or DOCX file."
    )
    st.stop()

detected_skills = extract_skills(cleaned_resume_text, skill_df)
skills_by_category = group_skills_by_category(detected_skills, skill_df)

role_results = analyze_all_roles(
    resume_text=cleaned_resume_text,
    detected_skills=detected_skills,
    job_roles_df=job_roles_df,
)

role_names = job_roles_df["role"].tolist()

st.sidebar.subheader("Target Role")
selected_role = st.sidebar.selectbox(
    "Choose the role you want to analyze",
    options=role_names,
)

selected_role_result = get_role_analysis(role_results, selected_role)

st.success(
    f"Uploaded: {uploaded_file.name} | File size: {file_size_mb:.2f} MB"
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Dashboard",
        "Detected Skills",
        "Resume Text",
        "Download Report",
    ]
)

with tab1:
    st.header("Resume Analysis Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Target Role",
        selected_role_result["role"],
    )

    col2.metric(
        "Target Match Score",
        f"{selected_role_result['final_score']}%",
    )

    col3.metric(
        "Skills Detected",
        len(detected_skills),
    )

    st.subheader("Role Match Scores")

    chart_df = role_results[["role", "final_score"]].copy()
    chart_df = chart_df.sort_values("final_score", ascending=False)

    fig = px.bar(
        chart_df,
        x="role",
        y="final_score",
        color="final_score",
        text="final_score",
        color_continuous_scale="Blues",
        labels={
            "role": "Job Role",
            "final_score": "Match Score (%)",
        },
        title="Resume-to-Role Match Scores",
    )

    fig.update_layout(
        yaxis_range=[0, 100],
        coloraxis_showscale=False,
        xaxis_title="Job Role",
        yaxis_title="Match Score (%)",
    )

    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")

    st.plotly_chart(fig, use_container_width=True)

with st.expander("Debug: View all role scores and matched skills"):
    debug_df = role_results[
        [
            "role",
            "required_skills",
            "matched_skills",
            "missing_skills",
            "skill_score",
            "text_similarity_score",
            "final_score",
        ]
    ]

    st.dataframe(
        debug_df,
        use_container_width=True,
    )

    top_roles = role_results.head(3).copy()
    top_roles.index = range(1, len(top_roles) + 1)

    st.dataframe(
        top_roles[
            [
                "role",
                "final_score",
                "skill_score",
                "text_similarity_score",
            ]
        ].rename(
            columns={
                "role": "Job Role",
                "final_score": "Final Score (%)",
                "skill_score": "Skill Match (%)",
                "text_similarity_score": "Text Similarity (%)",
            }
        ),
        use_container_width=True,
    )

    st.subheader(f"Skill-Gap Analysis: {selected_role}")

    left_column, right_column = st.columns(2)

    with left_column:
        st.markdown("### Skills Found for This Role")

        if selected_role_result["matched_skills"]:
            for skill in selected_role_result["matched_skills"]:
                st.success(skill.title())
        else:
            st.warning("No required skills were found for this role.")

    with right_column:
        st.markdown("### Missing Skills")

        if selected_role_result["missing_skills"]:
            for skill in selected_role_result["missing_skills"]:
                st.warning(skill.title())
        else:
            st.success("Excellent! All listed required skills were found.")

    st.subheader("Learning Roadmap")

    roadmap = generate_roadmap(selected_role_result["missing_skills"])

    if roadmap:
        roadmap_df = pd.DataFrame(roadmap)
        roadmap_df.index = roadmap_df.index + 1

        st.dataframe(
            roadmap_df.rename(
                columns={
                    "week": "Week",
                    "skill": "Missing Skill",
                    "learning_topic": "Suggested Learning Topic",
                }
            ),
            use_container_width=True,
        )
    else:
        st.success(
            "No roadmap is needed for the listed skills. "
            "You can improve your projects, portfolio, and interview preparation."
        )

with tab2:
    st.header("Detected Skills")

    if detected_skills:
        st.write(
            "The following skills were detected from the uploaded resume:"
        )

        for category, category_skills in skills_by_category.items():
            st.subheader(category.title())
            st.write(", ".join(skill.title() for skill in category_skills))
    else:
        st.warning(
            "No skills from the current skill dictionary were detected. "
            "You can improve the dictionary by adding more skills and synonyms."
        )

    st.subheader("All Detected Skills")

    skills_display_df = pd.DataFrame(
        {"Detected Skills": [skill.title() for skill in detected_skills]}
    )

    st.dataframe(
        skills_display_df,
        use_container_width=True,
        hide_index=True,
    )

with tab3:
    st.header("Extracted Resume Text")

    st.text_area(
        "Cleaned resume text",
        value=cleaned_resume_text,
        height=450,
    )

with tab4:
    st.header("Download Analysis Report")

    report_lines = [
        "AI RESUME ANALYZER AND JOB RECOMMENDATION SYSTEM",
        "=" * 55,
        "",
        f"Uploaded Resume: {uploaded_file.name}",
        f"Selected Target Role: {selected_role}",
        f"Target Role Match Score: {selected_role_result['final_score']}%",
        "",
        "DISCLAIMER",
        "This report is for educational guidance only.",
        "Scores are estimates and are not hiring decisions.",
        "Missing keywords do not always mean missing ability.",
        "",
        "DETECTED SKILLS",
        ", ".join(skill.title() for skill in detected_skills)
        if detected_skills
        else "No skills detected.",
        "",
        "TOP 3 RECOMMENDED ROLES",
    ]

    for index, row in role_results.head(3).iterrows():
        report_lines.append(
            f"{index + 1}. {row['role']} - {row['final_score']}%"
        )

    report_lines.extend(
        [
            "",
            f"SKILL-GAP ANALYSIS FOR {selected_role.upper()}",
            "",
            "MATCHED SKILLS",
        ]
    )

    if selected_role_result["matched_skills"]:
        report_lines.extend(
            f"- {skill.title()}"
            for skill in selected_role_result["matched_skills"]
        )
    else:
        report_lines.append("- No required skills matched.")

    report_lines.extend(["", "MISSING SKILLS"])

    if selected_role_result["missing_skills"]:
        report_lines.extend(
            f"- {skill.title()}"
            for skill in selected_role_result["missing_skills"]
        )
    else:
        report_lines.append("- No missing skills from the current role dataset.")

    report_lines.extend(["", "SUGGESTED LEARNING ROADMAP"])

    if roadmap:
        for item in roadmap:
            report_lines.append(
                f"Week {item['week']}: "
                f"{item['skill'].title()} - "
                f"{item['learning_topic']}"
            )
    else:
        report_lines.append(
            "Continue improving projects, portfolio, and interview skills."
        )

    report_text = "".join(report_lines)

    st.download_button(
        label="Download Analysis Report (.txt)",
        data=io.BytesIO(report_text.encode("utf-8")),
        file_name="resume_analysis_report.txt",
        mime="text/plain",
    )

    st.text_area(
        "Report Preview",
        value=report_text,
        height=450,
    )