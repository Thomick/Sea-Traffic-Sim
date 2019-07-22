import numpy as np


def follow_target(boat, target):
    # Choix du côté vers lequel on tourne par calcul du déterminant des vecteurs  (boat.dir,BT)
    # det < 0 => sin < 0 => Droite et inversement
    BT = target - boat.pos
    BT_norm = BT / np.linalg.norm(BT)
    scal = boat.dir[0] * BT_norm[0] + boat.dir[1] * BT_norm[1]
    det = boat.dir[0] * BT_norm[1] - boat.dir[1] * BT_norm[0]
    if scal == -1:
        boat.cape = -1
    elif det >= 0:
        boat.cape = -(det**0.5)
    else:
        boat.cape = (-det)**0.5


def go_right_maneuver(boat):
    for i in range(10):
        boat.maneuver.append(-1)


def strat_or_maneuver(boat, target):
    if len(boat.maneuver) > 0:
        boat.cape = boat.maneuver.pop()
    else:
        boat.common_nav_strat(boat, target)


def controlled(boat, target):  # Do nothing
    return None
