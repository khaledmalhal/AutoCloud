"""Testbed

This script declares general functions and implements Enum classes providing
a set of helpful functionalities to facilitate development in the testbed
at a high level and runs graceful_exit() to handle SIGINT and exit gracefully
the testbed scripts.

This file must be imported as a module and contains the following
Enum classes and functions:

Enum classes
------------
    * MESSAGE
        Naming for common messages such as ACK and others.
    * RFID_SENSOR
        Naming to indicate if RFID sensor is available or not
    * TRAFFLIGHTCOLOR
        Naming for trafficlight colors

Functions
---------
    * compare_color(color, trafficlightcolor)
        It returns True if color and trafficlightcolor are equal
    * is_green(color)
        It returns True if color is equal to TRAFFLIGHTCOLOR.GREEN
    * is_red(color)
        It returns True if color is equal to TRAFFLIGHTCOLOR.RED
    * is_yellow(color)
        It returns True if color is equal to TRAFFLIGHTCOLOR.YELLOW
    * is_valid_tag(tagid)
        It returns True if tagid is defined in the testbed; i.e., exists
        in RFIDTAG
    * get_trafficlight_from_tagid(tagid)
        It returns the trafficlightlocated at tagid, if any; i.e., if defined
        at tagid2trafficlight
    * to_trafficlight_color(color)
        It returns TRAFFLIGHTCOLOR corresponding to color if color is a str;
        or TRAFFLIGHTCOLOR if color is already TRAFFLIGHTCOLOR
    * end()
        Not implemented
    * parse_name(name)
        If name starts with @, it looks for it in SMARTCITY
    * mhelp(module_name, join=False)
        Creates a new thread which runs help(module_name). If join is True,
        then joins the thread and waits for it to finish.
    * arg_dns_ip(argv)
        Parses argv to get dns ip if provided
    * arg_dns_port(argv)
        Parses argv to get dns port if provided
    * dns_ip(argv)
        Returns dns ip from argv
    * dns_port(argv)
        Returns dns port from argv
    * default_port()
        Returns the default agent's port
    * signal_handler(signum, frame)
        Handles SIGNIT and SIGALRM
    * set_timeout(sec)
        Triggers SIGALRM after sec seconds
    * graceful_exit()
        Handles SIGINT to exit gracefully
"""

__author__ = "A. Asensio, S. Sanchez"
__credits__ = ["Adrian Asensio", "Sergi Sanchez"]
__version__ = "1.0.1"
__status__ = "Development"

import json
import threading
from _thread import start_new_thread

import psutil
import signal
import sys

import requests

from sc_layout import *


class MESSAGE(str, Enum):
    ACK = 'ack'
    NOACK = 'no_ack'
    SUBSCRIBED = 'subscribed'
    UNSUBSCRIBED = 'unsubscribed'
    ACTION_UNKNOWN = 'Undefined command/action'


class RFID_SENSOR(str, Enum):
    AVAILABLE = '1'
    NOT_AVAILABLE = '0'


class TRAFFLIGHTCOLOR(str, Enum):
    WAITING = 'waiting'
    GREEN = 'green'
    YELLOW = 'yellow'
    RED = 'red'
    EMERGENCY = 'emergency'
    ERROR = 'error'
    GREENYELLOWRED = 'gyr'
    NONE = ''


def compare_color(color, trafficlightcolor):
    """

    Parameters
    ----------
    color : str or TRAFFLIGHTCOLOR
    trafficlightcolor:  TRAFFLIGHTCOLOR

    Return
    ------
    bool:
    """
    try:
        if isinstance(color, str):
            if TRAFFLIGHTCOLOR[color.upper()] == trafficlightcolor:
                return True
            else:
                return False
        if isinstance(color, TRAFFLIGHTCOLOR):
            if color == trafficlightcolor:
                return True
            else:
                return False
    except:
        return False
    return False


def is_green(color):
    """
    Parameters
    ----------
    color : str or TRAFFLIGHTCOLOR
    """
    return compare_color(color, TRAFFLIGHTCOLOR.GREEN)


def is_red(color):
    """
    Parameters
    ----------
    color : str or TRAFFLIGHTCOLOR
    """
    return compare_color(color, TRAFFLIGHTCOLOR.RED)


def is_yellow(color):
    """
    Parameters
    ----------
    color : str or TRAFFLIGHTCOLOR
    """
    return compare_color(color, TRAFFLIGHTCOLOR.YELLOW)


def is_valid_tag(tagid):
    """
    Parameters
    ----------
    tagid : str
    """
    if tagid in RFIDTAG._value2member_map_:
        return True
    return False


