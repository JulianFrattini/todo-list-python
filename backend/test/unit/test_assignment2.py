import pytest
import unittest.mock as mock #Load the mocking library

from src.controllers.usercontroller import UserController

# tests for the get_user_by_email() method
@pytest.mark.unit
def test_get_user_by_email_valuerror():
    #Arrange
    obj = "emailemail.com"
    mockedusercontroller = mock.MagicMock() #Mock the dependency
    sut = UserController(mockedusercontroller) #Inject the dependency

    #Assert
    with pytest.raises(ValueError):
        sut.get_user_by_email(obj) #Act

@pytest.mark.unit
def test_get_user_by_email_exception():
    #Arrange
    obj = 'email@email.com'
    mockedusercontroller = mock.MagicMock()
    mockedusercontroller.find.side_effect = Exception()
    sut = UserController(mockedusercontroller)

    #Assert
    with pytest.raises(Exception):
        sut.get_user_by_email(obj) #Act

@pytest.mark.unit
def test_get_user_by_email_none():
    #Arrange
    obj = 'email@email.com'
    mockedusercontroller = mock.MagicMock()
    mockedusercontroller.get.return_value = None
    sut = UserController(mockedusercontroller)

    #Act
    result = sut.get_user_by_email(obj)

    #Assert
    assert result is None

@pytest.mark.unit
def test_get_user_by_email():
    #Arrange
    email = 'email@email.com'
    user1 = {'id': 1, 'name': "correct", 'email': email}
    mockedusercontroller = mock.MagicMock()
    mockedusercontroller.find.return_value = [user1]
    sut = UserController(mockedusercontroller)

    #Act
    result = sut.get_user_by_email(email)

    #Assert
    assert result == user1

@pytest.mark.unit
def test_get_user_by_email_warning():
    #Arrange
    email = "correct@email.com"
    user1 = {'id': 1, 'name': 'correct', 'email': email}
    user2 = {'id': 2, 'name': 'incorrect', 'email': email}
    mockedusercontroller = mock.MagicMock()
    mockedusercontroller.find.return_value = [user1, user2]
    sut = UserController(mockedusercontroller)

    #Act
    result = sut.get_user_by_email(email)

    #Assert
    assert result == user1
    assert mockedusercontroller.find.called