import socket
import threading
import os
import ssl
from pathlib import Path
import time

from classes import input

class tcp(input.input):

    def __init__(self,bindAddress="127.0.0.1",bindPort=6000,sslCertificate=None,sslPrivateKey=None,sslPrivateKeyPassword=None,sslClientCertificate=None,sslClientCertificateSubject=None,sslVersionMin=1.2,sslVersionMax=1.3,sslCiphers=None,maxActiveConnections=1024,**kwargs):
        self.bindAddress = bindAddress
        self.bindPort = bindPort
        self.server = None
        self.sslCertificate = sslCertificate
        self.sslPrivateKey = sslPrivateKey
        self.sslPrivateKeyPassword = sslPrivateKeyPassword
        self.sslClientCertificate = sslClientCertificate
        self.sslClientCertificateSubject = sslClientCertificateSubject
        self.sslVersionMin = sslVersionMin
        self.sslVersionMax = sslVersionMax
        self.sslCiphers = sslCiphers
        self.ssl = False
        if self.sslCertificate and self.sslPrivateKey:
            self.ssl = True
        self.maxActiveConnections = maxActiveConnections
        super().__init__(**kwargs)

    def start(self):
        super().start()
        if self.ssl:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            context.maximum_version = ssl.TLSVersion.TLSv1_3
            # TLS min version
            if self.sslVersionMin != 1.2:
                if self.sslVersionMin == 1.0:
                    context.minimum_version = ssl.TLSVersion.TLSv1
                elif self.sslVersionMin == 1.1:
                    context.minimum_version = ssl.TLSVersion.TLSv1_1
                elif self.sslVersionMin == 1.2:
                    context.minimum_version = ssl.TLSVersion.TLSv1_2
                elif self.sslVersionMin == 1.3:
                    context.minimum_version = ssl.TLSVersion.TLSv1_3
            # TLS max version
            if self.sslVersionMax != 1.3:
                if self.sslVersionMax == 1.0:
                    context.maximum_version = ssl.TLSVersion.TLSv1
                elif self.sslVersionMax == 1.1:
                    context.maximum_version = ssl.TLSVersion.TLSv1_1
                elif self.sslVersionMax == 1.2:
                    context.maximum_version = ssl.TLSVersion.TLSv1_2
                elif self.sslVersionMax == 1.3:
                    context.maximum_version = ssl.TLSVersion.TLSv1_3
            # TLS Ciphers
            if self.sslCiphers:
                context.set_ciphers(self.sslCiphers)
            # TLS Certificates
            context.load_cert_chain(str(Path(self.sslCertificate)), str(Path(self.sslPrivateKey)), self.sslPrivateKeyPassword)
            if self.sslClientCertificate:
                context.verify_mode = ssl.VerifyMode.CERT_REQUIRED
                context.load_verify_locations(cafile=str(Path(self.sslClientCertificate)))
        self.currentConnections = 0
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server.bind((self.bindAddress, self.bindPort))
        except Exception as e:
            self.logger.critical(f"critical error {e}")
            os._exit(255)
        self.server.listen(5)
        self.sock = self.server
        if self.ssl:
            self.sock = context.wrap_socket(self.server, server_side=True)
        while self.running:
            try:
                while self.maxActiveConnections > 0 and self.currentConnections >= self.maxActiveConnections:
                    time.sleep(1)
                client, address = self.sock.accept()
                if self.sslClientCertificate:
                    clientCert = client.getpeercert()
                    if not clientCert:
                        raise Exception("Mutual TLS handshake failed")
                    if self.sslClientCertificateSubject and self.sslClientCertificateSubject != [ x[0][1] for x in clientCert['subject'] if x[0][0] == "commonName" ][0]:
                        raise Exception("Mutual TLS handshake failed - invalid commonName")
                self.currentConnections += 1
                threading.Thread(target=self.accept, args=(client,address)).start()
            except Exception as e:
                self.logger.error(f"connection exception occurred {e}")

    def stop(self):
        if self.server:
            if self.ssl:
                self.sock.close()
            self.server.close()
            self.server = None
        super().stop()

    def accept(self,client,address):
        self.logger.info(f"new tcp connection: {address}")
        try:
            data = ""
            while True:
                data += client.recv(4096).decode()
                if not data:
                    break
                if "\n" in data:
                    for e in data.split("\n")[:-1]:
                        self.event(e)
                    data = data.split("\n")[-1]
        except Exception as e:
            self.logger.error(f"tcp protocol error: {e}")
        finally:
            client.close()
            self.currentConnections -= 1
