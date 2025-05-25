import pytest
import sys
import json
import logging

import core.globalLogger
import core.globalSettings

def test_unhandledHook():
    assert sys.excepthook == core.globalLogger.unhandledExceptionHook

def test_getLogger():
    logger = core.globalLogger.logger
    assert isinstance(logger, logging.Logger)
    assert logger.level == 10
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], core.globalLogger._logger)

def test_logger_emit(capsys):
    logger = core.globalLogger.logger
    logger.info("Test message", { "ip" : "1.1.1.1" }, extra={"source": "test_source", "type": "test_type"})

    captured = capsys.readouterr()
    assert "Accept Test message" in captured.err
    capturedDict = json.loads(captured.err.split(" | ")[1])
    assert capturedDict["@timestamp"] is not None
    assert capturedDict["msg"] == "Test message"
    assert capturedDict["level"] == "INFO"
    assert capturedDict["source"] == "test_source"
    assert capturedDict["type"] == "test_type"
    assert capturedDict["caller"]["pid"] > 0
    assert capturedDict["caller"]["filename"] == "test_core_globalLogger.py"
    assert capturedDict["caller"]["line"] > 0
    assert capturedDict["context"]["pipeline"] == core.globalSettings.args.pipeline
    assert capturedDict["context"]["cache"] == "test"
    assert capturedDict["props"]["ip"] == "1.1.1.1"
    assert "trace" not in capturedDict

def test_logger_emit_with_exception(capsys):
    logger = core.globalLogger.logger
    try:
        1 / 0
    except ZeroDivisionError:
        logger.error("Test exception", extra={"source": "test_source", "type": "test_type"}, exc_info=True)

    captured = capsys.readouterr()
    capturedDict = json.loads(captured.err.split(" | ")[1])
    assert "trace" in capturedDict