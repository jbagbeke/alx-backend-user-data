#!/usr/bin/env python3
"""
Basic Authorization implementation
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """
    Basic Authorization implementation
    """

    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """
        Extracts the header in base 64
        """
        if not auth_header or type(auth_header) is not str:
            return None

        if not auth_header.startswith('Basic '):
            return None

        authz = auth_header.split()[1]
        return authz

    def decode_base64_authorization_header(self, b64_auth_hdr: str) -> str:
        """
        Decodes base 64 authorization header
        """
        if not b64_auth_hdr or type(b64_auth_hdr) is not str:
            return None

        try:
            authz_bytes = base64.b64decode(b64_auth_hdr)
            return authz_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, dcoded_b64_auth_hdr: str) -> (str, str):
        """
        Extracting user credentials of user
        """
        if not dcoded_b64_auth_hdr or type(dcoded_b64_auth_hdr) is not str:
            return (None, None)

        if ':' not in dcoded_b64_auth_hdr:
            return (None, None)

        credentials = dcoded_b64_auth_hdr.split(':')

        if len(credentials) != 2:
            return (None, None)

        return (credentials[0], credentials[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        returns a user instance based on pwd and email else None
        """
        if not user_email or type(user_email) is not str:
            return None

        if not user_pwd or type(user_pwd) is not str:
            return None

        try:
            valid_users = User.search({'email': user_email})
            if not valid_users or len(valid_users) < 1:
                return None
            for user in valid_users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves user instance
        """
        auth_header = self.authorization_header(request)

        if auth_header:
            b64_header = self.extract_base64_authorization_header(auth_header)

            if b64_header:
                db4_head = self.decode_base64_authorization_header(b64_header)

                if db4_head:
                    creds = self.extract_user_credentials(db4_head)

                    if creds:
                        user = self.user_object_from_credentials(creds[0],
                                                                 creds[1])

                        if user:
                            return user
