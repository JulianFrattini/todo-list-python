import pytest
from unittest.mock import patch, MagicMock

# $ pytest -m unit

# different systems under test
from src.controllers.usercontroller import UserController

# Test cases:
# 1. The email address is not valid
# 2. The email address is valid, but causes an exception from the database
# 3. The email address is valid, and the user is not found
# 4. The email address is valid and the user is found
# 5. The email address is valid and multiple users are found

@pytest.mark.unit
def test_invalid_email():
    user = {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe'}

    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [user]

    uc = UserController(dao=mockedDAO)

    with pytest.raises(ValueError):
        uc.get_user_by_email(email='jane.doe')

@pytest.mark.unit
def test_valid_email_exception_from_db():
    mockedDAO = MagicMock()
    mockedDAO.find.side_effect = Exception('Something went wrong')

    uc = UserController(dao=mockedDAO)

    with pytest.raises(Exception):
        uc.get_user_by_email(email='not.present.user@example.com')

@pytest.mark.unit
def test_valid_email_user_not_found():
    user = None

    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [user]

    uc = UserController(dao=mockedDAO)
    assert uc.get_user_by_email(email='janedoe@example.com') == None

@pytest.mark.unit
def test_valid_email_user_found():
    user = {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'janedoe@example.com'}

    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [user]

    uc = UserController(dao=mockedDAO)
    assert uc.get_user_by_email(email='janedoe@example.com') == user

@pytest.mark.unit
def test_valid_email_multiple_users():
    user_a = {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'janedoe@example.com'}
    user_b = {'firstName': 'John', 'lastName': 'Doe', 'email': 'janedoe@example.com'}

    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [user_a, user_b]

    with patch('builtins.print') as mock_print:
        uc = UserController(dao=mockedDAO)
        assert uc.get_user_by_email(email='janedoe@example.com') == user_a

        mock_print.assert_called_once_with(f'Error: more than one user found with mail janedoe@example.com')
