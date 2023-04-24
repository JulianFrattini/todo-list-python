import pytest
import unittest.mock as mock
from unittest.mock import patch
from src.controllers.usercontroller import UserController

@pytest.fixture
def sut():
    mocked_dao = mock.MagicMock()
    return mocked_dao
    # clean-up

@pytest.mark.usercontroller
@pytest.mark.parametrize('email, expected', [('invalid.email.com', ValueError)])
def test_invalid_email(email, expected, sut):
    with patch('src.controllers.usercontroller.re.fullmatch') as mocked_validator:
        mocked_validator.return_value = None
    controller = UserController(dao=sut)
    with pytest.raises(expected):
        controller.get_user_by_email(email)

@pytest.mark.usercontroller
@pytest.mark.parametrize('email, expected', [('valid_email@email.com', Exception)])
def test_db_operation_failed(email, expected, sut):
    with patch('src.controllers.usercontroller.re.fullmatch') as mocked_validator:
        mocked_validator.return_value = True
    sut.find.return_value = Exception
    controller = UserController(dao=sut)
    with pytest.raises(expected):
        controller.get_user_by_email(email)

@pytest.mark.usercontroller
@pytest.mark.parametrize('email, expected', [('valid_email@email.com', None)])
def test_zero_associated_users(email, expected, sut):
    with patch('src.controllers.usercontroller.re.fullmatch') as mocked_validator:
        mocked_validator.return_value = True
    # Oracle does not specify type of return value for "find" in case no users are found
    # Return value of "None" also fails
    sut.find.return_value = []
    controller = UserController(dao=sut)
    assert controller.get_user_by_email(email) is expected

@pytest.mark.usercontroller
@pytest.mark.parametrize('email, expected', [('valid_email@email.com', {'email': 'valid_email@email.com'})])
def test_one_associated_user(email, expected, sut):
    with patch('src.controllers.usercontroller.re.fullmatch') as mocked_validator:
        mocked_validator.return_value = True
    sut.find.return_value = [{'email': email}]
    controller = UserController(dao=sut)
    result = controller.get_user_by_email(email)
    assert result == expected

@pytest.mark.usercontroller
@pytest.mark.parametrize('email, expected', [('valid_email@email.com', {'email': 'valid_email@email.com'})])
def test_two_associated_users(email, expected, sut):
    with patch('src.controllers.usercontroller.re.fullmatch') as mocked_validator:
        mocked_validator.return_value = True
    sut.find.return_value = [{'email': email}, {'email': 'another_valid_email@email.com'}]
    controller = UserController(dao=sut)
    result = controller.get_user_by_email(email)
    assert result == expected
