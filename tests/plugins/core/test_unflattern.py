import pytest

from plugins.core.processor.unflatten import unflatten

def test_unflatten():
    processor = unflatten()

    # Test with a flat dictionary
    flat_event = {
        'a.b.c': 1,
        'a.b.d': 2,
        'e': 3
    }
    expected_unflattened_event = {
        'a': {
            'b': {
                'c': 1,
                'd': 2
            }
        },
        'e': 3
    }
    assert processor.process(flat_event) == expected_unflattened_event