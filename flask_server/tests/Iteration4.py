from serverTests import ExpectedResponse, EndpointRequest, TestAutomator



if __name__ == '__main__':
    sessionToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoicGVkcm8iLCJleHAiOjE2NjY5Nzg3NjB9.R8OzfTbwZ-8U6uE7nRNTECm7nX6Sf93UqdS4CvvKEyM'
        
    tests = [
        EndpointRequest('/api/profile', 
                        {'username': 'pedro', 
                            'token': sessionToken, 
                            'caloriesEatenTarget': 3200, 
                            'caloriesBurnedTarget':3500, 
                            'distanceRanTarget':7000, 
                            'minutesTrainedTarget':90, 
                            'height': 301, 
                            'weight': 68, 
                            'vo2Max':64, 
                            'gender':1, 
                            'age': 17}, 
                        'POST'), 
        EndpointRequest('/api/profile', 
                        {'username': 'pedro', 
                            'token': sessionToken, 
                            'caloriesEatenTarget': 3200, 
                            'caloriesBurnedTarget':3500, 
                            'distanceRanTarget':7000, 
                            'minutesTrainedTarget':90, 
                            'height': 180, 
                            'weight': 68, 
                            'vo2Max':64, 
                            'gender':1, 
                            'age': 17}, 
                        'POST'), 
        EndpointRequest('/api/profile', 
                        {'username': 'test2223', 
                            'token': sessionToken}, 
                        'GET'),
        EndpointRequest('/api/profile', 
                        {'username': 'test2223', 
                            'token': sessionToken}, 
                        'GET'), 
        EndpointRequest('/api/profile', 
                        {'username': 'pedro', 
                            'token': sessionToken, 
                            'caloriesEatenTarget': 3200, 
                            'caloriesBurnedTarget':3500, 
                            'distanceRanTarget':7000, 
                            'minutesTrainedTarget':90, 
                            'height': 183, 
                            'weight': 68, 
                            'vo2Max':64, 
                            'gender':1, 
                            'age': 17}, 
                        'POST'), 
        EndpointRequest('/api/profile', 
                        {'username': 'pedro', 
                            'token': sessionToken, 
                        'caloriesEatenTarget':3200, 
                        'caloriesBurnedTarget':3800, 
                        'distanceRanTarget':8000, 
                        'minutesTrainedTarget':200, 
                        'height': 183, 
                        'vo2Max': 64, 
                        'gender': 1, 
                        'age': 17}, 
                        'PUT'),
        EndpointRequest('/api/profile', 
                        {'username': 'pedro', 
                            'token': sessionToken, 
                            'caloriesEatenTarget':3900}, 
                        'PUT'), 
        EndpointRequest('/api/profile',
                        {'username': 'pedro', 
                            'token': sessionToken, 
                            'age':'23454'}, 
                        'PUT') 
    ]

    responses = [
        ExpectedResponse(400, 
                            {'success': False, 
                            'message': 'Some of the values are out of range'}), 
        ExpectedResponse(200, {'success': True, 
                                'message': 'Profile created'}), 
        ExpectedResponse(400, {'success': False, 
                                'message': 'Token does not match username'}), 
        ExpectedResponse(400, {'success': False, 
                                'message': 'Token does not match username'}), 
        ExpectedResponse(400, {'success': False, 
                                'message': 'You already have a profile'}), 
        ExpectedResponse(200, {'success': True, 
                                'message': 'Data Updated'}),
        ExpectedResponse(200, {'success': True, 
                                'message': 'Data Updated'}),
        ExpectedResponse(400, {'success': False, 
                                'message': 'Some of the values are out of range or have the wrong data type'})
    ]


    automator = TestAutomator('http://localhost:8080')
    automator.checkEnpoints(tests, responses, 'profile')

    tests = [
        EndpointRequest('/api/runs', 
                        {'username': 'pedro', 
                            'token': sessionToken, 
                            'startDate': '16/9/2022', 
                            'endDate': '19/9/2022'},
                        'GET'), 
        EndpointRequest('/api/runs', 
                        {'username': 'pedro', 
                            'token': sessionToken, 
                            'startDate': 'abc', 
                            'endDate': '18/9/2022'}, 
                        'GET'), 
        EndpointRequest('/api/runs', 
                        {'username': 'pedro', 
                            'token': sessionToken, 
                            'startDate': '31/2/2022', 
                            'endDate': '18/9/2022'}, 
                        'GET'), 
        EndpointRequest('/api/runs', 
                        {'username': 'pedro', 
                            'token': sessionToken,
                            'distance': 7000, 
                            'durationSeconds': 1200, 
                            'caloriesBurned': 400}, 
                        'POST'), 
        EndpointRequest('/api/runs',
                        {'username': 'pedro', 
                            'token': sessionToken,
                            'distance': 500000, 
                            'durationSeconds': 86400, 
                            'caloriesBurned': 20000}, 
                        'POST'),
        EndpointRequest('/api/runs',
                        {'username': 'pedro', 
                            'token': sessionToken,
                            'distance': 500001,
                            'durationSeconds': 86401, 
                            'caloriesBurned': 20001}, 
                        'POST') 
    ]


    responses = [ExpectedResponse(200, {'success': True, 
                                        'message': 'Got run data successfully', 
                                        'data': {'runNumber': 3, 
                                                    'runs': [
                                                        {'distance': 5.0, 
                                                        'duration': 1200, 
                                                        'caloriesBurned': 350, 
                                                        'completionDate': '16/09/2022'}, 
                                                        {'distance': 5.5, 
                                                        'duration': 1320, 
                                                        'caloriesBurned': 370, 
                                                        'completionDate': '17/09/2022'}, 
                                                        {'distance': 6, 
                                                        'duration': 1320, 
                                                        'caloriesBurned': 430, 
                                                        'completionDate': '18/09/2022'}]
                                                    }
                                        }
                                    ), 
                    ExpectedResponse(400, {'success': False, 
                                        'message': 'Invalid date format' }), 
                    ExpectedResponse(400, {'success':False,
                                        'message': 'Invalid date format'}), 
                    ExpectedResponse(200, {'success': True, 
                                        'message': 'Run saved successfully'}),
                    ExpectedResponse(200, {'success': True,
                                        'message': 'Run saved successfully'}), 
                    ExpectedResponse(400, {'success': False, 
                                        'message': 'Some of the values are out of range'})
                ]

    automator = TestAutomator('http://localhost:8080')
    automator.checkEnpoints(tests, responses, 'runs')


    tests = [EndpointRequest('/api/workouts', 
                                {'username': 'pedro', 
                                'token': sessionToken, 
                                'targetWorkouts': 'ALL', 
                                'startDate': '19/9/2022',
                                'endDate': '20/9/2022'}, 
                                'GET'),
            
            EndpointRequest('/api/workouts', 
                                {'username': 'pedro', 
                                'token': sessionToken, 
                                'targetWorkouts': 'ALL', 
                                'startDate': '20/9/2022',
                                'endDate': '19/9/2022'}, 
                                'GET'),
            
            EndpointRequest('/api/workouts', 
                                {'username': 'pedro', 
                                'token': sessionToken, 
                                'name': 'Workout2', 
                                'caloriesBurned': 300, 
                                'exercises': [
                                    {
                                        'name': 'ex1', 
                                        'durationSeconds': 200, 
                                        'repetitions': 50
                                    }, 
                                    {
                                        'name': 'ex2',
                                        'durationSeconds': 500, 
                                        'repetitions': 100 
                                        
                                    }
                                ]}, 
                                'POST'),
            
            EndpointRequest('/api/workouts', 
                                {'username': 'pedro', 
                                'token': sessionToken, 
                                'name': 'w3', 
                                'caloriesBurned': 20000, 
                                'exercises': [
                                    {
                                        'name': 'ex1', 
                                        'durationSeconds': 86400, 
                                        'repetitions': 1000
                                    }, 
                                    {
                                        'name': 'ex2',
                                        'durationSeconds': 1, 
                                        'repetitions': 1 
                                        
                                    }
                                ]}, 
                                'POST'),
            
            EndpointRequest('/api/workouts', 
                                {'username': 'pedro', 
                                'token': sessionToken, 
                                'name': 'Workout2', 
                                'caloriesBurned': 20001, 
                                'exercises': [
                                    {
                                        'name': 'ex1', 
                                        'durationSeconds': 86401, 
                                        'repetitions': 1001
                                    }, 
                                    {
                                        'name': 'ex2',
                                        'durationSeconds': -1, 
                                        'repetitions': -3 
                                    }
                                ]}, 
                                'POST'),
            EndpointRequest('/api/workouts', 
                            {
                                'username': 'pedro', 
                                'token': sessionToken, 
                                'name': 'w3', 
                                'caloriesBurned': 200, 
                                'exercises': 'ex1, ex2, ex3, ...'
                            }, 
                            'POST')
                ]

    responses = [ExpectedResponse(200, {'success': True, 
                                        'message': 'Fetched saved workouts successfully', 
                                        'workouts': [
                                            {'name': 'Workout1', 
                                            'caloriesBurned': 150, 
                                            'exercises': [
                                                {'id': '1', 
                                                    'name': 'Exercise1', 
                                                    'durationSeconds': '300', 
                                                    'repetitions': '10'
                                                }, 
                                                {'id': '2', 
                                                    'name': 'Exercise2', 
                                                    'durationSeconds': '350', 
                                                    'repetitions': '30'
                                                }
                                            ]}
                                        ]
                                    }), 
                    ExpectedResponse(400, {'success': False, 
                                        'message': 'Start date must be before the end date'}), 
                    ExpectedResponse(200, {'success': True,
                                        'message': 'Added new workout'}), 
                    ExpectedResponse(200, {'success': True,
                                        'message': 'Added new workout'}), 
                    ExpectedResponse(400, {'success': False, 
                                        'message': 'Some of the values are out of range'}), 
                    ExpectedResponse(400, {'success': False, 
                                        'message': 'Invalid exercise list'})
                ]    
    automator = TestAutomator('http://localhost:8080')
    automator.checkEnpoints(tests, responses, 'workouts')