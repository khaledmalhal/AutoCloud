import os
import sys
import psutil
import socket
from time import sleep
import multiprocessing
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager

# from testbed.comminterface import *
# from hardware.car_FreeNove import CarPhy
# from hardware.ies_car_test import IESCar

from hardware.sensors import Sensors
from hardware.ADC import Adc

from controller.discovery import Discovery
from controller.receiver import Receiver
from controller.sender import Sender
from controller.forward import Forward
from settings import Settings

def close_port(port):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            print(f"Closing port {port} by terminating PID {conn.pid}")
            process = psutil.Process(conn.pid)
            process.terminate()

def discover(settings: Settings = None):
    print("Discover")
    if settings.get_im_edge() is True: 
        # If I am Edge, then I listen from Controllers
        receiver = Receiver(settings)
        while True:
            data, addr = receiver.receive()
            if data['type'] == receiver.msg.DISCOVERY:
                controller = data['controller']
                # print(f'[EdgeDevice] ->\tIP: {addr[0]}\tDiscovery type. Controller: {controller}')
                try:
                    ret = receiver.reply_controller(addr[0])
                    if ret is None:
                        # None return from socket.sendall() means success:
                        # https://docs.python.org/3/library/socket.html#socket.socket.sendall
                        settings.set_controller_ip(addr[0])
                except Exception as e:
                    print(f'[EdgeDevice] -> Error replying to Controller for Discovery')
    else:
        # I am not the Edge. I am the Controller and I discover for Edge Devices.
        discovery = Discovery(settings)
        forward = Forward(settings)
        while True:
            discovery.discover_edge_devices()
            sleep(2)

def wait_for_controller(settings: Settings = None):
    """
    Call this function before we attempt to read the sensor data,
    so the Edge Device can have a Controller to send the data to.
    """
    valid_ip = False
    print_err = False
    while valid_ip is False:
        try:
            ip = settings.get_controller_ip()
            socket.inet_aton(ip)
            valid_ip = True
        except Exception as e:
            if print_err is False and len(ip) > 0:
                print(f'Controller IP is {ip}, but valid')
                print_err = True
            sleep(1)

def read_sensor(settings: Settings = None):
    wait_for_controller(settings)
    pid_light = os.fork()
    try:
        if pid_light:
            # Parent. Not light.
            sender = Sender(settings)
            sensors = Sensors(name=settings.get_name())
            last_CardUID = ""
            upload_ready = True
            while True:
                key, value = sensors.read_line()
                if key == "Card UID":
                    if value != last_CardUID:
                        last_CardUID = value
                        upload_ready = True
                    else:
                        upload_ready = False
                else:
                    upload_ready = True
                if upload_ready == True:
                    sender.send_sensor_data((key, value))
                    sleep(0.5)
        else:
            # Child process.
            sender = Sender(settings)
            adc = Adc()
            last_light = -1
            while True:
                left  = adc.readRawADS7830(0)
                right = adc.readRawADS7830(1)
                light = int((left + right) / 2)
                if light != last_light:
                    last_light = light
                    sender.send_sensor_data(('photoresistor', light))
                sleep(1)
    except Exception as e:
        print("Exception:{}".format(e))

class SettingsManager(BaseManager):
    pass
SettingsManager.register('Settings', Settings)

def run_car(settings: Settings = None):
    # car = IESCar(settings.name, None, 12333, settings.name, settings.dns_ip, settings.dns_port)
    # car.run()
    pass

if __name__ == '__main__':
    try:
        close_port(5005)
        close_port(5006)
        sleep(1)
    except:
        print("No processes needed to be closed")

    with SettingsManager() as manager:
        settings = manager.Settings()

        # If we need to share data between the processes, we need to create them here. Eg.:
        # shared_list = manager.list()

        proc_discovery = Process(target=discover, args=(settings, ))
        proc_discovery.start()

        proc_car = Process(target=run_car, args=(settings, ))
        proc_car.start()

        proc_sensor = Process(target=read_sensor, args=(settings, ))
        proc_sensor.start()

        proc_car.join()
        proc_discovery.join()
        proc_sensor.join()
    sys.exit(0)
