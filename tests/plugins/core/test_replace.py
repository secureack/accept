import pytest

from plugins.core.processor.replace import replace

def test_replace():
    # Create an instance of the replace processor
    processor = replace(field='message', find='old', value='new')

    # Create a sample event
    event = {
        'message': 'This is an old message with old content.',
        'otherField': 'some value'
    }

    # Process the event
    processed_event = processor.process(event)

    # Check that the specified field has been replaced correctly
    assert processed_event['message'] == 'This is an new message with new content.'

    # Check that other fields remain unchanged
    assert processed_event['otherField'] == 'some value'