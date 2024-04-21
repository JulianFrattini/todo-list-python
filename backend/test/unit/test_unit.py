import pytest
from src.controllers.usercontroller import UserController
from src.util.dao import DAO
from pymongo.errors import WriteError
from unittest import mock

# fixed mocked DAO Class
@pytest.fixture
@pytest.mark.unit
def mocked_dao():

    dao = mock.MagicMock(DAO)

    yield dao

@pytest.mark.unit
def test_get_user_by_email_valid_email_one_user(mocked_dao):
    """
    Test case 1
        valid email adress, database connection, found 1 user
        Excpecting: the first user
    """
    user = {
        "name": "user1",
        "email": "test@email.com"
    }

    #one user returns from find
    mocked_dao.find.return_value = [user]
    userController = UserController(mocked_dao)

    result = userController.get_user_by_email("test@email.com")

    # Excpecting no print and the return of the user
    assert result == user

@pytest.mark.unit
def test_get_user_by_email_valid_email_multiple_users(mocked_dao):
    """
    Test case 2
        valid email adress, database connection, more than 1 users found
        Excpecting: the first user
    """
    user1 = {
        "firstName": "user1",
        "lastName": "user1",
        "email": "test@email.com"
    }
    user2 = {
        "firstName": "user2",
        "lastName": "user2",
        "email": "test@email.com"
    }
    user3 = {
        "firstName": "user3",
        "lastName": "user3",
        "email": "test@email.com"
    }

    #three users returns from find
    # mocked_dao.find.return_value = [user1, user2, user3]

    mocked_dao.find.return_value = [user1, user2, user3]
    userController = UserController(mocked_dao)

    result = userController.get_user_by_email("test@email.com")

    # Excpecting only the first user
    assert result == user1 # return only the first user, index 0

@pytest.mark.unit
def test_get_user_by_email_valid_email_multiple_users_print(mocked_dao, capsys):
    """
    Test case 3
        valid email adress, database connection, more than 1 users found
        Expecting: print in console
    """
    user1 = {
        "firstName": "user1",
        "lastName": "user1",
        "email": "test@email.com"
    }
    user2 = {
        "firstName": "user2",
        "lastName": "user2",
        "email": "test@email.com"
    }
    user3 = {
        "firstName": "user3",
        "lastName": "user3",
        "email": "test@email.com"
    }

    #three users returns from find
    mocked_dao.find.return_value = [user1, user2, user3]
    userController = UserController(mocked_dao)

    result = userController.get_user_by_email("test@email.com")
    captured = capsys.readouterr()

    # Excpecting print in console
    assert captured.out == 'Error: more than one user found with mail test@email.com\n'

@pytest.mark.unit
def test_get_user_by_email_invalid_email(mocked_dao):
    """
    Test case 4
        Invalid email adress
        Excpecting: 'ValueError'
    """
    userController = UserController(mocked_dao)

    # Expects that get_user_by_email raises ValueError
    with pytest.raises(ValueError):
        userController.get_user_by_email("testemail.com")


@pytest.mark.unit
def test_get_user_by_email_database_failure(mocked_dao):
    """
    Test case 5
        Database failure
        Excpecting: Exception
    """
    mocked_dao.find.side_effect = WriteError("The Class DAO raises WriteError when conection to database fails")
    userController = UserController(mocked_dao)

    # Expecting that get_user_by_email raises Exception
    with pytest.raises(Exception):
        userController.get_user_by_email("test@email.com")

@pytest.mark.unit
def test_get_user_by_email_valid_email_no_user(mocked_dao):
    """
    Test case 6
        valid email adress, database connection, no user found
        Excpecting: 'None'
    """

    # no user return empty list from dao.find
    mocked_dao.find.return_value = []
    userController = UserController(mocked_dao)

    result = userController.get_user_by_email("test@email.com")

    # Excpecting 'None'
    assert result == None