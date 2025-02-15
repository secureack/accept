import time
import threading
import os

from core import globalLogger, globalSettings
import accept.queue as queue

def start(pipelines):
    retryBuffer(True)
    lastRetryCheck = time.time()
    for pipeline in pipelines:
        globalLogger.logger.info(f"starting pipeline: {pipeline}")
        threading.Thread(target=pipeline.start, args=()).start()
    while len([ x for x in pipelines if x.running ]) > 0:
        if lastRetryCheck + 60 < time.time():
            retryBuffer()
            lastRetryCheck = time.time()
        queue.process()
        globalLogger.logger.info("Queue Stats",{ "queue" : { "running" : len(queue.taskPool.running), "waiting" : len(queue.taskPool.waiting) }, "pipelines" : { "running" : len([ x for x in pipelines if x.running ]) } })
        time.sleep(1)

def retryBuffer(includeBuild=False):
    for cacheFile in os.listdir(globalSettings.args.cache_dir):
        id, pipeline, name, *_ = cacheFile.split(".")
        if pipeline == globalSettings.args.pipeline:
            if cacheFile.endswith(".cache") or ( includeBuild and cacheFile.endswith(".build")):
                queue.register(cacheFile)