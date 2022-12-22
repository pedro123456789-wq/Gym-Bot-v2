'''Data Scaler'''
from pickle import load, dump
#from matrix import Matrix
from flask_server.neural_network.matrix import Matrix


class DataScaler:
    def __init__(self, featureNumber=1, minimum=0, maximum=1):
        self.featureMaxMin = [[0, 0]
                              for _ in range(featureNumber)]  # [[max, min]]
        self.featureNumber = featureNumber 
        self.minimum = minimum
        self.maximum = maximum

    def fitData(self, data: list):
        '''Get maximum and minimum value of each column (feature) to change range of data into desired range
           Normalizing the data will improve the performance of the neural network#
        '''
        # transpose array to turn columns into rows which are easier to index
        data = Matrix(len(data), self.featureNumber, data)
        columns = data.transpose()

        for i in range(0, len(columns.data)):
            column = columns.data[i]
            columnMin, columnMax = min(column), max(column)
            self.featureMaxMin[i][0] = columnMax
            self.featureMaxMin[i][1] = columnMin

    def transformData(self, data: list):
        # transpose data matrix to apply operation to one row at a time
        data = Matrix(len(data), self.featureNumber, data)
        columns = data.transpose()

        for i in range(0, len(columns.data)):
            # numpy allows one to perform arithmetic operations to a whole array
            # use linear interpolation to scale data one column at a time
            dataRange = self.featureMaxMin[i][0] - self.featureMaxMin[i][1]
            outputRange = self.maximum - self.minimum

            column = columns.data[i]
            # apply coding to data to make it lie between 0 and 1
            normalizedColumn = [
                (dp - self.featureMaxMin[i][1]) / dataRange for dp in column]
            # strech coded data to desired range
            output = [(dp * outputRange) +
                      self.minimum for dp in normalizedColumn]
            columns.data[i] = output

        return columns.transpose().data

    def inverseTransform(self, data: list):
        '''use linear interpolation to get data back in original range'''
        data = Matrix(len(data), self.featureNumber, data)
        columns = data.transpose()

        for i in range(0, len(columns.data)):
            dataRange = self.featureMaxMin[i][0] - self.featureMaxMin[i][1]
            outputRange = self.maximum - self.minimum
            column = columns.data[i]

            inputProportion = [(dp - self.minimum) /
                               outputRange for dp in column]
            output = [(dp * dataRange) + self.featureMaxMin[i][1]
                      for dp in column]
            columns.data[i] = output

        return columns.transpose().data

    def save(self, path):
        # serialize object and save it with pickle

        try:
            with open(f'{path}.pickle', 'wb') as stream:
                dump(self, stream)
                stream.close()
                return True

        except Exception as e:
            print(e)
            return False

    def load(self, path):
        # load saved pickle object
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
    data = [[1, 2], [1, 3], [4, 7], [8, 10]]

    scaler = DataScaler(2)
    scaler.fitData(data)

    transformed = scaler.transformData(data)
    print(transformed)

    invertedTransform = scaler.inverseTransform(transformed)
    print(invertedTransform)
