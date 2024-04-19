import pytest
import pymongo
import os
from dotenv import dotenv_values

@pytest.fixture(scope="session")
def mongodb():
    '''
    This fixture creates a MongoDB client instance and returns it.
    The instance is session-scoped and will be shared by all tests requesting it.
    '''
    LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
    MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)
    client = pymongo.MongoClient(MONGO_URL)
    
    try:
        client.admin.command('ping')
    except Exception as e:
        raise Exception("Could not connect to MongoDB. Please make sure that MongoDB is running.") from e
    
    yield client

    client.close()


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