import os
from pathlib import Path
import importlib

from core import functions

available = {
    "input" : {},
    "processor" : {},
    "output" : {}
}

def load():
    presentPlugins = os.listdir("plugins")
    for plugin in presentPlugins:
        if "__" not in plugin and "." not in plugin:
            for pluginType in ["input","processor","output","function"]:
                if os.path.exists(Path(f"plugins/{plugin}/{pluginType}")):
                    pluginClasses = os.listdir(Path(f"plugins/{plugin}/{pluginType}"))
                    for pluginClass in pluginClasses:
                        if pluginClass.endswith(".py"):
                            if pluginType != "function":
                                mod = __import__(f"plugins.{plugin}.{pluginType}.{pluginClass[:-3]}", fromlist=[f"{pluginClass[:-3]}"])
                                class_ = getattr(mod, f"{pluginClass[:-3]}")
                                available[pluginType][pluginClass[:-3]] = class_
                            else:
                                mod = importlib.import_module(f"plugins.{plugin}.{pluginType}.{pluginClass[:-3]}",pluginClass[:-3])
                                for func in dir(mod):
                                    if not func.startswith("__"):
                                        if hasattr(getattr(mod, func),"__call__"):
                                            functions.available[func] = getattr(mod, func) 
