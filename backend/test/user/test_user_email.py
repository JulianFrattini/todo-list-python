import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

# Setup
@pytest.fixture
def mock_dao():
    return MagicMock()

@pytest.fixture
def user_controller(mock_dao):
    return UserController(dao=mock_dao)

 # Test id:1
def test_get_user_by_valid_email(user_controller, mock_dao):
    mock_dao.find.return_value = [{'name': 'Test User', 'email': 'erik@mail.com'}]
    result = user_controller.get_user_by_email('erik@mail.com')
    assert result == {'name': 'Test User', 'email': 'erik@mail.com'}

# Test id:2
def test_multiple_users_warning(user_controller, mock_dao, capsys):
    mock_dao.find.return_value = [{'name': 'User One'}, {'name': 'User Two'}]
    result = user_controller.get_user_by_email('erik@mail.com')
    captured = capsys.readouterr()
    assert "more than one user found" in captured.out
    assert result == {'name': 'User One'}

# Test id:3
def test_no_user_found(user_controller, mock_dao):
    mock_dao.find.return_value = []
    result = user_controller.get_user_by_email('erik@mail.com')
    assert result is None

# Test id:4
def test_invalid_email(user_controller):
    with pytest.raises(ValueError):
        user_controller.get_user_by_email('invalidemail')

# Test id:5
def test_database_exception(user_controller, mock_dao):
    mock_dao.find.side_effect = Exception("DB Error")
    with pytest.raises(Exception) as excinfo:
        user_controller.get_user_by_email('erik@mail.com')
    assert "DB Error" in str(excinfo.value)
