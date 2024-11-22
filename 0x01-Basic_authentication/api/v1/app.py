#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

AUTH_TYPE = os.getenv('AUTH_TYPE')
if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def before_request():
    """
    This function performs the following checks in sequence:
    1. Validates if authentication is required for the requested path
    2. Verifies the presence of a valid authorization header
    3. Confirms the existence of a current user

    Returns:
        None: If authentication passes or path is excluded
        Response: 401 if missing/invalid auth header
                 403 if user not found/unauthorized

    Note:
        Excluded paths bypass all authentication checks.
        The function short-circuits and allows the request to proceed if:
        - auth object is None (authentication disabled)
        - requested path is in excluded_paths
    """
    # Skip all auth checks if authentication is disabled
    if auth is None:
        return

    # Define paths that don't require authentication
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']

    # Check if the current path requires authentication
    # If path is in excluded_paths, allow request to proceed
    if not auth.require_auth(request.path, excluded_paths):
        return

    # Verify authorization header exists
    # Return 401 Unauthorized if missing or invalid
    if auth.authorization_header(request) is None:
        abort(401)

    # Verify current user exists and has permission
    # Return 403 Forbidden if user not found or lacks permission
    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
