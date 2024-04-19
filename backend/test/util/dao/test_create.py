from dotenv import dotenv_values
import pytest
import unittest.mock as mock
from unittest.mock import patch
import os
import pymongo
import json
from bson.objectid import ObjectId
from src.util.dao import DAO



@pytest.fixture()
def test_db():
    LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
    MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)
    client = pymongo.MongoClient(MONGO_URL)

    db = client.edutask_test

    # "pre-create" the test-collection
    if 'test' not in db.list_collection_names():
        with open('./test/util/dao/test.json', 'r') as f:
            validator = json.load(f)
        db.create_collection('test', validator=validator)
    yield db
    db.drop_collection('test')

@pytest.fixture
def sut(test_db):
    with patch('src.util.dao.pymongo.MongoClient', autospec=True) as mock_pymongo, \
        patch('src.util.dao.getValidator', autospec=True) as mock_getValidator:
        mock_getValidator.return_value = None
        mock_client = mock.MagicMock()

        # replace so that edutask property points to
        # edutask_test database
        type(mock_client).edutask = mock.PropertyMock(return_value=test_db)
        mock_pymongo.return_value = mock_client
    
        sut = DAO(collection_name='test')
        yield sut


# includes only the required property
valid_obj_1 = {
    "email": "test@email.com"
}

# includes one required property and one
# optional
valid_obj_2 = {
    "email": "test@email.com",
    "name": "Test Testsson"
}

# missing required property
invalid_obj_1 = {
    "name": "Test Testsson"
}

# includes one required property and one that
# is not listed in the validator
invalid_obj_2 = {
    "email": "test@email.com",
    "phone": "073-050 34 00"
}

# property is of wrong type
invalid_obj_3 = {
    "email": "test@email.com",
    "name": True
}


@pytest.mark.integration
@pytest.mark.parametrize('new_obj', [
    (valid_obj_1),
    (valid_obj_2),
    ])
def test_create_ok(sut, new_obj):
    """
    Tests valid scenarios when the
    new object is registered to the database,
    that the return object has a objectid
    """
    res = sut.create(new_obj)
    print(res)

    obj_id = ObjectId(res['_id']['$oid'])

    assert isinstance(obj_id, ObjectId)


@pytest.mark.integration
@pytest.mark.parametrize('new_obj', [
    (valid_obj_1),
    (valid_obj_2),
    ])
def test_create_ok2(sut, new_obj):
    """
    Tests valid scenarios when the
    new object is registered to the database.
    Tests that the returned object has same attributes
    and values as the new object
    """
    res = sut.create(new_obj)
    res.pop('_id')
    assert res == new_obj

@pytest.mark.integration
@pytest.mark.parametrize('new_obj', [
    (invalid_obj_1),
    (invalid_obj_2),
    (invalid_obj_3)
    ])
def test_create_invalid_not_ok(sut, new_obj):
    """
    Tests create invalid objects:
    1. missing required property
    2. includes a property that is not listed
    3. includes a property with wrong bson type
    """
    with pytest.raises(pymongo.errors.WriteError):
        sut.create(new_obj)


@pytest.mark.integration
def test_create_dup_not_ok(sut):
    """
    Tests create object with duplicate unique property
    """
    sut.create(valid_obj_2)

    with pytest.raises(pymongo.errors.WriteError):
        sut.create(valid_obj_2)