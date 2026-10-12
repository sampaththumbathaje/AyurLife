"""
remedy_controller.py
--------------------

Controller for Ayurvedic remedy business logic.

Handles:
- Fetching remedy details
- Saving remedies to user profile
- Retrieving saved remedies
- Prakriti-based remedy filtering
"""

from datetime import datetime
from bson import ObjectId

from app.config.database import get_db


# -----------------------------
# Get Remedy Details by Name
# -----------------------------
def get_remedy_by_name(remedy_name: str):
    db = get_db()
    remedies = db.remedies

    remedy = remedies.find_one(
        {"name": remedy_name},
        {"_id": 0}
    )

    if not remedy:
        return None, "Remedy not found"

    return remedy, None


# -----------------------------
# Save Remedy for User
# -----------------------------
def save_remedy_for_user(user_id: str, remedy_id: str, remedy_name: str):
    db = get_db()
    users = db.users

    result = users.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$push": {
                "saved_remedies": {
                    "remedy_id": remedy_id,
                    "name": remedy_name,
                    "saved_at": datetime.utcnow()
                }
            },
            "$set": {"updated_at": datetime.utcnow()}
        }
    )

    if result.matched_count == 0:
        return "User not found"

    return None


# -----------------------------
# Get Saved Remedies for User
# -----------------------------
def get_saved_remedies(user_id: str):
    db = get_db()
    users = db.users

    user = users.find_one(
        {"_id": ObjectId(user_id)},
        {"saved_remedies": 1, "_id": 0}
    )

    if not user:
        return None, "User not found"

    return user.get("saved_remedies", []), None


# -----------------------------
# Filter Remedies by Prakriti
# -----------------------------
def get_remedies_by_prakriti(prakriti_type: str):
    db = get_db()
    remedies = db.remedies

    results = remedies.find(
        {"suitable_prakriti": prakriti_type},
        {"_id": 0}
    )

    return list(results)
