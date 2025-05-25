import pytest

import core.functions

def test_available_functions():
    def testFunction():
        return "testFunction"
    core.functions.available["test"] = testFunction
    assert core.functions.available["test"]() == "testFunction"