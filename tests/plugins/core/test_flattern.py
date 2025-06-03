import pytest

from plugins.core.processor.flatten import flatten

def test_flatten():
    processor = flatten()

    # Test with a nested dictionary
    event = {
        'a': 1,
        'b': {
            'c': 2,
            'd': {
                'e': 3
            }
        },
        'f': 4
    }
    
    expected = {
        'a': 1,
        'b.c': 2,
        'b.d.e': 3,
        'f': 4
    }
    
    result = processor.process(event)
    assert result == expected

    # Test with a flat dictionary
    event = {
        'x': 10,
        'y': 20
    }
    
    result = processor.process(event)
    assert result == event

    # Test with an empty dictionary
    event = {}
    
    result = processor.process(event)
    assert result == {}

