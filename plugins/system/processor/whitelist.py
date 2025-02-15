from classes import processor

class whitelist(processor.processor):

    def __init__(self,whitelist=None,**kwargs):
        self.whitelist = whitelist
        if type(self.whitelist) is list:
            self.whitelist = set(self.whitelist)
        super().__init__(**kwargs)

    def process(self,event):
        if self.whitelist:
            newEvent = {}
            eventFields = list(event.keys())
            for field in self.whitelist:
                try:
                    if field.endswith("*"):
                        for eventField in eventFields:
                            if eventField.startswith(field[:-1]):
                                newEvent[eventField] = event[eventField]
                    elif field in eventFields:
                        newEvent[field] = event[field]
                except KeyError:
                    pass
            event = newEvent
        return event
