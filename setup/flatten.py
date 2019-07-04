import sys
from cloudformation.yamlloader import YamlLoader, YamlFlattener
import contextlib

# from https://stackoverflow.com/questions/17602878/how-to-handle-both-with-open-and-sys-stdout-nicely
@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

def getFileName(filePath):
    return filePath.replace('.yaml', '.flat').replace('./', '').replace('/', '_')

if __name__ == "__main__":
    cloudFormationFilePath = sys.argv[1]
    outputFilePath = "-"
    if len(sys.argv) == 2:
        outDir = "./flat"
        outFile = getFileName(cloudFormationFilePath)
        outputFilePath = f"{outDir}/{outFile}"

    print(f"Loading CloudFormation: {cloudFormationFilePath}")

    yamlLoader = YamlLoader(cloudFormationFilePath)
    yamlFlattener = YamlFlattener(yamlLoader.data)
    flatList = yamlFlattener.flatten()

    with smart_open(outputFilePath) as output:
        for n in flatList:
            output.write(str(n))
            output.write("\n")

    print(f"Saved {outputFilePath}")