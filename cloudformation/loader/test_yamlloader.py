from cloudformation.loader.yamlloader import YamlLoader, YamlFlattener

def test_loader():
    yamlLoader = YamlLoader(f"/Users/jojo/code/infrastructure-designer/cloudformation/loader/cf_test1.yaml")
    assert yamlLoader.data != None
    yamlFlattener = YamlFlattener(yamlLoader.data)
    test = yamlFlattener.flatten()

    assert ['Resources', 'WebServerSecurityGroup', 'Properties',
            'SecurityGroupIngress[0]', 'CidrIp', '0.0.0.0/0'] in test

    assert ['Resources', 'WebServerSecurityGroup', 'Properties',
            'SecurityGroupIngress[1]', 'SourceSecurityGroupId', 'Ref___LoadBalancerSecurityGroup'] in test