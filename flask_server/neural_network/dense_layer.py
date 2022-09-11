'''Dense Layer'''
from layer import Layer
from matrix import Matrix


class DenseLayer(Layer):
    def __init__(self, inputSize, outputSize):
        #generate matrix with random numbers for initial weights
        self.weights = Matrix(inputSize, outputSize)
        self.weights.randomInit()

        self.bias = Matrix(1, outputSize)
        self.bias.randomInit()

    def forwardPropagate(self, inp: Matrix):
        self.input = inp
        #add product of inputs with heights plus the bias for each neuron
        self.output = (inp * self.weights) + self.bias

        return self.output

    def backPropagate(self, dEbydX: Matrix, learningRate: int):
        #partial derivative of error with respect to input
        dEbydW = self.input.transpose() * dEbydX
        inputError = dEbydX * self.weights.transpose()
            
        #gradient descent to update weights and biases based on error
        self.weights -= (dEbydW * learningRate)
        self.bias -= (dEbydX * learningRate)

        return inputError
        
    


if __name__ == '__main__':
    layer = DenseLayer(1, 3)
    print(layer.weights)
    print(layer.bias)
    # print(layer.forwardPropagate(Vector(1, [0.4])))
    
