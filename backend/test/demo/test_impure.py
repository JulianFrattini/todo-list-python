import pytest
import random
from unittest.mock import patch

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

@pytest.mark.demo
@pytest.mark.parametrize('value, expected', [(4, False), (5, True), (6, True)])
def test_diceroll_success(value, expected):
    with patch('random.randint') as mockrandint:
        mockrandint.return_value = value
        assert diceroll() == expected