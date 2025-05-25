import pytest

import core.logic

def test_if_eval_basic():
    assert core.logic.ifEval("if 1 == 1") is True
    assert core.logic.ifEval("if 1 == 2") is False
    assert core.logic.ifEval("if \"a\" in [\"a\", \"b\"]") is True
    assert core.logic.ifEval("if \"abc\" == 1 or 1 == 1") is True
    assert core.logic.ifEval("if \"abc\" == 1 and 1 == 1") is False
    assert core.logic.ifEval("if 1 == 1 and ( 2 == 2 or 3 == 3 )") is True
    assert core.logic.ifEval("if 1 == 1 and ( 2 == 2 and 3 == 4 )") is False
    assert core.logic.ifEval("if 1 != 2") is True
    assert core.logic.ifEval("if 1 != 1") is False
    assert core.logic.ifEval("if 1 < 2") is True
    assert core.logic.ifEval("if 2 < 1") is False
    assert core.logic.ifEval("if 1 <= 1") is True
    assert core.logic.ifEval("if 2 >= 1") is True
    assert core.logic.ifEval("if 1 > 0") is True
    assert core.logic.ifEval("if \"test\" not in \"abc\"") is True
    assert core.logic.ifEval("if \"test\" in \"test\"") is True
    assert core.logic.ifEval("if test match \".*\"") is True
    assert core.logic.ifEval("if test not match \".*\"") is False

def test_if_eval_eventData():
    assert core.logic.ifEval("if 1 == \"1\"") is False
    assert core.logic.ifEval("if event[test] == 1",{ "event" : { "test" :  1 } }) is True

def test_if_eval_function():
    import core.functions
    def testFunction():
        return "testFunction"
    core.functions.available["test"] = testFunction
    assert core.logic.ifEval("if test() == \"testFunction\"") is True