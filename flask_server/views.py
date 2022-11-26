# local imports
from flask_server import (
    app,
    db,
    validationSchemes,
    encryptionHandler,
    bodyFatPredictor,
    bodyFatScalerY,
    bodyFatScalerX,
    caloriesBurnedPredictor,
    caloriesBurnedScalerX,
    caloriesBurnedScalerY
)

from flask_server.foodData import FoodData
from flask_server.models import (
    User,
    Food,
    Workout,
    Exercise,
    Run,
    food_record,
    workout_exercise
)
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


def isSameDay(date1: datetime, date2: datetime) -> bool:
    return date1.day == date2.day and date1.month == date2.month and date1.year == date2.year


def checkRange(data, bounds):
    for key in data:
        if key in bounds:
            #can only perform artihmetic comparison on integers or floats 
            if type(data[key]) != int and type(data[key]) != float:
                return False 
            
            if (data[key] > bounds[key]['max'] 
                   or data[key] < bounds[key]['min']):
                return False
            
    return True


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
        field = error.path.pop()
        
        return customResponse(False, error.message)

        if field == 'password':
            return customResponse(False, 'Invalid password. Passwords must have 8+ characters, at least 1 special symbol,  1 capital letter and 1 number')
        elif field == 'email':
            return customResponse(False, 'Invalid email')

        return customResponse(False, error.message)

    username, email, password = data.get('username'), data.get('email'), data.get('password')
    hashedPassword = encryptionHandler.generate_password_hash(password).decode('utf-8')

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
            f'Your verification code is {confirmationCode}'
        )
    except Exception as e:
        print('Internal server failure')
        return customResponse(False, 'Internal server error')

    return customResponse(True, 'Account created')


@app.route('/api/confirm-email', methods=['PUT'])
def confirmEmail():
    data = request.get_json()

    # validate headers
    try:
        validate(instance=data, schema=validationSchemes.confirmEmailSchema)
    except exceptions.ValidationError as error:
        return customResponse(False, error.message)

    username, confirmationCode = data.get('username'), data.get('confirmationCode')

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
            token = jwt.encode({'user': username, 'exp': datetime.utcnow() + timedelta(minutes=60)}, app.config['SECRET_KEY']).decode('utf-8')
            return customResponse(True, 'Login successful', token=str(token))
        else:
            return customResponse(False, 'Incorrect password')

    else:
        return customResponse(False, 'Account does not exist')


@app.route('/api/check-session', methods=['GET'])
@loginRequired(methods=['GET'])
@profileRequired(methods=['GET'])
def checkSession():
    data = request.headers
    username = data.get('username')

    return customResponse(True, f'Session is valid for {username}')


