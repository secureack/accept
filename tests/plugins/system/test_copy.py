import pytest

from plugins.system.processor.copy import copy

def test_copy():
    # Create an instance of the copy processor
    processor = copy()

    # Define a sample event
    event = {
        "id": 1,
        "name": "Test Event",
        "data": {
            "value": 42
        }
    }

    # Process the event using the copy processor
    result = processor.process(event)

    # Assert that the result is a deep copy of the original event
    assert result == event
    assert result is not event  # Ensure it's a different object
    assert result["data"] is not event["data"]  # Ensure nested data is also copied