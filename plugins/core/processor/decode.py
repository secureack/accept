from classes import processor

from core import typecast

class decode(processor.processor):

    def __init__(self,**kwargs):
        self.field = kwargs.get('field')
        self.decode = kwargs.get('decode',"unicode_escape")
        super().__init__(**kwargs)

    def process(self,event):
        fieldValue = typecast.getField(self.field,event)
        if fieldValue:
            typecast.setField(self.field,fieldValue.encode("raw_unicode_escape").decode(self.decode),event)
        return event