import pytest
import requests
from http import HTTPStatus

class TestFavorites:
    def test_add_favorite(self, api_base_url, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        breed_id = "1"
        response = requests.post(
            f"{api_base_url}/favorites",
            headers=headers,
            json={"breed_id": breed_id}
        )
        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert "id" in data
        assert data["breed_id"] == breed_id

    def test_get_user_favorites(self, api_base_url, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{api_base_url}/favorites", headers=headers)
        assert response.status_code == HTTPStatus.OK
        favorites = response.json()
        assert isinstance(favorites, list)
        assert all(isinstance(fav, dict) for fav in favorites)

    def test_remove_favorite(self, api_base_url, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        favorite_id = "1"
        response = requests.delete(
            f"{api_base_url}/favorites/{favorite_id}",
            headers=headers
        )
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_unauthorized_access(self, api_base_url):
        response = requests.get(f"{api_base_url}/favorites")
        assert response.status_code == HTTPStatus.UNAUTHORIZED