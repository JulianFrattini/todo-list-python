import pytest
from unittest.mock import patch
from src.util.dao import DAO

collection_name = 'user'

users = [
    {'_id': '01', 'firstName': 'john', 'lastName': 'smith', 'email': 'john.smith@gmail.com'},
    {'_id': '02', 'firstName': 'jane', 'lastName': 'doe', 'email': 'jane.doe@gmail.com'},
    {'_id': '03', 'firstName': 'john', 'lastName': 'smurd', 'email': 'john.smurd@gmail.com'}
]

class TestCreate:
    @pytest.fixture(scope="class")
    def dao(self, mongodb):
        with patch('src.util.dao.pymongo.MongoClient') as mock_client:
            # Replace the edutask database with the mock database
            mock_client.return_value.edutask = mongodb.test

            # Create the DAO instance with the mocked MongoDB connection
            dao = DAO(collection_name)

            yield dao

            # Clean up the database after the test
            mongodb.test[collection_name].drop()

    @pytest.mark.integration
    @pytest.mark.parametrize("user", users)
    def test_return_user(self, dao, user):
       
        result = dao.create(user)

        # Assert that the result is as expected
        assert result == user

    @pytest.mark.integration
    @pytest.mark.parametrize("user", users)
    def test_db_contains_user(self, mongodb, user):
        # Check if the user is in the database
        assert mongodb.test[collection_name].find_one({"_id": user["_id"]}) == user
