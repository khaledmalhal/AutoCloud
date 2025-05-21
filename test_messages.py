import os
from time import sleep
import datetime
import psutil

from controller.discovery import Discovery
from controller.receiver import Receiver

def close_port(port):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            print(f"Closing port {port} by terminating PID {conn.pid}")
            process = psutil.Process(conn.pid)
            process.terminate()

if __name__ == '__main__':
    try:
        close_port(5005)
        close_port(5006)
        sleep(1)
    except:
        print("No processes needed to be closed")
    try:
        pid_receive = os.fork()
        if pid_receive: # Parent. This process sends messages
            discovery = Discovery(name='laptop')
            while True:
                discovery.discover_edge_devices()
                sleep(2)
        else:
            receiver = Receiver(name='autocloud1')
            while True:
                data, addr = receiver.wait_for_discovered()
                if data['type'] == receiver.msg.DISCOVERY:
                    controller = data['controller']
                    print(f'[EdgeDevice] ->\tIP: {addr[0]}\tDiscovery type. Controller: {controller}')
                    receiver.reply_controller(addr[0])
    except Exception as e:
        print(f"Error: {e}")