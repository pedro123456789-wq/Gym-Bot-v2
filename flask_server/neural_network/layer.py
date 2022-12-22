'''Base Class for neural network layers'''

class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def forwardPropagate(self, input):
        # raise error to simulate abstract class
        raise NotImplementedError
    

    def backwardPropagate(self, outputError, learningRate):
        # raise error to simulate abstract class
        raise NotImplementedError
