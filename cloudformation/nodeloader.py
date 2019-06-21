import sys
import datetime   # do not remove, needed for 'datetime' reference in cloudformation files

class CFComponent:
    def __init__(self, name):
        self.name = name
        self.type = "UNKNOWN"
        self.properties = {}

class Property(CFComponent):
    def __init__(self, name):
        super().__init__(name)
        self.values = []
        self.reference = False

    def is_reference(self):
        return self.reference or (type(property.values[0]) == str and property.values[0].startswith("Ref_"))

    def reference_to(self):
        return self.values

    def __str__(self):
        return f"name={self.name}, value={self.values}"

class Parameter(CFComponent):
    def __init__(self, name):
        super().__init__(name)

    def add(self, k, v):
        if k == "Type":
            self.type = v
        else:
            self.properties[k] = v

    def __str__(self):
        default = str(self.properties.get("Default", ""))
        defaultStr = f" = {default}" if len(default) > 0 else ""
        return f"(node) {self.name} ~~~ {self.type}{defaultStr}"

class Resource(CFComponent):
    def __init__(self, name):
        super().__init__(name)

    def add_property(self, data):
        # data, indices below
        # - Properties (Name) Ref_(Value)
        #              0,-2   1,-1
        # - Properties (Name1) (Name2) Ref_Value
        #              0,-3    1,-2    2,-1
        # - Properties (Name) Ref   (Value)
        #              0,-3   1,-2  2,-1
        # - Properties (Name1) (Name2) Ref   (Value)
        #              0,-4    1,-3    2,-2  3,-1

        # set the value for the above cases
        propertyValue = data[-1]
        isReference = False
        if type(propertyValue) == str and propertyValue.startswith("Ref_"):
            isReference = True
            propertyValue = propertyValue[4:]

        # if there is an explicit "Ref" get rid of it so that Properties data is (name*) (value)
        if data[-2] == "Ref":
            isReference = True
            del data[-2]

        propertyName = '.'.join(data[:-1])

        # get it if it's there, otherwise create it, then add the value to the list of values for that property
        property = self.properties.get(propertyName, Property(propertyName))
        property.values.append(propertyValue)
        property.reference = isReference
        self.properties[propertyName] = property

    def add(self, data):
        if data[0] == "Type":
            self.type = data[1]
        elif data[0] == "Properties":
            self.add_property(data[1:])

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


def getFileName(filePath):
    return filePath.replace('.flat', '.graph').replace('/flat/', '/graph/').replace('./', '')

if __name__ == "__main__":
    flatFile = sys.argv[1]
    if len(sys.argv) == 2:
        sys.stdout = open(getFileName(flatFile), "w")
    with open(flatFile, "r") as inFile:
        lines = inFile.readlines()
        lists = [ eval(line) for line in lines ]

    nodeLoader = NodeLoader(lists)

    print("-- parameters --")
    for k,v in nodeLoader.parameters.items():
        print(v)

    print("-- resources --")
    for k,v in nodeLoader.resources.items():
        print(v)
        for propertyName, property in v.properties.items():
            if property.is_reference():
                print(f"  (field) {property.name} --> (node) {property.reference_to()}")



