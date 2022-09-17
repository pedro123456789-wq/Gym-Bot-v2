'''JSON validation schemes for body and headers of API endpoints and decorators'''


'''/api/sign-up'''
signUpSchema = {
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string',
            'minLength': 5,
            'maxLength': 20
        },
        'password': {
            'type': 'string',
            'minLength': 7,
            'maxLength': 40,
            'pattern': '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
        },
        'email': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 40,
            # regex pattern for email validation
            'pattern': '[a-zA-Z0-9]*@[a-zA-Z0-9]*\.*[a-zA-Z0-9]*'
        }
    },
    'required': ['username', 'email', 'password']
}


'''api/confirm-email'''
confirmEmailSchema = {
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string',
            'minLength': 5,
            'maxLength': 20
        },
        'confirmationCode': {
            'type': 'string',
            'length': 5
        }
    },
    'required': ['username', 'confirmationCode']
}


'''api/log-in'''
loginSchema = {
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 40
        },
        'password': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 40,
        }
    },
    'required': ['username', 'password']
}


'''api/profile'''
profileSchema = {
    'type': 'object',
    'properties': {
        'height': {
            'type': 'number',
        },

        'weight': {
            'type': 'number'
        },

        'vo2Max': {
            'type': 'number'
        },

        'age': {
            'type': 'number'
        },

        'gender': {
            'type': 'number'
        },

        'caloriesEatenTarget': {
            'type': 'number'
        },

        'caloriesBurnedTarget': {
            'type': 'number'
        },

        'minutesTrainedTarget': {
            'type': 'number'
        },

        'distanceRanTarget': {
            'type': 'number'
        }
    },

    'required': ['height', 'weight', 'vo2Max', 'age', 'gender', 'caloriesEatenTarget',
                 'caloriesBurnedTarget', 'minutesTrainedTarget', 'distanceRanTarget']
}


profileBounds = {
    'height': {
        'max': 300,
        'min': 0,
    },

    'weight': {
        'max': 1000,
        'min': 0
    },

    'vo2Max': {
        'max': 200,
        'min': 0
    },

    'age': {
        'max': 300,
        'min': 0
    },

    'gender': {
        'max': 1,
        'min': 0
    },

    'caloriesEatenTarget': {
        'max': 20000,
        'min': 0
    },

    'caloriesBurnedTarget': {
        'max': 20000,
        'min': 0
    },

    'minutesTrainedTarget': {
        'max': 1440,
        'min': 0
    },

    'distanceRanTarget': {
        'max': 500000,
        'min': 0
    }
}


'''api/food'''
foodSchema = {
    'type': 'object',
    'properties': {
        'foodName': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 100
        },

        'calories': {
            'type': 'number'
        },

        'fat': {
            'type': 'number'
        },

        'carboHydrates': {
            'type': 'number'
        },

        'protein': {
            'type': 'number'
        }
    },

    'required': ['foodName', 'calories', 'protein', 'carboHydrates', 'fat']
}

foodBounds = {
    'calories': {
        'max': 10000,
        'min': 0
    },
    'protein': {
        'max': 10000,
        'min': 0
    },
    'carboHydrates': {
        'max': 10000,
        'min': 0
    },
    'fat': {
        'max': 10000,
        'min': 0
    },
}


'''api/workouts  => POST'''
workoutsSchema = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 30
        },
        'caloriesBurned': {
            'type': 'number'
        }
    },
    'required': ['name', 'caloriesBurned']
}

workoutBounds = {
    'caloriesBurned': {
        'max': 20000,
        'min': 1
    }
}


exerciseSchema = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 30
        },
        'durationSeconds': {
            'type': 'number'
        },
        'repetitions': {
            'type': 'number'
        }
    },
    'required': ['name', 'durationSeconds', 'repetitions']
}

exerciseBounds = {
    'durationSeconds': {
        'max': 86400,
        'min': 1
    },
    'repetitions': {
        'max': 1000,
        'min': 1
    }
}


'''api/runs => POST'''
runSchema = {
    'type': 'object',
    'properties': {
        'distance': {
            'type': 'number',
        },
        'durationSeconds': {
            'type': 'number'
        },
        'caloriesBurned': {
            'type': 'number'
        }
    },
    'required': ['distance', 'durationSeconds', 'caloriesBurned']
}

runBounds = {
    'distance': {
        'max': 500000,
        'min': 0
    },
    'durationSeconds': {
        'max': 86400,
        'min': 0
    },
    'caloriesBurned': {
        'max': 20000,
        'min': 0
    }
}

'''/api/body-fat-prediction'''
bodyFatPrediction = {
    'type': 'object',
    'properties': {
        'weight': {
            'type': 'number'
        },
        'chest': {
            'type': 'number'
        },
        'abdomen': {
            'type': 'number'
        },
        'hip': {
            'type': 'number'
        }
    },
    'required': ['weight', 'chest', 'abdomen', 'hip']
}

bodyFatPredictionBounds = {
    'weight': {
        'max': 1000,
        'min': 0
    },
    'chest': {
        'max': 1000,
        'min': 0
    },
    'abdomen': {
        'max': 1000,
        'min': 0,
    },
    'hip': {
        'max': 1000,
        'min': 0
    }
}


'''/api/calories-burned-prediction => GET'''
caloriesBurnedSchema = {
    'type': 'object',
    'properties': {
        'Duration': {
            'type': 'number'
        },
        'Heartrate': {
            'type': 'number'
        }
    },
    'required': ['Duration', 'HeartRate']
}

caloriesBurnedBounds = {
    'Duration': {
        'max': 1440,
        'min': 0
    },
    'HeartRate': {
        'max': 230,
        'min': 20
    }
}


'''@loginRequired'''
sessionValidationSchema = {
    'type': 'object',
    'properties': {
        'token': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 1000
        },
        'username': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 40
        }
    },
    'required': ['token', 'username']
}
