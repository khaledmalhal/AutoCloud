import serial
import sys
import datetime
import signal

sys.path.append('controller')
from Line_Tracking import *
from RFID import *

class ReadStreets():
    def __init__(self):
        self.readTag = []
        self.unknown = []
        self.error   = []
        self.card = ""
        self.tagNames = list(RFIDTAG.__members__.keys())
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.ser.reset_input_buffer()

    def output_debug(self, f, mesg, array):
        if len(array) > 0:
            f.write(mesg)
            for item in array:
                f.write(' '.join(item)+'\n')

    def read_streets(self):
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
    # r_rfid, w_rfid = os.pipe()
    # r_rfid, w_rfid = os.fdopen(r_rfid, 'r', 0), os.fdopen(w_rfid, 'w', 0)

    # r_line, _ = os.pipe()
    # r_line    = os.fdopen(r_line, 'r', 0)

    pid_line = os.fork()
    pid_rfid = 0

    try:
        if pid_line:        # Parent
            pid_rfid = os.fork()
            if pid_rfid:    # Parent
                print("##### I'm parent waiting for my children to finish")
                signal.pause()
                # os.waitid(os.P_PID, pid_rfid, os.WSTOPPED)
                print("##### I'm parent and my children have finished")
            else:       # RFID child
                print("$$$$$ I'm RFID child!")
                streets = ReadStreets()
                try:
                    while True:
                        streets.read_streets()
                except KeyboardInterrupt:
                    print("KeyboardInterrupt for RFID")
                    streets.ser.close()
                    with open('debug.log', 'a') as f:
                        f.write(str(datetime.datetime.now()))
                        streets.output_debug(f, '\n_____________________\nTags that car read:\n'              , streets.readTag)
                        streets.output_debug(f, '_____________________\nMissing tags that car did not read:\n', streets.tagNames)
                        streets.output_debug(f, '_____________________\nUnknown tags:\n'                      , streets.unknown)
                        streets.output_debug(f, '_____________________\nError:\n'                             , streets.error)
        else:   # Line child
            print("@@@@@ I'm line child!")
            line = Line_Tracking()
            try:
                while True:
                    line.run()
            except KeyboardInterrupt:
                print("KeyboardInterrupt for Line")
                PWM.setMotorModel(0,0,0,0)
                line.IR01_GPIO.close()
                line.IR02_GPIO.close()
                line.IR03_GPIO.close()
                print("Finished closing all GPIOs")
    except KeyboardInterrupt:
        # Only the parent can send these signals
        print("KeyboardInterrupt. pid_line: %d\tpid_rfid: %d\n" % (pid_line, pid_rfid))
        # if pid_line and pid_rfid:
        #     os.kill(pid_line, signal.SIGINT)
        #     os.kill(pid_rfid, signal.SIGINT)

if __name__ == '__main__':
    main()
