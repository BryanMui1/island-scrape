#!/usr/bin/env python3

### sample code that introduces the foundation to build loopable scripts for testing and navigation of the islands experiment simulator
### May or may not be working, but helpful to examine

################################################################################################################
## IMPORTS
################################################################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import numpy as np
import pandas as pd

import time
import datetime

start_time = time.time()

################################################################################################################
## LOGIN
################################################################################################################

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://islands.smp.uq.edu.au/login.php")

#driver.implicitly_wait(1)

email = driver.find_elements(by=By.TAG_NAME, value="input")

login = open('passwords.config', 'r')
usrpass = [line.rstrip('\n') for line in login]


email[0].send_keys(usrpass[1])
email[1].send_keys(usrpass[2])

email[2].click()

logURL = "https://islands.smp.uq.edu.au/index.php"

assert(driver.current_url == logURL)

#exit()

################################################################################################################
## FIND CITY BUTTONS 
################################################################################################################

cities = driver.find_elements(By.XPATH, '//a[starts-with(@href, "village")]')
num_cities = len(cities)

# for i in cities:
#     print(i.text)

buttons = []
for j in cities:
    buttons.append(j.find_element(By.XPATH, './/div[starts-with(@class, "town town")]'))
    
# for button in buttons:
#     print("found " + button.text)

################################################################################################################
## FIND CITY BUTTONS 
################################################################################################################


#for i in range(num_cities):

buttons[0].click()
driver.implicitly_wait(1)


#print(len(houses))


# for house in houses:
#     id = house.find_element(By.CLASS_NAME, "houseid")
#     print(id.text)

#print(len(ids))

# for id in ids:
#     print(id.text)

### example of clicking on a house
#houses[23].click()

################################################################################################################
## ENUMERATE INDICES
################################################################################################################

houses = driver.find_elements(By.CLASS_NAME, "house")

ids = driver.find_elements(By.CLASS_NAME, "houseid")

### get rid of bad indices
badindx = []
for i in range(len(ids)):
    txt = ids[i].text
    if len(txt) == 0 or not txt.isnumeric():
        badindx.append(i)

### get the good indices
indxgood = list(range(0, len(ids)))

for i in sorted(badindx, reverse=True):
    indxgood.pop(i)

################################################################################################################
## SCRAPE RESIDENT INFORMATION
################################################################################################################

"""
## Task 1: Get a list of population names and age
actions = ActionChains(driver)

for i in indxgood:
    houses = driver.find_elements(By.CLASS_NAME, "house")
    houses[i].click()
    driver.implicitly_wait(1)
    close = driver.find_element(By.XPATH, '//label[starts-with(@class, "modal__close")]')
    
    #acquire some meaningful information
    residents = driver.find_elements(By.XPATH, '//a[starts-with(@href, "islander.php")]')
    houseinfo = driver.find_element(By.ID, 'houseinfo')

    print(houseinfo.text)

    # print(houseinfo.text)
    # for j in range(len(residents)):
    #     residents = driver.find_elements(By.XPATH, '//a[starts-with(@href, "islander.php")]') 
    #     residents[j].click()
    #     driver.back()

    actions.move_to_element(close).click().perform()
"""
## Task 2: Touch every person's profile

# error checking: keep track of house num and people touched
pop_total = 0
people_touched = 0

actions = ActionChains(driver)
ctrl_click = ActionChains(driver)
for i in indxgood:
    # open the desired house
    houses = driver.find_elements(By.CLASS_NAME, "house")
    houses[i].click()
    driver.implicitly_wait(1)
    
    ### DO SOMETHING

    ## open the every person in the house
    resident_links = driver.find_elements(By.XPATH, '//a[starts-with(@href, "islander.php")]')
    num_residents = len(resident_links)
    pop_total+=num_residents
    for n in range(num_residents):
        ctrl_click.move_to_element(resident_links[n])
        ctrl_click.key_down(Keys.CONTROL)
        ctrl_click.click()
        ctrl_click.perform()

    for _ in range(num_residents):
        driver.implicitly_wait(1)
        driver.switch_to.window(driver.window_handles[-1])
        
        ### touch the person ###
        isl = driver.find_element(By.ID, "title")
        print("touched " + isl.text)
        people_touched+=1

        driver.close()
    ## move to the next house

    ### DONE

    ### close window 
    driver.switch_to.window(driver.window_handles[0])
    close = driver.find_element(By.XPATH, '//label[starts-with(@class, "modal__close")]')
    actions.move_to_element(close).click().perform()

# assert error checking that we touched everyone
print(people_touched)
print(pop_total)
assert(people_touched == pop_total)

end_time = time.time()

if __name__ == '__main__':
    execution_time = end_time - start_time
    print("Script completed normally.")
    print("Script runtime: " + str(datetime.timedelta(seconds=execution_time)))
    time.sleep(15)
    driver.close()
