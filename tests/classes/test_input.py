import pytest
import time

import classes.input
import core.globalSettings

def test_input():
    input_instance = classes.input.input(id="test_input")
    assert input_instance.id == "test_input"
    assert hasattr(input_instance, 'logger')
    assert hasattr(input_instance, 'next')
    assert input_instance.running == False
    assert input_instance.flushInterval == 60
    assert input_instance.flushEvery == 1000000

def test_input_non_default():
    input_instance = classes.input.input(id="test_input",flush_interval=30, flush_every=500000)
    assert input_instance.flushInterval == 30
    assert input_instance.flushEvery == 500000

def test_start_stop():
    input_instance = classes.input.input(id="test_input",flush_interval=2, flush_every=100)
    input_instance.start()
    time.sleep(1)
    assert input_instance.running == True
    assert input_instance.cacheWriter is not None
    assert input_instance.cacheWriter["file"] is not None
    assert input_instance.cacheWriter["filePath"].endswith('.build')
    assert input_instance.cacheWriter["createdTime"] > 0
    assert input_instance.cacheWriter["totalEvents"] == 0
    assert input_instance.cacheWriter["filePath"].startswith(core.globalSettings.args.cache_dir)
    assert input_instance.cacheWriter["filePath"].endswith(f".{core.globalSettings.args.pipeline}.{input_instance.name}.build")
    current_file = input_instance.cacheWriter["file"]
    with input_instance.lock:
        input_instance.rotateCache(createNew=True)
    assert input_instance.cacheWriter["file"] is not current_file
    current_file = input_instance.cacheWriter["file"]
    input_instance.event("test")
    assert input_instance.cacheWriter["totalEvents"] == 1
    time.sleep(4)
    assert input_instance.cacheWriter["file"] is not current_file
    assert input_instance.cacheWriter["totalEvents"] == 0
    current_file = input_instance.cacheWriter["file"]
    for i in range(102):
        input_instance.event(f"test_event_{i}")
    assert input_instance.cacheWriter["totalEvents"] == 1
    assert input_instance.cacheWriter["file"] is not current_file
    input_instance.stop()
    assert input_instance.running == False
    assert input_instance.cacheWriter["file"] is None

def test_process():
    input_instance = classes.input.input(id="test_input")
    input_instance.process()