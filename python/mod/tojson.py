import jsonify

def toJson(relativePath: str, outputPath: str) -> list:
    info = []
    
    with open(relativePath, 'r') as file:
        lines = file.readlines()
        file.close()
    
    for line in lines:
        if line[0] == '#':
            info.append({
                "path": line[2:-1],
                "status": False,
                "scope": None,
                "why": None,
            })
    

    json = jsonify(info)
    with open(outputPath, 'w') as outputFile:
        outputFile.write(json)
        outputFile.close()
    return info # returns list! not json