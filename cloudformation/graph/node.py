

class GraphNode:
    """A single node in a graph"""
    def __init__(self, name):
        self.name = name
        self.children = {}

    def addChild(self, edgeval):
        node = GraphNode(edgeval)
        self.children[edgeval] = node
        return node


