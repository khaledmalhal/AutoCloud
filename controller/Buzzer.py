import time
from periphery import GPIO
from Command import COMMAND as cmd

class Buzzer:
    def run(self,command):
        Buzzer_Pin = 146
        buzzer_GPIO = GPIO(Buzzer_Pin, "out")
        if command!="0":
            buzzer_GPIO.write(True)
        else:
            buzzer_GPIO.write(False)
        buzzer_GPIO.close()
if __name__=='__main__':
    B=Buzzer()
    B.run('1')
    time.sleep(3)
    B.run('0')
