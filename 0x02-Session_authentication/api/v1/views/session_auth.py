#!/usr/bin/env python3
"""
Session management authorization for the api
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from api.v1.auth.session_auth import SessionAuth
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    Authenticates session login
    """
    user_email = request.form.get('email')
    if not user_email:
        return jsonify({"error": "email missing"}), 400

    user_password = request.form.get('password')
    if not user_password:
        return jsonify({"error": "password missing"}), 400

    try:
        user_instances = User.search({'email': user_email})
        if not user_instances:
            return jsonify({"error": "no user found for this email"}), 404

        for user in user_instances:
            if user.is_valid_password(user_password):
                from api.v1.app import auth

                session_id = auth.create_session(user.id)
                user_response = jsonify(user.to_json())
                session_key = os.getenv('SESSION_NAME')

                if session_key:
                    user_response.set_cookie(session_key, session_id)
                    return user_response
            return jsonify({"error": "wrong password"}), 401
    except Exception as e:
        return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def delete_session():
    """
    Deletes user session
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
