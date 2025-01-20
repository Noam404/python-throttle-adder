import sys
# from typing import TextIO

def writeImport(file: str, lines, importLocation: str, importModule: str, entity: str) -> None: # file format 'w'
    foundSimilarImport = False # no need, but good convention wise    
    
    for line_number, line in enumerate(lines):
        if f"from {importLocation}.{importModule}" in line and entity in line and line.strip()[0] != '#':
            return;

    for line_number, line in enumerate(lines): # specfic import
        
        if f"from {importLocation}.{importModule}" in line and line.strip()[0] != '#':
            # add import to file itself here
            # adds entity to same import module
            lines[line_number] = line.strip() + f", {entity}\n"
            foundSimilarImport = True
            break
    
    if foundSimilarImport:
        with open(file, 'w') as f:
            f.writelines(lines)
            f.close()
        return
    
    for line_number, line in enumerate(lines): # less specific import
        if f"from {importLocation}" in line:
            # add import to line itself here
            # makes sure all rest framework imports are bundled together
            lines.insert(line_number, f"from {importLocation}.{importModule} import {entity}\n")
            foundSimilarImport = True
            break
    
    if foundSimilarImport:
        with open(file, 'w') as f:
            f.writelines(lines)
            f.close()
        return
    
    # if not any rest framework imports, just add it to first line of code
    lines.insert(0, f"from {importLocation}.{importModule} import {entity}\n")

    with open(file, 'w') as f:
        f.writelines(lines)
        f.close()

def writeClassScope(file: str, scope: str, inClass: str, lines) -> None:
    for line_number, line in enumerate(lines):
        if f"class {inClass}" in line:
            lines.insert(line_number + 1, f"    throttle_scope = \"{scope}\"\n")
            lines.insert(line_number + 2, "    throttle_classes = [ScopedRateThrottle]\n")
            break
    
    with open(file, 'w') as f:
        f.writelines(lines)
        f.close()

def writeFunctionScope(filePath: str, scope: str, function: str, lines: list):
    
    line_number = 0;
    for line_number, line in enumerate(lines):
        if f"def {function}" in line:
            lines.insert(line_number, f"@rate_limit_scope(\"{scope}\")\n")
            break

    with open(filePath, 'w') as file:
        file.writelines(lines)
        file.close()


def write(file: str, scope: str, viewName: str, lines: list) -> None:
    
    viewType = ""
    for line in lines:
        if f"class {viewName}" in line:
            viewType = "class"
            break
        elif f"def {viewName}" in line:
            viewType = "function"
            break

    if viewType == "": 
        return

    if viewType == "class":
        writeImport(file, lines, "rest_framework", "throttling", "UserRateThrottle")
        writeClassScope(file, scope, viewName, lines)
    elif viewType == "function":
            writeImport(file, lines, "middleware", "rate_limit", "rate_limit_scope")
            writeFunctionScope(file, scope, viewName, lines)

def handle(method: str, filePath: str, scope: str, viewName: str):
    fileLines = []
    with open(filePath, 'r') as file:
        fileLines = file.readlines()
        file.close()

    if method == "write":
        write(filePath, scope, viewName, fileLines)
        # print(fileLines)
    elif method == "read":
        return str.join(fileLines)
    
if __name__ == "__main__":    
    arguments = sys.argv[1:] # exclude script path
    #arguments: [type, filePath, scope, viewName]
    handle(arguments[0], arguments[1], arguments[2], arguments[3])