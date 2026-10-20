import re


def clean_resume_text(text):
    """
    Clean resume text while preserving useful technical symbols,
    including C++, C#, .NET, Node.js, and scikit-learn.
    """
    if not text:
        return ""

    text = str(text).lower()

    # Replace special whitespace characters.
    text = text.replace("\u00a0", " ")
    text = text.replace("\u200b", "")
    text = text.replace("\ufeff", "")
    text = text.replace("\t", " ")

    # Normalize repeated whitespace.
    text = re.sub(r"\s+", " ", text)

    # Keep letters, numbers, spaces, and common technical symbols.
    text = re.sub(r"[^a-z0-9\s+#./-]", " ", text)

    # Remove extra spaces introduced during cleaning.
    text = re.sub(r"\s+", " ", text)

    return text.strip()