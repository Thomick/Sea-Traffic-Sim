from BoatConstructor import *
from BoatFunctions import *
from Utils import *
from Strategies import *
import time

# Display sim
display = True

# Environment definition
targets = [(700, 200), (100, 200), (400, 100)]
boats = []
boat1 = buildBoat("BoatConfig/VectBoat.txt",
                  {'pos': (100, 200), 'angle': -90, 'gear': 1}, [targets[0]], name="Titanic")
boat2 = buildBoat("BoatConfig/VectBoat.txt",
                  {'pos': (700, 300), 'angle': 90}, [targets[1]], name="CDG")
boat3 = buildBoat("BoatConfig/VectBoat.txt",
                  {'pos': (400, 500)}, [targets[2]], name="USS Thomas")
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
    disp.runSim(100, draw_traj=False)
else:
    t = time.time()
    for i in range(2000):
        for b in boats:
            b.update()
    print(time.time() - t)
