from colorama import Fore, Style
import msvcrt, os, platform

from mod.file import handle
from mod.tojson import readJson, writeJson    

clearCommand = 'cls' if platform.system() == 'Windows' else 'clear'
# ugly code but gets the job done 
class Endpoint(): 
    def __init__(self, location, viewName, index, database):
        self.index: int = index
        self.path: str = location
        self.view_name: str = viewName
        self.database: Database = database

        info = self.database.json[self.index]
        self.why = info["why"]
        self.scope = info["scope"]
        self.status = info["status"]

    def getContent(self):
        content = ""
        with open(self.path, 'r') as file:
            content = file.read()
            file.close()

        return content

class Database():
    def __init__(self, filePath):
        self.path = filePath
        self.json = readJson(filePath)
        self.active_endpoints = [self.newEndpoint(i) for i in range(10)]

    def updateDatabase(self, endpoint: Endpoint):
        self.json[endpoint.index]["scope"] = endpoint.scope
        self.json[endpoint.index]["why"] = endpoint.why
        self.json[endpoint.index]["status"] = endpoint.status

        writeJson(self.json, self.path)

    def newEndpoint(self, index): # return Endpoint with info from database
        
        info = self.json[index]
        endpoint = Endpoint(
            info["path"],
            info["viewName"],
            index,
            self
        )

        return endpoint

    def updateEndpoint(self, endpoint: Endpoint, scope="", why=""):

        endpoint.scope = endpoint.scope if scope == "" else scope # doesnt update if its empty
        endpoint.why = endpoint.why if why == "" else why

        if endpoint.scope == "x":
            endpoint.scope = ""
        
        if endpoint.scope != "":
            endpoint.status = True
        else:
            endpoint.status = False

        self.updateDatabase(endpoint)

        handle("write", endpoint.path, endpoint.scope, endpoint.view_name) # review this!!!
        # this takes care of the file itself check if it's correct in your situation

database = Database("database.json")
inputChar = ' '
pointer = 0

def printTable(active: list, pointer: int):
    
    for endpoint in active:
        full_path = f"{endpoint.path}.{endpoint.view_name}"
        print(
            Fore.GREEN if endpoint.status else Fore.RED,
            f"{endpoint.index}{' '*(4 - len(str(endpoint.index)))}",
            Fore.CYAN if endpoint.index == pointer else Fore.WHITE, f"|  {endpoint.path}.{endpoint.view_name}{' '*(60 - len(full_path))}",
            Fore.WHITE + '|' + endpoint.scope
        )
        print('-' * 85)

def categorizeScope(endpoint: Endpoint):

    scope = input("Enter Scope: ")
    why = input("Why? ")
    endpoint.database.updateEndpoint(endpoint, scope, why)

def selectEndpoint(index):
    inputChar = ''
    while inputChar != '3':
        os.system(clearCommand)
        activeEndpoint = next((endpoint for endpoint in database.active_endpoints if endpoint.index == index), None)

        if activeEndpoint == None:
            activeEndpoint = database.newEndpoint(index)
        print(
            Fore.BLUE + activeEndpoint.path + Fore.YELLOW + '.' + activeEndpoint.view_name, 
            "\n\n" + Fore.BLUE + "Scope:" + Fore.WHITE + activeEndpoint.scope, 
            Fore.BLUE + "\nWhy:" + Fore.WHITE + activeEndpoint.why +
            (Fore.GREEN + "\n\nFinished" if activeEndpoint.status else Fore.RED + "\n\nNo Scope"), 
            Fore.WHITE
            )       
        print("\n\nSelect action:\n1 - update endpoint\n2 - open file\n3 - close")
        inputChar = msvcrt.getch().decode()
        match inputChar:
            case '1':
                categorizeScope(activeEndpoint)
            case '2':
                activeEndpoint.getContent()

def changePointer(changeTo):
    endpoint = next((endpoint for endpoint in database.active_endpoints if endpoint.index == pointer), None)
    if endpoint == None:
        database.active_endpoints = [database.newEndpoint(i) for i in range(int(pointer / 10) * 10, int(pointer / 10) * 10 + 10)]
        endpoint = next((endpoint for endpoint in database.active_endpoints if endpoint.index == pointer), None)

    return endpoint

endpoint = database.newEndpoint(pointer)
while inputChar != 'x':
    os.system(clearCommand)
    # print(list(range(30, 5)))
    printTable(database.active_endpoints, pointer)
    print("i - Select endpoint    n - Next endpoint     p - change pointer      x - exit")
    status = "Finished" if endpoint.scope != "" else "No Scope"
    print(f"\n\n{endpoint.path}.{endpoint.view_name}\nScope: {endpoint.scope}\nWhy: {endpoint.why}\n{status}")

    inputChar = msvcrt.getch().decode()

    match inputChar:
        case 'i':
            targetIndex = int(input("Enter endpoint index: "))
            inputChar = selectEndpoint(targetIndex)
        case 'p':
            pointer = int(input("Change pointer to "))
            endpoint = changePointer(pointer)
        case 'n':
            scope = ""
            while scope != "exit":    
                pointer += 1
                endpoint = changePointer(pointer)
                # selectEndpoint(pointer)
                os.system(clearCommand)
                printTable(database.active_endpoints, pointer)
                scope = input("To exit, type exit in scope\nFor further commands, type select\n" + Fore.CYAN + "Scope: " + Fore.WHITE)
                if scope == "exit":
                    break
                elif scope == "select":
                    selectEndpoint(pointer)
                    continue
                
                why = input(Fore.CYAN + "Why? " + Fore.WHITE)
                endpoint.database.updateEndpoint(endpoint, scope, why)