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
        self.ref_target = f"Ref___{target}"
        self.target = target
        super().__init__(maxDepth)

    def enterNode(self, node, depth):
        if str(node.name) == self.target or str(node.name) == self.ref_target:
            self.result = [] if self.result == None else self.result
            if node.parent.name != "Resources":
                self.result.append(node)
        elif isinstance(node.name, str):
            testName = node.name.split("[")[0]
            if testName == self.target:
                self.result = [] if self.result == None else self.result
                self.result.append(node)
