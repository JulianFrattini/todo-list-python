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
    """ Mock the getValidator function, set up DAO with collection integration_test, and drop the collection after each test. """
    with patch("src.util.dao.getValidator") as mock_get_validator:
        mock_get_validator.return_value = json_validator # Creates own validator for integration_test collection
        dao = DAO("integration_test") # Create collection if not already exists
        try:
            yield dao
        finally:
            dao.drop()

@pytest.mark.integration
@pytest.mark.parametrize("test_valid_property_and_bson_data", [({ "test_name": "Kasper", "test_studying": True })])
def test_create_with_valid_property_and_bson(daoSetUp, test_valid_property_and_bson_data):
    """ Test create function with valid property and bson to see if it creates a document in mongodb """
    result = "success"
    try:
        daoSetUp.create(test_valid_property_and_bson_data)
    except pymongo.errors.WriteError:
        result = "error"

    assert result == "success"

@pytest.mark.integration
@pytest.mark.parametrize("test_invalid_bson_data", [{ "test_name": 2, "test_studying": True }, { "test_name": "Kasper", "test_studying": "hej" }])
def test_create_with_invalid_bson(daoSetUp, test_invalid_bson_data):
    """ Test create function with invalid bson to see if it raises an exception """
    with pytest.raises(pymongo.errors.WriteError) as error:
        daoSetUp.create(test_invalid_bson_data)

@pytest.mark.integration
@pytest.mark.parametrize("test_invalid_properties_data", [{ "test_names": "Kasper", "test_studying": True }, { "test_name": "Kasper", "test_dancing": True }])
def test_create_invalid_properties(daoSetUp, test_invalid_properties_data):
    """ Test to create with diffrent properties (invalid properties)"""
    with pytest.raises(pymongo.errors.WriteError) as error:
        daoSetUp.create(test_invalid_properties_data)

@pytest.mark.integration
def test_create_with_dublicate_names(daoSetUp):
    """ 
    Test to create with duplicate names in the test_name (when test name have a uniqueItem to True) 
    and see if it raises an exception.
    """
    with pytest.raises(pymongo.errors.WriteError) as error:
        daoSetUp.create({ "test_name": "Kasper", "test_studying": True })
        daoSetUp.create({ "test_name": "Kasper", "test_studying": True })


@pytest.mark.integration
def test_create_no_valid_db():
    """ Test to set up dao with no valid database connection """
    with patch("pymongo.MongoClient") as mock_client:
        mock_client.side_effect = Exception()

        with pytest.raises(Exception):
            DAO("integration_test")