"""
auth_service.py
---------------

Service layer for authentication utilities.

Handles:
- Password hashing and verification
- JWT token generation
- JWT token decoding and validation
"""

from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

from app.config.settings import DevelopmentConfig


# -----------------------------
# Password Utilities
# -----------------------------
def hash_password(password: str) -> str:
    """
    Hash a plain-text password.
    """
    return generate_password_hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against its hash.
    """
    return check_password_hash(password_hash, password)


# -----------------------------
# JWT Utilities
# -----------------------------
def generate_token(user_id: str, email: str) -> str:
    """
    Generate JWT access token.
    """
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(
            seconds=DevelopmentConfig.JWT_ACCESS_TOKEN_EXPIRES
        ),
        "iat": datetime.utcnow()
    }

    token = jwt.encode(
        payload,
        DevelopmentConfig.JWT_SECRET_KEY,
        algorithm="HS256"
    )

    return token


def decode_token(token: str):
    """
    Decode and validate JWT token.

    Returns:
    - decoded payload on success
    - None on failure
    """
    try:
        payload = jwt.decode(
            token,
            DevelopmentConfig.JWT_SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
