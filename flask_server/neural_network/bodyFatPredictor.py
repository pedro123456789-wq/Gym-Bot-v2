import pandas as pd
from dense_layer import DenseLayer
from activation_layer import ActivationLayer
from performance_tracker import PerformanceTracker
from layer import Layer
from loss_functions import LossFunctions
from activation_functions import ActivationFunctions
from network import Network
from data_scaler import DataScaler




SAVE = True  


if __name__ == '__main__':
    data = pd.read_csv(r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\datasets\bodyfat.csv')
    headers = data.columns
    rows = len(data[headers[0]])

    #parameters being used: weight chest abdomen and hip measurements
    Y = [[data[headers[1]][i]] for i in range(0, rows)]
    X = [[data[headers[3]][i], 
          data[headers[6]][i], 
          data[headers[7]][i], 
          data[headers[8]][i]]
        for i in range(0, rows)]

    yScaler = DataScaler(1)
    yScaler.fitData(Y)
    convertedY = yScaler.transformData(Y)
    
    print(f'Y: {len(convertedY)}')

    xScaler = DataScaler(4)
    xScaler.fitData(X)
    convertedX = xScaler.transformData(X)
    print(f'X: {len(convertedX)}')

    convertedY = [y[0] for y in convertedY] #flatten array

    # build network model:
    #     input layer with 4 neurons
    #     two hidden layers with 10 neurons each
    #     output layer with one neuron and sigmoid activation function 


    network = Network()
    network.add(DenseLayer(4, 10))
    network.add(ActivationLayer(ActivationFunctions.RELU, ActivationFunctions.RELUPrime))
    network.add(DenseLayer(10, 10))
    network.add(ActivationLayer(ActivationFunctions.RELU, ActivationFunctions.RELUPrime))
    network.add(DenseLayer(10, 10))
    network.add(ActivationLayer(ActivationFunctions.RELU, ActivationFunctions.RELUPrime))
    network.add(DenseLayer(10, 1))
    network.add(ActivationLayer(ActivationFunctions.sigmoid, ActivationFunctions.sigmoidPrime))

    network.setLoss(LossFunctions.mse, LossFunctions.msePrime)
    
    print('Training network ...')
    network.fit(convertedX, convertedY, 10, 0.1, showLogs = True)

    #test accuracy of network
    print(type(convertedX))
    predictions = network.predict(convertedX)
    predictions = yScaler.inverseTransform([[prediction] for prediction in predictions]) 
    print(PerformanceTracker.getAverageAcuracy(Y, predictions, False))

    #save network and scalers
    if SAVE:    
        network.save(r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\models\body_fat_predictor\model')
        xScaler.save(r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\models\body_fat_predictor\x_scaler')
        yScaler.save(r'C:\Users\pl156\Documents\schoolwork\Computer Science A-Level\gym_bot_v2\flask_server\models\body_fat_predictor\y_scaler')
        print('Model Saved')