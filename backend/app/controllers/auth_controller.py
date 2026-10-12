"""
auth_controller.py
------------------

Controller for authentication logic.

Handles:
- User registration
- User login
- Password hashing
- JWT generation
"""

from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

from app.config.database import get_db
from app.config.settings import DevelopmentConfig


# -----------------------------
# JWT Utility
# -----------------------------
def generate_jwt(user_id, email):
    payload = {
        "user_id": str(user_id),
        "email": email,
        "exp": datetime.utcnow() + timedelta(
            seconds=DevelopmentConfig.JWT_ACCESS_TOKEN_EXPIRES
        )
    }

    token = jwt.encode(
        payload,
        DevelopmentConfig.JWT_SECRET_KEY,
        algorithm="HS256"
    )

    return token


# -----------------------------
# Register User
# -----------------------------
def register_user(name, email, password):
    db = get_db()
    users = db.users

    if users.find_one({"email": email}):
        return None, "Email already registered"

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

    return str(result.inserted_id), None


# -----------------------------
# Login User
# -----------------------------
def login_user(email, password):
    db = get_db()
    users = db.users

    user = users.find_one({"email": email})

    if not user:
        return None, "Invalid email or password"

    if not check_password_hash(user["password_hash"], password):
        return None, "Invalid email or password"

    token = generate_jwt(user["_id"], user["email"])

    user_data = {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "prakriti": user.get("prakriti")
    }

    return {
        "token": token,
        "user": user_data
    }, None
