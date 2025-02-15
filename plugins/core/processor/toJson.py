import json
import ast

from classes import processor
from core import typecast

class toJson(processor.processor):

    def __init__(self,**kwargs):
        self.field = kwargs.get('field')
        self.outputField = kwargs.get('outputField')
        self.singleQuoteSupport = kwargs.get('singleQuoteSupport',False)
        self.strict = kwargs.get('strict',True)
        self.merge = kwargs.get('merge',False)
        super().__init__(**kwargs)

    def process(self,event):
        if self.field:
            fieldValue = typecast.getField(self.field,event)
        else:
            fieldValue = event
            
        if fieldValue:
            if self.singleQuoteSupport:
                fieldValue = ast.literal_eval(fieldValue)
            else:
                fieldValue = json.loads(fieldValue,strict=self.strict)
            if self.outputField and type(event) is dict:
                event[self.outputField] = fieldValue
            elif self.merge and type(event) is dict:
                event.update(fieldValue)
            else:
                event = fieldValue
        return event
