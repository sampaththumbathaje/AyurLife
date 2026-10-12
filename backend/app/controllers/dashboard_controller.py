"""
dashboard_controller.py
-----------------------

Controller for Dashboard aggregation logic.

Combines user-specific data into a single structure
for efficient dashboard rendering.
"""

from datetime import datetime
from bson import ObjectId

from app.config.database import get_db


# -----------------------------
# Get Dashboard Data
# -----------------------------
def get_dashboard_data(user_id: str):
    db = get_db()
    users = db.users
    chat_history = db.chat_history

    user = users.find_one(
        {"_id": ObjectId(user_id)},
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
        return None, "User not found"

    # -----------------------------
    # Today's Dinacharya Tasks
    # -----------------------------
    today = datetime.utcnow().strftime("%Y-%m-%d")
    today_tasks = [
        task for task in user.get("dinacharya_planner", [])
        if task.get("date") == today
    ]

    # -----------------------------
    # Recent Chat Sessions
    # -----------------------------
    recent_chats = list(
        chat_history.find(
            {"user_id": ObjectId(user_id)},
            {
                "session_id": 1,
                "created_at": 1,
                "messages": {"$slice": -2},
                "_id": 0
            }
        ).sort("created_at", -1).limit(5)
    )

    dashboard = {
        "profile": {
            "name": user.get("name"),
            "email": user.get("email")
        },
        "prakriti": user.get("prakriti"),
        "saved_remedies": user.get("saved_remedies", []),
        "today_tasks": today_tasks,
        "recent_chats": recent_chats
    }

    return dashboard, None
