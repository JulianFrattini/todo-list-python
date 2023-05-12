import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController
from src.util.dao import DAO

# Prepare mock DAO
mock_dao = Mock(spec=DAO)
uc = UserController(dao=mock_dao)

@pytest.mark.unit
def test_valid_email_existing_user():
    email = 'test@example.com'
    mock_dao.find.return_value = [{'email': email, 'name': 'Test User'}]

    result = uc.get_user_by_email(email)
    assert result == {'email': email, 'name': 'Test User'}

@pytest.mark.unit
def test_valid_email_non_existing_user():
    email = 'non_existing@example.com'
    mock_dao.find.return_value = []

    result = uc.get_user_by_email(email)
    assert result is None

@pytest.mark.unit
def test_invalid_email_format():
    email = 'invalid_email_format'

    with pytest.raises(ValueError):
        uc.get_user_by_email(email)

@pytest.mark.unit
def test_empty_email():
    email = ''

    with pytest.raises(ValueError):
        uc.get_user_by_email(email)

@pytest.mark.unit
def test_non_string_email_input():
    email = 123

    with pytest.raises(ValueError):
        uc.get_user_by_email(email)

@pytest.mark.unit
def test_database_unavailable():
    email = 'test@example.com'
    mock_dao.find.side_effect = Exception("Database operation failed")

    with pytest.raises(Exception):
        uc.get_user_by_email(email)

    # Reset the side effect
    mock_dao.find.side_effect = None

@pytest.mark.unit
def test_duplicate_email_addresses():
    email = 'test@example.com'
    mock_dao.find.return_value = [
        {'email': email, 'name': 'Test User'},
        {'email': email, 'name': 'Test User 2'},
    ]

    result = uc.get_user_by_email(email)
    assert result == {'email': email, 'name': 'Test User'}
