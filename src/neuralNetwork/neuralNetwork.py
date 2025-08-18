import math
import random

def normalizeInputs(xDist, yDist):
    #normalize the inputs to be between 0 and 1
    
    xDist /= 193    # max distance (actually 439 at startup. let's see how it goes)
    
    # max distance (difference of position) between the bird and the gap
    yDist /= 393    # this is between -1 and 1 (gap at top with bird at bottom - vice versa), so:
    yDist += 1    # now it's between 0 and 2
    yDist /= 2    # now it's between 0 and 1

    return xDist, yDist

def neuronFunction(input, weight):
    aux = math.log((math.e**-weight)+1)
    aux -= math.log((math.e**weight)+1)
    aux += math.log((math.e**(input+weight))+1)
    aux -= math.log((math.e**(input-weight))+1)
    aux *= (weight**2)
    
    return aux


class Neuron:
    def __init__(self):
        self.value = 0
        self.bias = 0
        self.weights = []

class OutputNeuron:
    def __init__(self):
        self.value = 0
        self.bias = 0

class NeuralNetwork:   
    def __init__(self):
        # 2 input neurons, 2 hidden neurons, 1 output neuron
        self.inputNeuron = [Neuron(), Neuron()]
        self.hiddenNeuron = [Neuron(), Neuron()]
        self.outputNeuron = [OutputNeuron()]

        self.initializeWeights(self.inputNeuron, self.hiddenNeuron)
        self.initializeWeights(self.hiddenNeuron, self.outputNeuron)

        self.initializeBiases(self.inputNeuron)
        self.initializeBiases(self.hiddenNeuron)
        self.initializeBiases(self.outputNeuron)
    
    def initializeWeights(self, layer, nextLayer):
        for neuron in layer:
            for nextNeuron in nextLayer:
                neuron.weights.append(random.random()*2-1)    # random weights between -1 and 1

    def initializeBiases(self, layer):
        for neuron in layer:
            neuron.bias = random.random()*2-1    # random biases between -1 and 1

    def getInputs(self, xDist, yDist):
        # assign the two input neuron as the distances between the bird and the gap
        self.inputNeuron[0].value, self.inputNeuron[1].value = normalizeInputs(xDist, yDist)

    def feedForward(self):
        self.hiddenNeuron[0].value = neuronFunction(self.inputNeuron[0].value, self.inputNeuron[0].weights[0]) + neuronFunction(self.inputNeuron[1].value, self.inputNeuron[1].weights[0]) + self.hiddenNeuron[0].bias
        self.hiddenNeuron[1].value = neuronFunction(self.inputNeuron[0].value, self.inputNeuron[0].weights[1]) + neuronFunction(self.inputNeuron[1].value, self.inputNeuron[1].weights[1]) + self.hiddenNeuron[1].bias

        self.outputNeuron[0].value = neuronFunction(self.hiddenNeuron[0].value, self.hiddenNeuron[0].weights[0]) + neuronFunction(self.hiddenNeuron[1].value, self.hiddenNeuron[1].weights[0]) + self.outputNeuron[0].bias

    def flap(self):
        if self.outputNeuron[0].value > 0:  # jump if output neuron is greater than 0
            return True
        return False
