import logging
import sys
import time
import json
from traceback import format_exception

from core import globalSettings

class _logger(logging.Handler):

    def __init__(self):
        super().__init__()

    def emit(self, record):
        message = {
            "@timestamp" : time.time(),
            "msg" : record.msg,
            "level" : record.levelname,
            "source" : getattr(record,"source","Unknown"),
            "type" : getattr(record,"type","Unknown"),
            "caller" : {
                "pid" : record.process,
                "filename" : record.filename,
                "line" : record.lineno
            },
            "props" :  record.args if type(record.args) is dict else {},
            "context" : {
                "pipeline" : getattr(globalSettings.args,"pipeline","None"),
                "cache" : getattr(globalSettings.args,"cache","None")
            }
        }
        if record.exc_info:
            message["trace"] = format_exception(*record.exc_info)
        sys.stderr.write(f"Accept {message['msg']} | {json.dumps(message)}\n")

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s[%(process)d] %(filename)s:%(lineno)d | %(message)s")
logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(globalSettings.args.log_level)
logger.addHandler(_logger())

def getLogger(name,level=5):
    newLogger = logging.getLogger(name)
    newLogger.propagate = False
    newLogger.setLevel(level)
    newLogger.addHandler(_logger())
    return newLogger

def unhandledExceptionHook(*exc_info):
    global logger
    message = ''.join(format_exception(*exc_info)).replace("\n","\\n")
    logger.log(100,f"Critical Uncaught Exception",{ "exception" : message },extra={ "source" : "exception", "type" : "exception" })

sys.excepthook = unhandledExceptionHook

