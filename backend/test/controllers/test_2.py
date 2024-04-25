import pytest
from unittest.mock import patch, MagicMock

# different systems under test
from src.util.daos import getDao
from src.controllers.usercontroller import UserController





class TestUserController:
    @pytest.mark.parametrize('list_of_users, expected', [
        (["hej@gmail.com", "bubäaaa@hotmail.com"], "hej@gmail.com"),
        (["hej@gmail.com"], "hej@gmail.com"),
    ])
    def test_get_user_without_exceptions_raised(self, list_of_users, expected):

        mockedDAO = MagicMock()
        mockedDAO.find.return_value = list_of_users
        uc = UserController(dao=mockedDAO)

        with patch("src.controllers.usercontroller.re.fullmatch") as mockfullmatch:
            mockfullmatch.return_value = True

            assert uc.get_user_by_email(email='') == expected

    @pytest.mark.parametrize('list_of_users', [
        (["hej@gmail.com", "bubäaaa@hotmail.com"]),
        (["hej@gmail.com"], "hej@gmail.com"),
    ])
    def test_get_user_with_value_error(self, list_of_users):

        mockedDAO = MagicMock()
        mockedDAO.find.return_value = list_of_users
        uc = UserController(dao=mockedDAO)

        with pytest.raises(ValueError), patch("src.controllers.usercontroller.re.fullmatch") as mockfullmatch:
            mockfullmatch.return_value = False
            uc.get_user_by_email(email='')

    @pytest.mark.parametrize('list_of_users', [
        (["hej@gmail.com", "bubäaaa@hotmail.com"]),
        (["hej@gmail.com"], "hej@gmail.com"),
    ])
    def test_get_user_with_exception(self, list_of_users):

        mockedDAO = MagicMock()
        mockedDAO.find.return_value = list_of_users
        mockedDAO.find.side_effect = Exception()
        uc = UserController(dao=mockedDAO)

        with pytest.raises(Exception), patch("src.controllers.usercontroller.re.fullmatch") as mockfullmatch:
            mockfullmatch.return_value = True
            uc.get_user_by_email(email='')