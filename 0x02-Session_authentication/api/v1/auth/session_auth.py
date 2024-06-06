#!/usr/bin/env python3
"""
Authentication module for the app
"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """
    session authentication class
    for creating a new authentication mechanism.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for the user_id in routing
        """
        if type(user_id) == str:
            session_id = uuid.uuid4()
            self.user_id_by_session_id[session_id] = user_id
        return session_id
