import pytest

from plugins.system.processor.setTime import setTime

def test_setTime_epoch():
    processor = setTime(field="timestamp", inputFormat="epoch", outputField="event_time")
    event = {"timestamp": 1633072800}  # Example epoch time
    processed_event = processor.process(event)
    assert processed_event["event_time"] == "2021-10-01T07:20:00"

def test_setTime_iso():
    processor = setTime(field="timestamp", inputFormat="iso", outputField="event_time", outputFormat="%Y-%m-%dT%H:%M")
    event = {"timestamp": "2021-10-01T00:00:00"}
    processed_event = processor.process(event)
    assert processed_event["event_time"] == "2021-10-01T00:00"

def test_setTime_strptime():
    processor = setTime(field="timestamp", inputFormat="%Y-%m-%d %H:%M:%S", outputField="event_time", outputFormat="%Y-%m-%dT%H:%M")
    event = {"timestamp": "2021-10-01 00:00:00"}
    processed_event = processor.process(event)
    assert processed_event["event_time"] == "2021-10-01T00:00"

def test_setTime_no_field():
    processor = setTime(field="nonexistent", inputFormat="epoch", outputField="event_time")
    event = {}
    processed_event = processor.process(event)
    assert "event_time" not in processed_event  # Should not raise an error, just skip setting the field

def test_setTime_empty_event():
    processor = setTime(field="timestamp", inputFormat="epoch", outputField="event_time")
    event = {}
    processed_event = processor.process(event)
    assert "event_time" not in processed_event  # Should not raise an error, just skip setting the field