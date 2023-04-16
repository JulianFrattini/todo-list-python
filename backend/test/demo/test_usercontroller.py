import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController

@pytest.mark.task2

def test_get_user_by_email_connection_success_valid_one_match():
    mocked_doa = mock.MagicMock()
    mocked_doa.find.return_value = [{ "name":"alex", "email":"alex@gmail.com"}]
    sut = UserController(dao=mocked_doa)

    result = sut.get_user_by_email("alex@gmail.com")
    assert result == {"name":"alex","email": "alex@gmail.com"}
    
@pytest.mark.task2

def test_get_user_by_email_connection_success_valid_multiple_match():
    mocked_doa = mock.MagicMock()
    mocked_doa.find.return_value = [{"name":"alex", "email":"alex@gmail.com"},{ "name":"chelsea", "email":"alex@gmail.com"}]
    sut = UserController(dao=mocked_doa)

    result = sut.get_user_by_email("alex@gmail.com")
    assert result == {"name":"alex","email": "alex@gmail.com"}
    
    
@pytest.mark.task2

def test_get_user_by_email_connection_success_valid_no_match():
    mocked_doa = mock.MagicMock()
    mocked_doa.find.return_value = []
    sut = UserController(dao=mocked_doa)

    result = sut.get_user_by_email("alex@gmail.com")
    assert result == None
    
    
    
@pytest.mark.task2
def test_get_user_by_email_connection_success_invalid_no_match():
    mocked_doa = mock.MagicMock()
    mocked_doa.find.return_value = []
    sut = UserController(dao=mocked_doa)

    with pytest.raises(ValueError) as e:
        sut.get_user_by_email("alex#gmailcom")

    assert str(e.value) == "Error: invalid email address"


@pytest.mark.task2
def test_get_user_by_email_connection_fails():
    mocked_doa = mock.MagicMock()
    mocked_doa.find.side_effect = Exception("connection to database failed")
    sut = UserController(dao=mocked_doa)

    with pytest.raises(Exception) as e:
        sut.get_user_by_email("alex@gmail.com")

    assert str(e.value) == "connection to database failed"