"""
Test module for usercontroller
uses pytest
"""
import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController

class TestUserController:
    """
    Tests for usercontroller.py
    """

    def test_get_user_valid_registered(self):
        """_summary_
        """
        email = "an@email.com"
        mock_dao = mock.MagicMock()
        mock_dao.find.return_value = [ {'email': email } ]
        sut = UserController(dao = mock_dao)
        user_result = sut.get_user_by_email(email = email)
        assert user_result == { 'email': email }

    def test_get_user_valid_registered_multiple(self):
        """_summary_
        """
        email = "an@email.com"
        mock_dao = mock.MagicMock()
        mock_dao.find.return_value = [ {'email': email }, {'email': email } ]
        sut = UserController(dao = mock_dao)
        user_result = sut.get_user_by_email(email = email)
        assert user_result == { 'email': email }

    def test_get_user_invalid_email_no_dot_no_at(self):
        """s
        """
        email = "notanemail"
        mock_dao = mock.MagicMock()
        sut = UserController(dao = mock_dao)
        with pytest.raises(ValueError) as _e:
            _ = sut.get_user_by_email(email = email)


    def test_get_user_invalid_email_no_at(self):
        """s
        """
        email = "notan.email"
        mock_dao = mock.MagicMock()
        sut = UserController(dao = mock_dao)
        with pytest.raises(ValueError) as _e:
            _ = sut.get_user_by_email(email = email)


    def test_get_user_invalid_email_no_domain_and_host(self):
        """s
        """
        email = "notanemail@"
        mock_dao = mock.MagicMock()
        sut = UserController(dao = mock_dao)
        with pytest.raises(ValueError) as _e:
            _ = sut.get_user_by_email(email = email)


    def test_get_user_invalid_email_no_host(self):
        """s
        """
        email = "not@anemail."
        mock_dao = mock.MagicMock()
        sut = UserController(dao = mock_dao)
        with pytest.raises(ValueError) as _e:
            _ = sut.get_user_by_email(email = email)

    def test_get_user_invalid_email_no_local(self):
        """s
        """
        email = "@notan.email"
        mock_dao = mock.MagicMock()
        sut = UserController(dao = mock_dao)
        with pytest.raises(ValueError) as _e:
            _ = sut.get_user_by_email(email = email)


    def test_get_user_invalid_email_no_local_and_host(self):
        """s
        """
        email = "@notanemail"
        mock_dao = mock.MagicMock()
        sut = UserController(dao = mock_dao)
        with pytest.raises(ValueError) as _e:
            _ = sut.get_user_by_email(email = email)


    def test_get_user_invalid_email_no_domain(self):
        """s
        """
        email = "not@.anemail"
        mock_dao = mock.MagicMock()
        sut = UserController(dao = mock_dao)
        with pytest.raises(ValueError) as _e:
            _ = sut.get_user_by_email(email = email)


    def test_get_user_invalid_email_host_no_dot(self):
        """s
        """
        email = "not@anemailcom"
        mock_dao = mock.MagicMock()
        sut = UserController(dao = mock_dao)
        with pytest.raises(ValueError) as _e:
            _ = sut.get_user_by_email(email = email)


    def test_get_user_valid_email_not_registered(self):
        """_summary_
        """
        email = "an@email.com"
        mock_dao = mock.MagicMock()
        mock_dao.find.return_value = []
        sut = UserController(dao = mock_dao)
        user_result = sut.get_user_by_email(email = email)
        assert user_result is None


    def test_get_user_valid_email_database_error(self):
        """_summary_
        """
        email = "an@email.com"
        mock_dao = mock.MagicMock()
        mock_dao.find.side_effect = Exception("test")
        sut = UserController(dao = mock_dao)
        with pytest.raises(Exception) as _e:
            _ = sut.get_user_by_email(email = email)

    def test_get_user_invalid_email_database_error(self):
        """_summary_
        """
        email = "notanemail"
        mock_dao = mock.MagicMock()
        mock_dao.find.side_effect = Exception("test")
        sut = UserController(dao = mock_dao)
        with pytest.raises(ValueError) as _e:
            _ = sut.get_user_by_email(email = email)
