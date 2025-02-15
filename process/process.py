import psutil

from core import globalSettings, globalLogger
import core.pipelines

def start(pipelines):
    id, pipeline, name, *_ = globalSettings.args.cache.split(".")
    pipeline = [ x for x in pipelines if x.name == name ][0]
    pipeline.process()

    if globalSettings.args.pipeline_time:
        for id, objectClass in core.pipelines.objectCache.items():
            globalLogger.logger.info("Process Stats",objectClass.processStats())
    globalLogger.logger.info("Memory Stats", { "rss": psutil.Process().memory_info().rss })
