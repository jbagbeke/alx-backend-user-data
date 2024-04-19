#!/usr/bin/env python3
"""
Session authentication for the api
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from uuid import uuid4


class SessionAuth(Auth):
    """
    Session authentication class definition
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Session creation method
        """
        if not user_id or type(user_id) is not str:
            return None
        session_id = uuid4()
        SessionAuth.user_id_by_session_id[session_id] = user_id

        return session_id
