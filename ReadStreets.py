import serial
import sys
import datetime

sys.path.append('controller')
from Line_Tracking import *
from RFID import *

class ReadStreets():
    def __init__(self):
        self.line = Line_Tracking()
        self.readTag = []
        self.unknown = []
        self.error   = []
        self.card = ""
        self.tagNames = list(RFIDTAG.__members__.keys())
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.ser.reset_input_buffer()

    def output_debug(f, mesg, array):
        if len(array) > 0:
            f.write(mesg)
            for item in array:
                f.write(' '.join(item)+'\n')

    def run(self):
        self.line.run()
        if self.ser.in_waiting > 0:
            ser_line = self.ser.readline().decode('utf-8').rstrip()
            try:
                new_card = ser_line.split(": ")[1]
                print(new_card)
                if new_card != card and new_card not in self.readTag:
                    card = new_card
                    name = RFIDTAG(card).name
                    self.readTag.append(card)
                    print(name)
                    if name in tagNames:
                        tagNames.remove(name)
                        print(F'Found {name}')
                    else:
                        self.unknown.append(name)
                    print(card)
            except:
                print("Not a card detected, probably.")
                self.error.append(ser_line)

def main():
    streets = ReadStreets()
    try:
        while True:
            streets.run()
    except KeyboardInterrupt:
        streets.line.IR01_GPIO.close()
        streets.line.IR02_GPIO.close()
        streets.line.IR03_GPIO.close()
        PWM.setMotorModel(0,0,0,0)
        with open('debug.log', 'a') as f:
            f.write(datetime.datetime.now())
            streets.output_debug(f, '\n_____________________\nTags that car read:\n', streets.readTag)
            streets.output_debug(f, '_____________________\nMissing tags that car did not read:\n', streets.tagNames)
            streets.output_debug(f, '_____________________\nUnknown tags:\n', streets.unknown)
            streets.output_debug(f, '_____________________\nError:\n', streets.error)
        print("\nEnd of program")

if __name__ == '__main__':
    main()
