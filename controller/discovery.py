import socket
import psutil
import messages
from time import sleep

class Discovery:
    def __init__(self, name='no_controller'):
        msg = messages.Messages(name)
        self.discover_msg = str.encode(msg.discovery)
        print(self.discover_msg)

    def get_interfaces_IPs(self):
        ips = []
        for nic, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    ips.append(addr.address)
        return ips

    def discover_edge_devices(self):
        ips = self.get_interfaces_IPs()

        for ip in ips:
            print(f'Sending discovery message on {ip}')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((ip, 0))
            sock.sendto(self.discover_msg, ("255.255.255.255", 5005))
            sock.close()

if __name__ == '__main__':
    discovery = Discovery()
    while True:
        discovery.discover_edge_devices()
        sleep(1)
