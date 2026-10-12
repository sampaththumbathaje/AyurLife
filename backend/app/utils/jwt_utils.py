"""
jwt_utils.py
------------

Utility functions for JWT handling.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt

from flask import current_app


# -----------------------------
# Generate JWT Token
# -----------------------------
def generate_jwt(payload: Dict) -> str:
    """
    Generates a JWT token with expiry.
    """

    token_payload = payload.copy()
    token_payload["iat"] = datetime.utcnow()
    token_payload["exp"] = datetime.utcnow() + timedelta(
        seconds=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    )

    token = jwt.encode(
        token_payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )

    return token


# -----------------------------
# Decode & Validate JWT Token
# -----------------------------
def decode_jwt(token: str) -> Optional[Dict]:
    """
    Decodes and validates a JWT token.
    """

    try:
        decoded = jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=["HS256"]
        )
        return decoded

    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
