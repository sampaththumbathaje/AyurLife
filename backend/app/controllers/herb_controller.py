"""
herb_controller.py
------------------

Controller for Ayurvedic Herb Knowledge Base.

Handles:
- Fetching all herbs
- Fetching herb details by herb_id
- Searching herbs by name, use, or dosha
"""

from app.config.database import get_db


# -----------------------------
# Get All Herbs
# -----------------------------
def get_all_herbs():
    """
    Returns all herbs from the knowledge base.
    """
    db = get_db()
    herbs = db.herbs

    return list(herbs.find({}, {"_id": 0}))


# -----------------------------
# Get Herb by herb_id
# -----------------------------
def get_herb_by_id(herb_id: str):
    """
    Returns herb details for a given herb_id.
    """
    db = get_db()
    herbs = db.herbs

    herb = herbs.find_one(
        {"herb_id": herb_id},
        {"_id": 0}
    )

    if not herb:
        return None, "Herb not found"

    return herb, None


# -----------------------------
# Search Herbs
# -----------------------------
def search_herbs(
    query_text: str = None,
    use: str = None,
    dosha: str = None
):
    """
    Searches herbs based on name, usage, or dosha effect.

    Parameters:
    - query_text: herb name / botanical name / common name
    - use: therapeutic use (e.g., cough)
    - dosha: vata / pitta / kapha
    """

    db = get_db()
    herbs = db.herbs

    query = {}

    # Search by name / botanical / common names
    if query_text:
        query["$or"] = [
            {"name": {"$regex": query_text, "$options": "i"}},
            {"common_names": {"$regex": query_text, "$options": "i"}},
            {"botanical_name": {"$regex": query_text, "$options": "i"}}
        ]

    # Search by therapeutic use
    if use:
        query["used_for"] = {"$regex": use, "$options": "i"}

    # Search by dosha effect
    if dosha:
        query[f"dosha_effect.{dosha.lower()}"] = {
            "$in": ["pacifies", "balances"]
        }

    return list(herbs.find(query, {"_id": 0}))
