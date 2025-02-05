import sys
sys.path.append('controller')
sys.path.append('testbed')

import comminterface
from car_FreeNove import CarPhy
from ies_car_test import IESCar

if __name__ == '__main__':
    ip       = '172.16.0.9'
    dns_ip   = '172.16.0.2'
    dns_port = 13300
    # ip=None
    car = IESCar('autocloud-1', ip, 12333, 'AutoCloud1', dns_ip, dns_port)

