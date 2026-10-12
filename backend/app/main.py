"""
backend/app/main.py
-------------------

Main entry point for AyurLife Flask backend.

Responsibilities:
- Create Flask app
- Initialize database
- Register blueprints
- Handle global errors
- Start the server
"""

from flask import jsonify
from app import create_app

# -----------------------------
# App Creation
# -----------------------------
app = create_app()

# -----------------------------
# Database Initialization
# -----------------------------
from app.config.database import init_db
init_db(app)

# -----------------------------
# Blueprint Registration
# -----------------------------
from app.routes.auth_routes import auth_bp
from app.routes.chatbot_routes import chatbot_bp
from app.routes.remedy_routes import remedy_bp
from app.routes.prakriti_routes import prakriti_bp
from app.routes.planner_routes import planner_bp
from app.routes.herb_routes import herb_bp
from app.routes.dashboard_routes import dashboard_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")
app.register_blueprint(remedy_bp, url_prefix="/api/remedies")
app.register_blueprint(prakriti_bp, url_prefix="/api/prakriti")
app.register_blueprint(planner_bp, url_prefix="/api/planner")
app.register_blueprint(herb_bp, url_prefix="/api/herbs")
app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

# -----------------------------
# Health Check Route
# -----------------------------
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "running",
        "message": "AyurLife backend is running successfully"
    })

# -----------------------------
# Global Error Handlers
# -----------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
