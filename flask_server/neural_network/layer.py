'''Base Class for neural network layers'''

class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def forwardPropagate(self, input):
        raise NotImplementedError
    

    def backwardPropagate(self, outputError, learningRate):
        raise NotImplementedError
