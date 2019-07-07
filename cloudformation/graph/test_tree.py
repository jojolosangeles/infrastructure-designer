from cloudformation.loader.yamlloader import YamlLoader, YamlFlattener
from cloudformation.graph.builder import GraphBuilder
from cloudformation.graph.tree import TreeGraph

def make_tree():
    yamlLoader = YamlLoader(f"/Users/jojo/code/infrastructure-designer/cloudformation/loader/cf_test2.yaml")
    assert yamlLoader.data != None
    yamlFlattener = YamlFlattener(yamlLoader.data)
    test = yamlFlattener.flatten()
    gb = GraphBuilder()
    for list in test:
        gb.add(list)
    tree = TreeGraph(gb.ROOT)
    return tree

def test_tree():
    tree = make_tree()
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
    references = tree.findReferencesTo("WebServerSecurityGroup")
    results = [ 'DatabaseSecurityGroup.Properties.SecurityGroupIngress[0].SourceSecurityGroupId.Ref___WebServerSecurityGroup',
                'EFSSecurityGroup.Properties.SecurityGroupIngress[0].SourceSecurityGroupId.Ref___WebServerSecurityGroup',
                'LaunchConfiguration.Properties.SecurityGroups[0].Ref___WebServerSecurityGroup']
    for i in range(len(references)):
        name = []
        scanner = references[i]
        while scanner != tree_references[i]:
            name.append(scanner.name)
            scanner = scanner.parent
        name.append(tree_references[i].name)
        name.reverse()
        pathName = ".".join(name)
        assert pathName == results[i]

def test_igw():
    tree = make_tree()
    igw_references = tree.findBySpecification(["AWS::EC2::InternetGateway"])
    assert igw_references != None
    igw_references = tree.findReferencesToNodes(igw_references)
    assert igw_references != None
    igw_references = [tree.asResourceNode(igw) for igw in igw_references]
    assert igw_references != None
    vpc_gateway_references = tree.findBySpecification(["AWS::EC2::VPCGatewayAttachment"])
    assert vpc_gateway_references != None
    vpc_gateway_references = tree.findReferencesToNodes(vpc_gateway_references)
    assert vpc_gateway_references != None
    vpc_gateway_references = [tree.asResourceNode(vpcgw) for vpcgw in vpc_gateway_references]
    assert vpc_gateway_references != None

    nodes_referring_to_igw = []
    for igw in igw_references:
        nodes_referring_to_igw += tree.findResourceReferencesTo(igw.name)
    assert len(nodes_referring_to_igw) > 0

    nodes_referring_to_vpcgw = []
    for vpcgw in vpc_gateway_references:
        nodes_referring_to_vpcgw += tree.findResourceReferencesTo(vpcgw.name)
    assert len(nodes_referring_to_vpcgw) > 0