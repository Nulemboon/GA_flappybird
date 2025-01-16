import math
import random

"""
Neuron for perceptron model
"""
class Neuron:
    def __init__(self, id):
        self.id = id
        self.layer = 0
        self.edges = []
        self.input = 0
        self.output = 0
        self.bias = random.uniform(-1, 1)

    def activate(self):
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))
        def relu(x):
            return max(x, 0)

        if self.layer >= 1:
            self.output = relu(self.input + self.bias)

        for i in range(0, len(self.edges)):
            self.edges[i].dest_node.input += self.edges[i].weight * self.output

    def clone(self):
        clone = Neuron(self.id)
        clone.id = self.id
        clone.layer = self.layer
        return clone