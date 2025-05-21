import socket
import psutil
from ping3 import ping
from _thread import *
from time import sleep
from controller.messages import Messages
from controller.edgedevices import EdgeDevices
from settings import Settings

class Discovery:
    def __init__(self, settings: Settings = None, edgedevices: EdgeDevices = None):
        self.settings = settings
        self.msg = Messages()
        self.name = self.settings.get_name()
        self.discover_msg = self.msg.discovery(self.name)
        self.edgedevices = edgedevices
        self.api_url = self.settings.get_api_url()

        # TCP Socket for Edge-Controller communication
        self.sock_edge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_edge.bind(('0.0.0.0', 5005))
        self.sock_edge.listen(1)

        # TCP Socket for Controller-Cloud communication
        self.sock_cloud = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        start_new_thread(self.listen_reply, ())
        start_new_thread(self.ping_edge_devices, ())
        
    def get_interfaces_IPs(self):
        ips = []
        for nic, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    ips.append(addr.address)
        return ips

    def discover_edge_devices(self):
        ips = self.get_interfaces_IPs()
        # print(f'[Controller] -> Sending discovery message on {ips}')
        for ip in ips:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((ip, 0))
            sock.sendto(self.discover_msg, ("255.255.255.255", 5005))
            sock.close()

    def parse_cloud_msg(self, data: dict, conn: socket.socket, addr: tuple):
        msg_type = data['type']
        print(msg_type)
        if msg_type == self.msg.CLOUD_PING_REPLY:
            # I should reply and let the Cloud know that I am alive
            pass

    def ping_edge_devices(self):
        while True:
            devices = self.edgedevices.get_edge_devices()
            for device in devices:
                if 'ip' not in device.keys():
                    continue
                name = device['name']
                ip = device['ip']
                print(f'Pinging {name} ({ip})')
                ret = ping(device['ip'], timeout=2)
                if ret:
                    continue
                print(f'Unlinking {name}')
                self.edgedevices.unlink_edge(device['name'])
            sleep(10)

    def listen_reply(self):
        while True:
            conn, addr = self.sock_edge.accept()
            data = conn.recv(1024)
            try:
                ret = eval(data.decode('utf-8'))
                self.parse_client_msg(ret, addr)
            except Exception as e:
                print(f"\nNot possible to parse message from edge: {e}\nData: {data}.\n")
                self.parse_client_msg(data, addr)
            conn.close()

    def parse_client_msg(self, data, addr):
        # We filter all the possible messages that the Edge Device could give us.
        reply_type = data['type']
        if reply_type == self.msg.DISCOVERY_REPLY:
            self.edgedevices.append_or_update(data['edgedevice'], addr[0])


if __name__ == '__main__':
    discovery = Discovery()
    while True:
        discovery.discover_edge_devices()
        sleep(1)
