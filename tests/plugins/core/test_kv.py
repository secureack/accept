import pytest

from plugins.core.processor.kv import kv

def test_kv():
    # Test with default separator and spaced
    processor = kv()
    event = 'key1=value1 key2=value2'
    expected = {'key1': 'value1', 'key2': 'value2'}
    assert processor.process(event) == expected

    # Test with custom separator
    processor = kv(separator=':')
    event = 'key1:value1 key2:value2'
    expected = {'key1': 'value1', 'key2': 'value2'}
    assert processor.process(event) == expected

    # Test with spaced characters
    processor = kv(spaced=',')
    event = 'key1=value1,key2=value2'
    expected = {'key1': 'value1', 'key2': 'value2'}
    assert processor.process(event) == expected