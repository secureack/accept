import argparse
import time

startTime = time.perf_counter()

mainParser = argparse.ArgumentParser(add_help=False)
mainParser.add_argument('--log_level', type=str, default="INFO", help='--log_level INFO')
mainParser.add_argument('--debug', type=bool, default=False, help='Flag to enable debug', nargs="?", const=True)
mainParser.add_argument('--debug_memory', type=bool, default=False, help='Flag to enable debug_memory', nargs="?", const=True)
mainParser.add_argument('--cache_dir', type=str, default="cache", help='--cache_dir <path_to_cache_dir>')
subParsers = mainParser.add_subparsers(help='commands')

acceptParser = subParsers.add_parser('accept', parents=[mainParser])
acceptParser.add_argument('--pipeline', type=str, default="", required=True, help='--pipeline <pipeline_name>')
acceptParser.add_argument('--config', type=str, default="", required=True, help='--config <path_to_config_file>')
acceptParser.add_argument('--flush_timeout', type=int, default=60, help='--flush_timeout <timeout_in_seconds>')
acceptParser.add_argument('--flush_threads', type=int, default=5, help='--flush_threads <number_of_threads>')
acceptParser.add_argument('--flush_thread_max_memory', type=int, default=1073741824, help='--flush_thread_max_memory <max_memory_in_bytes>')
acceptParser.set_defaults(component='accept')

processParser = subParsers.add_parser('process', parents=[mainParser])
processParser.add_argument('--config', type=str, default="", required=True, help='--config <path_to_config_file>')
processParser.add_argument('--cache', type=str, default="", required=True, help='--cache <path_to_cache_file>')
processParser.add_argument('--pipeline_time', type=bool, default=False, help='Flag to enable pipeline time output', nargs="?", const=True)
processParser.set_defaults(component='process')

processorTestParser = subParsers.add_parser('processor', parents=[mainParser])
processorTestParser.add_argument('--id', type=str, default="", required=True, help='--id <processor_id>')
processorTestParser.add_argument('--config', type=str, default="", required=True, help='--config <path_to_config_file>')
processorTestParser.add_argument('--event', type=str, default="", required=True, help='--event <event>')
processorTestParser.add_argument('--event_json', type=bool, default=False, help='Flag to enable event as json', nargs="?", const=True)
processorTestParser.set_defaults(component='processor')

args = mainParser.parse_args()
if __name__ == "__main__":
    args.main = True
else:
    args.main = False

from core import globalLogger, globalSettings
globalSettings.args = args
globalLogger.logger.setLevel(globalSettings.args.log_level)

from core import debugging

if args.main:
    from core import parser, plugins, pipelines
    globalSettings.config = parser.yaml(open(globalSettings.args.config,"r").read())
    plugins.load()
    loadedPipelines = []
    for pipeline in globalSettings.config:
        loadedPipelines += pipelines.load(pipeline)
    if args.component == "accept":
        from accept import accept
        accept.start(loadedPipelines)
    elif args.component == "process":
        from process import process
        process.start(loadedPipelines)
    elif args.component == "processor":
        from process import processorTest
        processorTest.test()
globalLogger.logger.info(f"Execution time: {time.perf_counter() - startTime}")
