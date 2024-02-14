import unittest
import numpy as np
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import neural as nue

class TestNeuron(unittest.TestCase):
    def test_feedforward(self):
        weights = np.array([0, 1])
        bias = 4
        n = nue.Neuron(weights, bias)
        inputs = np.array([2, 3])
        result = n.feedforward(inputs)
        self.assertAlmostEqual(result, 0.9990889488055994)  # Replace with the expected output

if __name__ == '__main__':
    unittest.main()