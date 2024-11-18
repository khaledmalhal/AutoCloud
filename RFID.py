from enum import Enum

class RFIDTAG(str, Enum):
    ABOCADOR = '129 231 79 47'
    B1 = '243 223 166 137'
    B2 = '43 180 230 89'
    B3 = '206 93 226 41'
    B4 = '218 125 230 89'
    B5 = '95 173 230 89'
    B6 = '128 03 231 89'
    B7 = '250 68 255 41'
    C1 = '143 05 104 41'
    C2 = '158 224 83 32'
    C3 = '158 246 166 32'
    C4 = '143 101 015 41'
    E1 = '127 240 92 41'
    E2 = '143 121 02 41'
    E3 = '143 99 01 41'
    E4 = '143 133 87 41'
    EXTRA1 = '143 76 98 41'
    EXTRA2 = '143 78 107 41'
    N1 = '140 88 228 137'
    N2 = '158 220 186 89'
    N3 = '220 24 232 137'
    N4 = '119 44 171 169'
    N5 = '193 125 198 89'
    N6 = '014 137 254 41'
    N7 = '81 127 227 137'
    NE = '252 94 249 41'
    NW = '41 205 254 41'
    S1 = '186 134 166 13'
    S2 = '78 95 166 137'
    S3 = '255 014 167 137'
    S4 = '217 117 197 89'
    S5 = '137 40 167 137'
    S6 = '01 180 166 137'
    S7 = '50 74 227 41'
    SE = '227 134 166 137'
    SW = '47 34 231 89'
    UB = '57 156 167 137'
    W1 = '27 06 231 89'
    W2 = '01 84 254 41'
    W3 = '86 013 231 89'
    W4 = '187 205 166 13'
    NOTAG = 'NOTAG'
    X1='174 52 01 149'
    X2='227 134 166 13'
    X3='254 74 05 149'
    X4='222 75 02 149'
    X5='30 127 04 149'

tagNames = RFIDTAG.__members__.keys()
print(tagNames)
name = '30 127 04 149'
tagNames.remove(name)
print(RFIDTAG.name('30 127 04 149'))