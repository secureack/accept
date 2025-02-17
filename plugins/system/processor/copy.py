import json

from classes import processor

class copy(processor.processor):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self,event):
        return json.loads(json.dumps(event))
