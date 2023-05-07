import pytest
from unittest.mock import patch
from src.util.dao import DAO
import pymongo

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
def daoSetUp():
    """  Mock the getValidator function and assign it to own validator,  """
    with patch("src.util.dao.getValidator") as mock_get_validator:
        mock_get_validator.return_value = json_validator # Creates own validator for integration_test collection
        dao = DAO("integration_test") # Create collection if not already exists
        try:
            yield dao
        finally:
            dao.drop()

#@pytest.fixture(autouse=True)
#@patch("src.util.dao.getValidator")
#def daoSetUp(mock_get_validator):
#    """  Mock the getValidator function, clear and set up DAO with collection integration_test """
#    mock_get_validator.return_value = json_validator # Creates own validator for integration_test collection
#    dao = DAO("integration_test") # Create collection if not already exists
#
#    return dao

#@pytest.fixture(autouse=True)
#def daoTearDown(daoSetUp):
#    """ Drop the collection after each test is executed """
#    yield
#    daoSetUp.drop()

@pytest.mark.integration
@pytest.mark.parametrize("test_valid_data", [({ "test_name": "Kasper", "test_studying": True })])
def test_create_with_valid_data(daoSetUp, test_valid_data):
    """ Test create function with valid data to see if it creates a document in mongodb """
    test_case = True
    try:
        daoSetUp.create(test_valid_data)
    except pymongo.errors.WriteError:
        test_case = False

    assert test_case == True

@pytest.mark.integration
@pytest.mark.parametrize("invalid_data", [({ "test_name": 2, "test_studying": "hej" })])
def test_create_with_invalid_data(daoSetUp, invalid_data):
    """ Test create function with invalid data to see if it raises an exception """
    try:
        daoSetUp.create(invalid_data)
    except pymongo.errors.WriteError:
        assert True # If raises exception the test success

@pytest.mark.integration
@pytest.mark.parametrize("test_same_uniqueItem", [({ "test_name": "Kasper", "test_studying": True }, { "test_name": "Kasper", "test_studying": False })])
def test_create_with_same_uniqueItems(daoSetUp, test_same_uniqueItem):
    """ 
    Test to create with same name in the test_name (when test name is a uniqueItem) 
    and see if it raises an exception 
    """
    try:
        daoSetUp.create(test_same_uniqueItem)
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
@pytest.mark.parametrize("test_with_not_valid_properties", [({ "test_names": "Kasper", "test_studying": True }, { "test_name": "Kasper", "test_dancing": True })])
def test_create_with_diffrent_property(daoSetUp, test_with_not_valid_properties):
    """ Test to create with same name in the test_name """
    try:
        valid = daoSetUp.create(test_with_not_valid_properties)
        assert False # If not crash then fails the test
    except Exception:
        assert True