import pytest
import unittest.mock as mock #Load the mocking library

from src.controllers.usercontroller import UserController

# tests for the get_user_by_email() method
# (1) test cases for email address being invalid and valid
@pytest.mark.unit
def test_get_user_by_email_no_local_part():
    #Arrange
    obj = "@y.z"
    mockedusercontroller = mock.MagicMock() #Mock the dependency
    sut = UserController(mockedusercontroller) #Inject the dependency

    #Assert
    with pytest.raises(ValueError):
        sut.get_user_by_email(obj) #Act
        
@pytest.mark.unit
def test_get_user_by_email_no_at_sign():
    #Arrange
    obj = "xy.z"
    mockedusercontroller = mock.MagicMock() #Mock the dependency
    sut = UserController(mockedusercontroller) #Inject the dependency

    #Assert
    with pytest.raises(ValueError):
        sut.get_user_by_email(obj) #Act

@pytest.mark.unit
def test_get_user_by_email_no_domain():
    #Arrange
    obj = "x@.z"
    mockedusercontroller = mock.MagicMock() #Mock the dependency
    sut = UserController(mockedusercontroller) #Inject the dependency

    #Assert
    with pytest.raises(ValueError):
        sut.get_user_by_email(obj) #Act

@pytest.mark.unit
def test_get_user_by_email_no_dot_between_domain_host():
    #Arrange
    obj = "x@yz"
    mockedusercontroller = mock.MagicMock() #Mock the dependency
    sut = UserController(mockedusercontroller) #Inject the dependency

    #Assert
    with pytest.raises(ValueError):
        sut.get_user_by_email(obj) #Act

@pytest.mark.unit
def test_get_user_by_email_no_host():
    #Arrange
    obj = "x@y."
    mockedusercontroller = mock.MagicMock() #Mock the dependency
    sut = UserController(mockedusercontroller) #Inject the dependency

    #Assert
    with pytest.raises(ValueError):
        sut.get_user_by_email(obj) #Act



# (2) email address is valid, database raises Exception
@pytest.mark.unit
def test_get_user_by_email_exception():
    #Arrange
    obj = 'x@y.z'
    mockedusercontroller = mock.MagicMock()
    mockedusercontroller.find.side_effect = Exception()
    sut = UserController(mockedusercontroller)

    #Assert
    with pytest.raises(Exception):
        sut.get_user_by_email(obj) #Act

# (3) email address is valid, database raises no Exception, number of users is 0
@pytest.mark.unit
def test_get_user_by_email_none():
    #Arrange
    obj = 'x@y.z'
    mockedusercontroller = mock.MagicMock()
    mockedusercontroller.get.return_value = None
    sut = UserController(mockedusercontroller)

    #Act
    result = sut.get_user_by_email(obj)

    #Assert
    assert result is None


# (4) email address is valid, database raises no Exception, number of users is 1
@pytest.mark.unit
def test_get_user_by_email_correct():
    #Arrange
    email = 'x@y.z'
    user1 = {'id': 1, 'name': "correct", 'email': email}
    mockedusercontroller = mock.MagicMock()
    mockedusercontroller.find.return_value = [user1]
    sut = UserController(mockedusercontroller)

    #Act
    result = sut.get_user_by_email(email)

    #Assert
    assert result == user1



# (5) email address is valid, database raises no Exception, number of users is multiple, raises warning message
@pytest.mark.unit
def test_get_user_by_email_warning():
    #Arrange
    email = "x@y.z"
    user1 = {'id': 1, 'name': 'correct', 'email': email}
    user2 = {'id': 2, 'name': 'incorrect', 'email': email}
    mockedusercontroller = mock.MagicMock()
    mockedusercontroller.find.return_value = [user1, user2]
    sut = UserController(mockedusercontroller)

    #Act
    result = sut.get_user_by_email(email)

    #Assert
    assert mockedusercontroller.find.called


# (6) email address is valid, database raises no Exception, number of users is multiple, returns first user
@pytest.mark.unit
def test_get_user_by_email_return_first_user():
    #Arrange
    email = "x@y.z"
    user1 = {'id': 1, 'name': 'correct', 'email': email}
    user2 = {'id': 2, 'name': 'incorrect', 'email': email}
    mockedusercontroller = mock.MagicMock()
    mockedusercontroller.find.return_value = [user1, user2]
    sut = UserController(mockedusercontroller)

    #Act
    result = sut.get_user_by_email(email)

    #Assert
    assert result == user1