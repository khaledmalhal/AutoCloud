import socket
from _thread import *
from ping3 import ping
from controller.messages import Messages
from controller.commandExec import CommandExec
from settings import Settings

class Receiver():
    def __init__(self, settings: Settings = None):
        self.settings = settings
        self.name = self.settings.get_name()
        self.msg = Messages()
        self.executer = CommandExec(settings)

        self.discovery_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.discovery_sock.bind(('0.0.0.0', 5005))

        self.controller_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.controller_sock.bind(('0.0.0.0', 5006))
        self.controller_sock.listen(1)
        start_new_thread(self.receive_commands, ())
        print("Ready to receive!")

    def receive_commands(self):
        while True:
            conn, addr = self.controller_sock.accept()
            data = conn.recv(4096)
            try:
                ret = eval(data.decode('utf-8'))
                exec, msg = self.executer.execute(ret)
                if exec is True:
                    conn.sendall(self.msg.command_reply(ret['edgedevice'], ret['id'], Messages.SUCCESS_STATUS))
                else:
                    conn.sendall(self.msg.command_reply(ret['edgedevice'], ret['id'], Messages.FAILED_STATUS))
                conn.close()
            except Exception as e:
                print(f'Not possible to parse command from controller: {e}\nData: {data}.\n')
                return (data, addr)
            conn.close()

    def ping_ip(self, ip: str) -> bool:
        ret = ping(ip, timeout=2)
        if ret:
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
        if data['type'] == self.msg.DISCOVERY:
            controller = self.settings.get_controller_ip()
            if self.validate_controller(controller, addr[0]) is True:
                # If the Controller we know is valid, then we don't have to reply.
                # Else, we need to attempt to connect to the received Controller.
                return True
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((addr[0], 5005))
                ret = sock.sendall(self.msg.discovery_reply(self.name))
                self.settings.set_controller_ip(addr[0])
                if ret is None:
                    print(f"Connect to a new Controller -> {addr[0]}")
                return ret is None
            except Exception as e:
                print(f'[EdgeDevice] -> Error replying to Controller for Discovery')
                return False

if __name__ == '__main__':
    receiver = Receiver()
    while True:
        receiver.wait_for_discovered()
