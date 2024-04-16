import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

"""
Module that tests the get_user_by_email method of
class UserController in scenarios where exceptions should be raised:
database error and invalid email
"""

@pytest.fixture
def sut():
    mockedDAO = MagicMock()
    mockedsut = UserController(dao=mockedDAO)
    return mockedsut


# missing local part
invalid_email_1 = '@email.com'

# missing @
invalid_email_2 = 'jane.doeemail.com'

# missing domain
invalid_email_3 = 'jane.doe@.com'

# missing . between domain and TLD part
invalid_email_4 = 'jane.doe@emailcom'

# missing TLD part
invalid_email_5 = 'jane.doe@email.'

# more than one @
invalid_email_6 = 'jane@doe@email.com'

# just in case... empty string
invalid_email_7 = ''



@pytest.mark.unit
@pytest.mark.parametrize('invalid_email',
                        [
                            (invalid_email_1),
                            (invalid_email_2),
                            (invalid_email_3),
                            (invalid_email_4),
                            (invalid_email_5),
                            (invalid_email_6),
                            (invalid_email_7)
                        ])
def test_get_user_by_email_invalid(sut, invalid_email):
    """
    Tests get_user_by_email method by passing
    invalid email. Should raise Value Error.
    The following errors are tested for:
    1. missing local part
    2. missing @
    3. missing domain
    4. missing TLD part
    5. missing dot separator . between domain and TLD part
    6. more than one @
    7. empty string
    """

    # assert that ValueError is raised when invalid email is passed
    with pytest.raises(ValueError):
        sut.get_user_by_email(email=invalid_email)


@pytest.mark.unit
def test_get_user_by_email_db_failure(sut):
    """
    Tests get_user_by_email method, that Exception is raised when database fails
    """

    valid_email = 'jane.doe@email.com'
    sut.dao.find.side_effect = Exception("DBfailure")

    # assert that exception is raised when database fails
    with pytest.raises(Exception):
        sut.get_user_by_email(email=valid_email)




