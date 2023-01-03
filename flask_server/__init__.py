from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
import sys

from flask_server.neural_network.network import Network
from flask_server.neural_network.data_scaler import DataScaler
from flask_server.neural_network import network

# global path variables
HOME_PATH = 'C:/Users/pl156/Documents/schoolwork/Computer Science A-Level/gym_bot_v2/flask_server/'
NEURAL_NETWORK_PATH = 'C:/Users/pl156/Documents/schoolwork/Computer Science A-Level/gym_bot_v2/flask_server/neural_network'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# initialise flask application
app = Flask(__name__)
cors = CORS(app, supports_credentials = True)

# app configuration 
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'test_key' #change in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JSON_SORT_KEYS'] = False
app.config['URL'] = 'http://localhost:8080'

# create database and link it to alembic
db = SQLAlchemy(app)
migrate = Migrate(app, db)
encryptionHandler = Bcrypt()


# load body fat prediction model and scalers
print('Loading Body fat prediction model ...')
sys.path.insert(0, NEURAL_NETWORK_PATH)
MODELS_PATH = 'C:/Users/pl156/Documents/schoolwork/Computer Science A-Level/gym_bot_v2/flask_server/models/'

bodyFatPredictor = Network()
bodyFatPredictor.load(f'{MODELS_PATH}/body_fat_predictor/model')

bodyFatScalerX = DataScaler(4)
bodyFatScalerX.load(f'{MODELS_PATH}/body_fat_predictor/x_scaler')

bodyFatScalerY = DataScaler(1)
bodyFatScalerY.load(f'{MODELS_PATH}/body_fat_predictor/y_scaler')
print('Loaded body fat prediction model')


# load calories burned prediction model
print('Loading calories burned prediction model ...')
caloriesBurnedPredictor = Network()
caloriesBurnedPredictor.load(f'{MODELS_PATH}/calories_burned_predictor/model')

caloriesBurnedScalerX = DataScaler(6)
caloriesBurnedScalerX.load(f'{MODELS_PATH}/calories_burned_predictor/x_scaler')

caloriesBurnedScalerY = DataScaler(1)
caloriesBurnedScalerY.load(f'{MODELS_PATH}/calories_burned_predictor/y_scaler')
print('Loaded calories burned prediction model')



sys.path.insert(0, HOME_PATH)
from flask_server import views
from flask_server import models 