"""DEFAULT Smart City Layout

This script declares general variables and implements Enum classes
providing a logical description and naming of the smart city.

This file must be imported as a module in sc_layout and can be overriden.
It contains the following Enum classes and variables:

Enum classes
------------
    * SMARTCITY
        Aliases for naming of common (fixed) agents in the testbed - smart city
    * TRAFFLIGHTPHY
        Mapping of physical trafficlights in the testbed to arduino id and port id
    * RFIDTAG
        Mapping between rfid tag naming and its uid code

Variables
---------
    * dns_ip_default : str
        Default IP where DNS runs
    * dns_port_default : int
        Default port where DNS runs
    * port_default : int
        Default port for comm. interfaces
    * tagid2trafficlight : dict
        Contains tuples of RFIDTAG (key) and TRAFFLIGHTPHY (value), aimed at
        mapping rfid tags and trafficlights; i.e., location of trafficlights
"""

__author__ = "A. Asensio, S. Sanchez"
__credits__ = ["Adrian Asensio", "Sergi Sanchez"]
__version__ = "1.0.1"
__status__ = "Development"

from enum import Enum


class SMARTCITY(str, Enum):
    SCC = 'scc'  # Smart city controller
    TLC = 'tl_cluster0'  # Trafficlight cluster
    EVM = 'events'  # Event manager
    DNS = 'dns'  # DNS
    HLP = 'helper'

class TRAFFLIGHTPHY(list, Enum):
    # NAME_A_B
    # NAME: tl -> trafficlight
    # A -> Arduino id
    # B -> Trafficlight id within the arduino

    TW1 = [0, 1]  # TW1 - TL1
    TW2 = [0, 2]  # TW2 - TL2
    TS1 = [1, 1]  # TS1 - TL3
    TS2 = [1, 2]  # TS2 - TL4

class RFIDTAG(str, Enum):
    ABOCADOR = '129 231 79 47'
    B1       = '243 223 166 137'
    B2       = '43 180 230 89'
    B3       = '206 93 226 41'
    B4       = '218 125 230 89'
    B5       = '95 173 230 89'
    B6       = '128 03 231 89'
    B7       = '250 68 255 41'
    C1       = '143 05 104 41'
    C2       = '158 224 83 32'
    C3       = '158 246 166 32'
    C4       = '143 101 015 41'
    E1       = '127 240 92 41'
    E2       = '143 121 02 41'
    E3       = '143 99 01 41'
    E4       = '143 133 87 41'
    EXTRA1   = '143 76 98 41'
    EXTRA2   = '143 78 107 41'
    N1       = '140 88 228 137'
    N2       = '158 220 186 89'
    N3       = '220 24 232 137'
    N4       = '119 44 171 169'
    N5       = '193 125 198 89'
    N6       = '014 137 254 41'
    N7       = '81 127 227 137'
    NE       = '252 94 249 41'
    NW       = '41 205 254 41'
    S1       = '186 134 166 13'
    S2       = '78 95 166 137'
    S3       = '255 014 167 137'
    S4       = '217 117 197 89'
    S5       = '137 40 167 137'
    S6       = '01 180 166 137'
    S7       = '50 74 227 41'
    SE       = '227 134 166 137'
    SW       = '47 34 231 89'
    UB       = '57 156 167 137'
    W1       = '27 06 231 89'
    W2       = '01 84 254 41'
    W3       = '86 013 231 89'
    W4       = '187 205 166 13'
    NOTAG    = 'NOTAG'
    X1       = '174 52 01 149'
    X2       = '227 134 166 13'
    X3       = '254 74 05 149'
    X4       = '222 75 02 149'
    X5       = '30 127 04 149'

dns_ip_default = None
dns_port_default = 13300
port_default = 13301

tagid2trafficlight = {}

tagid2trafficlight[RFIDTAG.W3] = TRAFFLIGHTPHY.TW2
tagid2trafficlight[RFIDTAG.W4] = TRAFFLIGHTPHY.TW2
tagid2trafficlight[RFIDTAG.W2] = TRAFFLIGHTPHY.TW1
tagid2trafficlight[RFIDTAG.W1] = TRAFFLIGHTPHY.TW1
tagid2trafficlight[RFIDTAG.S5] = TRAFFLIGHTPHY.TS2
tagid2trafficlight[RFIDTAG.C3] = TRAFFLIGHTPHY.TS1
tagid2trafficlight[RFIDTAG.C4] = TRAFFLIGHTPHY.TS1


routing_table = {}

routing_table[(RFIDTAG.W3, RFIDTAG.B1)] = {0:'turn_right'}
routing_table[(RFIDTAG.W2, RFIDTAG.B1)] = {0:'turn_left'}
routing_table[(RFIDTAG.W2, RFIDTAG.W3)] = {0:'go_straight_on'}
routing_table[(RFIDTAG.W3, RFIDTAG.W2)] = {0:'go_straight_on'}

routing_table[(RFIDTAG.B1, RFIDTAG.W2)] = {0:'turn_right'}
routing_table[(RFIDTAG.B1, RFIDTAG.W3)] = {0:'turn_left'}


routing_table[(RFIDTAG.S5, RFIDTAG.C4)] = {0:'turn_right'}
routing_table[(RFIDTAG.S3, RFIDTAG.C4)] = {0:'turn_left'}
routing_table[(RFIDTAG.S5, RFIDTAG.S3)] = {0:'go_straight_on'}
routing_table[(RFIDTAG.S3, RFIDTAG.S5)] = {0:'go_straight_on'}

routing_table[(RFIDTAG.C4, RFIDTAG.S3)] = {0:'turn_right'}
routing_table[(RFIDTAG.C4, RFIDTAG.S5)] = {0:'turn_left'}


routing_table[(RFIDTAG.N3, RFIDTAG.C1)] = {0:'turn_right'}
routing_table[(RFIDTAG.N5, RFIDTAG.C1)] = {0:'turn_left'}
routing_table[(RFIDTAG.N5, RFIDTAG.N3)] = {0:'go_straight_on'}
routing_table[(RFIDTAG.N3, RFIDTAG.N5)] = {0:'go_straight_on'}

routing_table[(RFIDTAG.C1, RFIDTAG.N5)] = {0:'turn_right'}
routing_table[(RFIDTAG.C1, RFIDTAG.N3)] = {0:'turn_left'}


routing_table[(RFIDTAG.E2, RFIDTAG.B7)] = {0:'turn_right'}
routing_table[(RFIDTAG.E3, RFIDTAG.B7)] = {0:'turn_left'}
routing_table[(RFIDTAG.E2, RFIDTAG.E3)] = {0:'go_straight_on'}
routing_table[(RFIDTAG.E3, RFIDTAG.E2)] = {0:'go_straight_on'}

routing_table[(RFIDTAG.B7, RFIDTAG.E3)] = {0:'turn_right'}
routing_table[(RFIDTAG.B7, RFIDTAG.E2)] = {0:'turn_left'}


routing_table[(RFIDTAG.W1, RFIDTAG.N1)] = {0:'turn_right'}
routing_table[(RFIDTAG.W1, RFIDTAG.NW)] = {0:'go_straight_on'}


routing_table[(RFIDTAG.NW, RFIDTAG.NW)] = {0:'stop'}
