def split(string,splitOn,position=None):
    try:
        if position != None:
            return string.split(splitOn)[position]
        return string.split(splitOn)
    except:
        return ""

def splitLines(string,r=False):
    try:
        if r:
            return string.split("\r\n")
        else:
            return string.split("\n")
    except:
        return ""

def strCount(string,searchString):
    try:
        return string.count(searchString)
    except:
        return 0

def join(stringList,by=None):
    try:
        if by:
            return by.join(stringList)
        else:
            return "".join(stringList)
    except:
        stringList = [ str(item) for item in stringList ]
        if by:
            return by.join(stringList)
        else:
            return "".join(stringList)

def concat(*args):
    stringResult = ""
    try:
        for arg in args:
            stringResult += str(arg)
        return stringResult
    except:
        return stringResult

def strLower(string):
    try:
        return string.lower()
    except:
        return string

def replace(string,match,replacement):
    try:
        return string.replace(match,replacement)
    except:
        return string

def strip(string,stripOn=""):
    try:
        if stripOn:
            return string.strip(stripOn)
        return string.strip()
    except:
        return string
    
def startsWith(string, startswithString):
    try:
        return string.startswith(startswithString)
    except:
        return False
    
def endsWith(string, endswithString):
    try:
        return string.endswith(endswithString)
    except:
        return False
