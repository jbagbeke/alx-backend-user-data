#!/usr/bin/env python3
"""
Session authentication for the api
"""
from api.v1.auth.auth import Auth
from models.user import User
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
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieving user_id for provided session ID
        """
        if not session_id or type(session_id) is not str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """
        AUthenticates current user
        """
        session_id = super().session_cookie(request)

        if session_id:
            user_id = self.user_id_for_session_id(session_id)
            if user_id:
                user_instance = User.get(user_id)

                if user_instance:
                    return user_instance
        return None

    def destroy_session(self, request=None):
        """
        Destroys user session
        """
        if not request:
            return False

        try:
            session_id = self.session_cookie(request)
            if not session_id:
                return False
            if not self.user_id_for_session_id(session_id):
                return False
            del self.user_id_by_session_id[session_id]
            return True
        except Exception:
            return False
