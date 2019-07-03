from Boats import *
import numpy as np
from Utils import *


def collide(boat1, boat2):
    return distance(boat1.pos, boat2.pos) < boat1.colRadius + boat2.colRadius


def sprite_collide(boat_sprite1, boat_sprite2):
    return collide(boat_sprite1.boat, boat_sprite2.boat)


def prev_collision(boat1, boat2, step=1):
    next_pos1 = boat1.phantom_boat.pastTrajectory.to_list()
    next_pos2 = boat2.phantom_boat.pastTrajectory.to_list()
    nb_pos = min(len(next_pos1), len(next_pos2)) - 1
    j = 0
    for i in range(nb_pos, 1, -step):
        if distance(next_pos1[i], next_pos2[i]) < boat1.colRadius + boat2.colRadius:
            return True, j
        j += step
    return distance(next_pos1[0], next_pos2[0]) < boat1.colRadius + boat2.colRadius, nb_pos


def sprite_prev_collision(boat_sprite1, boat_sprite2):
    return prev_collision(boat_sprite1.boat, boat_sprite2.boat, step=1000)[0]
