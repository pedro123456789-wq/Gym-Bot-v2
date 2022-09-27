import requests
from time import time 


class ExpectedResponse:
    def __init__(self, statusCode, content):
        self.statusCode = statusCode
        self.content = content



class EndpointRequest:
    def __init__(self, url, headers, method):
        self.url = url
        self.headers = headers
        self.method = method



class TestAutomator:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.successful = 0
        self.failed = 0
        self.averageResponseTime = 0

    def checkEnpoints(self, endpointRequests, expectedResponses, endpointName = 'Enpoint'):
        passed = 0
        failed = 0
        testId = 1
        totalTests = len(endpointRequests)
        totalDuration = 0

        print('<--- Automated Tests --->')
        print(f'Performing {len(endpointRequests)} tests on {self.baseUrl}/{endpointName}\n\n')


        for endpointRequest, expectedResponse in zip(endpointRequests, expectedResponses):
            method = endpointRequest.method
            
            startTime = time()
            if method != 'GET':
                response = requests.request(method = endpointRequest.method, url = f'{self.baseUrl}/{endpointRequest.url}', json = endpointRequest.headers)
            else:
                response = requests.request(method = endpointRequest.method, url = f'{self.baseUrl}/{endpointRequest.url}', headers = endpointRequest.headers)
            
            statusCode = response.status_code
            content = response.json()
            duration = time() - startTime

            if statusCode == expectedResponse.statusCode and content == expectedResponse.content:
                passed += 1
                print(f'Passed test #{testId} in {duration}s')
            else:
                failed += 1
                print(f'Failed test #{testId}')
                print(f'Status Code: {statusCode}, expected: {expectedResponse.statusCode}')
                print(f'Response: {content}, expected: {expectedResponse.content}')

            testId += 1
            totalDuration += duration

        print(f'\n\nTests passed: {passed}/{totalTests}')
        print(f'Tests failed: {failed}/{totalTests}')
        print(f'Time elapsed: {totalDuration}s')
        print('<----   ---->')




if __name__ == '__main__':
    testEndpoints1 = [ 
                     EndpointRequest('/api/sign-up', {'username': 'user1', 'password': 'Password123#', 'email': '1234'}, 'POST'), 
                     EndpointRequest('/api/sign-up', {'username': 1234, 'password': 3345, 'email': 'false'}, 'POST'), 
                     EndpointRequest('/api/sign-up', {'username': 'user1', 'password': '12', 'email': 'email@gmail.com'}, 'POST'), 
                     EndpointRequest('/api/sign-up', {'username': 'user1', 'password': 'A123456#', 'email': 'email@gmail.com'}, 'POST'), 
                     EndpointRequest('/api/sign-up', {'username': 'pedro', 'password': 'Password123#', 'email': 'email2@gmail.com'}, 'POST'),
                     EndpointRequest('/api/sign-up', {'username': 'user3', 'password': 'Password1234#', 'email': 'email3@gmail.com'}, 'POST')
                    ]
    
    expectedResponses1 = [
                         ExpectedResponse(200, {'success': True, 'message': 'Account created'}), 
                         ExpectedResponse(400, {'success': False, 'message': 'Invalid email'}), 
                         ExpectedResponse(400, {'success': False, 'message': 'Invalid value for username'}), 
                         ExpectedResponse(400, {'success': False, 'message': 'Invalid password. Passwords must have 8+ characters, at least 1 special symbol and 1 capital letter'}), 
                         ExpectedResponse(200, {'success': True, 'message': 'Account created'}), 
                         ExpectedResponse(400, {'success': False, 'message': 'Username already taken'}), 
                         ExpectedResponse(200, {'success': True, 'message': 'Account created'})
                        ]
    
    automator = TestAutomator('http://localhost:8080')
    automator.checkEnpoints(testEndpoints1, expectedResponses1, 'sign-up')
    
    testEndpoints2 = [ 
                     EndpointRequest('/api/sign-up', {'username': 'user1', 'password': 'Password123#', 'email': '1234'}, 'POST'), 
                     EndpointRequest('/api/sign-up', {'username': 1234, 'password': 3345, 'email': 'false'}, 'POST'), 
                     EndpointRequest('/api/sign-up', {'username': 'user1', 'password': '12', 'email': 'email@gmail.com'}, 'POST'), 
                     EndpointRequest('/api/sign-up', {'username': 'user1', 'password': 'A123456#', 'email': 'email@gmail.com'}, 'POST'), 
                     EndpointRequest('/api/sign-up', {'username': 'pedro', 'password': 'Password123#', 'email': 'email2@gmail.com'}, 'POST'),
                     EndpointRequest('/api/sign-up', {'username': 'user3', 'password': 'Password1234#', 'email': 'email3@gmail.com'}, 'POST')
                    ]
    
    expectedResponses2 = [
                         ExpectedResponse(200, {'success': True, 'message': 'Account created'}), 
                         ExpectedResponse(400, {'success': False, 'message': 'Invalid email'}), 
                         ExpectedResponse(400, {'success': False, 'message': 'Invalid value for username'}), 
                         ExpectedResponse(400, {'success': False, 'message': 'Invalid password. Passwords must have 8+ characters, at least 1 special symbol and 1 capital letter'}), 
                         ExpectedResponse(200, {'success': True, 'message': 'Account created'}), 
                         ExpectedResponse(400, {'success': False, 'message': 'Username already taken'}), 
                         ExpectedResponse(200, {'success': True, 'message': 'Account created'})
                        ]
    
    automator.checkEnpoints(testEndpoints1, expectedResponses1, 'check-email')
    
    
    
    
    
