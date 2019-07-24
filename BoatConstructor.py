from Boats import *
from RLStrategy import *


def buildBoat(file, initState, targets, name=None):
    param = readParam(file)
    defInitState = {'pos': (0, 0), 'speed': (0, 0), 'angle': 0, 'angular_speed': 0,
                    'engine_on': True, 'gear': 1, 'reverse': False, 'cape': 0}
    for a in initState:
        defInitState[a] = initState[a]

    if name != None:
        param['boatName'] = name

    if param['boatType'] == 'BasicBoat':
        return Boat(param, defInitState, targets)
    elif param['boatType'] == 'TRBoat':
        return TRBoat(param, defInitState, targets)
    elif param['boatType'] == 'DQNBoat':
        return DQNBoat(param, defInitState, targets)


def readParam(file):
    param = {}
    with open(file) as f:
        text = f.readlines()
    for l in text:
        l = l.replace("\n", "")
        l = l.replace(" ", "")
        if len(l) > 1:
            a, b = l.split("=")
            try:
                param[a] = float(b)
                if param[a] == int(param[a]):
                    param[a] = int(param[a])
            except:
                param[a] = b
    return param
