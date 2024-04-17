#!/usr/bin/env python3
"""
Basic Authorization implementation
"""
from api.v1.auth.auth import Auth
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
        # print(authz)
        # try:
        #     authz_bytes = base64.b64decode(authz)
        #     return authz_bytes.decode('utf-8')
        # except Exception:
        #     return authz
