import uuid
import os
import time
from pathlib import Path
import threading

from core import globalSettings, globalLogger, objectCache
from accept import queue
from process import postRegister
from classes import base

class input(base.base):
    next = None

    def __init__(self,name=None,**kwargs):
        self.id = kwargs.get("id")
        self.name = name
        self.running = False
        self.logger = globalLogger.getLogger(__name__,kwargs.get("log_level",globalSettings.args.log_level))
        self.flushInterval = kwargs.get("flush_interval",60)
        self.flushEvery = kwargs.get("flush_every",1000000)
        self.nextError = kwargs.get("next_error",None)
        super().__init__(**kwargs)

    def start(self):
        self.running = True
        self.rotateCache()
        self.lock = threading.Lock()
        threading.Thread(target=self.cacheRotator, args=()).start()

    def stop(self):
        self.running = False
        self.rotateCache(createNew=False)

    def cacheRotator(self):
        while self.running:
            time.sleep(self.flushInterval)
            with self.lock:
                if time.time() - self.cacheWriter["createdTime"] >= self.flushInterval:
                    self.rotateCache()

    def rotateCache(self,createNew=True):
        try:
            if self.cacheWriter["file"]:
                self.cacheWriter["file"].close()
                self.cacheWriter["file"] = None
                os.rename(self.cacheWriter["filePath"],f"{self.cacheWriter['filePath'][:-len('.build')]}.cache")
                if self.cacheWriter["totalEvents"] == 0:
                    os.remove(f"{self.cacheWriter['filePath'][:-len('.build')]}.cache")
                else:
                    queue.register(f"{self.cacheWriter['filePath'][:-len('.build')]}.cache".split("/")[-1])
        except AttributeError:
            pass
        except Exception as e:
            self.logger.log(25,f"Exception",{ "name" : self.name, "id" : self.id },extra={ "source" : "input", "type" : "exception" },exc_info=True)
        filePath = str(Path(f"{globalSettings.args.cache_dir}/{uuid.uuid4()}.{globalSettings.args.pipeline}.{self.name}.build"))
        self.cacheWriter = {
            "createdTime" : time.time(),
            "filePath" : filePath,
            "file" : open(filePath,"wb") if createNew else None,
            "firstEvent" : 0,
            "lastEvent" : 0,
            "totalEvents" : 0
        }

    def process(self):
        startTime = time.perf_counter()
        cacheFile = os.path.join(globalSettings.args.cache_dir, globalSettings.args.cache)
        if os.path.exists(cacheFile): 
            with open(cacheFile) as f:
                for event in f:
                    eventStartTime = time.perf_counter_ns()
                    try:
                        for next in self.next if self.next else []:
                            int("a")
                            next.processHandler(event.strip(),stack=[self.id])
                    except:
                        if self.nextError and self.nextError in objectCache.objectCache:
                            objectCache.objectCache[self.nextError].processHandler(event.strip(),stack=[self.id])
                        else:
                            raise
                    self.updateProcessStats(eventStartTime)
            for item in postRegister.items:
                item()
            os.remove(cacheFile)
        else:
            self.logger.log(50,f"Cache file does not exist",{ "name" : self.name, "id" : self.id, "cache" : globalSettings.args.cache },extra={ "source" : "cache", "type" : "exception" })
        self.logger.log(7,f"Cache file processed",{ "name" : self.name, "id" : self.id, "cache" : globalSettings.args.cache, "took" : time.perf_counter() - startTime },extra={ "source" : "cache", "type" : "stats" })

    def event(self,event):
        event = event.strip()
        with self.lock:
            if event:
                self.cacheWriter["file"].write(f"{event}\n".encode())
                if self.cacheWriter["totalEvents"] == 0:
                    self.cacheWriter["firstEvent"] = time.time()
                elif self.flushEvery > 0 and self.cacheWriter["totalEvents"] > self.flushEvery:
                    self.rotateCache()
                self.cacheWriter["totalEvents"] += 1
                self.cacheWriter["lastEvent"] = time.time()