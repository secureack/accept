import pytest

from plugins.core.processor.lowercase import lowercase

def test_lowercase():
    # Create an instance of the lowercase processor
    processor = lowercase(fields=['field1', 'field2'])

    # Create a sample event
    event = {
        'field1': 'Hello World',
        'field2': 'ACCEPT',
        'field3': 'Ignore this field'
    }

    # Process the event
    processed_event = processor.process(event)

    # Check that the specified fields are lowercased
    assert processed_event['field1'] == 'hello world'
    assert processed_event['field2'] == 'accept'

    # Check that other fields remain unchanged
    assert processed_event['field3'] == 'Ignore this field'