from curses import delay_output
from requests import session
from flask_server.responses import customResponse
from flask_server.validationSchemes import sessionValidationSchema
from flask_server import app
from flask_server.models import User

from flask import request
from jsonschema import validate, exceptions
from functools import wraps
import jwt
from datetime import datetime


def loginRequired(methods = None):
    if methods == None: methods = []

    def wrapper(function):
        @wraps(function)
        def decorated(*args, **kwargs):
            if request.method in methods:
                data = request.get_json()

                #check if headers are valid with json schema
                try:
                    validate(data, schema = sessionValidationSchema)
                except exceptions.ValidationError as error:
                    return customResponse(False, error.message)

                username, token = data.get('username'), data.get('token')

                #check if token is valid and has not expired
                try:
                    decodedToken = jwt.decode(token, app.config['SECRET_KEY'])
                    tokenUsername, tokenExpiration = decodedToken.get('user'), decodedToken.get('exp')

                    if tokenUsername != username:
                        return customResponse(False, 'Token does not match username')
                    elif datetime.fromtimestamp(tokenExpiration) < datetime.now():
                        return customResponse(False, 'Token has expired')
                except Exception:
                    return customResponse(False, 'Invalid token')

            return function(*args, **kwargs)
        return decorated    
    return wrapper




def profileRequired(methods = []):
    def wrapper(function):
        @wraps(function)
        def decorated(*args, **kwargs):
            if request.method in methods:
                data = request.get_json()
                username = data.get('username')

                if username == None:
                    return customResponse(False, 'Missing username')

                targetUser = User.query.filter_by(username = username).first()
                accountFields = [
                                    'caloriesEatenTarget', 
                                    'caloriesBurnedTarget', 
                                    'minutesTrainedTarget', 
                                    'distanceRanTarget', 
                                    'height', 
                                    'weight', 
                                    'gender',
                                    'age'
                                ]  

                #check if user has set up profile
                for field in accountFields:
                    if eval(f'targetUser.{field}') == None:
                        return customResponse(False, f'Profile Error')
            
            return function(*args, **kwargs)
        return decorated
    return wrapper

                
