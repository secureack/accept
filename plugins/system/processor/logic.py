import time

from classes import processor
from plugins.system.core import logic as coreLogic

class logic(processor.processor):

    def __init__(self,logicString=None,**kwargs):
        self.logicString = logicString
        self.logicStatements = coreLogic.complieIf(logicString)
        super().__init__(**kwargs)

    def processHandler(self,event):
        eventStartTime = time.perf_counter()
        if coreLogic.compliedEval(self.logicString,self.logicStatements,{ "data" : { "event" : event } }): 
            self.updateProcessStats(eventStartTime)
            for next in self.next if self.next else []:
                next.processHandler(event)
        return event