import numpy as np

def segmoid(x) :
    return 1 / (1 + np.exp(-x))

class Neuron:
    def __init__(self, weights, bias) :
        self.weights = weights
        self.bias = bias

    def feedforward(self, inputs) :
        total = np.dot(inputs, self.weights) + self.bias
        return segmoid(total)

#weight of the neuron
weights = np.array([0, 1])
#bias of the neuron
bias = 4

n = Neuron(weights, bias)

x = np.array([2, 3])

print(n.feedforward(x))