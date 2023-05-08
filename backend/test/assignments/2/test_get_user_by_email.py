import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

@pytest.fixture
def dao_mock():
    return MagicMock()

@pytest.fixture
def controller(dao_mock):
    return UserController(dao=dao_mock)

#   Test if user[0] is returned when len is 1
def test_valid_email_returns_user_object_1(dao_mock, controller):
    # Arrange
    email = "test@example.com"
    user = { 'email': "test@test.com", 'firstName': "test", 'lastName': "testsson"}
    users = [user]
    dao_mock.find.return_value = users
    # Act
    result = controller.get_user_by_email(email)

    # Assert
    assert result == users[0]


def test_multiple_users_with_same_email_returns_first_user_object(dao_mock, controller):
    # Arrange
    email = "test@example.com"
    users = [{"email": email, "name": "Test User 1"}, {"email": email, "name": "Test User 2"}]
    dao_mock.find.return_value = users

    # Act
    result = controller.get_user_by_email(email)

    # Assert
    assert result == users[0]

def test_invalid_email_raises_value_error(dao_mock, controller):
    # Arrange
    email = "invalid.email.se"
    dao_mock.find.return_value = []

    # Act and Assert
    with pytest.raises(ValueError) as e:
        controller.get_user_by_email(email)
    assert str(e.value) == 'Error: invalid email address'
    
def test_empty_email_raises_value_error(dao_mock, controller):
    # Arrange
    email = ""
    dao_mock.find.return_value = []

    # Act and Assert
    with pytest.raises(ValueError) as e:
        controller.get_user_by_email(email)
    assert str(e.value) == 'Error: invalid email address'

def test_nonexistent_email_returns_none(dao_mock, controller):
    # Arrange
    email = "test@example.com"
    users = []
    dao_mock.find.return_value = users

    # Act
    result = controller.get_user_by_email(email)

    # Assert
    assert result is None

def test_raise_exception_Database_fails(dao_mock, controller):
    dao_mock.find.side_effect = Exception("Database operation fails.")
    email = "test@example.com"
    with pytest.raises(Exception) as e:
        controller.get_user_by_email(email)
    assert e.value.args[0] == "Database operation fails."