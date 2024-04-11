import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

"""
Module that tests the get_user_by_email method of
class UserController. The tests in this
module ensure that the warning
message is printed only in the scenario
where email address matches more than 1 user.
In all other cases no message should be printed.
"""

invalid_email = "invalidemail.com"
valid_email = 'jane.doe@email.com'
user = {
    'firstName': 'Jane',
    'email': valid_email
}
second_user = {
    'firstName': 'Hanna',
    'email': valid_email
}


@pytest.fixture
def sut():
    mockedDAO = MagicMock()
    mockedsut = UserController(dao=mockedDAO)
    return mockedsut


@pytest.mark.unit
def test_get_user_by_email_match_two_print(sut, capsys):
    """
    Tests get_user_by_email method with valid email.
    Two users match. No database failure.
    Assert that a warning message containing the
    email address is printed
    """
    # mockedDAO.find.return_value = [user, second_user]
    sut.dao.find.return_value = [user, second_user]

    sut.get_user_by_email(email=valid_email)
    printed = capsys.readouterr()

    assert valid_email in printed.out


@pytest.mark.unit
@pytest.mark.parametrize('user_email, user_array', [
    (valid_email, [user]),
    (valid_email, [])
    ])
def test_get_user_by_email_valid_no_print(sut, capsys, user_email, user_array):
    """
    Tests get_user_by_email method with:
    1. valid email - exactly one match,
    2. valid email - no match,
    In none of these cases should the
    print-function have been called
    """

    sut.dao.find.return_value = user_array
    sut.get_user_by_email(email=user_email)
    printed = capsys.readouterr()

    assert printed.out == ""


@pytest.mark.unit
def test_get_user_by_email_invalid_no_print(sut, capsys):
    """
    Tests get_user_by_email method with invalid email,
    The print function should not have been called
    """


    try:
        sut.get_user_by_email(email=invalid_email)
    except ValueError:
        # catch the value error so we can check
        # that the print function is not called before
        # ValueError is raised when the function
        # is called with invalid email.
        pass
    printed = capsys.readouterr()

    assert printed.out == ""


@pytest.mark.unit
def test_get_user_by_email_db_failure_no_print(sut, capsys):
    """
    Tests get_user_by_email method with valid email, there should be no printout when Exseption is raised due to database failure
    """

    sut.dao.find.side_effect = Exception("DBfailure")

    try:
        sut.get_user_by_email(email=valid_email)
    except Exception:
        # Using try/catch instead of pytest.raises because we do not
        # want more than 1 assert per test.
        # This way we can ensure that the
        # test does not stop before our assert for no
        # printout in case the Exception is not raised.
        # The Exception raising is tested in separate test
        pass

    printed = capsys.readouterr()

    assert printed.out == ""
