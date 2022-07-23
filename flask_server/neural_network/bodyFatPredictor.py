from fc_layer import FCLayer
from activation_layer import ActivationLayer
from performance_tracker import PerformanceTracker
from layer import Layer
from loss_functions import LossFunctions
from activation_functions import ActivationFunctions
from network import Network
from data_scaler import DataScaler

import numpy as np
import pandas as pd


SAVE = True 


if __name__ == '__main__':
    data = pd.read_csv(r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\datasets\bodyfat.csv')
    data = data.to_numpy()

    #parameters being used: weight chest abdomen and hip measurements

    Y = np.array([[row[1]] for row in data], dtype = 'float')
    Y = np.ma.masked_equal(Y, 0) #remove zeroes from data

    X = np.array([[row[3], row[6], row[7], row[8]] for row in data], dtype = 'float')


    yScaler = DataScaler(1)
    yScaler.fitData(Y)
    convertedY = yScaler.transformData(Y)
    print(f'Y: {len(convertedY)}')

    xScaler = DataScaler(4)
    xScaler.fitData(X)
    convertedX = xScaler.transformData(X)
    print(f'X: {len(convertedX)}')

    convertedY = convertedY.reshape(convertedY.shape[0], 1, 1)
    convertedX = convertedX.reshape(convertedX.shape[0], 1, X.shape[1])

    print(xScaler.featureMaxMin)

    # build network model:
    #     input layer with 4 neurons
    #     hidden layer with 4 neurons
    #     output layer with one neuron and sigmoid activation function 


    network = Network()
    network.add(FCLayer(4, 4))
    network.add(ActivationLayer(ActivationFunctions.RELU, ActivationFunctions.RELUPrime))
    network.add(FCLayer(4, 4))
    network.add(ActivationLayer(ActivationFunctions.RELU, ActivationFunctions.RELUPrime))
    network.add(FCLayer(4, 1))
    network.add(ActivationLayer(ActivationFunctions.sigmoid, ActivationFunctions.sigmoidPrime))

    network.setLoss(LossFunctions.mse, LossFunctions.msePrime)
    
    print('Training network ...')
    network.fit(convertedX, convertedY, 200, 0.05, showLogs = True)

    #test accuracy of network
    predictions = network.predict(convertedX)
    predictions = np.array([yScaler.inverseTransform(prediction[0]) for prediction in predictions])
    
    print(PerformanceTracker.getAverageAcuracy(Y, predictions, True))

    #save network and scalers
    if SAVE:    
        network.save(r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\models\body_fat_predictor\model')
        xScaler.save(r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\models\body_fat_predictor\x_scaler')
        yScaler.save(r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\models\body_fat_predictor\y_scaler')
        print('Model Saved')





