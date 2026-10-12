"""
remedy_routes.py
----------------
Routes for Ayurvedic remedies.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId

from app.config.database import get_db

remedy_bp = Blueprint(
    "remedy",
    __name__,
    url_prefix="/api/remedy"
)




# -------------------------------------------------
# Get Remedy Details by Name
# -------------------------------------------------
@remedy_bp.route("/<string:remedy_name>", methods=["GET"])
def get_remedy(remedy_name):
    db = get_db()
    remedies = db.remedies

    remedy = remedies.find_one(
        {"name": remedy_name},
        {"_id": 0}
    )

    if not remedy:
        return jsonify({"error": "Remedy not found"}), 404

    return jsonify(remedy), 200


# -------------------------------------------------
# Save Remedy to User Dashboard
# -------------------------------------------------
@remedy_bp.route("/save", methods=["POST"])
def save_remedy():
    data = request.json

    user_id = data.get("user_id")
    remedy_name = data.get("name")

    if not user_id or not remedy_name:
        return jsonify({"error": "user_id and name are required"}), 400

    db = get_db()
    users = db.users
    remedies = db.remedies

    # Validate ObjectId
    try:
        user_object_id = ObjectId(user_id)
    except InvalidId:
        return jsonify({"error": "Invalid user_id"}), 400

    # Validate user
    user = users.find_one({"_id": user_object_id})
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Validate remedy exists
    remedy = remedies.find_one({"name": remedy_name})
    if not remedy:
        return jsonify({"error": "Remedy does not exist"}), 404

    # Prevent duplicate save (case insensitive)
    existing_remedies = user.get("saved_remedies", [])
    if any(r["name"].lower() == remedy_name.lower() for r in existing_remedies):
        return jsonify({"message": "Remedy already saved"}), 200

    # Store full snapshot (better for dashboard stability)
    saved_entry = {
        "remedy_id": str(remedy["_id"]),
        "name": remedy["name"],
        "ingredients": remedy.get("ingredients"),
        "description": remedy.get("description"),
        "suitable_prakriti": remedy.get("suitable_prakriti"),
        "saved_at": datetime.utcnow()
    }

    users.update_one(
        {"_id": user_object_id},
        {
            "$push": {"saved_remedies": saved_entry},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )

    return jsonify({
        "message": "Remedy saved successfully",
        "saved_remedy": saved_entry
    }), 200


# -------------------------------------------------
# Get Saved Remedies (Dashboard)
# -------------------------------------------------
@remedy_bp.route("/saved/<string:user_id>", methods=["GET"])
def get_saved_remedies(user_id):
    db = get_db()
    users = db.users

    try:
        user_object_id = ObjectId(user_id)
    except InvalidId:
        return jsonify({"error": "Invalid user_id"}), 400

    user = users.find_one(
        {"_id": user_object_id},
        {"saved_remedies": 1, "_id": 0}
    )

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Sort newest first
    remedies = sorted(
        user.get("saved_remedies", []),
        key=lambda x: x.get("saved_at", datetime.min),
        reverse=True
    )

    return jsonify(remedies), 200


# -------------------------------------------------
# Filter Remedies by Prakriti
# -------------------------------------------------
@remedy_bp.route("/prakriti/<string:prakriti_type>", methods=["GET"])
def remedies_by_prakriti(prakriti_type):
    db = get_db()
    remedies = db.remedies

    result = remedies.find(
        {"suitable_prakriti": prakriti_type},
        {"_id": 0}
    )

    return jsonify(list(result)), 200
