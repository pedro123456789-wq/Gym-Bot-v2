'''Loss Functions'''


class LossFunctions:
    @staticmethod
    def mse(yTrue, yPred):
        return (yTrue - yPred) ** 2

    def msePrime(yTrue, yPred):
        return 2 * (yPred - yTrue)