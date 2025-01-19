import jsonify

def toJson(relativePath: str, outputPath: str) -> list:
    info = []
    
    with open(relativePath, 'r') as file:
        line = file.readline()
        while line:
            if line[0] == '#':
                info.append({
                    "path": line[2:-1],
                    "status": False,
                    "scope": None,
                    "why": None,
                })
            line = file.readline()
        file.close()

    json = jsonify(info)
    with open(outputPath, 'w') as outputFile:
        outputFile.write(json)
    return info # returns list! not json