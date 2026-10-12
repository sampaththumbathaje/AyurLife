"""
auth_middleware.py
------------------

JWT authentication middleware for Flask routes.

Responsibilities:
- Validate JWT token
- Attach authenticated user context
- Protect secured endpoints
"""

from functools import wraps
from flask import request, jsonify, g

from app.utils.jwt_utils import decode_jwt


# -----------------------------
# Auth Required Decorator
# -----------------------------
def auth_required(fn):
    """
    Decorator to protect routes with JWT authentication.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization token missing"}), 401

        token = auth_header.split(" ")[1]

        payload = decode_jwt(token)

        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401

        # Attach user context
        g.user = {
            "user_id": payload.get("user_id"),
            "email": payload.get("email")
        }

        return fn(*args, **kwargs)

    return wrapper
