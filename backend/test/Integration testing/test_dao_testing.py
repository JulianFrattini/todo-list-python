import pytest
from unittest.mock import patch
from src.util.dao import DAO

# Create own Schema Validator (mongodb)
json_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["test_name","test_studying"],
        "properties": {
            "test_name": { # (Name of the person) Test string and unique (validator)
                "bsonType": "string",
                "uniqueItems": True
            },
            "test_studying": { # (If you are studying or not) - Test boolean (validator)
                "bsonType": "bool",
            }
        }
    }
}

@pytest.fixture(autouse=True)
@patch("src.util.dao.getValidator")
def daoSetUp(mock_get_validator):
    """  Mock the getValidator function, clear and set up DAO with collection integration_test """
    mock_get_validator.return_value = json_validator # Creates own validator for integration_test collection
    dao = DAO("integration_test") # Create collection if not already exists
    dao.drop() # Drop the collection to be sure to remove everything (Yiled not working)
    dao = DAO("integration_test") # Create collection again if not already exists

    return dao

@pytest.mark.integration
@pytest.mark.parametrize("test_valid_data", [({ "test_name": "Kasper", "test_studying": True })])
def test_create_with_valid_data(daoSetUp, test_valid_data):
    """ Test create function with valid data to see if it creates a document in mongodb """
    validation_result = daoSetUp.create(test_valid_data)
    users = daoSetUp.find()

    assert validation_result is not None
    assert len(users) == 1

@pytest.mark.integration
@pytest.mark.parametrize("invalid_data", [({ "test_name": 2, "test_studying": "hej" })])
def test_create_with_invalid_data(daoSetUp, invalid_data):
    """ Test create function with invalid data to see if it raises a exception and it hasen't created any document in mongodb """
    with pytest.raises(Exception):
        daoSetUp.create(invalid_data)

    users = daoSetUp.find()

    assert len(users) == 0

@pytest.mark.integration
def test_create_unique_id(daoSetUp):
    """ Test create function with valid data and look for if it's unique id on both users that has been created """
    daoSetUp.create({ "test_name": "Majd", "test_studying": True })
    daoSetUp.create({ "test_name": "Kasper", "test_studying": True })
    users = daoSetUp.find()

    assert users[0]["_id"] != users[1]["_id"]

@pytest.mark.integration
def test_create_no_valid_db():
    """ Test to set up dao with no valid database connection """
    with patch("pymongo.MongoClient") as mock_client:
        mock_client.side_effect = Exception()
    
        with pytest.raises(Exception):
            DAO("test")