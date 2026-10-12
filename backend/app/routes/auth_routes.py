"""
auth_routes.py
--------------

Authentication routes for AyurLife backend.

Features:
- User registration
- User login
- Password hashing
- JWT-based authentication
"""

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from app.utils.jwt_utils import generate_jwt


from app.config.database import get_db
from app.config.settings import DevelopmentConfig

auth_bp = Blueprint("auth", __name__)





# -----------------------------
# Register
# -----------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"error": "All fields are required"}), 400

    db = get_db()
    users = db.users

    if users.find_one({"email": email}):
        return jsonify({"error": "Email already registered"}), 409

    password_hash = generate_password_hash(password)

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

    return jsonify({
        "message": "Registration successful",
        "user_id": str(result.inserted_id)
    }), 201


# -----------------------------
# Login
# -----------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Email and password required"}), 400

    db = get_db()
    users = db.users

    user = users.find_one({"email": email})

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_jwt({
        "user_id": str(user["_id"]),
        "email": user["email"]
    })

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "prakriti": user.get("prakriti")
        }
    }), 200
