import pytest

from plugins.core.processor.inject import inject

def test_inject():
    processor = inject(inject={
        'field1': 'value1',
        'field2': {'if 1 == 1': 'value2', 'default': 'default_value'},
        'field3': {'if 1 == 2': 'value3', 'default': 'default_value3'}
    })

    # Mock event
    event = {}

    # Test injecting simple value
    result = processor.process(event)
    assert result['field1'] == 'value1'

    # Test injecting with condition
    result = processor.process(event)
    assert result['field2'] == 'value2'

    # Test default value injection
    result = processor.process(event)
    assert result['field3'] == 'default_value3'

