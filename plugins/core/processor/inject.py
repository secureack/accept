from classes import processor

from core import logic

class inject(processor.processor):

    def __init__(self,**kwargs):
        self.inject = kwargs.get('inject')
        super().__init__(**kwargs)

    def process(self,event):
        for field, value in self.inject.items():
            if isinstance(value, list):
                for item in value:
                    if "logic" in item:
                        if logic.ifEval(item,{ "data" : {  "event" : event } }):
                            event[field] = item["value"]
                            break
                    elif "default" in item:
                        event[field] = item["default"]
                        break
            else:
                event[field] = value
        return event