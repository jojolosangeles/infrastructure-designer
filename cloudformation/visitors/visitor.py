

class Visitor:
    """Methods called by Graph Traversal implementations.

    Any visitor output is placed in 'result'

    Optional depth limit to traversal is implemented in 'traverseChildren'"""
    MAXDEPTH=999

    def __init__(self, maxDepth=None):
        self.maxDepth = Visitor.MAXDEPTH if maxDepth == None else maxDepth
        self.result = None

    def enterNode(self, node, depth=0):
        pass

    def exitNode(self, node, depth=0):
        pass

    def isDone(self):
        return False

    def shouldTraverseChildren(self, node=None, depth=0):
        return depth < self.maxDepth

class FindVisitor(Visitor):
    def __init__(self, target, maxDepth=None):
        self.target = target
        self.foundTarget = False
        super().__init__(maxDepth)

    def enterNode(self, node, depth):
        if node.name == self.target:
            self.foundTarget = True
            self.result = node

    def isDone(self):
        return self.foundTarget



