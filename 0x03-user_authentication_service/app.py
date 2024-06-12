#!/usr/bin/env python3
"""
Flask app module
"""
from flask import Flask, request, jsonify, abort
from flask import make_response, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def flask_home():
    """
    A GET request handler for the flask app.
    Returns a JSON response with a welcome message.
    """
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    Register a new user.
    Expects form data with "email" and "password".
    Returns a JSON response with the registration status.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions',  methods=['POST'], strict_slashes=False)
def login():
    """
    Log in a user.
    Expects form data with "email" and "password".
    If the login is successful, creates a session
    sets the session ID as a cookie,
    and returns a JSON response with the login status.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Log out a user.
    Expects the session ID as a cookie with key "session_id".
    If the user exists, destroy the session and redirect to the home page.
    If the user does not exist, respond with a 403 HTTP status.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect(url_for('flask_home'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    Get the user's profile.
    Expects the session ID as a cookie with key "session_id".
    If the user exists, respond with a JSON
    payload containing the user's email and a 200 HTTP status.
    If the session ID is invalid or the user
    does not exist, respond with a 403 HTTP status.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password():
    """
    Reset password route.
    Expects form data with "email".
    If the email is registered, generates a reset token and returns it.
    """
    email = request.form.get('email')

    if not email:
        abort(400)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    Reset password route.
    Expects form data with "email", "reset_token" and "new_password".
    If the token is invalid, responds with a 403 status code.
    Otherwise, updates the password and responds with a 200 HTTP status.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not (email and reset_token and new_password):
        abort(400)

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
