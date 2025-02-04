"""Driver for Freenove car

"""

__author__ = "A. Asensio, S. Sanchez"
__credits__ = ["Adrian Asensio", "Sergi Sanchez"]
__version__ = "1.0.1"
__status__ = "Development"

#import sys
#from car import *
import time
from random import random, randint



try:
    from car import *
except ImportError as e:
    print("ERROR:{}".format(e))


try:
    sys.path.insert(0, "/tmp/modules")
except Exception as e:
    print("ERROR:{}".format(e))


try:
    from Motor import *
except ImportError as e:
    print("ERROR:{}".format(e))
#from /tmp/modules/Motor.py import *

'''
try:
    from RPi import *
except ImportError as e:
    print("ERROR:{}".format(e))
'''

try:
    import RPi.GPIO as GPIO
except ImportError as e:
    print("ERROR:{}".format(e))

from AT_Client_vehiculo import AT_Client_vehiculo

class CarPhy(Car): #No heredar de line tracking si no implementarlo aqui directamente!

    #route = Route()

    IR01 = 14
    IR02 = 15
    IR03 = 23
    LMR = 0x00

    augmented_car = None

    def __init__(self, hostname, ip, port, description=None, dns_ip=None, dns_port=None):
        print('INIT Car FeeNove')
        #self.digitaltwin_enable()
        if self.digitaltwin_is_enabled():
            policyId = 'edu.upc.craax:car'
            thingId = 'edu.upc.craax:car'
            # thingId=''
            definitionId = 'edu.upc.craax:car:0.0.1'
            #payload = '{"policyId": "'+policyId+'", "definition": "' + definitionId + '", "attributes": { "name": "Car FreeNove", "description": "Autonomous car" }, "features": { "position": { "properties": { "tagid": ""} }  } }'
            payload = '{"policyId": "' + policyId + '", "definition": "' + definitionId + '", "attributes": { "name": "Car FreeNove", "description": "Autonomous car" }, "features": { "position": { "properties": { "tagid": "", "speed": 0.0, "tstamp": '+str(time.time())+'} }  } }'
            thingId = digitaltwin_create(payload, thingId)
            self.set_digitaltwin_id(thingId)
            #augmented_car = AT_Client_vehiculo('testbed', 'CAR', thingId)
            #augmented_car.conectar()
            #print('3D replica connected!')


        #GPIO.cleanup()
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01, GPIO.IN)
        GPIO.setup(self.IR02, GPIO.IN)
        GPIO.setup(self.IR03, GPIO.IN)
        Car.__init__(self, hostname, ip, port, description, dns_ip, dns_port)
        self.set_virtual(False)

    def follow_line(self):
        try:
            speed_base = 600
            self.set_speed(speed_base)
            #speed_min = 300
            #speed_max = 1200
            count = 0
            count_back = 0
            last_LMR = 0x00
            #latest_speed_factor = self.get_speed_factor()
            #latest_speed = speed_base
            while True:
                try:
                    if self.is_stopped():
                        #speed = 0
                        PWM.setMotorModel(0, 0, 0, 0)
                    elif not self.is_stopped():
                        #print('running')
                        #speed_factor = self.get_speed_factor()
                        speed = self.get_speed()#latest_speed
                        '''
                        if latest_speed_factor!=speed_factor:
                            speed = int(speed * speed_factor)
                            latest_speed_factor = speed_factor

                        if speed < speed_min:
                            speed=speed_min
                        elif speed > speed_max:
                            speed = speed_max

                        if speed>0:
                            #latest_speed = speed
                            self.set_speed(speed)
                        '''
                        self.LMR=0x00

                        if not GPIO.input(self.IR01): #True follow black line
                            self.LMR=(self.LMR | 4) #turn left
                        if not GPIO.input(self.IR02): #True follow black line
                            self.LMR=(self.LMR | 2) #go straight on
                        if not GPIO.input(self.IR03): #True follow black line
                            self.LMR=(self.LMR | 1) #turn right

                        if self.LMR == 0: #out of the line...reduce speed
                            count=count+1

                            max=2
                            max_back=90
                            if count<=max:
                                count_back = 0
                                #speed = 300
                                PWM.setMotorModel(300, 300, 300, 300)
                            elif count_back<=max_back:
                                count_back = count_back +1
                                #speed = -400
                                PWM.setMotorModel(-400, -400, -400, -400)
                            else:
                                #speed=0
                                PWM.setMotorModel(0, 0, 0, 0)
                            '''
                            if count_back>=10:
                                if last_LMR == 1 or last_LMR == 3:
                                    PWM.setMotorModel(1250, 1250, -750, -750)
                                elif last_LMR == 4 or last_LMR == 6:
                                    PWM.setMotorModel(-750, -750, 1250, 1250)
                                else:
                                    count_back = 0
                            else:
                                PWM.setMotorModel(speed, speed, speed, speed)
                            '''
                            #PWM.setMotorModel(speed, speed, speed, speed)
                        else:
                            count = 0
                            count_back = 0
                            if self.LMR == 1 or self.LMR == 3 or self.LMR == 4 or self.LMR == 6:
                                last_LMR = self.LMR


                            if self.LMR == 7:
                                if self.is_turning_right():
                                    PWM.setMotorModel(3000, 3000, -2000, -2000)#PWM.setMotorModel(4000, 4000, -2000, -2000)
                                    time.sleep(0.15)
                                    self.stop_turning_right()
                                    print('right')
                                elif self.is_turning_left():
                                    PWM.setMotorModel(-2000, -2000, 3000, 3000)#PWM.setMotorModel(-2000, -2000, 4000, 4000)
                                    time.sleep(0.15)
                                    self.stop_turning_left()
                                    print('left')
                                elif self.is_going_straight_on():
                                        #speed = int(speed_base * self.get_speed_factor()) #600#int(600 * self.get_speed_factor())#int(speed * 0.8)
                                        PWM.setMotorModel(speed, speed, speed, speed)
                                        time.sleep(0.6)
                                        self.stop_go_straight_on()
                                        print('straight on')
                                else:
                                    #pass
                                    #speed = int(speed_base * self.get_speed_factor()) #400#int(speed * 0.6)
                                    PWM.setMotorModel(speed, speed, speed, speed)
                            elif self.LMR == 5:
                                #speed = 500#int(speed * 0.6)
                                PWM.setMotorModel(speed, speed, speed, speed)
                                #time.sleep(0.1)
                            elif self.LMR==2:
                                PWM.setMotorModel(speed, speed, speed, speed)
                            elif self.LMR==4: #turn left
                               PWM.setMotorModel(-1000,-1000,2000,2000)#PWM.setMotorModel(-1500,-1500,2500,2500)
                            elif self.LMR==6: #turn left
                                PWM.setMotorModel(-1000,-1000,1500,1500)#PWM.setMotorModel(-1500,-1500,2500,2500) #PWM.setMotorModel(-2000, -2000, 4000, 4000)
                                #PWM.setMotorModel(-1500, -1500, 2500, 2500)
                            elif self.LMR==1: #turn right
                                PWM.setMotorModel(2000,2000,-1000,-1000)#PWM.setMotorModel(2500,2500,-1500,-1500)
                            elif self.LMR==3: #turn right
                                PWM.setMotorModel(1500,1500,-1000,-1000)#PWM.setMotorModel(2500,2500,-1500,-1500)#PWM.setMotorModel(4000, 4000, -2000, -2000)
                                #PWM.setMotorModel(2500, 2500, -1500, -1500)
                            else:
                                #speed = 0
                                PWM.setMotorModel(0, 0, 0, 0)
                        '''
                        elif self.LMR==7:
                            if self.is_turning_right():
                                PWM.setMotorModel(2500, 2500, -1500, -1500)
                            elif self.is_turning_left():
                                PWM.setMotorModel(-1500, -1500, 2500, 2500)
                            elif self.is_going_straight_on():
                                PWM.setMotorModel(speed, speed, speed, speed)
                            else:
                                PWM.setMotorModel(speed, speed, speed, speed)
                            #pass
                            #PWM.setMotorModel(0,0,0,0)
                        '''
                    #time.sleep(0.02)
                except Exception as e:
                    print("E4{}".format(e))
        except Exception as e:
            print("E3{}".format(e))
            #time.sleep(0.1)
        finally:
            self.stop()

    def stop(self):
        self.set_stopped(True)
        PWM.setMotorModel(0, 0, 0, 0)
        print("Stop")

    def start(self):
        self.wait_ready()
        self.set_stopped(False)
        print("Follow line")

    def left(self):
        self.set_stopped(True)
        PWM.setMotorModel(-1500,-1500,2500,2500)
        print("Turn left")

    def right(self):
        self.set_stopped(True)
        PWM.setMotorModel(2500,2500,-1500,-1500)
        print("Turn right")