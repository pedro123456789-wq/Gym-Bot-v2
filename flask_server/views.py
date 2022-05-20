#local imports
from flask_server import app, db
from flask_server.models import User, Food, Workout, Exercise, food_record, workout_exercise
from flask_server import encryptionHandler, bodyFatPredictor, bodyFatScalerY, bodyFatScalerX
from flask_server import validationSchemes
from flask_server.responses import customResponse
from flask_server.emailSender import sendEmail
from flask_server.sessionValidation import loginRequired, profileRequired

#package imports 
from jsonschema import validate, exceptions
from flask import request
from random import randint
import jwt
from datetime import datetime, timedelta
import numpy as np




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
            '\n'.join(['Thank you for signing up', 
                       f'Your verification code is: {confirmationCode}', 
                       f'Verify your email at: {app.config["URL"]}/verify-email'
                    ])
        )
    except Exception:
        print('Internal server failure')

    return customResponse(True, 'Account created')




@app.route('/api/confirm-email', methods = ['PUT'])
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
        return customResponse(False, 'Incorrect verification code')




@app.route('/api/log-in', methods = ['POST'])
def log_in():
    data = request.get_json()

    try:
        validate(instance = data, schema = validationSchemes.loginSchema)
    except exceptions.ValidationError as error:
        return customResponse(False, error.message)

    username, password = data.get('username'), data.get('password')
    targetUser = User.query.filter_by(username = username).first()   

    if targetUser:
        targetPassword = targetUser.password

        if not targetUser.emailConfirmed:
            return customResponse(False, 'We sent you a verification code. Please check your email')

        if encryptionHandler.check_password_hash(targetPassword, password):
            token = jwt.encode({'user' : username, 'exp' : datetime.utcnow() + timedelta(minutes = 60)}, app.config['SECRET_KEY']).decode('utf-8')            
            return customResponse(True, 'Login successful', token = str(token))
        else:
            return customResponse(False, 'Incorrect password')
    
    else:
        return customResponse(False, 'Account does not exist')




@app.route('/api/check-session', methods = ['POST'])
@loginRequired(methods = ['POST'])
@profileRequired(methods = ['POST'])
def checkSession():
    data = request.get_json()
    username = data.get('username')

    return customResponse(True, f'Session is valid for {username}')




#need to check if user already has profile
#display pop up for errors
#make error messages and labels more user friendly
@app.route('/api/profile', methods = ['GET', 'POST', 'PUT'])
@loginRequired()
@profileRequired(['GET', 'PUT'])
def profile():
    headerBounds = validationSchemes.profileBounds
    data = request.get_json()
    username = data.get('username')
    targetUser = User.query.filter_by(username = username).first()

    #get profile data 
    if request.method == 'GET':
        output = {field : eval(f'targetUser.{field}') 
                  for field in validationSchemes.profileSchema['required']}

        return customResponse(True, 'Fetched Data Successfully', data = output)


    #create profile by adding values to all null fields
    elif request.method == 'POST':
        #check if all required headers are present 
        try:
            validate(instance = data, schema = validationSchemes.profileSchema)
        except exceptions.ValidationError as error:
            return customResponse(False, error.message)

        #check if all values are within bounds
        for header in list(headerBounds):
            if data[header] > headerBounds[header]['max'] or data[header] < headerBounds[header]['min']:
                return customResponse(False, f'Value for {header} is not valid')

        #update user table with new values 
        for header in list(data.keys()):
            if header != 'username' and header != 'token': 
                exec(f'targetUser.{header} = {data[header]}')

        #save changes
        db.session.commit()
        return customResponse(True, 'Profile created')


    #update profile data
    elif request.method == 'PUT':       
        #check if all new values are in bounds
        for header in list(data.keys()):
            if data[header] > headerBounds[header]['max'] or data[header] < headerBounds[header]['min']:
                return customResponse(False, f'Value for {header} is not valid')

        #only set new values if all values provided are valid
        #this has impact on performance but ensures that transactions are atomic
        for header in list(data.keys()):
            if header != 'username' and header != 'token':
                exec(f'targetUser.{header} = {data[header]}')

        return customResponse(True, 'Data Updated')




