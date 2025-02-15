from classes import processor

class blacklist(processor.processor):

    def __init__(self,**kwargs):
        self.wildcards = []
        self.blacklist = set()
        for field in kwargs.get('blacklist'):
            if field.endswith("*"):
                self.wildcards.append(field)
            else:
                self.blacklist.add(field)
        super().__init__(**kwargs)

    def process(self,event):
        poplist = []
        for field in list(event.keys()):
            if field in self.blacklist:
                poplist.append(field)
            for wildcard in self.wildcards:
                if field.startswith(wildcard[:-1]):
                    poplist.append(field)
                    break
        for field in poplist:
            del event[field]
        return event
