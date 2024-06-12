#!/usr/bin/env python3
"""
method modules for the db setup
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    returns the hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def _generate_uuid():
    pass


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> None:
        """
        register a user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            self._db.add_user(email, _hash_password(password))
    
    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login credentials.
        
        Args:
        - email: str - The user's email.
        - password: str - The user's password.
        
        Returns:
        - bool - True if the login credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
                return True
            return False
        except NoResultFound:
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
