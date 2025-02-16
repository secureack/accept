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
    event = objectClass.process(event)
    print(f"Event type: {type(event).__name__}")
    if type(event) is dict:
        print(f"Event: {json.dumps(event)}")
    else:
        print(f"Event: {event}")