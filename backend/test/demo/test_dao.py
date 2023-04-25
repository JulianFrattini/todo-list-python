import pytest
from unittest.mock import patch
import pymongo
from src.util.dao import DAO

json_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["product_name", "price", "categories", "is_active"],
        "properties": {
            "product_name": {
                "bsonType": "string",
                "uniqueItems": True
            },
            "price": {
                "bsonType": "double"
            },
            "categories": {
                "bsonType": "array",
                "items": {
                    "bsonType": "string"
                }
            },
            "is_active": {
                "bsonType": "bool",
            }
        }
    }
}

@pytest.fixture()
def daoSetUp():
    with patch("src.util.dao.getValidator") as mock_get_validator:
        mock_get_validator.return_value = json_validator
        dao = DAO("test_unauthenticated")
        yield dao

def test_create_valid_object(daoSetUp):
    valid_data = {"product_name": "ProductA", "price": 25.99, "categories": ["Electronics", "Gadgets"], "is_active": True}
    result = daoSetUp.create(valid_data)
    assert result is not None

def test_create_missing_required_properties(daoSetUp):
    invalid_data = {"product_name": "ProductB", "categories": ["Electronics", "Gadgets"]}
    with pytest.raises(Exception):
        daoSetUp.create(invalid_data)

def test_create_incorrect_data_types(daoSetUp):
    invalid_data = {"product_name": "ProductC", "price": "100.0", "categories": ["Electronics", "Gadgets"], "is_active": "True"}
    with pytest.raises(Exception):
        daoSetUp.create(invalid_data)

def test_create_unique_ids(daoSetUp):
    data1 = {"product_name": "ProductD", "price": 45.0, "categories": ["Electronics", "Gadgets"], "is_active": True}
    data2 = {"product_name": "ProductE", "price": 55.0, "categories": ["Electronics", "Gadgets"], "is_active": False}
    result1 = daoSetUp.create(data1)
    result2 = daoSetUp.create(data2)
    assert result1["_id"] is not None
    assert result2["_id"] is not None
    assert result1["_id"] != result2["_id"]

def test_create_no_valid_db_connection(daoSetUp):
    test_data = {"product_name": "ProductF", "price": 75.99, "categories": ["Electronics", "Gadgets"], "is_active": True}
    with patch("src.util.dao.MongoClient") as mock_client:
        mock_client.side_effect = Exception("Database connection error")
        with pytest.raises(Exception, match="Database connection error"):
            daoSetUp.create(test_data)


