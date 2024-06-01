import pytest
import unittest.mock as mock
from pymongo import MongoClient, errors
from src.util.dao import DAO, getValidator

test_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "email"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "string, required",
                # unik
                "uniqueItems": True
            },
            "email": {
                "bsonType": "string",
                "description": "string, required"
            }
        }
    }
}

@pytest.fixture(scope="session")
def db_connection():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['test_database']
    yield db
    client.drop_database('test_database')

@pytest.fixture()
def sut(db_connection):
    collection_name = "test_collection"
    collection = db_connection[collection_name]
    
    collection.create_index("name", unique=True)

    with mock.patch("src.util.dao.getValidator") as mock_validator:
        mock_validator.return_value = test_validator
        dao = DAO(collection_name)
        return dao


# VALID USER, SUCCESSFUL CREATION
def test_create_valid_data(sut):
    data = {"name": "Casso", "email": "Casso@gmail.com"}
    result = sut.create(data)
    assert result is not None
    #assert result['name'] == 'Casso'

# VALID USER, DUPLICATE NAME
def test_create_duplicate_name(sut):
    data = {"name": "Casso", "email": "Casso@gmail.com"}
    result = sut.create(data)
    assert result is not None
    with pytest.raises(errors.WriteError):
        sut.create(data)

# INVALID (MISSING EMAIL), UNSUCCESSFUL CREATION
def test_create_missing_email(sut):
    data = {"name": "Casso"}
    with pytest.raises(errors.WriteError):
        sut.create(data)

# INVALID (WRONG BSON TYPE), UNSUCCESSFUL CREATION
def test_create_wrong_type(sut):
    data = {"name": "Casso", "email": 123}
    with pytest.raises(errors.WriteError):
        sut.create(data)


if __name__ == "__main__":
    pytest.main()
