'''Activation Layer'''
from layer import Layer


class ActivationLayer(Layer):
    def __init__(self, activationFunction, activationDerivative):
        self.activationFunction = activationFunction
        self.activationDerivative = activationDerivative

    def forwardPropagate(self, inputData):
        '''
            returns output of applying activation function on input
            this increases the complexity of the multi-layer perceptron and allows the representation of higher order functions
        '''

        self.inputData = inputData
        self.output = self.activationFunction(inputData)

        return self.output

    #returns input error (partial derivative of E with respect to x)
    def backPropagate(self, outputError, learningRate):
        return self.activationDerivative(self.inputData) * outputError
