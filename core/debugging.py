import threading
import time

from . import globalLogger, globalSettings

if globalSettings.args.debug_memory:
    globalLogger.logger.info("Debugger debug_memory started")

    import tracemalloc
    import gc
    import uuid
    import os
    import glob
    import psutil

    tracemalloc.start()

    def memory():
        while True:
            snapshot = tracemalloc.take_snapshot()
            snapshot = snapshot.filter_traces(( 
                tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
                tracemalloc.Filter(False, "<frozen importlib._bootstrap_external>"),
                tracemalloc.Filter(False, "<unknown>")
            ))
            top_stats = snapshot.statistics('lineno')
            output = []
            for stat in top_stats[:25]:
                output.append({ "trace" : stat.traceback.format(), "size" : stat.size, "count" : stat.count })
            process = psutil.Process()
            globalLogger.logger.info(f"debug_memory - rss: {process.memory_full_info().rss}, vms: {process.memory_full_info().vms}, uss: {process.memory_full_info().uss}, pss: {process.memory_full_info().pss}, limit: {tracemalloc.get_traceback_limit()}, traced_memory: {tracemalloc.get_traced_memory()}, trace_usage: {tracemalloc.get_tracemalloc_memory()}, gc_enabled: {gc.isenabled()}, gc_stats: {gc.get_stats()}, gc_length: {len(gc.get_objects())}, gc_garbage_length: {len(gc.garbage)}, snapshot: {output}")
            time.sleep(15)

    threading.Thread(target=memory, args=()).start()
