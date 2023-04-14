import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

@pytest.fixture
def dao_mock():
    return MagicMock()

@pytest.fixture
def controller(dao_mock):
    return UserController(dao=dao_mock)

def test_get_user_by_email_with_valid_email_returns_user_object(dao_mock, controller):
    # Arrange
    email = "test@example.com"
    user = {"email": email, "name": "Test User"}
    dao_mock.find.return_value = [user]

    # Act
    result = controller.get_user_by_email(email)

    # Assert
    assert result == user

def test_get_user_by_email_with_multiple_users_returns_first_user_object_and_prints_error_message(dao_mock, controller):
    # Arrange
    email = "test@example.com"
    users = [{"email": email, "name": "Test User 1"}, {"email": email, "name": "Test User 2"}]
    dao_mock.find.return_value = users

    # Act
    result = controller.get_user_by_email(email)

    # Assert
    assert result == users[0]

def test_get_user_by_email_with_invalid_email_raises_value_error(dao_mock, controller):
    # Arrange
    email = "invalid-email"
    dao_mock.find.return_value = []

    # Act and Assert
    with pytest.raises(ValueError):
        controller.get_user_by_email(email)

def test_get_user_by_email_with_none_existent_return_none(dao_mock, controller):
    # Arrange
    email = "test@example.com"

    dao_mock.find.return_value = None

    # Act and Assert
    with pytest.raises(Exception):
        controller.get_user_by_email(email)

