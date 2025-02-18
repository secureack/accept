import psutil

from core import globalSettings, globalLogger, objectCache
import core.pipelines

def start(pipelines):
    id, pipeline, name, *_ = globalSettings.args.cache.split(".")
    setattr(globalSettings.args,"pipeline",pipeline)
    pipeline = [ x for x in pipelines if x.name == name ][0]
    pipeline.process()

    if globalSettings.args.pipeline_time:
        for id, objectClass in core.pipelines.objectCache.objectCache.items():
            globalLogger.logger.log(100,"Process Stats",{ "stats" : objectClass.processStats() },extra={ "source" : "process", "type" : "stats" })
    globalLogger.logger.log(6,"Memory Stats", { "rss": psutil.Process().memory_info().rss }, extra={ "source" : "runtime", "type" : "memory" })
