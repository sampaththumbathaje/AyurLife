"""
error_handler.py
----------------

Centralized error handling utilities for the backend.

Provides:
- Standard error response format
- Global Flask error handlers
"""

from flask import jsonify
from werkzeug.exceptions import HTTPException


# -----------------------------
# Error Response Builder
# -----------------------------
def error_response(
    message: str,
    status_code: int = 400,
    error_type: str = "error"
):
    """
    Builds a standardized error response.
    """
    return jsonify({
        "status": "failure",
        "error_type": error_type,
        "message": message
    }), status_code


# -----------------------------
# Register Global Error Handlers
# -----------------------------
def register_error_handlers(app):
    """
    Registers global error handlers to the Flask app.
    """

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return error_response(
            message=e.description,
            status_code=e.code,
            error_type=e.name
        )

    @app.errorhandler(404)
    def handle_not_found(e):
        return error_response(
            message="Resource not found",
            status_code=404,
            error_type="NotFound"
        )

    @app.errorhandler(401)
    def handle_unauthorized(e):
        return error_response(
            message="Unauthorized access",
            status_code=401,
            error_type="Unauthorized"
        )

    @app.errorhandler(500)
    def handle_internal_error(e):
        return error_response(
            message="Internal server error",
            status_code=500,
            error_type="ServerError"
        )