@app.route('/api/food', methods = ['POST', 'GET'])
@loginRequired(methods = ['POST', 'GET'])
@profileRequired(methods = ['POST', 'GET'])
def food():
    data = request.get_json()
    username = data.get('username')
    targetUser = User.query.filter_by(username = username).first()

    if request.method == 'GET':
        startDate = data.get('startDate')
        endDate = data.get('endDate')

        #convert start and end date of db query into timestamps
        try:
            dateFormat = '%d/%m/%Y'
            startTs, endTs = datetime.strptime(startDate, dateFormat), datetime.strptime(endDate, dateFormat)
        except Exception:
            return customResponse(False, 'Invalid date format')


        #query food_record table (junction table) to find entries which have the user id of target user and have timestamp between start and end ts
        foodRecordQuery = db.session.query(food_record).filter((food_record.c.user_id == targetUser.id) &
                                                               (food_record.c.timestamp <= endTs) &
                                                               (food_record.c.timestamp >= startTs)).all()

        #get ids from the items returned in the query
        foodIds = [field.food_id for field in foodRecordQuery]

        #return list of foods with ids in foodIds
        foodItems = [{'name' : item.name,
                      'calories' : item.calories, 
                      'fat' : item.fat,
                      'carboHydrates' : item.carboHydrates, 
                      'protein' : item.protein
                      } for item in Food.query.all() if item.id in foodIds]

        return customResponse(True, 'Got Data', data = foodItems)
                                

    elif request.method == 'POST':
        #check if headers are valid
        try:
            validate(instance = data, schema = validationSchemes.foodSchema)
        except exceptions.ValidationError as error:
            return customResponse(False, error.message)

        foodName, calories, fat, carboHydrates, protein = data.get('foodName'), data.get('calories'), data.get('fat'), data.get('carboHydrates'), data.get('protein')
        
        #check if food item already exists
        itemMatches = Food.query.filter_by(name = foodName,
                                           calories = calories, 
                                           fat = fat, 
                                           carboHydrates = carboHydrates, 
                                           protein = protein
                                          ).all()

        if len(itemMatches) > 0:
            item = itemMatches[0]
        else:
            item = Food(name = foodName,
                        calories = calories, 
                        fat = fat,
                        carboHydrates = carboHydrates, 
                        protein = protein
                       )
            
            db.session.add(item)
            db.session.flush()

        
        #add entry to junction table between user and food item with corresponding primary keys
        insertionStatement = food_record.insert().values(user_id = targetUser.id, food_id = item.id)
        db.session.execute(insertionStatement)
        db.session.commit()

        return customResponse(True, 'New food record added to database')
    

    elif request.method == 'PUT':
        #delete or edit records
        pass




