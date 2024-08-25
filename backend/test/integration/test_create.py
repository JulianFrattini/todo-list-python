import json
import pytest
import pymongo
from pymongo.errors import WriteError
from unittest.mock import mock_open, patch
from src.util.dao import DAO
from src.util.validators import getValidator

SIMPLIFIED_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["firstName", "lastName", "email"],
        "properties": {
            "firstName": {"bsonType": "string", "description": "must be a string"},
            "lastName": {"bsonType": "string", "description": "must be a string"},
            "age": {"bsonType": "int"},
            "email": {
            "bsonType": "string",
            "description": "must be a string and is required",
            "pattern": "^.+@.+\\..+$"
        }
        }
    }
}

@pytest.fixture(scope="function")
def dao():
    # Initialize DAO with the test database
    dao_instance = DAO(collection_name='user')
    yield dao_instance
    # Clean up before tests to ensure isolation
    dao_instance.collection.delete_many({})

# Case 1
def test_create_valid_user(dao):
    """
    Ensure a new collection is correctly created with a properly initialized object.
    """

    valid_user = {"firstName": "John", "lastName": "Doe", "age": 20, "email": "john.doe@example.com"}
    created_user = dao.create(valid_user)
    assert created_user is not None
    assert created_user['email'] == "john.doe@example.com"

# Case 2
def test_attempt_to_create_duplicate_data_raises_error(dao):
    """
    Verify that attempting to add a user with an existing email raises a DuplicateKeyError, ensuring email uniqueness.
    """

    # The first set of data should be inserted without any issues.
    valid_data = {
        "firstName": "John",
        "lastName": "Doe",
        "age": 25,
        "email": "john@example.com",
    }
    dao.create(valid_data)

    # Inserting another document with the same 'email' should fail because 'email' is unique.
    duplicate_data = {
        "firstName": "Jane",
        "lastName": "Doe",
        "age": 25,
        "email": "john@example.com",  # Same email as in valid_data
    }

    with pytest.raises(pymongo.errors.WriteError):
        dao.create(duplicate_data)

# Case 3
def test_create_valid_does_not_match_bson_unique(dao):
    """
    Test the creation with incorrect BSON type should raise a validation error.
    """

    invalid_bson_type_data = {
        "firstName": ["John"],
        "lastName": ["Sven"],
        "age": "30",
        "email": "john.sven@example.com",
    }

    # Try to create a document with incorrect BSON types
    with pytest.raises(pymongo.errors.WriteError) as exc_info:
        dao.create(invalid_bson_type_data)

# Case 4
def test_create_invalid_data(dao):
    """
    Test the attempting to create a user with invalid data types for all fields results in a WriteError.
    """
    invalid_data = {
        "firstName": 123,
        "lastName": 43,
        "age": "Eleven",
        "email": "john@example.com",
    }
    with pytest.raises(pymongo.errors.WriteError) as excinfo:
        dao.create(invalid_data)


# Case 5, test not valid data, no match with the BSON but with unique identifier.
def test_create_with_invalid_data_and_type_errors(dao):
    invalid_data = {
        "firstName": 123,
        "lastName": 213,
        "age": "twenty",
        "email": "not-an-email"
    }

    # Attempt to insert invalid data and expect validation failure
    with pytest.raises(pymongo.errors.WriteError) as exc_info:
        dao.create(invalid_data)


# Case 6, test valid data, no match with BSON and not unique.
def test_valid_data_not_unique_type_mismatch(dao):
    # Insert with valid data
    valid_user = {"firstName": "Nisreen", "lastName": "Adb", "age": 11, "email": "nisreen@example.com"}
    dao.create(valid_user)

    # Trying to insert another record with non-matching BSON types and no-unique email
    invalid_user = {"firstName": "Nisreen", "lastName": "Adb", "age": "eleven", "email": 123}
    with pytest.raises(pymongo.errors.WriteError) as exc_info:
        dao.create(invalid_user)


# Case 7, test not valid data, no match and not unique.
def test_invalid_not_unique_data_type_mismatch(dao):
    user_data = {"firstName": "Sara", "lastName": "ka", "age": 13, "email": "sara@example.com"}
    dao.create(user_data)

    invalid_user = {"firstName": 123, "lastName": "ka", "age": "thirteen","email": "sara@example.com"}
    with pytest.raises(pymongo.errors.WriteError) as exc_info:
        dao.create(invalid_user)

# Test not valid data, matches BSON and not unqiue. 
def test_non_unique_email_with_valid_bson_raises_error(dao):
    valid_user = {"firstName": "John", "lastName": "Doe", "age": 30, "email": "email@example.com"}
    dao.create(valid_user)

    invalid_user = {"firstName": "Jane", "lastName": "Doe", "age": -1, "email": "email@example.com"}
    with pytest.raises(pymongo.errors.WriteError):
        dao.create(invalid_user)
