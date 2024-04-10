import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

"""
Module that tests the get_user_by_email method of
class UserController in scenarios where exceptions should be raised:
database error and invalid email
"""

valid_email = 'jane.doe@email.com'

@pytest.fixture
def sut():
    mockedDAO = MagicMock()
    mockedsut = UserController(dao=mockedDAO)
    return mockedsut

@pytest.mark.unit
def test_get_user_by_email_db_failure(sut):
    """
    Tests get_user_by_email method, that Exception is raised when database fails
    """

    sut.dao.find.side_effect = Exception("DBfailure")

    # assert that exception is raised when database fails
    with pytest.raises(Exception):
        sut.get_user_by_email(email=valid_email)

