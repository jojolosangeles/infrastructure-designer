import sys
from cloudformation.yamlloader import YamlLoader, YamlFlattener

class CFComponent:
    def __init__(self, name):
        self.name = name
        self.type = "UNKNOWN"
        self.properties = {}

class Property(CFComponent):
    def __init__(self, name):
        super().__init__(name)
        self.value = []
        self.reference = False

    def is_reference(self):
        return self.reference or (type(property.value) == str and property.value.startswith("Ref_"))

    def reference_to(self):
        return self.value[4:] if type(property.value) == str and property.value.startswith("Ref_") else self.value

    def __str__(self):
        return f"name={self.name}, value={self.value}"

class Parameter(CFComponent):
    def __init__(self, name):
        super().__init__(name)

    def add(self, k, v):
        if k == "Type":
            self.type = v
        else:
            self.properties[k] = v

    def __str__(self):
        default = self.properties.get("Default", "")
        defaultStr = f" = {default}" if len(default) > 0 else ""
        return f"(node) {self.name} ~~~ {self.type}{defaultStr}"

class Resource(CFComponent):
    def __init__(self, name):
        super().__init__(name)

    def add(self, data):
        if data[0] == "Type":
            self.type = data[1]
        elif data[0] == "Properties":
            # two cases:
            # - Properties (Name) Ref_(Value)
            # - Properties (Name) Ref (Value)
            value = data[-1]
            if type(value) == str and value.startswith("Ref_"):
                # properties[name] refers to (Value) node
                propertyName = ".".join(data[1:-1])
            elif data[-2] == "Ref":
                propertyName = ".".join(data[1:-2])
            else:
                propertyName = ".".join(data[1:-1])

            property = self.properties.get(propertyName, Property(propertyName))
            property.value.append(data[-1])
            property.reference = data[-2] == "Ref"
            self.properties[propertyName] = property

    def __str__(self):
        return f"(node) {self.name} ~~~ {self.type}"

class NodeLoader:
    def __init__(self, flatList):
        self.flatList = flatList
        self.parameters = self.loadParameters([data for data in flatList if data[0] == "Parameters"])
        self.resources = self.loadResources([data for data in flatList if data[0] == "Resources"])

    def loadParameters(self, paramList):
        parameters = {}
        for data in paramList:
            keyName = data[1]
            parameters[keyName] = parameters.get(keyName, Parameter(keyName))
            parameters[keyName].add(data[2], data[3])
        return parameters

    def loadResources(self, resourceList):
        resources = {}
        for data in resourceList:
            keyName = data[1]
            resources[keyName] = resources.get(keyName, Resource(keyName))
            resources[keyName].add(data[2:])
        return resources


if __name__ == "__main__":
    cloudFormationFilePath = sys.argv[1]
    print(f"Loading CloudFormation: {cloudFormationFilePath}")
    yamlLoader = YamlLoader(cloudFormationFilePath)
    yamlFlattener = YamlFlattener(yamlLoader.data)
    flatList = yamlFlattener.flatten()

    outDir = "./flat"
    outFile = getFileName(cloudFormationFilePath)
    outputFilePath = f"{outDir}/{outFile}"
    with open(outputFilePath, "w") as output:
        for n in flatList:
            output.write(str(n))
            output.write("\n")
    print(f"Saved {outputFilePath}")
    nodeLoader = NodeLoader(flatList)
    print("-- parameters --")
    for k,v in nodeLoader.parameters.items():
        print(v)

    print("-- resources --")
    for k,v in nodeLoader.resources.items():
        print(v)
        for propertyName, property in v.properties.items():
            if property.is_reference():
                print(f"  (field) {property.name} --> (node) {property.reference_to()}")

    print("-- node relationships --")
    nodes = []
    for k, v in nodeLoader.resources.items():
        for propertyName, property in v.properties.items():
            print(f"** {property}")
            if property.is_reference():
                print(f"{k} -> {property.reference_to()}")

