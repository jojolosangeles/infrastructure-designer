from visitors.visitor import Visitor

class PrintVisitor(Visitor):
    def __init__(self, spacer=" ", maxDepth=None):
        self.spacer = spacer
        super().__init__(maxDepth)

    def enterNode(self, node, depth):
        print(f"{self.spacer * depth}{node.name}")

