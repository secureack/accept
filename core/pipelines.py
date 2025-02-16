from core import plugins, globalLogger
import classes.input
import classes.processor
import classes.output

objectCache = {}

def load(pipeline):
    global objectCache
    inputClasses = []
    for input in [ x for x in pipeline.values() if x["type"] == "input" ]:
        try:
            inputClass = plugins.available["input"][input["plugin"]](name=input["name"],id=input["id"],**input["properties"])
        except KeyError:
            globalLogger.logger.error(f"input plugin {input['plugin']} not found")
            inputClass = classes.input.input(name=input["name"],id=input["id"],**input["properties"])
        objectCache[input["id"]] = inputClass
        inputClasses.append(inputClass)
        processList = [ (inputClass,x) for x in input["next"] ]
        while len(processList) > 0:
            processItem = processList.pop()
            currentClass = processItem[0]
            try:
                nextItem = pipeline[processItem[1]]
            except KeyError:
                globalLogger.logger.error(f"pipeline item {processItem[1]} not found")
                continue
            try:
                nextClass = objectCache[nextItem["id"]]
            except KeyError:
                try:
                    nextClass = plugins.available[nextItem["type"]][nextItem["plugin"]](id=nextItem["id"],**nextItem["properties"])
                except KeyError:
                    globalLogger.logger.error(f"{nextItem['type']} plugin {nextItem['plugin']} not found")
                    if nextItem["type"] == "processor":
                        nextClass = classes.processor.processor(id=nextItem["id"],**nextItem["properties"])
                    elif nextItem["type"] == "output":
                        nextClass = classes.output.output(id=nextItem["id"],**nextItem["properties"])
                if nextItem["type"] == "processor" and nextClass.next:
                    nextItem["next"] = nextClass.next
                    nextClass.next = None
                objectCache[nextItem["id"]] = nextClass
            if currentClass.next and ( nextClass.nextBehavior == 1 or nextClass not in currentClass.next ):
                currentClass.next.append(nextClass)
            else:
                currentClass.next = [nextClass]
            processList += [ (nextClass,x) for x in nextItem["next"] ]
    return inputClasses