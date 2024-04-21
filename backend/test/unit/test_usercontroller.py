import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController

@pytest.fixture
def user_controller():
    mock_dao = mock.Mock()
    controller = UserController(mock_dao)
    return controller

def test_valid_email_single_user(user_controller):
    user_controller.dao.find = mock.Mock(return_value=[{'email': 'Rama@gmail.com', 'user': 'Rama'}])
    
    result = user_controller.get_user_by_email('Rama@gmail.com')
    
    assert result == {'email': 'Rama@gmail.com', 'user': 'Rama'}
    user_controller.dao.find.assert_called_once_with({'email': 'Rama@gmail.com'})
    


def test_valid_email_multiple_users(user_controller, capsys):
    user_controller.dao.find = mock.Mock(return_value=[{'email': 'Rama@gmail.com', 'user': 'Rama'}, {'email': 'Rama@gmail.com', 'user': 'Casso'}])
    
    result = user_controller.get_user_by_email('Rama@gmail.com')

    # Error THEN name 
    captured = capsys.readouterr()
    assert "Error: more than one user found with mail Rama@gmail.com" in captured.out
    assert result == {'email': 'Rama@gmail.com', 'user': 'Rama'}
    user_controller.dao.find.assert_called_once_with({'email': 'Rama@gmail.com'})


def test_valid_email_no_user(user_controller):
    user_controller.dao.find = mock.Mock(return_value=[])
    result = user_controller.get_user_by_email('Rama@gmail.com')

    assert result is None


def test_invalid_email(user_controller):
    with pytest.raises(ValueError) as exc_info:
        user_controller.get_user_by_email('uiauwfbiawubf')
    assert 'Error: invalid email address' in str(exc_info.value)


def test_database_exception(user_controller):
    user_controller.dao.find = mock.Mock(side_effect=Exception("Database failure"))

    with pytest.raises(Exception) as exc_info:
        user_controller.get_user_by_email('Rama@gmail.com')
    assert 'Database failure' in str(exc_info.value)
