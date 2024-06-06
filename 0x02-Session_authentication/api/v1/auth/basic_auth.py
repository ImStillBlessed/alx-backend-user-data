#!/usr/bin/env python3
"""
This module contains the basic auth class
"""
from api.v1.auth.auth import Auth
from typing import TypeVar, Tuple
from models.user import User
import base64


class BasicAuth(Auth):
    """
    this class inherits from auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None or type(
                                authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None or type(
                                base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None or type(
                                decoded_base64_authorization_header
                                ) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> User:
        """
        returns the User instance based on his email and password
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                print('users is not a list of User objects')
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> User:
        """
        overloads Auth and retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None
        decode_header = self.decode_base64_authorization_header(base64_header)
        if decode_header is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(decode_header)
        if user_email is None or user_pwd is None:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)
