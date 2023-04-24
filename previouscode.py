import pytest
from unittest.mock import patch
from pymongo import MongoClient
from src.util.dao import DAO
from src.util.validators import getValidator

@pytest.fixture
@patch('src.util.dao.getValidator', autospec=True)
@patch('pymongo.MongoClient', autospec=True)
def sut(mockedValidator, mockedClient):
    # Change the return of mockedValidator
    mockedValidator.return_value = {
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

    client = mockedClient('mongodb://localhost:27017/')
    database = client['test_edutask']
    database['user'].drop()  # clean up any existing test data
    # validator = mockedValidator('user')
    mockedSut = getValidator(collection_name=mockedValidator)
    database.create_collection('user', validator=mockedValidator)
    yield DAO('user')

@pytest.mark.integration
def test_create(sut):
    # test creating a new document in the test collection
    obj = {'description': 'Test todo item', 'status': 'new'}
    dao = DAO(sut)
    result = dao.create(document)
    assert result == self.to_json(obj)











    # # test creating a document with missing required fields
    # invalid_document = {'status': 'new'}
    # with pytest.raises(Exception):
    #     sut.create(invalid_document)

    # # test creating a document with invalid fields
    # invalid_document = {'description': 'Test todo item', 'status': 'new', 'invalid_field': 'invalid_value'}
    # with pytest.raises(Exception):
    #     sut.create(invalid_document)
