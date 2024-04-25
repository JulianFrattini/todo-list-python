import pytest
import pymongo
from src.util.dao import DAO
from unittest.mock import patch, MagicMock

@pytest.fixture
def dao():
    with patch("src.util.dao.getValidator") as mockValidator:
        collection_name = 'create_dummy'
        validatorObject = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["name", "value"],
                "properties": {
                    "name": {
                        "bsonType": "string"
                    },
                    "value": {
                        "bsonType": "string"
                    }
                }
            }
        }
        mockValidator.return_value = validatorObject
        dao = DAO(collection_name)
        yield dao
        dao.collection.drop()

def test_create_success(dao):
    data = {"name": "Test Object", "value": "test value"}
    created_object = dao.create(data)
    assert created_object["name"] == data["name"] and created_object["value"] == data["value"]

@pytest.mark.parametrize('name, value', [
        (10, "test"),
        ("test", 10),
        (10, 10),
        (None, "test"),
        ("test", None),
        (None, None)
    ])
def test_failure(dao, name, value):
    data = {"name": name, "value": value}
    with pytest.raises(pymongo.errors.WriteError):
        dao.create(data)
