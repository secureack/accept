import inspect
import time

from core import globalSettings, globalLogger
from classes import base

class output(base.base):

    def __init__(self,**kwargs):
        self.id = kwargs.get("id")
        self.logger = globalLogger.getLogger(__name__,kwargs.get("log_level",globalSettings.args.log_level))
        self.trace = kwargs.get("trace",False)
        super().__init__(**kwargs)

    def processHandler(self,event):
        eventStartTime = time.perf_counter_ns()
        if self.trace:
            trace = []
            for stack in inspect.stack():
                try:
                    if stack.function == "processHandler":
                        trace.append(stack.frame.f_locals.get("self").id)
                except:
                    pass
            self.logger.log(10,"Event Trace", { "trace" : trace }, extra={ "source" : "output", "type" : "trace" })
        self.process(event)
        self.updateProcessStats(eventStartTime)
        
    def process(self,event):
        pass
