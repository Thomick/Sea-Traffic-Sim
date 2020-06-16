import numpy as np
import random
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Bloc de base pour des IA de jeu dynamiques


class BasicNeuralAI():
    def __init__(self, nb_neuron, weights=None):
        self.weights = weights

    def get_action(self, input):
        return 0


class NN1L():
    def __init__(self, nb_neuron, weights=None):
        self.nb_input = nb_neuron[0]
        self.nb_output = nb_neuron[1]
        if weights is None:
            self.randomize_weights()
        else:
            self.weights = weights

    def get_action(self, input):
        in_array = np.array([input[e] for e in input])
        return sigmoid(np.dot(self.weights[0], in_array))

    def randomize_weights(self):
        self.weights = [np.random.random((self.nb_output, self.nb_input)) *
                        2 - 1]


class Population():
    def __init__(self, nb_ind, NNType, NNShape, eval_function):
        self.nb_ind = nb_ind
        self.NNType = NNType
        self.NNShape = NNShape
        self.pop = [[0, self.pattern(NNShape)]
                    for i in range(nb_ind)]  # (reward,agent)
        self.eval_function = eval_function

    def select(self):
        self.pop.sort(key=lambda ind: ind[0], reverse=True)
        self.pop = self.pop[:self.nb_ind // 2]

    def breed(self):
        n = len(self.pop)
        rew_tot = np.sum([self.pop[i][0] for i in range(n)])
        prob = [self.pop[i][0] / rew_tot for i in range(n)]
        while len(self.pop) < self.nb_ind:
            a1, a2 = np.random.choice(n, 2, prob)
            new_w = []
            for k in range(len(self.pop[a1][1].weights)):
                w1, w2 = self.pop[a1][1].weights[k].ravel(
                ), self.pop[a2][1].weights[k].ravel()
                new_w.append(np.array([np.random.choice((w1[i], w2[i]))
                                       for i in range(len(w1))]).reshape(self.pop[a1][1].weights[k].shape))
            self.pop.append([0, self.NNType(
                self.NNShape, new_w)])

    def mutate(self, prob):
        for i in range(5, len(self.pop)):
            for k in range(len(self.pop[i][1].weights)):
                w = self.pop[i][1].weights[k].ravel()
                for j in range(len(w)):
                    if np.random.random() < prob:
                        w[j] += 0.5 * (np.random.normal() * 2 - 1)

    def train(self, nb_gen, render=False):
        for i in range(nb_gen):
            print(i)
            for a in range(len(self.pop)):
                self.pop[a][0] = 0
            for j in range(self.nb_ind):
                self.pop[j][0] += self.eval_function(self.pop[j][1])
            self.select()
            self.breed()
            self.mutate(0.3)
            print(f"Best Score {self.pop[0][0]}")
