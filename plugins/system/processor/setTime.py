import datetime
import re
import time

from classes import processor

class setTime(processor.processor):

    def __init__(self,field=None,outputField="@timestamp",inputFormat=None,outputFormat=None,regex=None,regexGroup="time",suppressErrors=True,**kwargs):
        self.field = field
        self.outputField = outputField
        self.inputFormat = inputFormat
        self.outputFormat = outputFormat
        self.regexExtract = regex
        self.regexExtractGroup = regexGroup
        self.suppressErrors = suppressErrors
        super().__init__(**kwargs)

    def process(self,event):
        eventTime = None
        if self.field in event:
            if self.regexExtract and self.field and self.inputFormat:
                try:
                    reResults = [x.groupdict() for x in re.finditer(self.regexExtract,event[self.field])][0]
                    if self.inputFormat == "epoch":
                        eventTime = datetime.datetime.fromtimestamp(int(reResults[self.regexExtractGroup]))
                    else:
                        eventTime = datetime.datetime.strptime(reResults[self.regexExtractGroup],self.inputFormat)
                except Exception as e:
                    if not self.suppressErrors:
                        self.logger.error(f"unable to extract datetime from: {event}, error: {e}")
            elif self.field and self.inputFormat:
                try:
                    if self.inputFormat == "epoch":
                        eventTime = datetime.datetime.fromtimestamp(int(event[self.field]))
                    elif self.inputFormat == "iso":
                        eventTime = datetime.datetime.fromisoformat(event[self.field])
                    else:
                        eventTime = datetime.datetime.strptime(event[self.field],self.inputFormat)
                except KeyError:
                    self.logger.debug(f"unable to extract datetime from: {event} with no such field {self.field}")
                except Exception as e:
                    if not self.suppressErrors:
                        self.logger.error(f"unable to extract datetime from: {event}, error: {e}")
            if not eventTime:
                eventTime = datetime.datetime.fromtimestamp(time.time())
            if self.outputFormat:
                try:
                    event[self.outputField] = eventTime.strftime(self.outputFormat)
                except Exception as e:
                    if not self.suppressErrors:
                        self.logger.error(f"unable to output datetime from: {event}, error: {e}")
                    event[self.outputField] = eventTime.isoformat()
            else:
                event[self.outputField] = eventTime.isoformat()
        return event
