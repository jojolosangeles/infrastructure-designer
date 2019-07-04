import sys
from graph.traversal import DFStraversal
from visitors.print_visitor import PrintVisitor
from visitors.name_type_visitor import NameTypeVisitor
from graph.builder import GraphBuilder
from graph.tree import TreeGraph

if __name__ == "__main__":
    graphBuilder = GraphBuilder()
    with open(sys.argv[1], "r") as inFile:
        for line in inFile:
            data = eval(line)
            graphBuilder.add(data)

    dfs = DFStraversal(PrintVisitor(" ", 3))
    dfs.traverse(graphBuilder.ROOT)

    tree = TreeGraph(graphBuilder.ROOT)
    resources = tree.findNode("Resources", maxDepth=3)

    print("****")
    dfs.traverse(resources)
    print("****")
    nameTypeVisitor = NameTypeVisitor()
    dfs = DFStraversal(nameTypeVisitor)
    dfs.traverse(resources)
