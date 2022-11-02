import requests
from time import sleep
from datetime import datetime


def homePageAttack(url, requestNumber, interval):
    for _ in range(requestNumber):
        resp = requests.get(url)
        sleep(interval)

    #check if webpage is still up and running
    checkResp = requests.get(url)

    if checkResp.ok:
        return True 
    else:
        return False



def slowLorrisAttack(self, url):
    pass 
