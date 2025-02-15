import subprocess
import time
import os
import sys
import resource

from core import globalLogger, globalSettings

PASSTHROUGH_ARGS = {
    "log_level" : "INFO",
    "cache_dir" : "cache",
    "config" : ""
}
WORKER_START_CMDLINE = f"python3 {sys.argv[0]} process " + " ".join([ f"--{arg} {getattr(globalSettings.args,arg)}" for arg, default in PASSTHROUGH_ARGS.items() if getattr(globalSettings.args,arg) != default ])

def limitVirtualMemory():
    resource.setrlimit(resource.RLIMIT_AS, (globalSettings.args.flush_thread_max_memory, resource.RLIM_INFINITY))

if globalSettings.args.debug:
    WORKER_START_CMDLINE = WORKER_START_CMDLINE.replace("python3","python3 -Xfrozen_modules=off")

class Process:
    pid:int
    startTime:float
    cache:str
    process:subprocess.Popen

    def __init__(self, cache:str) -> None:
        self.cache = cache
        self.process = subprocess.Popen(f"{WORKER_START_CMDLINE} --cache {cache}".split(" "),start_new_session=False,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,preexec_fn=limitVirtualMemory)
        os.set_blocking(self.process.stdout.fileno(), False)
        self.startTime = time.time()
        self.pid = self.process.pid

class TaskPool:
    running:list[Process]
    waiting:set

    def __init__(self) -> None:
        self.running = []
        self.waiting = set()

taskPool = TaskPool()

def remainingCapacity(includeWaiting=True) -> int:
    if includeWaiting:
        return globalSettings.args.flush_threads - ( len(taskPool.running) + len(taskPool.waiting) )
    else:
        return globalSettings.args.flush_threads - len(taskPool.running)

def register(cache:str):
    if cache not in taskPool.waiting and not any([ x.cache == cache for x in taskPool.running ]):
        taskPool.waiting.add(cache)
    globalLogger.logger.info("Task Registered",{ "cache" : cache, })

def kill(cache: str):
    for task in taskPool.waiting:
        if task == cache:
            taskPool.waiting.remove(task)
            return True
    for process in taskPool.running:
        if process.cache == cache:
            process.process.terminate()
            taskPool.running.remove(process)
            return True
    return False

def process():
    try:
        while remainingCapacity(False) > 0 and len(taskPool.waiting) > 0:
            cache = taskPool.waiting.pop()
            process = Process(cache)
            taskPool.running.append(process)
            globalLogger.logger.info("Worker Started",{ "cache" : cache, "pid" : process.pid })
    except IndexError:
        pass

    for process in taskPool.running:
        running = True if process.process.poll() == None else False
        for line in iter(process.process.stdout.readline, b''):
            sys.stdout.write(line.decode("utf-8"))
        if running and time.time() - process.startTime > ( process.startTime + globalSettings.args.flush_timeout ):
            process.process.terminate()
            globalLogger.logger.warning("Worker Killed",{ "cache" : process.cache, "pid" : process.process.pid })
        if not running:
            for line in iter(process.process.stdout.readline, b''):
                sys.stdout.write(line.decode("utf-8"))
            sys.stdout.flush()
            globalLogger.logger.info("Worker Ended",{ "cache" : process.cache, "pid" : process.process.pid })
            taskPool.running.remove(process)
            break