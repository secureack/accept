import json

from classes import processor

class copy(processor.processor):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def process(self,event):
        try:
            event = json.loads(json.dumps(event))
        except Exception as e:
            self.logger.error(f"unexpected error occurred copy: {e}")
        return event
