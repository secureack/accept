import pytest

import classes.processor as processor

from plugins.system.processor.logic import logic

def test_logic():
    hit = 0
    class DummyNext(processor.processor):
        def process(self, event):
            nonlocal hit
            hit += 1
            return event
    logic_instance = logic(logicString="if data[event][type] == test")
    logic_instance.next = [DummyNext()] 
    event = {"type": "test"}
    newEvent = logic_instance.processHandler(event)
    assert hit == 1

    logic_instance = logic(logicString="if data[event][type] != test")
    logic_instance.next = [DummyNext()] 
    event = {"type": "test"}
    newEvent = logic_instance.processHandler(event)
    assert hit == 1
