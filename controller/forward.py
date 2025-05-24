import socket
import os
import sys
from _thread import *
from settings import Settings
from controller.messages import Messages
from controller.edgedevices import EdgeDevices
from influx_api.upload import Influx

class Forward():
    """
    This class listens for data incoming from the edge devices and
    commands that the Cloud want to send to the edge devices.
    """
    def __init__(self, settings: Settings = None, edgedevices: EdgeDevices = None):
        self.influx = Influx(settings)
        self.msg = Messages()
        self.edgedevices = edgedevices
        self.last_CardUID = ""

        # TCP Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', 5006))
        self.sock.listen(1)
        start_new_thread(self.listen_data, ())

    def upload_sensor_data(self, key: str, value: str, from_edge: str):
        """
        Here, we do any pre-processing if needed for the data.
        For example, we don't send the same read Card UID, otherwise we will saturate the DB.
        """
        upload_ready = True
        if key == "Card UID":
            if value != self.last_CardUID:
                self.last_CardUID = value
            else:
                upload_ready = False
        if upload_ready == True:
            try:
                self.influx.upload_data((key, value), from_edge)
            except Exception as e:
                print(f'Error uploading data to InfluxDB:\n\t->{e}')

    def send_data(self, edge_ip: str, data: dict):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((edge_ip, 5006))
        ret = sock.sendall(str(data).encode('utf-8'))
        print(ret)
        sock.close()
        return ret is None

    def parse_command(self, edge: dict, data: dict):
        # Parse the command and forward it to the Edge Device
        command = data['command']
        if 'ip' not in edge.keys():
            raise Exception("Unknown Edge Device's IP.")
        if command == self.msg.COMMAND_PRINT:
            ip = edge['ip']
            self.send_data(ip, data)

    def parse_msg(self, sock: socket.socket, data: dict, addr: tuple[str, str]):
        """
        Parse the messages obtained from the Edge Device and validate the message.
        """
        reply_type = data['type']
        if reply_type == self.msg.SENSOR_DATA:
            keys = data.keys()
            if 'key' in keys and 'value' in keys and 'edgedevice' in keys:
                key = data['key']
                value = data['value']
                edgedevice = data['edgedevice']
                self.upload_sensor_data(key, value, edgedevice)

        if reply_type == self.msg.COMMAND_EDGE:
            # If the command was not send from the Cloud, then don't forward it
            print(addr[0])
            if addr[0] != '10.0.0.49':
                raise Exception("The command is not from the Cloud. We will not accept commands that are not from the Cloud.")
            # Validate message and then parse the command
            keys = data.keys()
            if not("edgedevice" in keys and "command" in keys and "message" in keys and "id" in keys):
                raise Exception("Command message has a wrong format.")
            edge = data['edgedevice']
            device = self.edgedevices.get_edge_in_list(edge)
            if device is None:
                raise Exception("Edge device is not in this controller")
            self.parse_command(device, data)

        if reply_type == self.msg.CLOUD_PING:
            # Respond a Cloud's ping
            return sock.sendall(self.msg.cloud_ping_reply()) is None

        if reply_type == self.msg.COMMAND_REPLY:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('10.0.0.49', 5007))
            return sock.sendall(str(data).encode('utf-8')) is None

    def listen_data(self):
        while True:
            conn, addr = self.sock.accept()
            pid = os.fork()
            if pid == 0:
                # Create a child that has the open socket with the Edge Device
                # and the parent will continue to read accept new sockets.
                while True:
                    data = conn.recv(1024)
                    if len(data) == 0:
                        continue
                    try:
                        ret = eval(data.decode('utf-8'))
                        self.parse_msg(conn, ret, addr)
                    except Exception as e:
                        print(f"\nNot possible to forward message: {e}\nData: {data}.\n")
                        conn.close()
                        sys.exit(1)