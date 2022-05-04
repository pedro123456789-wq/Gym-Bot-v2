'''Performance Tracker'''
'''Tracks performance of neural networks during training'''
import numpy as np


class PerformanceTracker:
    @staticmethod
    def getAverageAcuracy(targetValues, predictions, showData = False):
        targetValues = targetValues.reshape(targetValues.shape[0])
        predictions = predictions.reshape(predictions.shape[0])

        if showData:
            for i in range(0, len(targetValues)):
                print(targetValues[i], predictions[i])
            print('----------')

        #get array with percentage errors for all predicted values 
        errorPercentage = abs(targetValues - predictions) / targetValues

        #calculate mean value from array to get average error
        averageError = np.sum(errorPercentage) / errorPercentage.shape[0]

        #calculate average accuracy by subtracting average error from 1
        return f'Accuracy: {(1 - averageError) * 100}%'
