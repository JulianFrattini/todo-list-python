import pymongo.errors
import pytest
import pymongo
import unittest.mock as mock
from unittest.mock import patch

from src.util.dao import DAO

# the test values for the collection validator, mocking getValidator()
test_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["firstName", "lastName", "email", "paying_user"],
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
            },
            "paying_user": {
                "bsonType": "bool",
                "description": "the user has a paying subscription"
            }
        }
    }
}



# (2) A pytest fixture allowing interaction with the database without disturbing production code or data
@pytest.fixture
def sut():
    with patch ('src.util.dao.getValidator', autospec=True) as mockedValidator:
        mockedValidator.return_value = test_validator
        sut = DAO("test_collection")
        
        sut.collection.create_index([('email', pymongo.ASCENDING)], unique=True)

        yield sut
        sut.drop()

# (1) all required propertie is false
@pytest.mark.integration
def test_create_not_contain_required_properties_firstname(sut):
    # Arrange
    data = {
        'lastName': 'Ek',
        'email': 'bo.ek@mail.com',
        'paying_user': True
    }

    # Assert
    with pytest.raises(pymongo.errors.WriteError): 
        sut.create(data) #Act

@pytest.mark.integration
def test_create_not_contain_required_properties_lastname(sut):
    # Arrange
    data = {
        'firstName': 'Bo',
        'email': 'bo.ek@mail.com',
        'paying_user': True

    }

    # Assert
    with pytest.raises(pymongo.errors.WriteError): 
        sut.create(data) #Act

@pytest.mark.integration
def test_create_not_contain_required_properties_email(sut):
    # Arrange
    data = {
        'firstName': 'Bo',
        'lastName': 'Ek',
        'paying_user': True
    }

    # Assert
    with pytest.raises(pymongo.errors.WriteError): 
        sut.create(data) #Act

@pytest.mark.integration
def test_create_not_contain_required_properties_paying_user(sut):
    # Arrange
    data = {
        'firstName': 'Bo',
        'lastName': 'Ek',
        'email': 'bo.ek@mail.com'
    }

    # Assert
    with pytest.raises(pymongo.errors.WriteError): 
        sut.create(data) #Act


@pytest.mark.integration
def test_create_not_correct_data_type_constraint_firstName(sut):
    # Arrange
    data = {
        'firstName': 123,
        'lastName': 'Ek',
        'email': 'bo.ek@mail.com',
        'paying_user': True
    }

    # Assert
    with pytest.raises(pymongo.errors.WriteError): 
        sut.create(data) #Act

@pytest.mark.integration
def test_create_not_correct_data_type_constraint_lastName(sut):
    # Arrange
    data = {
        'firstName': 'Bo',
        'lastName': 123,
        'email': 'bo.ek@mail.com',
        'paying_user': True
    }

    # Assert
    with pytest.raises(pymongo.errors.WriteError): 
        sut.create(data) #Act

@pytest.mark.integration
def test_create_not_correct_data_type_constraint_email(sut):
    # Arrange
    data = {
        'firstName': 'Bo',
        'lastName': 'Ek',
        'email': 123,
        'paying_user': True
    }

    # Assert
    with pytest.raises(pymongo.errors.WriteError): 
        sut.create(data) #Act

@pytest.mark.integration
def test_create_not_correct_data_type_constraint_paying_user(sut):
    # Arrange
    data = {
        'firstName': 'Bo',
        'lastName': 'Ek',
        'email': 'bo.ek@mail.com',
        'paying_user': 'yes'
    }

    # Assert
    with pytest.raises(pymongo.errors.WriteError): 
        sut.create(data) #Act


@pytest.mark.integration
def test_create_no_unique_property_values(sut):
    user1 = {
        'firstName': 'Bo',
        'lastName': 'Ek',
        'email': 'bo.ek@mail.com',
        'paying_user': True
    }

    sut.create(user1)

    user2 = {
        'firstName': 'Bosse',
        'lastName': 'Ekman',
        'email': 'bo.ek@mail.com',
        'paying_user': True
    }
    with pytest.raises(pymongo.errors.WriteError): 
        sut.create(user2) #Act

@pytest.mark.integration
def test_create_success(sut):
    # Arrange
    data = {
        'firstName': 'Bo',
        'lastName': 'Ek',
        'email': 'bo.ek@mail.com',
        'paying_user': True
    }

    # Act
    sut.create(data)
    find_dict_data = sut.find(data)

    # Assert
    assert find_dict_data[0]['email'] == data['email']