"""
validators.py
-------------

Common validation utilities for AyurLife backend.

Used by:
- Routes
- Controllers
- Services
"""

import re
from typing import Dict, Tuple, Optional


# -----------------------------
# Basic Validators
# -----------------------------
def is_non_empty_string(value) -> bool:
    return isinstance(value, str) and value.strip() != ""


def is_valid_email(email: str) -> bool:
    if not is_non_empty_string(email):
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))


def is_valid_password(password: str) -> bool:
    """
    Password policy:
    - At least 6 characters
    """
    return isinstance(password, str) and len(password) >= 6


def is_valid_object_id(value: str) -> bool:
    """
    Validates MongoDB ObjectId string.
    """
    if not isinstance(value, str):
        return False
    return bool(re.fullmatch(r"[a-fA-F0-9]{24}", value))


# -----------------------------
# Auth Payload Validation
# -----------------------------
def validate_register_payload(data: Dict) -> Tuple[bool, Optional[str]]:
    if not is_non_empty_string(data.get("name")):
        return False, "Name is required"

    if not is_valid_email(data.get("email")):
        return False, "Invalid email address"

    if not is_valid_password(data.get("password")):
        return False, "Password must be at least 6 characters"

    return True, None


def validate_login_payload(data: Dict) -> Tuple[bool, Optional[str]]:
    if not is_valid_email(data.get("email")):
        return False, "Invalid email address"

    if not is_non_empty_string(data.get("password")):
        return False, "Password is required"

    return True, None


# -----------------------------
# Chatbot Validation
# -----------------------------
def validate_chat_message(data: Dict) -> Tuple[bool, Optional[str]]:
    if not is_valid_object_id(data.get("user_id")):
        return False, "Invalid user_id"

    if not is_non_empty_string(data.get("message")):
        return False, "Message cannot be empty"

    return True, None


# -----------------------------
# Prakriti Questionnaire Validation
# -----------------------------
def validate_prakriti_answers(answers: Dict) -> Tuple[bool, Optional[str]]:
    """
    Ensures answers are numeric and within expected range (1–3).
    """

    if not isinstance(answers, dict) or not answers:
        return False, "Answers must be a non-empty object"

    for key, value in answers.items():
        if not isinstance(value, int) or value not in (1, 2, 3):
            return False, f"Invalid answer for '{key}'"

    return True, None


# -----------------------------
# Planner Validation
# -----------------------------
def validate_planner_task(data: Dict) -> Tuple[bool, Optional[str]]:
    required_fields = ["user_id", "task_id", "task_name", "time", "date"]

    for field in required_fields:
        if not is_non_empty_string(data.get(field)):
            return False, f"{field} is required"

    if not is_valid_object_id(data.get("user_id")):
        return False, "Invalid user_id"

    return True, None

# -----------------------------
# Chatbot Intent Detection
# -----------------------------
def detect_chat_intent(message: str) -> str:
    text = message.lower().strip()

    greetings = {"hi", "hello", "hey"}
    capability = {
        "what can you do",
        "help",
        "features",
        "how can you help"
    }

    if text in greetings:
        return "greeting"

    if any(c in text for c in capability):
        return "capability"

    return "symptom"


def is_valid_symptom_text(message: str) -> bool:
    """
    Minimum signal check before ML.
    """
    return len(message.split()) >= 3
