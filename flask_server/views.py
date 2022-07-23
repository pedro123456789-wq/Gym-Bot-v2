# local imports
from flask_server import app, db
from flask_server.models import User, Food, Workout, Exercise, Run, food_record, workout_exercise
from flask_server import encryptionHandler, bodyFatPredictor, bodyFatScalerY, bodyFatScalerX
from flask_server import validationSchemes
from flask_server.responses import customResponse
from flask_server.emailSender import sendEmail
from flask_server.sessionValidation import loginRequired, profileRequired, hasProfile, accountFields

# package imports
from jsonschema import validate, exceptions
from flask import request
from random import randint
import jwt
from datetime import datetime, timedelta
import numpy as np


@app.route('/api', methods=['GET'])
def home():
    return 'Api is running ...'


@app.route('/api/sign-up', methods=['POST'])
def signUp():
    data = request.get_json()

    # check if headers have valid data using json validation schemes
    try:
        validate(instance=data, schema=validationSchemes.signUpSchema)
    except exceptions.ValidationError as error:
        return customResponse(False, error.message)

    username, email, password = data.get(
        'username'), data.get('email'), data.get('password')
    hashedPassword = encryptionHandler.generate_password_hash(
        password).decode('utf-8')

    # check if username or email are  already taken
    matching_usernames = User.query.filter_by(username=username).all()
    matching_emails = User.query.filter_by(email=email).all()

    if len(matching_usernames) > 0:
        return customResponse(False, 'Username already taken')

    if len(matching_emails) > 0:
        return customResponse(False, 'Email is already taken')

    # generate email confirmation code
    confirmationCode = randint(10000, 99999)

    newUser = User(
        username=username,
        email=email,
        password=hashedPassword,
        confirmationCode=confirmationCode
    )

    # save new user in database
    db.session.add(newUser)
    db.session.commit()

    # send email to user with confirmation code
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


@app.route('/api/confirm-email', methods=['PUT'])
def confirmEmail():
    data = request.get_json()

    # validate headers
    try:
        validate(instance=data, schema=validationSchemes.confirmEmailSchema)
    except exceptions.ValidationError as error:
        return customResponse(False, error.message)

    username, confirmationCode = data.get(
        'username'), data.get('confirmationCode')

    # check if username is in database
    users = User.query.filter_by(username=username).all()

    if len(users) < 1:
        return customResponse(False, 'Username not in database')

    targetUser = users[0]
    targetCode = targetUser.confirmationCode

    # check if confirmation code is correct
    if targetCode == confirmationCode:
        targetUser.emailConfirmed = True
        db.session.commit()

        return customResponse(True, 'Account was verified successfully')

    else:
        return customResponse(False, 'Incorrect verification code')


@app.route('/api/log-in', methods=['POST'])
def log_in():
    data = request.get_json()

    try:
        validate(instance=data, schema=validationSchemes.loginSchema)
    except exceptions.ValidationError as error:
        return customResponse(False, error.message)

    username, password = data.get('username'), data.get('password')
    targetUser = User.query.filter_by(username=username).first()

    if targetUser:
        targetPassword = targetUser.password

        if not targetUser.emailConfirmed:
            return customResponse(False, 'We sent you a verification code. Please check your email')

        if encryptionHandler.check_password_hash(targetPassword, password):
            token = jwt.encode({'user': username, 'exp': datetime.utcnow(
            ) + timedelta(minutes=60)}, app.config['SECRET_KEY']).decode('utf-8')
            return customResponse(True, 'Login successful', token=str(token))
        else:
            return customResponse(False, 'Incorrect password')

    else:
        return customResponse(False, 'Account does not exist')


@app.route('/api/check-session', methods=['POST'])
@loginRequired(methods=['POST'])
@profileRequired(methods=['POST'])
def checkSession():
    data = request.get_json()
    username = data.get('username')

    return customResponse(True, f'Session is valid for {username}')


@app.route('/api/has-profile', methods=['POST'])
@loginRequired(methods=['POST'])
def checkProfile():
    # check if user has profile to decide wether profile creation page should be displayed or not
    data = request.get_json()
    targetUser = User.query.filter_by(username=data.get('username')).first()

    if hasProfile(targetUser):
        return customResponse(False, 'User already has profile')
    else:
        return customResponse(True, 'User can create new profile')


