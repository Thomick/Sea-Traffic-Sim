from BoatConstructor import buildBoat
from SimDisplay import SimDisplay
from Utils import random_point_on_edge
import numpy as np

# Display sim
display = True
nbBoat = 8
scale_factor = 1 / 1
screen_size = [900, 600]
screen_rect = (100, 100, 700, 400)

# Environment definition
targets = []
boats = []
for i in range(nbBoat):
    targets.append(random_point_on_edge(screen_rect))
    boats.append(buildBoat("BoatConfig/LocTRBoat.txt",
                           {'pos': random_point_on_edge(screen_rect),
                            'angle': int(np.random.random() * 360 - 180)},
                           [targets[i]], name=str(i)))
for b in boats:
    b.boatList = boats

if display:
    boatFile = "Images/boat2.png"
    disp = SimDisplay(screen_size, boatFile)
    disp.initDisplay(boats, scale_factor, targets)
    disp.runSim(1000)
