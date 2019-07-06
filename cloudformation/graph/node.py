

class GraphNode:
    """A single node in a graph"""
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}

    def addChild(self, edgeval):
        node = GraphNode(edgeval, self)
        self.children[edgeval] = node
        return node


