import json

from core import globalSettings, pipelines

def test():
    objectClass = pipelines.objectCache[globalSettings.args.id]
    objectClass.next = []
    event = globalSettings.args.event
    if event.endswith(".event"):
        with open(event,"r") as file:
            event = file.read()
    if globalSettings.args.event_json:
        event = json.loads(event)
    print(f"LOADED EVENT | event({type(event).__name__}) | {event}")
    event = objectClass.process(event)
    print(f"PROCESSED EVENT | event({type(event).__name__}) | {event}")
