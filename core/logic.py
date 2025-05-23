import re
import logging
import operator

from core import globalSettings, functions, typecast

logger = logging.getLogger(__name__)
logger.setLevel(globalSettings.args.log_level)

OPERATORS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "in": lambda x, y: x in y,
    "not in": lambda x, y: x not in y,
    "match": lambda x, y: bool(re.fullmatch(y, x)),
    "not match": lambda x, y: not bool(re.fullmatch(y, x)),
}

def evaluateAnd(andStatement, dicts=None):
    operationList = []
    for statement in andStatement:
        if isinstance(statement, dict):
            operationList.append(statement)
        else:
            if not logicProcess(typecast.typeCast(statement[0], dicts), statement[1], typecast.typeCast(statement[2], dicts)):
                return False
    for operation in operationList:
        if "and" in operation:
            if not evaluateAnd(operation["and"], dicts):
                return False
        elif "or" in operation:
            if not evaluateOr(operation["or"], dicts):
                return False
    return True

def evaluateOr(orStatement, dicts=None):
    operationList = []
    for statement in orStatement:
        if type(statement) is dict:
            operationList.append(statement)
        else:
            if logicProcess(typecast.typeCast(statement[0], dicts), statement[1], typecast.typeCast(statement[2], dicts)):
                return True
    for operation in operationList:
        if "and" in operation:
            if evaluateAnd(operation["and"], dicts):
                return True
        elif "or" in operation:
            if evaluateOr(operation["or"], dicts):
                return True
    return False

def ifEval(logic, dicts=None):
    if type(logic) is dict:
        for logicSection in logic["logic"]:
            if type(logicSection) is list:
                if not logicProcess(typecast.typeCast(logicSection[0], dicts), logicSection[1], typecast.typeCast(logicSection[2], dicts)):
                    return False
            else:
                if "and" in logicSection:
                    if not evaluateAnd(logicSection["and"], dicts):
                        return False
                if "or" in logicSection:
                    if not evaluateOr(logicSection["or"], dicts):
                        return False
        return True
    return False

def logicProcess(value1, operator, value2):
    try:
        return OPERATORS[operator](value1, value2)
    except:
        print("Logic processing failed {}".format({ "statement" : (value1, value2, operator) }))
        return False