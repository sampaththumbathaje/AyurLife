"""
tokenizer.py
------------

Custom tokenizer for Ayurvedic symptom text.

This tokenizer is optimized for:
- Short symptom-based user inputs
- Ayurvedic and medical terminology
- TF-IDF vectorization

Used by:
- feature_encoder.py
- train_symptom_model.py
- predict_remedy.py
"""

import re
from typing import List

# Minimal but effective stopword list
STOPWORDS = {
    "i", "have", "am", "is", "are", "was", "were",
    "the", "a", "an", "and", "or", "of", "to",
    "with", "for", "in", "on", "at", "by",
    "my", "me", "it", "this", "that", "from"
}


def tfidf_tokenizer(text: str) -> List[str]:
    """
    Tokenizes symptom text for TF-IDF vectorization.

    Steps:
    1. Lowercase conversion
    2. Remove special characters
    3. Split on commas and whitespace
    4. Remove stopwords
    5. Remove very short tokens

    Parameters
    ----------
    text : str
        Raw symptom input (e.g., "fever, sore throat, body pain")

    Returns
    -------
    List[str]
        Clean list of tokens suitable for TF-IDF
    """

    if not isinstance(text, str):
        return []

    # Convert to lowercase
    text = text.lower()

    # Replace non-alphabetic characters with space
    text = re.sub(r"[^a-z\s,]", " ", text)

    # Split first by commas (important for symptom lists)
    raw_tokens = []
    for part in text.split(","):
        raw_tokens.extend(part.strip().split())

    # Clean tokens
    tokens = [
        token
        for token in raw_tokens
        if token not in STOPWORDS
        and len(token) > 2
    ]

    return tokens
