# AI Resume Analyzer and Job Recommendation System

## Project Objective

This project is an NLP-based resume analyzer that helps students understand how well their resume matches selected job roles.

The system:

- Accepts PDF and DOCX resumes
- Extracts and cleans resume text
- Detects technical skills
- Compares a resume with predefined job roles
- Calculates match scores
- Recommends top job roles
- Identifies missing skills
- Generates a learning roadmap
- Provides a Streamlit dashboard

---

## Features

- PDF and DOCX resume upload
- Resume text extraction
- Text cleaning and normalization
- Technical skill detection
- Five predefined job roles
- TF-IDF and cosine similarity matching
- Skill-overlap score calculation
- Top three job recommendations
- Missing skill analysis
- Rule-based learning roadmap
- Downloadable text report
- Responsible AI disclaimer

---

## Supported Job Roles

1. Data Analyst
2. Machine Learning Engineer
3. AI Engineer
4. NLP Engineer
5. Computer Vision Engineer

---

## Technologies Used

- Python
- Streamlit
- pypdf
- python-docx
- Pandas
- Scikit-learn
- Plotly
- TF-IDF
- Cosine Similarity
- Regular Expressions

---

## Project Structure

```text
ai_resume_analyzer/
│
├── app.py
├── resume_parser.py
├── text_cleaner.py
├── skill_extractor.py
├── job_matcher.py
├── roadmap_generator.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── data/
│   ├── job_roles.csv
│   └── skill_dictionary.csv
│
├── sample_resumes/
├── reports/
│
└── tests/
    └── test_cases.csv