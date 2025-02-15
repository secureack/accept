from core import typecast

def yaml(yamlData):
    def include(filename,indent):
        indent = " "*indent
        with open(filename, "r") as f:
            yamlIncludeData = f.read()
        finalYamlIncludeData = ""
        for index, line in enumerate(yamlIncludeData.split("\n")):
            if line.strip().startswith("#"):
                continue
            if line.strip().startswith("@include "):
                finalYamlIncludeData += include(line.split("@include ")[1],(len(line) - len(line.lstrip())))
                continue
            finalYamlIncludeData += f"{indent}{line}\n"
        return finalYamlIncludeData
    objects = {}
    objectData = None
    yamlData += "\n" # Force additional line at the end so we can detect and commit the last object without missing any properties
    finalYamlData = ""
    for index, line in enumerate(yamlData.split("\n")):
        if line.strip().startswith("#"):
            continue
        if line.strip().startswith("@include "):
            finalYamlData += include(line.split("@include ")[1],(len(line) - len(line.lstrip())))
            continue
        finalYamlData += f"{line}\n"
    lastLine = len(finalYamlData.split("\n")) -1
    for index, line in enumerate(finalYamlData.split("\n")):
        if objectData and ( line.startswith("input:") or line.startswith("processor:") or line.startswith("output:") or index == lastLine ):
            objects[objectData["id"]] = objectData
            objectData = None
        if line.startswith("input:"):
            objectData = { "type" : "input", "properties" : {}, "enabled" : True, "next" : []  }
        elif line.startswith("processor:"):
            objectData = { "type" : "processor", "properties" : {}, "enabled" : True, "next" : [] }
        elif line.startswith("output:"):
            objectData = { "type" : "output", "properties" : {}, "enabled" : True, "next" : [] }
        elif objectData:
            key = line.split(":")[0]
            try:
                value = typecast.simple(line[len(key)+1:].strip().replace("\\r","\r").replace("\\n","\n").replace("\\t","\t"))
            except:
                pass
            key = key.strip()
            if not key:
                continue
            if key in ["name","next","id","plugin"]:
                objectData[key] = value
            else:
                objectData["properties"][key] = value
    return [objects]
