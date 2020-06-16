from Boats import *
from BoatConstructor import *
from BoatFunctions import *
from Utils import *
from Strategies import *
from SimDisplay import *

# Display sim
display = True

# Environment definition
targets = [(800, 300), (200, 300), (500, 200)]
boats = []
boat1 = buildBoat("BoatConfig/VectBoatR.txt",
                  {'pos': (200, 300), 'angle': -90, 'gear': 3}, [targets[0]], name="Titanic")
boat2 = buildBoat("BoatConfig/VectBoatG.txt",
                  {'pos': (800, 300), 'angle': 90}, [targets[1]], name="CDG")
boat3 = buildBoat("BoatConfig/VectBoatB.txt",
                  {'pos': (500, 600)}, [targets[2]], name="USS Thomas")
boats.append(boat1)
boats.append(boat2)
boats.append(boat3)
boat1.boatList = boats
boat2.boatList = boats
boat3.boatList = boats

if display:
    scale_factor = 1 / 1
    screen_size = [900, 600]
    boatFile = "Images/boat2.png"
    disp = SimDisplay(screen_size, boatFile)
    disp.initDisplay(boats, scale_factor, targets)
    disp.runSim(100,vector_field = True)
