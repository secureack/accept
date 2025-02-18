import time

from core import globalSettings, globalLogger
from classes import base

class output(base.base):

    def __init__(self,**kwargs):
        self.id = kwargs.get("id")
        self.logger = globalLogger.getLogger(__name__,kwargs.get("log_level",globalSettings.args.log_level))
        self.trace = kwargs.get("trace",False)
        super().__init__(**kwargs)

    def processHandler(self,event,stack=[]):
        eventStartTime = time.perf_counter_ns()
        if self.trace and type(event) == dict:
            if "__accept__" not in event:
                event["__accept__"] = { }
            event["__accept__"]["trace"] = stack
        self.process(event)
        self.updateProcessStats(eventStartTime)
        
    def process(self,event):
        pass
