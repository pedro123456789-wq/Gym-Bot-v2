import pandas as pd
from data_scaler import DataScaler
from activation_layer import ActivationLayer
from performance_tracker import PerformanceTracker
from loss_functions import LossFunctions
from activation_functions import ActivationFunctions
from network import Network
from data_scaler import DataScaler
from dense_layer import DenseLayer

SAVE = False

if __name__ == '__main__':
    # -----------get data---------------
    # read data from csv files
    caloriesFile = pd.read_csv(
        r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\datasets\calories.csv')
    exerciseFile = pd.read_csv(
        r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\datasets\exercise.csv')

    # turn data into arrays
    Y = list(caloriesFile['Calories'])
    Y = [[y] for y in Y]

    columns = exerciseFile.columns
    rows = len(exerciseFile[columns[0]])
    X = [[1 if exerciseFile[columns[1]][i] == 'male' else 0,
          exerciseFile[columns[2]][i],
          exerciseFile[columns[3]][i],
          exerciseFile[columns[4]][i],
          exerciseFile[columns[5]][i],
          exerciseFile[columns[6]][i]]
         for i in range(0, rows)]

    # normalize data
    yScaler = DataScaler(1)
    yScaler.fitData(Y)
    Y = yScaler.transformData(Y)
    Y = [y[0] for y in Y]

    xScaler = DataScaler(6)
    xScaler.fitData(X)
    X = xScaler.transformData(X)

    xTrain, xTest = X[:14000], X[14000:]
    yTrain, yTest = Y[:14000], Y[14000:]

    # ---------build and train neural network---------------
    network = Network()
    # input layer
    network.add(DenseLayer(6, 10))
    network.add(ActivationLayer(ActivationFunctions.sigmoid,
                ActivationFunctions.sigmoidPrime))

    # hidden layer
    network.add(DenseLayer(10, 15))
    network.add(ActivationLayer(ActivationFunctions.RELU,
                ActivationFunctions.RELUPrime))

    # output layer
    network.add(DenseLayer(15, 1))
    network.add(ActivationLayer(ActivationFunctions.sigmoid,
                ActivationFunctions.sigmoidPrime))

    network.setLoss(LossFunctions.mse, LossFunctions.msePrime)

    # train model and make predictions
    network.fit(xTrain, yTrain, 5, 0.1)
    predictions = network.predict(xTest)
    predictions = yScaler.inverseTransform([[p] for p in predictions])
    yTest = yScaler.inverseTransform([[t] for t in yTest])

    # get accuracy of model
    print(PerformanceTracker.getAverageAcuracy(yTest, predictions, False))

    # save model and predictors
    if SAVE:
        network.save(
            r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\models\calories_burned_predictor\model')
        xScaler.save(
            r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\models\calories_burned_predictor\x_scaler')
        yScaler.save(
            r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\models\calories_burned_predictor\y_scaler')
    
    print('Model and data scalers Saved')
