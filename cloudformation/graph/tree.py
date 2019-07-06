from cloudformation.visitors.find_visitor import FindVisitor, ReferenceFinderVisitor
from cloudformation.graph.traversal import DFStraversal
from cloudformation.graph.node import GraphNode

class TreeGraph:
    """A Tree Graph with some convenience methods"""
    MAXDEPTH=999

    def __init__(self, root):
        self.root = root

    def findNode(self, nodeName, maxDepth=None) -> GraphNode:
        return self.findNodeFromStartNode(self.root, nodeName, maxDepth)

    def findNodeFromStartNode(self, startNode, nodeName, maxDepth=None) -> GraphNode:
        maxDepth = self.MAXDEPTH if maxDepth == None else maxDepth
        findVisitor = FindVisitor(nodeName, maxDepth)
        dfs = DFStraversal(findVisitor)
        dfs.traverse(startNode)
        return findVisitor.result

    def findBySpecification(self, valueList):
        return self.findBySpecFromStartNode(self.root, valueList)

    def findBySpecFromStartNode(self, node, valueList):
        nodeList = [node]
        for value in valueList:
            newNodeList = []
            for node in nodeList:
                newNode = self.findNodeFromStartNode(node, value)
                if newNode != None:
                    newNodeList.append(newNode)
            nodeList = newNodeList
        return nodeList

    def findReferencesTo(self, nodeName):
        referenceFinderVisitor = ReferenceFinderVisitor(nodeName)
        dfs = DFStraversal(referenceFinderVisitor)
        dfs.traverse(self.root)
        return referenceFinderVisitor.result

    def findResourceReferencesTo(self, nodeName):
        references = self.findReferencesTo(nodeName)
        return [self.asResourceNode(ref) for ref in references]

    def asResourceNode(self, startNode):
        scanner = startNode
        while scanner.parent.name != "Resources":
            scanner = scanner.parent
        return scanner

    def parentX(self, node, count):
        for _ in range(count):
            node = node[0].parent if isinstance(node,list) else node.parent
        return node