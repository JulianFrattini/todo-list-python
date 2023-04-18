import pytest
from src.controllers.usercontroller import UserController
from src.util.dao import DAO
import unittest.mock as mock

@pytest.mark.unit
def test_get_user_by_email_valid():
    mockedUsercontroller = mock.MagicMock()
    user_obj1 = { 'email': "test@test.com", 'firstName': "testytest", 'lastName': "testytest"}
    user_obj2 = { 'email': "testy@test.com", 'firstName': "testy", 'lastName': "testy"}
    users = [user_obj1, user_obj2]
    mockedUsercontroller.find.return_value = users
    email = "test@test.com"
    sut = UserController(dao=mockedUsercontroller)
    result = sut.get_user_by_email(email)
    assert result == users[0]

@pytest.mark.unit
def test_get_user_by_email_None():
    mockedUsercontroller = mock.MagicMock()
    user_obj1 = { 'email': "test@test.com", 'firstName': "testytest", 'lastName': "testytest"}
    user_obj2 = { 'email': "testy@test.com", 'firstName': "testy", 'lastName': "testy"}
    users = [user_obj1, user_obj2]
    mockedUsercontroller.find.return_value = users
    email = "nonetest.com"
    sut = UserController(dao=mockedUsercontroller)
    with pytest.raises(ValueError) as exc_info:
        sut.get_user_by_email(email)
    assert str(exc_info.value) == 'Error: invalid email address'

