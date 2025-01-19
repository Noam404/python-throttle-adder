import sys
# from typing import TextIO

def writeImport(file: str, lines) -> None: # file format 'w'
    foundSimilarImport = False # no need, but good convention wise
    for line_number, line in enumerate(lines): # specfic import
        
        if "import ..." in line:
            # add import to file itself here
            lines[line_number] = line.strip() + "import module ...\n"
            foundSimilarImport = True
            break
    
    if foundSimilarImport:
        with open(file, 'w') as f:
            f.write(lines)
            f.close()
        return
    
    for line_number, line in enumerate(lines): # less specific import
        if "less specific import..." in line:
            # add import to line itself here
            lines[line_number] = line + "new import\n"
            foundSimilarImport = True
            break
    
    if foundSimilarImport:
        with open(file, 'w') as f:
            f.write(lines)
            f.close()
        return
    
    lines.insert(0, "import\n")

def writeScope(file: str, scope: str, inClass: str, lines) -> None:
    for line_number, line in enumerate(lines):
        if f"class {inClass}" in line:
            lines[line_number + 1] = "scope...\n"
            lines[line_number + 2] = "scope_list..\n"
            break
    
    with open(file, 'w') as f:
        f.write(lines)
        f.close()

def write(file: str, scope: str, inClass: str, lines: list) -> None:
    
    writeImport(file=file, lines=lines)
    writeScope(file=file, scope=scope, inClass=inClass, lines=lines)

if __name__ == "__file__":
    arguments = sys.argv[1:] # exclude script path
    #argv: [type, filePath, scope, class]
    fileLines = []
    with open(arguments[1], 'r') as file:
        fileLines = file.readlines()
        file.close()

    match arguments[0]:
        case "writeScope":
            write(arguments[1], arguments[2], arguments[3], fileLines)
        case "readFile":
            print(fileLines)