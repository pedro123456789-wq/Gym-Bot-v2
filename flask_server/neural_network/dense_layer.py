'''Dense Layer'''
from layer import Layer
from matrix import Matrix


class DenseLayer(Layer):
    def __init__(self, inputSize, outputSize):
        #generate matrix with random numbers for initial weights
        self.weights = Matrix(outputSize, inputSize)
        self.weights.randomInit()

        self.bias = Matrix(outputSize, 1)
        self.bias.randomInit()

    def forwardPropagate(self, inp: Matrix):
        self.input = inp
        #add product of inputs with heights plus the bias for each neuron
        self.output = (self.weights * inp) + self.bias

        return self.output

    def backPropagate(self, outputError: Matrix, learningRate: int):
        #partial derivative of error with respect to input
        dEbydW = self.input.transpose() * outputError
        inputError = self.weights.transpose() * outputError

        #gradient descent to update weights and biases based on error
        self.weights -= (dEbydW * learningRate)
        self.bias -= (outputError * learningRate)

        return inputError
        
    


if __name__ == '__main__':
    layer = DenseLayer(1, 3)
    print(layer.weights)
    print(layer.bias)
    # print(layer.forwardPropagate(Vector(1, [0.4])))
    
