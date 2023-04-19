import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController

@pytest.mark.usercontroller
@pytest.mark.parametrize('email, expected', [('invalid.email.com', ValueError)])
def test_invalid_email(email, expected):
    mocked_dao = mock.MagicMock()
    controller = UserController(dao=mocked_dao)
    with pytest.raises(expected):
        controller.get_user_by_email(email)

@pytest.mark.usercontroller
@pytest.mark.parametrize('email, expected', [('valid_email@email.com', Exception)])
def test_db_operation_failed(email, expected):
    mocked_dao = mock.MagicMock()
    mocked_dao.find.return_value = Exception
    controller = UserController(dao=mocked_dao)
    with pytest.raises(expected):
        controller.get_user_by_email(email)

@pytest.mark.usercontroller
@pytest.mark.parametrize('email, expected', [('valid_email@email.com', None)])
def test_zero_associated_users(email, expected):
    mocked_dao = mock.MagicMock()
    # Oracle does not specify type of return value for "find" in case no users are found
    # Return value of "None" also fails
    mocked_dao.find.return_value = []
    controller = UserController(dao=mocked_dao)
    assert controller.get_user_by_email(email) is expected

@pytest.mark.usercontroller
@pytest.mark.parametrize('email, expected', [('valid_email@email.com', {'email': 'valid_email@email.com'})])
def test_one_associated_user(email, expected):
    mocked_dao = mock.MagicMock()
    mocked_dao.find.return_value = [{'email': email}]
    controller = UserController(dao=mocked_dao)
    result = controller.get_user_by_email(email)
    assert result == expected

@pytest.mark.usercontroller
@pytest.mark.parametrize('email, expected', [('valid_email@email.com', {'email': 'valid_email@email.com'})])
def test_two_associated_users(email, expected):
    mocked_dao = mock.MagicMock()
    mocked_dao.find.return_value = [{'email': email}, {'email': 'another_valid_email@email.com'}]
    controller = UserController(dao=mocked_dao)
    result = controller.get_user_by_email(email)
    assert result == expected
