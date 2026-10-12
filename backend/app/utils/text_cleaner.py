"""
text_cleaner.py
---------------

Utility module for cleaning and normalizing
user symptom text for ML processing.

Used during:
- Model training
- Model inference
"""

import re
import string
from typing import List

# Basic English stopwords (kept minimal on purpose)
STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "you", "your",
    "he", "she", "it", "they", "them",
    "is", "am", "are", "was", "were",
    "a", "an", "the",
    "and", "or", "but",
    "of", "in", "on", "for", "with", "to",
    "from", "by", "as",
    "have", "has", "had",
    "do", "does", "did"
}


# -----------------------------
# Core Text Cleaning
# -----------------------------
def clean_text(text: str) -> str:
    """
    Cleans raw user input text.

    Steps:
    1. Lowercase
    2. Remove numbers
    3. Remove punctuation
    4. Remove extra spaces

    Parameters
    ----------
    text : str
        Raw input text

    Returns
    -------
    str
        Cleaned text
    """

    if not text or not isinstance(text, str):
        return ""

    # Lowercase
    text = text.lower()

    # Remove numbers
    text = re.sub(r"\d+", " ", text)

    # Remove punctuation
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# -----------------------------
# Tokenization
# -----------------------------
def tokenize(text: str) -> List[str]:
    """
    Tokenizes cleaned text into words.
    """

    text = clean_text(text)
    return text.split()


# -----------------------------
# Stopword Removal
# -----------------------------
def remove_stopwords(tokens: List[str]) -> List[str]:
    """
    Removes stopwords from token list.
    """

    return [
        token for token in tokens
        if token not in STOPWORDS
    ]


# -----------------------------
# Full Preprocessing Pipeline
# -----------------------------
def preprocess_text(text: str) -> str:
    """
    Full preprocessing pipeline:
    - Clean text
    - Tokenize
    - Remove stopwords
    - Rejoin tokens

    Returns cleaned string suitable for ML models.
    """

    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    return " ".join(tokens)
