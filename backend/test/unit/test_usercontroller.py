import pytest
from src.controllers.usercontroller import UserController
from src.util.dao import DAO
from unittest.mock import Mock

mock_dao = Mock(spec=DAO) # Creating a mock DAO object
user_controller = UserController(dao=mock_dao) # Creating a UserController object with the mock DAO object

# Email variables to test
valid_email = 'valid@email.com'          #valid email
invalid_email = 'invalid@email.com'      #non existing email
wrong_format_email = 'wrongformat'       #wrong format email
empty_email = ''                         #empty field

# Test if existing email is valid
@pytest.mark.unit
def test_valid_email():
    mock_dao.find.return_value = [{'email': valid_email, 'name': 'Test User'}]

    result = user_controller.get_user_by_email(valid_email)
    assert result == {'email': valid_email, 'name': 'Test User'}

# Test if email doesn't exist
def test_email_not_found():
    mock_dao.find.return_value = []

    with pytest.raises(IndexError):
        user_controller.get_user_by_email(invalid_email)

# Test if multiple emails are found, if so, return first user.
@pytest.mark.unit
def test_multiple_emails_found():
    mock_dao.find.return_value = [{'email': valid_email, 'name': 'User 1'}, {'email': valid_email, 'name': 'User 2'}]

    result = user_controller.get_user_by_email(valid_email)

    assert result == {'email': valid_email, 'name': 'User 1'}

# Test if email has wrong format
@pytest.mark.unit
def test_invalid_format():

    with pytest.raises(ValueError):
        user_controller.get_user_by_email(wrong_format_email)

# Test if email field is empty
@pytest.mark.unit
def test_empty_field():

    with pytest.raises(ValueError):
        user_controller.get_user_by_email(empty_email)

