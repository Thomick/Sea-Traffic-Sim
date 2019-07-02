import numpy as np


def follow_target(boat, target):
    # Choix du côté vers lequel on tourne par calcul du déterminant des vecteurs  (boat.dir,BT)
    # det < 0 => sin < 0 => Droite et inversement
    BT = target - boat.pos
    BT_norm = BT / np.linalg.norm(BT)
    det = boat.dir[0] * BT_norm[1] - boat.dir[1] * BT_norm[0]
    boat.cape = -det / (1 + abs(boat.angular_speed))

def controlled(boat, target): #Do nothing
    return None