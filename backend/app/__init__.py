from flask import Flask
from flask_cors import CORS
from app.config.database import init_db
from app.utils.error_handler import register_error_handlers


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="ayurlife-secret-key",
        JSON_SORT_KEYS=False
    )

    # Enable CORS
    CORS(app, supports_credentials=True)

    # Initialize DB
    init_db(app)

    # Register error handlers
    register_error_handlers(app)

    # Import blueprints (ONLY here)
    from app.routes.auth_routes import auth_bp
    from app.routes.planner_routes import planner_bp
    from app.routes.remedy_routes import remedy_bp
    from app.routes.herb_routes import herb_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.chatbot_routes import chatbot_bp

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(planner_bp, url_prefix="/api/planner")
    app.register_blueprint(herb_bp, url_prefix="/api/herb")

    # 🔥 IMPORTANT: DO NOT add url_prefix again
    app.register_blueprint(remedy_bp)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")

    # Debug: show all routes
    print("\n==== REGISTERED ROUTES ====")
    print(app.url_map)
    print("===========================\n")

    return app