@app.route('/api/profile', methods=['GET', 'POST', 'PUT'])
@loginRequired(['GET', 'POST', 'PUT'])
@profileRequired(['GET', 'PUT'])
def profile():
    headerBounds = validationSchemes.profileBounds

    if request.method == 'POST' or request.method == 'PUT':
        data = request.get_json()
        targetUser = User.query.filter_by(
            username=data.get('username')).first()
    else:
        targetUser = User.query.filter_by(
            username=request.headers.get('username')).first()

    # get profile data
    if request.method == 'GET':
        # get class attributes from target user and return them in a dictionary
        output = vars(targetUser)
        output.pop('_sa_instance_state')

        return customResponse(True, 'Fetched Data Successfully', data=output)

    # create profile by adding values to all null fields
    elif request.method == 'POST':
        # check if all required headers are present
        try:
            validate(instance=data, schema=validationSchemes.profileSchema)
        except exceptions.ValidationError as error:
            return customResponse(False, error.message)

         # check if user already has a profile
         # has profile end-point is not enough has users may send requests without browser
        if hasProfile(targetUser):
            return customResponse(False, 'You already have a profile')

        # check if all values are within bounds
        for header in list(headerBounds):
            if data[header] > headerBounds[header]['max'] or data[header] < headerBounds[header]['min']:
                return customResponse(False, f'Value for {header} is not valid')

        # update user table with new values
        for header in list(data.keys()):
            if header != 'username' and header != 'token':
                exec(f'targetUser.{header} = {data[header]}')

        # save changes
        db.session.commit()
        return customResponse(True, 'Profile created')

    # update profile data
    elif request.method == 'PUT':
        # check if all new values are in bounds
        for header in list(data.keys()):
            if header != 'username' and header != 'token' and header != 'email' and header != 'password':
                if data[header] > headerBounds[header]['max'] or data[header] < headerBounds[header]['min']:
                    return customResponse(False, f'Value for {header} is not valid')

        # only set new values if all values provided are valid
        # this has impact on performance but ensures that transactions are atomic
        for header in list(data.keys()):
            if header != 'username' and header != 'token':
                exec(f'targetUser.{header} = {data[header]}')

        db.session.commit()

        return customResponse(True, 'Data Updated')


@app.route('/api/food', methods=['POST', 'GET'])
@loginRequired(methods=['POST', 'GET'])
@profileRequired(methods=['POST', 'GET'])
def food():
    # get requests recieve data through headers while other requests get data through json payload
    if request.method != 'GET':
        data = request.get_json()
        username = data.get('username')
        targetUser = User.query.filter_by(username=username).first()

    if request.method == 'GET':
        startDate = request.headers.get('startDate')
        endDate = request.headers.get('endDate')
        targetUser = User.query.filter_by(
            username=request.headers.get('username')).first()

        # convert start and end date of db query into timestamps
        try:
            dateFormat = '%d/%m/%Y'

            if endDate == '+1':
                startTs = datetime.strptime(startDate, dateFormat)
                endTs = startTs + timedelta(days=1)
            else:
                startTs, endTs = datetime.strptime(
                    startDate, dateFormat), datetime.strptime(endDate, dateFormat)
        except Exception as e:
            print(e)
            return customResponse(False, 'Invalid date format')

        # query food_record table (junction table) to find entries which have the user id of target user and have timestamp between start and end ts
        foodRecordQuery = db.session.query(food_record).filter((food_record.c.user_id == targetUser.id) &
                                                               (food_record.c.timestamp <= endTs) &
                                                               (food_record.c.timestamp >= startTs)).all()

        # get ids from the items returned in the query
        foodIds = [field.food_id for field in foodRecordQuery]

        # return list of foods with ids in foodIds
        foodItems = [{'name': item.name,
                      'calories': item.calories,
                      'fat': item.fat,
                      'carboHydrates': item.carboHydrates,
                      'protein': item.protein
                      } for item in Food.query.all() if item.id in foodIds]

        return customResponse(True, 'Got Data', data=foodItems)

    elif request.method == 'POST':
        # check if headers are valid
        try:
            validate(instance=data, schema=validationSchemes.foodSchema)
        except exceptions.ValidationError as error:
            return customResponse(False, error.message)

        foodName, calories, fat, carboHydrates, protein = data.get('foodName'), data.get(
            'calories'), data.get('fat'), data.get('carboHydrates'), data.get('protein')

        # check if food item already exists
        itemMatches = Food.query.filter_by(name=foodName,
                                           calories=calories,
                                           fat=fat,
                                           carboHydrates=carboHydrates,
                                           protein=protein
                                           ).all()

        if len(itemMatches) > 0:
            item = itemMatches[0]
        else:
            item = Food(name=foodName,
                        calories=calories,
                        fat=fat,
                        carboHydrates=carboHydrates,
                        protein=protein
                        )

            db.session.add(item)
            db.session.flush()

        # add entry to junction table between user and food item with corresponding primary keys
        insertionStatement = food_record.insert().values(
            user_id=targetUser.id, food_id=item.id)
        db.session.execute(insertionStatement)
        db.session.commit()

        return customResponse(True, 'New food record added to database')

    elif request.method == 'PUT':
        # delete or edit records
        pass


