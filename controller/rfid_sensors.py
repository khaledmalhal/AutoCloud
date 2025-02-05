import serial
# import smbus
# import time

class RFID_Sensors:

    def __init__(self):
        # self.bus = smbus.SMBus(1)
        self.arduino = serial.Serial(
            '/dev/ttyACM0', baudrate=9600, timeout=0.1)

    def read_RFID(self):
        self.arduino.flushInput()
        while self.arduino.inWaiting() < 15:
            pass
        c = self.arduino.read(15)
        text = c.decode()
        return text.strip()

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