from BoatConstructor import *
from BoatFunctions import *
from Utils import *
from Strategies import *
import time

# Display sim
display = False

# Environment definition
targets = [(800, 300), (200, 300), (500, 200)]
boats = []
boat1 = buildBoat("BoatConfig/LocTRBoat.txt",
                  {'pos': (200, 300), 'angle': -90, 'gear': 3}, [targets[0]], name="Titanic")
boat2 = buildBoat("BoatConfig/LocTRBoat.txt",
                  {'pos': (800, 300), 'angle': 90}, [targets[1]], name="CDG")
boat3 = buildBoat("BoatConfig/LocTRBoat.txt",
                  {'pos': (500, 600)}, [targets[2]], name="USS Thomas")
boats.append(boat1)
boats.append(boat2)
boats.append(boat3)
boat1.boatList = boats
boat2.boatList = boats
boat3.boatList = boats

if display:
    from SimDisplay import *
    scale_factor = 1 / 1
    screen_size = [900, 600]
    boatFile = "Images/boat2.png"
    disp = SimDisplay(screen_size, boatFile)
    disp.initDisplay(boats, scale_factor, targets)
    disp.runSim(100, draw_traj=True)
else:
    t = time.time()
    for i in range(2000):
        for b in boats:
            b.update()
    print(time.time() - t)
