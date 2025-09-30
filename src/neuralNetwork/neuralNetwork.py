import math
import random

def normalizeInputs(xDist, yDist):
    #normalize the inputs to be between 0 and 1
    
    xDist /= 193    # max distance (actually 439 at startup. let's see how it goes)
    
    # max distance (difference of position) between the bird and the gap
    yDist /= 393    # this is between -1 and 1 (gap at top with bird at bottom - vice versa), so:
    # let's normalize it to be between 0 and 1
    yDist = (yDist + 1) / 2 # yDist is 0.5 when bird and gap are aligned vertically

    return xDist, yDist

def neuronFunction(input, weight):
    aux = math.log((math.e**-weight)+1)
    aux -= math.log(math.e**(input-weight)+1)
    aux += input
    aux *= (weight**2)
    
    return max(0, aux)


class Neuron:
    def __init__(self, numOutputs):
        self.value = 0
        self.bias = random.random() * 2     # Bias is initialized randomly between 0 and 2.
        self.weights = [random.random() * 2 for _ in range(numOutputs)]     # A list of connection weights to each neuron in the next layer (output's neuron's will have an empty list)

class NeuralNetwork:
    def __init__(self, layerSizes):
        self.layers = []
        numLayers = len(layerSizes)

        # Create all layers based on the provided sizes.
        for i in range(numLayers):
            isOutputLayer = (i == numLayers - 1)
            # Neurons in the output layer have 0 outgoing connections.
            numOutputs = 0 if isOutputLayer else layerSizes[i + 1]
            
            # Create a layer (a list of Neuron objects) and add it to the network.
            layer = [Neuron(numOutputs) for _ in range(layerSizes[i])]
            if i == 0:      #the neurons of the input layer don't have biases
                for neuron in layer:
                    neuron.bias = 0

            self.layers.append(layer)

    def getInputs(self, xDist, yDist):
        # Normalize and set the input values for the network's first layer.
        norm_x, norm_y = normalizeInputs(xDist, yDist)
        self.layers[0][0].value = norm_x
        self.layers[0][1].value = norm_y

    def feedForward(self):
        # Iterate through each layer, starting from the first hidden layer (index 1)
        for i in range(1, len(self.layers)):
            prevLayer = self.layers[i - 1]
            currentLayer = self.layers[i]

            # For each neuron in the current layer...
            for j, neuron in enumerate(currentLayer):
                neuron.value = 0
                # ...sum the weighted outputs from the previous layer.
                for prevNeuron in prevLayer:
                    # Get the weight connecting the previous neuron to the current one.
                    weight = prevNeuron.weights[j]
                    neuron.value += neuronFunction(prevNeuron.value, weight)
                
                # The neuron's new value is the sum + its bias.
                neuron.value += neuron.bias

    def flap(self):
        if self.layers[-1][0].value < 5:    # output neuron ranges from 0 to 19 if weight and bias range from 0 to 2 (tested). Jump threshold set as 5 (usual mean output neuron value, when weights and biases are random) just for now (jumps if smaller because lower value means the bird is closer to the ground)
            return True
        else:
            return False
        
        # PS: array[-1] gets the last element of the array (output layer)
