import os
import psutil
from time import sleep
import multiprocessing
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager

# from testbed.comminterface import *
# from hardware.car_FreeNove import CarPhy
# from hardware.ies_car_test import IESCar
from controller.discovery import Discovery
from controller.receiver import Receiver
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
                print(f'[EdgeDevice] ->\tIP: {addr[0]}\tDiscovery type. Controller: {controller}')
                receiver.reply_controller(addr[0])
                settings.set_controller_ip(addr[0])
    else:
        # I am not the Edge. I am the Controller and I discover for Edge Devices.
        discovery = Discovery(settings)
        while True:
            discovery.discover_edge_devices()
            sleep(2)

class SettingsManager(BaseManager):
    pass
SettingsManager.register('Settings', Settings)

def main(settings: Settings = None):
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

        proc_car = Process(target=main, args=(settings, ))
        proc_car.start()

        proc_car.join()
        proc_discovery.join()
