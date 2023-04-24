import pytest
import unittest.mock as mock
from unittest.mock import patch
from pymongo import MongoClient
from src.util.dao import DAO
# from dao.py
import os
import pymongo
from dotenv import dotenv_values
# create a data access object
from src.util.validators import getValidator
import json
from bson import json_util
from bson.objectid import ObjectId

@pytest.fixture(scope="session")
@patch('pymongo.MongoClient', autospec=True)
@patch('src.util.dao.getValidator', autospec=True)
def sut(mockedValidator, mockedClient):
    # Change the return of mockedValidator

    client = mockedClient('mongodb://localhost:27017/')
    database = client['test_edutask']
    database['user'].drop()  # clean up any existing test data
    # validator = mockedValidator('user')
    mockedValidator = mock.MagicMock()
    obj = {
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
    mockedValidator.getValidator.return_value = obj
    # mockedSut = DAO(collection_name=mockedValidator)
    mockedSut = DAO(collection_name="test")
    database.create_collection('test', validator=mockedValidator)
    yield DAO('test')

@pytest.mark.integration
def test_create(sut):
    # test creating a new document in the test collection
    obj = {'description': 'Test todo item', 'status': 'new'}
    result = sut.DAO(obj)
    assert result == self.to_json(obj)











    # # test creating a document with missing required fields
    # invalid_document = {'status': 'new'}
    # with pytest.raises(Exception):
    #     sut.create(invalid_document)

    # # test creating a document with invalid fields
    # invalid_document = {'description': 'Test todo item', 'status': 'new', 'invalid_field': 'invalid_value'}
    # with pytest.raises(Exception):
    #     sut.create(invalid_document)
