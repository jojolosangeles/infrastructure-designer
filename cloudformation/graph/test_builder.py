from cloudformation.graph.builder import GraphBuilder
from cloudformation.loader.yamlloader import YamlLoader, YamlFlattener
from cloudformation.graph.tree import TreeGraph

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

def test_load():
    yamlLoader = YamlLoader(f"/Users/jojo/code/infrastructure-designer/cloudformation/loader/cf_test1.yaml")
    assert yamlLoader.data != None
    yamlFlattener = YamlFlattener(yamlLoader.data)
    test = yamlFlattener.flatten()
    gb = GraphBuilder()
    for list in test:
        gb.add(list)
    tree = TreeGraph(gb.ROOT)
    securityGroupIngress = tree.findNode("SecurityGroupIngress")
    assert securityGroupIngress != None
    assert len(securityGroupIngress) == 2
    sshSecurityGroup = tree.findBySpecification(["SecurityGroupIngress", "22"])
    assert sshSecurityGroup != None
    assert len(sshSecurityGroup) == 1
    assert sshSecurityGroup[0].parent.parent.parent.parent.name == "WebServerSecurityGroup"