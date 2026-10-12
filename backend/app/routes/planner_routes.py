"""
planner_routes.py
-----------------

Routes for Daily Dinacharya Planner.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId

from app.config.database import get_db

planner_bp = Blueprint("planner", __name__)

# =====================================================
# Get All Dinacharya Tasks
# =====================================================

@planner_bp.route("/tasks", methods=["GET"])
def get_all_tasks():

    db = get_db()
    dinacharya = db.dinacharya

    tasks = dinacharya.find({}, {"_id": 0})

    return jsonify(list(tasks)), 200


# =====================================================
# Get Tasks by Prakriti
# =====================================================

@planner_bp.route("/tasks/<string:prakriti>", methods=["GET"])
def get_tasks_by_prakriti(prakriti):

    db = get_db()
    dinacharya = db.dinacharya

    tasks = dinacharya.find(
        {"suitable_prakriti": prakriti},
        {"_id": 0}
    )

    return jsonify(list(tasks)), 200


# =====================================================
# Assign Task to User Planner
# =====================================================

@planner_bp.route("/assign", methods=["POST"])
def assign_task():

    data = request.json

    user_id = data.get("user_id")
    task_id = data.get("task_id")
    task_name = data.get("task_name")
    time = data.get("time")
    date = data.get("date")

    if not all([
        user_id,
        task_id,
        task_name,
        time,
        date
    ]):
        return jsonify({
            "error": "All fields are required"
        }), 400

    db = get_db()
    users = db.users

    user = users.find_one({
        "_id": ObjectId(user_id)
    })

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    planner = user.get("dinacharya_planner", [])

    # Prevent duplicate task
    for task in planner:

        if (
            str(task.get("task_id")) == str(task_id)
            and task.get("date") == date
        ):
            return jsonify({
                "message": "Task already added"
            }), 200

    new_task = {
        "task_id": str(task_id),
        "task_name": task_name,
        "time": time,
        "date": date,
        "completed": False,
        "created_at": datetime.utcnow()
    }

    users.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$push": {
                "dinacharya_planner": new_task
            },
            "$set": {
                "updated_at": datetime.utcnow()
            }
        }
    )

    return jsonify({
        "message": "Task assigned successfully",
        "task": new_task
    }), 200


# =====================================================
# Mark Task as Completed
# =====================================================

@planner_bp.route("/complete", methods=["POST"])
def complete_task():

    data = request.json

    user_id = data.get("user_id")
    task_id = data.get("task_id")
    date = data.get("date")

    if not all([user_id, task_id, date]):
        return jsonify({
            "error": "user_id, task_id and date are required"
        }), 400

    db = get_db()
    users = db.users

    user = users.find_one({
        "_id": ObjectId(user_id)
    })

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    planner = user.get("dinacharya_planner", [])

    updated = False

    for task in planner:

        current_task_id = str(
            task.get("task_id", "")
        )

        current_date = task.get("date")

        if (
            current_task_id == str(task_id)
            and current_date == date
        ):
            task["completed"] = True
            updated = True

    if not updated:
        return jsonify({
            "error": "Task not found"
        }), 404

    users.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$set": {
                "dinacharya_planner": planner,
                "updated_at": datetime.utcnow()
            }
        }
    )

    return jsonify({
        "message": "Task marked as completed"
    }), 200


# =====================================================
# Delete Planner Task
# =====================================================

@planner_bp.route("/delete", methods=["POST"])
def delete_task():

    data = request.json

    user_id = data.get("user_id")
    task_id = data.get("task_id")
    date = data.get("date")

    if not all([user_id, task_id, date]):
        return jsonify({
            "error": "user_id, task_id and date are required"
        }), 400

    db = get_db()
    users = db.users

    result = users.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$pull": {
                "dinacharya_planner": {
                    "task_id": str(task_id),
                    "date": date
                }
            }
        }
    )

    if result.modified_count == 0:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "message": "Task deleted successfully"
    }), 200


# =====================================================
# Get User Planner Tasks
# =====================================================

@planner_bp.route("/user/<string:user_id>", methods=["GET"])
def get_user_planner(user_id):

    try:

        db = get_db()
        users = db.users

        user = users.find_one(
            {"_id": ObjectId(user_id)},
            {
                "dinacharya_planner": 1,
                "_id": 0
            }
        )

        if not user:
            return jsonify([]), 200

        tasks = user.get(
            "dinacharya_planner",
            []
        )

        # Sort tasks by time
        tasks = sorted(
            tasks,
            key=lambda x: x.get("time", "23:59")
        )

        return jsonify(tasks), 200

    except Exception as e:

        print("Planner Error:", e)

        return jsonify({
            "error": "Failed to load planner"
        }), 500