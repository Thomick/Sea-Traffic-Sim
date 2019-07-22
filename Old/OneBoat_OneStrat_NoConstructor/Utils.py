import numpy as np


def scale_convert_vector(v, scale):
    return np.around(np.array(v) * scale).astype(int)


def distance(A, B):
    return np.linalg.norm(A - B)


def random_point_on_edge(rect):
    rand_pos = [0, 0]
    width, height = rect.width, rect.height
    p = np.random.randint(0, 2 * width + 2 * height)
    if p < (width + height):
        if p < width:
            rand_pos[0] = p
            rand_pos[1] = 0
        else:
            rand_pos[0] = width
            rand_pos[1] = p - width
    else:
        p = p - (width + height)
        if p < width:
            rand_pos[0] = width - p
            rand_pos[1] = height
        else:
            rand_pos[0] = 0
            rand_pos[1] = height - (p - width)
    return rand_pos
