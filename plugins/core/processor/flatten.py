from classes import processor

from core import typecast

class flatten(processor.processor):
    
    def process(self,event):
        if type(event) is dict:
            event = typecast.flatten(event)
        return event
