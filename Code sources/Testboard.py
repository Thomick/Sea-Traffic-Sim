from BoatConstructor import *
from BoatFunctions import *
from Utils import *
from Strategies import *
import time

# Display sim
display = True

# Environment definition
targets = [(600, 500), (600, 400), (600, 300), (600, 200), (600, 100)]
boats = []
boat1 = buildBoat("BoatConfig/VectBoatR.txt",
                  {'pos': (100, 100), 'angle': -90}, [targets[0]], name="Titanic", add_param={"priority": 1})
boat2 = buildBoat("BoatConfig/VectBoatB.txt",
                  {'pos': (100, 200), 'angle': -90}, [targets[1]], name="CDG", add_param={"priority": 1})
boat3 = buildBoat("BoatConfig/VectBoatG.txt",
                  {'pos': (100, 300), 'angle': -90}, [targets[2]], name="USS Thomas")
boat4 = buildBoat("BoatConfig/VectBoatR.txt",
                  {'pos': (100, 400), 'angle': -90}, [targets[3]], name="Titanic", add_param={"priority": 1})
boat5 = buildBoat("BoatConfig/VectBoatB.txt",
                  {'pos': (100, 500), 'angle': -90}, [targets[4]], name="CDG", add_param={"priority": 1})

boats.append(boat1)
boats.append(boat2)
boats.append(boat3)
boats.append(boat4)
boats.append(boat5)
boat1.boatList = boats
boat2.boatList = boats
boat3.boatList = boats
boat4.boatList = boats
boat5.boatList = boats

if display:
    from SimDisplay import *
    scale_factor = 1 / 1
    screen_size = [900, 600]
    boatFile = "Images/boat2.png"
    disp = SimDisplay(screen_size, boatFile)
    disp.initDisplay(boats, scale_factor, targets)
    disp.runSim(60, draw_traj=False, vector_field=True)
else:
    t = time.time()
    for i in range(2000):
        for b in boats:
            b.update()
    print(time.time() - t)
