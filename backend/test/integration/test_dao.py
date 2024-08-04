import pytest
from unittest.mock import patch
from src.util.dao import DAO
from pymongo.errors import WriteError

#Json validator based on the "todo" entity of the data model
json_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["description", "done"],
        "properties": {
            "description": {
                "bsonType": "string"
            },
            "done": {
                "bsonType": "bool"
            }
        }
    }
}


@pytest.fixture
def sut():
    with patch("src.util.dao.getValidator", autospec=True) as mockedgetvalidator:
        mockedgetvalidator.return_value = json_validator
        sut = DAO(collection_name="test")
    
    yield sut
    sut.collection.drop()


# Test valid data insertion
def test_valid_data(sut):
    result = sut.create({"description": "test", "done": True})
    assert result["description"] == "test"
    assert result["done"] == True

# Test where description is not a string
def test_description_not_string(sut):
    with pytest.raises(Exception):
        sut.create({"description": 123, "done": False})


# Test where done is not a boolean
def test_done_not_boolean(sut):
    with pytest.raises(Exception):
        sut.create({"description": "test", "done": 123})

# Test where description is missing
def test_missing_description(sut):
    with pytest.raises(WriteError):
        sut.create({"done": True})

# Test where done is missing
def test_missing_done(sut):
    with pytest.raises(WriteError):
        sut.create({"description": "test"})

# Test where both description and done are missing
def test_missing_both(sut):
    with pytest.raises(WriteError):
        sut.create({})