import matplotlib.pyplot as plt
from BoatConstructor import *
from BoatFunctions import *
import numpy as np


def get_vectors(boats, screen_size, sample_length):
    #b = buildBoat("BoatConfig/VectBoat.txt")
    #b.boatList = boats
    x = np.arange(0, screen_size[0], sample_length)
    y = np.arange(0, screen_size[1], sample_length)
    X, Y = np.meshgrid(x, y)
    x_shape = X.shape
    U = np.zeros(x_shape)
    V = np.zeros(x_shape)
    C = np.zeros(x_shape)
    for i in range(x_shape[0]):
        for j in range(x_shape[1]):
            v = np.array([0, 0])
            pos = np.array([X[i, j], Y[i, j]])
            if (X[i, j], Y[i, j]) == (450, 300):
                U[i, j] = 0
                V[i, j] = 0
                C[i, j] = 0
            else:
                for boat in boats:
                    v = v - gen_vect(pos, boat)
                n = np.linalg.norm(v)
                U[i, j] = v[0]
                V[i, j] = v[1]
                C[i, j] = n
    m = np.max(C)
    U = U / m * sample_length
    V = V / m * sample_length
    return X, Y, U, V, C


def plot_vectorfield(boats, screen_size, sample_length):
    X, Y, U, V, C = get_vectors(boats, screen_size, sample_length)
    fig, ax = plt.subplots()
    q = ax.quiver(X, Y, U, V, C)
    xb = [b.pos[0] for b in boats]
    yb = [b.pos[1] for b in boats]
    p = ax.scatter(xb, yb)
    ax.set_aspect('equal')
    plt.show()
