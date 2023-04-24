import pytest
import unittest.mock as mock
from unittest.mock import patch
from pymongo import MongoClient
from src.util.dao import DAO
# from dao.py
import os
import pymongo
from dotenv import dotenv_values
# create a data access object
from src.util.validators import getValidator
import json
from bson import json_util
from bson.objectid import ObjectId

@pytest.fixture
def test_DAO_class_constructor():
    mockedDAO = mock.MagicMock()

