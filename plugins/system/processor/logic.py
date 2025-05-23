import time

from classes import processor
from core import logic as coreLogic

class logic(processor.processor):

    def __init__(self,logicString=None,**kwargs):
        self.logicString = logicString
        super().__init__(**kwargs)

    def processHandler(self,event,stack=[]):
        stack.append(self.id)
        eventStartTime = time.perf_counter()
        if coreLogic.ifEval(self.logicString, { "data" : { "event" : event } }): 
            self.updateProcessStats(eventStartTime)
            for next in self.next if self.next else []:
                next.processHandler(event,stack)
        return event