"""
prakriti_controller.py
----------------------

Controller for Prakriti-related business logic.

Handles:
- Questionnaire retrieval
- Prakriti prediction using ML
- Saving and fetching user Prakriti
"""

from datetime import datetime
from bson import ObjectId

from app.config.database import get_db

# ML imports
from ml.inference.predict_prakriti import PrakritiPredictor
from ml.inference.questionnaire_logic import (
    get_questions,
    build_ml_input
)

# Load model once
_prakriti_predictor = PrakritiPredictor()


# -----------------------------
# Get Prakriti Questionnaire
# -----------------------------
def fetch_prakriti_questions():
    """
    Returns the Prakriti questionnaire.
    """
    return get_questions()


# -----------------------------
# Predict & Save Prakriti
# -----------------------------
def predict_and_save_prakriti(user_id: str, answers: dict):
    """
    Predicts Prakriti from questionnaire answers
    and saves it to the user's profile.

    Returns:
    - (prakriti, None) on success
    - (None, error_message) on failure
    """

    ml_input = build_ml_input(answers)

    if not ml_input:
        return None, "Invalid questionnaire answers"

    prakriti = _prakriti_predictor.predict(ml_input)

    db = get_db()
    users = db.users

    result = users.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$set": {
                "prakriti": {
                    "type": prakriti,
                    "last_updated": datetime.utcnow()
                },
                "updated_at": datetime.utcnow()
            }
        }
    )

    if result.matched_count == 0:
        return None, "User not found"

    return prakriti, None


# -----------------------------
# Get User Prakriti
# -----------------------------
def get_user_prakriti(user_id: str):
    """
    Retrieves stored Prakriti for a user.
    """

    db = get_db()
    users = db.users

    user = users.find_one(
        {"_id": ObjectId(user_id)},
        {"prakriti": 1, "_id": 0}
    )

    if not user or not user.get("prakriti"):
        return None, "Prakriti not found"

    return user["prakriti"], None
