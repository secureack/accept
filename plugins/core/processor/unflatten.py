from classes import processor

class unflatten(processor.processor):
    
    def process(self,event):
        if type(event) is dict:
            newEvent = {}
            for key, value in event.items():
                parts = key.split('.')
                currentPart = newEvent
                try:
                    for part in parts[:-1]:
                        if part not in currentPart:
                            currentPart[part] = {}
                        currentPart = currentPart[part]
                    currentPart[parts[-1]] = value
                except:
                    newEvent[key] = value
            return newEvent
        return event
