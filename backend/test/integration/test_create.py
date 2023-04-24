import os
import pytest
from unittest.mock import patch, Mock
import unittest.mock as mock
from src.util.dao import DAO
from pymongo import MongoClient
from dotenv import dotenv_values

@pytest.fixture(scope='session')
def mongo_client():
    LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
    MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)
    client = MongoClient(MONGO_URL)
    yield client
    client.drop_database('edutask_test')
    client.close()

@pytest.fixture(scope='session')
def mongo_db(mongo_client):
    db = mongo_client.edutask_test
    yield db
    db.drop_collection('test_collection')

@pytest.fixture(scope="module")
def dao(mongo_db):
    with patch('src.util.dao.getValidator') as mock_getValidator:
        mock_getValidator.return_value = {"$jsonSchema": {"bsonType": "object"}}
        collection_name = 'test_collection'
        dao = DAO(collection_name, mongo_db)
        yield dao

def test_create_successful(dao):
    data = {'name': 'John Doe', 'age': 30, 'is_active': True}
    obj = dao.create(data)
    assert '_id' in obj

def test_create_noncompliant_data(dao):
    data = {'name': 'John Doe', 'age': 'thirty', 'is_active': True}
    with pytest.raises(WriteError):
        dao.create(data)

def test_create_invalid_bson_data_type(dao):
    data = {'name': {'first': 'John', 'last': 'Doe'}, 'age': 30, 'is_active': True}
    with pytest.raises(WriteError):
        dao.create(data)

def test_create_unique_items_constraint(dao):
    data1 = {'name': 'John Doe', 'hobbies': ['reading', 'swimming']}
    data2 = {'name': 'Jane Doe', 'hobbies': ['swimming']}
    dao.create(data1)
    with pytest.raises(WriteError):
        dao.create(data2)
