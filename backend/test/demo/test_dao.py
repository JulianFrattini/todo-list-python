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

        # Yield the DAO to the test
        yield dao

        # Clean up: delete all documents in the collection after each test
        dao.collection.delete_many({})

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

# Exhaustive Testing: Create an object with maximum allowed properties
def test_create_max_allowed_properties(daoSetUp):
    max_data = {"product_name": "ProductM", "price": 999999999.99, "categories": ["Cat1", "Cat2", "Cat3", "Cat4", "Cat5"], "is_active": True}
    result = daoSetUp.create(max_data)
    assert result is not None

# Boundary Value Analysis (BVA): Create an object with minimum required properties
def test_create_min_required_properties(daoSetUp):
    min_data = {"product_name": "ProductN", "price": 0.0, "categories": [], "is_active": False}
    result = daoSetUp.create(min_data)
    assert result is not None

# Equivalence Partitioning (EP): Create an object with some typical properties
def test_create_typical_properties(daoSetUp):
    typical_data = {"product_name": "ProductO", "price": 99.99, "categories": ["Electronics"], "is_active": True}
    result = daoSetUp.create(typical_data)
    assert result is not None
