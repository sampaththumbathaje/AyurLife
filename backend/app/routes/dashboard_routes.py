"""
dashboard_routes.py
-------------------

Dashboard routes for AyurLife backend.
"""

from flask import Blueprint, jsonify
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId

from app.config.database import get_db

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)


# =====================================================
# User Dashboard Overview
# =====================================================
@dashboard_bp.route("/<string:user_id>", methods=["GET"])
def get_dashboard(user_id):

    db = get_db()
    users = db.users
    chat_history = db.chat_history

    # -----------------------------
    # Validate ObjectId
    # -----------------------------
    try:
        user_object_id = ObjectId(user_id)
    except InvalidId:
        return jsonify({"error": "Invalid user ID"}), 400

    # -----------------------------
    # Fetch User Profile
    # -----------------------------
    user = users.find_one(
        {"_id": user_object_id},
        {
            "name": 1,
            "email": 1,
            "prakriti": 1,
            "saved_remedies": 1,
            "dinacharya_planner": 1,
            "_id": 0
        }
    )

    if not user:
        return jsonify({"error": "User not found"}), 404

    # =====================================================
    # Today's Dinacharya Tasks
    # =====================================================
    today = datetime.utcnow().strftime("%Y-%m-%d")

    today_tasks = [
        task for task in user.get("dinacharya_planner", [])
        if task.get("date") == today
    ]

    # =====================================================
    # Recent Chat Sessions (Last 5)
    # =====================================================
    recent_sessions = (
        chat_history
        .find(
            {"user_id": user_object_id},
            {
                "session_id": 1,
                "user_message": 1,
                "bot_reply": 1,
                "timestamp": 1,
                "_id": 0
            }
        )
        .sort("timestamp", -1)
        .limit(5)
    )

    recent_chats = []

    for chat in recent_sessions:
        recent_chats.append({
            "session_id": chat.get("session_id"),
            "last_user_message": chat.get("user_message"),
            "last_bot_reply": chat.get("bot_reply"),
            "timestamp": chat.get("timestamp")
        })

    # =====================================================
    # Clean Prakriti Structure
    # =====================================================
    prakriti_data = user.get("prakriti")

    # Ensure consistent response format
    if prakriti_data:
        prakriti_response = {
            "prediction": prakriti_data.get("prediction"),
            "probabilities": prakriti_data.get("probabilities"),
            "identified_at": prakriti_data.get("identified_at")
        }
    else:
        prakriti_response = None

    # =====================================================
    # Final Dashboard Response
    # =====================================================
    dashboard_data = {
        "profile": {
            "name": user.get("name"),
            "email": user.get("email")
        },
        "prakriti": prakriti_response,
        "saved_remedies": user.get("saved_remedies", []),
        "today_tasks": today_tasks,
        "recent_chats": recent_chats
    }

    return jsonify(dashboard_data), 200
