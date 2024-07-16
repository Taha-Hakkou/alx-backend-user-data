#!/usr/bin/env python3
"""Auth module
"""
from db import DB
from user import User
import bcrypt
import uuid
from typing import Union

from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """"""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {user.email} already exists')
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if the credentials are valid
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Returns the Session ID of corresponding user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Returns the corresponding user to Session ID
        """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                pass
        return None

    def destroy_session(self, user_id: int) -> None:
        """Updates user's Session ID to None
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Creates a password reset token for user
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Changes user's password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password)
            self._db.update_user(user.id, reset_token=None)
        except NoResultFound:
            raise ValueError


def _hash_password(password: str) -> bytes:
    """Returns a salted hash of the input password
    """
    b_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(b_password, salt)


def _generate_uuid() -> str:
    """Returns string representation of a new uuid
    """
    return str(uuid.uuid4())
