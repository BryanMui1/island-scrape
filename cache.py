#!/usr/bin/env python3

'''
caching function that stores all of the indices of cities

speeds up the lookup time drastically
'''

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

import pickle

start_time = time.time()

################################################################################################################
## LOGIN
################################################################################################################

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://islands.smp.uq.edu.au/login.php")

driver.implicitly_wait(1)

email = driver.find_elements(by=By.TAG_NAME, value="input")

login = open('passwords.config', 'r')
usrpass = [line.rstrip('\n') for line in login]


email[0].send_keys(usrpass[1])
email[1].send_keys(usrpass[2])

email[2].click()

logURL = "https://islands.smp.uq.edu.au/index.php"

assert(driver.current_url == logURL)


################################################################################################################
## ENUMERATE CONSTANTS AND DATA STRUCTURES
################################################################################################################

cities = driver.find_elements(By.XPATH, '//a[starts-with(@href, "village")]')
NUM_CITIES = len(cities)

buttons = []
for j in cities:
    buttons.append(j.find_element(By.XPATH, './/div[starts-with(@class, "town town")]'))

assert(len(buttons) == NUM_CITIES)

# cache datastructure
cache = []


################################################################################################################
## ITERATE
################################################################################################################

for cityindex in range(NUM_CITIES):
    #reprocess island page
    cities = driver.find_elements(By.XPATH, '//a[starts-with(@href, "village")]')
    buttons = []
    for j in cities:
        buttons.append(j.find_element(By.XPATH, './/div[starts-with(@class, "town town")]'))
    buttons[cityindex].click()
    driver.implicitly_wait(3)

    ### PERFORM SOME TASK HERE ###
    isl = driver.find_element(By.ID, "title")
    print("touched " + isl.text)

    houses = driver.find_elements(By.CLASS_NAME, "house")

    ids = driver.find_elements(By.CLASS_NAME, "houseid")

    hashid = {}
    trueindics = np.array(range(0, len(ids)))
    houseids = np.array([id.text for id in ids])
    setids = set(houseids)

    for house, indic in zip(houseids, trueindics):
        hashid[house] = int(indic)

    ### find the number of houses 
    NUM_HOUSES = houseids[-1]

    cache.append(hashid)

    ### END TASK//

    driver.back()
    driver.implicitly_wait(3)


print("cities cached: " + str(len(cache)))

# save the cache into a file
file = open(r'cache', 'wb')
pickle.dump(cache, file)
file.close()


end_time = time.time()

if __name__ == '__main__':
    execution_time = end_time - start_time
    print("Script completed normally.")
    print("Script runtime: " + str(datetime.timedelta(seconds=execution_time)))

    time.sleep(10)
    driver.close()
