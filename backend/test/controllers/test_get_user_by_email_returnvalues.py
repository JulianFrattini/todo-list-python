import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

"""
Module that tests the get_user_by_email method of
class UserController in scenarios
where valid email is inputted and
no database error occurs
"""

@pytest.fixture
def sut():
    mockedDAO = MagicMock()
    mockedsut = UserController(dao=mockedDAO)
    return mockedsut

valid_email = 'jane.doe@email.com'
user = {
    'firstName': 'Jane',
    'lastName': 'Doe',
    'email': valid_email
}
second_user = {
    'firstName': 'Hanna',
    'lastName': 'Doe',
    'email': valid_email
}


@pytest.mark.unit
def test_get_user_by_email_no_match(sut):
    """
    Tests get_user_by_email method with valid email.
    No user match. No database failure.
    Should return None.
    """
    sut.dao.find.return_value = []

    assert sut.get_user_by_email(email=valid_email) is None


@pytest.mark.unit
@pytest.mark.parametrize('user_array, exp_user', [([user], user), ([second_user, user], second_user)])
def test_get_user_by_email_match(sut,user_array, exp_user):
    """
    Tests get_user_by_email method with valid email.
    Tests one match and then two matches.
    In the second case the first user should be returned
    """
    
    sut.dao.find.return_value = user_array

    assert sut.get_user_by_email(email=valid_email) == exp_user

