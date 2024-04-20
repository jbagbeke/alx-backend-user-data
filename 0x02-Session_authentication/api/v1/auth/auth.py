#!/usr/bin/env python3
"""
Basic Auth Implementation
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    Basic Authorization class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Auth requirement method
        """
        if not path or not excluded_paths or not len(excluded_paths):
            return True

        if path[-1] != '/':
            if path + '/' in excluded_paths:
                return False

        for p in excluded_paths:
            if p.endswith('*'):
                if path.startswith(p[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Handles authorization header
        """
        if not request or not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Checks current user
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request
        """
        if not request:
            return None
        
        session_name_val = os.getenv("SESSION_NAME")

        if session_name_val:
            return request.cookies.get(session_name_val)
        else:
            os.environ["SESSION_NAME"] = "_my_session_id"
            return request.cookies.get("_my_session_id", None)
