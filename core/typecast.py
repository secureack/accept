import re
import json
import functools

from core import functions, globalLogger

regexEvalString = re.compile(r"(%%(.*?)%%)",re.DOTALL)
regexDict = re.compile(r"^([a-zA-Z]+)((\[[^\]]*?\])|\])+$")
regexDictKeys = re.compile(r"(\[\"?([^\]\"]*)\"?\])")
regexDictOpen = re.compile(r"^([a-zA-Z0-9]+)\[.*")
regexFunctionKwarg = re.compile(r"^([a-zA-Z0-9_]+)=(.*)")
regexFunction = re.compile(r"^([a-zA-Z0-9_]+)\([\S\s]*\)")
regexFunctionOpen = re.compile(r"(^|[a-zA-Z0-9_]+=)([a-zA-Z0-9_]*)\(.*")
regexCommor = re.compile(r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)")
regexInt = re.compile(r"^(-|)[0-9]+$")
regexFloat = re.compile(r"^(-|)[0-9]+\.[0-9]+$")
regexString = re.compile(r"^\".*\"$")
regexJson = re.compile(r"^(\{.*\}|\[.*\])$")

def typeCast(varString:str,dicts:dict=None,functionSafeList:dict=functions.available):
    if type(varString) == str and varString:
        if varString[0] == "\"" and varString[-1] == "\"":
            return str(varString[1:-1])
    varString = simple(varString)
    if type(varString) == str:
        varString = dynamic(varString,dicts,functionSafeList)
    return varString

def simple(varString:str):
    if type(varString) == str and varString:
        if (varString[0] == "\"" and varString[-1] == "\"") or (varString[0] == "'" and varString[-1] == "'"):
            return str(varString[1:-1])
        # Int
        if regexInt.match(varString):
            return int(varString)
        # Float
        if regexFloat.match(varString):
            return float(varString)
        # Bool
        lower = varString.lower()
        if lower == "true":
            return True
        if lower == "false":
            return False
        # None
        if lower == "none" or lower == "null":
            return None
        # Attempt to cast dict and list
        if varString[0] == "{" or varString[0] == "[":
            try:
                return json.loads(varString)
            except:
                pass
    # Default to existing
    return varString