@app.route('/api/workouts', methods=['GET', 'POST', 'PUT'])
@loginRequired(methods=['GET', 'POST', 'PUT'])
@profileRequired(methods=['GET', 'POST', 'PUT'])
def workouts():
    if request.method != 'GET':
        data = request.get_json()
        username = data.get('username')
        targetUser = User.query.filter_by(username=username).first()

    if request.method == 'GET':
        targetUser = User.query.filter_by(username=request.headers.get('username')).first()
        targetWorkouts = request.headers.get('targetWorkouts')
        startDate = request.headers.get('startDate')
        endDate = request.headers.get('endDate')

        # convert start and end date of db query into timestamps
        try:
            dateFormat = '%d/%m/%Y'

            if endDate == '+1':
                startTs = datetime.strptime(startDate, dateFormat)
                endTs = startTs + timedelta(days=1)
            else:
                startTs, endTs = datetime.strptime(
                    startDate, dateFormat), datetime.strptime(endDate, dateFormat)
        except Exception as e:
            return customResponse(False, 'Invalid date format')

        # check if targetWorkouts is valid
        if not targetWorkouts:
            return customResponse(False, 'Missing required headers')

        workouts = targetUser.workouts
        if targetWorkouts == 'ALL':
            targetWorkouts = [workout.name for workout in workouts]

        if type(targetWorkouts) != list:
            return customResponse(False, 'Invalid format for workout list')

        # fetch list of all workouts saved by target user
        # workouts must be within the given date range and names must be in the targetWorkouts list

        # iterate through all workouts
        # for each workout append a dictionary with its names and its exercises
        # for each exercise create dictionary with its field values

        savedWorkouts = [
            {
                'name': workout.name,
                'caloriesBurned': workout.caloriesBurned,
                'exercises': [
                    {field.name: str(getattr(exercise, field.name))
                     for field in exercise.__table__.columns}
                    for exercise in workout.exercises
                ]
            }

            for workout in workouts if workout.name in targetWorkouts
            and workout.completionDate <= endTs
            and workout.completionDate >= startTs
        ]

        return customResponse(True, 'Fetched saved workouts successfully', workouts=savedWorkouts)

    elif request.method == 'POST':
        '''Create new workout'''

        # check if request has valid headers
        try:
            validate(instance=data, schema=validationSchemes.workoutsSchema)
        except exceptions.ValidationError as error:
            return customResponse(False, error.message)

        # create new entry in workout table
        newWorkout = Workout(name=data.get('name'), caloriesBurned=data.get('caloriesBurned'))
        db.session.add(newWorkout)
        db.session.flush()

        # link new entry to target user using foreign key
        targetUser.workouts.append(newWorkout)
        db.session.flush()

        '''Add exercises to newly created workout'''
        exerciseList = data.get('exercises')

        if type(exerciseList) != list:
            return customResponse(False, 'Invalid exercise list')

        if len(exerciseList) > 30:
            return customResponse(False, 'Exceeded exercise limit')

        # validate each exercise in the exercise list
        for exercise in exerciseList:
            try:
                validate(instance=exercise,
                         schema=validationSchemes.exerciseSchema)
            except exceptions.ValidationError as error:
                return customResponse(False, error.message)

        # create exercises and link them to new workout
        for exercise in exerciseList:
            name, duration, repetitions = exercise.get('name'), exercise.get(
                'durationSeconds'),  exercise.get('repetitions')

            # check if exercise already exists to save space in database
            matchingExercise = Exercise.query.filter_by(
                name=name, durationSeconds=duration, repetitions=repetitions).first()

            if matchingExercise:
                newExercise = matchingExercise
            else:
                # if exercise does not exist create new exercise
                newExercise = Exercise(name=name,
                                       durationSeconds=duration,
                                       repetitions=repetitions)

            # add new entry to exercise table
            db.session.add(newExercise)
            db.session.flush()

            # add new entry to junction table for workout and exercise
            insertionStatement = workout_exercise.insert().values(
                workout_id=newWorkout.id, exercise_id=newExercise.id)
            db.session.execute(insertionStatement)

        # save changes to database
        db.session.commit()
        return customResponse(True, 'Added new workout')


