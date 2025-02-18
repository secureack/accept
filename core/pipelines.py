from core import plugins, globalLogger, objectCache
import classes.input
import classes.processor
import classes.output

def load(pipeline):
    inputClasses = []
    for input in [ x for x in pipeline.values() if x["type"] == "input" ]:
        try:
            inputClass = plugins.available["input"][input["plugin"]](name=input["name"],id=input["id"],**input["properties"])
        except KeyError:
            globalLogger.logger.log(100,"Plugin Not Found",{ "plugin" : input['plugin'] },extra={ "source" : "pipeline", "type" : "error" })
            exit(5)
            inputClass = classes.input.input(name=input["name"],id=input["id"],**input["properties"])
        objectCache.objectCache[input["id"]] = inputClass
        inputClasses.append(inputClass)
        processList = [ (inputClass,x) for x in input["next"] ]
        while len(processList) > 0:
            processItem = processList.pop()
            currentClass = processItem[0]
            try:
                nextItem = pipeline[processItem[1]]
            except KeyError:
                globalLogger.logger.log(25,"WARNING: Config error referenced item not found",{ "item" : processItem[1] },extra={ "source" : "pipeline", "type" : "error" })
                continue
            try:
                nextClass = objectCache.objectCache[nextItem["id"]]
            except KeyError:
                try:
                    nextClass = plugins.available[nextItem["type"]][nextItem["plugin"]](id=nextItem["id"],**nextItem["properties"])
                except KeyError:
                    globalLogger.logger.log(100,"Plugin Not Found",{ "plugin" : nextItem['plugin'] },extra={ "source" : "pipeline", "type" : "error" })
                    exit(5)
                if nextItem["type"] == "processor" and nextClass.next:
                    nextItem["next"] = nextClass.next
                    nextClass.next = None
                objectCache.objectCache[nextItem["id"]] = nextClass
            if currentClass.next and ( nextClass.nextBehavior == 1 or nextClass not in currentClass.next ):
                currentClass.next.append(nextClass)
            else:
                currentClass.next = [nextClass]
            processList += [ (nextClass,x) for x in nextItem["next"] ]
    return inputClasses