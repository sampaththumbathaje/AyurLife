"""
user_model.py
-------------

Data access model for User collection.

Acts as a repository layer over MongoDB `users` collection.
Encapsulates all user-related database operations.
"""

from datetime import datetime
from bson import ObjectId
from typing import Optional, Dict, List

from app.config.database import get_db


class UserModel:
    """
    UserModel provides static methods to interact with users collection.
    """

    # -----------------------------
    # Create User
    # -----------------------------
    @staticmethod
    def create_user(
        name: str,
        email: str,
        password_hash: str
    ) -> str:
        db = get_db()
        users = db.users

        user = {
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "role": "user",
            "prakriti": None,
            "saved_remedies": [],
            "dinacharya_planner": [],
            "chat_history": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = users.insert_one(user)
        return str(result.inserted_id)

    # -----------------------------
    # Get User by Email
    # -----------------------------
    @staticmethod
    def get_by_email(email: str) -> Optional[Dict]:
        db = get_db()
        return db.users.find_one({"email": email})

    # -----------------------------
    # Get User by ID
    # -----------------------------
    @staticmethod
    def get_by_id(user_id: str, projection: Dict = None) -> Optional[Dict]:
        db = get_db()
        return db.users.find_one(
            {"_id": ObjectId(user_id)},
            projection
        )

    # -----------------------------
    # Update Prakriti
    # -----------------------------
    @staticmethod
    def update_prakriti(user_id: str, prakriti: str):
        db = get_db()
        return db.users.update_one(
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

    # -----------------------------
    # Save Remedy
    # -----------------------------
    @staticmethod
    def save_remedy(
        user_id: str,
        remedy_id: str,
        remedy_name: str
    ):
        db = get_db()
        return db.users.update_one(
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

    # -----------------------------
    # Get Saved Remedies
    # -----------------------------
    @staticmethod
    def get_saved_remedies(user_id: str) -> List[Dict]:
        db = get_db()
        user = db.users.find_one(
            {"_id": ObjectId(user_id)},
            {"saved_remedies": 1, "_id": 0}
        )
        return user.get("saved_remedies", []) if user else []

    # -----------------------------
    # Assign Planner Task
    # -----------------------------
    @staticmethod
    def assign_planner_task(
        user_id: str,
        task_id: str,
        task_name: str,
        time: str,
        date: str
    ):
        db = get_db()
        return db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$push": {
                    "dinacharya_planner": {
                        "task_id": task_id,
                        "task_name": task_name,
                        "time": time,
                        "date": date,
                        "completed": False
                    }
                },
                "$set": {"updated_at": datetime.utcnow()}
            }
        )

    # -----------------------------
    # Complete Planner Task
    # -----------------------------
    @staticmethod
    def complete_planner_task(
        user_id: str,
        task_id: str,
        date: str
    ):
        db = get_db()
        return db.users.update_one(
            {
                "_id": ObjectId(user_id),
                "dinacharya_planner.task_id": task_id,
                "dinacharya_planner.date": date
            },
            {
                "$set": {
                    "dinacharya_planner.$.completed": True,
                    "updated_at": datetime.utcnow()
                }
            }
        )
