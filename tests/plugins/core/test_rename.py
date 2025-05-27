import pytest

from plugins.core.processor.rename import rename

def test_rename():
    # Create an instance of the rename processor
    processor = rename(rename={'oldField1': 'newField1', 'oldField2': 'newField2'})

    # Create a sample event
    event = {
        'oldField1': 'value1',
        'oldField2': 'value2',
        'unrelatedField': 'unrelatedValue'
    }

    # Process the event
    processed_event = processor.process(event)

    # Check that the specified fields are renamed
    assert 'newField1' in processed_event
    assert processed_event['newField1'] == 'value1'
    assert 'newField2' in processed_event
    assert processed_event['newField2'] == 'value2'

    # Check that the old fields are removed
    assert 'oldField1' not in processed_event
    assert 'oldField2' not in processed_event

    # Check that other fields remain unchanged
    assert processed_event['unrelatedField'] == 'unrelatedValue'

def test_rename_preserve():
    # Create an instance of the rename processor
    processor = rename(rename={'oldField1': 'newField1', 'oldField2': 'newField2'},preserve=True)

    # Create a sample event
    event = {
        'oldField1': 'value1',
        'oldField2': 'value2',
        'unrelatedField': 'unrelatedValue'
    }

    # Process the event
    processed_event = processor.process(event)

    assert 'newField1' in processed_event
    assert processed_event['newField1'] == 'value1'
    assert 'newField2' in processed_event
    assert processed_event['newField2'] == 'value2'
    assert processed_event['unrelatedField'] == 'unrelatedValue'
    # Check that the old fields are still present
    assert 'oldField1' in processed_event
    assert processed_event['oldField1'] == 'value1'
    assert 'oldField2' in processed_event
    assert processed_event['oldField2'] == 'value2'

