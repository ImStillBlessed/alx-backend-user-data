#!/usr/bin/env python3
""" Module of session views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv
from typing import TypeVar


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
      - 400 if email or password is missing
      - 401 if email or password is incorrect
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({"error": "email is missing"}), 400
    if password is None:
        return jsonify({"error": "password is missing"}), 400
    users = User.search({'email': email})
    if users == []:
        return jsonify({ "error": "no user found for this email" }), 404
    user = users[0]
    if not user.is_valid_password(password):
            return jsonify({ "error": "wrong password" }), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    SESSION_NAME = getenv('SESSION_NAME')
    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)
    return response
