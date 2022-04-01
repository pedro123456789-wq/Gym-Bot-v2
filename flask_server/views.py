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

    #check if username or email are  already taken
    matching_usernames = User.query.filter_by(username = username).all()
    matching_emails = User.query.filter_by(email = email).all()


    if len(matching_usernames) > 0 or len(matching_emails) > 0:
        return customResponse(False, 'Username already taken')

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
    try:
        sendEmail(
            email, 
            'Gym Bot verification code', 
            f'Thank you for signing up.\nYour verification code is {confirmationCode}'
        )
    except Exception:
        print('Internal server failure')


    return customResponse(True, 'Account created')



@app.route('/api/cofirm-email', methods = ['PUT'])
def confirmEmail():
    data = request.get_json()

    #validate headers
    try:
        validate(instance = data, schema = validationSchemes.confirmEmailSchema)
    except exceptions.ValidationError as error:
        return customResponse(False, error.message)

    username, confirmationCode = data.get('username'), data.get('confirmationCode')

    #check if username is in database
    users = User.query.filter_by(username = username).all()

    if len(users) < 1:
        return customResponse(False, 'Username not in database')

    
    targetUser = users[0]
    targetCode = targetUser.confirmationCode

    #check if confirmation code is correct
    if targetCode == confirmationCode:
        targetUser.emailConfirmed = True 
        db.session.commit()

        return customResponse(True, 'Account was verified successfully')

    else:
        return customResponse(False, 'Incorred verification code')
    



    

    

    

    
    

    

