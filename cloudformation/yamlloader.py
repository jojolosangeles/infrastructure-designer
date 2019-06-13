import yaml

def general_constructor(loader, tag_suffix, node):
    return f"{tag_suffix}_{node.value}"

yaml.SafeLoader.add_multi_constructor(u'!', general_constructor)

class YamlLoader:
    """Loads a Cloudformation yaml file special handling for the Ref! syntax
    """
    def __init__(self, yamlFile):
        with open(yamlFile, 'r') as stream:
            try:
                self.data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

class YamlFlattener:
    """Flatten hierarchy so that each line becomes a list, where each
    elemenet is the path from the root to the element.

    For example:

    Resources:
      VPC:
        Type: 'AWS::EC2::VPC'
        Properties:
          CidrBlock: '172.31.0.0/16'
          EnableDnsHostnames: true

    becomes:

    ['Resources', 'VPC', 'Type', 'AWS::EC2::VPC']
    ['Resources', 'VPC', 'Properties', 'CidrBlock', '172.31.0.0/16']
    ['Resources', 'VPC', 'Properties', 'EnableDnsHostnames', True]
      """
    def __init__(self, yamlData):
        self.data = yamlData

    # started with: https://stackoverflow.com/questions/12507206/how-to-completely-traverse-a-complex-dictionary-of-unknown-depth
    def dict_generator(self, indict, pre=None):
        # copy preceding list
        pre = pre[:] if pre else []
        if isinstance(indict, dict):
            for key in indict:
                value = indict.get(key)
                # if the value is a dict, yield the list with each value at end
                if isinstance(value, dict):
                    for d in self.dict_generator(value, pre + [key]):
                        yield d
                elif isinstance(value, list) or isinstance(value, tuple):
                    for v in value:
                        for d in self.dict_generator(v, pre + [key]):
                            yield d
                else:
                    yield pre + [key, value]
        else:
            yield pre + [indict]

    def flatten(self):
        return [n for n in self.dict_generator(self.data)]
