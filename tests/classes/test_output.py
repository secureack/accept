import pytest
import time

import classes.output
import core.globalSettings

def test_output():
    output = classes.output.output(id="test_output")
    assert output.id == "test_output"
    assert hasattr(output, 'logger')
    assert hasattr(output, 'trace')

def test_processHandler():
    output = classes.output.output(id="test_output", trace=True)
    event = {"data": "test_event"}
    stack = ["test_stack"]
    
    output.processHandler(event, stack)
    
    assert "__accept__" in event
    assert "trace" in event["__accept__"]
    assert event["__accept__"]["trace"] == stack
    
    # Check if processStats were updated
    stats = output.processStats()
    assert stats["events"]["count"] == 1
    assert stats["time"]["total"] > 0
    assert stats["time"]["last"] > 0
    assert stats["time"]["first"] > 0

def test_process():
    output = classes.output.output(id="test_output")
    event = {"data": "test_event"}
    
    # This should not raise an error
    output.process(event)
    
    # Check if processStats were not updated
    stats = output.processStats()
    assert stats["events"]["count"] == 0
    assert stats["time"]["total"] == 0
    assert stats["time"]["last"] == 0
    assert stats["time"]["first"] == 0