from Boats import *
from BoatConstructor import *
from BoatFunctions import *
from Utils import *
from Strategies import *
from SimDisplay import *

# Display sim
display = True

# Environment definition
targets = [(800, 200), (200, 200)]
boats = []
boat1 = buildBoat("BoatConfig/testboat.txt",
                  {'pos': (100, 200), 'angle': -90}, [targets[0]], name="Titanic")
boat2 = buildBoat("BoatConfig/testboat.txt",
                  {'pos': (800, 200), 'angle': 90}, [targets[1]], name="CDG")
boats.append(boat1)
boats.append(boat2)
boat1.boatList = boats
boat1.boatList = boats

if display:
    scale_factor = 1 / 1
    screen_size = [900, 600]
    boatFile = "Images/boat2.png"
    disp = SimDisplay(screen_size, boatFile)
    disp.initDisplay(boats, scale_factor, targets)
    disp.runSim(1000)
