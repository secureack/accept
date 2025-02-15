from classes import processor

from core import typecast, logic

class rename(processor.processor):

    def __init__(self,**kwargs):
        self.rename = kwargs.get('rename')
        self.preserve = kwargs.get('preserve',False)
        super().__init__(**kwargs)

    def process(self,event):
        for oldField, newField in self.rename.items():
            if type(newField) is str:
                event[newField] = typecast.getField(oldField,event)
                if not self.preserve:
                    try:
                        del event[oldField]
                    except KeyError:
                        self.logger.debug(f"Unable to delete {oldField} from {event}")
            elif type(newField) is list:
                for k, v in newField[1].items():
                    if k.startswith("if ") and logic.ifEval(k,{ "data" : {  "event" : event } }):
                        event[newField[0]] = v
                        if not self.preserve:
                            del event[oldField]
                        break
                    elif k == "default":
                        event[newField[0]] = v
                        if not self.preserve:
                            try:
                                del event[oldField]
                            except KeyError:
                                self.logger.debug(f"Unable to delete {oldField} from {event}")
                        break
        return event
