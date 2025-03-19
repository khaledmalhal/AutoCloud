import serial

class Sensors:
    def __init__(self):
        self.esp32 = serial.Serial(
            '/dev/ttyUSB0', baudrate=9600, timeout=None)
        
    def read_line(self):
        try:
            input = self.esp32.read_until(expected=b'\n')
            print(input)
        except Exception as e:
            print("ERROR:{}".format(e))

if __name__ == '__main__':
    sensors = Sensors()
    try:
        while True:
            sensors.read_line()
    except Exception as e:
        print("ERROR:{}".format(e))
        