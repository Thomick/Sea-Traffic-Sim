from BoatConstructor import *
from BoatFunctions import *
from Utils import *
from Strategies import *
import time

# Display sim
display = True

# Environment definition
targets = [(500, 200), (400, 100)]
boats = []
boat1 = buildBoat("BoatConfig/VectBoatR.txt",
                  {'pos': (200, 200), 'angle': -90, 'gear': 1}, [targets[0]], name="Titanic")

boat3 = buildBoat("BoatConfig/VectBoatG.txt",
                  {'pos': (400, 400)}, [targets[1]], name="USS Thomas")
boats.append(boat1)
boats.append(boat3)
boat1.boatList = boats
boat3.boatList = boats

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
