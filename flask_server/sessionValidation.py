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


def loginRequired(methods=None):
    if methods == None:
        methods = []

    def wrapper(function):
        @wraps(function)
        def decorated(*args, **kwargs):
            if request.method in methods:
                # if request method is GET, the login data will be sent as headers, not in the request body
                if request.method != 'GET':
                    data = request.get_json()

                    # check if headers are valid with json schema
                    try:
                        validate(data, schema=sessionValidationSchema)
                    except exceptions.ValidationError as error:
                        return customResponse(False, error.message)

                    username, token = data.get('username'), data.get('token')
                else:
                    headers = request.headers
                    username, token = headers.get('username'), headers.get('token')

                    if username == None or token == None:
                        return customResponse(False, 'Missing required headers')

                # check if token is valid and has not expired
                try:
                    decodedToken = jwt.decode(token, app.config['SECRET_KEY'])
                    tokenUsername, tokenExpiration = decodedToken.get(
                        'user'), decodedToken.get('exp')

                    if tokenUsername != username:
                        return customResponse(False, 'Token does not match username')
                    elif datetime.fromtimestamp(tokenExpiration) < datetime.now():
                        return customResponse(False, 'Token has expired')
                except Exception:
                    return customResponse(False, 'Invalid token')

            return function(*args, **kwargs)
        return decorated
    return wrapper
  

def hasProfile(targetUser: User):
    # check if user has set up profile
    for field in accountFields:
        if eval(f'targetUser.{field}') == None:
            return False

    return True


def profileRequired(methods=[]):
    def wrapper(function):
        @wraps(function)
        def decorated(*args, **kwargs):
            if request.method in methods:

                if request.method != 'GET':
                    data = request.get_json()
                    username = data.get('username')
                else:
                    headers = request.headers
                    username = headers.get('username')

                if username == None:
                    return customResponse(False, 'Missing username')

                targetUser = User.query.filter_by(username=username).first()

                # check if user is in database
                if targetUser == None:
                    return customResponse(False, 'User not found')

                if not hasProfile(targetUser):
                    return customResponse(False, 'Profile Error')

            return function(*args, **kwargs)
        return decorated
    return wrapper
