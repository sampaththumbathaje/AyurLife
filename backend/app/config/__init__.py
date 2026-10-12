def init_db(app):
    from app.config.settings import DevelopmentConfig

    app.config.from_object(DevelopmentConfig)

    mongo_uri = app.config.get("MONGO_URI")

    try:
        client = MongoClient(mongo_uri)
        client.admin.command("ping")
    except ConnectionFailure as e:
        raise RuntimeError(f"❌ MongoDB connection failed: {e}")

    app.mongo_client = client
    app.db = client.get_default_database()
