import socket

class msg:
    def __init__(self, msg):
        self.msg = msg

class network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "" # replace this with your ip
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()

    def getP(self):
        return self.id
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
    def send(self,data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
