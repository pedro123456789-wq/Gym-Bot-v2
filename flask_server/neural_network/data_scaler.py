'''Data Scaler'''
import numpy as np
from pickle import load, dump



class DataScaler:
    def __init__(self, featureNumber = 1, minimum = 0, maximum = 1):
        self.featureMaxMin = [[0, 0] for _ in range(featureNumber)]  #[[max, min]]
        self.minimum = minimum
        self.maximum = maximum


    def fitData(self, data):
        '''Get maximum and minimum value of each column (feature) to change range of data into desired range
           Normalizing the data will improve the performance of the neural network#
        '''
        #transpose array to turn columns into rows which are easier to index
        columns = data.T

        for i in range(0, len(columns)):
            columnMin, columnMax = np.percentile(columns[i], [0, 100])
            self.featureMaxMin[i][0] = columnMax
            self.featureMaxMin[i][1] = columnMin


    def transformData(self, data):
        #transpose data matrix to apply operation to one row at a time
        dataCopy = np.copy(data).T

        for i in range(0, len(dataCopy)):
            #numpy allows one to perform arithmetic operations to a whole array
            #use linear interpolation to scale data one column at a time
            dataRange = self.featureMaxMin[i][0] - self.featureMaxMin[i][1]
            outputRange = self.maximum - self.minimum

            inputProportion = (dataCopy[i] - self.featureMaxMin[i][1]) / dataRange
            output = (inputProportion * outputRange) + self.minimum
            dataCopy[i] = output

        return dataCopy.T


    def inverseTransform(self, data):
        #linear interpolate back to get data in original range
        dataCopy = np.copy(data).T
        
        for i in range(0, len(dataCopy)):
            dataRange = self.featureMaxMin[i][0] - self.featureMaxMin[i][1]
            outputRange = self.maximum - self.minimum

            inputProportion = (dataCopy[i] - self.minimum) / outputRange
            output = (inputProportion * dataRange) + self.featureMaxMin[i][1]
            dataCopy[i] = output
        
        return dataCopy.T

    
    def save(self, path):
        #serialize object and save it with pickle

        try:
            with open(f'{path}.pickle', 'wb') as stream:
                dump(self, stream)
                stream.close()
                return True

        except Exception as e:
            print(e)
            return False 


    def load(self, path):
        #load save pickle object

        try:
            with open(f'{path}.pickle', 'rb') as stream:
                scaler = load(stream)
                self.featureMaxMin = scaler.featureMaxMin
                self.minimum = scaler.minimum
                self.maximum = scaler.maximum
                
                return True
        
        except Exception as e:
            print(e)
            return False
                            




if __name__ == '__main__':
    '''Test'''

    data = np.array([[1, 2], [1, 3], [4, 7], [8, 10]], dtype = 'float')
    print(data)

    scaler = DataScaler(2)
    scaler.fitData(data)
    
    transformed = scaler.transformData(data)
    print(transformed)

    invertedTransform = scaler.inverseTransform(transformed)
    print(invertedTransform)