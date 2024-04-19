import pytest

@pytest.mark.admin
def test_mongodb_fixture(mongodb):
    '''
    This test checks if the MongoDB fixture is working by pinging the MongoDB server.
    '''
    assert mongodb.admin.command("ping")["ok"] > 0

@pytest.mark.admin
def test_rollback_session(mongodb, rollback_session):
    '''
    This test checks if the rollback session fixture is working by inserting a document
    into the database and then rolling back the transaction.
    (Check the MongoDB Compass or use mongosh to see if the document is not there after the test).
    '''
    mongodb.test.tests.insert_one(
        {
            "_id": "test_document",
            "description": "If this still exists after the test, the rollback session is not working.",
        },
        session=rollback_session,
    )
    assert (
        mongodb.test.tests.find_one(
            {"_id": "test_document"}, session=rollback_session
        )
        != None
)
