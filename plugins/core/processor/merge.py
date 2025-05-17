from classes import processor

from core import typecast

class merge(processor.processor):

    def __init__(self,**kwargs):
        self.field = kwargs.get('field')
        super().__init__(**kwargs)
    
    def process(self,event):
        if self.field:
            fieldValue = typecast.getField(self.field,event)
            if type(event) is dict and type(fieldValue) is dict:
                event.update(fieldValue)
                try:
                    del event[self.field]
                except KeyError:
                    pass
        return event
