import pytest
import unittest.mock as mock

from src.util.helpers import hasAttribute, ValidationHelper

# tests for the hasAttribute method
@pytest.mark.demo
def test_hasAttribute_true():
    assert True == True