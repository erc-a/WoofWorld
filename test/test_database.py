from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class TestDatabase:
    @pytest.fixture
    def db_client(self):
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client[os.getenv('DB_NAME')]
        yield db
        client.close()

    def test_database_connection(self, db_client):
        assert db_client.command('ping')

    def test_collections_exist(self, db_client):
        collections = db_client.list_collection_names()
        required_collections = ['users', 'breeds', 'favorites']
        assert all(coll in collections for coll in required_collections)

    def test_breed_insertion(self, db_client, test_breed):
        result = db_client.breeds.insert_one(test_breed)
        assert result.inserted_id is not None
        db_client.breeds.delete_one({'_id': result.inserted_id})

    def test_user_creation(self, db_client, test_user):
        result = db_client.users.insert_one(test_user)
        assert result.inserted_id is not None
        db_client.users.delete_one({'_id': result.inserted_id})