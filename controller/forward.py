import socket
import os
import sys
from _thread import *
from settings import Settings
from controller.messages import Messages
from influx_api.upload import Influx

class Forward():
    def __init__(self, settings: Settings = None):
        self.influx = Influx(settings)
        self.msg = Messages()
        self.last_CardUID = ""

        # TCP Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', 5006))
        self.sock.listen(1)
        start_new_thread(self.listen_data, ())

    def upload_sensor_data(self, key: str, value: str):
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
                self.influx.upload_data((key, value))
            except Exception as e:
                print(f'Error uploading data to InfluxDB:\n\t->{e}')

    def parse_edge_msg(self, data: dict, addr: tuple[str, str]):
        """
        Parse the messages obtained from the Edge Device and validate the message.
        """
        reply_type = data['type']
        if reply_type == self.msg.SENSOR_DATA:
            keys = data.keys()
            if 'key' in keys and 'value' in keys:
                key = data['key']
                value = data['value']
                self.upload_sensor_data(key, value)

    def listen_data(self):
        while True:
            conn, addr = self.sock.accept()
            pid = os.fork()
            if pid == 0:
                # Create a child that has the open socket with the Edge Device
                # and the parent will continue to read accept new sockets.
                while True:
                    data = conn.recv(1024)
                    try:
                        ret = eval(data.decode('utf-8'))
                        self.parse_edge_msg(ret, addr)
                    except Exception as e:
                        print(f"\nNot possible to parse message from edge: {e}\nData: {data}.\n")
                        conn.close()
                        sys.exit(1)