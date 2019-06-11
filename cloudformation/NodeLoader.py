import yaml
import sys


def general_constructor(loader, tag_suffix, node):
    return f"{tag_suffix}_{node.value}"

yaml.SafeLoader.add_multi_constructor(u'!', general_constructor)

class YamlLoader:
    def __init__(self, yamlFile):
        with open(yamlFile, 'r') as stream:
            try:
                self.data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

# started with: https://stackoverflow.com/questions/12507206/how-to-completely-traverse-a-complex-dictionary-of-unknown-depth
def dict_generator(indict, pre=None):
    # copy preceding list
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key in indict:
            value = indict.get(key)
            # if the value is a dict, yield the list with each value at end
            if isinstance(value, dict):
                for d in dict_generator(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in dict_generator(v, pre + [key]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]


def getFileName(filePath):
    return filePath.replace('.yaml', '.flat').replace('./', '').replace('/', '_')

if __name__ == "__main__":
    cloudFormationFilePath = sys.argv[1]
    nodeLoader = YamlLoader(cloudFormationFilePath)
    outDir = "./flat"
    outFile = getFileName(cloudFormationFilePath)
    flatList = [n for n in dict_generator(nodeLoader.data)]
    with open(f"{outDir}/{outFile}", "w") as output:
        for n in flatList:
            output.write(str(n))
            output.write("\n")
