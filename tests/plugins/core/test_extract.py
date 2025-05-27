import pytest

from plugins.core.processor.extract import extract

def test_extract():
    event = {'message': 'This is a test message'}
    processor = extract(field='message', regex='(?P<test>test)', regexExtractGroup="test")
    result = processor.process(event)
    assert result == { "test" : "test" }

    event = {'message': 'This is a test message'}
    processor = extract(field='message', regex='(?P<test>test)', regexExtractGroup="test", outputField="test")
    result = processor.process(event)
    assert result == { "message": "This is a test message", "test" : { "test" :  "test" } }

    event = {'message': 'This is a test message' }
    processor = extract(field='message', regex='(?P<test>test)', merge=True)
    result = processor.process(event)
    assert result == { "message": "This is a test message", "test" : "test" }

