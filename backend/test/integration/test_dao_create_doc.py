from unittest.mock import patch
import pytest
import pymongo
from src.util.dao import DAO

@pytest.fixture(scope="function")
def dao_task_collection():
    # Initialize the DAO with the test collection name

    with patch('src.util.dao.getValidator') as mock_getValidator:
        mock_getValidator.return_value = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["description"],
                "properties": {
                    "description": {
                        "bsonType": "string",
                        "description": "the description of a todo must be determined",
                        "uniqueItems": True
                    }, 
                    "done": {
                        "bsonType": "bool"
                    }
                }
            }
        }
        dao_instance = DAO('test_collection')
        # dao_instance.collection = mongodb['test_collection']
        yield dao_instance

    # Clean up by dropping the test collection after each test
    dao_instance.drop()

def test_create_document_valid(dao_task_collection):
    # Arrange
    data = {
        "description": "task1",
        "done": True,
    }

    print(dao_task_collection.collection)

    # Act
    dao_task_collection.create(data)

    # Assert
    assert '_id' in dao_task_collection.find({'description': 'task1'})[0]

def test_create_document_missing_reqired_field(dao_task_collection):
    data = {
        "done": True,
    }

    with pytest.raises(pymongo.errors.WriteError):
        dao_task_collection.create(data)

def test_create_document_invalid_field_type(dao_task_collection):
    data = {
        "description": "task1",
        "done": "True",
    }

    with pytest.raises(pymongo.errors.WriteError):
        dao_task_collection.create(data)

def test_create_document_uniqueItems(dao_task_collection):
    data = {
        "description": "task2",
        "done": True,
    }

    dao_task_collection.create(data)

    with pytest.raises(pymongo.errors.WriteError):
        dao_task_collection.create(data)

def test_create_document_contains_extra_data_fields(dao_task_collection):
    data = {
        "description": "task10",
        "done": True,
        "extra": "extra",
    }

    with pytest.raises(pymongo.errors.WriteError):
        dao_task_collection.create(data)
