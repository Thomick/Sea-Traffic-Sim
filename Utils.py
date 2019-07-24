import numpy as np


def scale_convert_vector(v, scale):
    return np.around(np.array(v) * scale).astype(int)


def distance(A, B):
    return np.linalg.norm(A - B)


def unit_vector(V):
    return V / np.linalg.norm(V)


def angle_between(A, B):
    A_u = unit_vector(A)
    B_u = unit_vector(B)
    # Attention angle en radians
    return np.arccos(np.clip(np.dot(A_u, B_u), -1.0, 1.0))


def scalar_to_coord_on_edge(rect, p):
    pos = [rect[0], rect[1]]
    width, height = rect[2], rect[3]
    p = p * (2 * width + 2 * height)
    if p < (width + height):
        if p < width:
            pos[0] += p
        else:
            pos[0] += width
            pos[1] += p - width
    else:
        p = p - (width + height)
        if p < width:
            pos[0] += width - p
            pos[1] += height
        else:
            pos[1] += height - (p - width)
    return pos


def random_point_on_edge(rect):
    p = np.random.random()
    pos = scalar_to_coord_on_edge(rect, p)
    return pos


def evenly_spaced_points_on_edge(rect, nbPoints):
    p = np.linspace(0, 1, nbPoints + 1)[:nbPoints]
    pos = []
    for s in p:
        pos.append(scalar_to_coord_on_edge(rect, s))
    print(len(pos))
    return pos
