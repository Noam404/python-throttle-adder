import jsonify, json
import sys

def toJson(relativePath: str, outputPath: str) -> list:
    info = []
    
    with open(relativePath, 'r') as file:
        lines = file.readlines()
        file.close()
    
    for line in lines:
        if line[0] == '#':
            splitted = line[2:-1].split(".")
            info.append({
                "path": "/".join(splitted[:-1]),
                "viewName": splitted[-1],
                "status": False,
                "scope": None,
                "why": None,
            })
    

    jsonInfo = json.dumps(info, indent=4)
    with open(outputPath, 'w') as outputFile:
        outputFile.write(jsonInfo)
        outputFile.close()
    return info # returns list! not json

def readJson(filePath):
    data = []
    with open(filePath, 'r') as file:
        data = json.load(file)
        file.close()

    return data

def writeJson(data, filePath):
    with open(filePath, 'r') as file:
        file.write(jsonify(data))
        file.close()

if __name__ == "__main__":
    arguments = sys.argv[1:]
    toJson(arguments[0], arguments[1])