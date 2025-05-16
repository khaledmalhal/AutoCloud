import os
import socket
import psutil
import requests
import json
from _thread import *
from time import sleep
from dotenv import load_dotenv
from controller.messages import Messages
from settings import Settings

class Discovery:
    def __init__(self, settings: Settings = None):
        load_dotenv()
        self.settings = settings
        self.msg = Messages()
        self.name = self.settings.get_name()
        self.discover_msg = self.msg.discovery(self.name)
        self.edge_devices = []
        self.api_url = self.settings.get_api_url()
        self.obtain_devices_from_cloud()
        print(f"Obtained the following edge devices for this controller: {[ edge['name'] for edge in self.edge_devices ]}")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', 5006))
        self.sock.listen(1)
        start_new_thread(self.listen_reply, ())

    def obtain_devices_from_cloud(self):
        ret = requests.get(f'{self.api_url}/controller/{self.name}')
        try:
            if ret.ok:
                data = ret.json()
                if len(data['edgedevices']) == 0:
                    return
                self.edge_devices = [edge for edge in data['edgedevices']]
        except Exception as e:
            print(f"Error obtaining Edge Devices: {e}")

    def get_edge(self, edge: str):
        ret = requests.get(f'{self.api_url}/edge/{edge}')
        try:
            if ret.ok:
                data = ret.json()
                return data
        except Exception as e:
            print(f'Error updating edge: {e}')
            return None

    def update_edge(self, edge: str):
        ret = requests.post(f'{self.api_url}/controller/{self.name}/{edge}')
        try:
            if ret.ok:
                return True
        except Exception as e:
            print(f'Error updating edge: {e}')
            return False
        
    def get_interfaces_IPs(self):
        ips = []
        for nic, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    ips.append(addr.address)
        return ips

    def discover_edge_devices(self):
        ips = self.get_interfaces_IPs()
        print(f'[Controller] -> Sending discovery message on {ips}')
        for ip in ips:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((ip, 0))
            sock.sendto(self.discover_msg, ("255.255.255.255", 5005))
            sock.close()

    def listen_reply(self):
        while True:
            conn, addr = self.sock.accept()
            data = conn.recv(1024)
            try:
                ret = eval(data.decode('utf-8'))
                self.parse_client_msg(ret, addr)
            except Exception as e:
                print(f"\nNot possible to parse message from edge: {e}\nData: {data}.\n")
                self.parse_client_msg(data, addr)
            conn.close()

    def parse_client_msg(self, data, addr):
        reply_type = data['type']
        if reply_type == self.msg.DISCOVERY_REPLY:
            edge = next((e for e in self.edge_devices if e['name'] == data['edgedevice']), None)
            if edge == None:
                edge = self.get_edge(data['edgedevice'])
                self.edge_devices.append(edge)
            edge['IP'] = addr[0]
            edge['controller'] = self.name
            self.update_edge(edge['name'])
            print(self.edge_devices)


if __name__ == '__main__':
    discovery = Discovery()
    while True:
        discovery.discover_edge_devices()
        sleep(1)
