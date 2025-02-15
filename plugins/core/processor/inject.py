from classes import processor

from core import logic

class inject(processor.processor):

    def __init__(self,**kwargs):
        self.inject = kwargs.get('inject')
        super().__init__(**kwargs)

    def process(self,event):
        for field, value in self.inject.items():
            if type(value) is dict:
                for k,v in value.items():
                    if k.startswith("if ") and logic.ifEval(k,{ "data" : {  "event" : event } }):
                        event[field] = v
                        break
                    elif k == "default":
                        event[field] = v
                        break
            else:
                event[field] = value
        return event
