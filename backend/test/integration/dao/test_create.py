import pytest
import unittest.mock as mock
from unittest.mock import patch

from src.util.dao import DAO

class TestTodo:
    """ * """

    @pytest.fixture
    @patch('src.util.dao.getValidator', autospec=True)
    def sut(self, mocked_validator):

        mocked_validator.return_value = {
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

        sut = DAO(collection_name="todo")

        return sut

        # yield sut

        # Do after yield
        # sut.drop()

    @pytest.mark.integration
    def test_create_valid(self, sut):
        todo_dict = {
            "description": "Testing",
        }

        # with pytest.raises(Exception):
            # sut.create(todo_dict)

        result = sut.create(todo_dict)

        assert isinstance(result, object)



