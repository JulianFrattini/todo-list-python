import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController

@pytest.fixture
def sut(DAOreturn: list):
    mockeDAO = mock.MagicMock()
    mockeDAO.find.return_value = DAOreturn
    mockedsut = UserController(dao=mockeDAO)
    return mockedsut

@pytest.mark.email
@pytest.mark.parametrize('mail, DAOreturn, expected', [('jane.doe@gmail.com', [{'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe@gmail.com'}], {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe@gmail.com'}),
                                                        ('jane.doe@gmail.com', [{}], {}),
                                                        ('jane.doe@gmail.com', [{'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe@gmail.com'}, {'firstName': 'Jane2', 'lastName': 'Doe2', 'email': 'jane.doe@gmail.com'}], {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe@gmail.com'}),
                                            ])
def test_validateAge(sut, mail, DAOreturn, expected):
    validationresult = sut.get_user_by_email(email=mail)
    print(validationresult)
    assert validationresult == expected 