@app.route('/api/profile', methods=['GET', 'POST', 'PUT'])
@loginRequired(['GET', 'POST', 'PUT'])
@profileRequired(['GET', 'PUT'])
def profile():
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
        output['distanceRanTarget'] = output['distanceRanTarget'] / 1000  # convert distance to km
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
        if not checkRange(data, validationSchemes.profileBounds):
            return customResponse(False, 'Some of the values are out of range')

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
        if not checkRange(data, validationSchemes.profileBounds):
            return customResponse(False, 'Some of the values are out of range or have the wrong data type')

        # only set new values if all values provided are valid
        # this has impact on performance but ensures that transactions are atomic
        for header in list(data.keys()):
            #only set values of new fields 
            if header in validationSchemes.profileBounds.keys():
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

        # check if header values are in the valid range
        if not checkRange(data, validationSchemes.foodBounds):
            return customResponse(False, 'Some of the values are out of range')

        foodName, calories, fat, carboHydrates, protein = data.get('foodName'), data.get(
            'calories'), data.get('fat'), data.get('carboHydrates'), data.get('protein')

        # check if food item already exists
        itemMatches = Food.query.filter_by(name=foodName,
                                           calories=calories,
                                           fat=fat,
                                           carboHydrates=carboHydrates,
                                           protein=protein).all()

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
        targetUser = User.query.filter_by(
            username=request.headers.get('username')).first()
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
                startTs, endTs = datetime.strptime(startDate, dateFormat), datetime.strptime(endDate, dateFormat)
        except Exception as e:
            return customResponse(False, 'Invalid date format')
        
        if startTs > endTs:
            return customResponse(False, 'Start date must be before the end date')

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

        # check if header values are within valid range
        if not checkRange(data, validationSchemes.workoutBounds):
            return customResponse(False, 'Some of the values are out of range')

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

        for exercise in exerciseList:
            # validate each exercise in the exercise list
            try:
                validate(instance=exercise,
                         schema=validationSchemes.exerciseSchema)
            except exceptions.ValidationError as error:
                return customResponse(False, error.message)

            if not checkRange(data, validationSchemes.exerciseBounds):
                return customResponse(False, 'Some of the header values are out of range')

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

        if startDate == 'ALL' and endDate == 'ALL':
            targetRuns = Run.query.all()
        else:
            try:
                dateFormat = '%d/%m/%Y'

                if endDate == '+1':
                    startTs = datetime.strptime(startDate, dateFormat)
                    endTs = startTs + timedelta(days=1)
                else:
                    startTs, endTs = datetime.strptime(
                        startDate, dateFormat), datetime.strptime(endDate, dateFormat)
            except:
                return customResponse(False, 'Invalid date format')

            targetRuns = Run.query.filter((Run.completionDate <= endTs) & (
                Run.completionDate >= startTs) & (Run.userId == targetUser.id)).all()

        outputDict = {
            'runNumber': len(targetRuns),
            'runs': [{
                'distance': run.distance / 1000,
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

        if not checkRange(data, validationSchemes.runBounds):
            return customResponse(False, 'Some of the values are out of range')

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


@app.route('/api/insights', methods=['GET'])
@loginRequired(methods=['GET'])
@profileRequired(methods=['GET'])
def insights():
    data = request.headers
    targetUser = User.query.filter_by(username=data.get('username')).first()
    startDate, endDate = data.get('startDate'), data.get('endDate')

    # validate dates
    try:
        dateFormat = '%d/%m/%Y'

        if endDate == '+1':
            startTs = datetime.strptime(startDate, dateFormat)
            endTs = startTs + timedelta(days=1)
        else:
            startTs, endTs = datetime.strptime(
                startDate, dateFormat), datetime.strptime(endDate, dateFormat)
            endTs += timedelta(days=1)
    except:
        return customResponse(False, 'Invalid date format')
    
    print(startTs, endTs)
    print(startTs > endTs)
        
    if startTs >= endTs:
        return customResponse(False, 'Start date must be before end date')

    interval = (endTs - startTs).days
    distancesRan, timeTrained, caloriesEaten, caloriesBurned = {}, {}, {}, {}

    # initialize all dicts to zeros for all dates
    # this is necessary because otherwize days in which data was not entered would not be present in the dictionaries
    for i in range(0, interval):
        currentDate = startTs + timedelta(days=i)
        dayString = f'{currentDate.day}/{currentDate.month}/{currentDate.year}'
        distancesRan[dayString] = 0
        timeTrained[dayString] = 0
        caloriesEaten[dayString] = 0
        caloriesBurned[dayString] = 0

    targetRuns = Run.query.filter((Run.completionDate <= endTs) & (
        Run.completionDate >= startTs) & (Run.userId == targetUser.id)).all()
    foodRecords = db.session.query(food_record).filter((food_record.c.user_id == targetUser.id) &
                                                       (food_record.c.timestamp <= endTs) &
                                                       (food_record.c.timestamp >= startTs)).all()
    workouts = Workout.query.filter((Workout.completionDate <= endTs) & (
        Workout.completionDate >= startTs) & (Workout.userId == targetUser.id)).all()

    for run in targetRuns:
        completionDate = run.completionDate
        dayString = f'{completionDate.day}/{completionDate.month}/{completionDate.year}'
        distancesRan[dayString] += run.distance / 1000
        timeTrained[dayString] += run.durationSeconds / 60
        caloriesBurned[dayString] += run.caloriesBurned

    for food in foodRecords:
        completionDate = food.timestamp
        dayString = f'{completionDate.day}/{completionDate.month}/{completionDate.year}'
        foodItem = Food.query.filter_by(id=food.food_id).first()
        caloriesEaten[dayString] += foodItem.calories

    for workout in workouts:
        completionDate = workout.completionDate
        dayString = f'{completionDate.day}/{completionDate.month}/{completionDate.year}'
        caloriesBurned[dayString] += workout.caloriesBurned
        # sum of duration of each exercise
        timeTrained[dayString] += sum(
            [exercise.durationSeconds for exercise in workout.exercises]) / 60

    return customResponse(True, 'Fetched data successfully', data={'distance': distancesRan,
                                                                   'time': timeTrained,
                                                                   'caloriesEaten': caloriesEaten,
                                                                   'caloriesBurned': caloriesBurned
                                                                   })


@app.route('/api/body-fat-prediction', methods=['POST'])
@loginRequired(methods=['POST'])
@profileRequired(methods=['POST'])
def bodyFat():
    data = request.get_json()

    try:
        validate(instance=data, schema=validationSchemes.bodyFatPrediction)
    except Exception as error:
        return customResponse(False, error.message)

    if not checkRange(data, validationSchemes.bodyFatPredictionBounds):
        return customResponse(False, 'Some values are out of range')

    #transform data into smaller range
    X = [[data.get('weight'), data.get('chest'), data.get('abdomen'), data.get('hip')]]
    X = bodyFatScalerX.transformData(X)
    
    # use neural network to make predictions
    prediction = bodyFatPredictor.predict(X)
    
    #use data scaler to convert data back into original range
    prediction = bodyFatScalerY.inverseTransform([[prediction[0]]])[0][0]
    return customResponse(True, 'Successful prediction', prediction=round(prediction, 1))


@app.route('/api/calories-burned-prediction', methods=['POST'])
@loginRequired(methods=['POST'])
@profileRequired(methods=['POST'])
def caloriesBurnedPrediction():
    data = request.get_json()
    targetUser = User.query.filter_by(username=data.get('username')).first()

    try:
        validate(instance=data, schema=validationSchemes.caloriesBurnedSchema)
    except Exception as error:
        return customResponse(False, error.message)

    if not checkRange(data, validationSchemes.caloriesBurnedBounds):
        return customResponse(False, 'Some of the values are out of range')

    duration, heartRate = data.get('duration'), data.get('heartRate')
    gender, age, height, weight = targetUser.gender, targetUser.age, targetUser.height, targetUser.weight

    # format and convert data into necessary format
    X = [[gender, age, height, weight, duration, heartRate]]
    X = caloriesBurnedScalerX.transformData(X)

    # make prediction of calories burned and transform it back to original range
    prediction = caloriesBurnedPredictor.predict(X)
    prediction = caloriesBurnedScalerY.inverseTransform([[prediction[0]]])[0][0]
    print(duration, heartRate, prediction)
    
    return customResponse(True, 'Successful prediction', prediction=round(prediction, 1))


@app.route('/api/food-data', methods=['GET'])
@loginRequired(methods=['GET'])
@profileRequired(methods=['GET'])
def foodData():
    data = request.headers
    queryType = data.get('queryType')

    if queryType == 'barcode':
        barcode = data.get('barcode')
        if not barcode:
            return customResponse(False, 'You did not provide a barcode')

        if len(barcode) > 100:
            return customResponse(False, 'The barcode provided is too long')

        result = FoodData.searchByBarcode(barcode)

        if result:
            return customResponse(True, 'Found item', data=result)
        else:
            return customResponse(False, 'No matches found for this barcode')

    elif queryType == 'text':
        searchQuery = data.get('searchQuery')
        resultsNumber = data.get('resultNumber')

        if not searchQuery or not resultsNumber:
            return customResponse(False, 'searchQuery and resultNumber are required headers')

        if len(searchQuery) > 1000:
            return customResponse(False, 'The search query is too long')

        if int(resultsNumber) > 200:
            return customResponse(False, 'The maximum number of results is 200')

        results = FoodData.getItems(searchQuery, resultsNumber)

        if len(results) > 0:
            return customResponse(True, 'Got data successfully', results=results)
        else:
            return customResponse(False, 'No results found')
    else:
        return customResponse(False, 'Invalid query type')