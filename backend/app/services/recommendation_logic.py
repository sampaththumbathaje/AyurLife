"""
recommendation_logic.py
-----------------------

Core recommendation logic for AyurLife.

This module combines:
- ML-predicted remedies
- User Prakriti
- Ayurvedic suitability rules

It ensures that final recommendations are:
- Prakriti-appropriate
- Safe
- Explainable
"""

from typing import Dict, Optional

from app.config.database import get_db


# -----------------------------
# Fetch Remedy from DB
# -----------------------------
def _get_remedy_by_name(remedy_name: str) -> Optional[Dict]:
    db = get_db()
    return db.remedies.find_one(
        {"name": remedy_name},
        {"_id": 0}
    )


# -----------------------------
# Check Prakriti Suitability
# -----------------------------
def is_prakriti_compatible(remedy: Dict, prakriti: Optional[str]) -> bool:
    """
    Checks whether a remedy is suitable for a given Prakriti.
    """

    if not prakriti:
        # If Prakriti not known, allow recommendation
        return True

    suitable = remedy.get("suitable_prakriti", [])

    return prakriti in suitable


# -----------------------------
# Build Final Recommendation
# -----------------------------
def build_recommendation(
    predicted_remedy: str,
    user_prakriti: Optional[str] = None
) -> Optional[Dict]:
    """
    Builds the final recommendation object.

    Parameters
    ----------
    predicted_remedy : str
        Remedy name predicted by ML
    user_prakriti : str, optional
        User's Prakriti (Vata / Pitta / Kapha)

    Returns
    -------
    dict or None
        Final recommendation payload
    """

    remedy = _get_remedy_by_name(predicted_remedy)

    if not remedy:
        return None

    # Check Prakriti compatibility
    compatible = is_prakriti_compatible(remedy, user_prakriti)

    recommendation = {
        "name": remedy.get("name"),
        "category": remedy.get("category"),
        "used_for": remedy.get("used_for"),
        "dosage": remedy.get("dosage"),
        "precautions": remedy.get("precautions"),
        "suitable_prakriti": remedy.get("suitable_prakriti"),
        "prakriti_compatible": compatible
    }

    # Add advisory note if not compatible
    if not compatible:
        recommendation["advisory"] = (
            f"This remedy is generally not recommended for "
            f"{user_prakriti} Prakriti. Please consult an Ayurvedic expert."
        )

    return recommendation