def get_trafficlight_from_tagid(tagid):
    """
    Parameters
    ----------
    tagid : str

    Return
    ------
    TRAFFLIGHTPHY or None:
    """
    try:
        print("get_trafficlight_from_tagid(" + tagid + ")")
        return tagid2trafficlight[tagid]
    except:
        return None


def to_trafficlight(trafficlight):
    """
    Parameters
    ----------
    trafficlight : str or TRAFFLIGHTPHY

    Return
    ------
    TRAFFLIGHTPHY:
    """
    if isinstance(trafficlight, str):
        return TRAFFLIGHTPHY[trafficlight.upper()]
    elif isinstance(trafficlight, TRAFFLIGHTPHY):
        return trafficlight
    else:
        return None


def to_trafficlight_color(color):
    """
    Parameters
    ----------
    color : str or TRAFFLIGHTCOLOR

    Return
    ------
    TRAFFLIGHTCOLOR:
    """
    try:
        if isinstance(color, str):
            return TRAFFLIGHTCOLOR[color.upper()]
        else:
            return color
    except:
        return TRAFFLIGHTCOLOR.NONE


def end():
    pass


def parse_name(name: str):
    if name.startswith('@'):
        name = name.replace('@', '').upper()
        name = SMARTCITY[name]
    return name


def mhelp(module_name: str, join: bool = False):
    '''
    method_attribute = ''
    if "." in module_name:
        x=module_name.split('.')
        module_name = x[0]
        i =0
        for s in x:
            if i==0:
                continue
            i +=1
            method_attribute += '.'+s

    query = module_name+method_attribute
    '''

    if join:
        try:
            # module = __import__(str(module_name))
            # t = threading.Thread(target=help, args=(module,))
            t = threading.Thread(target=help, args=(module_name,))
            t.start()
            # sys.modules.pop(module_name)
            t.join()
        except Exception as e:
            print("ERROR:{}".format(e))
    else:
        try:
            # module = __import__(str(module_name))
            # start_new_thread(help, (module,))
            start_new_thread(help, (module_name,))
            sys.modules.pop(module_name)
        except Exception as e:
            print("ERROR:{}".format(e))


def arg_dns_ip(argv: list):
    if len(argv) >= 2:
        return argv[1]


def arg_dns_port(argv: list):
    if len(argv) >= 3:
        return int(argv[2])
    else:
        return dns_port_default


def dns_ip(argv: list):
    if len(argv) >= 2:
        return arg_dns_ip(argv)
    else:
        return dns_ip_default


def dns_port(argv: list):
    return arg_dns_port(argv)


def default_port():
    return port_default


def default_digitaltwin_server():
    return digitaltwin_server


def digitaltwin_create(payload, thingId='', digitaltwin_ip_port=digitaltwin_server):
    print('Creating DT...')
    headers = {'Content-Type': 'application/json'}
    url = 'http://' + digitaltwin_ip_port + '/api/2/things/' + thingId
    print('Trying to create the digital twin...')
    try:
        if thingId == '':
            cur = requests.post(url, data=payload, headers=headers, auth=('ditto', 'ditto'))
            response = json.loads(cur.text)
            dt_id = response['thingId']
        else:
            cur = requests.put(url, data=payload, headers=headers, auth=('ditto', 'ditto'))
            dt_id = thingId
        print(cur)
        print(dt_id + ": " + str(cur.text))
    except Exception as e:
        print("ERROR:{}".format(e))

    return dt_id


def digitaltwin_update(thingId, endpoint, payload, digitaltwin_ip_port=digitaltwin_server):
    # headers = {'Content-Type': 'application/octet-stream'}
    headers = {'Content-Type': 'application/json'}
    cur = requests.put(
        'http://' + digitaltwin_ip_port + '/api/2/things/' + thingId + endpoint, auth=('ditto', 'ditto'), data=payload,
        headers=headers)
    print(str(cur))


def digitaltwin_get(thingId, endpoint, digitaltwin_ip_port=digitaltwin_server):
    # headers = {'Content-Type': 'application/octet-stream'}
    headers = {'Content-Type': 'application/json'}
    cur = requests.get(
        'http://' + digitaltwin_ip_port + '/api/2/things/' + thingId + endpoint, auth=('ditto', 'ditto'),
        headers=headers)
    return cur.text


