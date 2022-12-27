# TODO
# /api/body-fat-prediction and /api/calories-burned-prediction tests

from serverTests import EndpointRequest, ExpectedResponse, TestAutomator


if __name__ == '__main__':
    sessionToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoicGVkcm8iLCJleHAiOjE2NjYyODIxMTB9'

    tests = [EndpointRequest('/api/body-fat-prediction',
                             {'usename': 'pedro',
                              'token': sessionToken,
                              'weight': 72,
                              'chest': 90,
                              'abdomen': 75,
                              'hip': 80},
                             'GET'),
             EndpointRequest('/api/body-fat-prediction',
                             {'token': sessionToken,
                              'weight': 1000,
                              'chest': 1000,
                              'abdomen': 1000,
                              'hip': 1},
                             'GET'),
             EndpointRequest('/api/body-fat-prediction',
                             {'usename': 'pedro',
                              'token': sessionToken,
                              'weight': -1,
                              'chest': 'two',
                              'abdomen': 111,
                              'hip': '3'},
                             'GET'),
             
             EndpointRequest('/api/calories-burned-prediction',
                             {'username': 'pedro',
                              'token': sessionToken,
                              'duration': 24,
                              'heartRate': 190},
                             'GET'),
             EndpointRequest('/api/calories-burned-prediction',
                             {'username': 'pedro',
                              'token': sessionToken,
                              'duration': 1440,
                              'heartRate': 230},
                             'GET'),
             EndpointRequest('/api/calories-burned-prediction',
                             {'username': 'pedro',
                              'token': sessionToken,
                              'duration': 1441,
                              'heartRate': -1},
                             'GET'),
             EndpointRequest('/api/calories-burned-prediction',
                             {'username': 'pedro',
                              'token': sessionToken,
                              'duration': '2 minutes',
                              'heartRate': 8908908908},
                             'GET'),
             ]
    
    
    expectedResponses = [
        ExpectedResponse(200,
                        {'success': True,
                         'message': 'Successful prediction', 
                         'prediction': 5.0}), 
        ExpectedResponse(200,
                        {'success': True,
                         'message': 'Successful prediction', 
                         'prediction': 98}),
        ExpectedResponse(400,
                         {'success': False, 
                          'message': "'two' is not a number"}), 
        ExpectedResponse(200, 
                         {'success': True, 
                          'message': 'Successful prediction', 
                          'prediction': 320}), 
        ExpectedResponse(200, 
                         {'success': True, 
                          'message': 'Successful prediction', 
                          'prediction': 10000}), 
        ExpectedResponse(400, 
                         {'success': False, 
                          'message': 'Some of the values are out of range'}), 
        ExpectedResponse(400, 
                         {'success': False, 
                          'message': 'Invalid value for duration'})
    ]
    
    automator = TestAutomator('http://localhost:8080')
    automator.checkEnpoints(tests, expectedResponses)