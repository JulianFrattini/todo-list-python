import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController
from src.util.helpers import hasAttribute, ValidationHelper

def test_get_email_from_db():
    mockDatabase = mock.MagicMock()
    email = 'majdmazen24@gmail.com'
    mockDatabase.find.return_value = [{'email': email}]
    sut = UserController(dao=mockDatabase)
    validationResult = sut.get_user_by_email(email)
    assert validationResult == { "email": email}
    