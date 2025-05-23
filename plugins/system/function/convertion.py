import json
from core import typecast

def getType(x):
    return type(x).__name__

def toInt(x):
    return int(x)

def toFloat(x):
    return float(x)

def toBool(x):
    return bool(x)

def toStr(x):
    return str(x)

def strToInt(string):
    return int(string)

def strToFloat(string):
    return float(string)

def strToBool(string):
    return bool(string)

def strToBytes(string):
    return string.encode()

def bytesToStr(bytes):
    return bytes.decode()

def intToStr(integer):
    return str(integer)

def lower(string):
    try:
        return string.lower()
    except:
        return string

def upper(string):
    try:
        return string.upper()
    except:
        return string

def toJson(string,**kwargs):
    try:
        return json.loads(string,**kwargs)
    except:
        return string

def fromJson(j,indent=False,**kwargs):
    try:
        if indent:
            return "\"{0}\"".format(json.dumps(j,indent = 3,**kwargs))
        return "\"{0}\"".format(json.dumps(j,**kwargs))
    except:
        return j

def encode(obj,*args):
    return obj.encode(*args)

def decode(obj,*args):
    return obj.decode(*args)

def typeCast(value):
    return typeCast(value)