#!/usr/bin/env python3
"""
Session ID expiration class definition
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    Session expiration class implementation
    """
    def __init__(self):
        """
        Constructor method
        """
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates user session
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {'user_id': user_id,
                                                  'created_at': datetime.now()}
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns user_id for the provided session id
        """
        if not session_id:
            return None
        session_user = self.user_id_by_session_id.get(session_id)

        if not session_user:
            return None
        if self.session_duration <= 0:
            return session_user.get('user_id')

        created_at = session_user.get('created_at')
        if not created_at:
            return None
        exp_date = created_at + timedelta(seconds=self.session_duration)

        if exp_date < datetime.now():
            return None
        return session_user.get('user_id')
