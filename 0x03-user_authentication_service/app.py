#!/usr/bin/env python3
"""
User authentication flask application
"""
from flask import Flask, abort, request, jsonify, redirect
from flask import url_for
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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def sessions():
    """
    Session creation for a User
    """
    try:
        user_data = request.form
        email = user_data.get('email')
        password = user_data.get('password')

        if not email or not password:
            abort(401)
        if not AUTH.valid_login(email, password):
            abort(401)
        session_id = AUTH.create_session(email)
        user_response = jsonify({"email": str(email), "message": "logged in"})
        user_response.set_cookie("session_id", session_id)

        return user_response
    except Exception:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Destroys User session
    """
    user_session = request.cookies.get("session_id")
    if not user_session:
        abort(403)
    user = AUTH.get_user_from_session_id(user_session)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('app_root'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    Retrieve User Profile
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": "{}".format(user.email)})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    Password reset for the user
    """
    user_email = request.form.get('email')
    if not user_email:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(user_email)
        return jsonify({"email": str(user_email),
                       "reset_token": str(reset_token)})
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    Updates User Password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    if not email or not reset_token or not new_password:
        abort(403)
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": str(email), "message": "Password updated"})
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
