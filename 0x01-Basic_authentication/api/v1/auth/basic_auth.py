#!/usr/bin/env python3
""" basic_auth """
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ BasicAuth class """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization
        header for a Basic Authentication """
        if authorization_header and \
                isinstance(authorization_header, str) and \
                authorization_header[0: len('Basic ')] == 'Basic ':
            return authorization_header[len('Basic '):]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns the decoded value of a Base64
        string base64_authorization_header """
        if base64_authorization_header and \
                isinstance(base64_authorization_header, str):
            try:
                b64 = base64.b64decode(base64_authorization_header)
                return b64.decode('utf-8')
            except Exception:
                return None
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ returns the user email and password
        from the Base64 decoded value """
        if decoded_base64_authorization_header and \
                isinstance(decoded_base64_authorization_header, str) and \
                ':' in decoded_base64_authorization_header:
            return tuple(decoded_base64_authorization_header.split(':', 1))
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on his email and password """
        if user_email and isinstance(user_email, str) and \
                user_pwd and isinstance(user_pwd, str):
            users = User.search({'email': user_email})
            if len(users) > 0 and users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ (overloaded) retrieves the User instance for a request """
        auth = self.authorization_header(request)
        b64 = self.extract_base64_authorization_header(auth)
        decoded = self.decode_base64_authorization_header(b64)
        credentials = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(*credentials)
