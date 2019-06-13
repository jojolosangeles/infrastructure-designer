import sys
from cloudformation.yamlloader import YamlLoader, YamlFlattener


def getFileName(filePath):
    return filePath.replace('.yaml', '.flat').replace('./', '').replace('/', '_')

if __name__ == "__main__":
    cloudFormationFilePath = sys.argv[1]
    print(f"Loading CloudFormation: {cloudFormationFilePath}")

    yamlLoader = YamlLoader(cloudFormationFilePath)
    yamlFlattener = YamlFlattener(yamlLoader.data)
    flatList = yamlFlattener.flatten()

    outDir = "./flat"
    outFile = getFileName(cloudFormationFilePath)
    outputFilePath = f"{outDir}/{outFile}"
    with open(outputFilePath, "w") as output:
        for n in flatList:
            output.write(str(n))
            output.write("\n")

    print(f"Saved {outputFilePath}")