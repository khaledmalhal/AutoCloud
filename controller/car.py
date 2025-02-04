"""Car

This script implements the `Car` abstract class. It inherits from
the Device class.

"""

__author__ = "A. Asensio, S. Sanchez"
__credits__ = ["Adrian Asensio", "Sergi Sanchez"]
__version__ = "1.0.1"
__status__ = "Development"

from math import tan
from random import random

from device import *

'''
try:
    sys.path.insert(0, "/tmp/modules")
except Exception as e:
    print("ERROR:{}".format(e))

try:
    #import RPi.GPIO as GPIO
    from RPi import *
except ImportError as e:
    print("CAR-ERROR:{}".format(e))
'''

try:
    from rfid_sensors import RFID_Sensors
except ImportError as e:
    print("ERROR:{}".format(e))

from multiprocessing import current_process
import multiprocessing as mp

# from route import Route

try:
    import smbus
except ImportError as e:
    print("ERROR:{}".format(e))


class Car(Device):
    __q = None
    __rfid_tag = None
    __rfid_tag_previous = None
    __stopped = True
    __turn_left = False
    __turn_right = False
    __straight_on = False
    __rfid_sensor = False
    __speed = 0
    __speed_prev = 0
    __speed_factor = 1.0
    __speed_factor_prev = 1.0
    ready = False
    _route = Route()

    # MIFAREReader = None

    def __init__(self, hostname, ip, port, description=None, dns_ip=None, dns_port=None):
        Device.__init__(self, hostname, ip, port, description, dns_ip, dns_port)

    def __del__(self):
        print("destructing")

    def __read_rfid(self):

        last_read_tagid = RFIDTAG.NOTAG
        try:
            sensors = RFID_Sensors()
            print("RFID is available in the car.")
            self.__q.put(RFID_SENSOR.AVAILABLE)
        except Exception as e:
            print("RFID is not available in the car.")
            self.__q.put(RFID_SENSOR.NOT_AVAILABLE)
            return

        start_time = time.time()
        while True:
            try:
                tagid = sensors.read_RFID()
                print("id:", tagid)
                if tagid != last_read_tagid:
                    if is_valid_tag(tagid):  # Ver si existe en la lista de tags if l in ....
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        start_time = end_time
                        print("Valid tagid: " + tagid)
                        # last_read_tagid = tagid
                        try:
                            self.__q.put(tagid)
                        except Exception as e:
                            print("E5{}".format(e))
                        try:
                            if self.digitaltwin_is_enabled() and tagid is not None:
                                print('Update DT...')
                                thingId = self.get_digitaltwin_id()  # 'edu.upc.craax:trafficlights'
                                print(thingId + "tagId: " + tagid)
                                print("!!!!! " + str(RFIDTAG(tagid)))
                                distance = get_distance_between_tags(last_read_tagid, tagid)
                                print(distance)
                                print("Distance between " + str(RFIDTAG(last_read_tagid).name) + " and " + str(RFIDTAG(tagid).name) + ": " + str(
                                    distance) + "cm")
                                current_speed = distance / elapsed_time
                                print("Current speed: " + str(current_speed) + " cm/s")
                                # payload = '"' + str(RFIDTAG(self.__rfid_tag).name) + '"'
                                payload = '{"tagid": "' + str(RFIDTAG(tagid).name) + '", "speed": ' + str(
                                    current_speed) + ', "tstamp": '+str(time.time())+'}'
                                print(payload)
                                # endpoint = '/features/position/properties/tagid'
                                endpoint = '/features/position/properties'
                                # print(endpoint)
                                print('Update ' + thingId + ' @' + endpoint)
                                digitaltwin_update(thingId, endpoint, payload)
                        except Exception as e:
                            print("DT connection error {}".format(e))

                        last_read_tagid = tagid

                    else:
                        print("INVALID TAG: " + tagid)
            except KeyboardInterrupt:
                print("E6{}".format(e))
                exit()
            except Exception as e:
                print("E7{}".format(e))
                if "Errno 5" in str(e):
                    print("revise if more than one rfid tags are present at that point.")
                try:
                    self.__q.put("ERROR")
                except Exception as e:
                    print("E5b{}".format(e))
                break
            time.sleep(0.15)

            '''
        #self.__q.put(RFID_SENSOR.AVAILABLE)



        #GPIO.cleanup()

        try:
            MIFAREReader = MFRC522.MFRC522()
            print("RFID is available in the car.")
            self.__q.put(RFID_SENSOR.AVAILABLE)
        except Exception as e:
            print("RFID is not available in the car.")
            self.__q.put(RFID_SENSOR.NOT_AVAILABLE)
            return


        try:
            while True:
                try:
                    print('Reading RFID...')
                    # Scan for cards
                    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                    #print(status)
                    # Get the UID of the card
                    (status, uid) = MIFAREReader.MFRC522_Anticoll()

                    #print(uid)
                    #print(status)
                    # If we have the UID, continue
                    if status == MIFAREReader.MI_OK:
                    #if len(uid) >= 4:
                        # Print UID
                        UID = str(uid[0]) + " " + str(uid[1]) + " " + str(uid[2]) + " " + str(uid[3])
                        print("UID:", UID)

                        tagid = UID
                        if is_valid_tag(tagid):  # Ver si existe en la lista de tags if l in ....
                            #print("Valid tagid: " + tagid)
                            try:
                                self.__q.put(tagid)
                            except Exception as e:
                                print(e)

                    time.sleep(0.1)
                except Exception as e:
                    print(e)
                    time.sleep(0.1)

        except KeyboardInterrupt:
            GPIO.cleanup()
        '''

    def __parse_rfid(self):
        print('Start parsing rfid data')
        while True:
            if self.__rfid_sensor:
                try:
                    # print('__parse_rfid')
                    tmp_rfid_tag = self.__rfid_tag
                    self.__rfid_tag = self.__q.get_nowait()
                    # self.__rfid_tag = self.__q.get()
                    # self.set_coordinates(self.__rfid_tag)

                    # if self.__rfid_tag == RFIDTAG.NW:
                    #    if not self.__stopped:
                    #        self.__stopped = True
                    if self.__rfid_tag == 'ERROR':
                        print("RFID ERROR: " + str(self.__rfid_tag))
                        if not self.__stopped:
                            self.__stopped = True
                    if self.__rfid_tag != tmp_rfid_tag:
                        self.__rfid_tag_previous = tmp_rfid_tag
                        print("Previous RFID tag: " + str(self.__rfid_tag_previous))
                        print("Current RFID tag: " + str(self.__rfid_tag))
                        '''
                        if self.digitaltwin_is_enabled():
                            print('Update DT...')

                            thingId = self.get_digitaltwin_id()  # 'edu.upc.craax:trafficlights'
                            print(thingId)
                            payload = '"' + str(RFIDTAG(self.__rfid_tag).name) + '"'
                            print(payload)
                            endpoint = '/features/position/properties/tagid'
                            # print(endpoint)
                            print('Update ' + thingId + ' @' + endpoint)
                            digitaltwin_update(thingId, endpoint, payload)
                        '''



                except Exception as e:
                    pass  # print(e)

                time.sleep(0.15)

    def parse_rfid(self):
        self.__parse_rfid()

    def run_default_driving(self):
        print('Starting the autonomous testing car...')
        time.sleep(2)
        for n in range(3, 0, -1):
            print(n)
            time.sleep(1)
        print('Go!')

        try:
            #self.start()
            self.stop()
            while True:

                # Driving
                try:
                    # self.run_default_driving_random()
                    self.run_default_driving_outside()
                    #self.run_default_driving_outside_test()
                except Exception as e:
                    print("E_DrivingDefault{}".format(e))

                # Trafficlights

                try:
                    self.run_default_driving_trafficlights()
                except Exception as e:
                    print("E_DrivingTrafficLights{}".format(e))


                time.sleep(0.1)
        except Exception as e:
            print("E2{}".format(e))

    def run_default_driving_trafficlights(self):
        if (self.get_previous_tag_id() == RFIDTAG.W1 and self.get_tag_id() == RFIDTAG.W2) or (
                self.get_previous_tag_id() == RFIDTAG.NW and self.get_tag_id() == RFIDTAG.W1):
            try:
                color = self.get_trafficlight_color(None)
                if self.get_tag_id() == RFIDTAG.W1 or self.get_tag_id() == RFIDTAG.W2:
                    if not self.is_stopped():
                        if is_red(color) or is_yellow(color):
                            self.stop()
                            print('Stop due to trafficlight color')
                    else:
                        if is_green(color):
                            self.start()
                            print('Start due to trafficlight color')
            except Exception as e:
                print("Exception requesting trafficlight color: {}".format(e))

        elif (self.get_previous_tag_id() == RFIDTAG.W4 and self.get_tag_id() == RFIDTAG.W3) or (
                self.get_previous_tag_id() == RFIDTAG.SW and self.get_tag_id() == RFIDTAG.W4):
            try:
                color = self.get_trafficlight_color(None)
                if self.get_tag_id() == RFIDTAG.W4 or self.get_tag_id() == RFIDTAG.W3:
                    if not self.is_stopped():
                        if is_red(color) or is_yellow(color):
                            self.stop()
                            print('Stop due to trafficlight color')
                    else:
                        if is_green(color):
                            self.start()
                            print('Start due to trafficlight color')
            except Exception as e:
                print("Exception requesting trafficlight color: {}".format(e))
        elif self.get_previous_tag_id() == RFIDTAG.C3 and self.get_tag_id() == RFIDTAG.C4:
            try:
                color = self.get_trafficlight_color(None)
                if self.get_tag_id() == RFIDTAG.C4:
                    if not self.is_stopped():
                        if is_red(color) or is_yellow(color):
                            self.stop()
                            print('Stop due to trafficlight color')
                    else:
                        if is_green(color):
                            self.start()
                            print('Start due to trafficlight color')
            except Exception as e:
                print("Exception requesting trafficlight color: {}".format(e))
        elif self.get_previous_tag_id() == RFIDTAG.S6 and self.get_tag_id() == RFIDTAG.S5:
            try:
                color = self.get_trafficlight_color(None)
                if self.get_tag_id() == RFIDTAG.S5 or self.get_tag_id() == RFIDTAG.S4:
                    if not self.is_stopped():
                        if is_red(color) or is_yellow(color):
                            self.stop()
                            print('Stop due to trafficlight color')
                    else:
                        if is_green(color):
                            self.start()
                            print('Start due to trafficlight color')
            except Exception as e:
                print("Exception requesting trafficlight color: {}".format(e))

    def reset_tagids(self):
        self.__rfid_tag = RFIDTAG.NOTAG
        self.__rfid_tag_previous = RFIDTAG.NOTAG
        print("Clean tagids")

    def reset_tagid(self):
        self.__rfid_tag_previous = self.__rfid_tag
        self.__rfid_tag = RFIDTAG.NOTAG
        print("Clean tagid")

    def set_tagid(self, tagid):
        self.__rfid_tag = tagid
        print("Tag id has been set to: " + str(self.__rfid_tag))

    def get_tagid(self):
        self.__rfid_tag

    def run_default_driving_outside(self):
        cont = 0
        try:
            '''
            if not self.is_stopped():
                if self.get_previous_tag_id() == RFIDTAG.W2 and self.get_tag_id() == RFIDTAG.W1:
                    if not self.is_turning_right() :
                        self.turn_right()
                elif not self.is_going_straight_on():
                    self.go_straight_on()
            '''
            if self.get_tag_id() == RFIDTAG.S1 or self.get_tag_id() == RFIDTAG.W1 or self.get_tag_id() == RFIDTAG.N7 or self.get_tag_id() == RFIDTAG.E4:  # velocidad normal al entrar en la curva
                if self.__speed != 330 and self.__speed>0:
                    self.__speed_prev = self.__speed
                    self.set_speed(330)
                    print('Speed reduced to enter the curve:' + str(self.__speed))
            elif self.get_tag_id() == RFIDTAG.SW or self.get_tag_id() == RFIDTAG.N1 or self.get_tag_id() == RFIDTAG.E1 or self.get_tag_id() == RFIDTAG.S7:  # restaurar velocidad calculada al salir de la curva:
                if self.__speed_prev != self.__speed and self.__speed_prev>0 and self.__speed>0:
                    self.set_speed(self.__speed_prev)
                    self.__speed_prev = self.__speed
                    print('Speed set to the one before the curve:' + str(self.__speed))
            elif not self.is_going_straight_on() and not self.is_stopped():
                self.go_straight_on()

            if self.get_tag_id() == RFIDTAG.ABOCADOR:
                if not self.is_stopped():
                    self.stop()
                    print("Start/Stop key")
            elif self.get_tag_id() != 'None' and self.get_tag_id() is not None and self.get_tag_id() != RFIDTAG.NOTAG:
                #print("Let's go!" + str(self.get_tag_id()))
                if not self.is_started():
                    self.start()
            
            '''if self.get_tag_id() == RFIDTAG.W1 or self.get_tag_id() == RFIDTAG.N7 or self.get_tag_id() == RFIDTAG.E4:  # velocidad normal al entrar en la curva
                if self.__speed != 330 and self.__speed>0:
                    self.__speed_prev = self.__speed
                    self.set_speed(330)
                    print('Speed reduced to enter the curve:' + str(self.__speed))
            elif self.get_tag_id() == RFIDTAG.SW or self.get_tag_id() == RFIDTAG.N1 or self.get_tag_id() == RFIDTAG.E1 or self.get_tag_id() == RFIDTAG.S7:  # restaurar velocidad calculada al salir de la curva:
                if self.__speed_prev != self.__speed and self.__speed_prev>0 and self.__speed>0:
                    self.set_speed(self.__speed_prev)
                    self.__speed_prev = self.__speed
                    print('Speed set to the one before the curve:' + str(self.__speed))
            elif not self.is_going_straight_on() and not self.is_stopped():
                self.go_straight_on()

            if self.get_tag_id() == RFIDTAG.ABOCADOR:
                if not self.is_stopped():
                    self.stop()
                    print("Start/Stop key")
            if self.get_tag_id() == RFIDTAG.S1 and cont == 0:
                time.sleep(0.5)
                self.stop()
                time.sleep(10)
                self.start()
                cont = 1
            elif self.get_tag_id() != 'None' and self.get_tag_id() is not None and self.get_tag_id() != RFIDTAG.NOTAG and self.get_tag_id() != RFIDTAG.N5 and self.get_tag_id() != RFIDTAG.N3:
                #print("Let's go!" + str(self.get_tag_id()))
                if not self.is_started():
                    self.start()'''

        except Exception as e:
            print("E1{}".format(e))


    def run_default_driving_outside_test(self):
        try:
            if self.get_tag_id() == RFIDTAG.S1 or self.get_tag_id() == RFIDTAG.W1 or self.get_tag_id() == RFIDTAG.N7 or self.get_tag_id() == RFIDTAG.E4:  # velocidad normal al entrar en la curva
                if self.__speed != 330 and self.__speed > 0:
                    self.__speed_prev = self.__speed
                    self.set_speed(330)
                    print('Speed reduced to enter the curve:' + str(self.__speed))
            elif self.get_tag_id() == RFIDTAG.SW or self.get_tag_id() == RFIDTAG.N1 or self.get_tag_id() == RFIDTAG.E1:  # restaurar velocidad calculada al salir de la curva:
                if self.__speed_prev != self.__speed and self.__speed_prev > 0 and self.__speed > 0:
                    self.set_speed(self.__speed_prev)
                    self.__speed_prev = self.__speed
                    print('Speed set to the one before the curve:' + str(self.__speed))


            if self.get_tag_id() == RFIDTAG.ABOCADOR:
                print("Start/Stop key")
                if not self.is_stopped():
                    self.stop()

            elif self.get_tag_id() == RFIDTAG.X4 or self.get_tag_id() == RFIDTAG.X5:
                if not self.is_stopped():
                    self.stop()

            #elif self.get_tag_id() == RFIDTAG.W2: # or self.get_tag_id() == RFIDTAG.X5:
            #    print("Testing stop")
            #    if not self.is_stopped():
            #        self.stop()
            #    if self.__speed_factor != 1.0:
            #        self.set_speed_factor(1.0)
            #elif self.get_tag_id() == RFIDTAG.X4:
            #    if self.__speed_factor != 1.0:
            #        if not self.is_stopped():
            #            self.set_speed_factor(1.0)
            #elif self.get_tag_id() != 'None' and self.get_tag_id() is not None and self.get_tag_id()!=RFIDTAG.NOTAG and self.get_tag_id()!=RFIDTAG.W3  and self.get_tag_id()!=RFIDTAG.W4  and self.get_tag_id()!=RFIDTAG.X5:

            #elif self.get_tag_id() != 'None' and self.get_tag_id() is not None and self.get_tag_id() != RFIDTAG.NOTAG:
                #print("Let's go!" + str(self.get_tag_id()))
                #if not self.is_started():
                    #self.start()



        except Exception as e:
            print("E1{}".format(e))

    def run_default_driving_random(self):
        try:
            if self.get_tag_id() == RFIDTAG.ABOCADOR:
                print("Start/Stop key")
                if not self.is_stopped():
                    self.stop()
            if not self.get_tag_id() == RFIDTAG.ABOCADOR and self.get_previous_tag_id() == RFIDTAG.ABOCADOR:
                print("Start after being stopped by Start/Stop key")
                if self.is_stopped():
                    self.start()
            elif (
                    not self.get_tag_id() == RFIDTAG.B1 and not self.get_tag_id() == RFIDTAG.B2 and not self.get_tag_id() == RFIDTAG.B6 and not self.get_tag_id() == RFIDTAG.B7) and (
                    self.get_previous_tag_id() == RFIDTAG.B1 or self.get_previous_tag_id() == RFIDTAG.B2 or self.get_previous_tag_id() == RFIDTAG.B6 or self.get_previous_tag_id() == RFIDTAG.B7):
                if self.is_stopped():
                    self.start()
            elif self.get_tag_id() == RFIDTAG.B1 or self.get_tag_id() == RFIDTAG.B2 or self.get_tag_id() == RFIDTAG.B6 or self.get_tag_id() == RFIDTAG.B7:
                self.stop()
                print('Bridge access is restricted!')
                print('Please, move the car to another street')
            elif self.get_previous_tag_id() == RFIDTAG.S2 and self.get_tag_id() == RFIDTAG.S3:
                if not self.is_turning_left() and not self.is_going_straight_on():
                    if random() < 0.5:
                        self.turn_left()
                    else:
                        self.go_straight_on()
            elif self.get_previous_tag_id() == RFIDTAG.N6 and self.get_tag_id() == RFIDTAG.N5:
                if not self.is_turning_left() and not self.is_going_straight_on():
                    if random() < 0.5:
                        self.turn_left()
                    else:
                        self.go_straight_on()
            elif self.get_previous_tag_id() == RFIDTAG.S6 and self.get_tag_id() == RFIDTAG.S5:
                if not self.is_turning_right() and not self.is_going_straight_on():
                    if random() < 0.5:
                        self.turn_right()
                    else:
                        self.go_straight_on()
            elif self.get_previous_tag_id() == RFIDTAG.N2 and self.get_tag_id() == RFIDTAG.N3:
                if not self.is_turning_right() and not self.is_going_straight_on():
                    if random() < 0.5:
                        self.turn_right()
                    else:
                        self.go_straight_on()
            elif self.get_previous_tag_id() == RFIDTAG.E4 and self.get_tag_id() == RFIDTAG.E3:
                if not self.is_going_straight_on():
                    self.go_straight_on()
            elif self.get_previous_tag_id() == RFIDTAG.E1 and self.get_tag_id() == RFIDTAG.E2:
                if not self.is_going_straight_on():
                    self.go_straight_on()
            elif self.get_previous_tag_id() == RFIDTAG.W1 and self.get_tag_id() == RFIDTAG.W2:
                if not self.is_going_straight_on():
                    self.go_straight_on()
            elif self.get_previous_tag_id() == RFIDTAG.W4 and self.get_tag_id() == RFIDTAG.W3:
                if not self.is_going_straight_on():
                    self.go_straight_on()
            elif self.get_previous_tag_id() == RFIDTAG.W2 and self.get_tag_id() == RFIDTAG.W1:
                if not self.is_turning_right():
                    self.turn_right()
            elif self.get_previous_tag_id() == RFIDTAG.C2 and self.get_tag_id() == RFIDTAG.C1:
                if not self.is_turning_right() and not self.is_turning_left():
                    if random() < 0.5:
                        self.turn_right()
                    else:
                        self.turn_left()
            elif self.get_previous_tag_id() == RFIDTAG.C3 and self.get_tag_id() == RFIDTAG.C4:
                if not self.is_turning_right() and not self.is_turning_left():
                    if random() < 0.5:
                        self.turn_right()
                    else:
                        self.turn_left()
        except Exception as e:
            print("E1{}".format(e))

    def run_default(self):
        # self.MIFAREReader = MFRC522.MFRC522()
        ctx = mp.get_context('fork')
        self.__q = ctx.Queue()
        p = ctx.Process(target=self.__read_rfid, args=())
        p.start()
        # Esperamos a leer si está o no equipado con sensores RFID
        status = self.__q.get()
        print(status)
        if RFID_SENSOR.AVAILABLE == status:
            self.__rfid_sensor = True
        else:
            p.close()

        # p.join()
        if current_process().name == 'MainProcess':
            self.set_ready(True)
            start_new_thread(self.__parse_rfid, ())
            # Nuevo thread que vaya controlando las acciones por defecto de la ruta, girar, seguir, etc o bien ponerlo en el followline...
            start_new_thread(self.run_default_driving, ())
            self.follow_line()
            # start_new_thread(self.follow_line, ())

    def api_processing_default(self, action, args):
        try:
            if action == 'stop':
                self.stop()
                return 'Stopped'
            elif action == 'start':
                self.start()
                return 'Started'
            elif action == 'left':
                self.left()
                return 'Left'
            elif action == 'right':
                self.right()
                return 'Right'
            elif action == 'turn_left':
                self.turn_left(args[0])
                return 'Turn left'
            elif action == 'turn_right':
                self.turn_right(args[0])
                return 'Turn right'
            elif action == 'go_straight_on':
                self.go_straight_on(args[0])
                return 'Go straight on'
            elif action == 'accelerate':
                self.accelerate()
                return 'Accelerate'
            elif action == 'decelerate':
                self.decelerate()
                return 'Decelerate'
            elif action == 'set_speed_factor':
                f=float(args[0])
                self.set_speed_factor(f)
                return str(self.__speed)
            elif action == 'set_speed':
                speed=int(args[0])
                self.set_speed(speed)
                return str(self.__speed)
            elif action == 'reset_speed':
                speed=int(args[0])
                self.set_speed(speed)
                self.__speed_prev=speed
                self.set_speed_factor(1.0)
                return str(self.__speed)

        except Exception as e:
            print(e)

        return None

    def stop(self):
        pass

    def stop_wait_continue(self, seconds=0.0):
        print('Stop & Wait & Continue')
        self.stop()
        if seconds > 0:
            time.sleep(seconds)
        self.start()

    def start(self):
        pass

    def follow_line(self):
        pass

    def left(self):
        pass

    def right(self):
        pass

    def turn_left(self):
        self.stop_turning_right()
        self.stop_go_straight_on()
        self.__turn_left = True
        print("set turn_left")

    def turn_right(self):
        self.stop_turning_left()
        self.stop_go_straight_on()
        self.__turn_right = True
        print("set turn_right")

    def go_straight_on(self, seconds=2):
        self.stop_turning_right()
        self.stop_turning_left()
        self.__straight_on = True
        print("set go_straight_on")

    def is_stopped(self):
        return self.__stopped

    def is_started(self):
        return not self.__stopped

    def is_turning_left(self):
        return self.__turn_left

    def is_turning_right(self):
        return self.__turn_right

    def stop_turning_right(self):
        self.__turn_right = False

    def stop_turning_left(self):
        self.__turn_left = False

    def stop_go_straight_on(self):
        self.__straight_on = False

    def is_going_straight_on(self):
        return self.__straight_on

    def rfid_sensor(self):
        if RFID_SENSOR.AVAILABLE == self.__rfid_sensor:
            return True
        return False

    def get_tag_id(self):
        return str(self.__rfid_tag)

    def get_previous_tag_id(self):
        return str(self.__rfid_tag_previous)

    def get_tag(self):  # get_tag_id alias
        return self.get_tag_id()

    def get_previous_tag(self):  # get_tag_id alias
        return self.get_previous_tag_id()

    def set_stopped(self, b):
        self.__stopped = b

    def get_trafficlight_color(self, trafficlight):
        if trafficlight is not None and len(trafficlight) > 0:
            return self.api_send(SMARTCITY.SCC, 'get_trafficlight_color:' + trafficlight)
        else:
            return self.api_send(SMARTCITY.SCC, 'get_trafficlight_color_from_tag:' + self.get_tag_id())

    def get_trafficlight_color_from_tag(self, tagid=None):
        if tagid is None:
            tagid = self.get_tag_id()
        return self.api_send(SMARTCITY.SCC, 'get_trafficlight_color_from_tag:' + tagid)

    def accelerate(self):
        if self.__speed_factor < 1.5:
            self.__speed_factor = self.__speed_factor + 0.1

    def decelerate(self):
        if self.__speed_factor > 0.6:
            self.__speed_factor = self.__speed_factor - 0.1

    def get_speed_factor(self):
        return self.__speed_factor

    def get_speed(self):
        return self.__speed

    def set_speed(self, speed):
        self.__speed = speed
        print('Speed set to: ' + str(self.__speed))

    '''
    def set_speed_factor(self, f):
        self.__speed_factor = f
        print('Speed factor set to: ' + str(self.__speed_factor))
        speed = int(self.__speed * self.__speed_factor)
        self.set_speed(speed)
    '''

    def set_speed_factor(self, f):
        self.__speed_factor = f
        print('Speed factor set to: ' + str(self.__speed_factor))
        speed = int(self.__speed * self.__speed_factor)
        if speed < 300:
            speed = 300
        elif speed > 1300:
            speed = 1300
        self.set_speed(speed)
