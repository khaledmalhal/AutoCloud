import time
from Motor import *
from periphery import GPIO

class Line_Tracking:
    def __init__(self):
        self.IR01 = 148
        self.IR02 = 147
        self.IR03 = 154
        self.IR01_GPIO = GPIO(self.IR01, 'in')
        self.IR02_GPIO = GPIO(self.IR02, 'in')
        self.IR03_GPIO = GPIO(self.IR03, 'in')
    def run(self):
        while True:
            self.LMR=0x00
            if self.IR01_GPIO.read() != True:
                self.LMR=(self.LMR | 4)
            if self.IR02_GPIO.read() != True:
                self.LMR=(self.LMR | 2)
            if self.IR03_GPIO.read() != True:
                self.LMR=(self.LMR | 1)

            if self.LMR==2:
                # Move forward
                PWM.setMotorModel(800,800,800,800)
            elif self.LMR==4:
                # Move left
                PWM.setMotorModel(-1500,-1500,2500,2500)
            elif self.LMR==6:
                # Move left sharp
                PWM.setMotorModel(-2000,-2000,4000,4000)
            elif self.LMR==1:
                # Move left
                PWM.setMotorModel(2500,2500,-1500,-1500)
            elif self.LMR==3:
                # Move left sharp
                PWM.setMotorModel(4000,4000,-2000,-2000)
            elif self.LMR==7:
                #pass
                PWM.setMotorModel(0,0,0,0)
            
infrared=Line_Tracking()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0,0,0,0)
        infrared.IR01_GPIO.close()
        infrared.IR02_GPIO.close()
        infrared.IR03_GPIO.close()
