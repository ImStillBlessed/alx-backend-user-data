#!/usr/bin/env python3
"""
encryption module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Encrypt password to byte string
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    checks if a password encryption is correct
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
