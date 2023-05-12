import pytest
from src.controllers.usercontroller import UserController
from src.util.dao import DAO
import unittest.mock as mock

@pytest.mark.unit
def test_get_user_by_email_valid():
    mockedUsercontroller = mock.MagicMock()
    user_obj1 = { 'email': "test@test.com", 'firstName': "testytest", 'lastName': "testytest"}
    users = [user_obj1]
    mockedUsercontroller.find.return_value = users
    email = "test@test.com"
    sut = UserController(dao=mockedUsercontroller)
    result = sut.get_user_by_email(email)
    assert result == users[0]

@pytest.mark.unit
def test_get_user_by_email_invalid_str():
    mockedUsercontroller = mock.MagicMock()
    users = []
    mockedUsercontroller.find.return_value = users
    email = "nonetest.com"
    sut = UserController(dao=mockedUsercontroller)
    with pytest.raises(ValueError) as exc_info:
        sut.get_user_by_email(email)
    assert str(exc_info.value) == 'Error: invalid email address'

@pytest.mark.unit
def test_get_user_by_email_multiple_users():
    mockedUsercontroller = mock.MagicMock()
    user_obj1 = { 'email': "test@test.com", 'firstName': "testytest", 'lastName': "testytest"}
    user_obj2 = { 'email': "test@test.com", 'firstName': "testy", 'lastName': "testy"}
    user_obj3 = { 'email': "test@test.com", 'firstName': "testA", 'lastName': "testA"}
    users = [user_obj1, user_obj2, user_obj3]
    mockedUsercontroller.find.return_value = users
    email = "test@test.com"
    sut = UserController(dao=mockedUsercontroller)
    result = sut.get_user_by_email(email)
    assert result == users[0]

# cover line 38-39
# @pytest.mark.unit
# def test_get_user_by_email_None():
#     mockedUsercontroller = mock.MagicMock()
#     users = []
#     mockedUsercontroller.find.return_value = users
#     email = "none@test.com"
#     sut = UserController(dao=mockedUsercontroller)
#     result = sut.get_user_by_email(email)
#     assert result == None

@pytest.mark.unit
def test_get_user_by_email_raise_exception():
    mockedUsercontroller = mock.MagicMock()
    mockedUsercontroller.find.side_effect = Exception("Database operation fails.")
    email = "test@test.com"
    sut = UserController(dao=mockedUsercontroller)
    with pytest.raises(Exception) as exc_info:
        sut.get_user_by_email(email)
    assert str(exc_info.value) == "Database operation fails."