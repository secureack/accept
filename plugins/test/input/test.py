from pathlib import Path
import time

from classes import input

class test(input.input):

    def __init__(self,path,**kwargs):
        self.eventsPath = path
        self.loop = kwargs.get("loop",False)
        self.loopDelay = kwargs.get("loop_delay",5)
        super().__init__(**kwargs)

    def start(self):
        super().start()
        while self.running and self.loop:
            try:
                with open(Path(self.eventsPath),"r") as f:
                    for e in f.readlines():
                        self.event(e)
                time.sleep(self.loopDelay)
            except Exception as e:
                self.logger.log(50,f"Exception occurred {e}")