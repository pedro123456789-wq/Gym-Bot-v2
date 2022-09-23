import requests



class ExpectedResponse:
    def __init__(self, statusCode, content):
        self.statusCode = statusCode
        self.content = content



class EndpointRequest:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers



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
        totalTests = len(endpoints)

        print('<--- Automated Tests --->')
        print(f'Performing {len(endpoints)} tests on {baseUrl}/{endpointName}')


        for endpointRequest, expectedResponse in zip(endpointRequests, expectedResponses):
            response = requests.get(url = f'{self.baseUrl}/{endpointRequest.url}', headers = endpointRequest.headers)
            statusCode = response.status_code
            content = response.content

            if statusCode == expectedResponse.statusCode and content == expectedResponse.content:
                passed += 1
                print(f'Passed test #{testId}')
            else:
                failed += 1
                print(f'Failed test #{testId}')

            testId += 1

        print(f'Tests passed: {passed}/{totalTests}')
        print(f'Tests failed: {failed}/{totalTests}')
        print('<----   ---->')




if __name__ == '__main__':
    #sign-up tests
    pass 
