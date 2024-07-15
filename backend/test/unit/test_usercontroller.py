import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController

"""Email exists, email not unique"""
@pytest.mark.unit
def test_exists_not_unique():
    mockedDao = mock.MagicMock()
    mockedDao.find.return_value = [{'Email': 'hello@gmail.com'}, {'Email': 'hello@gmail.com'}]
    user_controller = UserController(mockedDao)
    result = user_controller.get_user_by_email('hello@gmail.com')
    assert result == {'Email': 'hello@gmail.com'}

"""Email exists, email unique"""
@pytest.mark.unit
def test_exists_unique():
    mockedDao = mock.MagicMock()
    mockedDao.find.return_value = [{'Email': 'hello@gmail.com'}]
    user_controller = UserController(mockedDao)
    result = user_controller.get_user_by_email('hello@gmail.com')
    assert result == {'Email': 'hello@gmail.com'}

"""Email not valid"""
@pytest.mark.unit
def test_not_valid():
    with pytest.raises(ValueError, match='Error: invalid email address'):
        mockedDao = mock.MagicMock()
        mockedDao.find.return_value = [{'Email': 'hello'}]
        user_controller = UserController(mockedDao)
        user_controller.get_user_by_email('hello')

"""Email does not exists"""
@pytest.mark.unit
def test_not_exists():
    mockedDao = mock.MagicMock()
    mockedDao.find.return_value = []
    user_controller = UserController(mockedDao)
    result = user_controller.get_user_by_email("hello@gmail.com")
    assert result is None

"""Database operation failed"""
@pytest.mark.unit
def test_database_fail():
    with pytest.raises(Exception) as e:
        mockedDao = mock.MagicMock()
        mockedDao.side_effect = Exception()
        user_controller = UserController(mockedDao)
        user_controller.get_user_by_email("hello@gmail.com")