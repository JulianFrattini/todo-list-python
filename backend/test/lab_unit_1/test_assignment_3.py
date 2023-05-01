import pytest
import unittest.mock as mock
from unittest.mock import patch
from src.util.dao import DAO

def test_create():

    # with patch('pymongo.MongoClient') as dao_init_mock:
    #     dao_init_mock.side_effect = lambda self: print("HALLOJ")
        # dao_init_mock.assert_called_once_with(dao)


        # mock av data
        # callar init med mock
        # callar create med mock

    dao = DAO("test")