# AI Resume Analyzer and Job Recommendation System

This app helps students check how well their resume matches the job roles they are aiming for. You upload a resume, pick a target role, and it shows a match score, the skills it found, the skills you are missing, and a simple week-by-week plan to fill the gaps. I built it as my major project for the AI course at Unlox Academy.

The idea came from a common problem: most students don't know whether their resume actually contains the skills a role asks for. This gives them a quick, rough answer before they start applying.

The match score is only an estimate to guide you. It is not a hiring decision, and a missing keyword doesn't always mean a missing ability.

## What it does

- Reads resumes in PDF or DOCX format
- Cleans the text and finds technical skills using a skill dictionary
- Compares the resume with at least five job roles
- Gives a match score for each role and recommends the top three
- Shows which skills you already have and which ones are missing for your target role
- Builds a basic learning roadmap based on the missing skills
- Shows the results on a Streamlit dashboard with a match-score chart
- Lets you download the analysis report

## How it works

1. **Upload**: you upload a PDF or DOCX resume. The file type and size are checked first.
2. **Extract text**: `pypdf` reads each PDF page and `python-docx` reads each DOCX paragraph.
3. **Clean text**: the text is made lowercase and extra symbols and spaces are removed. Symbols like C++, C# and .NET are kept, because removing them would break those skills.
4. **Find skills**: the cleaned text is searched for skills from `data/skill_dictionary.csv`. Each skill belongs to a category such as programming, databases, ML, cloud or tools.
5. **Load job roles**: the required skills for each role come from `data/job_roles.csv`.
6. **Match**: the resume and each job role are turned into TF-IDF vectors, and cosine similarity gives a score for every role.
7. **Recommend**: roles are ranked from highest to lowest score and the top three are shown.
8. **Skill gap**: the skills found in the resume are compared with the target role, and the missing ones are listed.
9. **Roadmap**: each missing skill is mapped to a learning topic and arranged week by week.

## Example output

```
Target Role: Machine Learning Engineer
Match Score: 74%

Skills Found:   Python, Pandas, Machine Learning, scikit-learn, SQL
Missing Skills: FastAPI, Docker, MLflow, Cloud deployment

Recommended Roles:
1. Data Analyst - 86%
2. Junior ML Engineer - 74%
3. Python Developer - 69%

Roadmap:
Week 1: FastAPI basics
Week 2: Deploy an ML model
Week 3: Docker fundamentals
Week 4: MLflow and cloud deployment
```

## Tech used

- Python
- Streamlit (dashboard)
- pypdf and python-docx (resume text extraction)
- Regular expressions (text cleaning)
- scikit-learn (TF-IDF and cosine similarity)
- Pandas and NumPy (data handling)
- Plotly (charts)
- python-dotenv (environment variables)

## Project structure

```
ai_resume_analyzer/
├── app.py                 # Streamlit dashboard
├── resume_parser.py       # reads PDF and DOCX files
├── text_cleaner.py        # cleans the extracted text
├── skill_extractor.py     # finds skills using the dictionary
├── job_matcher.py         # TF-IDF, cosine similarity, ranking
├── roadmap_generator.py   # builds the learning roadmap
├── requirements.txt
├── data/
│   ├── job_roles.csv          # job roles and required skills
│   └── skill_dictionary.csv   # skills grouped by category
├── sample_resumes/        # sample resumes with personal info removed
├── reports/               # generated reports
└── tests/
    └── test_cases.csv     # testing sheet
```

## How to run it

You need Python 3.10 or newer.

**1. Clone the repo**
```
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

**2. Create a virtual environment**
```
python -m venv venv
venv\Scripts\activate
```
On Mac/Linux use `source venv/bin/activate` instead.

**3. Install the packages**
```
pip install -r requirements.txt
```

**4. Start the app**
```
streamlit run app.py
```
It opens in your browser at `http://localhost:8501`.

If you add any API keys later (for example for AI feedback), put them in a `.env` file. That file is in `.gitignore` and should never be uploaded to GitHub.

## How to use it

1. Upload your resume (PDF or DOCX).
2. Choose the job role you want to target.
3. Check the skills that were extracted from your resume.
4. Look at the match-score chart and the top three recommended roles.
5. Read the missing skills and the roadmap.
6. Download the report if you want to keep it.

## Customizing it

The job roles and skills are plain CSV files, so you can change them without touching the code:

- Add a new role as a new row in `data/job_roles.csv` with its required skills.
- Add new skills to `data/skill_dictionary.csv` with their category.

## Testing

I tested the app with different resumes and roles. `tests/test_cases.csv` records the expected top role for each test resume, the role the app actually gave, and comments. I also checked that the score goes up when a required skill is added to a resume and goes down when one is removed.

## Responsible use

- The tool is for guidance only. It should never be used to automatically hire or reject anyone.
- It only looks at job-related skills, education, projects and experience. Gender, age, religion, nationality, photo, marital status and disability are not used for scoring.
- Scores are estimates, not recruiter decisions.
- Uploaded resumes are not stored permanently, and temporary files are deleted after processing.

## Limitations

- Skills are found by keyword matching, so a skill written in an unusual way can be missed.
- It cannot judge how good someone actually is at a skill, only that the word appears.
- The job roles and skills list is small and manually made, so it covers only a few roles.
- Scanned resumes (images of text) are not supported.

## Possible improvements

- Semantic matching with Sentence Transformers
- Upload a job description instead of choosing a fixed role
- Resume improvement suggestions
- PDF version of the report
- FastAPI backend and Docker deployment

## Author

Hemavarshini R