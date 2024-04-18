import pytest
from src.util.dao import DAO
import pymongo.errors
import json
import os
from pymongo.errors import WriteError


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
def test_dao_create_invalid_dict(dao):
    """
    TestCase 1:
        data = invalid_dict
    """
    data_invalid = {}

    with pytest.raises(pymongo.errors.WriteError):
        dao.create(data_invalid)

@pytest.mark.integration
def test_dao_create_valid(dao):
    """
    TestCase 2:
        data = valid data
        prop_is_BSON_type = True
        unique_property = True
    """

    # data
    data_valid = {
        "firstName": "Firstname",
        "lastName": "Lastname",
        "email": "firstname.lastname@test.com"
    }

    result = dao.create(data_valid)

    # unique property email
    unique_property = dao.find({"email": "firstname.lastname@test.com"})

    # BSON_type
    BSON_firstName = isinstance(data_valid["firstName"], str)
    BSON_lastName = isinstance(data_valid["lastName"], str)
    BSON_email = isinstance(data_valid["email"], str)

    # assert expected outcome
    assert isinstance(result, dict)
    assert "firstName" in result
    assert "lastName" in result
    assert "email" in result
    assert "_id" in result
    assert len(unique_property) == 1
    assert BSON_firstName == True
    assert BSON_lastName == True
    assert BSON_email == True

@pytest.mark.integration
def test_dao_create_not_unique_prop(dao):
    """
    TestCase 3:
        data = valid data
        unique_property = False
    """

    # data
    data_valid1 = {
        "firstName": "Firstname",
        "lastName": "Lastname",
        "email": "firstname.lastname@test.com"
    }
    result1 = dao.create(data_valid1)

    # unique_property = False
    data_valid2 = {
        "firstName": "Firstname",
        "lastName": "Lastname",
        "email": "firstname.lastname@test.com"
    }

    result2 = dao.create(data_valid2)

    # assert expected outcome
    assert isinstance(result1, dict)
    assert "firstName" in result1
    assert "lastName" in result1
    assert "email" in result1
    assert "_id" in result1
    with pytest.raises(WriteError):
        dao.create(result2)

@pytest.mark.integration
def test_dao_create_not_BSON(dao):
    """
    TestCase 4:
        prop_is_BSON_type = False
    """

    # data
    data = {
        "firstName": "Firstname",
        "lastName": 12345,
        "email": "firstname.lastname@test.com"
    }

    # assert expected outcome
    with pytest.raises(WriteError):
        dao.create(data)
