'''Performance Tracker'''
'''Tracks performance of neural networks during training'''


class PerformanceTracker:
    @staticmethod
    def getAverageAcuracy(targetValues: list, predictions: list, showData = False):

        if showData:
            for i in range(0, len(targetValues)):
                print(targetValues[i], predictions[i])
            print('----------')

        #get array with percentage errors for all predicted values 
        percentageErrors = [abs(targetValue[0] - prediction[0]) / max(1, targetValue[0]) for targetValue, prediction in zip(targetValues, predictions)]
        # get mean from percentage errors array to get mean error
        averageError = sum(percentageErrors) / len(percentageErrors) 

        #calculate average accuracy by subtracting average error from 1
        return f'Accuracy: {(1 - averageError) * 100}%'
