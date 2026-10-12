"""
chat_history_model.py
---------------------

Data access model for Chat History collection.

Encapsulates all MongoDB operations related to:
- Chat sessions
- Chat messages
- Conversation history
"""

from datetime import datetime
from typing import List, Dict, Optional
from bson import ObjectId

from app.config.database import get_db


class ChatHistoryModel:
    """
    ChatHistoryModel provides static methods to interact with
    the chat_history collection.
    """

    # -----------------------------
    # Create New Chat Session
    # -----------------------------
    @staticmethod
    def create_session(
        user_id: str,
        session_id: str,
        messages: List[Dict]
    ):
        db = get_db()
        return db.chat_history.insert_one({
            "user_id": ObjectId(user_id),
            "session_id": session_id,
            "messages": messages,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })

    # -----------------------------
    # Append Message to Existing Session
    # -----------------------------
    @staticmethod
    def append_message(
        user_id: str,
        session_id: str,
        message: Dict
    ):
        db = get_db()
        return db.chat_history.update_one(
            {
                "user_id": ObjectId(user_id),
                "session_id": session_id
            },
            {
                "$push": {"messages": message},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )

    # -----------------------------
    # Get All Sessions for User
    # -----------------------------
    @staticmethod
    def get_sessions_by_user(user_id: str) -> List[Dict]:
        db = get_db()
        return list(
            db.chat_history.find(
                {"user_id": ObjectId(user_id)},
                {"_id": 0}
            ).sort("created_at", -1)
        )

    # -----------------------------
    # Get Recent Chat Sessions
    # -----------------------------
    @staticmethod
    def get_recent_sessions(
        user_id: str,
        limit: int = 5
    ) -> List[Dict]:
        db = get_db()
        return list(
            db.chat_history.find(
                {"user_id": ObjectId(user_id)},
                {
                    "session_id": 1,
                    "created_at": 1,
                    "messages": {"$slice": -2},
                    "_id": 0
                }
            ).sort("created_at", -1).limit(limit)
        )

    # -----------------------------
    # Get Full Session by session_id
    # -----------------------------
    @staticmethod
    def get_session(
        user_id: str,
        session_id: str
    ) -> Optional[Dict]:
        db = get_db()
        return db.chat_history.find_one(
            {
                "user_id": ObjectId(user_id),
                "session_id": session_id
            },
            {"_id": 0}
        )
