import pymongo
import json

from classes import output
from process import postRegister

class mongodb(output.output):

    def __init__(self,connectionString=None,database=None,collection=None,autoUnflatten=True,maxEvents=0,maxFlushSize=50000000,**kwargs):
        self.connectionString = connectionString
        self.database = database
        self.collection = collection
        self.buffer = []
        self.bufferSize = 0
        self.maxEvents = maxEvents
        self.maxFlushSize = maxFlushSize/2
        self.autoUnflatten = autoUnflatten
        self.database = pymongo.MongoClient(self.connectionString)[self.database]
        postRegister.items.add(self.onEnd)
        super().__init__(**kwargs)

    def process(self,event):
        if type(event) is not dict:
            self.logger.log(50,"ERROR: Event is not a dictionary, skipping",{ "event" : event },extra={ "source" : "mongodb", "type" : "error" })
            return
        if self.autoUnflatten:
            event = self.unflatten(event)
        self.buffer.append(event)
        self.bufferSize += len(json.dumps(event))
        if (self.maxEvents > 0 and len(self.buffer) >= self.maxEvents) or (self.maxFlushSize > 0 and self.bufferSize >= self.maxFlushSize):
            self.flush()
            self.buffer = []
            self.bufferSize = 0

    def unflatten(self,event):
        newEvent = {}
        for key, value in event.items():
            parts = key.split('.')
            currentPart = newEvent
            try:
                for part in parts[:-1]:
                    if part not in currentPart:
                        currentPart[part] = {}
                    currentPart = currentPart[part]
                currentPart[parts[-1]] = value
            except:
                newEvent[key] = value
        return newEvent

    def onEnd(self):
        self.flush()
    
    def flush(self):
        if len(self.buffer) > 0:
            result = self.database[self.collection].insert_many(self.buffer)
            if len(result.inserted_ids) != len(self.buffer):
                self.logger.log(25,"WARNING: Not all events were inserted into MongoDB",{ "count" : len(self.buffer), "inserted" : len(result.inserted_ids) },extra={ "source" : "mongodb", "type" : "warning" })
        self.buffer = []
