from flask import current_app, g
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def init_db(app):
    """
    Initialize MongoDB connection and attach it to the Flask app.
    """

    from app.config.settings import DevelopmentConfig

    # Load config
    app.config.from_object(DevelopmentConfig)

    mongo_uri = app.config.get("MONGO_URI")
    db_name = app.config.get("MONGO_DB_NAME", "ayurlife")

    try:
        client = MongoClient(mongo_uri)
        client.admin.command("ping")
    except ConnectionFailure as e:
        raise RuntimeError(f"❌ MongoDB connection failed: {e}")

    # Attach client and DB explicitly
    app.mongo_client = client
    app.db = client[db_name]


def get_db():
    if "db" not in g:
        g.db = current_app.db
    return g.db
