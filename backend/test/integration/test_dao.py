import pytest
from unittest.mock import patch
from pymongo.errors import WriteError
from src.util.dao import DAO


validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title"],
        "properties": {
            "title": {
                "bsonType": "string",
                "description": "the title of a task must be determined",
                "uniqueItems": True
            },
        }
    }
}


@pytest.fixture
def sut():
    with patch('src.util.dao.getValidator', autospec=True) as mockedValidator:
        mockedValidator.return_value = validator
        sut = DAO("test")
        yield sut
        sut.drop()

@pytest.mark.integration
def test_missing_property(sut):
    with pytest.raises(WriteError):
        sut.create({"title": 142})

@pytest.mark.integration
def test_not_bson_compile(sut):
    with pytest.raises(WriteError):
        sut.create({"title": 142, "description": "TestOne"})
        sut.create({"title": 142, "description": "TestOne"})

@pytest.mark.integration
def test_not_unique(sut):
    with pytest.raises(WriteError):
        sut.create({"title": 142, "description": "TestOne"})
        sut.create({"title": 142, "description": "TestOne"})

@pytest.mark.integration
def test_create_valid_data(sut):
    result = sut.create({"title": "testOne", "description": "TestOne"})
    assert isinstance(result, object)
    sut.drop()