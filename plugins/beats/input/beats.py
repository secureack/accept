import socket
import threading
import io
import zlib
import os
import ssl
from pathlib import Path
import time

from classes import input

class beats(input.input):

    def __init__(self,bindAddress="127.0.0.1",bindPort=3002,sslCertificate=None,sslPrivateKey=None,sslPrivateKeyPassword=None,sslClientCertificate=None,sslClientCertificateSubject=None,sslVersionMin=1.2,sslVersionMax=1.3,sslCiphers=None,maxActiveConnections=1024,**kwargs):
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
    
    def recv(self,recvObj,bufferLength):
        buffer = bytes()
        while len(buffer) < bufferLength:
            if bufferLength - len(buffer) > 4096:
                tempBuffer = recvObj.recv(4096)
            else:
                tempBuffer = recvObj.recv(bufferLength - len(buffer))
            if not tempBuffer:
                break
            buffer += tempBuffer
        if len(buffer) < bufferLength:
            self.logger.warning(f"received data buffer is smaller than expected {len(buffer)} {bufferLength}")
        return buffer

    def accept(self,client,address):
        self.logger.info(f"new beats connection: {address}")
        try:
            nextAck = 0
            windowSize = 0
            while True:
                byteReader = client
                while byteReader != None:
                    version =  byteReader.recv(1).decode()
                    if not version or not version == "2":
                        self.logger.debug(f"invalid frame version={version}")
                        raise Exception("invalid frame version")
                    atype = byteReader.recv(1).decode()
                    self.logger.debug(f"version={version} type={atype}")
                    if atype == "D":
                        sequenceNumber = int.from_bytes(byteReader.recv(4),"big")
                        pairCount = int.from_bytes(byteReader.recv(4),"big")
                        event = {}
                        for x in range(pairCount):
                            keyLength = int.from_bytes(byteReader.recv(4),"big")
                            key = self.recv(byteReader,keyLength).decode()
                            valueLength = int.from_bytes(byteReader.recv(4),"big")
                            value = self.recv(byteReader,valueLength).decode()
                            event[key] = value
                        self.event(event)
                        self.logger.debug(f"sequenceNumber={sequenceNumber} nextAck={nextAck} pairCount={pairCount}")
                        nextAck -= 1
                    elif atype == "J":
                        # Json payload
                        sequenceNumber = int.from_bytes(byteReader.recv(4),"big")
                        documentLength = int.from_bytes(byteReader.recv(4),"big")
                        document = self.recv(byteReader,documentLength).decode()
                        self.event(document)
                        self.logger.debug(f"sequenceNumber={sequenceNumber} nextAck={nextAck} documentLength={documentLength}")
                        nextAck -= 1
                    elif atype == "A":
                        # Act
                        sequenceNumber = byteReader.recv(4)
                        self.logger.debug(f"sequenceNumber={sequenceNumber} nextAck={nextAck}")
                        nextAck -= 1
                    elif atype == "W":
                        # Window size before ack is required
                        windowSize = int.from_bytes(byteReader.recv(4),"big")
                        nextAck = windowSize
                        self.logger.debug(f"windowSize={windowSize}")
                    elif atype == "C":
                        # Compressed payload
                        compressedPayloadLength = int.from_bytes(byteReader.recv(4),"big")
                        compressedPayload = self.recv(byteReader,compressedPayloadLength)
                        zobj = zlib.decompressobj()
                        decompressedPayload = zobj.decompress(compressedPayload)
                        byteReader = io.BytesIO(decompressedPayload)
                        byteReader.seek(0,2)
                        byteReaderEOF = byteReader.tell()
                        byteReader.seek(0)
                        setattr(byteReader,"recv",byteReader.read)
                        self.logger.debug(f"starting reading compressed payload compressedPayloadLength={compressedPayloadLength}")
                    if nextAck == 0:
                        # Ack
                        ackMessage = bytearray()
                        ackMessage += str(2).encode()
                        ackMessage += str("A").encode()
                        ackMessage += sequenceNumber.to_bytes(4,"big")
                        client.send(ackMessage)
                        nextAck = windowSize
                        self.logger.debug(f"ack {sequenceNumber}")
                    if type(byteReader) is io.BytesIO and byteReader.tell() >= byteReaderEOF:
                        self.logger.debug(f"finished reading compressed payload")
                        byteReader.close()
                        byteReader = None
        except Exception as e:
            self.logger.error(f"lumberjack protocol error: {e}")
        finally:
            client.close()
            self.currentConnections -= 1
