import pytest
from unittest.mock import patch, MagicMock
from src.controllers.usercontroller import UserController

# Test case for a valid email
@pytest.mark.parametrize('user_array, exp_user', [([{
        'firstName': 'Jane',
        'lastName': 'Doe',
        'email': 'jane.doe@email.com'
    }], {
        'firstName': 'Jane',
        'lastName': 'Doe',
        'email': 'jane.doe@email.com'
    }), ([{
        'firstName': 'Some',
        'lastName': 'Doe',
        'email': 'jane.doe@email.com'
    }, {
        'firstName': 'Jane',
        'lastName': 'Doe',
        'email': 'jane.doe@email.com'
    }], {
        'firstName': 'Some',
        'lastName': 'Doe',
        'email': 'jane.doe@email.com'
    })])
def test_valid_email_users_found(user_array, exp_user):
    """
    Tests get_user_by_email method for
    valid email. It should
    1. return the user for one user
    2. return the first user for multiple user
    """
    email= "jane.doe@email.com"
    mock_dao = MagicMock()
    mock_dao.find.return_value = user_array
    user_controller_instance = UserController(mock_dao)
    assert user_controller_instance.get_user_by_email(email=email) == exp_user


# Test case for a valid email with multiple users prints warning message
def test_valid_email_multiple_users_found():
    """
        Tests get_user_by_email method for
        valid email with multiple users. It should
        print a warning message containing that email.Its a white box test. 
    """
    email = "first@domain.host"
    with patch('builtins.print') as mock_print:
        mock_dao = MagicMock()
        mock_dao.find.return_value = [{'email': email}, {'email': email}]
        user_controller_instance = UserController(mock_dao)
        user = user_controller_instance.get_user_by_email(email)
        # Assert that the warning message is printed with the correct content
        mock_print.assert_called()
        mock_print.assert_any_call(f'Error: more than one user found with mail {email}')


# Test case for an invalid email
@pytest.mark.parametrize('email', 
                         ["@email.com",
                          "jane.doeemail.com",
                          "jane.doe@.com",
                          "jane.doe@email",
                          "jane.doe@emailcom",
                          "jane.do@e@email.com",
                          ""])
def test_invalid_email(email):
              """
              Tests get_user_by_email method for
              invalid email. It should raise Value Error.
              The following errors are tested for:
              1. missing local part
              2. missing @
              3. missing domain
              4. missing TLD part
              5. missing dot separator . between domain and TLD part
              6. more than one @
              7. empty string
              """
              mock_dao = MagicMock()
              user_controller_instance = UserController(mock_dao)
              with pytest.raises(ValueError):
                     user_controller_instance.get_user_by_email(email)

# Test case for a valid email with no user found
@pytest.mark.parametrize('email', [
    "examplename.lastname@example.com"
])
def test_valid_email_with_no_user(email):
    """
    Tests get_user_by_email method for valid email but
    no user found. It should return None.
    """
    # Set up mock DAO
    with patch('src.util.helpers.DAO', autospec=True):
        mockedDAO = MagicMock()
        mockedDAO.find.return_value = []  # Simulate no user found
        uc = UserController(dao=mockedDAO)
        user = uc.get_user_by_email(email)
        assert user is None



# Test case for database fail
def test_database_fail(email = "examplename.lastname@example.com"):
    """
        Tests get_user_by_email method for
        database fail. It should
        raise Exception. 
    """
    with patch('src.util.helpers.DAO', autospec=True):
            with patch('re.fullmatch', autospec=True) as mockfullmatch:
                    mockfullmatch.return_value = True
                    mockedDAO = MagicMock()
                    mockedDAO.find.side_effect = Exception()
                    ucinstance = UserController(dao=mockedDAO)
                    with pytest.raises(Exception):
                        ucinstance.get_user_by_email(email)    

