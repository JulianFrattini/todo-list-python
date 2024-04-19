import pytest
from unittest.mock import patch
from pymongo.errors import WriteError
import json

from src.util.dao import DAO

class TestDAOCreateMethod:
    @pytest.fixture
    def dao_instance(self):
       
        validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["firstName", "lastName", "email"],
                "properties": {
                    "firstName": {"bsonType": "string"},
                    "lastName": {"bsonType": "string"},
                    "email": {"bsonType": "string", "uniqueItems": True},
                    "tasks": {"bsonType": "array", "items": {"bsonType": "objectId"}}
                }
            }
        }
        with patch('src.util.dao.getValidator', return_value=validator):
            dao = DAO("test")
            yield dao
            dao.collection.drop()


#Test ID:1
    def test_valid_data_insertion(self, dao_instance):
       
        data = {"firstName": "John", "lastName": "Doe", "email": "john.doe@example.com"}
        result = dao_instance.create(data)
        assert '_id' in result, "Document should have an '_id' after insertion."


#Test ID:2
    def test_invalid_data_insertion(self, dao_instance):
        invalid_data = {"firstName": "John", "lastName": 12345, "email": "John.doe@example.com"}
        with pytest.raises(WriteError):
            dao_instance.create(invalid_data)

#Test ID:3
    def test_unique_item_constraint(self, dao_instance):
        valid_data = {"firstName": "Erik", "lastName": "Smith", "email": "erik.smith@example.com"}
        dao_instance.create(valid_data)  
        with pytest.raises(WriteError):
            dao_instance.create(valid_data)  

#Test ID:4
    def test_various_bson_types(self, dao_instance):
        data = {
            "firstName": "Bob",
            "lastName": "Belly",
            "email": "bob@example.com",
            "tasks": [json.dumps({"task_id": "123abc"})]  
        }
        result = dao_instance.create(data)
        assert '_id' in result, "Should handle BSON types correctly."


#Test ID:5
    def test_missing_required_fields(self, dao_instance):
        incomplete_data = {"firstName": "Eve"}  
        with pytest.raises(WriteError):
            dao_instance.create(incomplete_data)

