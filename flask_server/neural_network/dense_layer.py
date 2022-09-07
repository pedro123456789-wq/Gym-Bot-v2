'''Dense Layer'''
from layer import Layer
from matrix import Matrix
from vector import Vector

class DenseLayer(Layer):
    def __init__(self, inputSize, outputSize):
        #generate matrix with random numbers for initial weights
        self.weights = Matrix(outputSize, inputSize)
        self.weights.randomInit()

        self.bias = Vector(outputSize)
        self.bias.randomInit()

    def forwardPropagate(self, input: Vector):
        self.input = input
        #add product of inputs with heights plus the bias for each neuron
        self.output = self.weights.multiply(input) + self.bias

        return self.output

    def backPropagate(self, outputError: 'Vector', learningRate: int):
        #partial derivative of error with respect to input
        inputError = weights.transpose().multiply(outputError)
        weights = 
        #partial derivative of input with respect to weights
        weightsError = np.dot(self.input.T, outputError)

        #gradient descent to update weights and biases based on error
        self.weights -= learningRate * weightsError
        self.bias -= learningRate * outputError

        return inputError
        
    


if __name__ == '__main__':
    layer = DenseLayer(1, 3)
    print(layer.weights)
    print(layer.bias)
    # print(layer.forwardPropagate(Vector(1, [0.4])))
    
