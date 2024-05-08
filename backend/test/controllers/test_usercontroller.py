import pytest
from unittest.mock import MagicMock

from src.controllers.usercontroller import UserController

class TestUserControllerGetUserByEmail:
    @pytest.fixture
    def sut_single_user(self):
        """
        Fixture for creating a user controller with a mocked DAO configured to return a single user.

        Returns: UserController: An instance of UserController with a mocked DAO configured to return a single user.
        """
        matched_users = [
            {'firstName': 'test1_first', 'lastName': 'test1_last', 'email': 'test@test.com'}
        ]
        mocked_dao = MagicMock()
        mocked_dao.find.return_value = matched_users #This configures the find method of the mocked DAO to return a list containing two user objects
        uc = UserController(dao=mocked_dao)
        return uc

    @pytest.fixture
    def sut_multiple_user(self):
        """
        Fixture for creating a user controller with a mocked DAO configured to return multiple users.

        Returns: UserController: An instance of UserController with a mocked DAO configured to return multiple users.
        """
        matched_users = [
            {'firstName': 'test1_first', 'lastName': 'test1_last', 'email': 'test@test.com'},
            {'firstName': 'test2_first', 'lastName': 'test2_last', 'email': 'test@test.com'}
        ]
        mocked_dao = MagicMock()
        mocked_dao.find.return_value = matched_users #This configures the find method of the mocked DAO to return a list containing two user objects
        uc = UserController(dao=mocked_dao)
        return uc

    @pytest.fixture
    def invalid_email(self):
        """
        Fixture for providing an invalid email address string.

        Returns: str: An invalid email address string.
        """
        return "test.com"

    @pytest.fixture
    def valid_email(self):
        """
        Fixture for providing a valid email address string.

        Returns: str: A valid email address string.
        """
        return "test@test.com"

    @pytest.fixture
    def other_email(self):
        """
        Fixture for providing another valid email address string.

        Returns: str: Another valid email address string.
        """
        return "foo@bar.com"

    @pytest.mark.usercontroller
    def test_get_user_by_email_1(self, valid_email):
        """
        Test case 1: Database fails
        Email associated with user: Not applicable
        Multiple Users: Not applicable
        Email is Valid: Not applicable
        Database Operation Fails: TRUE
        Outcome: Exception
        """
        mocked_dao = MagicMock()
        mocked_dao.find.side_effect = Exception() #This configures the find method of the mocked DAO to raise an Exception when called
        uc = UserController(dao=mocked_dao)

        with pytest.raises(Exception):
            uc.get_user_by_email(valid_email) #This context manager asserts that the code block within it raises an Exception. If the expected exception is not raised, the test will fail.

    @pytest.mark.usercontroller
    def test_get_user_by_email_first_in_list_2(self, sut_multiple_user, valid_email):
        """
        Test case 2: Valid email associated to multiple users
        Email  associated with user: TRUE
        Multiple Users: TRUE
        Email is Valid: TRUE
        Database Operation Fails: FALSE
        Outcome: User object (first in list); Print warning
        """
        # return the first one and print a warning message containing the email address
        user = sut_multiple_user.get_user_by_email(valid_email)
        assert user == {'firstName': 'test1_first', 'lastName': 'test1_last', 'email': 'test@test.com'}

    @pytest.mark.usercontroller
    def test_get_user_by_email_print_error_2(self, sut_multiple_user, capfd, valid_email):
        """
        Test case 2: Valid email associated to multiple users
        Email  associated with user: TRUE
        Multiple Users: TRUE
        Email is Valid: TRUE
        Database Operation Fails: FALSE
        Outcome: User object (first in list); Print warning
        """
        # print a warning message containing the email address
        sut_multiple_user.get_user_by_email(valid_email)
        # Check if the warning message is printed
        out, err = capfd.readouterr()
        assert valid_email in out

    @pytest.mark.usercontroller
    def test_get_user_by_email_3(self, sut_single_user, invalid_email):
        """
        Test case 3: Email is not valid
        Email associated with user: Not applicable
        Multiple Users: Not applicable
        Email is Valid: FALSE
        Database Operation Fails: Not applicable
        Outcome: ValueError
        """
        with pytest.raises(ValueError):
            sut_single_user.get_user_by_email(invalid_email)

    @pytest.mark.usercontroller
    def test_get_user_by_email_4(self, sut_single_user, valid_email):
        """
        Test case 4: Valid email associated with one user
        Email  associated with user: TRUE
        Multiple Users: FALSE
        Email is Valid: TRUE
        Database Operation Fails: FALSE
        Outcome: User object
        """
        user = sut_single_user.get_user_by_email(valid_email)
        assert user == {'firstName': 'test1_first', 'lastName': 'test1_last', 'email': 'test@test.com'}

    @pytest.mark.usercontroller
    def test_get_user_by_email_5(self, other_email):
        """
        Test case 5: Valid email not associated with any user
        Email  associated with user: FALSE
        Multiple Users: FALSE
        Email is Valid: TRUE
        Database Operation Fails: FALSE
        Outcome: None
        """
        mocked_dao = MagicMock()
        mocked_dao.find.return_value = []
        uc = UserController(dao=mocked_dao)
        user = uc.get_user_by_email(other_email)
        assert user == None

    # @pytest.fixture
    # def sut(self, email: str):
    #     """
    #     Fixture function that creates and returns an instance of the UserController class.

    #     Parameters:
    #     - email (str): The email address used to retrieve list with users from the email_ dictionary.

    #     Returns:
    #     - uc (UserController): An instance of the UserController class with a mocked DAO object.

    #     """
    #     email_ = {
    #         'foo@bar.com': [],
    #         'test@test.com' : [
    #             {'firstName': 'test1_first', 'lastName': 'test1_last', 'email': 'test@test.com'},
    #             {'firstName': 'test2_first', 'lastName': 'test2_last', 'email': 'test@test.com'}
    #         ],
    #         'one@one.com' : [
    #             {'firstName': 'test_one', 'lastName': 'test_one', 'email': 'one@one.com'},
    #         ]
    #     }
    #     matched_users = email_[email]
    #     mocked_dao = MagicMock()
    #     # This configures the find method of the mocked DAO to return a list containing user objects
    #     mocked_dao.find.return_value = matched_users
    #     uc = UserController(dao=mocked_dao)
    #     return uc

    # @pytest.mark.usercontroller
    # @pytest.mark.parametrize('email, expected', [
    #     ('foo@bar.com', None),
    #     ('test@test.com', {'firstName': 'test1_first', 'lastName': 'test1_last', 'email': 'test@test.com'}),
    #     ('one@one.com', {'firstName': 'test_one', 'lastName': 'test_one', 'email': 'one@one.com'})
    #     ])
    # def test_get_user_by_email(self, sut, email, expected):
    #     result = sut.get_user_by_email(email=email)
    #     assert result == expected