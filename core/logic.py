import re
import logging

from core import globalSettings, functions, typecast

logger = logging.getLogger(__name__)
logger.setLevel(globalSettings.args.log_level)

complied = {}

class typeCastType():
    def __init__(self,varString):
        self.varString = varString

    def get(self,dicts=None):
        return typecast.dynamic(self.varString,dicts,functionSafeList=functions.available)

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
                statement[x] = typecast.typeCast(statement[x],dicts,functions.available)
            tempLogic = tempLogic.replace(logicMatch.group(0),str(logicProcess(statement)))
        # Checking that result only includes True, False, ( ), or, and,
        if regexLogicSafeValidationString.search(tempLogic):
            result = eval(tempLogic) # Can be an unsafe call be very careful with this!
            return result
        else:
            logger.log(50,"Unsafe logic eval",{ "tempLogic" : tempLogic },extra={ "source" : "logic", "type" : "unsafe" })
    return False

def compileIf(logicString):
    statements = []
    if "if " == logicString[:3]:
        # statement = None
        logicMatches = regexLogicString.finditer(logicString[3:])
        for index, logicMatch in enumerate(logicMatches, start=1):
            statement = [logicMatch.group(1).strip(),logicMatch.group(17).strip(),logicMatch.group(16).strip()]
            # Cast typing statement vars
            for x in range(0,2):
                statement[x] = typecast.simple(statement[x])
                if typecast.regexDict.match(statement[x]) or typecast.regexFunction.match(statement[x]):
                    statement[x] = typeCastType(statement[x])
            if statement[2] == "match" or statement[2] == "not match":
                if statement[1] not in complied:
                    complied[statement[1]] = re.compile(statement[1])
            statements.append([logicMatch.group(0),statement])
    return statements

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
