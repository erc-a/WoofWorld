import pytest
import requests
from http import HTTPStatus

class TestBreeds:
    def test_get_all_breeds(self, api_base_url):
        response = requests.get(f"{api_base_url}/breeds")
        assert response.status_code == HTTPStatus.OK
        breeds = response.json()
        assert isinstance(breeds, list)
        assert all(isinstance(breed, dict) for breed in breeds)

    def test_get_breed_by_id(self, api_base_url):
        breed_id = "1"
        response = requests.get(f"{api_base_url}/breeds/{breed_id}")
        assert response.status_code == HTTPStatus.OK
        breed = response.json()
        assert all(key in breed for key in ['id', 'name', 'description'])

    def test_search_breeds(self, api_base_url):
        search_term = "Golden"
        response = requests.get(f"{api_base_url}/breeds/search", 
                              params={"q": search_term})
        assert response.status_code == HTTPStatus.OK
        results = response.json()
        assert all(search_term.lower() in breed["name"].lower() 
                  for breed in results)

    def test_filter_breeds(self, api_base_url):
        filters = {"size": "large", "temperament": "Friendly"}
        response = requests.get(f"{api_base_url}/breeds/filter", 
                              params=filters)
        assert response.status_code == HTTPStatus.OK
        results = response.json()
        assert all(breed["size"] == filters["size"] for breed in results)