import re
import time
from classes import processor

from core import typecast

class match(processor.processor):
    defaultRule = None
    nextBehavior = 1

    def __init__(self,**kwargs):
        self.rules = []
        self.next = []
        for k,v in kwargs.items():
            if k.startswith("field"):
                x = k[5:]
                if match := kwargs.get(f"match{x}"):
                    if nextRule := kwargs.get(f"next{x}"):
                        self.rules.append([v,re.compile(match)])
                        self.next.append(nextRule)
        if kwargs.get("default"):
            self.rules.insert(0,None)
            self.next.insert(0,kwargs.get("default"))
            self.defaultRule = 0
        self.next.reverse()
        super().__init__(**kwargs)

    def processHandler(self,event):
        eventStartTime = time.perf_counter_ns()
        for index, rule in enumerate(self.rules):
            if self.defaultRule is not None and index == 0:
                continue
            try:
                fieldValue = typecast.getField(rule[0],event)
                if type(fieldValue) is not str and fieldValue is not None:
                    fieldValue = str(fieldValue)
            except:
                continue
            if fieldValue:
                if rule[1].match(fieldValue):
                    self.updateProcessStats(eventStartTime)
                    self.next[index].processHandler(event)
                    return
        if self.defaultRule is not None:
            self.updateProcessStats(eventStartTime)
            self.next[0].processHandler(event)
        