
import pytest
from unittest.mock import patch
from src.util.dao import DAO
import enum
import json
from pymongo.errors import WriteError


class Test_DAO_Create_Get_User_Validator:
    @pytest.fixture
    def sut(self):
        with patch("src.util.dao.getValidator", autospec=True) as mockGetValidators:
            mockGetValidators.return_value = JSONSchema.user.value
            sut = DAO(collection_name="user_test")

            yield sut
            # deleting the recentl created collection "uster_test"
            sut.collection.drop()


    # testCase1 with valid properites, required properites, fullfilled sub-properites .
    @pytest.mark.task3
    def testCase1(self, sut):
        validationResult = sut.create({"firstName":"testCase1", "lastName":"test", "email":"testCase1@gmail.com"})
        assert validationResult == {"_id":validationResult["_id"], "firstName":"testCase1", "lastName":"test", "email":"testCase1@gmail.com"}

    # testCase2 with valid properites, required properites, not fullfilled sub-properites(firstName not type string)
    @pytest.mark.task3
    def testCase2(self, sut):
        with pytest.raises(WriteError):
            sut.create({"firstName":10, "lastName":"test", "email":"testCase2@gmail.com"})
        assert WriteError == WriteError
        
    # testCase3 with valid properites, required properites, not fullfilled sub-properites(lastName not type string)
    @pytest.mark.task3
    def testCase3(self, sut):
        with pytest.raises(WriteError):
            sut.create({"firstName":"testCase3", "lastName":10, "email":"testCase3@gmail.com"})
        assert WriteError == WriteError

    # testCase4 with valid properites, required properites, not fullfilled sub-properites(email not type string)
    @pytest.mark.task3
    def testCase4(self, sut):
        with pytest.raises(WriteError):
            sut.create({"firstName":"testCase4", "lastName":"test", "email":10})
        assert WriteError == WriteError


    # testCase5 with valid properites, required properites, not fullfilled sub-properites (email) duplicated.
    # testing with the same input data as "testCase1"
    @pytest.mark.task3
    def testCase5(self, sut):
        with pytest.raises(WriteError):
            sut.create({"firstName":"testCase1", "lastName":"test", "email":"testCase1@gmail.com"})
        assert WriteError == WriteError

    # testCase6 with valid properites, not all required properites.
    @pytest.mark.task3
    def testCase6(self, sut):
        with pytest.raises(WriteError):
            sut.create({"firstName":"testCase6", "email":"testCase6@gmail.com"})
        assert (WriteError) == WriteError

    # testCase7 with invalid properites.
    @pytest.mark.task3
    def testCase7(self, sut):
        with pytest.raises(WriteError):
            sut.create({"firstName":"testCase7", "tel":"077777777", "lastName":"test", "email":"testCase7@gmail.com"})
        assert (WriteError) == WriteError




class JSONSchema(enum.Enum):
    task = json.loads('''{
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["title", "description"],
            "properties": {
                "title": {
                    "bsonType": "string",
                    "description": "the title of a task must be determined",
                    "uniqueItems": true
                }, 
                "description": {
                    "bsonType": "string",
                    "description": "the description of a task must be determined"
                }, 
                "startdate": {
                    "bsonType": "date"
                }, 
                "duedate": {
                    "bsonType": "date"
                },
                "requires": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "objectId"
                    }
                },
                "categories": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "string"
                    }
                },
                "todos": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "objectId"
                    }
                },
                "video": {
                    "bsonType": "objectId"
                }
            }
        }
    }''')

    todo = json.loads('''{
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["description"],
            "properties": {
                "description": {
                    "bsonType": "string",
                    "description": "the description of a todo must be determined",
                    "uniqueItems": true
                }, 
                "done": {
                    "bsonType": "bool"
                }
            }
        }
    }''')

    user = json.loads('''{
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
                    "uniqueItems": true
                },
                "tasks": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "objectId"
                    }
                }
            }
        }
    }''')

    video = json.loads('''{
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["url"],
            "properties": {
                "url": {
                    "bsonType": "string",
                    "description": "the url of a YouTube video must be determined"
                }
            }
        }
    }''')

