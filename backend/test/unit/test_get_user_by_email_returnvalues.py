import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

"""
Module that tests the get_user_by_email method of
class UserController in scenarios
where valid email is inputted and
no database error occurs
"""

valid_email = 'jane.doe@email.com'
user = {
    'firstName': 'Jane',
    'lastName': 'Doe',
    'email': 'jane.doe@email.com'
}
second_user = {
    'firstName': 'Hanna',
    'lastName': 'Doe',
    'email': 'jane.doe@email.com'
}
mockedDAO = MagicMock()
sut = UserController(dao=mockedDAO)



@pytest.mark.unit
def test_get_user_by_email_no_match():
    """
    Tests get_user_by_email method with valid email.
    No user match. No database failure.
    Should return None.
    """
    mockedDAO.find.return_value = []

    assert sut.get_user_by_email(email=valid_email) is None

@pytest.mark.unit
@pytest.mark.parametrize('user_array, exp_user', [([user], user), ([second_user, user], second_user)])
def test_get_user_by_email_match(user_array, exp_user):
    """
    Tests get_user_by_email method with email.
    Tests one match and then two matches.
    In the second case the first user should be returned
    """
    
    mockedDAO.find.return_value = user_array

    assert sut.get_user_by_email(email=valid_email) == exp_user

