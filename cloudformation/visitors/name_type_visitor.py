from visitors.visitor import Visitor

class NameTypeBuilder:
    def __init__(self):
        self.name = None
        self.type = None
        self.traverseChildrenForType = False

    def add(self, value, depth):
        # level 1 is name, traverse children
        # if level 2 is "Type" traverse children
        # if level 3, save type value
        if depth == 1:
            self.name = value
            self.type = None
        elif depth == 2:
            self.traverseChildrenForType = (value == "Type")
        elif depth == 3:
            self.type = value

    def isDone(self):
        return self.name != None and self.type != None

    def reset(self):
        print(f"{self.type} '{self.name}'")
        self.name = None
        self.type = None
        self.traverseChildrenForType = False

class NameTypeVisitor(Visitor):
    """Collect names and types from cloudformation 'Resources' section"""
    def __init__(self):
        self.nameTypes = {}
        self.builder = NameTypeBuilder()
        super().__init__(maxDepth=5)

    def enterNode(self, node, depth):
        self.builder.add(node.name, depth)
        if self.builder.isDone():
            self.nameTypes[self.builder.name] = self.builder.type
            self.builder.reset()

    def shouldTraverseChildren(self, node, depth):
        return super().shouldTraverseChildren(node, depth) or self.builder.traverseChildrenForType