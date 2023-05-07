import pytest
import unittest.mock as mock
from unittest.mock import patch
from src.controllers.usercontroller import UserController

@pytest.mark.unit
def test_check_valid_email():
    """ 
    Test if get_user_by_email function returns the user object when the valid email is sent and
    the email exists in the database
    """
    mockDatabase = mock.MagicMock()
    email = 'test@gmail.com'
    mockDatabase.find.return_value = [{'email': email}]
    sut = UserController(dao=mockDatabase)

    results = sut.get_user_by_email(email)
    assert results == { "email": email}
    
@pytest.mark.unit
def test_check_valid_email_not_in_db():
    """ 
    Test if get_user_by_email function does not return a user object when a valid email is sent but
    not exists in database
    """
    mockDatabase = mock.MagicMock()
    emailInDB = 'test@gmail.com'
    mockDatabase.find.return_value = [{'email': emailInDB}]
    sut = UserController(dao=mockDatabase)
    emailNotInDB = 'sut@edutask.com'

    results = sut.get_user_by_email(emailNotInDB)
    assert results == None

@pytest.mark.unit
def test_empty_string():
    """ 
    Test if get_user_by_email function raises an exception when the input is empty string
    """
    mockDatabase = mock.MagicMock()
    sut = UserController(dao=mockDatabase)
    emptyEmail = ''

    with pytest.raises(Exception):
        sut.get_user_by_email(emptyEmail)

@pytest.mark.unit
def test_empty_input():
    """
    Test if get_user_by_email function raises an exception when the input is empty
    """
    mockDatabase = mock.MagicMock()
    sut = UserController(dao=mockDatabase)

    with pytest.raises(Exception):
        sut.get_user_by_email()

@pytest.mark.unit
def test_no_at():
    """
    Test if get_user_by_email function raises a ValueError when sending no @
    """
    mockDatabase = mock.MagicMock()
    email = 'testgmail.com'
    mockDatabase.find.return_value = [{'email': email}]
    sut = UserController(dao=mockDatabase)

    with pytest.raises(ValueError):
        sut.get_user_by_email(email)

@pytest.mark.unit
@patch('builtins.print')
def test_with_two_same_email(mock_print):
    """
    Test if get_user_by_email function raises a print error message when 2 of same mail exists in database
    """
    mockDatabase = mock.MagicMock()
    email = 'test@gmail.com'
    mockDatabase.find.return_value = [{'email': email}, {'email': email}]
    sut = UserController(dao=mockDatabase)
    sut.get_user_by_email(email)

    # This test if the print displays in usercontroller
    mock_print.assert_called_with('Error: more than one user found with mail test@gmail.com')

@pytest.mark.unit
def test_missing_dot_before_domain():
    """
    Test if get_user_by_email function raises an exception when no dot is sent
    """
    mockDatabase = mock.MagicMock()
    email = 'test@gmailcom'
    mockDatabase.find.return_value = [{'email': email}]
    sut = UserController(dao=mockDatabase)

    with pytest.raises(ValueError):
        sut.get_user_by_email(email)

@pytest.mark.unit
def test_database_operation_exception():
    """
    Test if get_user_by_email function raises an exception when database operation fails.
    """
    mockDatabase = mock.MagicMock()
    email = 'test@gmail.com'
    mockDatabase.find.side_effect = Exception("Database operation failed")  # Simulate a database operation failure
    sut = UserController(dao=mockDatabase)

    with pytest.raises(Exception):
        sut.get_user_by_email(email)