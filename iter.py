#!/usr/bin/env python3

### Iteration script that goes through the entire island population
### Performs some task that is defined by the user

################################################################################################################
## IMPORTS
################################################################################################################


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time

import numpy as np
import pandas as pd

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

################################################################################################################
## ENUMERATE CONSTANTS
################################################################################################################

cities = driver.find_elements(By.XPATH, '//a[starts-with(@href, "village")]')
NUM_CITIES = len(cities)

buttons = []
for j in cities:
    buttons.append(j.find_element(By.XPATH, './/div[starts-with(@class, "town town")]'))

assert(len(buttons) == NUM_CITIES)

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

    





    ### END TASK//

    driver.back()
    driver.implicitly_wait(3)


if __name__ == '__main__':
    time.sleep(15)
    driver.close()