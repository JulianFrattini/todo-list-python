import pytest
from src.util.helpers import hasAttribute

@pytest.fixture
def obj():
    return {'name': 'Jane'}

def test_hasAttribute_true(obj):
    result = hasAttribute(obj, 'name')
    assert result == True

def test_hasAttribute_false(obj):
    result = hasAttribute(obj, 'email')
    assert result == False

def test_hasAttribute_None():
    obj = None
    result = hasAttribute(obj, 'name')
    assert result == False

