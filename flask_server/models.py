from flask_server import db

workout_exercise = db.Table('workout_exercise', 
    db.Column('workout_id', db.Integer, db.ForeignKey('workout.id')),   
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'))
)




class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, unique = False, nullable = False)
    emailConfirmed = db.Column(db.Boolean, unique = False, default = False)
    emailConfirmationDate = db.Column(db.DateTime, nullable = True)
    
    foodRecords = db.relationship('FoodRecord', backref = 'user')
    fitnessData = db.relationship('FitnessData', backref = 'user', uselist = False)
    targets = db.relationship('Targets', backref = 'user', uselist = False)
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

    foodRecordId = db.Column(db.Integer, db.ForeignKey('food_record.id'))




class FoodRecord(db.Model):
    __tablename__ = 'food_record'

    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    foodItem = db.relationship('Food', uselist = False, backref = 'food_record')




class FitnessData(db.Model):
    __tablename__ = 'fitness_data'

    id = db.Column(db.Integer, primary_key = True)
    height = db.Column(db.Integer, unique = False, nullable = True)
    weight = db.Column(db.Integer, unique = False, nullable = True)
    vo2Max = db.Column(db.Integer, unique = False, nullable = True)
    gender = db.Column(db.Integer, unique = False, nullable = True)
    age = db.Column(db.Integer, unique = False, nullable = True)

    userId = db.Column(db.Integer, db.ForeignKey('user.id'))




class Targets(db.Model):
    __tablename__ = 'targets'

    id = db.Column(db.Integer, primary_key = True)
    caloriesEaten = db.Column(db.Integer, unique = False, nullable = True)
    caloriesBurned = db.Column(db.Integer, unique = False, nullable = True)
    minutesTrained = db.Column(db.Integer, unique = False, nullable = True)
    distanceRan = db.Column(db.Integer, unique = False, nullable = True)

    userId = db.Column(db.Integer, db.ForeignKey('user.id'))




class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, unique = False, nullable = False)
    durationSeconds = db.Column(db.Integer, unique = False, nullable = False)
    repetitions = db.Column(db.Integer, unique = False, nullable = False)




class Workout(db.Model):
    __tablename__ = 'workout'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable = False, unique = False)
    
    exercises = db.relationship('Exercise', secondary = workout_exercise, backref = 'exercise')
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))