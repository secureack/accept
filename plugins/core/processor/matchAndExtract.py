import re
import time
from classes import processor

from core import typecast

class matchAndExtract(processor.processor):
    defaultRule = None
    nextBehavior = 1

    def __init__(self,**kwargs):
        self.typecast = kwargs.get("typecast",False)
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

    def processHandler(self,event,stack=[]):
        stack.append(self.id)
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
                reResults = [x.groupdict() for x in rule[1].finditer(fieldValue)]
                if reResults:
                    reResults = reResults[0]
                    if self.typecast:
                        reResults = {k.replace('__', '.'): typecast.simple(v) for k, v in reResults.items()}
                    else:
                        reResults = {k.replace('__', '.'): v for k, v in reResults.items()}
                    if type(event) is dict:
                        event.update(reResults)
                    else:
                        event = reResults
                    self.updateProcessStats(eventStartTime)
                    self.next[index].processHandler(event,stack)
                    return
        if self.defaultRule is not None:
            self.updateProcessStats(eventStartTime)
            self.next[0].processHandler(event,stack)
        