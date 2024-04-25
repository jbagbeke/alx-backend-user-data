#!/usr/bin/env python3
"""
Testing API ENDPOINTS OF AUTHENTICATION SERVICE
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Check user registration endpoint
    """
    response1 = requests.post('http://127.0.0.1:5000/users',
                              data={'email': email,
                                    'password': password})
    assert response1.status_code == 200
    assert response1.json() == {"email": email, "message": "user created"}

    response2 = requests.post('http://127.0.0.1:5000/users',
                              data={'email': email,
                                    'password': password})
    assert response2.status_code == 400
    assert response2.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Check login endpoint
    """
    response1 = requests.post('http://127.0.0.1:5000/sessions',
                              data={'email': email,
                                    'password': password})
    assert response1.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Check login endpoint of api
    """
    response1 = requests.post('http://127.0.0.1:5000/sessions',
                              data={'email': email,
                                    'password': password})
    assert response1.status_code == 200
    assert response1.json() == {"email": email, "message": "logged in"}
    return response1.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    Check profile endpoint of api with wrong session_id
    """
    response1 = requests.get('http://127.0.0.1:5000/profile',
                             cookies={"session_id": "invalid_session_id"})
    assert response1.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Checks profile endpoint with correct session_id
    """
    response1 = requests.get('http://127.0.0.1:5000/profile',
                             cookies={"session_id": session_id})
    assert response1.status_code == 200


def log_out(session_id: str) -> None:
    """
    Testing Logout endpoint of api
    """
    response1 = requests.delete('http://127.0.0.1:5000/sessions',
                                cookies={"session_id": session_id})
    assert response1.status_code == 200
    assert response1.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    Check password reset endpoint of api
    """
    response1 = requests.post('http://127.0.0.1:5000/reset_password',
                              data={'email': email})
    reset_token = response1.json().get("reset_token")
    assert response1.status_code == 200
    assert response1.json() == {"email": email, "reset_token": reset_token}

    response2 = requests.post('http://127.0.0.1:5000/reset_password',
                              data={'email': "a_very_fake_email"})
    assert response2.status_code == 403
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Check password update endpoint
    """
    response1 = requests.put('http://127.0.0.1:5000/reset_password',
                             data={'email': email,
                                   'reset_token': reset_token,
                                   'new_password': new_password})
    assert response1.status_code == 200
    assert response1.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
