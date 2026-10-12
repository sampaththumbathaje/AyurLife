from flask import Blueprint, request, jsonify
from app.config.database import get_db

herb_bp = Blueprint("herb", __name__)

# -----------------------------
# Get All Herbs
# -----------------------------
@herb_bp.route("/herbs", methods=["GET"], strict_slashes=False)
def get_all_herbs():
    db = get_db()
    result = db.herbs.find({}, {"_id": 0})
    return jsonify(list(result)), 200


# -----------------------------
# Get Herb by herb_id (H001)
# -----------------------------
@herb_bp.route("/herbs/id/<string:herb_id>", methods=["GET"], strict_slashes=False)
def get_herb_by_id(herb_id):
    db = get_db()
    herb = db.herbs.find_one(
        {"herb_id": herb_id},
        {"_id": 0}
    )

    if not herb:
        return jsonify({"error": "Herb not found"}), 404

    return jsonify(herb), 200


# -----------------------------
# ✅ Get Herb by NAME (Tulsi)
# -----------------------------
@herb_bp.route("/herbs/name/<string:herb_name>", methods=["GET"], strict_slashes=False)
def get_herb_by_name(herb_name):
    db = get_db()
    herb = db.herbs.find_one(
        {"name": {"$regex": f"^{herb_name}$", "$options": "i"}},
        {"_id": 0}
    )

    if not herb:
        return jsonify({"error": "Herb not found"}), 404

    return jsonify(herb), 200


# -----------------------------
# Search Herbs
# -----------------------------
@herb_bp.route("/herbs/search", methods=["GET"], strict_slashes=False)
def search_herbs():
    query_text = request.args.get("q")
    use = request.args.get("use")
    dosha = request.args.get("dosha")

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
        query["dosha_effect.pacify"] = dosha.capitalize()

    result = herbs.find(query, {"_id": 0})
    return jsonify(list(result)), 200
