import time

from core import globalSettings

class base:
    nextBehavior = 0

    def __init__(self, *args, **kwargs):
        self._processStats = { 
            "time" : {
                "total": 0,
                "last": 0,
                "first": 0
            },
            "events" : {
                "count" : 0
            }
        }

    def processStats(self):
        return {
            "cache" : globalSettings.args.cache,
            "id" : self.id,
            "time" : {
                "total": self._processStats["time"]["total"],
                "last": self._processStats["time"]["last"],
                "first": self._processStats["time"]["first"],
                "average" : {
                    "1" : int(self._processStats["time"]["total"] / self._processStats["events"]["count"]),
                    "100" : int((self._processStats["time"]["total"] / self._processStats["events"]["count"]) * 100),
                    "1000" : int((self._processStats["time"]["total"] / self._processStats["events"]["count"]) * 1000)
                } if self._processStats["events"]["count"] > 0 else {}
                
            },
            "events" : {
                "count" : self._processStats["events"]["count"]
            }
        }
    
    def updateProcessStats(self,eventStartTime):
        self._processStats["time"]["total"] += time.perf_counter_ns() - eventStartTime
        self._processStats["time"]["last"] = time.perf_counter_ns() - eventStartTime
        if self._processStats["events"]["count"] == 0:
            self._processStats["time"]["first"] = time.perf_counter_ns() - eventStartTime
        self._processStats["events"]["count"] += 1