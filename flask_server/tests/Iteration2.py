from serverTests import EndpointRequest, ExpectedResponse, TestAutomator


if __name__ == '__main__':
    sessionToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoicGVkcm8iLCJleHAiOjE2NjYyODIxMTB9'
    
    tests = [EndpointRequest('/api/food', {'username': 'pedro', 'token': sessionToken, 'startDate': '16/9/2022', 'endDate': '18/9/2022'}, 
                             'GET'),
             EndpointRequest('/api/food', {'username': 'pedro', 'token': sessionToken, 'startDate': '300-20-12', 'endDate': '500-2-1'}, 
                             'GET'),
             EndpointRequest('/api/food', {'username': 'pedro', 'token': sessionToken, 'foodName': 'test', 'calories': 200, 'fat': 1,  
                                           'carboHydrates': 5, 
                                           'protein': 5}, 'POST'),
             EndpointRequest('/api/food', {'username': 'pedro',
                                           'foodName': 'test2',
                                           'token': sessionToken,
                                           'calories': 10000,
                                           'fat': 10000,
                                           'carboHydrates': 10000,
                                           'protein': 10000}, 'POST'),
             EndpointRequest('/api/food', {'username': 'pedro',
                                           'foodName': 'test3',
                                           'calories': 10001,
                                           'fat': 10001,
                                           'carboHydrates': 10001,
                                           'token': sessionToken,
                                           'protein': 10001}, 'POST'),
             ]

    expectedResponses = [
        ExpectedResponse(200, {'success': True,'message': 'Got Data',
                               'data': [{'name': 'pasta',
                                         'calories': 100,
                                         'fat': 1,
                                         'carbohydrates': 20,
                                         'protein': 5},
                                        {'name': 'rice',
                                         'calories': 100,
                                         'fat': 1,
                                         'carbohydrates': 20,
                                         'protein': 5}]}),
        ExpectedResponse(400, {'success': False, 'message': 'Invalid date format'}),
        ExpectedResponse(200, {'success': True, 'message': 'New food record added to database'}),
        ExpectedResponse(200, {'success': True, 'message': 'New food record added to database'}),
        ExpectedResponse(400, {'success': False, 'message': 'Some of the values are out of range'})
    ]

    automator = TestAutomator('http://localhost:8080')
    automator.checkEnpoints(tests, expectedResponses, 'food')
