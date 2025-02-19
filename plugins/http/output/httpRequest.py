import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from classes import output
from process import postRegister

class httpRequest(output.output):

    def __init__(self,**kwargs):
        self.url = kwargs.get("url",None)
        self.verify = kwargs.get("verify",True)
        self.method = kwargs.get("method","GET")
        self.bulk = kwargs.get("bulk",False)
        self.useSession = kwargs.get("use_session",False)
        self.bulkMaxEvents = kwargs.get("bulk_max_events",0)
        self.headers = kwargs.get("headers",{})
        self.expectedStatusCode = kwargs.get("status_code",200)
        self.buffer = []
        if self.bulk:
            postRegister.items.add(self.onEnd)
        if self.useSession:
            self.session = requests.Session()
        super().__init__(**kwargs)

    def process(self,event):
        self.buffer.append(event)
        if self.bulk:
            if self.bulkMaxEvents > 0 and len(self.buffer) >= self.bulkMaxEvents:
                self.flush(self.buffer)
        else:
            self.flush(self.buffer)

    def onEnd(self):
        self.flush()
    
    def flush(self):
        if len(self.buffer) > 0:
            if len(self.buffer) == 1 and type(self.buffer[0]) == dict:
                self.buffer = self.buffer[0]
            request = requests.request
            if self.useSession:
                request = self.session.request
            response = request(self.method,self.url,json=self.buffer,verify=self.verify,headers=self.headers)
            if response.status_code != self.expectedStatusCode:
                self.logger.log(10,"Unexpected response status code",{ "status_code" : response.status_code, "expected_status_code" : self.expectedStatusCode, "url" : self.url, "response" : response.text },extra={ "source" : "httpRequest", "type" : "error" })
        self.buffer = []
