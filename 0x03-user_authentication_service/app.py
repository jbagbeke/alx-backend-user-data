#!/usr/bin/env python3
"""
User authentication flask application
"""
from flask import Flask, abort, request, jsonify
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def app_root():
    """
    Root path for the app
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    Registers A user to the Database
    """
    user_data = request.form
    email = user_data.get('email')
    password = user_data.get('password')

    if not email or not password:
        abort(404)
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": str(email), "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
