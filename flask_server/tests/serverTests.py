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
    testEndpoints = [EndpointRequest('/api/sign-up', {'username': 'user1', 'password': 'password123', 'email': 'abc'}, 'POST'), 
                     EndpointRequest('/api/sign-up', {'username': '1234', 'password': '3345', 'email': 'false'}, 'POST'), 
                     EndpointRequest('/api/sign-up', {'username': 'user1', 'password': '12', 'email': 'email@gmail.com'}, 'POST'), 
                     EndpointRequest('/api/sign-up', {'username': 'user1', 'password': 'a123456#', 'email': 'email@gmail.com'}, 'POST'), 
                     EndpointRequest('/api/sign-up', {'username': 'pedro', 'password': 'password123#', 'email': 'email@gmail.com'}, 'POST'),
                     EndpointRequest('/api/sign-up', {'username': 'user3', 'password': 'Password1234#', 'email': 'email2@gmail.com'}, 'POST')
                    ]
    
    expectedResponses = [ExpectedResponse(400, {'success': False, 'message': 'Invalid password. Passwords must have 8+ characters, at least 1 special symbol and 1 capital letter'}), 
                         ExpectedResponse(400, {'success': False, 'message': 'Invalid password. Passwords must have 8+ characters, at least 1 special symbol and 1 capital letter'}), 
                         ExpectedResponse(400, {'success': False, 'message': 'Invalid password. Passwords must have 8+ characters, at least 1 special symbol and 1 capital letter'}), 
                         ExpectedResponse(400, {'success': False, 'message': 'Invalid password. Passwords must have 8+ characters, at least 1 special symbol and 1 capital letter'}), 
                         ExpectedResponse(400, {'success': False, 'message': 'Invalid password. Passwords must have 8+ characters, at least 1 special symbol and 1 capital letter'}), 
                         ExpectedResponse(400, {'success': False, 'message': 'Invalid password. Passwords must have 8+ characters, at least 1 special symbol and 1 capital letter'})
                        ]
    automator = TestAutomator('http://localhost:8080')
    automator.checkEnpoints(testEndpoints, expectedResponses, 'Sign Up')
    
    
