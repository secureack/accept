import pytest

from plugins.core.processor.decode import decode

def test_decode():
    # Initialize the decode processor with a specific field and decode method
    processor = decode(field='message', decode='unicode_escape')
    # Create a sample event with a field that needs decoding
    event = {
        'message': 'Hello\\nWorld'
    }
    # Process the event
    processed_event = processor.process(event)
    # Check if the field has been decoded correctly
    assert processed_event['message'] == 'Hello\nWorld'


