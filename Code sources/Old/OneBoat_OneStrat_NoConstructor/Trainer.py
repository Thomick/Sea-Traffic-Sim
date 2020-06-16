from Ocean import *
from Utils import *
from TNeuralNetwork import *


def run(boat, nbIt):
    for it in range(nbIt):
        boat.update()
        if boat.targetReached:
            return it, distance(boat.pos, boat.target)
    return it, distance(boat.pos, boat.target)


def eval_func(weights):
    return None
    #TODO

def trainer():
    return None
    #TODO
