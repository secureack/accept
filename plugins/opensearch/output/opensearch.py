import requests
import json
import datetime
import urllib3
import time
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from classes import output
from process import postRegister

class opensearch(output.output):

    def __init__(self,url=None,username=None,password=None,verify=True,timeout=30,index=None,maxEvents=0,maxFlushSize=50000000,**kwargs):
        if not url.endswith("/"):
            url += "/"
        self.url = f"{url}{index}/"
        self.username = username
        self.password = password
        self.verify = verify
        self.timeout = timeout
        self.index = index
        self.buffer = []
        self.bufferSize = 0
        self.maxEvents = maxEvents
        self.maxFlushSize = maxFlushSize/2
        self.lastRefresh = 0
        postRegister.items.add(self.onEnd)
        super().__init__(**kwargs)

    def process(self,event):
        if type(event) is not dict:
            event = { "message" : event }
        if "@timestamp" not in event:
            event["@timestamp"] = datetime.datetime.now().isoformat()
        eventString = json.dumps(event)
        self.buffer.append(eventString)
        self.bufferSize += len(eventString)
        if (self.maxEvents > 0 and len(self.buffer) >= self.maxEvents) or (self.maxFlushSize > 0 and self.bufferSize >= self.maxFlushSize):
            self.flush()
            self.buffer = []
            self.bufferSize = 0

    def onEnd(self):
        self.flush()
    
    def buildEvents(self,events):
        result = []
        for event in events:
            result.append(json.dumps({ "index" : {} }))
            result.append(event)
        return result

    def flush(self):
        failedEvents = []
        if len(self.buffer) > 0:
            events = self.buildEvents(self.buffer)
            resultCode, resultMessage, eventErrors = self.flushOpenSearch(events)
            # Event errors occurred
            if resultCode == 1:
                for eventError in eventErrors:
                    self.logger.log(10,"Reject By opensearch",{ "reason" : f"{eventError[1]['index']['error']['type']} - {eventError[1]['index']['error']['reason']}" } )
                    failedEvents.append(json.dumps({ "@timestamp" : datetime.datetime.now().isoformat(), "message" : self.buffer[eventError[0]], "error_type" : eventError[1]['index']['error']['type'], "error_reason" : eventError[1]['index']['error']['reason'] }))
            elif resultCode == 2:
                sys.exit(2)
            # Unauthorized
            elif resultCode == 3:
                sys.exit(3)
            # Request failure ( too large )
            elif resultCode == 4 or resultCode == 5:
                if resultCode == 5:
                    time.sleep(10)
                buffer_chunks = [self.buffer[i::4] for i in range(4)]
                for chunk in buffer_chunks:
                    events = self.buildEvents(chunk)
                    resultCode, resultMessage, eventErrors = self.flushOpenSearch(events)
                    if resultCode not in [0,1]:
                        sys.exit(10)
                    elif resultCode == 1:
                        for eventError in eventErrors:
                            self.logger.log(10,"Reject By opensearch",{ "reason" : f"{eventError[1]['index']['error']['type']} - {eventError[1]['index']['error']['reason']}" } )
                            failedEvents.append(json.dumps({ "@timestamp" : datetime.datetime.now().isoformat(), "message" : chunk[eventError[0]], "error_type" : eventError[1]['index']['error']['type'], "error_reason" : eventError[1]['index']['error']['reason'] }))
        if len(failedEvents) > 0:
            events = self.buildEvents(failedEvents)
            resultCode, resultMessage, eventErrors = self.flushOpenSearch(events)
            if not resultCode == 0:
                self.logger.log(10,"Failed events failed to flush",{ "result_code" : resultCode, "result_message" : resultMessage, "count" : len(eventErrors) } )

    def flushOpenSearch(self,bulkPayload):
        resultCode = 999
        resultMessage = ""
        failedEvents = []
        response = requests.post(f"{self.url}_bulk",data="\n".join(bulkPayload)+"\n",auth=(self.username,self.password),verify=self.verify,headers={ "Content-Type" : "application/json", "Accept" : "application/json" },timeout=self.timeout)
        self.logger.debug(f"flush opensearch {response.status_code} {response.elapsed.total_seconds()}")
        if response.status_code == 200:
            resultCode = 0
            responseJSON = json.loads(response.text)
            if responseJSON["errors"]:
                resultMessage = "valid response but errors occurred"
                resultCode = 1
                for index, event in enumerate(responseJSON["items"]):
                    if event["index"]["status"] != 201:
                        failedEvents.append([index,event])
        elif response.status_code == 400:
            resultCode = 2
            resultMessage = "request aborted"
        elif response.status_code == 401:
            resultCode = 3
            resultMessage = "unauthorized"
        elif response.status_code == 413:
            resultCode = 4
            resultMessage = "request body too large"
        elif response.status_code == 429:
            resultCode = 5
            resultMessage = "too many requests"
        return (resultCode,resultMessage,failedEvents)
