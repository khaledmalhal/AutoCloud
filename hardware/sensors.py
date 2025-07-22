import serial
import os

class Sensors:
    def __init__(self, name='nodevice'):
        self.esp32 = serial.Serial(
            '/dev/ttyUSB0', baudrate=9600, timeout=None)
        self.name = name

    def read_line(self):
        input = self.esp32.read_until(expected=b'\n')
        input = input.decode('utf-8').split(":")
        key   = input[0]
        value = input[1][:-1].strip()
        print(f'Key: {key}. Value: {value}.')
        return (key, value)


if __name__ == '__main__':
    sensors = Sensors(name='autocloud1')
    try:
        while True:
            sensors.read_line()
    except Exception as e:
        print("ERROR:{}".format(e))
