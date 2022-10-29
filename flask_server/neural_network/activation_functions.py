'''Activation Functions'''
import math 

class ActivationFunctions:
    @staticmethod
    def tanh(x): 
        return math.tanh(x)
    
    def tanhPrime(x): 
        return 1 - (math.tanh(x) ** 2)

    def sigmoid(x):
        return 1 - 1 / (1 + math.exp(x)) if x < 0 else 1/ (1 + math.exp(-x))

    def sigmoidPrime(x):
        return ActivationFunctions.sigmoid(x) * (1 - ActivationFunctions.sigmoid(x))

    def RELU(x):
        return max(x, 0)

    def RELUPrime(x):
        return 1 if x > 0 else 0


    
    


