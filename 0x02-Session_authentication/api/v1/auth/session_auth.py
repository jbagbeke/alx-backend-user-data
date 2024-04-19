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
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieving user_id for provided session ID
        """
        if not session_id or type(session_id) is not str:
            return None

        val =  SessionAuth.user_id_by_session_id["session_id"]
        print()
        print(val)
        print()
