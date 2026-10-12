"""
planner_controller.py
---------------------

Controller for Dinacharya Planner business logic.

Handles:
- Fetching Dinacharya task templates
- Assigning tasks to users
- Tracking task completion
- Retrieving user planner data
"""

from datetime import datetime
from bson import ObjectId

from app.config.database import get_db


# -----------------------------
# Fetch All Dinacharya Tasks
# -----------------------------
def get_all_tasks():
    db = get_db()
    dinacharya = db.dinacharya

    tasks = dinacharya.find({}, {"_id": 0})
    return list(tasks)


# -----------------------------
# Fetch Tasks by Prakriti
# -----------------------------
def get_tasks_by_prakriti(prakriti: str):
    db = get_db()
    dinacharya = db.dinacharya

    tasks = dinacharya.find(
        {"suitable_prakriti": prakriti},
        {"_id": 0}
    )
    return list(tasks)


# -----------------------------
# Assign Task to User Planner
# -----------------------------
def assign_task_to_user(
    user_id: str,
    task_id: str,
    task_name: str,
    time: str,
    date: str
):
    db = get_db()
    users = db.users

    result = users.update_one(
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

    if result.matched_count == 0:
        return "User not found"

    return None


# -----------------------------
# Mark Task as Completed
# -----------------------------
def mark_task_completed(user_id: str, task_id: str, date: str):
    db = get_db()
    users = db.users

    result = users.update_one(
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

    if result.matched_count == 0:
        return "Task not found for given date"

    return None


# -----------------------------
# Get User Planner Tasks
# -----------------------------
def get_user_planner(user_id: str):
    db = get_db()
    users = db.users

    user = users.find_one(
        {"_id": ObjectId(user_id)},
        {"dinacharya_planner": 1, "_id": 0}
    )

    if not user:
        return None, "User not found"

    return user.get("dinacharya_planner", []), None
