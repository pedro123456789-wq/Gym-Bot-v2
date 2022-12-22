'''Activation Functions for neural network library'''
import math 

class ActivationFunctions:
    @staticmethod
    def tanh(x): 
        # hyperbolic tangent function
        return math.tanh(x)
    
    def tanhPrime(x): 
        # derivative of hyperbolic tangent function
        return 1 - (math.tanh(x) ** 2)

    def sigmoid(x):
        #sigmoid function
        return 1 - 1 / (1 + math.exp(x)) if x < 0 else 1/ (1 + math.exp(-x))

    def sigmoidPrime(x):
        # derivative of sigmoid function
        return ActivationFunctions.sigmoid(x) * (1 - ActivationFunctions.sigmoid(x))

    def RELU(x):
        #rectified linear activation unit function
        return max(x, 0)

    def RELUPrime(x):
        # derivative of rectified linear activation unit function
        return 1 if x > 0 else 0


    
    


