import pytest
from unittest.mock import patch
from src.util.dao import DAO
from pymongo.errors import WriteError

@pytest.fixture
def sut():
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
    with patch('src.util.dao.getValidator', autospec=True) as mocked_validator, patch('src.util.dao.DAO.to_json', autospec=True) as mocked_to_json:
        mocked_to_json.return_value = True
        mocked_validator.return_value = validator
        dao = DAO(collection_name="todo")   
        yield dao
        dao.drop()
    
    # clean-up

@pytest.mark.dao
@pytest.mark.parametrize('input, expected', [({}, WriteError)])
def test_description_not_defined(input, expected, sut):
    with pytest.raises(expected):
        sut.create(input)

@pytest.mark.dao
@pytest.mark.parametrize('input, expected', [({'description': 'test'}, WriteError)])
def test_description_not_unique(input, expected, sut):
    sut.create(input)
    with pytest.raises(expected):
        sut.create(input)

@pytest.mark.dao
@pytest.mark.parametrize('input, expected', [({'description': 42}, WriteError)])
def test_description_not_correct_type(input, expected, sut):
    with pytest.raises(expected):
        sut.create(input)

@pytest.mark.dao
@pytest.mark.parametrize('input, expected', [({'description': 'test'}, True)])
def test_description_no_done(input, expected, sut):
    assert sut.create(input) == expected

@pytest.mark.dao
@pytest.mark.parametrize('input, expected', [({'description': 'test', 'done': True}, True)])
def test_description_with_done(input, expected, sut):
    assert sut.create(input) == expected
