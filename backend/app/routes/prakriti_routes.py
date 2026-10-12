"""
prakriti_routes.py
------------------

Routes for Prakriti determination and management.

Features:
- Fetch Prakriti questionnaire
- Predict Prakriti using ML
- Save Prakriti to user profile
- Retrieve user's Prakriti
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId

from app.config.database import get_db

# ML imports
from ml.inference.predict_prakriti import PrakritiPredictor
from ml.inference.questionnaire_logic import (
    get_questions,
    build_ml_input
)

prakriti_bp = Blueprint("prakriti", __name__)

# Load model once
prakriti_predictor = PrakritiPredictor()


# -----------------------------
# Get Prakriti Questionnaire
# -----------------------------
@prakriti_bp.route("/questions", methods=["GET"])
def get_prakriti_questions():
    """
    Returns Prakriti questionnaire questions.
    """
    return jsonify({
        "questions": get_questions()
    }), 200


# -----------------------------
# Predict & Save Prakriti
# -----------------------------
@prakriti_bp.route("/predict", methods=["POST"])
def predict_prakriti():
    """
    Predicts Prakriti based on questionnaire answers
    and saves it to the user's profile.
    """

    data = request.json

    user_id = data.get("user_id")
    answers = data.get("answers")

    if not user_id or not answers:
        return jsonify({"error": "user_id and answers are required"}), 400

    ml_input = build_ml_input(answers)

    if not ml_input:
        return jsonify({"error": "Invalid questionnaire answers"}), 400

    prakriti = prakriti_predictor.predict(ml_input)

    db = get_db()
    users = db.users

    users.update_one(
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

    return jsonify({
        "message": "Prakriti identified successfully",
        "prakriti": prakriti
    }), 200


# -----------------------------
# Get User Prakriti
# -----------------------------
@prakriti_bp.route("/<string:user_id>", methods=["GET"])
def get_user_prakriti(user_id):
    """
    Retrieves stored Prakriti of a user.
    """

    db = get_db()
    users = db.users

    user = users.find_one(
        {"_id": ObjectId(user_id)},
        {"prakriti": 1, "_id": 0}
    )

    if not user or not user.get("prakriti"):
        return jsonify({"error": "Prakriti not found"}), 404

    return jsonify(user["prakriti"]), 200
