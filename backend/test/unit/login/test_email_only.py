import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController

@pytest.mark.unit
def test_get_user_matching_single():
    """ Test that get_user_by_email returns a single match. """

    mocked_dao = mock.MagicMock()
    mocked_dao.find.return_value = [
        {
            "_id": {
                "$oid": "6615a3bca483a805520a9b44"
            },
            "email": "micke@bth.se",
            "firstName": "mikael",
            "lastName": "svensson"
        }
    ]

    sut = UserController(dao=mocked_dao)

    # email param doesn't matter since dao.find is mocked
    result = sut.get_user_by_email("micke@bth.se")
    assert result == mocked_dao.find.return_value[0]

@pytest.mark.unit
def test_get_user_matching_multiple():
    """ Test that get_user_by_email returns the first of multiple matches. """

    mocked_dao = mock.MagicMock()
    mocked_dao.find.return_value = [
        {
            "_id": {
                "$oid": "6615a3bca483a805520a9b44"
            },
            "email": "micke@bth.se",
            "firstName": "mikael",
            "lastName": "svensson"
        },
        {
            "_id": {
                "$oid": "6615a3bca483a805520a9b43"
            },
            "email": "micke@bth.se",
            "firstName": "micke",
            "lastName": "larsson"
        }
    ]

    sut = UserController(dao=mocked_dao)

    # email param doesn't matter since dao.find is mocked
    result = sut.get_user_by_email("micke@bth.se")
    assert result == mocked_dao.find.return_value[0]

@pytest.mark.unit
def test_get_user_matching_multiple_error_message(capsys):
    """ Test that get_user_by_email prints an error message when multiple matches found. """

    mocked_dao = mock.MagicMock()
    mocked_dao.find.return_value = [
        {
            "_id": {
                "$oid": "6615a3bca483a805520a9b44"
            },
            "email": "micke@bth.se",
            "firstName": "mikael",
            "lastName": "svensson"
        },
        {
            "_id": {
                "$oid": "6615a3bca483a805520a9b43"
            },
            "email": "micke@bth.se",
            "firstName": "micke",
            "lastName": "larsson"
        }
    ]

    sut = UserController(dao=mocked_dao)

    # email param doesn't matter since dao.find is mocked
    sut.get_user_by_email("micke@bth.se")

    captured = capsys.readouterr()
    assert captured.out == "Error: more than one user found with mail micke@bth.se\n"

@pytest.mark.unit
def test_get_user_invalid_email():
    """ Test that providing an invalid email address raises a ValueError. """

    mocked_dao = mock.MagicMock()
    mocked_dao.find.return_value = [
        {
            "_id": {
                "$oid": "6615a3bca483a805520a9b44"
            },
            "email": "micke@bth.se",
            "firstName": "mikael",
            "lastName": "svensson"
        }
    ]

    sut = UserController(dao=mocked_dao)

    with pytest.raises(ValueError):
        result = sut.get_user_by_email("micke.se")

# TEST FAILS
@pytest.mark.unit
def test_get_user_no_match():
    """ Test that None is returned when no user is found for email. """

    mocked_dao = mock.MagicMock()
    mocked_dao.find.return_value = []

    sut = UserController(dao=mocked_dao)

    result = sut.get_user_by_email("micke@bth.se")
    assert result == None

@pytest.mark.unit
def test_get_user_database_failure():
    """ Test that an Exception is raised when a database operation fails. """

    mocked_dao = mock.MagicMock()

    # Mock an Exception being raised when dao.find is called (database operation failing)
    mocked_dao.find.side_effect = Exception()

    sut = UserController(dao=mocked_dao)

    with pytest.raises(Exception):
        result = sut.get_user_by_email("micke.se")