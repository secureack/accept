import time
import socket
import os

from classes import input

class udp(input.input):

    def __init__(self,bindAddress="127.0.0.1",bindPort=6000,**kwargs):
        self.bindAddress = bindAddress
        self.bindPort = bindPort
        self.server = None
        super().__init__(**kwargs)

    def start(self):
        super().start()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server.bind((self.bindAddress, self.bindPort))
        except Exception as e:
            self.logger.critical(f"critical error {e}")
            os._exit(255)

        responseBuffer = {}
        nextCheck = time.time() + 60
        while self.running:
            try:
                if time.time() > nextCheck:
                    for address in list(responseBuffer.keys()):
                        if responseBuffer[address]["last"] < time.time():
                            del responseBuffer[address]
                    nextCheck = time.time() + 60

                data, address = self.server.recvfrom(4096)
                if address not in responseBuffer:
                    responseBuffer[address] = { "last" : time/time() + 60, "data" : "" }
                else:
                    responseBuffer[address]["last"] = time.time() + 60
                responseBuffer[address]["data"] += data.decode("utf-8")
                if "\n" in responseBuffer[address]["data"]:
                    for e in responseBuffer[address]["data"].split("\n")[:-1]:
                        self.event(e)
                    responseBuffer[address]["data"] = responseBuffer[address]["data"].split("\n")[-1]
                    if not responseBuffer[address]["data"]:
                        del responseBuffer[address]
            except Exception as e:
                self.logger.error(f"connection exception occurred {e}")

    def stop(self):
        if self.server:
            if self.ssl:
                self.sock.close()
            self.server.close()
            self.server = None
        super().stop()

