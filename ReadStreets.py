import serial
import sys
import datetime
sys.path.append('controller')
from threading import Thread
from Line_Tracking import *
from RFID import *

def output_debug(f, mesg, array):
    if len(array) > 0:
        f.write(mesg)
        for item in array:
            f.write(' '.join(item)+'\n')

def main():
    line = Line_Tracking()
    readTag = []
    unknown = []
    error   = []
    card = ""
    tagNames = list(RFIDTAG.__members__.keys())
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    try:
        thread = Thread(target=line.run)
        thread.start()
        print("Started thread")
        print("Started reading")
        while True:
            # if   line.IR01_GPIO.read() != True and line.IR02_GPIO.read() == True and line.IR03_GPIO.read() != True:
            #     print ('Middle')
            # elif line.IR01_GPIO.read() != True and line.IR02_GPIO.read() != True and line.IR03_GPIO.read() == True:
            #     print ('Right')
            # elif line.IR01_GPIO.read() == True and line.IR02_GPIO.read() != True and line.IR03_GPIO.read() != True:
            #     print ('Left')
            if ser.in_waiting > 0:
                ser_line = ser.readline().decode('utf-8').rstrip()
                try:
                    new_card = ser_line.split(": ")[1]
                    print(new_card)
                    if new_card != card and new_card not in readTag:
                        card = new_card
                        name = RFIDTAG(card).name
                        readTag.append(card)
                        print(name)
                        if name in tagNames:
                            tagNames.remove(name)
                            print(F'Found {name}')
                        else:
                            unknown.append(name)
                        print(card)
                except:
                    print("Not a card detected, probably.")
                    error.append(ser_line)

    except KeyboardInterrupt:
        line.IR01_GPIO.close()
        line.IR02_GPIO.close()
        line.IR03_GPIO.close()
        PWM.setMotorModel(0,0,0,0)
        print(F'Tags that car read:\n{readTag}\n_____________________')
        print(F'Missing tags that car did not read:\n{tagNames}\n_____________________')
        print(F'Unknown tags:\n{unknown}\n_____________________')
        print(F'Error: \n{error}\n_____________________')
        with open('all_cards.txt', 'a') as f:
            f.write(datetime.datetime.now())
            output_debug(f, '\n_____________________\nTags that car read:\n', readTag)
            output_debug(f, '_____________________\nMissing tags that car did not read:\n', tagNames)
            output_debug(f, '_____________________\nUnknown tags:\n', unknown)
            output_debug(f, '_____________________\nError:\n', error)
        print("\nEnd of program")

if __name__ == '__main__':
    main()
