import sys

import comminterface
from car_FreeNove import CarPhy

if __name__ == '__main__':
    ip = '10.0.1.109'
   # ip=None
    car = CarPhy('car-1', ip, 12333, 'Cotxe1', comminterface.arg_dns_ip(sys.argv), comminterface.arg_dns_port(sys.argv))

