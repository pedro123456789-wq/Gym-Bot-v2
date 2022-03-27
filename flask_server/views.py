#local imports
from flask_server import app, db
from flask_server.models import User
from flask_server import encryptionHandler
from flask_server import validationSchemes
from flask_server.responses import custom_response

#package imports 
from jsonschema import validate, exceptions
from flask import request, jsonify, make_response




@app.route('/api', methods = ['GET'])
def home():
    return 'Api is running ...'



@app.route('/api/sign-up', methods = ['POST'])
def sign_up():
    data = request.get_json()

    #check if headers have valid data
    try:
        validate(instance = data, schema = validationSchemes.signUpSchema)
    except exceptions.ValidationError as error:
        return custom_response(False, error.message)


    username, email, password = data.get('username'), data.get('email'), data.get('password')
    hashedPassword = encryptionHandler.generate_password_hash(password).decode('utf-8')

    newUser = User(
                    username = username, 
                    email = email, 
                    password = hashedPassword
                  )

    db.session.add(newUser)
    db.session.commit()

    return custom_response(True, 'Account added to database')
    

    

