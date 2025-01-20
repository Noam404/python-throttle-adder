from colorama import Fore, Style
import msvcrt, os, platform

from mod.file import handle
from mod.tojson import readJson, writeJson    

clearCommand = 'cls' if platform.system() == 'Windows' else 'clear'

class Endpoint():
    def __init__(self, location, viewName, index, database):
        self.index: int = index
        self.path: str = location
        self.view_name: str = viewName
        self.why = "",
        self.scope = "",
        self.status = False,
        self.database: Database = database

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
        self.active_endpoints = [self.newEndpoint(i) for i in range(5)]

    def update(self, endpoint: Endpoint):
        self.json[endpoint.index]["why"] = endpoint.why
        self.json[endpoint.index]["scope"] = endpoint.scope

        writeJson(self.json, self.path)

    def newEndpoint(self, index):
        
        info = self.json[index]
        endpoint = Endpoint(
            info["path"],
            info["viewName"],
            index,
            self
        )
        endpoint.status = info["status"]
        endpoint.why = info["why"]
        endpoint.scope = info["scope"]

        return endpoint

    def updateInfo(scope="", why=""):

        self.scope = self.scope if scope == "" else scope
        self.why = self.why if scope == "" else why

        self.database.update(self)

def printTable(database: Database):
    
    for endpoint in database.active_endpoints:
        full_path = f"{endpoint.path}.{endpoint.view_name}"
        print(
            Fore.GREEN if endpoint.status else Fore.RED,
            f"{endpoint.index}{' '*(4 - len(str(endpoint.index)))}",
            Fore.WHITE, f"|  {endpoint.path}.{endpoint.view_name}{' '*(60 - len(full_path))}|",
            Fore.BLUE, endpoint.scope, Fore.WHITE
        ) # don't even try to understand whats going on here its not gonna be changed anyways
        print('-' * 85)

database = Database("database.json")
inputChar = ' '
while inputChar != 'x':
    os.system(clearCommand)
    printTable(database)
    print("i - Open endpoint\nn - next endpoint")

    inputChar = msvcrt.getch().decode()
