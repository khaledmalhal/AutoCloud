import socket
from controller.messages import Messages
from settings import Settings

class Receiver():
    def __init__(self, settings: Settings = None):
        self.settings = settings
        self.name = self.settings.get_name()
        self.msg = Messages()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(('0.0.0.0', 5005))
        print("Ready to receive!")

    def receive(self):
        data, addr = self.sock.recvfrom(1024)
        print(f'Received from {addr}: {data}')
        try:
            ret = eval(data.decode('utf-8'))
            return (ret, addr)
        except Exception as e:
            print(f"Not possible to parse message from controller: {e}\nData: {data}.\n")
            return (data, addr)

    def reply_controller(self, ip: str):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, 5005))
        return sock.sendall(self.msg.discovery_reply(self.name))

if __name__ == '__main__':
    receiver = Receiver()
    while True:
        receiver.receive()