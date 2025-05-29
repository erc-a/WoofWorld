import pytest
import jwt
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture
def api_base_url():
    return "http://localhost:8000/api"

@pytest.fixture
def test_user():
    return {
        "email": "test@woofworld.com",
        "password": "TestPass123!",
        "name": "Test User"
    }

@pytest.fixture
def auth_token():
    secret_key = os.getenv('JWT_SECRET_KEY')
    token = jwt.encode({
        'user_id': '12345',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, secret_key, algorithm='HS256')
    return token

@pytest.fixture
def test_breed():
    return {
        "name": "Golden Retriever",
        "size": "large",
        "temperament": ["Friendly", "Intelligent", "Devoted"],
        "life_span": "10-12 years",
        "description": "Friendly family dog"
    }