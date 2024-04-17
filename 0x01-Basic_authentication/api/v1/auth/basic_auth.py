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

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the header in base 64
        """
        if not authorization_header or type(authorization_header) != str:
            return None
        
        if not authorization_header.startswith('Basic '):
            return None

        authz = authorization_header.split()[1]

        return authz
        # print(authz)
        # try:
        #     authz_bytes = base64.b64decode(authz)
        #     return authz_bytes.decode('utf-8')
        # except Exception:
        #     return authz
