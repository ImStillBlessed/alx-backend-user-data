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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
