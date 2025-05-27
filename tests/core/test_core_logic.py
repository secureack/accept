import pytest

import core.logic

def test_legacy_if_eval_basic():
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
    assert core.logic.ifEval("if (1 == 2) or (1 == 2 or 2 == 2)") is True
    assert core.logic.ifEval("if (1 == 2) and (1 == 2 and 2 == 2)") is False
    assert core.logic.ifEval("if (1 == 2) or (1 == 2 and 2 == 2)") is False
    assert core.logic.ifEval("if (1 == 1) and (1 == 2 or 2 == 2)") is True
    assert core.logic.ifEval("if (1 == 2) or (1 == 1 and 2 == 2)") is True
    assert core.logic.ifEval("if (1 == 1) and (1 == 2 or 2 == 1)") is False

def test_legacy_if_eval_eventData():
    assert core.logic.ifEval("if 1 == \"1\"") is False
    assert core.logic.ifEval("if event[test] == 1",{ "event" : { "test" :  1 } }) is True

def test_legacy_if_eval_function():
    import core.functions
    def testFunction():
        return "testFunction"
    core.functions.available["test"] = testFunction
    assert core.logic.ifEval("if test() == \"testFunction\"") is True

def test_if_eval_basic():
    assert core.logic.ifEval({"logic": []}) is False
    assert core.logic.ifEval({"logic": [["1", "===", "1"]]}) is False
    assert core.logic.ifEval({"logic": [["1", "==", "1"]]}) is True
    assert core.logic.ifEval({"logic": [["1", "==", "2"]]}) is False
    assert core.logic.ifEval({"logic": [["a", "in", ["a", "b"]]]}) is True
    assert core.logic.ifEval({'logic': [{'and': [["1", '==', "1"], {'or': [["2", '==', "2"], ["3", '==', "3"]]}]}]}) is True
    assert core.logic.ifEval({'logic': [{'and': [["1", '==', "1"], {'and': [["2", '==', "2"], ["3", '==', "4"]]}]}]}) is False
    assert core.logic.ifEval({"logic": [["1", "!=", "2"]]}) is True
    assert core.logic.ifEval({"logic": [["1", "!=", "1"]]}) is False
    assert core.logic.ifEval({"logic": [["1", "<", "2"]]}) is True
    assert core.logic.ifEval({"logic": [["2", "<", "1"]]}) is False
    assert core.logic.ifEval({"logic": [["1", "<=", "1"]]}) is True
    assert core.logic.ifEval({"logic": [["2", ">=", "1"]]}) is True
    assert core.logic.ifEval({"logic": [["1", ">", "0"]]}) is True
    assert core.logic.ifEval({"logic": [["test", "not in", "abc"]]}) is True
    assert core.logic.ifEval({"logic": [["test", "in", "test"]]}) is True
    assert core.logic.ifEval({"logic": [["test", "match", ".*"]]}) is True
    assert core.logic.ifEval({"logic": [["test", "not match", ".*"]]}) is False
    assert core.logic.ifEval({"logic": [{'or': [["1", "==", "2"], {'or': [["1", "==", "2"], ["2", "==", "2"]]}]}]}) is True
    assert core.logic.ifEval({"logic": [{'and': [["1", "==", "2"], {'and': [["1", "==", "2"], ["2", "==", "2"]]}]}]}) is False
    assert core.logic.ifEval({"logic": [{'or': [["1", "==", "2"], {'and': [["1", "==", "2"], ["2", "==", "2"]]}]}]}) is False
    assert core.logic.ifEval({"logic": [{'and': [["1", "==", "1"], {'or': [["1", "==", "2"], ["2", "==", "2"]]}]}]}) is True
    assert core.logic.ifEval({"logic": [{'or': [["1", "==", "2"], {'and': [["1", "==", "1"], ["2", "==", "2"]]}]}]}) is True
    assert core.logic.ifEval({"logic": [{'and': [["1", "==", "1"], {'or': [["1", "==", "2"], ["2", "==", "1"]]}]}]}) is False


def test_if_eval_eventData():
    assert core.logic.ifEval({"logic": [['1', '==', '"1"']]}, {"event": {}}) is False
    assert core.logic.ifEval({"logic": [["event[test]", "==", "1"]]}, {"event": {"test": 1}}) is True
    assert core.logic.ifEval({"logic": [["event[test]", "==", "2"]]}, {"event": {"test": 1}}) is False

def test_if_eval_function():
    import core.functions
    def testFunction():
        return "testFunction"
    core.functions.available["test"] = testFunction
    assert core.logic.ifEval({"logic": [["test()", "==", "testFunction"]]}) is True
