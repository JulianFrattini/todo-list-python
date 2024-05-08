import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController



@pytest.mark.unit
def test_email_multiple_entries():
    mock_controller = mock.MagicMock()
    user_detail1 = {'email': "duplicate@example.com", 'firstName': "John", 'lastName': "Doe"}
    user_detail2 = {'email': "duplicate@example.com", 'firstName': "Jane", 'lastName': "Doe"}
    user_detail3 = {'email': "duplicate@example.com", 'firstName': "Jim", 'lastName': "Beam"}
    user_list = [user_detail1, user_detail2, user_detail3]
    mock_controller.find.return_value = user_list
    test_email = "duplicate@example.com"
    user_controller = UserController(dao=mock_controller)
    outcome = user_controller.get_user_by_email(test_email)
    assert outcome == user_list[0]


@pytest.mark.unit
def test_valid_email():
    mock_controller = mock.MagicMock()
    user_detail = {'email': "user@example.com", 'firstName': "FirstName", 'lastName': "LastName"}
    user_list = [user_detail]
    mock_controller.find.return_value = user_list
    test_email = "user@example.com"
    user_controller = UserController(dao=mock_controller)
    outcome = user_controller.get_user_by_email(test_email)
    assert outcome == user_list[0]

@pytest.mark.unit
def test_invalid_email_format():
    mock_controller = mock.MagicMock()
    empty_user_list = []
    mock_controller.find.return_value = empty_user_list
    test_email = "invalidemail"
    user_controller = UserController(dao=mock_controller)
    with pytest.raises(ValueError) as exception_info:
        user_controller.get_user_by_email(test_email)
    assert str(exception_info.value) == 'Error: invalid email address'

@pytest.mark.unit
def test_email_throws_exception():
    mock_controller = mock.MagicMock()
    mock_controller.find.side_effect = Exception("Failed to query database.")
    test_email = "error@example.com"
    user_controller = UserController(dao=mock_controller)
    with pytest.raises(Exception) as exception_info:
        user_controller.get_user_by_email(test_email)
    assert str(exception_info.value) == "Failed to query database."
