from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId

from app.config.database import get_db

from ml.inference.predict_remedy import RemedyPredictor
from ml.inference.predict_prakriti import PrakritiPredictor
from ml.inference.questionnaire_logic import (
    get_questions,
    build_ml_input,
    map_user_input_to_option
)

chatbot_bp = Blueprint("chatbot", __name__)

remedy_predictor = RemedyPredictor()
prakriti_predictor = PrakritiPredictor()


# =====================================================
# HELPERS
# =====================================================

def is_greeting(text):
    return any(
        w in text.lower()
        for w in [
            "hi",
            "hello",
            "hey",
            "namaste"
        ]
    )


def is_capability(text):
    return any(
        k in text.lower()
        for k in [
            "what can you do",
            "help",
            "features"
        ]
    )


def is_prakriti_request(text):
    return any(
        k in text.lower()
        for k in [
            "prakriti",
            "check prakriti",
            "my prakriti",
            "prakriti test",
            "dosha"
        ]
    )


def is_stop_symptom(text):
    return (
        text.lower().strip()
        in {
            "no",
            "no more",
            "that's all",
            "done"
        }
    )


def is_valid_general_input(text):
    text = text.strip().lower()

    return (
        len(text) >= 3
        and any(c.isalpha() for c in text)
    )


# =====================================================
# GET FULL CHAT SESSION
# =====================================================

@chatbot_bp.route(
    "/session/<session_id>",
    methods=["GET"]
)
def get_chat_session(session_id):

    db = get_db()

    chat = db.chat_history

    messages = list(
        chat.find(
            {"session_id": session_id},
            {
                "_id": 0,
                "user_message": 1,
                "bot_reply": 1,
                "prakriti": 1,
                "predicted_remedy": 1,
                "timestamp": 1
            }
        ).sort("timestamp", 1)
    )

    if not messages:
        return jsonify({
            "error": "Session not found"
        }), 404

    formatted = []

    for m in messages:

        formatted.append({
            "sender": "user",
            "text": m.get("user_message")
        })

        formatted.append({
            "sender": "bot",
            "text": m.get("bot_reply"),
            "prakriti": m.get("prakriti"),
            "predictedRemedy":
                m.get("predicted_remedy")
        })

    return jsonify({
        "session_id": session_id,
        "messages": formatted
    }), 200


# =====================================================
# CHATBOT MESSAGE
# =====================================================

