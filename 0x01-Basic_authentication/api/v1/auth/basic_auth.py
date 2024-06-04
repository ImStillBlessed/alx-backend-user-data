#!/usr/bin/env python3
"""
This module contains the basic auth class
"""
from auth import Auth


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
