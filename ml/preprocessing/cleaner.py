"""
cleaner.py
----------

Text cleaning utilities for Ayurvedic symptom text.

This module standardizes raw text input before tokenization.
It is used during:
- Model training
- Model inference (prediction)

IMPORTANT:
- No ML models are loaded here
- No external frameworks (Flask, DB) are used
"""

import re
from typing import Optional


def clean_text(text: Optional[str]) -> str:
    """
    Cleans raw symptom text.

    Cleaning steps:
    1. Handle None or empty input
    2. Convert to lowercase
    3. Normalize common separators
    4. Remove unwanted special characters
    5. Normalize whitespace

    Parameters
    ----------
    text : str or None
        Raw symptom input text

    Returns
    -------
    str
        Cleaned text ready for tokenization
    """

    if not text or not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Normalize common separators
    text = text.replace(";", ",")
    text = text.replace("|", ",")
    text = text.replace("/", " ")

    # Remove unwanted characters (keep letters, spaces, commas)
    text = re.sub(r"[^a-z\s,]", " ", text)

    # Replace multiple spaces with single space
    text = re.sub(r"\s+", " ", text)

    # Remove extra spaces around commas
    text = re.sub(r"\s*,\s*", ", ", text)

    return text.strip()
