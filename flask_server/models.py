from flask_server import db
from datetime import datetime



#juction table for Workout and Exercise
workout_exercise = db.Table('workout_exercise', 
    db.Column('id', db.Integer, primary_key = True), 
    db.Column('workout_id', db.Integer, db.ForeignKey('workout.id')),   
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'))
)


#table to store workouts that user has done
workout_record = db.Table('workout_record', 
    db.Column('record_id', db.Integer, primary_key = True),  
    db.Column('workout_id', db.Integer, db.ForeignKey('workout.id'), 
    db.Column('timestamp', db.DateTime, default = datetime.utcnow)
)


#juction table for User and Food
food_record = db.Table('food_record', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')), 
    db.Column('food_id', db.Integer, db.ForeignKey('food.id')), 
    db.Column('timestamp', db.DateTime, default = datetime.utcnow)
)




class User(db.Model):
    __tablename__ = 'user'

    #account data - one to one relationship
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, unique = False, nullable = False)
    confirmationCode = db.Column(db.String, unique = False, nullable = False)
    emailConfirmed = db.Column(db.Boolean, unique = False, default = False)

    #targets - one to one relationship
    caloriesEatenTarget = db.Column(db.Integer, unique = False, nullable = True)
    caloriesBurnedTarget = db.Column(db.Integer, unique = False, nullable = True)
    minutesTrainedTarget = db.Column(db.Integer, unique = False, nullable = True)
    distanceRanTarget = db.Column(db.Integer, unique = False, nullable = True)

    #fitness data - one to one relationship
    height = db.Column(db.Integer, unique = False, nullable = True)
    weight = db.Column(db.Integer, unique = False, nullable = True)
    vo2Max = db.Column(db.Integer, unique = False, nullable = True)
    gender = db.Column(db.Integer, unique = False, nullable = True) #1 = male, 0 = female
    age = db.Column(db.Integer, unique = False, nullable = True)

    #FoodRecords - many-to-many relationship
    foodRecords = db.relationship('Food', backref = 'user', secondary = food_record)

    #Workouts - one-to-many relationship
    workouts = db.relationship('Workout', backref = 'user')




class Food(db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = False, nullable = False)
    calories = db.Column(db.Integer, unique = False, nullable = False)

    #macro nutrients measured in grams
    fat = db.Column(db.Integer, unique = False, nullable = False)
    protein = db.Column(db.Integer, unique = False, nullable = False)
    carboHydrates = db.Column(db.Integer, unique = False, nullable = False)




class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key = True)
    durationSeconds = db.Column(db.Integer, unique = False, nullable = False)
    repetitions = db.Column(db.Integer, unique = False, nullable = False)
    caloriesBurned = db.Column(db.Integer, unique = False, nullable = False)
    exerciseType = db.Column(db.Text, unique = False, nullable = False)


    

class Workout(db.Model):
    __tablename__ = 'workout'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable = False, unique = True) #make workout name unique
    
    #Exercise - many-to-many relationship
    exercises = db.relationship('Exercise', secondary = workout_exercise, backref = 'exercise')
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))


