import pytest
from unittest.mock import patch, MagicMock

from src.controllers.usercontroller import UserController

valid_email = 'jane.doe@email.com'
user = {
    'firstName': 'Jane',
    'lastName': 'Doe',
    'email': 'jane.doe@email.com'
}


@pytest.mark.unit
def test_get_user_by_email_valid_match_one_nofail():
    """
    Tests get_user_by_email method with valid email.
    Exactly 1 user match. No database failure.
    Should return the user object.
    """
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [user]

    sut = UserController(dao=mockedDAO)

    assert sut.get_user_by_email(email=valid_email) == user

@pytest.mark.unit
def test_get_user_by_email_valid_nomatch_nofail():
    """
    Tests get_user_by_email method with valid email.
    No user match. No database failure.
    Should return None.
    """
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = []

    sut = UserController(dao=mockedDAO)

    assert sut.get_user_by_email(email=valid_email) is None


