#local imports
from flask_server import app, db
from flask_server.models import User
from flask_server import encryptionHandler
from flask_server import validationSchemes
from flask_server.responses import customResponse
from flask_server.emailSender import sendEmail

#package imports 
from jsonschema import validate, exceptions
from flask import request, jsonify, make_response
from random import randint




@app.route('/api', methods = ['GET'])
def home():
    return 'Api is running ...'



@app.route('/api/sign-up', methods = ['POST'])
def signUp():
    data = request.get_json()

    #check if headers have valid data using json validation schemes
    try:
        validate(instance = data, schema = validationSchemes.signUpSchema)
    except exceptions.ValidationError as error:
        return customResponse(False, error.message)


    username, email, password = data.get('username'), data.get('email'), data.get('password')
    hashedPassword = encryptionHandler.generate_password_hash(password).decode('utf-8')

    #generate email confirmation code
    confirmationCode = randint(10000, 99999)

    newUser = User(
                    username = username, 
                    email = email, 
                    password = hashedPassword, 
                    confirmationCode = confirmationCode
                  )


    #save new user in database
    db.session.add(newUser)
    db.session.commit()


    #send email to user with confirmation code
    sendEmail(
        email, 
        'Gym Bot verification code', 
        f'Thank you for signing up.\nYour verification code is {confirmationCode}'
    )


    return customResponse(True, 'Account created')



@app.route('/api/cofirm-email', methods = ['PUT'])
def confirmEmail():
    data = request.get_json()
    
    

    

