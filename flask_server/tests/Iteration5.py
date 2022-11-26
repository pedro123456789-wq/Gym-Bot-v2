from serverTests import ExpectedResponse, EndpointRequest, TestAutomator

if __name__ == '__main__':
    sessionToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoicGVkcm8iLCJleHAiOjE2NjcwNjMwMzl9.I1WRBF_WiWp8L29hqfii1TF7ajTAgk8gvz33Q76Xoeg'
        
    tests = [
        EndpointRequest('/api/insights', 
                        {'username': 'pedro', 
                         'token': sessionToken, 
                         'startDate': '15/09/2022', 
                         'endDate': '17/09/2022'}, 
                        'GET'), 
        EndpointRequest('/api/insights',
                        {'username': 'pedro',
                         'token': sessionToken,
                         'startDate': '-1/-2/-2', 
                         'endDate': '-1/1/1'},
                        'GET'),  
        EndpointRequest('/api/insights',
                        {'username': 'pedro',
                         'token': sessionToken,
                         'startDate': '19/09/2022', 
                         'endDate': '18/09/2022'}, 
                        'GET'),
    ]

    responses = [
        ExpectedResponse(200, {'success': True, 
                               'message': 'Fetched data successfully', 
                               'data': {'distance': {'15/9/2022': 0, '16/9/2022': 5.0, '17/9/2022': 5.5}, 
                                        'time': {'15/9/2022': 0, '16/9/2022': 20.0, '17/9/2022': 22.0}, 
                                        'caloriesEaten': {'15/9/2022': 0, '16/9/2022': 0, '17/9/2022': 0}, 
                                        'caloriesBurned': {'15/9/2022': 0, '16/9/2022': 350, '17/9/2022': 370}}}), 
        ExpectedResponse(400, {'success': False, 
                               'message': 'Invalid date format'}), 
        ExpectedResponse(400, {'success': False, 
                               'message': 'Start date must be before end date'})
    ]


    automator = TestAutomator('http://localhost:8080')
    automator.checkEnpoints(tests, responses, '/api/insights')