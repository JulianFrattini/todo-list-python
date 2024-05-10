import pytest
from unittest.mock import patch, MagicMock
from src.controllers.usercontroller import UserController
from src.util.dao import DAO
import pymongo
import re


# Tests for get_user_by_email, ValueError separated due to more info shown if put in 
# pytest.raises.


# Test case for a valid email with one user found
def test_get_user_by_email_exceptions_mail(email="local_part@domain.host"):
              mock_dao = MagicMock()
              user_controller_instance = UserController(mock_dao)
              assert user_controller_instance.get_user_by_email(email)

# Test case for an invalid email
@pytest.mark.parametrize('email', 
                         [("ojsan")])
def test_get_user_by_email_exceptions_badmail(email):
              mock_dao = MagicMock()
              user_controller_instance = UserController(mock_dao)
              with pytest.raises(ValueError):
                     user_controller_instance.get_user_by_email(email)

# Test case for a valid email with no users found
@pytest.mark.parametrize('email, outcome', 
                         [("examplename.lastname@example.com", None), ("jane.doe@gmail.com", {'Email: jane.doe@gmail.com'})])
def test_get_user_by_email_nomatch(email, outcome):
       with patch('src.util.helpers.DAO', autospec=True):
              mockedDAO = MagicMock()
              mockedDAO.find.return_value = outcome
              uc = UserController(dao=mockedDAO)
              with pytest.raises(Exception):
                     assert uc.get_user_by_email(email) == outcome

# Test case for a valid email with multiple users returns first user
def test_valid_email_multiple_users_found():
    email = "local_part@domain.host"
    mock_dao = MagicMock()
    # Simulate finding multiple users with the given email
    mock_dao.find.return_value = [{'email': email}, {'email': email}]
    user_controller_instance = UserController(mock_dao)
    user = user_controller_instance.get_user_by_email(email)
    assert user == {'email': email}


# Test case for a valid email with multiple users prints warning message
def test_valid_email_multiple_users_found_warning():
    email = "local_part@domain.host"
    with patch('builtins.print') as mock_print:
       mock_dao = MagicMock()
       mock_dao.find.return_value = [{'email': email}, {'email': email}]
       user_controller_instance = UserController(mock_dao)
       user = user_controller_instance.get_user_by_email(email)        
       # Assert that the warning message contains the email using a regular expression pattern
       email_pattern = re.compile(rf'.*{re.escape(email)}.*')
       assert any(email_pattern.search(call[0][0]) for call in mock_print.call_args_list)

# Test case for database fail
def test_get_user_by_email_database_fail(email = "examplename.lastname@example.com"):
       with patch('src.util.helpers.DAO', autospec=True):
              with patch('re.fullmatch', autospec=True) as mockfullmatch:
                     mockfullmatch.return_value = True
                     mockedDAO = MagicMock()
                     mockedDAO.find.side_effect = Exception()
                     ucinstance = UserController(dao=mockedDAO)
                     with pytest.raises(Exception):
                            ucinstance.get_user_by_email(email)    


