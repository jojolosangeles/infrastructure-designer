from queue import Queue

class NodeVisit:
    """Enter/exit a node when it is visited"""
    def __init__(self, visitor, node, depth):
        self.visitor = visitor
        self.node = node
        self.depth = depth

    def __enter__(self):
        self.visitor.enterNode(self.node, self.depth)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.visitor.exitNode(self.node, self.depth)

class DFStraversal:
    """Depth First traversal with a Visitor"""
    def __init__(self, visitor):
        self.visitor = visitor

    def traverse(self, nodeOrList, depth=0):
        nodeList = nodeOrList if isinstance(nodeOrList, list) else [ nodeOrList ]
        for node in nodeList:
            with NodeVisit(self.visitor, node, depth):
                if not self.visitor.isDone() and self.visitor.shouldTraverseChildren(node, depth):
                    for key,child in node.children.items():
                        self.traverse(child, depth+1)

class BFStraversal:
    """Breadth First traversal with a Visitor"""
    def __init__(self, visitor):
        self.visitor = visitor
        self.queue = Queue()

    def traverse(self, node, depth=0):
        self.queue.put((node, depth))
        while not self.queue.empty():
            node, depth = self.queue.get()
            self.visitor.enterNode(node, depth)
            if not self.visitor.isDone() and self.visitor.shouldTraverseChildren(node, depth):
                for key,child in node.children.items():
                    self.queue.put((child, depth+1))
            self.visitor.exitNode(node, depth)
