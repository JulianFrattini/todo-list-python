from unittest.mock import patch
import unittest.mock as mock
import pytest
import pymongo.errors
import sys
from src.util.dao import DAO


@pytest.fixture
def sut():
    with patch('src.util.dao.getValidator', autospec=True) as mock_get_validator:
        #mock_get_validator = mock.MagicMock()
        # Set the return value of the mocked getValidator function
        validator = {
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

        #mock_get_validator.getValidator.return_value = validator
        mock_get_validator.return_value = validator

        # Create and return the DAO object
        name = "test_todo"
        sut = DAO(collection_name=name)
        yield sut
        sut.drop()

# All flags are valid
@pytest.mark.integration
def test_create_1(sut):
    task = {"description":"test task one.", "done": False}
    result = sut.create(task)
    assert result['description'] == "test task one."
    assert result['done'] == False

# The unique flag is violated
@pytest.mark.integration
def test_create_2(sut):
    task = {"description":"test task one.", "done": True}
    task2 = {"description":"test task one.", "done": True}
    sut.create(task)

    with pytest.raises(pymongo.errors.WriteError) as exc_info:
        sut.create(task2)
    assert "Document failed validation" in str(exc_info.value)


# At least one property does not comply with bson
@pytest.mark.integration
def test_create_3(sut):
    task = {"description":"test task one.", "done": 1}

    with pytest.raises(pymongo.errors.WriteError) as exc_info:
        sut.create(task)
    assert "Document failed validation" in str(exc_info.value)

# At least one of the required properties is missing
@pytest.mark.integration
def test_create_4(sut):
    task = {"done": True}
    #task2 = {"description":"test task one.", "done": True}
    #sut.create(task)

    with pytest.raises(pymongo.errors.WriteError) as exc_info:
        sut.create(task)
    assert "Document failed validation" in str(exc_info.value)
