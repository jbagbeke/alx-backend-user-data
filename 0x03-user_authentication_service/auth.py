#!/usr/bin/env python3
"""
Authorization authentication
"""
# from db import DB
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Password hashing function using bcrypt
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                    bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """
    Generates UUIDs
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers and adds user to the dataBase
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates User login
        """
        try:
            user = self._db.find_user_by(email=email)
            if not user:
                return False
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except Exception:
            return False
    
    def create_session(self, email: str) -> str:
        """
        Creates User session and stores in the database
        """
        try:
            user = self._db.find_user_by(email=email) 
            if not user:
                None
            user_uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=user_uuid)
            return user_uuid
        except Exception:
            return None
