import numpy as np
from Utils import distance


def collide(boat1, boat2):
    return distance(boat1.pos, boat2.pos) < boat1.colRadius + boat2.colRadius


def sprite_collide(boat_sprite1, boat_sprite2):
    return collide(boat_sprite1.boat, boat_sprite2.boat)


def prev_collision(boat1, boat2, step=0, nb_test=5):
    next_pos1 = boat1.phantom_boat.pastTrajectory.to_list()
    next_pos2 = boat2.phantom_boat.pastTrajectory.to_list()
    nb_pos = min(len(next_pos1), len(next_pos2)) - 1
    if step == -1:
        pass
    elif step == 0:
        for i in range(1, nb_test + 1):
            j = i * (nb_pos // (nb_test + 1))
            if distance(next_pos1[j], next_pos2[j]) < boat1.colRadius + boat2.colRadius:
                return True, j
    else:
        j = 0
        for i in range(nb_pos, 1, -step):
            if distance(next_pos1[i], next_pos2[i]) < boat1.colRadius + boat2.colRadius:
                return True, j
            j += step
    return distance(next_pos1[0], next_pos2[0]) < boat1.colRadius + boat2.colRadius, nb_pos


def sprite_prev_collision(boat_sprite1, boat_sprite2):
    col, j = prev_collision(boat_sprite1.boat, boat_sprite2.boat, step=100)
    return col


def gen_vect(pos, boat):
    vect = np.array([0, 0])
    d = distance(pos, boat.pos)
    V = boat.pos - pos
    N = np.array([-boat.dir[1], boat.dir[0]])
    vect = 30 * (V / d - 0.2 * N) / d
    if (V[0]) * boat.dir[0] + (V[1]) * boat.dir[1] < 0:
        vect = vect
    return vect
