import pytest

from plugins.core.processor.stringEvent import stringEvent

def test_stringEvent():
    processor = stringEvent(field='message')

    # Test with a simple string
    event = {'message': 'Hello, World!'}
    processed_event = processor.process(event)
    assert processed_event['message'] == "'Hello, World!'"

    # Test with a dictionary
    event = {'message': {'key': 'value'}}
    processed_event = processor.process(event)
    assert processed_event['message'] == "'{\"key\": \"value\"}'"