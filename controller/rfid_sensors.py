import serial
# import smbus
# import time

class RFID_Sensors:

    def __init__(self):
        # self.bus = smbus.SMBus(1)
        self.arduino = serial.Serial(
            '/dev/ttyUSB0', baudrate=9600, timeout=0.1)

    def read_RFID(self):
        timeout = 0
        max_timeout = 500
        while self.arduino.in_waiting <= 0 and timeout < max_timeout:
            timeout += 1
        if timeout >= max_timeout:
            return ''
        ser_line = self.arduino.readline().decode('utf-8').rstrip()
        card = ser_line.split(": ")[1]
        return card
'''
if __name__ == '__main__':
    sensors = RFID_Sensors()
    try:
        while True:
            tag = sensors.read_RFID()
            print("id:",tag)
            time.sleep(1)
    except Exception as e:
        print("{}".format(e))
'''
