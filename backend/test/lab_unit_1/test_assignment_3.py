import pytest
from unittest.mock import patch, Mock, call
from src.util.dao import DAO


class TestCreate:
    @pytest.fixture
    def mock_collection(self):
        return Mock()

    @pytest.fixture
    def sut(self, mock_collection):
        mock_insert_one = Mock()
        mock_insert_one.inserted_id = 20

        mock_collection.insert_one.return_value = mock_insert_one
        mock_collection.find_one.return_value = {"Test"}

        mock_database = Mock()
        mock_database.__getitem__ = Mock(return_value=mock_collection)
        mock_database.list_collection_names.return_value = ['test']

        mock_client = Mock()
        mock_client.edutask = mock_database

        with patch('pymongo.MongoClient', return_value=mock_client) as mongo_mock:
            dao = DAO("test")
            return dao

    def test_create(self, sut, mock_collection):
        assert sut.create({"data": "data!"}) == ["Test"]
        assert mock_collection.find_one.call_args_list == [call({"_id": 20})]
