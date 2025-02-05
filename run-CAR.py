import sys
sys.path.append('controller')
sys.path.append('testbed')

import comminterface
from car_FreeNove import CarPhy

if __name__ == '__main__':
    ip = '172.16.0.9'
    # ip=None
    car = CarPhy('autocloud-1', ip, 12333, 'AutoCloud1', comminterface.arg_dns_ip(sys.argv), comminterface.arg_dns_port(sys.argv))

