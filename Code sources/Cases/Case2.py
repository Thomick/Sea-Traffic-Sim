from BoatConstructor import buildBoat
from SimDisplay import SimDisplay

# Display sim
display = True

# Environment definition
targets = [(800, 200), (200, 200)]
boats = []
boat1 = buildBoat("BoatConfig/LocTRBoat.txt",
                  {'pos': (100, 200), 'angle': -90, 'gear': 3}, [targets[0]], name="Titanic")
boat2 = buildBoat("BoatConfig/LocTRBoat.txt",
                  {'pos': (800, 200), 'angle': 90}, [targets[1]], name="CDG")
boat3 = buildBoat("BoatConfig/LocTRBoat.txt",
                  {'pos': (400, 200), 'angle': -90}, [targets[0]], name="USS Thomas")
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
    disp.runSim(1000)
