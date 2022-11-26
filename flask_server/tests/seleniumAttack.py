from time import sleep

from selenium import webdriver
from password import PASSWORD

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get('http://localhost:3000/log-in')
    
    sleep(2)
    
    # login
    driver.find_element_by_xpath('/html/body/div/div/div/div/div[2]/form/div/div[1]/div/div/input').send_keys('pedro') #enter username
    driver.find_element_by_xpath('/html/body/div/div/div/div/div[2]/form/div/div[2]/div/div/input').send_keys(PASSWORD) #enter password
    sleep(0.5)
    driver.find_element_by_xpath('/html/body/div/div/div/div/div[2]/form/div/div[3]/input').click() #click login button 
    sleep(5)
    
    # perform test
    clickNumber = 500
    intervalSeconds = 0.3
    missedClicks = 0
    
    for _ in range(clickNumber):
        try:
            driver.find_element_by_xpath('/html/body/div[1]/div/div/nav/div[2]/div/div/div[2]/ul/div[5]').click() #click on insights button in sidebar
            sleep(0.1)
            driver.find_element_by_xpath('/html/body/div[1]/div/div/nav/div[2]/div/div/div[2]/ul/div[1]').click() #click on dashboard button in sidebar
            sleep(intervalSeconds)
        except:
            pass 
            
        
    
    