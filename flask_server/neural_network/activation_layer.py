'''Activation Layer'''
from flask_server.neural_network.matrix import Matrix
# from matrix import Matrix
from layer import Layer


class ActivationLayer(Layer):
    def __init__(self, activationFunction, activationDerivative):
        self.activationFunction = activationFunction
        self.activationDerivative = activationDerivative

    def forwardPropagate(self, inputData: Matrix):
        '''
            returns output of applying activation function on input
            this increases the complexity of the multi-layer perceptron and allows the representation of higher order functions
        '''

        self.inputData = inputData
        output = inputData.data
        
        for i in range(0, len(output)):
            for x in range(0, len(output[i])):
                output[i][x] = self.activationFunction(output[i][x])

        self.output = Matrix(inputData.rows, inputData.cols, output)
        return self.output 

    def backPropagate(self, outputError, learningRate):
        #returns input error (partial derivative of E with respect to x)
        output = self.inputData.data
        
        for i in range(0, len(output)):
            for x in range(0, len(output[i])):
                output[i][x] = self.activationDerivative(output[i][x])
        
        output = Matrix(self.inputData.rows, self.inputData.cols, output)
        return outputError.hadamardProduct(output)