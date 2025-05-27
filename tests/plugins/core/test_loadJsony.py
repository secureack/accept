import pytest

from plugins.core.processor.loadJson import loadJson


def test_loadJson():
    # Test with a simple JSON string
    processor = loadJson(field='json_data', outputField='output_data')
    event = {'json_data': '{"key": "value"}'}
    result = processor.process(event)
    assert result['output_data'] == {'key': 'value'}

    # Test with a JSON string containing nested objects
    event = {'json_data': '{"outer": {"inner": "value"}}'}
    result = processor.process(event)
    assert result['output_data'] == {'outer.inner': 'value'}

    # Test with a malformed JSON string
    event = {'json_data': '{"key": "value"'}
    result = processor.process(event)
    assert result['output_data'] == {'decode_error': '{"key": "value"'}

    # Test with single quote support
    processor = loadJson(field='json_data', outputField='output_data', singleQuoteSupport=True)
    event = {'json_data': "{'key': 'value'}"}
    result = processor.process(event)
    assert result['output_data'] == {'key': 'value'}