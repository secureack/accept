import pytest
import time

import classes.processor
import core.globalSettings

def test_processor():
    processor_instance = classes.processor.processor(id="test_processor")
    assert processor_instance.id == "test_processor"
    assert hasattr(processor_instance, 'logger')
    assert hasattr(processor_instance, 'next')

def test_processHandler():
    processor_instance = classes.processor.processor(id="test_processor", next=[])
    event = {"data": "test_event"}
    stack = ["test_stack"]
    
    processor_instance.processHandler(event, stack)

    # Check if processStats were updated
    stats = processor_instance.processStats()
    assert stats["events"]["count"] == 1
    assert stats["time"]["total"] > 0
    assert stats["time"]["last"] > 0
    assert stats["time"]["first"] > 0

def test_process():
    processor_instance = classes.processor.processor(id="test_processor")
    event = {"data": "test_event"}
    
    # This should not raise an error
    processed_event = processor_instance.process(event)
    
    # Check if the event is returned unchanged
    assert processed_event == event
    
    # Check if processStats were not updated
    stats = processor_instance.processStats()
    assert stats["events"]["count"] == 0
    assert stats["time"]["total"] == 0
    assert stats["time"]["last"] == 0
    assert stats["time"]["first"] == 0