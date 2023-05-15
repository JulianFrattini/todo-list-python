import pytest
from src.util.dao import DAO
from unittest.mock import patch
from pymongo.errors import WriteError


@pytest.fixture
def mock_validator():
    # Define the mocked validator
    validator = {"$jsonSchema": {
        "bsonType": "object",
        "required": ["firstName", "lastName", "email"],
        "properties": {
            "firstName": {
                    "bsonType": "string",
                    "description": "the first name of a user must be determined"
            },
            "lastName": {
                "bsonType": "string",
                "description": "the last name of a user must be determined"
            },
            "email": {
                "bsonType": "string",
                "description": "the email address of a user must be determined",
                "uniqueItems": True
            },
            "tasks": {
                "bsonType": "array",
                "items": {
                    "bsonType": "objectId"
                }
            }
        }
    }
    }

    with patch('src.util.dao.getValidator', autospec=True) as mocked_validator:
        mocked_validator.return_value = validator
        dao = DAO(collection_name="test_user_collection")
        yield dao
        dao.collection.drop()

@pytest.mark.unit
def test_create_user_with_valid_email(mock_validator):
    # Call the create method and check the return value
    new_user = {
        "firstName": "testCase1",
        "lastName": "testingCase1",
        "email": "testcase1@test.com",
        "tasks": []
    }
    result = mock_validator.create(new_user)

    assert result['firstName'] == new_user['firstName']
    assert result['lastName'] == new_user['lastName']
    assert result['email'] == new_user['email']

@pytest.mark.unit
def test_create_user_with_same_email(mock_validator):
    # Call the create method and check the return value

    # New user with same email as a existing user (email has to be unique)
    new_user = {
        "firstName": "testCase1",
        "lastName": "testingCase1",
        "email": "testcase1@test.com",
        "tasks": []
    }
    # Use pytest.raises to check if WriteError is raised
    with pytest.raises(WriteError) as e:
        mock_validator.create(new_user)
    assert isinstance(e.value, WriteError)

@pytest.mark.unit
def test_create_user_with_invalid_email_type(mock_validator):
    # Call the create method and check the return value
    new_user = {
        "firstName": "testCase2",
        "lastName": "testingCase2",
        "email": 123,
        "tasks": []
    }
    # Use pytest.raises to check if WriteError is raised
    with pytest.raises(WriteError) as e:
        mock_validator.create(new_user)
    assert isinstance(e.value, WriteError)

@pytest.mark.unit
def test_create_user_with_missing_property(mock_validator):
    # Call the create method and check the return value

    # New user with same email as a existing user (email has to be unique)
    new_user = {
        "lastName": "Testingsson",
        "email": "testing@test.com",
        "tasks": []
    }
    # Use pytest.raises to check if WriteError is raised
    with pytest.raises(WriteError) as e:
        mock_validator.create(new_user)
    assert isinstance(e.value, WriteError)