@app.route('/api/runs', methods=['GET', 'POST', 'PUT'])
@loginRequired(methods=['GET', 'POST', 'PUT'])
@profileRequired(methods=['GET', 'POST', 'PUT'])
def runs():
    if request.method != 'GET':
        data = request.get_json()
        targetUser = User.query.filter_by(
            username=data.get('username')).first()

    if request.method == 'GET':
        targetUser = User.query.filter_by(
            username=request.headers.get('username')).first()
        startDate = request.headers.get('startDate')
        endDate = request.headers.get('endDate')

        try:
            dateFormat = '%d/%m/%Y'
            
            if endDate == '+1':
                startTs = datetime.strptime(startDate, dateFormat)
                endTs = startTs + timedelta(days=1)
            else:
                startTs, endTs = datetime.strptime(startDate, dateFormat), datetime.strptime(endDate, dateFormat)
        except:
            return customResponse(False, 'Invalid Date format')


        targetRuns = Run.query.filter((Run.completionDate <= endTs) & (
            Run.completionDate >= startTs) & (Run.userId == targetUser.id)).all()

        outputDict = {
            'runNumber': len(targetRuns),
            'runs': [{
                'distance': run.distance,
                'duration': run.durationSeconds,
                'caloriesBurned': run.caloriesBurned,
                'completionDate': run.completionDate.strftime(dateFormat)
            } for run in targetRuns]
        }

        return customResponse(True, 'Got run data successfully', data=outputDict)

    elif request.method == 'POST':
        # add new run to database

        try:
            validate(instance=data, schema=validationSchemes.runSchema)
        except exceptions.ValidationError as error:
            return customResponse(False, error.message)

        distance, durationSeconds, caloriesBurned = data.get(
            'distance'), data.get('durationSeconds'), data.get('caloriesBurned')

        newRun = Run(distance=distance, durationSeconds=durationSeconds,
                     caloriesBurned=caloriesBurned)
        targetUser.runs.append(newRun)

        db.session.add(newRun)
        db.session.commit()

        return customResponse(True, 'Run saved successfully')

    elif request.method == 'PUT':
        # change data in database:
        # delete run
        # edit run
        pass



@app.route('/api/daily-data', methods = ['GET'])
@loginRequired(methods = ['GET'])
@profileRequired(methods = ['GET'])
def dailyData():
    headers = request.headers
    targetUser = User.query.filter_by(username = headers.get('username')).first()
    currentDate = datetime.now()
    
    startTs = datetime(currentDate.year, currentDate.month, currentDate.month)
    endTs = startTs + timedelta(days = 1)
    
    
@app.route('/api/body-fat-prediction', methods=['GET'])
@loginRequired(methods=['GET'])
@profileRequired(methods=['GET'])
def bodyFat():
    data = request.get_json()

    # check if all required headers are present
    try:
        validate(instance=data, schema=validationSchemes.bodyFatPredictionSchema)
    except exceptions.ValidationError as error:
        return customResponse(False, error.message)

    # check if all headers have valid values
    for header in list(data.keys()):
        if header != 'token' and header != 'username':
            if float(data[header]) < 0 or float(data[header]) > 1000:
                return customResponse(f'The value for {header} is invalid', False)

    # scale inputs
    X = np.array([list(map(float, [data.get('weight'), data.get('chest'), data.get('abdomen'), data.get('hip')]))])
    X = bodyFatScalerX.transformData(X)
    X = X.reshape(1, 1, 4)

    # use neural network to make predictions
    prediction = bodyFatPredictor.predict(X)
    prediction = round(bodyFatScalerY.inverseTransform(prediction)[0][0][0], 0)

    return customResponse(True, 'Successful prediction', prediction=prediction)



@app.route('/api/food-data')
@loginRequired(methods = ['GET'])
def foodData():
    pass
    


# use garmin connect to get garmin data from watch
