import re
import functools
import logging
import json

from core import globalSettings, functions

logger = logging.getLogger(__name__)
logger.setLevel(globalSettings.args.log_level)

regexEvalString = re.compile(r"(%%(.*?)%%)",re.DOTALL)
regexDict = re.compile(r"^([a-zA-Z]+)((\[[^\]]*?\])|\])+$")
regexDictKeys = re.compile(r"(\[\"?([^\]\"]*)\"?\])")
regexDictOpen = re.compile(r"^([a-zA-Z0-9]+)\[.*")
regexFunctionKwarg = re.compile(r"^([a-zA-Z0-9_]+)=(.*)")
regexFunction = re.compile(r"^([a-zA-Z0-9_]+)\([\S\s]*\)")
regexFunctionOpen = re.compile(r"(^|[a-zA-Z0-9_]+=)([a-zA-Z0-9_]*)\(.*")
regexInt = re.compile(r"^(-|)[0-9]+$")
regexFloat = re.compile(r"^(-|)[0-9]+\.[0-9]+$")
regexString = re.compile(r"^\".*\"$")
regexJson = re.compile(r"^(\{.*\}|\[.*\])$")

complied = {}

class typeCastType():
    def __init__(self,varString):
        self.varString = varString

    def get(self,dicts=None):
        return self.typeCast(self.varString,dicts,functionSafeList=functions.available)
    
    def typeCast(self,varString:str,dicts:dict=None,functionSafeList:dict=functions.available):
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
                        logger.error(f"Function exception {e}")
                else:
                    logger.warning("Function is not a valid function {}".format({ "function_name" : functionName }))
        # Default to exsiting
        return varString

def preTypeCast(varString):
    if type(varString) == str and varString:
        # String defined
        if varString[0] == "\"" and varString[-1] == "\"":
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
        # Dict
        if regexDict.match(varString):
            return typeCastType(varString)
        # Attempt to cast dict and list
        if regexJson.match(varString):
            try:
                return json.loads(varString)
            except:
                pass
        # %% %%
        if varString.startswith("%%") and varString.endswith("%%"):
            return typeCastType(varString)
        # Function
        if regexFunction.match(varString):
            return typeCastType(varString)
    # Default to exsiting
    return varString

def typeCast(varString:str,dicts:dict=None,functionSafeList:dict=functions.available):
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
                    return typeCast(nested_dict_get(dicts[dictName],dictKeys))
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
        # String defined
        if varString[0] == "\"" and varString[-1] == "\"":
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
        # Attempt to cast dict and list
        if regexJson.match(varString):
            try:
                return json.loads(varString)
            except:
                pass
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
                    logger.log(25,f"Function Exception",extra={ "source" : "function", "type" : "exception" },exc_info=True)
            else:
                logger.log(25,f"Function not found",{ "function_name" : functionName },extra={ "source" : "function", "type" : "exception" })
    # Default to exsiting
    return varString


regexLogicString = re.compile(r'((\"(.*?\\\\\"|(.*?[^\\])\")|([a-zA-Z0-9]+(\[(.*?)\])+)|(%%(.*?)%%)|([a-zA-Z0-9]+(\((.*?)(\)\)|\)))+)|\[(.*?)\]|([a-zA-Z0-9\.\-]*)))\s?( not match | match | not in | in |==|!=|>=|>|<=|<)\s?((\"(.*?\\\\\"|(.*?[^\\])\")|(%%(.*?)%%)|([a-zA-Z0-9]+(\[(.*?)\])+)|([a-zA-Z0-9]+(\((.*?)(\)\)|\))(|$))+)|\[(.*?)\]|([a-zA-Z0-9\.\-]*)))',re.DOTALL)
regexLogicSafeValidationString = re.compile(r'^(True|False|\(|\)| |or|and|not)*$')

def ifEval(logicString,dicts=None):
    if "if " == logicString[:3]:
        tempLogic = logicString[3:]
        # statement = None
        logicMatches = regexLogicString.finditer(tempLogic)
        for index, logicMatch in enumerate(logicMatches, start=1):
            statement = [logicMatch.group(1).strip(),logicMatch.group(17).strip(),logicMatch.group(16).strip()]
            # Cast typing statement vars
            for x in range(0,2):
                statement[x] = typeCast(statement[x],dicts,functions.available)
            tempLogic = tempLogic.replace(logicMatch.group(0),str(logicProcess(statement)))
        # Checking that result only includes True, False, ( ), or, and,
        if regexLogicSafeValidationString.search(tempLogic):
            result = eval(tempLogic) # Can be an unsafe call be very careful with this!
            return result
        else:
            logger.log(50,"Unsafe logic eval",{ "tempLogic" : tempLogic },extra={ "source" : "logic", "type" : "unsafe" })
    return False

def compliedEval(logicString,statements,dicts=None):
    if "if " == logicString[:3]:
        tempLogic = logicString[3:]
        for statement in statements:
            newStatement = [None,None,statement[1][2]]
            for x in range(0,2):
                newStatement[x] = statement[1][x] if type(statement[1][x]) is not typeCastType else statement[1][x].get(dicts)
            tempLogic = tempLogic.replace(statement[0],str(logicProcess(newStatement)))
        if regexLogicSafeValidationString.search(tempLogic):
            result = eval(tempLogic) # Can be an unsafe call be very careful with this!
            return result
        else:
            logger.log(50,"Unsafe logic eval",{ "tempLogic" : tempLogic },extra={ "source" : "logic", "type" : "unsafe" })
    return False

def logicProcess(statement):
    try:
        if statement[2] == "==":
            return (statement[0] == statement[1])
        elif statement[2] == "!=":
            return (statement[0] != statement[1])
        elif statement[2] == ">":
            return (statement[0] > statement[1])
        elif statement[2] == ">=":
            return (statement[0] >= statement[1])
        elif statement[2] == "<":
            return (statement[0] < statement[1])
        elif statement[2] == "<=":
            return (statement[0] <= statement[1])
        elif statement[2] == "in":
            return (statement[0] in statement[1])
        elif statement[2] == "not in":
            return (statement[0] not in statement[1])
        elif statement[2] == "match":
            if complied[statement[1]].search(statement[0]):
                return True
            else:
                return False
        elif statement[2] == "not match":
            if complied[statement[1]].search(statement[0]):
                return False
            else:
                return True
        else:
            return False
    except:
        return False