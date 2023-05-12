import pytest
import unittest.mock as mock
from unittest.mock import patch

from src.util.helpers import ValidationHelper2

class TestValidationHelper1:
    """Patching a hard-coded dependency (of the ValidationHelper2 onto (1) the DAO and (2) the UserController) using patch in the decorators. 
    The code of TestValidationHelper1 and TestValidationHelper2 do the same, but are syntactically different.
    """

    @pytest.fixture
    @patch('src.util.helpers.UserController', autospec=True)
    @patch('src.util.helpers.DAO', autospec=True)
    def sut(self, mockedDAO, mockedusercontroller):
        mockedDAO.return_value = None
        mockedusercontroller.return_value = mock.MagicMock()
        mockedusercontroller.return_value.get.return_value = {'age': 20}
        sut = ValidationHelper2()
        return sut

    @pytest.mark.demo
    def test_validateAge(self, sut):
        validationresult = sut.validateAge(userid=None)
        assert validationresult == 'valid'

class TestValidationHelper2:
    """Patching a hard-coded dependency (of the ValidationHelper2 onto (1) the DAO and (2) the UserController) using patch and the keyword with. 
    """

    @pytest.fixture
    def sut(self):
        with patch('src.util.helpers.UserController', autospec=True) as mockedusercontroller, \
                patch('src.util.helpers.DAO', autospec=True) as mockedDAO:
            mockedDAO.return_value = None
            mockedusercontroller.return_value = mock.MagicMock()
            mockedusercontroller.return_value.get.return_value = {'age': 20}
            sut = ValidationHelper2()
            return sut

    @pytest.mark.demo
    def test_validateAge(self, sut):
        validationresult = sut.validateAge(userid=None)
        assert validationresult == 'valid'