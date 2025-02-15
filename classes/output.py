import logging
import time

from core import globalSettings, globalLogger
from classes import base

class output(base.base):

    def __init__(self,**kwargs):
        self.id = kwargs.get("id")
        self.logger = globalLogger.getLogger(__name__,kwargs.get("log_level",globalSettings.args.log_level))
        super().__init__(**kwargs)

    def processHandler(self,event):
        eventStartTime = time.perf_counter_ns()
        self.process(event)
        self.updateProcessStats(eventStartTime)
        
    def process(self,event):
        pass
        