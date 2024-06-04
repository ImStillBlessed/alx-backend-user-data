#!/usr/bin/env python3
"""
Authentication module for the app
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Authentication class definition
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that require authentication
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Method that handles authorization header
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that handles current user
        """
        return None
