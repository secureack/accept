import re

regexLogicString = re.compile(r'((\"(.*?\\\\\"|(.*?[^\\])\")|([a-zA-Z0-9]+(\[(.*?)\])+)|(%%(.*?)%%)|([a-zA-Z0-9]+(\((.*?)(\)\)|\)))+)|\[(.*?)\]|([a-zA-Z0-9\.\-]*)))\s?( not match | match | not in | in |==|!=|>=|>|<=|<)\s?((\"(.*?\\\\\"|(.*?[^\\])\")|(%%(.*?)%%)|([a-zA-Z0-9]+(\[(.*?)\])+)|([a-zA-Z0-9]+(\((.*?)(\)\)|\))(|$))+)|\[(.*?)\]|([a-zA-Z0-9\.\-]*)))',re.DOTALL)

def parse(inputString):
    strippedInput = inputString.strip()
    if strippedInput.lower().startswith("if "):
        strippedInput = strippedInput[3:].strip()
    logicTokens = []
    currentIndex = 0
    while currentIndex < len(strippedInput):
        if strippedInput[currentIndex] in ("(", ")"):
            logicTokens.append(strippedInput[currentIndex])
            currentIndex += 1
        elif strippedInput[currentIndex:currentIndex+2].lower() == "or" and (currentIndex+2 == len(strippedInput) or not strippedInput[currentIndex+2].isalnum()):
            logicTokens.append("or")
            currentIndex += 2
        elif strippedInput[currentIndex:currentIndex+3].lower() == "and" and (currentIndex+3 == len(strippedInput) or not strippedInput[currentIndex+3].isalnum()):
            logicTokens.append("and")
            currentIndex += 3
        else:
            matchResult = regexLogicString.match(strippedInput, currentIndex)
            if matchResult:
                leftOperand = matchResult.group(1).strip()
                operator = matchResult.group(16).strip()
                rightOperand = matchResult.group(17).strip()
                logicTokens.append([leftOperand, operator, rightOperand])
                currentIndex = matchResult.end()
            else:
                currentIndex += 1  # skip unknown character

    def nestLogic(tokenList):
        stack = []
        currentGroup = []
        currentOperator = None
        tokenIndex = 0
        while tokenIndex < len(tokenList):
            token = tokenList[tokenIndex]
            if token == "(":
                depth = 1
                searchIndex = tokenIndex + 1
                while searchIndex < len(tokenList):
                    if tokenList[searchIndex] == "(":
                        depth += 1
                    elif tokenList[searchIndex] == ")":
                        depth -= 1
                        if depth == 0:
                            break
                    searchIndex += 1
                group = nestLogic(tokenList[tokenIndex+1:searchIndex])
                currentGroup.append(group)
                tokenIndex = searchIndex
            elif token in ("or", "and"):
                currentOperator = token
            else:
                currentGroup.append(token)
            tokenIndex += 1

        if currentOperator:
            return {currentOperator: [item if isinstance(item, dict) else item for item in currentGroup if item != currentOperator]}
        elif len(currentGroup) == 1:
            return currentGroup[0]
        else:
            return currentGroup

    nestedLogic = nestLogic(logicTokens)
    return {"logic": [nestedLogic]}