from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS


SQLALCHEMY_TRACK_MODIFICATIONS = True


app = Flask(__name__)
cors = CORS(app)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'test_key' #change in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)
encryptionHandler = Bcrypt()

from flask_server import views
from flask_server import models 