#!/usr/bin/env python3
"""
Flask app module
"""
from flask import Flask, request, jsonify
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
