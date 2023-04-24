import pytest
from unittest.mock import patch
import pymongo
import unittest.mock as mock
from src.util.dao import DAO

json_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["test_name","test_bitcoins", "test_games", "test_fake_or_not"],
        "properties": {
            "test_name": { # Test string and unique (validator)
                "bsonType": "string",
                "uniqueItems": True
            },
            "test_bitcoins": { # Test int (validator)
                "bsonType": "int"
            },
            "test_games": { # Test array (validator)
                "bsonType": "array",
                "items": {
                    "bsonType": "string"
                }
            },
            "test_fake_or_not": { # Test boolean (validator)
                "bsonType": "bool",
            }
        }
    }
}

@pytest.fixture()
@patch("src.util.dao.getValidator")
def daoSetUp(mock_get_validator):
    mock_get_validator.return_value = json_validator
    dao = DAO("test")
    return dao

@pytest.mark.integration
@pytest.mark.parametrize("test_valid_data", [({"test_name": "Juelian", "test_bitcoins": 69,"test_games": ["Game1", "Game2"], "test_fake_or_not":True})])
def test_create_valid_data(daoSetUp, test_valid_data):
    """Document with valid data"""
    validation_result = daoSetUp.create(test_valid_data)
    print(validation_result)
    assert validation_result is not None


# @pytest.mark.integration
# @pytest.mark.parametrize("invalid_data", [({"test_name": "hej", "test_bitcoins": "-25"}), ({"test_name": "", "test_bitcoins": "25"}), ({"test_bitcoins": "25"})])
# def test_create_invalid_data(daoSetUp, invalid_data):
#     """Document with invalid data """
#     with pytest.raises(Exception):
#         daoSetUp.create(invalid_data)


# @pytest.mark.integration
# @pytest.mark.parametrize("test_data", [({"test_name": "Julian", "test_bitcoins": 69}), ({"test_name": "Eriks", "test_bitcoins": 79})])
# def test_create_unique_id(daoSetUp,test_data):
#     """Test create document with unique id"""
#     created_document = daoSetUp.create(test_data)
#     assert created_document is not None
#     assert created_document["_id"] is not None
    
# @pytest.mark.integration
# @pytest.mark.parametrize("test_data", [({"test_name": "Julian", "test_bitcoins": 69,"test_games": ["Game1", "Game2"], "test_fake_or_not":True})])
# def test_create_no_valid_db(daoSetUp, test_data):
#     """test no valid database connection """
#     with patch("pymongo.MongoClient") as mock_client:
#          mock_client.side_effect = Exception("något gick snett brorsan")

#          with pytest.raises(Exception):
#              daoSetUp.create(test_data)
