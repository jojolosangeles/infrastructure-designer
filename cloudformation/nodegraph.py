import sys

class GraphNode:
    def __init__(self, name):
        self.name = name
        self.children = {}

    def addChild(self, edgeval):
        node = GraphNode(edgeval)
        self.children[edgeval] = node
        return node


class GraphBuilder:
    """A graph starts with a ROOT node.

    Each line creates a new leaf node, and possibly intermediate nodes between the root and the leaf"""
    def __init__(self):
        self.ROOT = GraphNode("ROOT")

    def add(self, data):
        node = self.ROOT
        for level,edgeval in enumerate(data):
            if edgeval in node.children:
                node = node.children.get(edgeval)
            else:
                node = node.addChild(edgeval)

class DFSvisitor:
    def __init__(self, visitor):
        self.visitor = visitor

    def traverse(self, node, depth=0):
        self.visitor.enterNode(node, depth)
        if self.visitor.traverseChildren():
            for key,child in node.children.items():
                self.traverse(child, depth+1)
        self.visitor.exitNode(node, depth)

class Visitor:
    def enterNode(self, node, depth=0):
        pass

    def exitNode(self, node, depth=0):
        pass

    def traverseChildren(self):
        return True

class PrintVisitor(Visitor):
    def __init__(self, spacer=" "):
        self.spacer = spacer

    def enterNode(self, node, depth):
        print(f"{self.spacer * depth}{node.name}")



if __name__ == "__main__":
    graphBuilder = GraphBuilder()
    with open(sys.argv[1], "r") as inFile:
        for line in inFile:
            data = eval(line)
            graphBuilder.add(data)

    visitor = DFSvisitor(PrintVisitor(" "))
    visitor.traverse(graphBuilder.ROOT)