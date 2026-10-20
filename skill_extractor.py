import re
import pandas as pd


# Common spelling variations mapped to canonical skill names.
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
    """Normalize a skill name for consistent comparison."""
    skill = str(skill).lower().strip()
    skill = re.sub(r"\s+", " ", skill)

    return SKILL_ALIASES.get(skill, skill)


def load_skill_dictionary(file_path):
    """
    Load the skill dictionary CSV.
    Required columns: skill, category.
    """
    skill_df = pd.read_csv(file_path)

    required_columns = {"skill", "category"}

    if not required_columns.issubset(skill_df.columns):
        raise ValueError(
            "skill_dictionary.csv must contain "
            "'skill' and 'category' columns."
        )

    skill_df = skill_df.dropna(subset=["skill"]).copy()

    skill_df["skill"] = (
        skill_df["skill"].astype(str).str.lower().str.strip()
    )

    skill_df["category"] = (
        skill_df["category"]
        .fillna("other")
        .astype(str)
        .str.lower()
        .str.strip()
    )

    skill_df = skill_df[skill_df["skill"] != ""]

    return skill_df.drop_duplicates(subset=["skill"]).reset_index(
        drop=True
    )


def skill_exists_in_text(skill, text):
    """
    Search for a complete skill name rather than a substring.
    """
    if not skill or not text:
        return False

    skill = normalize_skill(skill)
    text = str(text).lower()

    # Permit flexible whitespace between words.
    escaped_skill = re.escape(skill)
    escaped_skill = escaped_skill.replace(r"\ ", r"\s+")

    pattern = rf"(?<![a-z0-9]){escaped_skill}(?![a-z0-9])"

    return bool(re.search(pattern, text))


def extract_skills(cleaned_resume_text, skill_df):
    """Detect dictionary skills mentioned in the resume."""
    if not cleaned_resume_text:
        return []

    found_skills = set()

    for skill in skill_df["skill"].dropna().unique():
        canonical_skill = normalize_skill(skill)

        # Match the canonical name or a known alias.
        candidates = [canonical_skill]

        candidates.extend(
            alias
            for alias, canonical in SKILL_ALIASES.items()
            if canonical == canonical_skill
        )

        if any(
            skill_exists_in_text(candidate, cleaned_resume_text)
            for candidate in candidates
        ):
            found_skills.add(canonical_skill)

    return sorted(found_skills)


def group_skills_by_category(detected_skills, skill_df):
    """Group detected skills by their dictionary categories."""
    grouped_skills = {}

    for skill in detected_skills:
        normalized = normalize_skill(skill)

        matching_rows = skill_df[
            skill_df["skill"].apply(normalize_skill) == normalized
        ]

        if matching_rows.empty:
            category = "other"
        else:
            category = matching_rows.iloc[0]["category"]

        grouped_skills.setdefault(category, []).append(skill)

    return dict(sorted(grouped_skills.items()))