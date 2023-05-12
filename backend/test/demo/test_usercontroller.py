import re
import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController
from src.util.dao import DAO

# Prepare mock DAO
mock_dao = Mock(spec=DAO)
uc = UserController(dao=mock_dao)

emailValidator = re.compile('.*@.*')

# Test if email of existing user is valid
@pytest.mark.unit
def test_valid_email_existing_user():
    email = 'test@example.com'
    mock_dao.find.return_value = [{'email': email, 'name': 'Test User'}]

    result = uc.get_user_by_email(email)
    assert result == {'email': email, 'name': 'Test User'}

#Test valid email of a non-existing user
@pytest.mark.unit
def test_valid_email_non_existing_user():
    email = 'non_existing@example.com'
    mock_dao.find.return_value = []

    result = uc.get_user_by_email(email)
    assert result is None
@pytest.mark.unit
def get_user_by_email(self, email):
    if not isinstance(email, str) or not re.fullmatch(emailValidator, email):
        raise ValueError('Error: invalid email address')

    users = self.dao.find({'email': email})
    if not users:
        return None
    elif len(users) >= 1:
        return users[0]
    else:
        print(f'Error: more than one user found with mail {email}')
        return users[0]

# Test case for an invalid email format
@pytest.mark.unit
def test_invalid_email_format():
    email = 'invalid_email_format'

    with pytest.raises(ValueError):
        uc.get_user_by_email(email)

# Test case for an empty email string
@pytest.mark.unit
def test_empty_email():
    email = ''

    with pytest.raises(ValueError):
        uc.get_user_by_email(email)

# Test case for a non-string email input
@pytest.mark.unit
def test_non_string_email_input():
    email = 123

    with pytest.raises(ValueError):
        uc.get_user_by_email(email)

# Test case for when the database is unavailable
@pytest.mark.unit
def test_database_unavailable():
    email = 'test@example.com'
    mock_dao.find.side_effect = Exception("Database operation failed")

    with pytest.raises(Exception):
        uc.get_user_by_email(email)

    # Reset the side effect
    mock_dao.find.side_effect = None

# Test case for duplicate email addresses in the database
@pytest.mark.unit
def test_duplicate_email_addresses():
    email = 'test@example.com'
    mock_dao.find.return_value = [
        {'email': email, 'name': 'Test User'},
        {'email': email, 'name': 'Test User 2'},
    ]

    result = uc.get_user_by_email(email)
    assert result == {'email': email, 'name': 'Test User'}
