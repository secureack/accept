from classes import processor

from core import typecast, logic

class rename(processor.processor):

    def __init__(self,**kwargs):
        self.rename = kwargs.get('rename')
        self.preserve = kwargs.get('preserve',False)
        self.NoneFields = kwargs.get('none_fields',False)
        super().__init__(**kwargs)

    def process(self,event):
        for oldField, newField in self.rename.items():
            if isinstance(newField, str):
                fieldValue = typecast.getField(oldField,event)
                if fieldValue or self.NoneFields:
                    event[newField] = fieldValue
                else:
                    continue
                if not self.preserve:
                    try:
                        del event[oldField]
                    except KeyError:
                        self.logger.log(4,"Unable to delete",{ "field" : oldField },extra={ "source" : "rename", "type" : "error" })
            elif isinstance(newField, list):
                for item in newField[1:]:
                    if "logic" in item:
                        if logic.ifEval(item,{ "data" : {  "event" : event } }):
                            event[newField[0]] = item["value"]
                            if not self.preserve:
                                del event[oldField]
                            break
                    elif "default" in item:
                        event[newField[0]] = item["default"]
                        if not self.preserve:
                            try:
                                del event[oldField]
                            except KeyError:
                                self.logger.log(4,"Unable to delete",{ "field" : oldField },extra={ "source" : "rename", "type" : "error" })
                        break
        return event