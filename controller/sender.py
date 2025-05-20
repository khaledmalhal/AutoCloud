import socket
from settings import Settings
from controller.messages import Messages

class Sender():
    def __init__(self, settings: Settings = None):
        self.settings = settings
        self.msg = Messages()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.update_socket_bind()
        print("Ready to send sensor data!")

    def send_sensor_data(self, data: tuple[str, str]):
        self.sock.connect((self.settings.controller_ip, 5006))
        self.sock.sendall(self.msg.sensor_data(data[0], data[1]))
