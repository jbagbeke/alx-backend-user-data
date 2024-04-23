#!/usr/bin/env python3
"""
Authorization authentication
"""
# from db import DB
# from user import User
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Password hashing function using bcrypt
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                    bcrypt.gensalt())
    return hashed_password
