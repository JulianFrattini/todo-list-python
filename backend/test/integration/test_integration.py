import pytest
import unittest.mock as mock
from unittest.mock import patch
from src.util.dao import DAO
import pymongo.errors
import json
import os


# Set temporary validator to return same rules as the validator 'user'
@pytest.fixture
@pytest.mark.integration
def set_validator_user_sut():

    with open('./src/static/validators/user.json', 'r') as f:
        validator_data = json.load(f)

    test_user_rules = './src/static/validators/test_user_collection.json'
    with open(test_user_rules, 'w') as new_file:
        json.dump(validator_data, new_file)

    yield test_user_rules

    try:
        os.remove(test_user_rules)
    except OSError:
        pass  # Ignore if the file doesn't exist or cannot be removed


@pytest.fixture
@pytest.mark.integration
def dao(set_validator_user_sut):
    dao_instance = DAO('test_user_collection')

    yield dao_instance

    dao_instance.drop() # Drop the collection after the the tests is done


@pytest.mark.integration
def test_dao_create_valid_dict(dao):
# Test DAO.create with valid data
    data_valid = {
        "firstName": "Firstname",
        "lastName": "Lastname",
        "email": "firstname.lastname@test.com"
    }

    result = dao.create(data_valid)

    assert isinstance(result, dict)
    assert "firstName" in result
    assert "lastName" in result
    assert "email" in result
    assert "_id" in result

@pytest.mark.integration
# Test DAO.create with invalid data
def test_dao_create_invalid_dict(dao):

    data_invalid = {
        "firstName": "Firstname",
        "email": "firstname.lastname@test.com"
    }

    with pytest.raises(pymongo.errors.WriteError):
        dao.create(data_invalid)

@pytest.mark.integration
# Test DAO.create with empty data
def test_dao_create_empty_dict(dao):

    data_invalid = {}

    with pytest.raises(pymongo.errors.WriteError):
        dao.create(data_invalid)
