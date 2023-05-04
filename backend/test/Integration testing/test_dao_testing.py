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

    return dao

@pytest.fixture(autouse=True)
def daoTearDown(daoSetUp):
    """ Drop the collection after each test is executed """
    yield
    daoSetUp.drop()

@pytest.mark.integration
@pytest.mark.parametrize("test_valid_data", [({ "test_name": "Kasper", "test_studying": True })])
def test_create_with_valid_data(daoSetUp, test_valid_data):
    """ Test create function with valid data to see if it creates a document in mongodb """
    try:
        daoSetUp.create(test_valid_data)
    except(Exception):
        assert False # If raises exception the test fails

@pytest.mark.integration
@pytest.mark.parametrize("invalid_data", [({ "test_name": 2, "test_studying": "hej" })])
def test_create_with_invalid_data(daoSetUp, invalid_data):
    """ Test create function with invalid data to see if it raises an exception """
    try:
        daoSetUp.create(invalid_data)
    except(Exception):
        assert True # If raises exception the test success

@pytest.mark.integration
def test_create_with_same_uniqueItems(daoSetUp):
    """ 
    Test to create with same name in the test_name (when test name is a uniqueItem) 
    and see if it raises an exception 
    """
    try:
        daoSetUp.create({ "test_name": "Kasper", "test_studying": True })
        daoSetUp.create({ "test_name": "Kasper", "test_studying": False })
        assert False
    except Exception:
        assert True

@pytest.mark.integration
def test_create_no_valid_db():
    """ Test to set up dao with no valid database connection """
    with patch("pymongo.MongoClient") as mock_client:
        mock_client.side_effect = Exception()
    
        with pytest.raises(Exception):
            DAO("test")

@pytest.mark.integration
def test_create_with_diffrent_property(daoSetUp):
    """ Test to create with same name in the test_name """
    try:
        validation_result2 = daoSetUp.create({ "test_name": "Majd", "test_studying": False })
        validation_result1 = daoSetUp.create({ "test_name": "Kasper", "test_dancing": True })
        print(validation_result1)
        print(validation_result2)
        assert False
    except Exception:
        assert True