@app.route('/api/workouts', methods = ['GET', 'POST', 'PUT'])
@loginRequired(methods = ['GET', 'POST', 'PUT'])
@profileRequired(methods = ['GET', 'POST', 'PUT'])
def workouts():
    data = request.get_json()
    username = data.get('username')
    targetUser = User.query.filter_by(username = username).first()

    if request.method == 'GET':
        workouts = Workout.query.filter_by(user_id = targetUser.id).all()
        output = []

        for workout in workouts:
            exercises = []
            pass

            #iterate through the exercises in each workout and add them to exercises

    elif request.method == 'POST':
        '''Create new workout'''

        #check if request has valid headers
        try:
            validate(instance = data, schema = validationSchemes.workoutsSchema)
        except exceptions.ValidationError as error:
            return customResponse(False, error.message)

        #create new entry in workout table
        newWorkout = Workout(name = data.get('name'))
        db.session.add(newWorkout)
        db.session.flush()
        
        #link new entry to target user using foreign key
        targetUser.workouts.append(newWorkout)
        db.session.commit()
        

    elif request.method == 'PUT':
        '''Modify or delete workouts'''

        #append exercises to an workout
        exerciseList, workoutName, action = data.get('exercises'), data.get('workoutName'), data.get('action')
        
        #check if all headers are present
        if not exerciseList or not workoutName or not action:
            return customResponse(False, 'Missing required headers')

        #validate each exercise in the exercise list 
        for exercise in exerciseList:
            try:
                validate(instance = exercise, schema = validationSchemes.exerciseSchema)
            except exceptions.ValidationError as error:
                return customResponse(False, error.message)

        #check if workout exists
        targetWorkout = Workout.query.filter_by(name = workoutName).first()

        if not targetWorkout:
            return customResponse(False, 'Workout does not exist')


        if action == 'ADD EXERCISES':
            #either add all exercises or do not add any, hence the use of two loops is permited
            for exercise in exerciseList:
                name, duration, repetitions = exercise.get('name'), exercise.get('durationSeconds'), repetitions = exercise.get('repetitions')

                newExercise = Exercise(name = name, 
                                    durationSeconds = duration, 
                                    repetitions = repetitions)
                
                #add new entry to exercise table
                db.session.add(newExercise)
                db.session.flush()

                #add new entry to junction table for workout and exercises
                insertionStatement = workout_exercise.insert().values(workout_id = targetWorkout.id, exercise_id = newExercise.id)
                db.session.execute(insertionStatement)
            
            #commit changes
            db.session.commit()
        

        elif action == 'REMOVE WORKOUT':
            pass


        elif action == 'REMOVE EXERCISE':
            pass





@app.route('/api/body-fat-prediction', methods = ['GET'])
@loginRequired(methods = ['GET'])
@profileRequired(methods = ['GET'])
def bodyFat():
    data = request.get_json()

    #check if all required headers are present
    try:
        validate(instance = data, schema = validationSchemes.bodyFatPredictionSchema)
    except exceptions.ValidationError as error:
        return customResponse(False, error.message)

    #check if all headers have valid values
    for header in list(data.keys()):
        if header != 'token' and header != 'username':
            if float(data[header]) < 0 or float(data[header]) > 1000:
                return customResponse(f'The value for {header} is invalid', False)

    
    #scale inputs
    X = np.array(list(map(float, [data.get('weight'), data.get('chest'), data.get('abdomen'), data.get('hip')])))
    X = bodyFatScalerX.transformData(X)
    X = X.reshape(1, 1, 4)

    #use neural network to make predictions
    prediction = bodyFatPredictor.predict(X)
    rediction = bodyFatScalerY.inverseTransform(prediction)

    return customResponse(True, 'Successful prediction', prediction = prediction)




@app.route('/api/daily-data', methods = ['GET'])
@loginRequired(methods = ['GET'])
@profileRequired(methods = ['GET'])
def getDailyData():
    data = requests.get_json()
    username = data.get('username')
    targetDate = data.get('date')
    targetUser = User.query.filter_by(username = username).first()

    try:
        dateFormat = '%d/%m/%Y'
        targetDate = datetime.strptime(startDate, dateFormat)
    except Exception:
        return customResponse(False, 'Invalid date format')

    #get calories eaten in target date 
    foodRecordQuery = db.session.query(food_record).filter((food_record.c.user_id == targetUser.id) &
                                                           (food_record.c.timestamp.day == targetDate.day)).all()

    foodIds = [field.food_id for field in foodRecordQuery]
    calories = sum([int(item.calories), for item in Food.query.all() if item.id in foodIds])


    #get total time trained for target date
    workouts = Workout.query.filter_by(user_id = targetUser.id).all()
    totalDurationMinutes = sum([int(workout.durationSeconds) for workout in workouts]) / 60

    return customResponse(True, 'Got data successfully', calories = calories, timeTrained = totalDurationMinutes)



#use garmin connect to get garmin data from watch
