"""Smart City Layout

This script declares general variables and implements Enum classes
providing a logical description and naming of the smart city.

This file must import sc_layout_default and can override anyone of
its classes and variables aimed at designing a particular testbed
scenario/configuration.

This file must be imported in testbed.py
"""

__author__ = "A. Asensio, S. Sanchez"
__credits__ = ["Adrian Asensio", "Sergi Sanchez"]
__version__ = "1.0.1"
__status__ = "Development"

from sc_layout_default import *

routing_table = {}

#dns_ip_default = '192.168.1.36'
dns_ip_default = '172.16.0.2'
digitaltwin_server = '172.16.0.103:8080'

distance_between_tags_id = [
    RFIDTAG.X2,
    RFIDTAG.S7,
    RFIDTAG.S6,
    RFIDTAG.S5,
    RFIDTAG.X1,
    RFIDTAG.X3,
    RFIDTAG.S3,
    RFIDTAG.S2,
    RFIDTAG.S1,
    RFIDTAG.SW,
    RFIDTAG.W4,
    RFIDTAG.W3,
    RFIDTAG.X4,
    RFIDTAG.X5]
distance_between_tags_cm = [
    0.0,
    48.0,
    70.0,
    60.0,
    63.0,
    35.0,
    54.0,
    61.0,
    61.0,
    48.0,
    57.0,
    17.0,
    23.0,
    46.0
]

distance_between_tags_cm_relative = [0.0 for n in range(len(distance_between_tags_cm))]

for i in range(len(distance_between_tags_cm)):
    if i<1:
        pass
    distance_between_tags_cm_relative[i] = distance_between_tags_cm_relative[i-1] + distance_between_tags_cm[i]
