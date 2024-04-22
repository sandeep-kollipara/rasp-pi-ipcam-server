import socket
from threading import *

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#host = ""
port = 10050
#print (host)
#print (port)
#serversocket.bind((host, port))
hostname = socket.gethostname()
dns_resolved_addr = socket.gethostbyname(hostname)
serversocket.bind((dns_resolved_addr, port))
print(dns_resolved_addr)

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            print('Client sent:', self.sock.recv(1024).decode())
            self.sock.send(b'Oi you sent something to me')

serversocket.listen(5)
print ('server started and listening')
while 1:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)
