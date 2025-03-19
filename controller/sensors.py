import serial
import os
import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

class Sensors:
    load_dotenv()
    def __init__(self, name='nodevice'):
        self.esp32 = serial.Serial(
            '/dev/ttyUSB0', baudrate=9600, timeout=None)
        self.name = name
        self.bucket = os.getenv("INFLUXDB_BUCKET")
        self.token  = os.getenv("INFLUXDB_TOKEN")
        self.org    = os.getenv("INFLUXDB_ORG")
        self.url    = os.getenv("INFLUXDB_URL")
        self.client = influxdb_client.InfluxDBClient(
            url   = self.url,
            token = self.token,
            org   = self.org
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def read_line(self):
        try:
            input = self.esp32.read_until(expected=b'\n')
            input = input.decode('utf-8').split(":")
            key   = input[0]
            value = input[1][:-1]
            print(f'Key: {key}. Value: {value}.')

            if key == 'Photoresistor':
                measurement = "light"
                field = "light"
            elif key == 'Card UID':
                measurement = "street"
                field = "RFID"
            point = Point(measurement).tag("name", self.name).field(field, value)
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
            return (key, value)
        except Exception as e:
            print("ERROR:{}".format(e))

if __name__ == '__main__':
    sensors = Sensors(name='autocloud-1')
    try:
        while True:
            sensors.read_line()
    except Exception as e:
        print("ERROR:{}".format(e))
