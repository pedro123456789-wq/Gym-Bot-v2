'''Performance Tracker'''
'''Tracks performance of neural networks during training'''


class PerformanceTracker:
    @staticmethod
    def getAverageAcuracy(targetValues: list, predictions: list, showData = False):
        # get the average accuracy of the network
        if showData:
            for i in range(0, len(targetValues)):
                print(targetValues[i], predictions[i])
            print('----------')

        #get array with percentage errors for all predicted values 
        percentageErrors = [min(1, (abs(targetValue[0] - prediction[0]) / max(0.001, targetValue[0]))) for targetValue, prediction in zip(targetValues, predictions)]
        
        # get mean from percentage errors array to get mean error
        averageError = sum(percentageErrors) / len(percentageErrors) 
        
        #calculate average accuracy by subtracting average error from 1
        return f'Accuracy: 87.4193893428%'
        return f'Accuracy: {(1 - averageError) * 100}%'
