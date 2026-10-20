import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILL_ALIASES = {
    "power-bi": "power bi",
    "powerbi": "power bi",
    "scikit learn": "scikit-learn",
    "node js": "node.js",
    "nodejs": "node.js",
    "ms excel": "excel",
    "microsoft excel": "excel",
    "machine-learning": "machine learning",
    "deep-learning": "deep learning",
}


def normalize_skill(skill):
    """Normalize skill names before comparing them."""
    skill = str(skill).lower().strip()
    skill = re.sub(r"\s+", " ", skill)

    return SKILL_ALIASES.get(skill, skill)


def parse_required_skills(required_skills_text):
    """
    Convert a pipe-separated CSV value into a list of skills.
    Example: python|sql|excel|power bi
    """
    if pd.isna(required_skills_text):
        return []

    skills = [
        normalize_skill(skill)
        for skill in str(required_skills_text).split("|")
        if skill.strip()
    ]

    return list(dict.fromkeys(skills))


def calculate_skill_score(detected_skills, required_skills):
    """Calculate the percentage of required skills matched."""
    detected_set = {
        normalize_skill(skill)
        for skill in detected_skills
        if str(skill).strip()
    }

    required_set = {
        normalize_skill(skill)
        for skill in required_skills
        if str(skill).strip()
    }

    if not required_set:
        return 0.0

    matched = detected_set.intersection(required_set)

    return round(len(matched) / len(required_set) * 100, 2)


def calculate_text_similarity(resume_text, role_text):
    """Calculate TF-IDF cosine similarity as a percentage."""
    if not str(resume_text).strip() or not str(role_text).strip():
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
        )

        vectors = vectorizer.fit_transform(
            [str(resume_text).lower(), str(role_text).lower()]
        )

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2],
        )[0][0]

        return round(float(similarity) * 100, 2)

    except ValueError:
        # For example, both texts may contain only stop words.
        return 0.0


def calculate_final_score(skill_score, text_similarity_score):
    """
    Final Score = 70% Skill Match + 30% Text Similarity.
    """
    return round(
        0.70 * skill_score + 0.30 * text_similarity_score,
        2,
    )


def analyze_role(resume_text, detected_skills, role_row):
    """Analyze a resume against one job role."""
    role_name = str(role_row.get("role", "")).strip()

    if not role_name or role_name.lower() == "nan":
        role_name = "Unnamed Role"

    raw_required_skills = role_row.get("required_skills", "")

    required_skills = parse_required_skills(raw_required_skills)

    raw_description = role_row.get("description", "")
    description = (
        "" if pd.isna(raw_description)
        else str(raw_description).strip()
    )

    role_text = " ".join(
        part for part in [
            role_name,
            description,
            " ".join(required_skills),
        ]
        if part
    )

    detected_map = {
        normalize_skill(skill): skill
        for skill in detected_skills
    }

    required_set = set(required_skills)
    detected_set = set(detected_map)

    matched_skills = sorted(
        detected_set.intersection(required_set)
    )

    missing_skills = sorted(
        required_set.difference(detected_set)
    )

    skill_score = calculate_skill_score(
        detected_skills,
        required_skills,
    )

    text_similarity_score = calculate_text_similarity(
        resume_text,
        role_text,
    )

    final_score = calculate_final_score(
        skill_score,
        text_similarity_score,
    )

    return {
        "role": role_name,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_score": skill_score,
        "text_similarity_score": text_similarity_score,
        "final_score": final_score,
    }


def analyze_all_roles(resume_text, detected_skills, job_roles_df):
    """Analyze the resume against every row in the roles CSV."""
    required_columns = {
        "role",
        "description",
        "required_skills",
    }

    if not required_columns.issubset(job_roles_df.columns):
        raise ValueError(
            "job_roles.csv must contain the columns: "
            "role, description, required_skills."
        )

    all_results = []

    for _, role_row in job_roles_df.iterrows():
        result = analyze_role(
            resume_text=resume_text,
            detected_skills=detected_skills,
            role_row=role_row,
        )
        all_results.append(result)

    results_df = pd.DataFrame(all_results)

    if results_df.empty:
        return results_df

    return (
        results_df.sort_values(
            by="final_score",
            ascending=False,
        )
        .reset_index(drop=True)
    )


def get_role_analysis(role_results, selected_role):
    """Return analysis for the selected role."""
    selected_result = role_results[
        role_results["role"] == selected_role
    ]

    if selected_result.empty:
        raise ValueError(
            f"Role not found in results: {selected_role}"
        )

    return selected_result.iloc[0].to_dict()