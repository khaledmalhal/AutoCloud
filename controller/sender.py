import socket
from settings import Settings
from controller.messages import Messages

class Sender():
    def __init__(self, settings: Settings = None):
        self.settings = settings
        self.msg = Messages()
        self.sock = None
        self.connect_socket()
        print("Ready to send sensor data!")

    def connect_socket(self):
        if self.sock is not None:
            self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.settings.get_controller_ip(), 5006))

    def send_sensor_data(self, data: tuple):
        key = data[0]
        value = str(data[1])
        edgedevice = self.settings.get_name()
        try:
            self.sock.sendall(self.msg.sensor_data(key, value, edgedevice))
            return True
        except Exception as e:
            self.settings.set_controller_ip("")
            print(f"Error sending data to Controller ({self.settings.get_controller_ip()}): {e}\nData: ({key}, {value})")
            return False
