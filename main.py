import os
import sys
import psutil
import socket
from ping3 import ping
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
            ret = receiver.wait_for_discovered()
            if ret is False:
                # None return from socket.sendall() means success:
                # https://docs.python.org/3/library/socket.html#socket.socket.sendall
                settings.set_controller_ip("")
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
    valid_host = False
    print_err = True
    while valid_host is False:
        try:
            ip = settings.get_controller_ip()
            if len(ip) == 0:
                continue
            ret = ping(ip, timeout=2)
            if ret:
                valid_host = True
        except Exception as e:
            if print_err is True and len(ip) > 0:
                print(f'Controller IP is {ip}, but valid: {e}')
                print_err = False
            sleep(1)

def read_sensor(settings: Settings = None):
    pid_light = os.fork()
    while True:
        try:
            if pid_light:
                wait_for_controller(settings)
                # Parent. Not light.
                sender = Sender(settings)
                sensors = Sensors(name=settings.get_name())
                last_CardUID = ""
                upload_ready = True
                while True:
                    if len(settings.get_controller_ip()) == 0:
                        break
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
                        ret = sender.send_sensor_data((key, value))
                        if ret == False:
                            break
                        sleep(0.5)
            else:
                wait_for_controller(settings)
                # Child process.
                sender = Sender(settings)
                adc = Adc()
                last_light = -1
                while True:
                    if len(settings.get_controller_ip()) == 0:
                        break
                    left  = adc.readRawADS7830(0)
                    right = adc.readRawADS7830(1)
                    light = int((left + right) / 2)
                    if light != last_light:
                        last_light = light
                        ret = sender.send_sensor_data(('photoresistor', light))
                        if ret == False:
                            break
                    sleep(1)
        except Exception as e:
            print(f"Error sending data to the controller: {e}")

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
        close_port(5007)
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

        if settings.get_im_edge():
            proc_sensor = Process(target=read_sensor, args=(settings, ))
            proc_sensor.start()
            proc_sensor.join()

        proc_car.join()
        proc_discovery.join()
    sys.exit(0)
