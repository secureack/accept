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

        while self.running:
            data = ""
            try:
                data, address = self.server.recvfrom(4096)
                if "\n" in data:
                    for e in data.split("\n")[:-1]:
                        self.event(e)
                    data = data.split("\n")[-1]
            except Exception as e:
                self.logger.error(f"connection exception occurred {e}")

    def stop(self):
        if self.server:
            if self.ssl:
                self.sock.close()
            self.server.close()
            self.server = None
        super().stop()

