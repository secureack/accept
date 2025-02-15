import json
import datetime

from classes import processor

from core import typecast

class stringEvent(processor.processor):

    def __init__(self,**kwargs):
        self.field = kwargs.get('field')
        super().__init__(**kwargs)

    def process(self,event):
        if self.field:
            fieldValue = typecast.getField(self.field,event)
            if type(fieldValue) is dict:
                event[self.field] = f"'{json.dumps(fieldValue)}'"
            else:
                event[self.field] = f"'{fieldValue}'"
            return event
        return { "@timestamp" : datetime.datetime.now().isoformat(), "message" : f"'{json.dumps(event)}'" }