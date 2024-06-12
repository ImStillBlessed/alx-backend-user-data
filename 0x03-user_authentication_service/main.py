#!/usr/bin/env python3
"""
Main test file
advanced task
"""
import requests

BASE_URL = 'http://localhost:5000'  # Update with your Flask app's base URL

def register_user(email: str, password: str) -> None:
    url = f'{BASE_URL}/users'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

def log_in_wrong_password(email: str, password: str) -> None:
    url = f'{BASE_URL}/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 401

def log_in(email: str, password: str) -> str:
    url = f'{BASE_URL}/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert 'session_id' in response.cookies
    return response.cookies['session_id']

def profile_unlogged() -> None:
    url = f'{BASE_URL}/profile'
    response = requests.get(url)
    assert response.status_code == 403

def profile_logged(session_id: str) -> None:
    url = f'{BASE_URL}/profile'
    cookies = {'session_id': session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    assert response.json()['email'] == "user@example.com"  # Replace with expected email

def log_out(session_id: str) -> None:
    url = f'{BASE_URL}/sessions'
    cookies = {'session_id': session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200

def reset_password_token(email: str) -> str:
    url = f'{BASE_URL}/reset_password'
    data = {'email': email}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    return response.json()['reset_token']

def update_password(email: str, reset_token: str, new_password: str) -> None:
    url = f'{BASE_URL}/reset_password'
    data = {'email': email, 'reset_token': reset_token, 'new_password': new_password}
    response = requests.put(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}
