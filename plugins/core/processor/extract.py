import re

from classes import processor
from core import  typecast

class extract(processor.processor):

    def __init__(self,**kwargs):
        self.field = kwargs.get('field')
        self.outputField = kwargs.get('outputField')
        self.regexExtract = re.compile(kwargs.get('regex'))
        self.regexExtractGroup = kwargs.get('regexExtractGroup')
        self.merge = kwargs.get('merge',False)
        super().__init__(**kwargs)

    def process(self,event):
        if self.field:
            fieldValue = typecast.getField(self.field,event)
        else:
            fieldValue = event
        if fieldValue:
            reResults = [x.groupdict() for x in self.regexExtract.finditer(fieldValue)]
            if reResults:
                reResults = reResults[0]
                reResults = {k.replace('__', '.'): v for k, v in reResults.items()}
                if self.regexExtractGroup:
                    reResults = { self.regexExtractGroup : reResults[self.regexExtractGroup] }
                if self.outputField and type(event) is dict:
                    event[self.outputField] = reResults
                elif self.merge and type(event) is dict:
                    event.update(reResults)
                else:
                    event = reResults
        return event

