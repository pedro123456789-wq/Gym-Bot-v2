import pandas as pd
import numpy as np
from data_scaler import DataScaler
from activation_layer import ActivationLayer
from performance_tracker import PerformanceTracker
from loss_functions import LossFunctions
from activation_functions import ActivationFunctions
from network import Network
from data_scaler import DataScaler
from fc_layer import FCLayer

SAVE = True 

if __name__ == '__main__':
    #-----------get data---------------
    # read data from csv files 
    caloriesFile = pd.read_csv(r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\datasets\calories.csv')
    exerciseFile = pd.read_csv(r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\datasets\exercise.csv')
    exercises = exerciseFile.to_numpy()
    
    # turn data into arrays 
    Y = np.array(caloriesFile['Calories'])
    Y = Y.reshape(Y.shape[0], 1)
    X = np.array([[1 if row[1] == 'male' else 0, row[2], row[3], row[4], row[5], row[6]] for row in exercises])
    
    # normalize data 
    yScalar = DataScaler(1)
    yScalar.fitData(Y)
    Y = yScalar.transformData(Y)
    
    xScalar = DataScaler(6)
    xScalar.fitData(X)
    X = xScalar.transformData(X)
    
    Y = Y.reshape(Y.shape[0], 1, 1)
    X = X.reshape(X.shape[0], 1, X.shape[1])
    
    xTrain, xTest = X[:14000], X[14000:]
    yTrain, yTest = Y[:14000], Y[14000:]
    
    #---------build and train neural network---------------
    network = Network()
    # input layer 
    network.add(FCLayer(6, 10))
    network.add(ActivationLayer(ActivationFunctions.sigmoid, ActivationFunctions.sigmoidPrime))
    
    # hidden layer
    network.add(FCLayer(10, 10))
    network.add(ActivationLayer(ActivationFunctions.RELU, ActivationFunctions.RELUPrime))
    
    # output layer
    network.add(FCLayer(10, 1))
    network.add(ActivationLayer(ActivationFunctions.sigmoid, ActivationFunctions.sigmoidPrime))
    
    network.setLoss(LossFunctions.mse, LossFunctions.msePrime)
    
    # train model and make predictions
    network.fit(xTrain, yTrain, 100, 0.07)
    predictions = network.predict(xTest)
    predictions = np.array([yScalar.inverseTransform(prediction[0]) for prediction in predictions])
    yTest = np.array([yScalar.inverseTransform(dp) for dp in yTest])
    
    # get accuracy of model
    print(PerformanceTracker.getAverageAcuracy(yTest, predictions, True))
    
    # save model and predictors
    if SAVE:
        network.save(r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\models\calories_burned_predictor\model')
        xScalar.save(r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\models\calories_burned_predictor\x_scaler')
        yScalar.save(r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\models\calories_burned_predictor\y_scaler')
        print('Model Saved')