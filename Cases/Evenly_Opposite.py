from Boats import *
from BoatConstructor import *
from BoatFunctions import *
from Utils import *
from Strategies import *
import time

# Display sim
display = True
nbBoat = 10
screen_rect = (100, 100, 700, 400)

# Environment definition
targets = []
boats = []
pos = evenly_spaced_points_on_edge(screen_rect, nbBoat)
for i in range(nbBoat):
    targets.append(random_point_on_edge(screen_rect))
    boats.append(buildBoat("BoatConfig/LocTRBoat.txt",
                           {'pos': pos[i], 'angle': int(np.random.random() * 360 - 180)}, [pos[(i + nbBoat // 2) % nbBoat]], name=str(i)))
for b in boats:
    b.boatList = boats

if display:
    from SimDisplay import *
    scale_factor = 1 / 1
    screen_size = [900, 600]
    boatFile = "Images/boat2.png"
    disp = SimDisplay(screen_size, boatFile)
    disp.initDisplay(boats, scale_factor, pos)
    disp.runSim(100)
else:
    t = time.time()
    for i in range(2000):
        for b in boats:
            b.update()
    print(time.time() - t)
