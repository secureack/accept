import time
import threading
import os

from core import globalLogger, globalSettings
import accept.queue as queue

def start(pipelines):
    retryBuffer(True)
    startTime = time.time()
    for pipeline in pipelines:
        globalLogger.logger.log(7,"starting input",{ "id" : pipeline.id, "name" : pipeline.name},extra={ "source" : "pipeline", "type" : "start" })
        threading.Thread(target=pipeline.start, args=()).start()
    lastRetryCheck = startTime
    while len([ x for x in pipelines if x.running ]) > 0 or time.time() - startTime < 10:
        if lastRetryCheck + 60 < time.time():
            retryBuffer()
            lastRetryCheck = time.time()
        queue.process()
        globalLogger.logger.log(6,"Queue Stats",{ "queue" : { "running" : len(queue.taskPool.running), "waiting" : len(queue.taskPool.waiting) }, "pipelines" : { "running" : len([ x for x in pipelines if x.running ]) } },extra={ "source" : "pipeline", "type" : "stats" })
        time.sleep(1)

def retryBuffer(includeBuild=False):
    for cacheFile in os.listdir(globalSettings.args.cache_dir):
        if cacheFile.endswith(".cache") or ( includeBuild and cacheFile.endswith(".build")):
            id, pipeline, name, *_ = cacheFile.split(".")
            if pipeline == globalSettings.args.pipeline:
                queue.register(cacheFile)