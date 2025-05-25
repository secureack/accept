import pytest

import core.objectCache

def test_objectCache():
    # Test adding an object to the cache
    core.objectCache.objectCache['test_key'] = 'test_value'
    assert core.objectCache.objectCache['test_key'] == 'test_value'

    # Test retrieving an object from the cache
    assert core.objectCache.objectCache.get('test_key') == 'test_value'

    # Test checking if a key exists in the cache
    assert 'test_key' in core.objectCache.objectCache

    # Test removing an object from the cache
    del core.objectCache.objectCache['test_key']
    assert 'test_key' not in core.objectCache.objectCache

    # Test clearing the cache
    core.objectCache.objectCache['another_key'] = 'another_value'
    core.objectCache.objectCache.clear()
    assert len(core.objectCache.objectCache) == 0