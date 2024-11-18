import serial
import sys
sys.path.append('controller')
from threading import Thread
from Line_Tracking import *
from RFID import *

def main():
    line = Line_Tracking()
    readTag = []
    card = ""
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    tagNames = RFIDTAG.__members__.keys()
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
                    new_card = ser_line.split("Card UID: ")[1]
                    if new_card != card:
                        card = new_card
                        name = RFIDTAG.name(card)
                        if name in tagNames:
                            del tagNames[name]
                        if card not in readTag:
                            readTag.append(card)
                        print(card)
                except:
                    print("Not a card detected, probably.")

    except KeyboardInterrupt:
        PWM.setMotorModel(0,0,0,0)
        line.IR01_GPIO.close()
        line.IR02_GPIO.close()
        line.IR03_GPIO.close()
        print(tagNames)
        with open('all_cards.txt', 'w') as f:
            for card in readTag:
                f.write(' '.join(card)+'\n')
        print("\nEnd of program")


if __name__ == '__main__':
    main()
