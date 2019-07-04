from cloudformation.graph.node import GraphNode

class GraphBuilder:
    """Build a graph from arrays of strings.

       ['Aaa','Bbb','Ccc']
       ['Aaa','Bbb','Ddd']
       ['Aaa','Xxx']

       results in a graph:

       Aaa
        +- Bbb
        |   +- Ccc
        |   +- Ddd
        +- Xxx
    """
    def __init__(self):
        self.ROOT = GraphNode("ROOT")

    def add(self, data):
        node = self.ROOT
        for level,edgeval in enumerate(data):
            if edgeval in node.children:
                node = node.children.get(edgeval)
            else:
                node = node.addChild(edgeval)
        return self