@chatbot_bp.route(
    "/message",
    methods=["POST"]
)
def chatbot_message():

    data = request.json

    user_id = data.get("user_id")
    message = data.get("message")
    session_id = data.get("session_id")

    if not user_id or not message:
        return jsonify({
            "reply": "Invalid request."
        }), 400

    db = get_db()

    chat = db.chat_history

    state = db.chat_state

    # =====================================================
    # CREATE SESSION ID
    # =====================================================

    if not session_id:
        session_id = f"S{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    session = state.find_one({
        "user_id": ObjectId(user_id),
        "session_id": session_id
    }) or {}

    mode = session.get("mode")

    collected_symptoms = session.get(
        "collected_symptoms",
        []
    )

    prakriti_step = session.get(
        "prakriti_step",
        0
    )

    prakriti_answers = session.get(
        "prakriti_answers",
        {}
    )

    questions = get_questions()

    reply = ""

    prakriti_response = None

    predicted_remedy = None

    # =====================================================
    # PRAKRITI FLOW
    # =====================================================

    if mode == "prakriti":

        prev_step = prakriti_step - 1

        if prev_step >= 0:

            prev_q = questions[prev_step]

            option_value = (
                map_user_input_to_option(
                    prev_q,
                    message
                )
            )

            if option_value is None:

                return jsonify({
                    "reply":
                        "❌ Invalid input. Please choose one of the options.",

                    "options": [
                        o["label"]
                        for o in prev_q["options"]
                    ],

                    "session_id":
                        session_id
                }), 200

            prakriti_answers[
                prev_q["id"]
            ] = option_value

        # =====================================================
        # FINAL PRAKRITI RESULT
        # =====================================================

        if prakriti_step >= len(questions):

            ml_input = build_ml_input(
                prakriti_answers
            )

            result = (
                prakriti_predictor.predict(
                    ml_input
                )
            )

            prediction = result["prediction"]

            probabilities = (
                result["probabilities"]
            )

            sorted_probs = sorted(
                probabilities.items(),
                key=lambda x: x[1],
                reverse=True
            )

            top1, top2 = (
                sorted_probs[0],
                sorted_probs[1]
            )

            if abs(top1[1] - top2[1]) < 0.05:

                display_text = (
                    f"{top1[0]}-{top2[0]}"
                )

            else:
                display_text = prediction

            prakriti_response = {
                "prediction":
                    display_text,

                "probabilities":
                    probabilities
            }

            # =====================================================
            # SAVE TO USER PROFILE
            # =====================================================

            db.users.update_one(
                {
                    "_id":
                        ObjectId(user_id)
                },

                {
                    "$set": {
                        "prakriti": {
                            "prediction":
                                display_text,

                            "probabilities":
                                probabilities,

                            "identified_at":
                                datetime.utcnow()
                        }
                    }
                }
            )

            # =====================================================
            # CLEAR SESSION STATE
            # =====================================================

            if session.get("_id"):

                state.delete_one({
                    "_id":
                        session["_id"]
                })

            reply = f"🌿 Your Prakriti is {display_text}."

        else:

            next_q = questions[
                prakriti_step
            ]

            state.update_one(

                {
                    "user_id":
                        ObjectId(user_id),

                    "session_id":
                        session_id
                },

                {
                    "$set": {
                        "mode":
                            "prakriti",

                        "prakriti_step":
                            prakriti_step + 1,

                        "prakriti_answers":
                            prakriti_answers
                    }
                },

                upsert=True
            )

            return jsonify({

                "reply":
                    next_q["question"],

                "type":
                    "prakriti_question",

                "options": [
                    o["label"]
                    for o in next_q["options"]
                ],

                "help":
                    next_q.get("help"),

                "session_id":
                    session_id

            }), 200

    # =====================================================
    # START PRAKRITI
    # =====================================================

    elif is_prakriti_request(message):

        first_q = questions[0]

        state.update_one(

            {
                "user_id":
                    ObjectId(user_id),

                "session_id":
                    session_id
            },

            {
                "$set": {
                    "mode":
                        "prakriti",

                    "prakriti_step":
                        1,

                    "prakriti_answers":
                        {}
                }
            },

            upsert=True
        )

        return jsonify({

            "reply":
                first_q["question"],

            "type":
                "prakriti_question",

            "options": [
                o["label"]
                for o in first_q["options"]
            ],

            "help":
                first_q.get("help"),

            "session_id":
                session_id

        }), 200

    # =====================================================
    # GREETING
    # =====================================================

    elif is_greeting(message):

        reply = (
            "Hello! 👋 I’m your Ayurvedic assistant.\n\n"
            "🌿 Type prakriti to identify your constitution\n"
            "💊 Or tell me your symptoms"
        )

    # =====================================================
    # STOP SYMPTOMS
    # =====================================================

    elif is_stop_symptom(message):

        if not collected_symptoms:

            reply = (
                "Please tell me at least one valid symptom."
            )

        else:

            combined = ", ".join(
                collected_symptoms
            )

            remedy = (
                remedy_predictor.predict(
                    combined
                )
            )

            predicted_remedy = remedy

            reply = (
                f"Based on your symptoms ({combined}), "
                f"I recommend {remedy}."
            )

            if session.get("_id"):

                state.delete_one({
                    "_id":
                        session["_id"]
                })

    # =====================================================
    # SYMPTOM COLLECTION
    # =====================================================

    else:

        if not is_valid_general_input(
            message
        ):

            reply = (
                "❌ I couldn't understand that."
            )

        else:

            collected_symptoms.append(
                message
            )

            state.update_one(

                {
                    "user_id":
                        ObjectId(user_id),

                    "session_id":
                        session_id
                },

                {
                    "$set": {
                        "mode":
                            "symptom",

                        "collected_symptoms":
                            collected_symptoms
                    }
                },

                upsert=True
            )

            reply = (
                "Got it 👍 Any other symptom? "
                "If not, type no."
            )

    # =====================================================
    # SAVE CHAT HISTORY
    # =====================================================

    chat.insert_one({

        "user_id":
            ObjectId(user_id),

        "session_id":
            session_id,

        "user_message":
            message,

        "bot_reply":
            reply,

        "prakriti":
            prakriti_response,

        "predicted_remedy":
            predicted_remedy,

        "timestamp":
            datetime.utcnow()
    })

    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    return jsonify({

        "reply":
            reply,

        "prakriti":
            prakriti_response,

        "predicted_remedy":
            predicted_remedy,

        "session_id":
            session_id

    }), 200