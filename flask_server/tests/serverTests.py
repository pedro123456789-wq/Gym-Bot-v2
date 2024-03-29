import requests
from time import time
from json import dumps


class ExpectedResponse:
    def __init__(self, statusCode, content):
        self.statusCode = statusCode
        self.content = content


class EndpointRequest:
    def __init__(self, url, headers, method, useJson=False):
        self.url = url
        self.headers = headers
        self.method = method
        self.useJson = useJson


class TestAutomator:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.successful = 0
        self.failed = 0
        self.averageResponseTime = 0

    def checkEnpoints(self, endpointRequests, expectedResponses, endpointName='Enpoint'):
        passed = 0
        failed = 0
        testId = 1
        totalTests = len(endpointRequests)
        totalDuration = 0

        print('<--- Automated Tests --->')
        print(
            f'Performing {len(endpointRequests)} tests on {self.baseUrl}/{endpointName}\n\n')

        for endpointRequest, expectedResponse in zip(endpointRequests, expectedResponses):
            method = endpointRequest.method

            startTime = time()
            if method != 'GET':
                response = requests.request(
                    method=endpointRequest.method, url=f'{self.baseUrl}/{endpointRequest.url}', json=endpointRequest.headers)
            else:
                if endpointRequest.useJson:
                    response = requests.request(
                        method=endpointRequest.method, url=f'{self.baseUrl}/{endpointRequest.url}', json=endpointRequest.headers)
                else:
                    response = requests.request(
                        method=endpointRequest.method, url=f'{self.baseUrl}/{endpointRequest.url}', headers=endpointRequest.headers)

            statusCode = response.status_code
            content = response.json()
            duration = time() - startTime

            # token is randomly generated so cannot be predicted. Comparing given token to it will cause
            # tests to fail incorrectly

            if 'token' in content:
                content.pop('token')

            if statusCode == expectedResponse.statusCode and content == expectedResponse.content:
                passed += 1
                print(f'Passed test #{testId} in {duration}s')
            else:
                failed += 1
                print(f'Failed test #{testId}')
                print(
                    f'Status Code: {statusCode}, expected: {expectedResponse.statusCode}')
                print(
                    f'Response: {content}, expected: {expectedResponse.content}')

            testId += 1
            totalDuration += duration

        print(f'\n\nTests passed: {passed}/{totalTests}')
        print(f'Time elapsed: {totalDuration}s')
        print('<----   ---->')


if __name__ == '__main__':
    pass 