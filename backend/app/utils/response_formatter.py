"""
response_formatter.py
---------------------

Utility for formatting chatbot responses.

Ensures consistent structure for:
- Chatbot replies
- Remedy recommendations
- Prakriti results
- Error messages
"""

from datetime import datetime
from typing import Optional, Dict, List


# -----------------------------
# Base Response
# -----------------------------
def base_response(
    message: str,
    intent: str,
    extra: Optional[Dict] = None
) -> Dict:
    """
    Builds a base chatbot response.
    """

    response = {
        "timestamp": datetime.utcnow().isoformat(),
        "intent": intent,
        "message": message
    }

    if extra:
        response.update(extra)

    return response


# -----------------------------
# Remedy Recommendation Response
# -----------------------------
def remedy_response(
    recommendation: Dict,
    llm_explanation: Optional[str] = None
) -> Dict:
    """
    Formats remedy recommendation response.
    """

    return base_response(
        message=llm_explanation or
        f"I recommend {recommendation.get('name')}.",
        intent="remedy_recommendation",
        extra={
            "remedy": recommendation,
            "actions": [
                {"type": "save_remedy", "label": "Save Remedy"},
                {"type": "view_precautions", "label": "View Precautions"}
            ]
        }
    )


# -----------------------------
# Prakriti Result Response
# -----------------------------
def prakriti_response(
    prakriti_type: str,
    explanation: Optional[str] = None
) -> Dict:
    """
    Formats Prakriti identification response.
    """

    return base_response(
        message=explanation or
        f"Your Prakriti is identified as {prakriti_type}.",
        intent="prakriti_result",
        extra={
            "prakriti": prakriti_type,
            "actions": [
                {"type": "view_prakriti", "label": "Know Your Prakriti"},
                {"type": "start_planner", "label": "Start Daily Planner"}
            ]
        }
    )


# -----------------------------
# Question Response
# -----------------------------
def question_response(
    questions: List[Dict]
) -> Dict:
    """
    Formats questionnaire response.
    """

    return base_response(
        message="Please answer the following questions:",
        intent="questionnaire",
        extra={
            "questions": questions
        }
    )


# -----------------------------
# Error Response
# -----------------------------
def error_response(message: str) -> Dict:
    """
    Formats error response.
    """

    return base_response(
        message=message,
        intent="error"
    )


# -----------------------------
# General Chat Response
# -----------------------------
def chat_response(
    message: str
) -> Dict:
    """
    Formats general chat response.
    """

    return base_response(
        message=message,
        intent="general_chat"
    )
