from cloudformation.visitors.visitor import FindVisitor
from cloudformation.graph.traversal import DFStraversal
from cloudformation.graph.node import GraphNode

class TreeGraph:
    """A Tree Graph with some convenience methods"""
    MAXDEPTH=999

    def __init__(self, root):
        self.root = root

    def findNode(self, nodeName, maxDepth=None) -> GraphNode:
        maxDepth = self.MAXDEPTH if maxDepth == None else maxDepth
        findVisitor = FindVisitor(nodeName, maxDepth)
        dfs = DFStraversal(findVisitor)
        dfs.traverse(self.root)
        return findVisitor.result
