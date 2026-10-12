"""
feature_encoder.py
------------------

Feature encoding utilities for Ayurvedic symptom text.

This module converts cleaned & tokenized text into
numerical feature vectors using TF-IDF.

Used by:
- train_symptom_model.py
- predict_remedy.py
"""

import os
import joblib
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from .tokenizer import tfidf_tokenizer


# -------------------------------------------------
# ABSOLUTE PROJECT ROOT (final 2/)
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

MODEL_DIR = os.path.join(PROJECT_ROOT, "ml", "models")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")


# -------------------------------------------------
# Build & FIT vectorizer (TRAINING ONLY)
# -------------------------------------------------
def build_tfidf_vectorizer(
    corpus: List[str],
    max_features: int = 3000,
    ngram_range: tuple = (1, 2)
) -> TfidfVectorizer:
    """
    Builds and fits a TF-IDF vectorizer on symptom text.
    Used ONLY during training.
    """

    if not corpus or not isinstance(corpus, list):
        raise ValueError("Corpus must be a non-empty list of strings")

    vectorizer = TfidfVectorizer(
        tokenizer=tfidf_tokenizer,
        lowercase=False,  # already handled in cleaner
        max_features=max_features,
        ngram_range=ngram_range
    )

    # 🔥 CRITICAL: FIT THE VECTORIZER
    vectorizer.fit(corpus)

    # Ensure model directory exists
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Save fitted vectorizer
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"💾 TF-IDF vectorizer saved at: {VECTORIZER_PATH}")

    return vectorizer


# -------------------------------------------------
# Load fitted vectorizer (INFERENCE ONLY)
# -------------------------------------------------
def load_tfidf_vectorizer() -> TfidfVectorizer:
    """
    Loads the saved TF-IDF vectorizer.
    """

    if not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(
            f"TF-IDF vectorizer not found at {VECTORIZER_PATH}"
        )

    vectorizer = joblib.load(VECTORIZER_PATH)

    # 🔒 SAFETY CHECK (prevents silent ML crashes)
    if not hasattr(vectorizer, "idf_"):
        raise RuntimeError(
            f"Loaded TF-IDF vectorizer at {VECTORIZER_PATH} is NOT fitted. "
            "Delete models and retrain."
        )

    return vectorizer
