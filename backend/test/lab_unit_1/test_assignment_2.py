

from src.controllers.usercontroller import UserController
import pytest
import unittest.mock as mock
from unittest.mock import patch
from src.util.dao import DAO


# def test_get_user_by_email_old():
#     mockedDAO = mock.MagicMock()
#     mockedDAO.find.return_value = [{"person object"}]

#     sut = UserController(dao=mockedDAO)

#     usercontrollerresult = sut.get_user_by_email(email="test@email.com")
#     assert usercontrollerresult == {"person object"}


@pytest.mark.parametrize(
    "input_email, return_value, output_expected",
    [
        (
            "test@email.com",
            [{"person object"}],
            {"person object"}
        ), # test basic functionality
        (
            "not an email",
            [{"person object"}],
            ValueError('Error: invalid email address')
        ), # test error if not an email
        (
            "test@email.com",
            (),
            TypeError("tuple index out of range") 
        ), # tests returning tuple as person object
        (
            "test@email.com",
            13,
            TypeError("object of type 'int' has no len()")
        ), # tests returning integer as person object
        (
            13,
            [{"person object"}],
            "expected string or bytes-like object"
        ), # test error email not a string
        (
            "test@email.com",
            [{"person object"}, {"other person object"}],
            {"person object"}
        ) # tests returning first email applicable
    ]
)
def test_get_user_by_email(input_email, return_value, output_expected):
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = return_value

    sut = UserController(dao=mockedDAO)

    try:
        usercontrollerresult = sut.get_user_by_email(email=input_email)
        assert usercontrollerresult == output_expected
    except Exception as e:
        assert str(e) == str(output_expected)

