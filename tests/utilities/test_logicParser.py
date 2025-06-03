import pytest

import utilities.logicParser

def test_logic_parser():
    assert utilities.logicParser.parse("if 1 == 1") == {
        "logic": [
            ["1", "==", "1"]
        ]
    }
    assert utilities.logicParser.parse("if 1 != 2") == {
        "logic": [
            ["1", "!=", "2"]
        ]
    }
    assert utilities.logicParser.parse("if 1 == 1 or (2 == 2 and 3 == 3)") == {
        "logic": [
            {
                "or": [
                    ["1", "==", "1"],
                    {
                        "and": [
                            ["2", "==", "2"],
                            ["3", "==", "3"]
                        ]
                    }
                ]
            }
        ]
    }
    assert utilities.logicParser.parse("if 1 == 1 and (2 == 2 or 3 == 3)") == {
        "logic": [
            {
                "and": [
                    ["1", "==", "1"],
                    {
                        "or": [
                            ["2", "==", "2"],
                            ["3", "==", "3"]
                        ]
                    }
                ]
            }
        ]
    }
    assert utilities.logicParser.parse("if data[event][test] == test") == {
        "logic": [
            ["data[event][test]", "==", "test"]
        ]
    }
    assert utilities.logicParser.parse("if testFunction() == test") == {
        "logic": [
            ["testFunction()", "==", "test"]
        ]
    }
    assert utilities.logicParser.parse("if (1 == 1 or (2 == 2 and 3 == 3)) and (4 == 4 or 5 == 5)") == {
        "logic": [
            {
                "and": [
                    {
                        "or": [
                            ["1", "==", "1"],
                            {
                                "and": [
                                    ["2", "==", "2"],
                                    ["3", "==", "3"]
                                ]
                            }
                        ]
                    },
                    {
                        "or": [
                            ["4", "==", "4"],
                            ["5", "==", "5"]
                        ]
                    }
                ]
            }
        ]
    }
    with pytest.raises(ValueError):
        utilities.logicParser.parse("if 1 == 1 2 == 2")
