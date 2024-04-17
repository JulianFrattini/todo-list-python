import pytest
from src.util.dao import DAO
from bson.objectid import ObjectId

@pytest.fixture
def dao():
    dao = DAO('todo')
    yield dao
    dao.drop()

# Type found in: src/static/validators/todo.json
valid_data = {
    "description": "Hello World!",
}
invalid_data = {
    "description": 5, # not a string
}
missing_required_data = {
    "desc": "Hello World!", # missing required property 'description'
}

@pytest.mark.integration
def test_create_missing_required_properties(dao):
    with pytest.raises(Exception):
        dao.create(missing_required_data)

@pytest.mark.integration
def test_create_valid_document(dao):
    result = dao.create(valid_data)
    id = result['_id']['$oid']
    document = dao.findOne(id)
    del document['_id']
    assert document == valid_data

@pytest.mark.integration
def test_create_invalid_document(dao):
    with pytest.raises(Exception):
        dao.create(invalid_data)

@pytest.mark.integration
def test_create_duplicate_unique_fields(dao):
    dao.create(valid_data)
    with pytest.raises(Exception):
        dao.create(valid_data)
