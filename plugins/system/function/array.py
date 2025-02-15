import re

def index(array,*args):
    tempArray = array
    try:
        for arg in args:
            tempArray = tempArray[arg]
    except:
        return None
    return tempArray

def listMatch(array, key, value, regex=False):
    def getNestedValue(dict, keys):
        result = dict
        for key in keys:
            result = result[key]
        return result

    try:
        if type(key) is list:
            if regex:
                results = len(list(filter(lambda item: re.search(value,str(getNestedValue(item, key))), array)))
            else:
                results = len(list(filter(lambda item: getNestedValue(item, key) == value, array)))
        else:
            if regex:
                results = len(list(filter(lambda item: re.search(value,str(item[key])), array)))
            else:
                results = len(list(filter(lambda item: item[key] == value, array)))
    except:
        results = 0

    if results > 0:
        return True
    return False
