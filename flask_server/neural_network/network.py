'''Neural Network'''
from time import time
from pickle import dump, load
from flask_server.neural_network.matrix import Matrix
#from matrix import Matrix


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
                inputData = xTrain[sampleIndex]
                inputData = Matrix(1, len(inputData), [inputData])

                for layer in self.layers:
                    inputData = layer.forwardPropagate(inputData)
                
                #compute error by comparing output of network with correct value in the training dataset
                error += self.loss(yTrain[sampleIndex], inputData.data[0][0])

                #back propagation to update weights after computing error
                #start with error at output layer and work backwards to obtain error at the input layer
                dEbydX = Matrix(1, 1, [[self.lossPrime(yTrain[sampleIndex], inputData.data[0][0])]])

                for layer in self.layers[::-1]:
                    dEbydX = layer.backPropagate(dEbydX, learningRate)

            meanError = error / samples
            duration = time() - epochStart
            
            if showLogs:
                print(f'-> Epoch: {epoch + 1}  Error: {meanError}  Duration: {duration}')

        totalTime = time() - trainStart

        if showLogs:
            print('\n--- Training Finished ---')
            print(f'Error: {meanError} \n Execution Time: {totalTime}')


    def predict(self, inputData: list):
        outputs = []
        inputData = [Matrix(1, len(dataPoint), [dataPoint]) for dataPoint in inputData]
        
        #forward propagate all inputs
        for i in range(0, len(inputData)):
            output = inputData[i]

            for layer in self.layers:
                output = layer.forwardPropagate(output)
            
            outputs.append(output.data[0][0])

        return outputs


    def save(self, path):
        #serialize object with pickle and save it for future use
        try:
            with open(f'{path}.pickle', 'wb') as stream:
                dump(self, stream)
                stream.close()
                return True

        except Exception as e:
            print(e)
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
        
        except Exception as e:
            print(e)
            return False 
    