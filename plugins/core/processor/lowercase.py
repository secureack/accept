from classes import processor

from core import typecast

class lowercase(processor.processor):

    def __init__(self,**kwargs):
        self.fields = kwargs.get('fields')
        self.suppressErrors = kwargs.get('suppressErrors',True)
        super().__init__(**kwargs)

    def process(self,event):
        for field in self.fields:
            typecast.setField(field,str(typecast.getField(field,event)).lower(),event)
        return event
