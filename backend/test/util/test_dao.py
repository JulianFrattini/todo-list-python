import pytest
from unittest.mock import patch, MagicMock
from pymongo import MongoClient
from pymongo.errors import WriteError
import json

from src.util.dao import DAO

class TestCreate:
    """
    A test suite for the create() method of the DAO class.
    """

    @pytest.fixture
    def sut(self):
        """
        System Under Test (SUT).

        Returns: DAO: An instance of the DAO class with mocked getValidation.
        """

        test_json = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["firstName", "lastName", "email"],
                "properties": {
                    "firstName": {
                        "bsonType": "string",
                        "description": "the first name of a user must be determined"
                    }, 
                    "lastName": {
                        "bsonType": "string",
                        "description": "the last name of a user must be determined"
                    },
                    "email": {
                        "bsonType": "string",
                        "description": "the email address of a user must be determined",
                        "uniqueItems": True
                    },
                    "tasks": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "objectId"
                        }
                    }
                }
            }
        }

        with patch('src.util.dao.getValidator', autospec=True) as mockedgetValidator:
            mockedgetValidator.return_value = test_json

            sut = DAO("test")
            
            yield sut

        client = MongoClient('localhost', 27017)
        db = client['edutask']
        db['test'].drop()
    
    # @pytest.mark.dao
    # def test_create(self, sut):
    #     """
    #     Test case for the create method of the DAO class.
    #     This is a TEST test case to ensure that it works.

    #     Parameters: sut (DAO): The System Under Test (SUT) instance.

    #     Assertion: Asserts that the result from the create() method is true
    #     """

    #     data = {
    #         "firstName": "Joe",
    #         "lastName": "Bloggs",
    #         "email": "joe.bloggs@test.com"
    #     }

    #     result = sut.create(data)

    #     print(result)

    #     assert result

    @pytest.mark.dao
    def test_create_1_id(self, sut):
        """
        Test case 1: Required properties, BSON compliance, and flagged with uniqueItems.
        Required Properties: TRUE
        Comply with BSON: TRUE
        Flagged with uniqueItems: TRUE
        Outcome: JSON Object returned with data: dict and _id.

        Testing for an _id attribute
        """

        data = {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "test@test.com"
        }
    
        result = sut.create(data)

        assert "_id" in result

    @pytest.mark.dao
    def test_create_1_json(self, sut):
        """
        Test case 1: Required properties, BSON compliance, and flagged with uniqueItems.
        Required Properties: TRUE
        Comply with BSON: TRUE
        Flagged with uniqueItems: TRUE
        Outcome: JSON Object returned with data: dict and _id.

        Testing for a JSON Object (Dict in Python)
        """

        data = {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "test@test.com"
        }

        result = sut.create(data)

        # assert isinstance(result, dict)

        try:
            json_object = json.loads(json.dumps(result))
            assert isinstance(json_object, dict) or isinstance(json_object, list)
            # If it's a JSON object (dictionary or list), the test passes
        except json.JSONDecodeError:
            assert False  # If parsing fails, the return value is not JSON

    @pytest.mark.dao
    def test_create_2(self, sut):
        """
        Test case 2: Required properties, BSON compliance, but not flagged with uniqueItems.
        Required Properties: TRUE
        Comply with BSON: TRUE
        Flagged with uniqueItems: FALSE
        Outcome: WriteError.
        """

        data = {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "test@test.com"
        }

        sut.create(data)

        newData = {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "test@test.com"
        }

        with pytest.raises(WriteError):
            sut.create(newData)

    @pytest.mark.dao
    def test_create_3(self, sut):
        """
        Test case 3: Required properties, not BSON compliant, and not flagged with uniqueItems.
        Required Properties: TRUE
        Comply with BSON: FALSE
        Flagged with uniqueItems: FALSE
        Outcome: WriteError.
        """
        data = {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "test@test.com"
        }

        sut.create(data)

        newData = {
            "firstName": "Jonathan",
            "lastName": (1, 2, 3),
            "email": "test@test.com"
        }

        with pytest.raises(WriteError):
            sut.create(newData)

    @pytest.mark.dao
    def test_create_4(self, sut):
        """
        Test case 4: Required properties, not BSON compliant, but flagged with uniqueItems.
        Required Properties: TRUE
        Comply with BSON: FALSE
        Flagged with uniqueItems: TRUE
        Outcome: WriteError.
        """

        data = {
            "firstName": "Jonathan",
            "lastName": (1, 2, 3),
            "email": "test@test.com"
        }

        with pytest.raises(WriteError):
            sut.create(data)

    @pytest.mark.dao
    def test_create_5(self, sut):
        """
        Test case 5: No required properties, BSON compliant, and flagged with uniqueItems.
        Required Properties: FALSE
        Comply with BSON: TRUE
        Flagged with uniqueItems: TRUE
        Outcome: WriteError.
        """

        data = {
            "firstName": "Joe",
            "email": "test@test.com"
        }

        with pytest.raises(WriteError):
            sut.create(data)

    @pytest.mark.dao
    def test_create_6(self, sut):
        """
        Test case 6: No required properties, BSON compliant, but not flagged with uniqueItems.
        Required Properties: FALSE
        Comply with BSON: TRUE
        Flagged with uniqueItems: FALSE
        Outcome: WriteError.
        """

        data = {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "test@test.com"
        }

        sut.create(data)

        newData = {
            "firstName": "Joe",
            "email": "test@test.com"
        }

        with pytest.raises(WriteError):
            sut.create(newData)

    @pytest.mark.dao
    def test_create_7(self, sut):
        """
        Test case 7: No required properties, not BSON compliant, but flagged with uniqueItems.
        Required Properties: FALSE
        Comply with BSON: FALSE
        Flagged with uniqueItems: TRUE
        Outcome: WriteError.
        """

        data = {
            "firstName": (1,2,3),
            "email": "test@test.com"
        }

        with pytest.raises(WriteError):
            sut.create(data)

    @pytest.mark.dao
    def test_create_8(self, sut):
        """
        Test case 8: No required properties, not BSON compliant, and not flagged with uniqueItems.
        Required Properties: FALSE
        Comply with BSON: FALSE
        Flagged with uniqueItems: FALSE
        Outcome: WriteError.
        """

        data = {
            "firstName": "Joe",
            "lastName": "Bloggs",
            "email": "test@test.com"
        }

        sut.create(data)

        newData = {
            "firstName": (1,2,3),
            "email": "test@test.com"
        }

        with pytest.raises(WriteError):
            sut.create(newData)
