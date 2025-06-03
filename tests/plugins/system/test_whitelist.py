import pytest

from plugins.system.processor.whitelist import whitelist

def test_whitelist():
    # Initialize the whitelist processor with a set of fields
    processor = whitelist(whitelist=["field1", "field2", "field3*"])

    # Create an event with multiple fields
    event = {
        "field1": "value1",
        "field2": "value2",
        "field3_extra": "value3",
        "field4": "value4"
    }

    # Process the event
    processed_event = processor.process(event)

    # Check that only whitelisted fields are present in the processed event
    assert processed_event == {
        "field1": "value1",
        "field2": "value2",
        "field3_extra": "value3"
    }