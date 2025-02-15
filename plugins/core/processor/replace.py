from classes import processor

from core import typecast

class replace(processor.processor):

    def __init__(self,**kwargs):
        self.field = kwargs.get('field')
        self.find = kwargs.get('find')
        self.value = kwargs.get('value')
        super().__init__(**kwargs)

    def process(self,event):
        fieldValue = typecast.getField(self.field,event)
        if fieldValue:
            typecast.setField(self.field,fieldValue.replace(self.find, self.value),event)
        return event