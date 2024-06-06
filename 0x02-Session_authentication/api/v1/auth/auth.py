#!/usr/bin/env python3
"""
Authentication module for the app
"""
from flask import request
import os
import fnmatch
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
        for exclude_path in excluded_paths:
            if fnmatch.fnmatch(path, exclude_path):
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
    
    def session_cookie(self, request=None):
        """
        Returns: a cookie value from a request
        """
        if request == None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name) 
