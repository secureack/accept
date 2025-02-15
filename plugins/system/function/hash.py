import hashlib

def md5(string):
    encrypt = hashlib.md5(string.encode())
    return encrypt.hexdigest()

def sha1(string):
    encrypt = hashlib.sha1(string.encode())
    return encrypt.hexdigest()

def sha256(string):
    encrypt = hashlib.sha256(string.encode())
    return encrypt.hexdigest()

def sha512(string):
    encrypt = hashlib.sha512(string.encode())
    return encrypt.hexdigest()
