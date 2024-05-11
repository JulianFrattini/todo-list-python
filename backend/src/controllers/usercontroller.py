from src.controllers.controller import Controller
from src.util.dao import DAO

import re
# https://stackoverflow.com/questions/201323/how-can-i-validate-an-email-address-using-a-regular-expression
emailValidator = re.compile(r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])')

class UserController(Controller):
    def __init__(self, dao: DAO):
        super().__init__(dao=dao)

    def get_user_by_email(self, email: str):
        """Given a valid email address of an existing account, return the user object contained in the database associated
        to that user. For now, do not assume that the email attribute is unique. Additionally print a warning message containing the email
        address if the search returns multiple users.

        parameters:
            email -- an email address string

        returns:
            user -- the user object associated to that email address (if multiple users are associated to that email: return the first one)
            None -- if no user is associated to that email address

        raises:
            ValueError -- in case the email parameter is not valid (i.e., conforming <local-part>@<domain>.<host>)
            Exception -- in case any database operation fails
        """

        if not re.fullmatch(emailValidator, email):
            raise ValueError('Error: invalid email address')

        try:
            users = self.dao.find({'email': email})
            if len(users) == 1:
                return users[0]
            elif len(users) > 1:
                print(f'Error: more than one user found with mail {email}')
                return users[0]
            else:
                print(f'Error: no user found with mail {email}')
                return None
        except Exception as e:
            raise

    def update(self, id, data):
        try:
            update_result = super().update(id=id, data={'$set': data})
            return update_result
        except Exception as e:
            raise