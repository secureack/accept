import uvicorn
import json
from classes import input

EMPTY_RESPONSE = {
    'type': 'http.response.body',
    'body': b''
}

class httpWebHook(input.input):

    def __init__(self,**kwargs):
        self.bindAddress = kwargs.get("bind_address","127.0.0.1")
        self.bindPort = kwargs.get("bind_port",5656)
        self.path = kwargs.get("path",None)
        self.contentType = kwargs.get("content_type","json")
        self.authParameter = kwargs.get("authentication_parameter",None)
        self.authHeader = kwargs.get("authentication_header",None)
        self.customHeaders = []
        if kwargs.get("headers",None):
            for headerName, headerValue in kwargs.get("headers",{}).items():
                self.customHeaders.append([headerName.encode('UTF-8'), headerValue.encode('UTF-8')])
        super().__init__(**kwargs)

    def start(self):
        super().start()
        uvicorn.run(self,host=self.bindAddress,port=self.bindPort)

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http":
            if self.customHeaders and scope['method'] == "HEAD":
                await send(self.generateHeaders(200))
                await send(EMPTY_RESPONSE)
                return
            elif scope['method'] in ("GET", "POST"):
                if self.path and scope['path'] != self.path:
                    await send(self.generateHeaders(403))
                    await send(EMPTY_RESPONSE)
                    return
                if self.authParameter:
                    queryParams = dict(param.split('=') for param in scope.get('query_string', b'').decode('utf-8').split('&') if '=' in param)
                    for parameter, value in self.authParameter.items():
                        if queryParams.get(parameter) != value:
                            await send(self.generateHeaders(403))
                            await send(EMPTY_RESPONSE)
                            return
                if self.authHeader:
                    headers = { header.decode('utf-8') : value.decode('utf-8') for header, value in scope.get('headers', []) }
                    for header, value in self.authHeader.items():
                        if headers.get(header) != value:
                            await send(self.generateHeaders(403))
                            await send(EMPTY_RESPONSE)
                            return  
                getBody = True
                body = ''
                while getBody:
                    msg = await receive()
                    body += msg.get('body', '').decode('utf-8')
                    getBody = msg.get('moreBody', False)
                if self.contentType == "json":
                    try:
                        events = json.loads(body)
                        if type(events) == list:
                            for event in events:
                                self.event(event)
                        else:
                            self.event(events)
                    except:
                        pass
                events = body.split('\n')
                for event in events:
                    self.event(event)
                await send(self.generateHeaders(200))
                await send(EMPTY_RESPONSE)
                return
            await send(self.generateHeaders(403))
            await send(EMPTY_RESPONSE)

    def generateHeaders(self, status=200):
        obj = {
            'type': 'http.response.start',
            'status': status,
            'headers': []
        }
        obj['headers'].extend(self.customHeaders)
        return obj
    