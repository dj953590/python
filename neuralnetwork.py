import numpy as np
import neural as nue

class NeuralNetwork:
    def __init__(self):
        weights = np.array([0,1])
        bias = 0
        
        self.h1 = nue.Neuron(weights, bias)
        self.h2 = nue.Neuron(weights, bias)
        self.o1 = nue.Neuron(weights, bias)
        
    def feedforward(self, inputs):
        h1_output = self.h1.feedforward(inputs)
        h2_output = self.h2.feedforward(inputs)
        o1_output = self.o1.feedforward(np.array([h1_output, h2_output]))
        return o1_output
    
netw = NeuralNetwork()    
x = np.array([2,3])

print(netw.feedforward(x))