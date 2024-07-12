#!/usr/bin/env python3
""" session_db_auth """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class """

    def create_session(self, user_id=None):
        """ (overloaded) creates and stores a new UserSession instance """
        if user_id:
            session_id = str(uuid.uuid4())
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """ (overloaded) returns the User ID
        by requesting based on session_id """
        if session_id:
            try:
                user_session = UserSession.search({'session_id': session_id})
                if len(user_session) == 0:
                    return user_session[0].user_id
            except Exception:
                pass
        return None

    def destroy_session(self, request=None):
        """ (overloaded) destroys the UserSession instance """
        if request:
            session_id = request.cookies.get(getenv('SESSION_NAME'))
            if session_id:
                user_session = UserSession.search({'session_id': session_id})
                if user_session:
                    user_session[0].remove()
                    return True
        return False
