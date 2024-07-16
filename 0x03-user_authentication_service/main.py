#!/usr/bin/env python3
"""Main
"""
import requests


def register_user(email: str, password: str) -> None:
    """Creates a new user if not already exists
    """
    credentials = {'email': email, 'password': password}
    response = requests.post('localhost:5000/users', data=credentials)
    assert response.json() == {'email': email, 'message': 'user created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """Checks log in with wrong password
    """
    credentials = {'email': email, 'password': password}
    response = requests.post('localhost:5000/sessions', data=credentials)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Checks log in with correct password
    """
    credentials = {'email': email, 'password': password}
    response = requests.post('localhost:5000/sessions', data=credentials)
    assert response.json() == {'email': email, 'message': 'logged in'}
    # cookies
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """Checks if user is not logged in
    """
    response = requests.get('localhost:5000/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Checks if user is logged in
    """
    cookies = {'session_id': session_id}
    response = requests.get('localhost:5000/profile', cookies=cookies)
    assert response.status_code == 200
    # checks for response json


def log_out(session_id: str) -> None:
    """Deletes a user session
    """
    cookies = {'session_id': session_id}
    response.delete('localhost:5000/sessions', cookies=cookies)
    assert response.status_code == 200 and \
        response.json() == {'message': 'Bienvenue'}
    # or 304 temporary redirect


def reset_password_token(email: str) -> str:
    """Returns a new password reset token for the user
    """
    response = requests.post('localhost:5000/reset_password',
                             data={'email': email})
    assert response.status_code == 200
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Checks if user's password is updated
    """
    credentials = {'email': email,
                   'reset_token': reset_token,
                   'new_password': new_password}
    response = requests.put('localhost:5000/reset_password', data=credentials)
    assert response.status_code == 200 and \
        response.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    """Main program
    """
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
