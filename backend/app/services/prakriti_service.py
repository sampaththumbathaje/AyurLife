"""
prakriti_service.py
-------------------

Service layer for Prakriti-related operations.

Responsibilities:
- Validate questionnaire answers
- Predict Prakriti using MLService
- Provide reusable Prakriti utilities
"""

from typing import Dict, Optional

from ml.inference.questionnaire_logic import build_ml_input
from app.services.ml_service import MLService


# -----------------------------
# Predict Prakriti
# -----------------------------
def predict_prakriti(answers: Dict[str, int]) -> Optional[str]:
    """
    Predicts Prakriti from questionnaire answers.

    Parameters
    ----------
    answers : dict
        Questionnaire answers (numeric values)

    Returns
    -------
    str or None
        Predicted Prakriti (Vata / Pitta / Kapha)
    """

    if not answers or not isinstance(answers, dict):
        return None

    # Validate & normalize input
    ml_input = build_ml_input(answers)

    if not ml_input:
        return None

    # Call centralized ML service
    return MLService.predict_prakriti(ml_input)
