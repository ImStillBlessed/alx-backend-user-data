#!/usr/bin/env python3
"""
method modules for the db setup
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
    returns the hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid():
    """
    The function should return a string representation of a new UUID
    """
    return str(uuid.uuid4())


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
            if user and bcrypt.checkpw(password.encode('utf-8'),
                                       user.hashed_password.encode('utf-8')):
                return True
            return False
        except NoResultFound:
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def create_session(self, email: str) -> str:
        """
        It takes an email string argument
        and returns the session ID as a string.
        """
        user = self._db.find_user_by(email)
        session_id = _generate_uuid()
        user.session_id = session_id
        self._db._session.commit()
        return session_id

    def get_user_from_session_id(self, session_id: str):
        """
        Retrieve a user based on a session ID.
        Args:
        - session_id: str - The session ID.
        Returns:
        - User or None: The user if found, otherwise None.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user's session by setting their session ID to None.
        Args:
        - user_id: int - The user's ID.
        Returns:
        - None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db._session.commit()
        except NoResultFound:
            pass
