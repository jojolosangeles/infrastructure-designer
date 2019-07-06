from cloudformation.visitors.visitor import Visitor

class FindVisitor(Visitor):
    def __init__(self, target, maxDepth=None):
        self.target = target
        self.foundTarget = False
        super().__init__(maxDepth)

    def enterNode(self, node, depth):
        if str(node.name) == self.target:
            self.foundTarget = True
            self.result = node
        elif isinstance(node.name, str):
            testName = node.name.split("[")[0]
            if testName == self.target:
                self.result = [] if self.result == None else self.result
                self.result.append(node)

    def isDone(self):
        return self.foundTarget

class ReferenceFinderVisitor(Visitor):
    def __init__(self, target, maxDepth=None):
        self.target = f"Ref___{target}"
        super().__init__(maxDepth)

    def enterNode(self, node, depth):
        if str(node.name) == self.target:
            self.result = [] if self.result == None else self.result
            self.result.append(node)
        elif isinstance(node.name, str):
            testName = node.name.split("[")[0]
            if testName == self.target:
                self.result = [] if self.result == None else self.result
                self.result.append(node)
