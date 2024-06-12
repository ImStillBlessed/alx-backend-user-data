#!/usr/bin/env python3
"""
This module contaons the User class
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    """
    User class
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __init__(self, email: str, hashed_password: str) -> None:
        """Initialize a new User instance
        """
        self.email = email
        self.hashed_password = hashed_password
        self.session_id = None
        self.reset_token = None
