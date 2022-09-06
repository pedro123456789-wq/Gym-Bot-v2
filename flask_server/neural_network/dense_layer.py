'''Fully Connected Layer'''
from layer import Layer
import numpy as np

class FCLayer(Layer):
    def __init__(self, inputSize, outputSize):
        #generate matrix with random numbers for initial weights
        self.weights = np.random.rand(inputSize, outputSize) - 0.5 
        self.bias = np.random.rand(1, outputSize) - 0.5 #bias vector

    def forwardPropagate(self, input):
        self.input = input
        #add product of inputs with heights plus the bias for each neuron
        self.output = np.dot(self.input, self.weights) + self.bias

        return self.output

    def backPropagate(self, outputError, learningRate):
        #partial derivative of error with respect to input
        inputError = np.dot(outputError, self.weights.T)

        #partial derivative of input with respect to weights
        weightsError = np.dot(self.input.T, outputError)

        #gradient descent to update weights and biases based on error
        self.weights -= learningRate * weightsError
        self.bias -= learningRate * outputError

        return inputError
        
    


if __name__ == '__main__':
    
    layer = FCLayer()
    