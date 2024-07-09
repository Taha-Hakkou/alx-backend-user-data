#!/usr/bin/env python3
""" auth """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns True if the path is not in the list of strings excluded_paths """
        if path and excluded_paths and len(excluded_paths) > 0:
            if path[-1] != '/':
                path += '/'
            if path in excluded_paths:
                return False
            for xpath in excluded_paths:
                if xpath[-1] == '*':
                    if path[:len(xpath[:-1])] == xpath[:-1]:
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """ returns the value of the header request Authorization """
        if request is None:
            return None
        authorization = request.headers.get('Authorization')
        return authorization if authorization else None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user """
        return None
