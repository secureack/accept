import time

from classes import processor

from core import logic

class rule(processor.processor):
    nextBehavior = 1

    def __init__(self,**kwargs):
        self.rules = []
        self.next = []
        self.statements = []
        for k,v in kwargs.items():
            if k.startswith("rule"):
                x = k[4:]
                if nextRule := kwargs.get(f"next{x}"):
                    self.rules.append(v)
                    self.next.append(nextRule)
        self.next.reverse()
        super().__init__(**kwargs)

    def processHandler(self,event,stack=[]):
        eventStartTime = time.perf_counter_ns()
        for index, rule in enumerate(self.rules):
            if rule and logic.ifEval(rule,{ "data" : { "event" : event } }):
                self.updateProcessStats(eventStartTime)
                try:
                    self.next[index].processHandler(event,stack)
                except Exception as e:
                    raise Exception(f"Unable to execute next for rule {rule}, {e}")
                break