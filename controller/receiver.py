import socket
import json

class Receiver():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(('0.0.0.0', 5005))

    def receive(self):
        data, addr = self.sock.recvfrom(1024)
        print(f'Received from {addr}: {data}')

if __name__ == '__main__':
    receiver = Receiver()
    while True:
        receiver.receive()