"""
herb_model.py
-------------

Data access model for the Herbs collection.

Encapsulates all MongoDB operations related to Ayurvedic herbs.
"""

from typing import Optional, List, Dict
from app.config.database import get_db


class HerbModel:
    """
    HerbModel provides static methods to interact with herbs collection.
    """

    # -----------------------------
    # Get All Herbs
    # -----------------------------
    @staticmethod
    def get_all() -> List[Dict]:
        db = get_db()
        return list(db.herbs.find({}, {"_id": 0}))

    # -----------------------------
    # Get Herb by herb_id
    # -----------------------------
    @staticmethod
    def get_by_id(herb_id: str) -> Optional[Dict]:
        db = get_db()
        return db.herbs.find_one(
            {"herb_id": herb_id},
            {"_id": 0}
        )

    # -----------------------------
    # Search Herbs
    # -----------------------------
    @staticmethod
    def search(
        query_text: str = None,
        use: str = None,
        dosha: str = None
    ) -> List[Dict]:
        """
        Search herbs by name, therapeutic use, or dosha effect.
        """

        db = get_db()
        herbs = db.herbs

        query = {}

        if query_text:
            query["$or"] = [
                {"name": {"$regex": query_text, "$options": "i"}},
                {"common_names": {"$regex": query_text, "$options": "i"}},
                {"botanical_name": {"$regex": query_text, "$options": "i"}}
            ]

        if use:
            query["used_for"] = {"$regex": use, "$options": "i"}

        if dosha:
            query[f"dosha_effect.{dosha.lower()}"] = {
                "$in": ["pacifies", "balances"]
            }

        return list(herbs.find(query, {"_id": 0}))
