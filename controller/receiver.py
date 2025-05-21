import socket
import pyping
from controller.messages import Messages
from settings import Settings

class Receiver():
    def __init__(self, settings: Settings = None):
        self.settings = settings
        self.name = self.settings.get_name()
        self.msg = Messages()
        self.discovery_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.commands_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commands_sock.bind(('0.0.0.0', 5006))
        print("Ready to receive!")

    def receive_commands(self):
        data, addr = self.commands_sock.recvfrom(4096)
        try:
            ret = eval(data.decode('utf-8'))
            return (ret, addr)
        except Exception as e:
            print(f'Not possible to parse command from controller: {e}\nData: {data}.\n')
            return (data, addr)

    def ping_ip(self, ip: str) -> bool:
        ret = pyping.ping(ip)
        if ret.ret_code == 0:
            return True
        return False

    def validate_controller(self, known: str, received: str) -> bool:
        if len(known) > 0:
            if known == received:
                # There is not need to reply the Controller.
                return True
            else:
                # It's a different controller that sent a discovery message.
                if self.ping_ip(known):
                    # We check that the controller we know is still alive.
                    # If it is not alive, then we don't have to change
                    # Controllers.
                    return True
        return False

    def wait_for_discovered(self):
        """
        This method waits for the Controller's dicovery message and replies to the Controller.
        When we receive a discovery message from the Controller, we will also save its IP.
        :return: True if it is the same IP as previously saved, False if it's different
                 and we still are connected to the previous one and None in case there was
                 an error at sending the reply.
        """
        data, addr = self.discovery_sock.recvfrom(1024)
        # print(f'Received from {addr}: {data}')
        try:
            ret = eval(data.decode('utf-8'))
            reply = self.reply_controller(ret, addr)
            return reply
        except Exception as e:
            print(f"Not possible to parse message from controller: {e}\nData: {data}.\n")
            return False

    def reply_controller(self, data: dict, addr: tuple):
        if data['type'] == receiver.msg.DISCOVERY:
            controller = self.settings.get_controller_ip()
            if self.validate_controller(controller, addr[0]) is True:
                # If the Controller we know is valid, then we don't have to reply.
                # Else, we need to attempt to connect to the received Controller.
                return True
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((addr, 5005))
                self.settings.set_controller_ip(addr[0])
                ret = sock.sendall(self.msg.discovery_reply(self.name))
                return ret is True
            except Exception as e:
                print(f'[EdgeDevice] -> Error replying to Controller for Discovery')
                return False

if __name__ == '__main__':
    receiver = Receiver()
    while True:
        receiver.wait_for_discovered()