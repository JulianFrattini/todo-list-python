import pytest
from unittest.mock import MagicMock, patch
from src.controllers.usercontroller import UserController
from src.util.dao import DAO

# Setting up the test enviroment with UserController with a mocked DAO returning tuple
@pytest.fixture
def user_controller():
    dao_mock = MagicMock(spec=DAO)
    controller = UserController(dao=dao_mock)
    return controller, dao_mock

# Valid Email with single User
def test_get_user_by_email_single_user(user_controller):
    controller, dao_mock = user_controller
    expected_user = {'email': 'jane.doe@gmail.com'}
    dao_mock.find.return_value = [expected_user]

    with patch('re.fullmatch', return_value=True):
        user = controller.get_user_by_email('jane.doe@gmail.com')
    assert user == expected_user
    dao_mock.find.assert_called_once_with({'email': 'jane.doe@gmail.com'})

# Valid Email with no User
def test_get_user_by_email_no_user(user_controller):
    controller, dao_mock = user_controller
    dao_mock.find.return_value = []

    with patch('re.fullmatch', return_value=True):
        user = controller.get_user_by_email('jane.doe@gmail.com')
    assert user is None

# Valid Email with multiple Users
def test_get_user_by_email_multiple_users(user_controller):
    controller, dao_mock = user_controller
    dao_mock.find.return_value = [{'email': 'jane.doe@gmail.com'}, {'email': 'jane.doe@gmail.com'}]

    with patch('re.fullmatch', return_value=True):
        user = controller.get_user_by_email('jane.doe@gmail.com')
    assert user == dao_mock.find.return_value[0]

# Invalid Email
def test_get_user_by_email_invalid_email(user_controller):
    controller, dao_mock = user_controller

    with patch('re.fullmatch', return_value=False), pytest.raises(ValueError):
        controller.get_user_by_email('jane.doe')