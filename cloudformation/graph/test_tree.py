from cloudformation.loader.yamlloader import YamlLoader, YamlFlattener
from cloudformation.graph.builder import GraphBuilder
from cloudformation.graph.tree import TreeGraph

def test_tree():
    yamlLoader = YamlLoader(f"/Users/jojo/code/infrastructure-designer/cloudformation/loader/cf_test2.yaml")
    assert yamlLoader.data != None
    yamlFlattener = YamlFlattener(yamlLoader.data)
    test = yamlFlattener.flatten()
    gb = GraphBuilder()
    for list in test:
        gb.add(list)
    tree = TreeGraph(gb.ROOT)
    securityGroupIngress = tree.findNode("SecurityGroupIngress")
    assert securityGroupIngress != None
    assert len(securityGroupIngress) == 5
    sshSecurityGroup = tree.findBySpecification(["SecurityGroupIngress", "22"])
    assert sshSecurityGroup != None
    assert len(sshSecurityGroup) == 1
    assert sshSecurityGroup[0].parent.parent.parent.parent.name == "WebServerSecurityGroup"
    securityGroupNode = tree.asResourceNode(sshSecurityGroup[0])
    assert securityGroupNode.name == "WebServerSecurityGroup"
    securityGroupNode = tree.parentX(sshSecurityGroup[0], 4)
    assert securityGroupNode.name == "WebServerSecurityGroup"
    references = [tree.asResourceNode(ref) for ref in tree.findReferencesTo("WebServerSecurityGroup")]
    assert references != None
    tree_references = tree.findResourceReferencesTo("WebServerSecurityGroup")
    assert tree_references != None
    assert len(references) == len(tree_references)
    for i in range(len(references)):
        assert tree_references[i] == references[i]