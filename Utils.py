import numpy as np


def scale_convert_vector(v, scale):
    return np.around(np.array(v) * scale).astype(int)


def distance(A, B):
    return np.linalg.norm(A - B)


def random_point_on_edge(rect):
    rand_pos = [0, 0]
    x, y = rect[0], rect[1]
    width, height = rect[2], rect[3]
    p = np.random.randint(0, 2 * width + 2 * height)
    if p < (width + height):
        if p < width:
            rand_pos[0] = x + p
            rand_pos[1] = y
        else:
            rand_pos[0] = x + width
            rand_pos[1] = y + p - width
    else:
        p = p - (width + height)
        if p < width:
            rand_pos[0] = x + width - p
            rand_pos[1] = y + height
        else:
            rand_pos[0] = x
            rand_pos[1] = y + height - (p - width)
    return rand_pos
