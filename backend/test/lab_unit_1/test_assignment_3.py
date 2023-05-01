import pytest
from unittest.mock import patch
from src.util.dao import DAO
from unittest.mock import Mock, call


@pytest.mark.parametrize(
    "input_id",
    [
        (
            20
        ), # test basic functionality
    ]
)
def test_create(input_id):

    
    mock_insert_one = Mock()
    mock_insert_one.inserted_id = input_id

    mock_collection = Mock()
    mock_collection.insert_one.return_value = mock_insert_one
    mock_collection.find_one.return_value = {"Test"}

    mock_database = Mock()
    mock_database.__getitem__ = Mock(return_value=mock_collection)

    mock_database.list_collection_names.return_value = ['test']

    mock_client = Mock()
    mock_client.edutask = mock_database

    with patch('pymongo.MongoClient', return_value=mock_client) as mongo_mock:
        dao = DAO("test")


    assert dao.create({"data" : "data!"}) == ["Test"]

    assert mock_collection.find_one.call_args_list == [call({"_id": input_id})]