def dynamic(varString:str,dicts:dict=None,functionSafeList:dict=functions.available):
    def getDictValue(varString:str,dicts:dict=None):
        def nested_dict_get(dictionary, keys):
            return functools.reduce(lambda d, key: d.get(key) if d else None, keys, dictionary)
        if regexDict.search(varString):
            dictName = varString.split("[")[0]
            if dictName in dicts:
                dictKeys = []
                for key in regexDictKeys.findall(varString):
                    dictKeys.append(key[1])
                try:
                    return nested_dict_get(dicts[dictName],dictKeys)
                except AttributeError:
                    try:
                        currentValue = dicts[dictName]
                        for key in dictKeys:
                            if type(currentValue) is dict:
                                currentValue = currentValue[key]
                            elif type(currentValue) is list:
                                currentValue = currentValue[int(key)]
                            else:
                                return None
                    except:
                        return None
                    return currentValue
        return None
    if type(varString) == str and varString:
        # Dict
        if regexDict.match(varString):
            dictName = varString.split("[")[0]
            dictValue = varString[(len(dictName)):]
            dictKeys = []
            tempKey = ""
            index = 0
            while index <= len(dictValue)-1:
                keyFound = 0
                while index <= len(dictValue)-1:
                    if keyFound > 0:
                        tempKey += dictValue[index]
                        index += 1
                        if dictValue[index] == "[":
                            keyFound += 1
                        elif dictValue[index] == "]":
                            keyFound -= 1
                            if keyFound == 0:
                                break
                    elif dictValue[index] == "[":
                        if tempKey:
                            tempKey += dictValue[index]
                        index += 1
                        if regexDictOpen.search(tempKey):
                            keyFound = 2
                    elif dictValue[index] != "]":
                        tempKey += dictValue[index]
                        index += 1
                    else:
                        break

                if tempKey != "":
                    value = typeCast(tempKey.strip(),dicts,functionSafeList)
                    dictKeys.append(value)
                    tempKey = ""
                index+=1

            dictString = f"{dictName}"
            for key in dictKeys:
                dictString += f"[{key}]"
            return getDictValue(dictString,dicts)
        # %% %%
        if varString.startswith("%%") and varString.endswith("%%"):
            return typeCast(varString.split("%%")[1],dicts,functionSafeList)
        # Function
        if regexFunction.match(varString):
            functionName = varString.split("(")[0]
            if functionName in functionSafeList:
                functionValue = varString[(len(functionName)+1):-1]
                functionArgs = []
                functionKwargs = {}
                tempArg = ""
                index = 0
                # Decoding string function arguments to single arguments for typeCasting - Regex maybe faster but has to handle encaspulation of " \" [ ' (, old search regex only worked with "
                while index <= len(functionValue)-1:
                    if functionValue[index] == "\"":
                        tempArg += functionValue[index]
                        index += 1
                        while index <= len(functionValue)-1:
                            if functionValue[index] != "\"":
                                tempArg += functionValue[index]
                                index += 1
                            else:
                                tempArg += functionValue[index]
                                if (functionValue[index-1] != "\\") or (functionValue[index-1] == "\\" and functionValue[index-2] == "\\"):
                                    tempArg = tempArg.replace("\\\\","\\")
                                    break
                                # \" remove escape \ so string is "
                                elif functionValue[index-1] == "\\":
                                    tempArg = tempArg[:-2] + functionValue[index]
                                index += 1
                    elif functionValue[index] == "[":
                        while index <= len(functionValue)-1:
                            if functionValue[index] != "]":
                                tempArg += functionValue[index]
                                index += 1
                            else:
                                tempArg += functionValue[index]
                                index += 1
                                break
                    else:
                        functionFound = 0
                        inQuote = False
                        while index <= len(functionValue)-1:
                            if functionFound > 0:
                                if functionValue[index] == "\"":
                                    if functionValue[index-1] != "\\" and functionValue[index-2] != "\\":
                                        inQuote = not inQuote
                                if not inQuote: 
                                    if functionValue[index] == "(":
                                        functionFound += 1
                                    elif functionValue[index] == ")":
                                        functionFound -= 1
                                        if functionFound == 0:
                                            tempArg += functionValue[index]
                                            index += 1
                                            break
                                tempArg += functionValue[index]
                                index += 1
                            elif functionValue[index] == "(":
                                tempArg += functionValue[index]
                                index += 1
                                if regexFunctionOpen.search(tempArg.lstrip()):
                                    tempArg = tempArg.lstrip()
                                    functionFound += 1
                            elif functionValue[index] != "," and functionValue[index] != ")":
                                tempArg += functionValue[index]
                                index += 1
                            else:
                                break
                    
                    if tempArg.strip() != "":
                        kwargType = regexFunctionKwarg.match(tempArg)
                        if kwargType:
                            functionKwargs[kwargType.group(1)] = typeCast(kwargType.group(2),dicts,functionSafeList)
                        else:
                            functionArgs.append(typeCast(tempArg.strip(),dicts,functionSafeList))
                        tempArg = ""
                    index+=1
                # Catch any execution errors within functions
                try:
                    return functionSafeList[functionName](*functionArgs,**functionKwargs)
                except Exception as e:
                    globalLogger.logger.log(3,f"Function Exception",extra={ "source" : "function", "type" : "exception" },exc_info=True)
            else:
                globalLogger.logger.log(4,f"Function not found",{ "function_name" : functionName },extra={ "source" : "function", "type" : "exception" })
    # Default to existing
    return varString

def flatten(event):
    def flattenField(eventNest, prefix=""):
        fields = {}
        for field in eventNest:
            value = eventNest[field]
            if type(value) == dict:
                nested_fields = flattenField(value, f"{prefix}{field}.")
                fields.update(nested_fields)
            elif type(value) == list:
                fields[f"{prefix}{field}"] = f"{value}"
            else:
                fields[f"{prefix}{field}"] = value
        return fields
    return flattenField(event)

def getField(field, event):
    if type(event) is dict:
        if field in event:
            return event[field]
        else:
            if regexDict.match(field) or regexFunction.match(field):
                return dynamic(field,{ "data" : { "event" : event } },functions.available)
    return None

def setField(field, value, event):
    dicts = { "data" : { "event" : event } }
    if type(event) is dict:
        if field in event:
            event[field] = value
        else:
            if regexDict.match(field):
                dictName = field.split("[")[0]
                dictValue = field[(len(dictName)):]
                dictKeys = []
                tempKey = ""
                index = 0
                while index <= len(dictValue)-1:
                    keyFound = 0
                    while index <= len(dictValue)-1:
                        if keyFound > 0:
                            tempKey += dictValue[index]
                            index += 1
                            if dictValue[index] == "[":
                                keyFound += 1
                            elif dictValue[index] == "]":
                                keyFound -= 1
                                if keyFound == 0:
                                    break
                        elif dictValue[index] == "[":
                            if tempKey:
                                tempKey += dictValue[index]
                            index += 1
                            if regexDictOpen.search(tempKey):
                                keyFound = 2
                        elif dictValue[index] != "]":
                            tempKey += dictValue[index]
                            index += 1
                        else:
                            break
                    if tempKey != "":
                        dictKeys.append(tempKey.strip())
                        tempKey = ""
                    index += 1
                currentDict = dicts["data"]
                for key in dictKeys[:-1]:
                    if key not in currentDict:
                        currentDict[key] = {}
                    currentDict = currentDict[key]
                currentDict[dictKeys[-1]] = value