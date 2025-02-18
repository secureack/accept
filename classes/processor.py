import time

from core import globalSettings, globalLogger
from classes import base

class processor(base.base):
    next = None

    def __init__(self,**kwargs):
        self.id = kwargs.get("id")
        self.logger = globalLogger.getLogger(__name__,kwargs.get("log_level",globalSettings.args.log_level))
        super().__init__(**kwargs)

    def processHandler(self,event,stack=[]):
        stack.append(self.id)
        eventStartTime = time.perf_counter_ns()
        event = self.process(event)
        self.updateProcessStats(eventStartTime)
        self.processNext(event,stack)
        
    def processNext(self,event,stack=[]):
        for next in self.next if self.next else []:
            next.processHandler(event,stack)

    def process(self,event):
        return event
