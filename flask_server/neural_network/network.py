'''Neural Network'''
from time import time
from pickle import dump, load



class Network:
    def __init__(self):
        self.layers = []
        self.loss = None
        self.lossPrime = None

    
    def add(self, layer):
        self.layers.append(layer)

    
    def setLoss(self, loss, lossPrime):
        self.loss = loss
        self.lossPrime = lossPrime


    #function used to train the network
    def fit(self, xTrain, yTrain, epochs, learningRate, showLogs = True):
        samples = len(xTrain)
        trainStart = time()
        
        for epoch in range(epochs):
            epochStart = time()
            error = 0

            for sampleIndex in range(samples):
                #forward propagtion
                #for each sample, input it to the input layer and computer its output at the output layer
                output = xTrain[sampleIndex]

                for layer in self.layers:
                    output = layer.forwardPropagate(output)
                
                #compute error by comparing output of network with correct value in the training dataset
                error += self.loss(yTrain[sampleIndex], output)


                #back propagation to update weights after computing error
                #start with error at output layer and work backwards to obtain error at the input layer
                errorPrime = self.lossPrime(yTrain[sampleIndex], output)
                for layer in self.layers[::-1]:
                    errorPrime = layer.backPropagate(errorPrime, learningRate)

            meanError = error / samples
            duration = time() - epochStart
            
            if showLogs:
                print(f'-> Epoch: {epoch + 1}  Error: {meanError}  Duration: {duration}')

        totalTime = time() - trainStart

        if showLogs:
            print('\n--- Training Finished ---')
            print(f'Error: {meanError} \n Execution Time: {totalTime}')


    def predict(self, inputData):
        outputs = []

        #forward propagate all inputs
        for i in range(0, len(inputData)):
            output = inputData[i]

            for layer in self.layers:
                output = layer.forwardPropagate(output)
            
            outputs.append(output)

        return outputs


    def save(self, path):
        #serialize object with pickle and save it for future use
        try:
            with open(f'{path}.pickle', 'wb') as stream:
                dump(self, stream)
                stream.close()
                return True

        except Exception:
            print('Invalid path')
            return False 


    def load(self, path):
        #load saved network object
        try:
            with open(f'{path}.pickle', 'rb') as stream:
                network = load(stream)
                self.layers = network.layers
                self.loss = network.loss
                self.lossPrime = network.lossPrime
                
                stream.close()
                return True
        
        except Exception:
            print('Invalid path')
            return False 
    