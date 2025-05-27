import pytest

from plugins.core.processor.toJson import toJson


def test_loadJson():
    # Test with a simple JSON string
    processor = toJson(field='json_data', outputField='output_data')
    event = {'json_data': '{"key": "value"}'}
    result = processor.process(event)
    assert result['output_data'] == {'key': 'value'}

    # Test with a JSON string containing nested objects
    event = {'json_data': '{"outer": {"inner": "value"}}'}
    result = processor.process(event)
    assert result['output_data'] == {'outer' : { 'inner': 'value'} }