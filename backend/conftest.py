import pytest
import pymongo

@pytest.fixture(scope="session")
def mongodb():
    '''
    This fixture creates a MongoDB client instance and returns it.
    The instance is session-scoped and will be shared by all tests requesting it.
    '''
    client = pymongo.MongoClient('localhost', 27017, directConnection=True, replicaset="rs0")
    try:
        client.admin.command('ping')
    except Exception as e:
        raise Exception("Could not connect to MongoDB. Please make sure that MongoDB is running.") from e
    return client

@pytest.fixture
def rollback_session(mongodb):
    '''
    This fixture creates a session that will be rolled back after the test function.
    Meaning that any changes made to the database during the test will be undone.
    The fixture value must be provided as a session argument to the database operations.
    '''
    session = mongodb.start_session()
    session.start_transaction()
    try:
        yield session
    finally:
        session.abort_transaction()