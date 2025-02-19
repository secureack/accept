import re

from classes import processor
from core import typecast

class kv(processor.processor):

    def __init__(self,**kwargs):
        self.separator = kwargs.get('separator',"=")
        self.spaced = kwargs.get('spaced'," ")
        self.quoteSupport = kwargs.get('support_quotes',False)
        self.typecast = kwargs.get('typecast',True)
        if self.quoteSupport:
            self.pattern = re.compile(r'(?{separator}(?P<key>"[^"]+"|\'[^\']+\'|[^{spaced}]+){separator}(?P<value>"[^"]+"|\'[^\']+\'|[^{spaced}]+))'.format(spaced=self.spaced, separator=self.separator))
        super().__init__(**kwargs)

    def process(self,event):
        kvEvent = {}
        if self.quoteSupport:
            matches = self.pattern.finditer(event)
            for match in matches:
                key = match.group('key').strip('"\'')
                value = match.group('value').strip('"\'')
                if self.typecast:
                    value = typecast.typecast(value)
                kvEvent[key] = value
        else:
            kvPairs = event.split(self.spaced)
            for kvPair in kvPairs:
                kv = kvPair.split(self.separator)
                if len(kv) == 2:
                    if self.typecast:
                        kvEvent[kv[0]] = typecast.typecast(kv[1])
                    else:
                        kvEvent[kv[0]] = kv[1]
        return kvEvent