from datetime import datetime
from bson import ObjectId

from app.config.database import get_db

# ML imports
from ml.inference.predict_remedy import RemedyPredictor
from ml.inference.predict_prakriti import PrakritiPredictor
from ml.inference.questionnaire_logic import (
    get_questions,
    build_ml_input
)

# -----------------------------
# Load ML models once
# -----------------------------
_remedy_predictor = RemedyPredictor()
_prakriti_predictor = PrakritiPredictor()


# -----------------------------
# Helper intent checks
# -----------------------------
def is_greeting(text: str) -> bool:
    return text.lower().strip() in {"hi", "hello", "hey"}

def is_capability(text: str) -> bool:
    return any(k in text.lower() for k in [
        "what can you do", "help", "features"
    ])

def is_prakriti_request(text: str) -> bool:
    return any(k in text.lower() for k in [
        "prakriti",
        "check prakriti",
        "my prakriti",
        "prakriti test",
        "body type",
        "dosha"
    ])

def is_stop_symptom(text: str) -> bool:
    return text.lower().strip() in {
        "no", "no more", "that's all", "nothing else", "done"
    }


# -----------------------------
# Main Chatbot Handler
# -----------------------------
def handle_chat_message(
    user_id: str,
    message: str,
    session_id: str = None,
    prakriti_answers: dict = None
):
    if not session_id:
        session_id = f"S{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    db = get_db()
    users = db.users
    chat_history = db.chat_history

    # Fetch session data
    session = chat_history.find_one({
        "user_id": ObjectId(user_id),
        "session_id": session_id
    })

    collected_symptoms = session.get("collected_symptoms", []) if session else []

    # -----------------------------
    # PRAKRITI FLOW
    # -----------------------------
    if is_prakriti_request(message):
        # Clear symptom flow if switching
        chat_history.update_one(
            {"user_id": ObjectId(user_id), "session_id": session_id},
            {"$unset": {"collected_symptoms": ""}},
            upsert=True
        )

        return {
            "type": "prakriti_questions",
            "questions": get_questions(),
            "session_id": session_id
        }

    # Handle Prakriti answers
    if prakriti_answers:
        ml_input = build_ml_input(prakriti_answers)
        prakriti = _prakriti_predictor.predict(ml_input)

        users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "prakriti": {
                    "type": prakriti,
                    "last_updated": datetime.utcnow()
                }
            }}
        )

        return {
            "reply": f"Your Prakriti has been identified as {prakriti}.",
            "prakriti": prakriti,
            "session_id": session_id
        }

    # -----------------------------
    # GREETING
    # -----------------------------
    if is_greeting(message):
        reply = "Hello! 👋 Please tell me what symptoms you are experiencing."

    # -----------------------------
    # CAPABILITY
    # -----------------------------
    elif is_capability(message):
        reply = (
            "I can understand your symptoms and suggest Ayurvedic remedies "
            "along with dosage and precautions."
        )

    # -----------------------------
    # USER SAYS NO MORE SYMPTOMS
    # -----------------------------
    elif is_stop_symptom(message):
        if not collected_symptoms:
            reply = "Please tell me at least one symptom."
        else:
            combined = ", ".join(collected_symptoms)
            predicted_remedy = _remedy_predictor.predict(combined)

            reply = (
                f"Based on your symptoms ({combined}), "
                f"I recommend {predicted_remedy}. "
                "Would you like to know the dosage or precautions?"
            )

            # Clear symptoms after prediction
            chat_history.update_one(
                {"user_id": ObjectId(user_id), "session_id": session_id},
                {"$unset": {"collected_symptoms": ""}}
            )

            return {
                "reply": reply,
                "predicted_remedy": predicted_remedy,
                "session_id": session_id
            }

    # -----------------------------
    # SYMPTOM COLLECTION (HUMAN-LIKE)
    # -----------------------------
    else:
        collected_symptoms.append(message)

        chat_history.update_one(
            {"user_id": ObjectId(user_id), "session_id": session_id},
            {"$set": {"collected_symptoms": collected_symptoms}},
            upsert=True
        )

        reply = (
            "Got it 👍 Is there any other symptom? "
            "If not, please type **no**."
        )

    # -----------------------------
    # Save chat history
    # -----------------------------
    chat_history.insert_one({
        "user_id": ObjectId(user_id),
        "session_id": session_id,
        "message": message,
        "reply": reply,
        "timestamp": datetime.utcnow()
    })

    return {
        "reply": reply,
        "session_id": session_id
    }
