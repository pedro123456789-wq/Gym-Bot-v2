from dense_layer import DenseLayer
from activation_layer import ActivationLayer
from activation_functions import ActivationFunctions
from loss_functions import LossFunctions
from network import Network


if __name__ == '__main__':
    xTrain = [[0, 0], [0, 1], [1, 0], [1, 1]]
    yTrain = [0, 1, 1, 0]

    network = Network()
    network.add(DenseLayer(2, 3))
    network.add(ActivationLayer(ActivationFunctions.tanh, ActivationFunctions.tanhPrime))
    network.add(DenseLayer(3, 1))
    network.add(ActivationLayer(ActivationFunctions.tanh, ActivationFunctions.tanhPrime))

    network.setLoss(LossFunctions.mse, LossFunctions.msePrime)
    network.fit(xTrain, yTrain, 1000, 0.3, showLogs = True)
        
    print(list(map(lambda i : round(i), network.predict(xTrain))))


