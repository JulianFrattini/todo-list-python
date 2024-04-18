import pytest
from unittest.mock import patch, MagicMock

# $ pytest -m controllers

# different systems under test
from src.controllers.usercontroller import UserController

# Test cases:
# 1. The email address is not valid
# 2. The email address is valid, but causes an exception from the database
# 3. The email address is valid and the user is not found
# 4. The email address is valid and the user is found
# 5. The email address is valid and multiple users are found

@pytest.mark.unit
def test_1():
    user = {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe'}

    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [user]

    uc = UserController(dao=mockedDAO)

    try:
        uc.get_user_by_email(email='jane.doe')
    except ValueError:
        pass
    else:
        assert False, 'Expected ValueError but none was raised.'

@pytest.mark.unit
def test_2():
    mockedDAO = MagicMock()
    mockedDAO.find.side_effect = Exception('Something went wrong')

    uc = UserController(dao=mockedDAO)

    try:
        uc.get_user_by_email(email='not.present.user@example.com')
    except Exception:
        pass
    else:
        assert False, 'Expected Exception but none was raised.'

@pytest.mark.unit
def test_3():
    user = None

    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [user]

    uc = UserController(dao=mockedDAO)
    assert uc.get_user_by_email(email='janedoe@example.com') == None

@pytest.mark.unit
def test_4():
    user = {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'janedoe@example.com'}

    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [user]

    uc = UserController(dao=mockedDAO)
    assert uc.get_user_by_email(email='janedoe@example.com') == user

@pytest.mark.unit
def test_5():
    user_a = {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'janedoe@example.com'}
    user_b = {'firstName': 'John', 'lastName': 'Doe', 'email': 'janedoe@example.com'}

    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [user_a, user_b]

    uc = UserController(dao=mockedDAO)
    assert uc.get_user_by_email(email='janedoe@example.com') == user_a
