from src.controllers.usercontroller import UserController
from src.util.dao import DAO
import random

def hasAttribute(obj: dict, attribute: str):
    """Check whether a given dict contains a specific attribute

    attributes:
        obj -- a dict object
        attribute -- the key which potentially occurs in the obj dict

    returns:
        True -- if the dict contains the attribute as a key
        False -- if the dict does not contain the attribute as a key or is None    
    """
    return (attribute in obj)

class ValidationHelper:
    def __init__(self, usercontroller: UserController):
        self.usercontroller = usercontroller

    def validateAge(self, userid: str):
        """Validate the age of a given user

        attributes:
            userid -- string id of the user object

        returns:
            "invalid" -- if the age is below 0 or above 120
            "valid" -- if the user is of age
            "underaged" -- otherwise
        """
        user = self.usercontroller.get(id=userid)

        if user['age'] < 0 or user['age'] > 120:
            return "invalid"
        if user['age'] > 18:
            return "valid"
        return "underaged"

class ValidationHelper2:
    def __init__(self):
        """Similar behavior to ValidationHelper, but this time the dependency is hard-coded and cannot be injected.
        """
        self.usercontroller = UserController(dao=DAO(collection_name='user'))

    def validateAge(self, userid: str):
        """Validate the age of a given user

        attributes:
            userid -- string id of the user object

        returns:
            "invalid" -- if the age is below 0 or above 120
            "valid" -- if the user is of age
            "underaged" -- otherwise
        """
        user = self.usercontroller.get(id=userid)

        if user['age'] < 0 or user['age'] > 120:
            return "invalid"
        if user['age'] > 18:
            return "valid"
        return "underaged"

def diceroll():
    """Roll a simple six sided die and see if you win.

    returns:
        True -- if the rolled number is higher than a 4
        False -- else
    """
    number = random.randint(1, 6)

    if number >= 4:
        return True
    return False