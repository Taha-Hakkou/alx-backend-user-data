#!/usr/bin/env python3
""" session_exp_auth """
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class """

    def __init__(self):
        """ (overloaded) SessionExpAuth constructor """
        super().__init__()
        sd = getenv('SESSION_DURATION')
        self.session_duration = int(sd) if sd and sd.isdigit() else 0

    def create_session(self, user_id=None):
        """ (overloaded) creates a Session ID """
        session_id = super().create_session(user_id)
        if session_id:
            session_dictionary = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            self.user_id_by_session_id[session_id] = session_dictionary
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """ (overloaded) return User ID based on Session ID """
        if session_id and session_id in self.user_id_by_session_id.keys():
            session_dictionary = self.user_id_by_session_id.get(session_id)
            if self.session_duration <= 0:
                return session_dictionary.get('user_id')
            if 'created_at' in session_dictionary.keys():
                created_at = session_dictionary.get('created_at')
                duration = timedelta(seconds=self.session_duration)
                if created_at + duration > datetime.now():
                    return session_dictionary.get('user_id')
        return None
