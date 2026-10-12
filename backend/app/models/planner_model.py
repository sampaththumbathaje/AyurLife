"""
planner_model.py
----------------

Data access model for Dinacharya Planner.

Encapsulates all MongoDB operations related to:
- Dinacharya task templates
- User-specific planner tasks
"""

from datetime import datetime
from typing import List, Dict, Optional
from bson import ObjectId

from app.config.database import get_db


class PlannerModel:
    """
    PlannerModel provides static methods to interact with
    dinacharya and user planner data.
    """

    # -----------------------------
    # Get All Dinacharya Tasks
    # -----------------------------
    @staticmethod
    def get_all_tasks() -> List[Dict]:
        db = get_db()
        return list(db.dinacharya.find({}, {"_id": 0}))

    # -----------------------------
    # Get Tasks by Prakriti
    # -----------------------------
    @staticmethod
    def get_tasks_by_prakriti(prakriti: str) -> List[Dict]:
        db = get_db()
        return list(
            db.dinacharya.find(
                {"suitable_prakriti": prakriti},
                {"_id": 0}
            )
        )

    # -----------------------------
    # Assign Task to User Planner
    # -----------------------------
    @staticmethod
    def assign_task(
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
    # Mark Planner Task as Completed
    # -----------------------------
    @staticmethod
    def mark_task_completed(
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

    # -----------------------------
    # Get User Planner Tasks
    # -----------------------------
    @staticmethod
    def get_user_planner(user_id: str) -> Optional[List[Dict]]:
        db = get_db()
        user = db.users.find_one(
            {"_id": ObjectId(user_id)},
            {"dinacharya_planner": 1, "_id": 0}
        )

        if not user:
            return None

        return user.get("dinacharya_planner", [])
