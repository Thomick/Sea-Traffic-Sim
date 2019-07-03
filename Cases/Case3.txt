from Boats import *
from BoatFunctions import *
from Utils import *
from Strategies import *
from SimDisplay import *

# Display sim
display = True

# Environment definition
targets = [(800, 200), (200, 200), (500, 200)]
boats = []
boat1 = Boat("Bateau 1", follow_target, go_right_maneuver,
             (200, 300), [targets[0]])
boat2 = Boat("Bateau 2", follow_target, go_right_maneuver, (800, 300),
             [targets[1]], starting_angle=90)
boat3 = Boat("Bateau 3", follow_target, go_right_maneuver, (500, 600),
             [targets[2]], starting_angle=0)
boats.append(boat1)
boats.append(boat2)
boats.append(boat3)

if display:
    scale_factor = 1 / 1
    screen_size = [900, 600]
    boatFile = "Images/boat2.png"
    disp = SimDisplay(screen_size, boatFile)
    disp.initDisplay(boats, scale_factor, targets)
    disp.runSim(100)
