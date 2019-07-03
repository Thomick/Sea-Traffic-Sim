from Boats import *
from BoatFunctions import *
from Utils import *
from Strategies import *
from SimDisplay import *

# Display sim
display = True

# Environment definition
targets = [(300, 100)]
boats = []
boat1 = Boat("Bateau 1", follow_target,
             (100, 100), targets)
boat2 = Boat("Bateau 2", follow_target, (500, 500), targets[::-1])
boats.append(boat1)
boats.append(boat2)

if display:
    scale_factor = 1 / 1
    screen_size = [900, 600]
    boatFile = "Images/boat2.png"
    disp = SimDisplay(screen_size, boatFile)
    disp.initDisplay(boats, scale_factor, targets)
    disp.runSim(100)

else:
    for i in range(1000):
        for b in boats:
            b.update
