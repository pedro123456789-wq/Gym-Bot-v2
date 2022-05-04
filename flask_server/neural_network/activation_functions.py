'''Activation Functions'''
import numpy as np

class ActivationFunctions:
    @staticmethod
    def tanh(x): 
        return np.tanh(x)
    
    def tanhPrime(x): 
        return 1 - (np.tanh(x) ** 2)

    def sigmoid(x):
        return 1  / (1 + np.exp(-x))

    def sigmoidPrime(x):
        return ActivationFunctions.sigmoid(x) * (1 - ActivationFunctions.sigmoid(x))

    def RELU(x):
        return np.maximum(x, 0)

    def RELUPrime(x):
        return np.where(x > 0, 1.0, 0.0)


    
    


