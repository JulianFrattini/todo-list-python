import pytest
from src.util.dao import DAO
from unittest.mock import patch
from pymongo.errors import WriteError

@pytest.fixture
def mock_validator():
    # Define the mocked validator
            return {"user": {
                "validator": {
                    "$jsonSchema": {
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
            }
            }

@pytest.fixture
def dao(mock_validator):
    # Patch the getValidator method and return the DAO object
    with patch('src.util.dao.getValidator') as mockedGetValidator:
        mockedGetValidator.return_value = mock_validator
        yield DAO('user')
     

def test_create_user_with_valid_email(dao):
    # Call the create method and check the return value
    new_user = {
        "firstName": "Help",
        "lastName": "Helping",
        "email": "help@test1.com",
        "tasks": []
    }
    result = dao.create(new_user)
    dao.delete(result['_id']['$oid'])
    assert result['firstName'] == new_user['firstName']
    assert result['lastName'] == new_user['lastName']
    assert result['email'] == new_user['email']

def test_create_user_with_invalid_email_type(dao):
    # Call the create method and check the return value
    new_user = {
        "firstName": "Help",
        "lastName": "Helping",
        "email": 123,
        "tasks": []
    }
    # Use pytest.raises to check if WriteError is raised
    with pytest.raises(WriteError):
            dao.create(new_user)

def test_create_user_with_same_email(dao):
    # Call the create method and check the return value

    # New user with same email as a existing user (email has to be unique)
    new_user = {
        "firstName": "Test",
        "lastName": "Testingsson",
        "email": "testing@test.com",
        "tasks": []
    }
    # Use pytest.raises to check if WriteError is raised
    with pytest.raises(WriteError):
        result = dao.create(new_user)
        dao.delete(result['_id']['$oid'])

    
def test_create_user_with_missing_property(dao):
    # Call the create method and check the return value

    # New user with same email as a existing user (email has to be unique)
    new_user = {
        "lastName": "Testingsson",
        "email": "testing@test.com",
        "tasks": []
    }
    # Use pytest.raises to check if WriteError is raised
    with pytest.raises(WriteError):
        result = dao.create(new_user)
        dao.delete(result['_id']['$oid'])

    