def get_distance_between_tags(tagid_s, tagid_t):
    try:
        idx_s = distance_between_tags_id.index(tagid_s)
        idx_t = distance_between_tags_id.index(tagid_t)
        distance = distance_between_tags_cm_relative[idx_t] - distance_between_tags_cm_relative[idx_s]
    except Exception as e:
        print("ERROR: get_distance_between_tags")
        print(e)
        distance = 0
    return abs(distance)


def compute_expected_time_distance_to_target(source, target=RFIDTAG.X4.name):
    if target != RFIDTAG.X4.name:
        print("Error compute_expected_time_to_target")
        sys.exit()

    avg_time_curves = 4.0
    try:
        distance_w = 0.0
        distance_n = 0.0
        distance_e = 0.0
        distance_s = 0.0

        if source.startswith('W') or source == RFIDTAG.SW.name:
            distance_w = get_distance_between_tags(RFIDTAG[source], RFIDTAG[target])  # recta W
            avg_time_curves = 0.0
        elif source.startswith('S') and source != RFIDTAG.SE.name and source != RFIDTAG.SW.name:
            distance_w = get_distance_between_tags(RFIDTAG.SW, RFIDTAG[target])  # recta W
            distance_s = get_distance_between_tags(RFIDTAG[source], RFIDTAG.S1)  # recta S
            avg_time_curves = avg_time_curves * 1.0
        elif source.startswith('E'):
            distance_w = get_distance_between_tags(RFIDTAG.SW, RFIDTAG[target])  # recta W
            distance_s = get_distance_between_tags(RFIDTAG.S7, RFIDTAG.S1)  # recta S
            distance_e = get_distance_between_tags(RFIDTAG[source], RFIDTAG.SE)  # recta E
            avg_time_curves = avg_time_curves * 2.0
        elif source.startswith('N') and source != RFIDTAG.NE.name and source != RFIDTAG.NW.name:
            distance_w = get_distance_between_tags(RFIDTAG.SW, RFIDTAG[target])  # recta W
            distance_s = get_distance_between_tags(RFIDTAG.X2, RFIDTAG.S1)  # recta S
            distance_e = get_distance_between_tags(RFIDTAG.E1, RFIDTAG.SE)  # recta E
            distance_n = get_distance_between_tags(RFIDTAG[source], RFIDTAG.N7)  # recta N
            avg_time_curves = avg_time_curves * 3.0
        else:
            print("Error compute_expected_time_to_target")
            sys.exit()

        distance = distance_w + distance_n + distance_e + distance_s
        return avg_time_curves, distance

    except Exception as e:
        print(e)
        sys.exit()


def compute_expected_time_to_target(speed, source, target='X4'):
    avg_time_curves, distance = compute_expected_time_distance_to_target(source, target)
    print(str(avg_time_curves) + " - " + str(distance))
    time_to_target = (distance / speed) + avg_time_curves
    return time_to_target


def compute_expected_speed_factor_to_target(time_objective, speed, source, target='X4'):
    avg_time_curves, distance = compute_expected_time_distance_to_target(source, target)
    print(str(avg_time_curves) + "/" + str(distance) + "/" + str(time_objective))
    t = time_objective - avg_time_curves
    if t <= 0:
        return 1.0
    speed_factor = (distance / t) / speed
    return speed_factor


'''
def find_self_ip(ip=None):

    if ip != '' and ip is not None:
        return ip
    platform = distro.linux_distribution()
    #print(platform[0].lower())
    if 'ubuntu' in platform[0].lower():
        for i in socket.gethostbyname_ex(socket.gethostname() + ".local")[-1]:
            if i == '127.0.0.1' or i == '127.0.1.1':
                continue
            return i

    else:
        for i in socket.gethostbyname_ex(socket.gethostname())[-1]:
            if i == '127.0.0.1' or i == '127.0.1.1':
                continue
            return i
    return ''
'''


def print_bye_message():
    print("\n\nWe hope to see you soon")
    print("*** CRAAX Team ***\n")


def signal_handler(signum, frame):
    # raise Exception("Timed out!")
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    # while len(children) > 0:
    '''
    for child in children:
        print("childs {}".format(child))
        #child.send_signal(signal.SIGINT)
    '''
    #    children = current_process.children(recursive=True)

    print_bye_message()

    if (signum == signal.SIGINT):
        sys.exit(1)
    elif (signum == signal.SIGALRM):
        raise Exception("Time out!")


def set_timeout(sec: int):
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(sec)  # seconds
    print("Timeout set to " + str(sec) + " seconds")


def graceful_exit():
    signal.signal(signal.SIGINT, signal_handler)


try:
    graceful_exit()
except:
    pass
