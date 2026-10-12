"""
remedy_model.py
---------------

Data access model for the Remedies collection.

Encapsulates all MongoDB operations related to Ayurvedic remedies.
"""

from typing import Optional, List, Dict
from app.config.database import get_db


class RemedyModel:
    """
    RemedyModel provides static methods to interact with remedies collection.
    """

    # -----------------------------
    # Get Remedy by Name
    # -----------------------------
    @staticmethod
    def get_by_name(name: str) -> Optional[Dict]:
        db = get_db()
        return db.remedies.find_one(
            {"name": name},
            {"_id": 0}
        )

    # -----------------------------
    # Get Remedy by remedy_id
    # -----------------------------
    @staticmethod
    def get_by_id(remedy_id: str) -> Optional[Dict]:
        db = get_db()
        return db.remedies.find_one(
            {"remedy_id": remedy_id},
            {"_id": 0}
        )

    # -----------------------------
    # Get All Remedies
    # -----------------------------
    @staticmethod
    def get_all() -> List[Dict]:
        db = get_db()
        return list(db.remedies.find({}, {"_id": 0}))

    # -----------------------------
    # Filter Remedies by Prakriti
    # -----------------------------
    @staticmethod
    def get_by_prakriti(prakriti: str) -> List[Dict]:
        db = get_db()
        return list(
            db.remedies.find(
                {"suitable_prakriti": prakriti},
                {"_id": 0}
            )
        )

    # -----------------------------
    # Search Remedies by Symptom / Category
    # -----------------------------
    @staticmethod
    def search(query: str) -> List[Dict]:
        """
        Search remedies by symptom, name, or category.
        """
        db = get_db()
        return list(
            db.remedies.find(
                {
                    "$or": [
                        {"name": {"$regex": query, "$options": "i"}},
                        {"used_for": {"$regex": query, "$options": "i"}},
                        {"category": {"$regex": query, "$options": "i"}}
                    ]
                },
                {"_id": 0}
            )
        )
