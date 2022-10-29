from serverTests import EndpointRequest, ExpectedResponse, TestAutomator


if __name__ == '__main__':
    # sign-up endpoint tests
    testEndpoints1 = [
        EndpointRequest('/api/sign-up', {'username': 'user1','password': 'Password123#', 'email': '1234'}, 'POST'),
        EndpointRequest('/api/sign-up', {'username': 1234, 'password': 3345, 'email': 'false'}, 'POST'),
        EndpointRequest('/api/sign-up', {'username': 'user1','password': '12', 'email': 'email@gmail.com'}, 'POST'),
        EndpointRequest('/api/sign-up', {'username': 'user1','password': 'A123456#', 'email': 'email@gmail.com'}, 'POST'),
        EndpointRequest('/api/sign-up', {'username': 'pedro','password': 'Password123#', 'email': 'email2@gmail.com'}, 'POST'),
        EndpointRequest('/api/sign-up', {'username': 'user3','password': 'Password1234#', 'email': 'email3@gmail.com'}, 'POST')
    ]

    expectedResponses1 = [
        ExpectedResponse(400, {'success': False, 'message': 'Invalid email'}),
        ExpectedResponse(400, {'success': False, 'message': "1234 is not of type 'string'"}),
        ExpectedResponse(400, {
                         'success': False, 'message': 
                         'Invalid password. Passwords must have 8+ characters, at least 1 special symbol and 1 capital letter'}),
        ExpectedResponse(200, {'success': True, 'message': 'Account created'}),
        ExpectedResponse(400, {'success': False, 'message': 'Username already taken'}),
        ExpectedResponse(200, {'success': True, 'message': 'Account created'})
    ]

    automator = TestAutomator('http://localhost:8080')
    automator.checkEnpoints(testEndpoints1, expectedResponses1, 'sign-up')

    # confirm-email endpoint tests
    testEndpoints2 = [
        EndpointRequest('/api/confirm-email', {'username': 'pedro', 'confirmationCode': 12345}, 'PUT'),
        EndpointRequest('/api/confirm-email', {'username': 'pedro', 'confirmationCode': '12345'}, 'PUT'),
        EndpointRequest('/api/confirm-email', {'username': 'pedro', 'confirmationCode': '15432'}, 'PUT'),
        EndpointRequest('/api/confirm-email', {'username': 12, 'confirmationCode': 'abc'}, 'PUT'),
        EndpointRequest('/api/confirm-email', {'username': 'pedro', 'confirmationCode': 'abc'}, 'PUT'),
    ]

    expectedResponses2 = [
        ExpectedResponse(200, {'success': False, 'message':  "123456 is not of type 'string'"}),
        ExpectedResponse(400, {'success': False, 'message': 'Incorrect verification code'}),
        ExpectedResponse(200, {'success': True, 'message': 'Account was verified successfully'}),
        ExpectedResponse(400, {'success': False, 'message': "12 is not of type 'string'"}),
        ExpectedResponse(400, {'success': False, 'message': "'abc' is too short"}),
    ]

    automator.checkEnpoints(
        testEndpoints2, expectedResponses2, 'confirm-email')

    # log-in endpoint tests
    testEndpoints3 = [
        EndpointRequest('/api/log-in', {'username': 'pedro', 'password': 'Password123#'}, 'POST'),
        EndpointRequest('/api/log-in', {'username': 'pedro', 'password': 'WrongPassword'}, 'POST'),
        EndpointRequest('/api/log-in', {'username': '', 'password': ''}, 'POST'),
        EndpointRequest('/api/log-in', {'username': 'pedro', 'password': 'A12345#'}, 'POST'),
        EndpointRequest('/api/log-in', {'username': 'abcd', 'password': 'Password123#'}, 'POST'),
    ]

    expectedResponses3 = [
        ExpectedResponse(200, {'success': True, 'message': 'Login successful'}),
        ExpectedResponse(400, {'success': False, 'message': 'Incorrect password'}),
        ExpectedResponse(400, {'success': False, 'message': "'' is too short"}),
        ExpectedResponse(400, {'success': False, 'message': 'Incorrect password'}),
        ExpectedResponse(400, {'success': False, 'message': 'Account does not exist'}),
    ]

    automator.checkEnpoints(testEndpoints3, expectedResponses3, 'log-in')