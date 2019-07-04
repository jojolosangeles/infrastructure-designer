from cloudformation.graph.builder import GraphBuilder

def test_gb():
    gb = GraphBuilder()
    assert gb != None

def test_basic():
    d1 = [ 'Aaa', 'Bbb' ]
    d2 = [ 'Aaa', 'Xxx' ]
    gb = GraphBuilder()
    gb.add(d1).add(d2)

    node = gb.ROOT.children["Aaa"]
    assert(node.name == "Aaa")
    assert(len(node.children) == 2)
    assert("Bbb" in node.children)
    assert("Xxx" in node.children)