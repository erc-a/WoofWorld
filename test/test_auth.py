import pytest
import requests
from http import HTTPStatus

class TestAuth:
    def test_user_registration(self, api_base_url, test_user):
        response = requests.post(f"{api_base_url}/auth/register", json=test_user)
        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert all(key in data for key in ['id', 'token', 'email'])

    def test_duplicate_registration(self, api_base_url, test_user):
        # First registration
        requests.post(f"{api_base_url}/auth/register", json=test_user)
        # Duplicate registration
        response = requests.post(f"{api_base_url}/auth/register", json=test_user)
        assert response.status_code == HTTPStatus.CONFLICT

    def test_login_success(self, api_base_url, test_user):
        response = requests.post(f"{api_base_url}/auth/login", 
                               json={"email": test_user["email"], 
                                   "password": test_user["password"]})
        assert response.status_code == HTTPStatus.OK
        assert "token" in response.json()

    def test_login_invalid_credentials(self, api_base_url):
        response = requests.post(f"{api_base_url}/auth/login", 
                               json={"email": "wrong@email.com", 
                                   "password": "wrongpass"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_token_validation(self, api_base_url, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{api_base_url}/auth/validate", headers=headers)
        assert response.status_code == HTTPStatus.OK