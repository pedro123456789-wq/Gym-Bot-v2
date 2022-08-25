'''JSON validation schemes for body and headers of API endpoints and decorators'''


'''/api/sign-up'''
signUpSchema = {
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 20
        },
        'password': {
            'type': 'string',
            'minLength': 7,
            'maxLength': 40,
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
            'minLength': 1,
            'maxLength': 40
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
            'maxLength': 40
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
        'max': 100000,
        'min': 0
    },

    'caloriesBurnedTarget': {
        'max': 100000,
        'min': 0
    },

    'minutesTrainedTarget': {
        'max': 1224,
        'min': 0
    },

    'distanceRanTarget': {
        'max': 500,
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

    'required': ['foodName', 'calories', 'fat', 'carboHydrates', 'protein']
}


'''api/body-fat-prediction'''
bodyFatPredictionSchema = {
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
    'required': ['name']
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
    }
}


'''@loginRequired'''
sessionValidationSchema = {
    'type': 'object',
    'properties': {
        'token': {
            'type': 'string'
        },
        'username': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 40
        }
    },
    'required': ['token', 'username']
}
