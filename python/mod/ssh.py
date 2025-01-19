import pexpect

class Connection(object):
    def __init__(self, hostname, username, password):
        self.username = username
        self.hostname = hostname
        self.password = password

        self.child = pexpect.spawn(f"ssh {username}@{hostname}")
        self.child.expect("password:")
        self.child.sendline(password)

        self.child.expect(f"{username}@")

    def scp(self, localPath, remotePath):
        self.child.sendline(f"scp {localPath} {self.username}@{self.hostname}:{remotePath}")
        self.child.expect("password:")
        self.child.sendline(self.password)
        self.child.expect(f"{self.username}@") # wait for answer

    def runPythonFile(self, remotePath):
        self.child.sendline(f"python3 {remotePath}")
        self.child.expect(f"{self.username}@") # wait for script to end

        output = self.child.before.decode()
        return output
        