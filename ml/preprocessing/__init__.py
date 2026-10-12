"""
Preprocessing package for AyurLife ML pipeline.

This package contains utilities for:
- Text cleaning and normalization
- Tokenization
- Feature encoding (TF-IDF)

Used during:
- Model training
- Model inference (prediction)

NOTE:
This package must remain framework-agnostic.
No Flask, DB, or API logic is allowed here.
"""

from .cleaner import clean_text
from .tokenizer import tfidf_tokenizer
from .feature_encoder import build_tfidf_vectorizer

__all__ = [
    "clean_text",
    "tfidf_tokenizer",
    "build_tfidf_vectorizer",
]
