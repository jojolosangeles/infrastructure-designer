

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




