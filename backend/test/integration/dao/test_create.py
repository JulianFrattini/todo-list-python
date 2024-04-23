import pytest
import unittest.mock as mock
from unittest.mock import patch

from src.util.dao import DAO

class TestTodo:
    """ Test cases for creating todo documents. """

    @pytest.fixture
    def sut(self):
        with patch('src.util.dao.getValidator', autospec=True) as mocked_validator:

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

            sut = DAO(collection_name="test_todo")

            yield sut

            # Do after yield
            sut.drop()

    @pytest.mark.integration
    def test_create_valid(self, sut):
        """ Test that creating a valid todo returns the created MongoDB document. """

        todo_dict = {
            "description": "Testing",
        }

        result = sut.create(todo_dict)

        assert todo_dict["description"] == result["description"]

    @pytest.mark.integration
    def test_create_invalid_missing_property(self, sut):
        """ Test that creating a todo without a required property raises a WriteError. """

        todo_dict = {
            "desc": "Testing",
        }

        with pytest.raises(Exception):
            sut.create(todo_dict)

    @pytest.mark.integration
    def test_create_invalid_wrong_data_type(self, sut):
        """ Test that creating a todo with the wrong data type for a property raises a WriteError. """

        todo_dict = {
            "description": 1,
        }

        with pytest.raises(Exception):
            sut.create(todo_dict)

    # FAILS
    @pytest.mark.integration
    def test_create_valid_not_unique(self, sut):
        """ Test that creating two valid todo:s with the same descriptions raises a WriteError. """

        todo_dict = {
            "description": "Testing2",
        }

        sut.create(todo_dict)

        with pytest.raises(Exception):
            sut.create(todo_dict)

