import pytest

from plugins.core.processor.blacklist import blacklist

def test_blacklist():
    # Initialize the blacklist processor with some fields
    processor = blacklist(blacklist=['field1', 'field2*'])

    # Create a sample event
    event = {
        'field1': 'value1',
        'field2': 'value2',
        'field3': 'value3',
        'field4': 'value4'
    }

    # Process the event
    processed_event = processor.process(event)

    # Check that field1 and field2 are removed, but field3 and field4 remain
    assert 'field1' not in processed_event
    assert 'field2' not in processed_event
    assert 'field3' in processed_event
    assert 'field4' in processed_event